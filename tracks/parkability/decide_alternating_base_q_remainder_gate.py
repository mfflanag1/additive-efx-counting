#!/usr/bin/env python3
"""Decide the base-q-remainder desired-bundle gate in one packet cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_singleton_return_cegar import ORDER, dominates, integerize
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        desired_expression,
        make_cell,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from run_alternating_singleton_return_cegar import ORDER, dominates, integerize
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        desired_expression,
        make_cell,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-base-q-remainder-gate-v2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_bundles(cell):
    residual = tuple(
        good for good in range(cell["m"]) if good not in (cell["x"], cell["y"])
    )
    for size in range(1, len(residual) + 1):
        yield from itertools.combinations(residual, size)


def deletion_safe_expression(values, own, candidate, observers):
    return z3.And(
        *(
            own[observer]
            >= subset_sum(
                values,
                observer,
                tuple(good for good in candidate if good != removed),
            )
            for observer in observers
            for removed in candidate
        )
    )


def symbolic_candidate(values, own, cell, source: int, desired_bundle, gate: str):
    xq = cell["packets"][2] + cell["packets"][3]
    q_remainder = tuple(good for good in xq if good not in desired_bundle)
    if gate == "exact_efx":
        allocation = allocation_from_witness(
            cell, source, desired_bundle, q_remainder
        )
        return z3.Not(rival_blocker(values, own, allocation, ORDER))
    if gate == "desired":
        active_condition = desired_expression(values, own, source, desired_bundle)
    else:
        fixed_observers = (0, 1) if source == 2 else (0, 2)
        active_condition = z3.And(
            subset_sum(values, source, desired_bundle) > own[source],
            deletion_safe_expression(
                values, own, desired_bundle, fixed_observers
            ),
            deletion_safe_expression(values, own, q_remainder, (0, 1, 2)),
        )
    return z3.And(
        active_condition,
        *(
            subset_sum(values, 3, q_remainder)
            >= subset_sum(
                values,
                3,
                tuple(good for good in desired_bundle if good != removed),
            )
            for removed in desired_bundle
        ),
    )


def numeric_desired(values, base_own, source: int, desired_bundle) -> bool:
    return sum(values[source][good] for good in desired_bundle) > base_own[source] and all(
        base_own[observer]
        >= sum(values[observer][good] for good in desired_bundle if good != removed)
        for observer in range(4)
        for removed in desired_bundle
    )


def numeric_safe_for(values, base_own, candidate, observers) -> bool:
    return all(
        base_own[observer]
        >= sum(values[observer][good] for good in candidate if good != removed)
        for observer in observers
        for removed in candidate
    )


def numeric_gate_witnesses(values, cell, bundles, gate: str):
    base_own = numeric_utilities(values, cell["base_owner"])
    xq = cell["packets"][2] + cell["packets"][3]
    witnesses = []
    for source in (2, 1):
        for desired_bundle in bundles:
            q_remainder = tuple(good for good in xq if good not in desired_bundle)
            if gate == "exact_efx":
                allocation = allocation_from_witness(
                    cell, source, desired_bundle, q_remainder
                )
                active = numeric_efx(values, allocation) and dominates(
                    values, cell, allocation
                )
            elif gate == "desired":
                active = numeric_desired(
                    values, base_own, source, desired_bundle
                )
            else:
                fixed_observers = (0, 1) if source == 2 else (0, 2)
                active = (
                    sum(values[source][good] for good in desired_bundle)
                    > base_own[source]
                    and numeric_safe_for(
                        values, base_own, desired_bundle, fixed_observers
                    )
                    and numeric_safe_for(
                        values, base_own, q_remainder, (0, 1, 2)
                    )
                )
            if not active:
                continue
            q_value = sum(values[3][good] for good in q_remainder)
            q_threshold = max(
                sum(values[3][good] for good in desired_bundle if good != removed)
                for removed in desired_bundle
            )
            if q_value >= q_threshold:
                witnesses.append((source, desired_bundle, q_remainder))
    return witnesses


def allocation_from_witness(cell, source, desired_bundle, q_remainder):
    owner = [None] * cell["m"]
    owner[cell["x"]] = 0
    owner[cell["y"]] = 1 if source == 2 else 2
    for good in desired_bundle:
        owner[good] = source
    for good in q_remainder:
        owner[good] = 3
    return tuple(owner)


def decide(sizes, timeout_seconds: float, gate: str) -> dict:
    cell = make_cell(sizes)
    bundles = tuple(candidate_bundles(cell))
    solver, values, own = structural_solver(cell)
    conditions = tuple(
        symbolic_candidate(values, own, cell, source, desired_bundle, gate)
        for source in (2, 1)
        for desired_bundle in bundles
    )
    solver.add(*(z3.Not(condition) for condition in conditions))
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    status = solver.check()
    result = {
        "schema": SCHEMA,
        "gate": gate,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "agent_order": list(ORDER),
        "agent_order_names": [AGENTS[agent] for agent in ORDER],
        "desired_bundle_count_per_source": len(bundles),
        "symbolic_candidate_count": len(conditions),
        "solver_status": str(status),
        "claim_boundary": {
            "unsat": "the selected base-q-remainder gate holds in this exact packet cell",
            "sat": "only the selected base-q-remainder gate is refuted; the broader singleton-return and external-observer lemmas require separate checks",
            "unknown": "no mathematical decision",
        },
    }
    if status == z3.sat:
        integers = integerize(solver.model(), values)
        witnesses = numeric_gate_witnesses(integers, cell, bundles, gate)
        if witnesses:
            raise AssertionError("SAT model still has a base-q-remainder witness")
        singleton_escapes = 0
        for source in (2, 1):
            for desired_bundle in bundles:
                xq = cell["packets"][2] + cell["packets"][3]
                q_remainder = tuple(good for good in xq if good not in desired_bundle)
                allocation = allocation_from_witness(
                    cell, source, desired_bundle, q_remainder
                )
                if numeric_efx(integers, allocation) and dominates(
                    integers, cell, allocation
                ):
                    singleton_escapes += 1
        result.update(
            {
                "status": f"BASE_Q_REMAINDER_{gate.upper()}_GATE_REFUTED",
                "values": [list(row) for row in integers],
                "base_q_remainder_witness_count": 0,
                "base_q_remainder_allocation_escape_count": singleton_escapes,
            }
        )
    elif status == z3.unsat:
        result["status"] = f"UNSAT_BASE_Q_REMAINDER_{gate.upper()}_GATE"
    else:
        result["status"] = "UNKNOWN"
        result["reason_unknown"] = solver.reason_unknown()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument(
        "--gate",
        choices=("desired", "recipient_relaxed", "exact_efx"),
        default="desired",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        raise ValueError("--sizes must contain four positive integers")
    result = decide(sizes, args.timeout_seconds, args.gate)
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
