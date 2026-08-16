#!/usr/bin/env python3
"""CEGAR for valuation-ranked Hamiltonian-path repairs in one row-merge cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .analyze_row_merge_q4_chain_trace import action_key, actions_by_partition
    from .anneal import atomic_json
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
    from .run_row_merge_q4_exchange_chain_cegar import complete_audit
except ImportError:
    from analyze_row_merge_q4_chain_trace import action_key, actions_by_partition
    from anneal import atomic_json
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
    from run_row_merge_q4_exchange_chain_cegar import complete_audit


SCHEMA = "row-merge-q4-ranked-path-cegar-v1"
N = 4
BASE = ((0, 1), (2, 3), (4, 5), (6, 7, 8))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_policy(raw: str) -> tuple[int, ...]:
    policy = tuple(int(part) for part in raw.split(","))
    if len(policy) != N or any(agent not in range(N) for agent in policy):
        raise argparse.ArgumentTypeError("policy must be four agent IDs, e.g. 0,0,0,3")
    return policy


def hamiltonian_actions() -> tuple[tuple[dict, tuple], ...]:
    found = {}
    for partition, actions in actions_by_partition().items():
        for action in actions:
            if (
                action["kind"] == "path"
                and action["length"] == N - 1
                and len(set(action["vertices"])) == N
            ):
                found[action_key(action)] = (action, partition)
    if len(found) != 264:
        raise AssertionError("Hamiltonian action universe changed")
    return tuple(found[key] for key in sorted(found))


def selected_literal(
    values: tuple[tuple[int, ...], ...],
    action: dict,
    policy: tuple[int, ...],
) -> bool:
    vertices = action["vertices"]
    return all(
        values[policy[source]][good]
        == min(values[policy[source]][candidate] for candidate in BASE[source])
        for source, good in zip(vertices[:-1], action["goods"])
    )


def selected_expression(post_rows, action: dict, policy: tuple[int, ...]):
    vertices = action["vertices"]
    return z3.And(
        *(
            post_rows[policy[source]][good]
            <= post_rows[policy[source]][candidate]
            for source, good in zip(vertices[:-1], action["goods"])
            for candidate in BASE[source]
        )
    )


def run(
    result_path: Path,
    formula_path: Path,
    fixed_graph_source_path: Path,
    policies: tuple[tuple[int, ...], ...],
    integer_upper: int,
    max_rounds: int,
    per_check_limit: float,
) -> None:
    if result_path.exists() or formula_path.exists():
        raise ValueError("result and formula outputs must be new")
    if integer_upper < 1 or max_rounds < 1 or per_check_limit <= 0:
        raise ValueError("invalid decision limits")
    if not policies or len(set(policies)) != len(policies):
        raise ValueError("provide one or more distinct policies")

    original, w, critical_good, m = make_bundles((2, 1, 2, 3))
    if original != BASE:
        raise AssertionError("wall partition changed")
    u = original[0]
    perturb_good = w[0]
    small_step_goods = tuple(good for bundle in original[2:] for good in bundle)
    action_universe = hamiltonian_actions()

    fixed_source = json.loads(fixed_graph_source_path.read_text())
    if (
        fixed_source.get("schema") != "row-merge-q4-exchange-chain-cegar-v1"
        or fixed_source.get("m") != m
    ):
        raise ValueError("fixed graph source describes another cell")
    sat_rounds = [
        record for record in fixed_source["rounds"] if record.get("solver_status") == "sat"
    ]
    if not sat_rounds:
        raise ValueError("fixed graph source has no SAT model")
    fixed_wall_values = tuple(tuple(row) for row in sat_rounds[-1]["wall_values"])
    fixed_values = tuple(tuple(row) for row in sat_rounds[-1]["post_wall_values"])
    fixed_wall_graph = literal_graph(fixed_wall_values, original)
    fixed_graph = literal_graph(fixed_values, original)

    master = ParkabilityLRAMaster(N, m, integer_upper=integer_upper)
    solver = master.solver
    wall_rows = master.values
    epsilon = z3.Int("wall_epsilon")
    solver.add(epsilon > 0)
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
    solver.add(*(epsilon < wall_rows[0][good] for good in small_step_goods))

    wall_edges = edge_matrix(solver, wall_rows, original, "wall_original")
    post_edges = edge_matrix(solver, post_rows, original, "post_original")
    solver.add(*(wall_edges[agent][agent] for agent in range(N)))
    solver.add(z3.Not(post_edges[0][0]))
    deficient_bundles = tuple(range(1, N))
    for agent in range(N):
        solver.add(z3.Not(post_edges[agent][0]))
    for size in range(1, N):
        for agents in __import__("itertools").combinations(range(N), size):
            solver.add(has_matching_expression(post_edges, agents, deficient_bundles))
    for agent in range(N):
        for bundle in range(N):
            solver.add(wall_edges[agent][bundle] == fixed_wall_graph[agent][bundle])
            solver.add(post_edges[agent][bundle] == fixed_graph[agent][bundle])

    base_pivots = pair_pivots(original, w, critical_good, complete_bundle_menu=True)
    partition_edges = {}

    def edges_for(partition):
        if partition not in partition_edges:
            partition_edges[partition] = edge_matrix(
                solver, post_rows, partition, f"ranked_partition_{len(partition_edges)}"
            )
        return partition_edges[partition]

    for partition in base_pivots:
        solver.add(z3.Not(has_matching_expression(edges_for(partition))))

    learned = set()
    learned_records = []
    rounds = []
    final_wall_values = None
    final_post_values = None
    final_selected_records = None
    final_complete = None
    final_chain_support_count = None
    overall_status = None
    started = time.time()
    for round_index in range(max_rounds):
        solver.set(timeout=int(per_check_limit * 1000))
        check_started = time.time()
        status = solver.check()
        elapsed = time.time() - check_started
        record = {
            "round": round_index,
            "learned_conditions_before_solve": len(learned),
            "solver_status": str(status),
            "solver_wall_seconds": elapsed,
        }
        if status == z3.unsat:
            rounds.append(record)
            overall_status = "unsat"
            break
        if status != z3.sat:
            record["reason_unknown"] = solver.reason_unknown()
            rounds.append(record)
            overall_status = "unknown"
            break

        model = solver.model()
        rational_wall = tuple(
            tuple(as_fraction(model, value) for value in row) for row in wall_rows
        )
        rational_post = tuple(as_fraction(model, value) for value in post_row)
        decoded_wall, decoded_post_row = primitive_rows(rational_wall, rational_post)
        decoded_post = (decoded_post_row, *decoded_wall[1:])
        if literal_graph(decoded_post, original) != fixed_graph:
            raise AssertionError("decoded model left the fixed graph cell")

        selected_records = []
        violating = []
        for policy_index, policy in enumerate(policies):
            for action, partition in action_universe:
                if not selected_literal(decoded_post, action, policy):
                    continue
                count = matching_count(literal_graph(decoded_post, partition))
                action_record = {
                    "policy_index": policy_index,
                    "vertices": action["vertices"],
                    "goods": action["goods"],
                    "partition": [list(bundle) for bundle in partition],
                    "matching_count": count,
                }
                selected_records.append(action_record)
                key = (policy_index, action_key(action))
                if count and key not in learned:
                    violating.append((key, policy, action, partition, action_record))

        record.update(
            {
                "wall_values": [list(row) for row in decoded_wall],
                "post_wall_values": [list(row) for row in decoded_post],
                "selected_action_count": len(selected_records),
                "selected_partition_count": len(
                    {tuple(tuple(bundle) for bundle in item["partition"]) for item in selected_records}
                ),
                "selected_support_action_count": sum(
                    item["matching_count"] > 0 for item in selected_records
                ),
                "selected_support_partition_count": len(
                    {
                        tuple(tuple(bundle) for bundle in item["partition"])
                        for item in selected_records
                        if item["matching_count"] > 0
                    }
                ),
                "selected_supports": [
                    item for item in selected_records if item["matching_count"] > 0
                ],
            }
        )
        rounds.append(record)
        if not violating:
            if any(
                matching_count(literal_graph(decoded_post, partition))
                for partition in base_pivots
            ):
                raise AssertionError("decoded model gained a base-pivot repair")
            final_wall_values = decoded_wall
            final_post_values = decoded_post
            final_selected_records = selected_records
            final_complete = complete_audit(decoded_post, original)
            final_chain_support_count = sum(
                matching_count(literal_graph(decoded_post, partition)) > 0
                for partition in actions_by_partition()
            )
            overall_status = "sat"
            break

        for key, policy, action, partition, action_record in violating:
            condition = selected_expression(post_rows, action, policy)
            solver.add(
                z3.Implies(condition, z3.Not(has_matching_expression(edges_for(partition))))
            )
            learned.add(key)
            learned_records.append(action_record)
    else:
        overall_status = "round_limit"

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    if overall_status == "sat":
        status_label = "RANKED_PATH_SELECTOR_REFUTATION_FOUND"
        interpretation = (
            "The exact cap-bounded profile blocks every base pivot and every "
            "Hamiltonian path selected by the listed source-wise minimum rules."
        )
    elif overall_status == "unsat":
        status_label = "RANKED_PATH_SELECTOR_CAP_VERIFIED"
        interpretation = (
            "UNSAT proves that a base pivot or a Hamiltonian path selected by "
            "the listed rules repairs every profile in this fixed cap-bounded cell."
        )
    else:
        status_label = "RANKED_PATH_SELECTOR_GATE_INCOMPLETE"
        interpretation = "The configured bounded decision ended without a theorem verdict."
    result = {
        "schema": SCHEMA,
        "status": status_label,
        "domain": f"positive integer wall values at most {integer_upper}",
        "n": N,
        "m": m,
        "wall_partition": [list(bundle) for bundle in original],
        "fixed_graph_source": str(fixed_graph_source_path),
        "fixed_graph_source_sha256": sha256(fixed_graph_source_path),
        "fixed_wall_graph": [list(row) for row in fixed_wall_graph],
        "fixed_post_wall_graph": [list(row) for row in fixed_graph],
        "policies": [list(policy) for policy in policies],
        "policy_meaning": (
            "For each source bundle s, policy[s] names the agent whose minimum-"
            "valued good in s is moved. All 24 oriented Hamiltonian bundle paths "
            "and all tied minima are included."
        ),
        "hamiltonian_action_universe_count": len(action_universe),
        "base_pivot_partition_count": len(base_pivots),
        "integer_upper": integer_upper,
        "max_rounds": max_rounds,
        "per_check_limit_seconds": per_check_limit,
        "elapsed_seconds": time.time() - started,
        "rounds": rounds,
        "learned_action_condition_count": len(learned),
        "learned_action_conditions": learned_records,
        "solver_status": overall_status,
        "wall_values": [list(row) for row in final_wall_values] if final_wall_values else None,
        "post_wall_values": (
            [list(row) for row in final_post_values] if final_post_values else None
        ),
        "selected_actions": final_selected_records,
        "simple_chain_support_count": final_chain_support_count,
        "complete_efx_audit": final_complete,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": interpretation,
        "claim_boundary": (
            "This decides only the listed valuation-ranked selector in one "
            "four-agent nine-good fixed graph cell at the stated integer cap. "
            "It does not decide the full 515-partition chain candidate, row-merge "
            "continuation, or complete additive EFX."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--fixed-graph-source", type=Path, required=True)
    parser.add_argument("--policy", type=parse_policy, action="append", required=True)
    parser.add_argument("--integer-upper", type=int, default=20)
    parser.add_argument("--max-rounds", type=int, default=20)
    parser.add_argument("--per-check-limit", type=float, default=60.0)
    args = parser.parse_args()
    run(
        args.result,
        args.formula,
        args.fixed_graph_source,
        tuple(args.policy),
        args.integer_upper,
        args.max_rounds,
        args.per_check_limit,
    )


if __name__ == "__main__":
    main()
