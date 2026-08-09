#!/usr/bin/env python3
"""Extract structural premise dependencies for the alternating q-face gate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .decide_alternating_safe_pair_schema import schema_records
    from .decide_alternating_two_safe_bundle_gate import pair_expression
    from .run_alternating_variable_packet_rooted_cegar import (
        N,
        desired_expression,
        make_cell,
        subset_sum,
    )
except ImportError:
    from decide_alternating_safe_pair_schema import schema_records
    from decide_alternating_two_safe_bundle_gate import pair_expression
    from run_alternating_variable_packet_rooted_cegar import (
        N,
        desired_expression,
        make_cell,
        subset_sum,
    )


SCHEMA = "alternating-qface-dependency-core-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_structural_solver(cell):
    m = cell["m"]
    tr, br, tq, bq = cell["packets"]
    x, y, floater = cell["x"], cell["y"], cell["floater"]
    base_bundles = cell["base_bundles"]
    values = tuple(
        tuple(z3.Real(f"vd_{agent}_{good}") for good in range(m))
        for agent in range(N)
    )
    own = tuple(
        subset_sum(values, agent, base_bundles[agent]) for agent in range(N)
    )
    solver = z3.SolverFor("QF_LRA")
    groups = {}

    def group(name, constraints):
        constraints = tuple(constraints)
        if not constraints:
            return
        label = z3.Bool(f"premise_{name}")
        solver.add(z3.Implies(label, z3.And(*constraints)))
        groups[name] = label

    group("positive", (entry > 0 for row in values for entry in row))
    group("normalized", (z3.Sum(*values[agent]) == 1 for agent in range(N)))
    group(
        "packet_order",
        (
            values[0][left] < values[0][right]
            for packet in cell["packets"]
            for left, right in zip(packet, packet[1:])
        ),
    )
    group(
        "charity_dominance",
        (own[agent] > values[agent][floater] for agent in range(N)),
    )

    expected_envy = {(1, 2), (3, 0)}
    group(
        "expected_envy",
        (
            subset_sum(values, observer, base_bundles[target]) > own[observer]
            for observer, target in sorted(expected_envy)
        ),
    )
    group(
        "absent_envy",
        (
            own[observer] > subset_sum(values, observer, base_bundles[target])
            for observer in range(N)
            for target in range(N)
            if observer != target and (observer, target) not in expected_envy
        ),
    )
    group(
        "base_efx",
        (
            own[observer]
            > subset_sum(
                values,
                observer,
                tuple(
                    good
                    for good in base_bundles[target]
                    if good != removed
                ),
            )
            for observer in range(N)
            for target in range(N)
            for removed in base_bundles[target]
        ),
    )

    expected_desired = {
        (0, 1): tr + (floater,),
        (1, 2): (y,),
        (2, 3): tq + (floater,),
        (3, 0): (x,),
    }
    for source in range(N):
        for target in range(N):
            offer = base_bundles[target] + (floater,)
            expected = expected_desired.get((source, target))
            if expected is not None:
                group(
                    f"desired_{source}_{target}",
                    (desired_expression(values, own, source, expected),),
                )
                group(
                    f"full_offer_forbidden_{source}_{target}",
                    (z3.Not(desired_expression(values, own, source, offer)),),
                )
                continue
            group(
                f"no_desired_{source}_{target}",
                (
                    z3.Not(desired_expression(values, own, source, candidate))
                    for size in range(1, len(offer) + 1)
                    for candidate in itertools.combinations(offer, size)
                ),
            )

    compatible_families = (
        (1, 3, br),
        (2, 3, br),
        (3, 1, bq),
        (0, 1, bq),
    )
    for source, target, incoming in compatible_families:
        target_bundle = base_bundles[target]
        group(
            f"compatible_absence_{source}_{target}",
            (
                z3.Not(desired_expression(values, own, source, candidate))
                for incoming_size in range(len(incoming) + 1)
                for incoming_subset in itertools.combinations(incoming, incoming_size)
                for release_size in range(len(target_bundle) + 1)
                for release in itertools.combinations(target_bundle, release_size)
                for offer in (
                    tuple(
                        good for good in target_bundle if good not in release
                    )
                    + incoming_subset,
                )
                for size in range(1, len(offer) + 1)
                for candidate in itertools.combinations(offer, size)
            ),
        )
    return solver, values, own, groups


def fine_structural_solver(cell):
    m = cell["m"]
    tr, br, tq, bq = cell["packets"]
    floater = cell["floater"]
    base_bundles = cell["base_bundles"]
    values = tuple(
        tuple(z3.Real(f"vf_{agent}_{good}") for good in range(m))
        for agent in range(N)
    )
    own = tuple(
        subset_sum(values, agent, base_bundles[agent]) for agent in range(N)
    )
    solver = z3.SolverFor("QF_LRA")
    groups = {}

    def premise(name, constraint):
        label = z3.Bool(f"premise_{name}")
        solver.add(z3.Implies(label, constraint))
        groups[name] = label

    for agent, row in enumerate(values):
        for good, entry in enumerate(row):
            premise(f"positive_{agent}_{cell['goods'][good]}", entry > 0)

    def forbid_pool(source, pool_name, pool):
        for size in range(1, len(pool) + 1):
            for candidate in itertools.combinations(pool, size):
                suffix = "_".join(cell["goods"][good] for good in candidate)
                premise(
                    f"forbid_{source}_{pool_name}_{suffix}",
                    z3.Not(desired_expression(values, own, source, candidate)),
                )

    x_r = tuple(base_bundles[1])
    x_q = tuple(base_bundles[3])
    q_offer = x_q + (floater,)
    forbid_pool(0, "xqf", q_offer)
    forbid_pool(1, "xqf", q_offer)
    forbid_pool(2, "xrf", x_r + (floater,))
    premise(
        "desired_2_tqf",
        desired_expression(values, own, 2, tq + (floater,)),
    )
    forbid_pool(3, "xqf", q_offer)
    forbid_pool(2, "xqbr", x_q + br)
    forbid_pool(3, "xrbq", x_r + bq)
    forbid_pool(0, "xrbq", x_r + bq)
    return solver, values, own, groups


def decide(sizes, timeout_seconds, deletion_timeout_seconds, granularity):
    cell = make_cell(sizes)
    records = tuple(schema_records(cell, "any"))
    if granularity == "fine":
        solver, values, own, groups = fine_structural_solver(cell)
    else:
        solver, values, own, groups = tracked_structural_solver(cell)
    solver.add(
        *(
            z3.Not(pair_expression(values, own, source, desired_bundle, q_bundle))
            for _, source, desired_bundle, q_bundle in records
        )
    )
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    labels = tuple(groups.values())
    status = solver.check(*labels)
    result = {
        "schema": SCHEMA,
        "packet_sizes": list(sizes),
        "candidate_pair_count": len(records),
        "premise_group_count": len(groups),
        "granularity": granularity,
        "solver_status": str(status),
        "claim_boundary": "dependency audit of the exact bounded q-face gate only",
    }
    if status != z3.unsat:
        result["status"] = "UNKNOWN"
        if status == z3.unknown:
            result["reason_unknown"] = solver.reason_unknown()
        return result

    core_labels = {str(label) for label in solver.unsat_core()}
    core_names = [name for name, label in groups.items() if str(label) in core_labels]
    solver.set(timeout=max(1, int(deletion_timeout_seconds * 1000)))
    deletion_checks = []
    active = list(core_names)
    for name in tuple(active):
        trial = tuple(groups[other] for other in active if other != name)
        trial_status = solver.check(*trial)
        record = {"omitted": name, "status": str(trial_status)}
        if trial_status == z3.unsat:
            active.remove(name)
            record["removed"] = True
        else:
            record["removed"] = False
        if trial_status == z3.unknown:
            record["reason_unknown"] = solver.reason_unknown()
        deletion_checks.append(record)
    replay_status = solver.check(*(groups[name] for name in active))
    result.update(
        {
            "status": "UNSAT_DEPENDENCY_CORE_EXTRACTED",
            "core_group_count": len(core_names),
            "core_groups": core_names,
            "minimal_core_group_count": len(active),
            "minimal_core_groups": active,
            "minimal_core_replay_status": str(replay_status),
            "sequential_deletion_checks": deletion_checks,
        }
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,3,2")
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--deletion-timeout-seconds", type=float, default=10.0)
    parser.add_argument("--granularity", choices=("coarse", "fine"), default="coarse")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    result = decide(
        sizes,
        args.timeout_seconds,
        args.deletion_timeout_seconds,
        args.granularity,
    )
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": sha256(script),
        "z3_version": z3.get_version_string(),
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
