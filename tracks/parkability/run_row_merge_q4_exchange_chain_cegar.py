#!/usr/bin/env python3
"""CEGAR for a simple exchange-chain repair at a q=4 row-merge wall."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import z3

try:
    from .analyze_row_merge_q4_distance3_exchange import (
        exchange_chain_partitions,
    )
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import (
        canonical,
        transfer_distance,
    )
    from .core import iter_unlabeled_nonempty_partitions
    from .decide_row_merge_q4_small_step_pivot import pair_pivots
    from .decide_row_merge_single_wall_radius import (
        as_fraction,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        zsum,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from analyze_row_merge_q4_distance3_exchange import (
        exchange_chain_partitions,
    )
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import canonical, transfer_distance
    from core import iter_unlabeled_nonempty_partitions
    from decide_row_merge_q4_small_step_pivot import pair_pivots
    from decide_row_merge_single_wall_radius import (
        as_fraction,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        zsum,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "row-merge-q4-exchange-chain-cegar-v1"
N = 4


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def complete_audit(post_values, original):
    support_count = 0
    allocation_count = 0
    histogram = Counter()
    nearest = None
    for candidate in iter_unlabeled_nonempty_partitions(N, len(post_values[0])):
        count = matching_count(literal_graph(post_values, candidate))
        if not count:
            continue
        distance = transfer_distance(canonical(original), candidate)
        support_count += 1
        allocation_count += count
        histogram[distance] += 1
        if nearest is None or (distance, candidate) < nearest:
            nearest = (distance, candidate)
    return {
        "supporting_partition_count": support_count,
        "allocation_count": allocation_count,
        "minimum_transfer_distance": nearest[0] if nearest else None,
        "nearest_partition": (
            [list(bundle) for bundle in nearest[1]] if nearest else None
        ),
        "distance_histogram": {
            str(distance): histogram[distance] for distance in sorted(histogram)
        },
    }


def add_partition_obstruction(solver, edges, prefix, encoding):
    if encoding == "matching_clauses":
        solver.add(z3.Not(has_matching_expression(edges)))
        return
    if encoding != "hall_selectors":
        raise ValueError("unknown partition-obstruction encoding")
    selectors = []
    for observer_mask in range(1, 1 << N):
        observers = tuple(
            observer
            for observer in range(N)
            if observer_mask & (1 << observer)
        )
        if len(observers) == 1:
            continue
        selector = z3.Bool(f"{prefix}_hall_{observer_mask}")
        selectors.append(selector)
        neighborhood = tuple(
            z3.Or(*(edges[observer][bundle] for observer in observers))
            for bundle in range(N)
        )
        for forbidden in itertools.combinations(neighborhood, len(observers)):
            solver.add(
                z3.Implies(
                    selector,
                    z3.Or(*(z3.Not(neighbor) for neighbor in forbidden)),
                )
            )
    solver.add(z3.Or(*selectors))


def run(
    result_path: Path,
    formula_path: Path,
    d_size: int,
    maximum_chain_length: int,
    max_rounds: int,
    add_per_round: int,
    per_check_limit: float,
    obstruction_encoding: str,
    integer_upper: int | None = None,
    seed_analysis_path: Path | None = None,
    warm_source_path: Path | None = None,
    warm_cut_limit: int | None = None,
    extra_warm_source_paths: tuple[Path, ...] = (),
    fixed_graph_source_path: Path | None = None,
    repair_menu_kind: str = "all_chain",
    fix_wall_graph: bool = False,
) -> None:
    if result_path.exists() or formula_path.exists():
        raise ValueError("result and formula outputs must be new")
    if (
        d_size < 1
        or maximum_chain_length < 1
        or maximum_chain_length > 3
        or max_rounds < 1
        or add_per_round < 1
        or per_check_limit <= 0
        or obstruction_encoding not in {"matching_clauses", "hall_selectors"}
        or repair_menu_kind not in {"all_chain", "hamiltonian_paths"}
        or (integer_upper is not None and integer_upper < 1)
    ):
        raise ValueError("invalid CEGAR parameters")
    sizes = (2, 1, 2, d_size)
    original, w, critical_good, m = make_bundles(sizes)
    u = original[0]
    small_step_goods = tuple(good for bundle in original[2:] for good in bundle)
    full_universe = exchange_chain_partitions(original, maximum_chain_length)
    if repair_menu_kind == "hamiltonian_paths":
        if maximum_chain_length != 3:
            raise ValueError("Hamiltonian paths require maximum chain length three")
        try:
            from .analyze_row_merge_q4_chain_trace import actions_by_partition
        except ImportError:
            from analyze_row_merge_q4_chain_trace import actions_by_partition
        hamiltonian = {
            partition
            for partition, actions in actions_by_partition().items()
            if any(
                action["kind"] == "path" and action["length"] == N - 1
                for action in actions
            )
        }
        universe = tuple(
            partition for partition in full_universe if partition in hamiltonian
        )
        if len(universe) != 264:
            raise AssertionError("Hamiltonian-path repair menu changed")
    else:
        universe = full_universe
    universe_set = set(universe)

    master = ParkabilityLRAMaster(N, m, integer_upper=integer_upper)
    solver = master.solver
    wall_rows = master.values
    epsilon = (
        z3.Int("wall_epsilon")
        if integer_upper is not None
        else z3.Real("wall_epsilon")
    )
    solver.add(epsilon > 0)
    perturb_good = w[0]
    post_row = tuple(
        value + epsilon if good == perturb_good else value
        for good, value in enumerate(wall_rows[0])
    )
    post_rows = (post_row, *wall_rows[1:])

    solver.add(zsum(wall_rows[0], u) == zsum(wall_rows[0], w))
    solver.add(wall_rows[0][critical_good] < wall_rows[0][w[0]])
    for target_index, target in enumerate(original):
        if target_index == 0:
            continue
        for removed in target:
            remainder = tuple(good for good in target if good != removed)
            if target_index == 1 and removed == critical_good:
                continue
            solver.add(zsum(wall_rows[0], u) > zsum(wall_rows[0], remainder))
    solver.add(
        *(epsilon < wall_rows[0][good] for good in small_step_goods)
    )

    wall_edges = edge_matrix(solver, wall_rows, original, "wall_original")
    post_edges = edge_matrix(solver, post_rows, original, "post_original")
    solver.add(*(wall_edges[agent][agent] for agent in range(N)))
    solver.add(z3.Not(post_edges[0][0]))
    deficient_bundles = tuple(range(1, N))
    for agent in range(N):
        solver.add(z3.Not(post_edges[agent][0]))
    for size in range(1, N):
        for agents in itertools.combinations(range(N), size):
            solver.add(
                has_matching_expression(post_edges, agents, deficient_bundles)
            )

    active = []
    active_set = set()

    def add_partition(partition):
        if partition in active_set:
            return
        index = len(active)
        edges = edge_matrix(solver, post_rows, partition, f"chain_cut_{index}")
        add_partition_obstruction(
            solver,
            edges,
            f"chain_cut_{index}",
            obstruction_encoding,
        )
        active.append(partition)
        active_set.add(partition)

    base_initial = pair_pivots(
        original,
        w,
        critical_good,
        complete_bundle_menu=True,
    )
    if repair_menu_kind == "all_chain" and any(
        partition not in universe_set for partition in base_initial
    ):
        raise AssertionError("a pair pivot lies outside the chain menu")
    for partition in base_initial:
        add_partition(partition)

    seed_analysis_sha256 = None
    seed_partition_count = 0
    if seed_analysis_path is not None:
        seed = json.loads(seed_analysis_path.read_text())
        if (
            seed.get("schema")
            != "row-merge-q4-distance-three-exchange-analysis-v1"
            or seed.get("m") != m
            or seed.get("wall_partition")
            != [list(bundle) for bundle in original]
        ):
            raise ValueError("seed analysis describes a different chain cell")
        seed_analysis_sha256 = sha256(seed_analysis_path)
        for record in seed["supporting_simple_exchange_chain_partitions"]:
            partition = tuple(tuple(bundle) for bundle in record["partition"])
            if partition not in universe_set:
                raise AssertionError("a seeded partition lies outside the chain menu")
            before = len(active)
            add_partition(partition)
            seed_partition_count += len(active) - before

    warm_source_sha256 = None
    warm_partition_count = 0
    warm = None
    if warm_source_path is not None:
        warm = json.loads(warm_source_path.read_text())
        if (
            warm.get("schema") != SCHEMA
            or warm.get("m") != m
            or warm.get("maximum_chain_length") != maximum_chain_length
            or warm.get("wall_partition")
            != [list(bundle) for bundle in original]
            or warm.get("repair_menu_kind", "all_chain") != repair_menu_kind
        ):
            raise ValueError("warm source describes a different chain cell")
        warm_source_sha256 = sha256(warm_source_path)
        warm_partitions = [
            raw_partition
            for warm_round in warm["rounds"]
            for raw_partition in warm_round.get("learned_partitions", ())
        ]
        if warm_cut_limit is not None:
            if warm_cut_limit < 0:
                raise ValueError("warm cut limit must be nonnegative")
            warm_partitions = warm_partitions[:warm_cut_limit]
        for raw_partition in warm_partitions:
            partition = tuple(tuple(bundle) for bundle in raw_partition)
            if partition not in universe_set:
                raise AssertionError("a warm partition lies outside the chain menu")
            before = len(active)
            add_partition(partition)
            warm_partition_count += len(active) - before

    extra_warm_sources = []
    extra_warm_partition_count = 0
    for extra_path in extra_warm_source_paths:
        extra = json.loads(extra_path.read_text())
        if (
            extra.get("schema") != SCHEMA
            or extra.get("m") != m
            or extra.get("maximum_chain_length") != maximum_chain_length
            or extra.get("wall_partition")
            != [list(bundle) for bundle in original]
            or extra.get("repair_menu_kind", "all_chain") != repair_menu_kind
        ):
            raise ValueError("extra warm source describes a different chain cell")
        before_source = len(active)
        for extra_round in extra["rounds"]:
            for raw_partition in extra_round.get("learned_partitions", ()):
                candidate = tuple(tuple(bundle) for bundle in raw_partition)
                if candidate not in universe_set:
                    raise AssertionError(
                        "an extra warm partition lies outside the chain menu"
                    )
                add_partition(candidate)
        added = len(active) - before_source
        extra_warm_partition_count += added
        extra_warm_sources.append(
            {"path": str(extra_path), "sha256": sha256(extra_path), "added": added}
        )

    fixed_graph = None
    fixed_graph_source_sha256 = None
    if fixed_graph_source_path is not None:
        fixed_source = (
            warm
            if fixed_graph_source_path == warm_source_path and warm is not None
            else json.loads(fixed_graph_source_path.read_text())
        )
        if (
            fixed_source.get("schema") != SCHEMA
            or fixed_source.get("m") != m
            or fixed_source.get("wall_partition")
            != [list(bundle) for bundle in original]
        ):
            raise ValueError("fixed-graph source describes a different chain cell")
        sat_rounds = [
            record
            for record in fixed_source["rounds"]
            if record.get("solver_status") == "sat"
        ]
        if not sat_rounds:
            raise ValueError("fixed-graph source has no SAT model")
        fixed_wall_values = tuple(
            tuple(row) for row in sat_rounds[-1]["wall_values"]
        )
        fixed_values = tuple(
            tuple(row) for row in sat_rounds[-1]["post_wall_values"]
        )
        fixed_wall_graph = literal_graph(fixed_wall_values, original)
        fixed_graph = literal_graph(fixed_values, original)
        for agent in range(N):
            for bundle in range(N):
                solver.add(post_edges[agent][bundle] == fixed_graph[agent][bundle])
                if fix_wall_graph:
                    solver.add(
                        wall_edges[agent][bundle]
                        == fixed_wall_graph[agent][bundle]
                    )
        fixed_graph_source_sha256 = sha256(fixed_graph_source_path)

    started = time.time()
    rounds = []
    terminal_values = None
    status = z3.unknown
    for round_index in range(max_rounds):
        solver.set(timeout=int(per_check_limit * 1000))
        check_started = time.time()
        status = solver.check()
        record = {
            "round": round_index,
            "cuts_before_solve": len(active),
            "solver_status": str(status),
            "solver_wall_seconds": time.time() - check_started,
        }
        if status != z3.sat:
            record["reason_unknown"] = (
                solver.reason_unknown() if status == z3.unknown else None
            )
            rounds.append(record)
            break

        model = solver.model()
        wall_fractions = tuple(
            tuple(as_fraction(model, value) for value in row) for row in wall_rows
        )
        post_fractions = tuple(as_fraction(model, value) for value in post_row)
        wall_values, post_values_row = primitive_rows(
            wall_fractions, post_fractions
        )
        post_values = (post_values_row, *wall_values[1:])
        supports = tuple(
            (partition, matching_count(literal_graph(post_values, partition)))
            for partition in universe
        )
        supports = tuple(record for record in supports if record[1])
        new_supports = tuple(
            record for record in supports if record[0] not in active_set
        )
        record.update(
            {
                "wall_values": [list(row) for row in wall_values],
                "post_wall_values": [list(row) for row in post_values],
                "chain_support_count": len(supports),
                "new_chain_support_count": len(new_supports),
                "new_chain_supporting_allocation_count": sum(
                    count for _partition, count in new_supports
                ),
            }
        )
        if not new_supports:
            terminal_values = (wall_values, post_values)
            rounds.append(record)
            break
        learned = new_supports[:add_per_round]
        for partition, _count in learned:
            add_partition(partition)
        record["learned_partition_count"] = len(learned)
        record["cuts_after_learning"] = len(active)
        record["learned_partitions"] = [
            [list(bundle) for bundle in partition]
            for partition, _count in learned
        ]
        rounds.append(record)
    else:
        status = z3.unknown

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    if status == z3.unsat:
        final_status = "EXCHANGE_CHAIN_CELL_VERIFIED"
    elif terminal_values is not None:
        final_status = "EXCHANGE_CHAIN_REFUTATION_FOUND"
    else:
        final_status = "CEGAR_INCOMPLETE"
    terminal_audit = (
        complete_audit(terminal_values[1], original)
        if terminal_values is not None
        else None
    )
    result = {
        "schema": SCHEMA,
        "status": final_status,
        "solver_status": str(status),
        "domain": (
            "positive additive integer wall valuations with each wall item "
            f"in 1..{integer_upper}; the perturbed post-wall entry may exceed "
            "the wall cap"
            if integer_upper is not None
            else "strictly positive additive real valuations"
        ),
        "n": N,
        "m": m,
        "wall_partition": [list(bundle) for bundle in original],
        "bundle_sizes_excluding_critical_good": list(sizes),
        "minimal_hall_witness_size": 4,
        "maximum_chain_length": maximum_chain_length,
        "repair_menu_kind": repair_menu_kind,
        "chain_partition_count": len(universe),
        "obstruction_encoding": obstruction_encoding,
        "integer_upper": integer_upper,
        "small_step_goods": list(small_step_goods),
        "base_initial_cut_count": len(base_initial),
        "seed_analysis": (
            str(seed_analysis_path) if seed_analysis_path is not None else None
        ),
        "seed_analysis_sha256": seed_analysis_sha256,
        "seed_partition_count": seed_partition_count,
        "warm_source": (
            str(warm_source_path) if warm_source_path is not None else None
        ),
        "warm_source_sha256": warm_source_sha256,
        "warm_cut_limit": warm_cut_limit,
        "warm_partition_count": warm_partition_count,
        "extra_warm_sources": extra_warm_sources,
        "extra_warm_partition_count": extra_warm_partition_count,
        "fixed_graph_source": (
            str(fixed_graph_source_path)
            if fixed_graph_source_path is not None
            else None
        ),
        "fixed_graph_source_sha256": fixed_graph_source_sha256,
        "fixed_post_wall_graph": (
            [list(row) for row in fixed_graph] if fixed_graph is not None else None
        ),
        "fixed_wall_graph": (
            [list(row) for row in fixed_wall_graph]
            if fixed_graph is not None and fix_wall_graph
            else None
        ),
        "wall_graph_fixed": fix_wall_graph,
        "initial_cut_count": (
            len(base_initial)
            + seed_partition_count
            + warm_partition_count
            + extra_warm_partition_count
        ),
        "final_cut_count": len(active),
        "round_count": len(rounds),
        "rounds": rounds,
        "terminal_wall_values": (
            [list(row) for row in terminal_values[0]]
            if terminal_values is not None
            else None
        ),
        "terminal_post_wall_values": (
            [list(row) for row in terminal_values[1]]
            if terminal_values is not None
            else None
        ),
        "terminal_complete_efx_audit": terminal_audit,
        "elapsed_seconds": time.time() - started,
        "max_rounds": max_rounds,
        "add_per_round": add_per_round,
        "per_check_time_limit_seconds": per_check_limit,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT proves that a partition in the stated exchange repair menu "
            "supports complete EFX in this exact wall cell."
            if status == z3.unsat
            else "SAT refutes the simple exchange-chain repair in this exact wall cell."
            if terminal_values is not None
            else (
                "The bounded exact-integer master reached its resource limit."
                if integer_upper is not None
                else "The exact-real master reached its bounded resource limit."
            )
        ),
        "claim_boundary": (
            (
                "A bounded-integer verdict applies only to the stated wall "
                "cap. "
                if integer_upper is not None
                else ""
            )
            + "This decides only the displayed small-step Hall-size-four cell; "
            "it is not general row-merge continuation or complete EFX."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--d-size", type=int, default=3)
    parser.add_argument("--maximum-chain-length", type=int, default=3)
    parser.add_argument("--max-rounds", type=int, default=20)
    parser.add_argument("--add-per-round", type=int, default=32)
    parser.add_argument("--per-check-limit", type=float, default=300)
    parser.add_argument(
        "--obstruction-encoding",
        choices=("matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument("--integer-upper", type=int)
    parser.add_argument("--seed-analysis", type=Path)
    parser.add_argument("--warm-source", type=Path)
    parser.add_argument("--warm-cut-limit", type=int)
    parser.add_argument("--extra-warm-source", type=Path, action="append", default=[])
    parser.add_argument("--fixed-graph-source", type=Path)
    parser.add_argument(
        "--repair-menu-kind",
        choices=("all_chain", "hamiltonian_paths"),
        default="all_chain",
    )
    parser.add_argument("--fix-wall-graph", action="store_true")
    args = parser.parse_args()
    run(
        args.result,
        args.formula,
        args.d_size,
        args.maximum_chain_length,
        args.max_rounds,
        args.add_per_round,
        args.per_check_limit,
        args.obstruction_encoding,
        args.integer_upper,
        args.seed_analysis,
        args.warm_source,
        args.warm_cut_limit,
        tuple(args.extra_warm_source),
        args.fixed_graph_source,
        args.repair_menu_kind,
        args.fix_wall_graph,
    )


if __name__ == "__main__":
    main()
