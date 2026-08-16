#!/usr/bin/env python3
"""Solver-free audit of selected row-merge topology-compression refutations."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .analyze_row_merge_q4_distance3_exchange import (
        exchange_chain_partitions,
    )
    from .anneal import atomic_json
    from .decide_row_merge_q4_small_step_pivot import pair_pivots
    from .decide_row_merge_single_wall_radius import (
        literal_graph,
        make_bundles,
        matching_count,
    )
    from .run_row_merge_q4_exchange_chain_cegar import complete_audit
except ImportError:
    from analyze_row_merge_q4_distance3_exchange import exchange_chain_partitions
    from anneal import atomic_json
    from decide_row_merge_q4_small_step_pivot import pair_pivots
    from decide_row_merge_single_wall_radius import (
        literal_graph,
        make_bundles,
        matching_count,
    )
    from run_row_merge_q4_exchange_chain_cegar import complete_audit


SCHEMA = "row-merge-q4-topology-mining-gate-audit-v1"
GATE_SCHEMA = "row-merge-q4-cycle023-gate-v1"
ANALYSIS_SCHEMA = "row-merge-q4-chain-trace-analysis-v1"
N = 4
M = 9
FIXED_GRAPH = (
    (False, True, True, False),
    (False, True, False, True),
    (False, True, True, False),
    (False, True, False, True),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def values_sha256(values) -> str:
    payload = json.dumps(values, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def audit_gate(path: Path) -> dict:
    gate = json.loads(path.read_text())
    if (
        gate.get("schema") != GATE_SCHEMA
        or gate.get("solver_status") != "sat"
        or not gate.get("status", "").endswith("REFUTATION_FOUND")
        or gate.get("integer_upper") != 20
        or gate.get("n") != N
        or gate.get("m") != M
        or tuple(tuple(row) for row in gate.get("fixed_post_wall_graph", ()))
        != FIXED_GRAPH
    ):
        raise AssertionError(f"invalid promoted gate: {path}")
    sizes = (2, 1, 2, 3)
    original, w, critical_good, _m = make_bundles(sizes)
    wall = tuple(tuple(row) for row in gate["wall_values"])
    post = tuple(tuple(row) for row in gate["post_wall_values"])
    if len(wall) != N or any(len(row) != M for row in wall):
        raise AssertionError("valuation dimensions changed")
    if any(not 1 <= value <= 20 for row in wall for value in row):
        raise AssertionError("wall value left the exact integer cap")
    epsilon = post[0][w[0]] - wall[0][w[0]]
    if epsilon <= 0:
        raise AssertionError("wall step is not positive")
    expected_post = tuple(
        tuple(
            value + epsilon if agent == 0 and good == w[0] else value
            for good, value in enumerate(row)
        )
        for agent, row in enumerate(wall)
    )
    if post != expected_post:
        raise AssertionError("post-wall matrix is not the claimed one-entry step")
    if sum(wall[0][good] for good in original[0]) != sum(
        wall[0][good] for good in w
    ):
        raise AssertionError("wall equality failed")
    if not wall[0][critical_good] < wall[0][w[0]]:
        raise AssertionError("critical-good order failed")
    if any(epsilon >= wall[0][good] for bundle in original[2:] for good in bundle):
        raise AssertionError("small-step premise failed")
    wall_graph = literal_graph(wall, original)
    if any(not wall_graph[agent][agent] for agent in range(N)):
        raise AssertionError("wall partition lost its identity EFX allocation")
    if literal_graph(post, original) != FIXED_GRAPH:
        raise AssertionError("decoded post-wall graph changed")

    base = pair_pivots(original, w, critical_good, complete_bundle_menu=True)
    if len(base) != gate["base_pivot_partition_count"]:
        raise AssertionError("base-pivot count changed")
    if gate["base_pivots_blocked"] and any(
        matching_count(literal_graph(post, partition)) for partition in base
    ):
        raise AssertionError("a blocked base pivot supports EFX")

    menu = gate.get("topology_cover_partitions")
    if menu is None:
        menu = gate.get("path_partitions")
    if menu is None:
        menu = gate.get("cycle_partitions")
    menu = tuple(tuple(tuple(bundle) for bundle in partition) for partition in menu)
    declared_count = (
        gate.get("topology_cover_partition_count")
        or gate.get("path_partition_count")
        or gate.get("cycle_partition_count")
    )
    if len(menu) != declared_count or len(set(menu)) != len(menu):
        raise AssertionError("selected menu count changed")
    if any(matching_count(literal_graph(post, partition)) for partition in menu):
        raise AssertionError("a selected-menu partition supports EFX")
    if len(set(menu) | set(base)) != gate["combined_partition_count"]:
        raise AssertionError("combined menu count changed")

    chain = exchange_chain_partitions(original, 3)
    chain_support_count = sum(
        bool(matching_count(literal_graph(post, partition))) for partition in chain
    )
    if chain_support_count != gate["simple_chain_support_count"]:
        raise AssertionError("full chain-support count changed")
    global_audit = complete_audit(post, original)
    if global_audit != gate["complete_efx_audit"]:
        raise AssertionError("complete EFX audit changed")
    formula_path = Path(gate["formula"])
    if sha256(formula_path) != gate["formula_sha256"]:
        raise AssertionError("formula hash changed")
    cover_source = gate.get("topology_cover_source")
    if cover_source is not None and sha256(Path(cover_source)) != gate.get(
        "topology_cover_source_sha256"
    ):
        raise AssertionError("topology-cover source hash changed")
    return {
        "path": str(path),
        "sha256": sha256(path),
        "status": gate["status"],
        "menu_kind": gate["menu_kind"],
        "selected_partition_count": declared_count,
        "combined_partition_count": gate["combined_partition_count"],
        "simple_chain_support_count": chain_support_count,
        "complete_efx_allocation_count": global_audit["allocation_count"],
        "post_values_sha256": values_sha256(gate["post_wall_values"]),
        "formula_sha256": gate["formula_sha256"],
    }


def run(analysis_path: Path, gate_paths: tuple[Path, ...], output_path: Path) -> None:
    if output_path.exists():
        raise ValueError("output must be new")
    analysis = json.loads(analysis_path.read_text())
    if (
        analysis.get("schema") != ANALYSIS_SCHEMA
        or analysis.get("status") != "EXACT_TRACE_MOTIFS_CLASSIFIED"
        or analysis.get("sat_model_count") != 23
        or analysis.get("minimum_topology_cover_size") != 2
        or analysis.get("minimum_topology_cover_partition_count") != 24
        or analysis.get("universal_action_count") != 0
        or analysis.get("universal_partition_count") != 0
        or tuple(tuple(row) for row in analysis.get("fixed_post_wall_graph", ()))
        != FIXED_GRAPH
    ):
        raise AssertionError("final topology analysis changed")
    for model in analysis["models"]:
        trace_path = Path(model["trace"])
        if sha256(trace_path) != model["trace_sha256"]:
            raise AssertionError("a trace hash changed")
    audited_gates = [audit_gate(path) for path in gate_paths]
    result = {
        "schema": SCHEMA,
        "status": "SELECTED_TOPOLOGY_COMPRESSIONS_REFUTED_AT_CAP20",
        "domain": (
            "positive additive integer wall valuations in 1..20 in the fixed "
            "four-agent, nine-good Hall-size-four graph cell"
        ),
        "analysis": str(analysis_path),
        "analysis_sha256": sha256(analysis_path),
        "sat_model_count": analysis["sat_model_count"],
        "minimum_topology_cover_size_after_two_refutations": analysis[
            "minimum_topology_cover_size"
        ],
        "minimum_topology_cover_partition_count_after_two_refutations": analysis[
            "minimum_topology_cover_partition_count"
        ],
        "universal_existential_signatures": analysis[
            "universal_existential_signatures"
        ],
        "audited_refutations": audited_gates,
        "interpretation": (
            "All one-good three-cycle repairs, all simple paths starting at "
            "the three-good bundle, and two successive minimum two-topology "
            "covers are exactly refuted even when combined with the sixteen "
            "base pivots. Every refuting profile still has complete EFX "
            "allocations and other simple-chain repairs."
        ),
        "claim_boundary": (
            "This refutes only the listed topology-compressed repair menus at "
            "the stated integer cap. It does not refute the full 515-partition "
            "exchange-chain candidate, row-merge continuation, or complete EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--gate", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.analysis, tuple(args.gate), args.output)


if __name__ == "__main__":
    main()
