#!/usr/bin/env python3
"""Solver-free audit of valuation-ranked Hamiltonian-path refutations."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .analyze_row_merge_q4_chain_trace import action_key, actions_by_partition
    from .anneal import atomic_json
    from .decide_row_merge_q4_small_step_pivot import pair_pivots
    from .decide_row_merge_single_wall_radius import (
        literal_graph,
        make_bundles,
        matching_count,
    )
    from .run_row_merge_q4_exchange_chain_cegar import complete_audit
    from .run_row_merge_q4_ranked_path_cegar import (
        hamiltonian_actions,
        selected_literal,
    )
except ImportError:
    from analyze_row_merge_q4_chain_trace import action_key, actions_by_partition
    from anneal import atomic_json
    from decide_row_merge_q4_small_step_pivot import pair_pivots
    from decide_row_merge_single_wall_radius import (
        literal_graph,
        make_bundles,
        matching_count,
    )
    from run_row_merge_q4_exchange_chain_cegar import complete_audit
    from run_row_merge_q4_ranked_path_cegar import hamiltonian_actions, selected_literal


SCHEMA = "row-merge-q4-ranked-path-gate-audit-v1"
GATE_SCHEMA = "row-merge-q4-ranked-path-cegar-v1"
MINING_SCHEMA = "row-merge-q4-valuation-selector-mining-v1"
N = 4
M = 9
FIXED_GRAPH = (
    (False, True, True, False),
    (False, True, False, True),
    (False, True, True, False),
    (False, True, False, True),
)
FIXED_WALL_GRAPH = (
    (True, True, True, False),
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
        or gate.get("status") != "RANKED_PATH_SELECTOR_REFUTATION_FOUND"
        or gate.get("solver_status") != "sat"
        or gate.get("integer_upper") != 20
        or gate.get("n") != N
        or gate.get("m") != M
        or tuple(tuple(row) for row in gate.get("fixed_post_wall_graph", ()))
        != FIXED_GRAPH
        or tuple(tuple(row) for row in gate.get("fixed_wall_graph", ()))
        != FIXED_WALL_GRAPH
    ):
        raise AssertionError(f"invalid ranked-path gate: {path}")
    original, w, critical_good, _m = make_bundles((2, 1, 2, 3))
    wall = tuple(tuple(row) for row in gate["wall_values"])
    post = tuple(tuple(row) for row in gate["post_wall_values"])
    if len(wall) != N or any(len(row) != M for row in wall):
        raise AssertionError("valuation dimensions changed")
    if any(not 1 <= value <= 20 for row in wall for value in row):
        raise AssertionError("wall value left the exact cap")
    epsilon = post[0][w[0]] - wall[0][w[0]]
    expected_post = tuple(
        tuple(
            value + epsilon if agent == 0 and good == w[0] else value
            for good, value in enumerate(row)
        )
        for agent, row in enumerate(wall)
    )
    if epsilon <= 0 or post != expected_post:
        raise AssertionError("post matrix is not a positive one-entry wall step")
    if sum(wall[0][good] for good in original[0]) != sum(
        wall[0][good] for good in w
    ):
        raise AssertionError("wall equality failed")
    if not wall[0][critical_good] < wall[0][w[0]]:
        raise AssertionError("critical-good order failed")
    if any(epsilon >= wall[0][good] for bundle in original[2:] for good in bundle):
        raise AssertionError("small-step premise failed")
    wall_graph = literal_graph(wall, original)
    post_graph = literal_graph(post, original)
    if any(not wall_graph[agent][agent] for agent in range(N)):
        raise AssertionError("wall identity allocation is not EFX")
    changed = tuple(
        (agent, bundle, wall_graph[agent][bundle], post_graph[agent][bundle])
        for agent in range(N)
        for bundle in range(N)
        if wall_graph[agent][bundle] != post_graph[agent][bundle]
    )
    if (
        changed != ((0, 0, True, False),)
        or wall_graph != FIXED_WALL_GRAPH
        or post_graph != FIXED_GRAPH
    ):
        raise AssertionError("wall graph transition changed")

    base = pair_pivots(original, w, critical_good, complete_bundle_menu=True)
    if len(base) != gate["base_pivot_partition_count"] or any(
        matching_count(literal_graph(post, partition)) for partition in base
    ):
        raise AssertionError("a base pivot supports EFX")

    policies = tuple(tuple(policy) for policy in gate["policies"])
    if not policies or len(set(policies)) != len(policies):
        raise AssertionError("policy list changed")
    action_universe = hamiltonian_actions()
    if len(action_universe) != gate["hamiltonian_action_universe_count"]:
        raise AssertionError("Hamiltonian action universe changed")
    selected_records = []
    for policy_index, policy in enumerate(policies):
        for action, partition in action_universe:
            if not selected_literal(post, action, policy):
                continue
            count = matching_count(literal_graph(post, partition))
            selected_records.append(
                {
                    "policy_index": policy_index,
                    "vertices": action["vertices"],
                    "goods": action["goods"],
                    "partition": [list(bundle) for bundle in partition],
                    "matching_count": count,
                }
            )
    if selected_records != gate["selected_actions"]:
        raise AssertionError("selected action replay changed")
    if any(record["matching_count"] for record in selected_records):
        raise AssertionError("a valuation-ranked path supports EFX")

    chain_support_count = sum(
        matching_count(literal_graph(post, partition)) > 0
        for partition in actions_by_partition()
    )
    if chain_support_count != gate["simple_chain_support_count"]:
        raise AssertionError("full chain support count changed")
    global_audit = complete_audit(post, original)
    if global_audit != gate["complete_efx_audit"]:
        raise AssertionError("complete EFX census changed")
    formula_path = Path(gate["formula"])
    if sha256(formula_path) != gate["formula_sha256"]:
        raise AssertionError("formula hash changed")
    source_path = Path(gate["fixed_graph_source"])
    if sha256(source_path) != gate["fixed_graph_source_sha256"]:
        raise AssertionError("fixed-graph source hash changed")
    return {
        "path": str(path),
        "sha256": sha256(path),
        "policies": [list(policy) for policy in policies],
        "selected_action_count": len(selected_records),
        "learned_action_condition_count": gate["learned_action_condition_count"],
        "cegar_round_count": len(gate["rounds"]),
        "simple_chain_support_count": chain_support_count,
        "complete_efx_allocation_count": global_audit["allocation_count"],
        "post_values_sha256": values_sha256(gate["post_wall_values"]),
        "formula_sha256": gate["formula_sha256"],
    }


def audit_boundary(path: Path) -> dict:
    gate = json.loads(path.read_text())
    if (
        gate.get("schema") != GATE_SCHEMA
        or gate.get("status") != "RANKED_PATH_SELECTOR_GATE_INCOMPLETE"
        or gate.get("solver_status") != "unknown"
        or gate.get("integer_upper") != 20
        or gate.get("n") != N
        or gate.get("m") != M
        or tuple(tuple(row) for row in gate.get("fixed_wall_graph", ()))
        != FIXED_WALL_GRAPH
        or tuple(tuple(row) for row in gate.get("fixed_post_wall_graph", ()))
        != FIXED_GRAPH
    ):
        raise AssertionError("invalid ranked-path boundary")
    original, w, critical_good, _m = make_bundles((2, 1, 2, 3))
    base = pair_pivots(original, w, critical_good, complete_bundle_menu=True)
    policies = tuple(tuple(policy) for policy in gate["policies"])
    action_universe = hamiltonian_actions()
    learned = set()
    last_post = None
    sat_round_count = 0
    for round_record in gate["rounds"]:
        if round_record["solver_status"] != "sat":
            if round_record["solver_status"] != "unknown":
                raise AssertionError("boundary contains an unexpected solver status")
            continue
        sat_round_count += 1
        wall = tuple(tuple(row) for row in round_record["wall_values"])
        post = tuple(tuple(row) for row in round_record["post_wall_values"])
        if any(not 1 <= value <= 20 for row in wall for value in row):
            raise AssertionError("boundary wall value left the cap")
        epsilon = post[0][w[0]] - wall[0][w[0]]
        expected_post = tuple(
            tuple(
                value + epsilon if agent == 0 and good == w[0] else value
                for good, value in enumerate(row)
            )
            for agent, row in enumerate(wall)
        )
        if (
            epsilon <= 0
            or post != expected_post
            or sum(wall[0][good] for good in original[0])
            != sum(wall[0][good] for good in w)
            or not wall[0][critical_good] < wall[0][w[0]]
            or any(
                epsilon >= wall[0][good]
                for bundle in original[2:]
                for good in bundle
            )
            or literal_graph(wall, original) != FIXED_WALL_GRAPH
            or literal_graph(post, original) != FIXED_GRAPH
            or any(
                matching_count(literal_graph(post, partition)) for partition in base
            )
        ):
            raise AssertionError("boundary SAT round left the generic wall cell")
        selected = []
        selected_supports = []
        selected_keys = []
        for policy_index, policy in enumerate(policies):
            for action, partition in action_universe:
                if not selected_literal(post, action, policy):
                    continue
                count = matching_count(literal_graph(post, partition))
                record = {
                    "policy_index": policy_index,
                    "vertices": action["vertices"],
                    "goods": action["goods"],
                    "partition": [list(bundle) for bundle in partition],
                    "matching_count": count,
                }
                selected.append(record)
                if count:
                    selected_supports.append(record)
                    selected_keys.append((policy_index, action_key(action)))
        if (
            len(selected) != round_record["selected_action_count"]
            or len(
                {tuple(tuple(bundle) for bundle in item["partition"]) for item in selected}
            )
            != round_record["selected_partition_count"]
            or selected_supports != round_record["selected_supports"]
            or len(selected_supports) != round_record["selected_support_action_count"]
            or any(key in learned for key in selected_keys)
            or len(learned) != round_record["learned_conditions_before_solve"]
        ):
            raise AssertionError("boundary selected-action replay changed")
        learned.update(selected_keys)
        last_post = post
    if (
        sat_round_count + 1 != len(gate["rounds"])
        or len(learned) != gate["learned_action_condition_count"]
        or len(gate["learned_action_conditions"]) != len(learned)
        or gate["rounds"][-1]["solver_status"] != "unknown"
        or gate["rounds"][-1].get("reason_unknown") != "canceled"
    ):
        raise AssertionError("boundary CEGAR ledger changed")
    formula_path = Path(gate["formula"])
    source_path = Path(gate["fixed_graph_source"])
    if (
        sha256(formula_path) != gate["formula_sha256"]
        or sha256(source_path) != gate["fixed_graph_source_sha256"]
    ):
        raise AssertionError("boundary provenance hash changed")
    if last_post is None:
        raise AssertionError("boundary has no exact SAT round")
    chain_support_count = sum(
        matching_count(literal_graph(last_post, partition)) > 0
        for partition in actions_by_partition()
    )
    global_audit = complete_audit(last_post, original)
    return {
        "path": str(path),
        "sha256": sha256(path),
        "policies": [list(policy) for policy in policies],
        "sat_round_count": sat_round_count,
        "learned_action_condition_count": len(learned),
        "terminal_status": "unknown_timeout_at_60_seconds",
        "last_sat_selected_support_action_count": gate["rounds"][-2][
            "selected_support_action_count"
        ],
        "last_sat_simple_chain_support_count": chain_support_count,
        "last_sat_complete_efx_allocation_count": global_audit["allocation_count"],
        "last_sat_post_values_sha256": values_sha256(
            gate["rounds"][-2]["post_wall_values"]
        ),
        "formula_sha256": gate["formula_sha256"],
    }


def run(
    mining_path: Path,
    refutation_paths: tuple[Path, ...],
    boundary_path: Path,
    output_path: Path,
) -> None:
    if output_path.exists():
        raise ValueError("output must be new")
    mining = json.loads(mining_path.read_text())
    source_decision = mining.get("decisions", {}).get("row_min", {}).get("source", {})
    expected_policies = (
        {"source:0": "row0_min", "source:1": "row0_min", "source:2": "row0_min", "source:3": "row1_min"},
        {"source:0": "row0_min", "source:1": "row1_min", "source:2": "row0_min", "source:3": "row1_min"},
        {"source:0": "row0_min", "source:1": "row0_min", "source:2": "row0_min", "source:3": "row3_min"},
    )
    if (
        mining.get("schema") != MINING_SCHEMA
        or mining.get("status") != "FINITE_TRACE_SELECTOR_FOUND"
        or mining.get("exact_model_count") != 23
        or source_decision.get("status") != "sat"
        or source_decision.get("minimum_distinct_criterion_count") != 2
        or source_decision.get("minimum_policy_count") != 3
        or tuple(source_decision.get("minimum_policies", ())) != expected_policies
        or mining["decisions"]["row_min"]["global"]["status"] != "unsat"
        or mining["decisions"]["row_min"]["target"]["status"] != "unsat"
    ):
        raise AssertionError("valuation-selector mining result changed")
    analysis_path = Path(mining["analysis"])
    if sha256(analysis_path) != mining["analysis_sha256"]:
        raise AssertionError("mining analysis hash changed")
    for trace, expected_hash in mining["trace_hashes"].items():
        if sha256(Path(trace)) != expected_hash:
            raise AssertionError("a mining trace hash changed")

    audited = [audit_gate(path) for path in refutation_paths]
    boundary = audit_boundary(boundary_path)
    result = {
        "schema": SCHEMA,
        "status": "SINGLE_STATIC_SELECTOR_REFUTED_UNION_INCOMPLETE_AT_CAP20",
        "domain": (
            "positive additive integer wall valuations in 1..20 in the fixed "
            "four-agent, nine-good Hall-size-four graph cell"
        ),
        "mining": str(mining_path),
        "mining_sha256": sha256(mining_path),
        "exact_trace_model_count": mining["exact_model_count"],
        "trace_surviving_minimum_policy_count": source_decision[
            "minimum_policy_count"
        ],
        "audited_refutations": audited,
        "audited_union_boundary": boundary,
        "interpretation": (
            "Three source-wise minimum policies cover all 23 stored exact "
            "models. The natural 0,0,0,3 policy is exactly refuted in a fresh "
            "generic-wall cap-20 profile. Their three-policy union remains "
            "undecided after 12 SAT rounds, 100 conditional cuts, and a final "
            "60-second timeout."
        ),
        "next_target": (
            "Choose each transfer after recomputing a minimal Hall blocker; "
            "prove that the blocker size or a lexicographic slack potential "
            "decreases, or terminate in an EFX matching."
        ),
        "claim_boundary": (
            "This refutes only the audited 0,0,0,3 source-wise minimum selector "
            "at integer cap 20. The union of all three trace-surviving policies "
            "is neither proved nor refuted. No result here refutes adaptive Hall-"
            "blocker paths, the full 515-partition chain candidate, row-merge "
            "continuation, or complete additive EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mining", type=Path, required=True)
    parser.add_argument("--refutation", type=Path, action="append", required=True)
    parser.add_argument("--boundary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.mining, tuple(args.refutation), args.boundary, args.output)


if __name__ == "__main__":
    main()
