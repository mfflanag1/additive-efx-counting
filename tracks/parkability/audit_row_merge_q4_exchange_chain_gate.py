#!/usr/bin/env python3
"""Audit the open q=4 nine-good simple exchange-chain gate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .analyze_row_merge_q4_distance3_exchange import (
        exchange_chain_partitions,
    )
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import (
        canonical,
        graph,
        matching_count,
        transfer_distance,
    )
    from .core import iter_unlabeled_nonempty_partitions, validate_values
    from .decide_row_merge_q4_small_step_pivot import pair_pivots
    from .decide_row_merge_single_wall_radius import make_bundles
except ImportError:
    from analyze_row_merge_q4_distance3_exchange import (
        exchange_chain_partitions,
    )
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import (
        canonical,
        graph,
        matching_count,
        transfer_distance,
    )
    from core import iter_unlabeled_nonempty_partitions, validate_values
    from decide_row_merge_q4_small_step_pivot import pair_pivots
    from decide_row_merge_single_wall_radius import make_bundles


SCHEMA = "row-merge-q4-exchange-chain-gate-audit-v1"
N = 4
MATCHINGS = tuple(itertools.permutations(range(N)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_formula_record(path: Path, schema: str):
    record = json.loads(path.read_text())
    formula = Path(record["formula"])
    if (
        record.get("schema") != schema
        or not formula.is_file()
        or sha256(formula) != record["formula_sha256"]
    ):
        raise AssertionError(f"formula chain failed for {path}")
    return record


def partition(raw):
    return tuple(tuple(bundle) for bundle in raw)


def chain_supports(values, menu):
    return tuple(
        (candidate, matching_count(graph(values, candidate)))
        for candidate in menu
        if matching_count(graph(values, candidate))
    )


def hall_differential():
    checked = 0
    for row_masks in itertools.product(range(1, 1 << N), repeat=N):
        feasible = tuple(
            tuple(bool(mask & (1 << bundle)) for bundle in range(N))
            for mask in row_masks
        )
        has_matching = any(
            all(feasible[agent][matching[agent]] for agent in range(N))
            for matching in MATCHINGS
        )
        has_hall_obstruction = any(
            len(
                {
                    bundle
                    for agent in agents
                    for bundle in range(N)
                    if feasible[agent][bundle]
                }
            )
            < len(agents)
            for size in range(2, N + 1)
            for agents in itertools.combinations(range(N), size)
        )
        if has_matching == has_hall_obstruction:
            raise AssertionError("matching and Hall encodings disagree")
        checked += 1
    return checked


def run(
    analysis_path: Path,
    cegar_path: Path,
    normalization_path: Path,
    cvc5_path: Path,
    fixed56_path: Path,
    ladder8_path: Path,
    ladder4_path: Path,
    hall56_path: Path,
    output_path: Path,
) -> None:
    if output_path.exists():
        raise ValueError("output must be new")
    analysis = json.loads(analysis_path.read_text())
    if (
        analysis.get("schema")
        != "row-merge-q4-distance-three-exchange-analysis-v1"
        or analysis.get("status")
        != "DISTANCE_THREE_EXCHANGE_MOTIF_CLASSIFIED"
    ):
        raise AssertionError("exchange analysis has the wrong status")
    terminal_path = Path(analysis["source"])
    terminal = json.loads(terminal_path.read_text())
    if sha256(terminal_path) != analysis["source_sha256"]:
        raise AssertionError("exchange-analysis source hash changed")
    post = validate_values(
        terminal["terminal_post_wall_values"], expected_n=N, lower=1
    )
    base = partition(terminal["wall_partition"])
    menu = exchange_chain_partitions(base, 3)
    supports = chain_supports(post, menu)
    global_support_count = 0
    nearest_histogram = Counter()
    for candidate in iter_unlabeled_nonempty_partitions(N, 9):
        if not matching_count(graph(post, candidate)):
            continue
        global_support_count += 1
        nearest_histogram[transfer_distance(canonical(base), candidate)] += 1
    if (
        len(menu) != 515
        or len(supports) != 8
        or any(transfer_distance(canonical(base), item[0]) != 3 for item in supports)
        or global_support_count != 123
        or nearest_histogram != Counter({3: 20, 4: 62, 5: 41})
    ):
        raise AssertionError("the terminal exchange classification changed")

    cegar = load_formula_record(
        cegar_path, "row-merge-q4-exchange-chain-cegar-v1"
    )
    original, w, critical_good, _m = make_bundles((2, 1, 2, 3))
    base_initial = set(
        pair_pivots(original, w, critical_good, complete_bundle_menu=True)
    )
    seed_initial = {
        partition(record["partition"])
        for record in analysis["supporting_simple_exchange_chain_partitions"]
    }
    first_model = validate_values(
        cegar["rounds"][0]["post_wall_values"], expected_n=N, lower=1
    )
    first_supports = chain_supports(first_model, menu)
    learned32 = tuple(
        partition(raw) for raw in cegar["rounds"][0]["learned_partitions"]
    )
    if (
        cegar.get("status") != "CEGAR_INCOMPLETE"
        or cegar.get("initial_cut_count") != 24
        or cegar.get("final_cut_count") != 56
        or cegar["rounds"][0].get("solver_status") != "sat"
        or cegar["rounds"][0].get("chain_support_count") != 48
        or cegar["rounds"][1].get("solver_status") != "unknown"
        or len(base_initial) != 16
        or len(seed_initial) != 8
        or any(
            matching_count(graph(first_model, candidate))
            for candidate in base_initial | seed_initial
        )
        or len(first_supports) != 48
        or len(learned32) != 32
        or any(not matching_count(graph(first_model, candidate)) for candidate in learned32)
    ):
        raise AssertionError("the 24-to-56 matching-clause trace changed")

    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    normalized_formula = Path(normalization["output"])
    if (
        normalization.get("schema") != "strict-smt2-normalization-v1"
        or normalization.get("source_sha256") != cegar["formula_sha256"]
        or not normalized_formula.is_file()
        or sha256(normalized_formula) != normalization["output_sha256"]
        or cvc5.get("schema") != "external-smt-replay-v1"
        or cvc5.get("formula_sha256") != normalization["output_sha256"]
        or cvc5.get("verdict") is not None
        or cvc5.get("returncode") != -6
        or "timeout" not in cvc5.get("stderr", "")
        or cvc5.get("time_limit_seconds") != 300.0
    ):
        raise AssertionError("the independent cvc5 timeout chain changed")

    fixed56 = load_formula_record(
        fixed56_path, "row-merge-q4-exchange-chain-cegar-v1"
    )
    ladder8 = load_formula_record(
        ladder8_path, "row-merge-q4-exchange-chain-cegar-v1"
    )
    ladder4 = load_formula_record(
        ladder4_path, "row-merge-q4-exchange-chain-cegar-v1"
    )
    hall56 = load_formula_record(
        hall56_path, "row-merge-q4-exchange-chain-cegar-v1"
    )
    expected_graph = (
        (False, True, True, False),
        (False, True, False, True),
        (False, True, True, False),
        (False, True, False, True),
    )
    fixed_model = validate_values(
        ladder8["rounds"][0]["post_wall_values"], expected_n=N, lower=1
    )
    fixed_supports = chain_supports(fixed_model, menu)
    if (
        tuple(tuple(row) for row in fixed56["fixed_post_wall_graph"])
        != expected_graph
        or fixed56.get("initial_cut_count") != 56
        or fixed56["rounds"][0].get("solver_status") != "unknown"
        or fixed56["rounds"][0].get("reason_unknown") != "timeout"
        or ladder8.get("initial_cut_count") != 32
        or ladder8["rounds"][0].get("solver_status") != "sat"
        or ladder8["rounds"][0].get("chain_support_count") != 9
        or len(fixed_supports) != 9
        or graph(fixed_model, base) != expected_graph
        or ladder8["rounds"][1].get("cuts_before_solve") != 40
        or ladder8["rounds"][1].get("solver_status") != "unknown"
        or ladder4.get("initial_cut_count") != 32
        or ladder4["rounds"][0].get("solver_status") != "sat"
        or ladder4["rounds"][1].get("cuts_before_solve") != 36
        or ladder4["rounds"][1].get("solver_status") != "unknown"
        or hall56.get("obstruction_encoding") != "hall_selectors"
        or hall56.get("initial_cut_count") != 56
        or hall56["rounds"][0].get("solver_status") != "unknown"
        or hall56["rounds"][0].get("reason_unknown") != "timeout"
    ):
        raise AssertionError("the fixed-graph ladder changed")

    hall_graph_count = hall_differential()
    result = {
        "schema": SCHEMA,
        "status": "EXCHANGE_CHAIN_CANDIDATE_OPEN_AT_56_CUT_GATE",
        "analysis": str(analysis_path),
        "analysis_sha256": sha256(analysis_path),
        "terminal_source_sha256": sha256(terminal_path),
        "chain_partition_count": len(menu),
        "terminal_nearest_supporting_partition_count": 20,
        "terminal_supporting_chain_partition_count": len(supports),
        "global_24_cut_trace": str(cegar_path),
        "global_24_cut_trace_sha256": sha256(cegar_path),
        "global_24_cut_status": "sat",
        "global_24_cut_support_count": len(first_supports),
        "global_56_cut_z3_status": "unknown",
        "global_56_cut_cvc5_status": "timeout_without_verdict",
        "global_56_cut_formula_sha256": cegar["formula_sha256"],
        "global_56_cut_normalized_formula_sha256": normalization["output_sha256"],
        "fixed_post_wall_graph": [list(row) for row in expected_graph],
        "fixed_graph_32_cut_status": "sat",
        "fixed_graph_32_cut_support_count": len(fixed_supports),
        "fixed_graph_36_cut_status": "unknown",
        "fixed_graph_40_cut_status": "unknown",
        "fixed_graph_56_cut_matching_status": "unknown",
        "fixed_graph_56_cut_hall_status": "unknown",
        "nonempty_row_graph_encoding_differential_count": hall_graph_count,
        "matching_vs_hall_obstruction_encoding": "PASS",
        "interpretation": (
            "Simple paths and cycles of at most three one-good transfers form "
            "a compact 515-partition successor menu. The first two exact "
            "models retain respectively 48 and 9 repairs, but the strengthened "
            "56-cut cell remains undecided under two obstruction encodings and "
            "two exact solvers."
        ),
        "claim_boundary": (
            "This neither proves nor refutes the exchange-chain candidate, row-"
            "merge continuation, or general complete additive EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--cegar", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--fixed56", type=Path, required=True)
    parser.add_argument("--ladder8", type=Path, required=True)
    parser.add_argument("--ladder4", type=Path, required=True)
    parser.add_argument("--hall56", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.analysis,
        args.cegar,
        args.normalization,
        args.cvc5,
        args.fixed56,
        args.ladder8,
        args.ladder4,
        args.hall56,
        args.output,
    )


if __name__ == "__main__":
    main()
