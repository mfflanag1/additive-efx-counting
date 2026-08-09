#!/usr/bin/env python3
"""Decide the hard-branch threshold-matching promotion gate for psqr."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .decide_alternating_two_safe_bundle_gate import powerset, safe_expression
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        desired_expression,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from decide_alternating_two_safe_bundle_gate import powerset, safe_expression
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        desired_expression,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-psqr-extension-or-suffix-handoff-gate-v2"
ORDER = (0, 2, 3, 1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def promoted_matching_candidates(cell):
    root_offer = cell["base_bundles"][1] + (cell["floater"],)
    residual = tuple(
        good for good in range(cell["m"])
        if good not in (cell["x"], cell["y"])
    )
    for desired in powerset(root_offer):
        if not desired:
            continue
        available = tuple(good for good in residual if good not in desired)
        for payment in powerset(available):
            yield desired, payment


def dominates_threshold(values, observer, own_bundle, target_bundle):
    return z3.And(
        *(
            subset_sum(values, observer, own_bundle)
            >= subset_sum(
                values,
                observer,
                tuple(good for good in target_bundle if good != removed),
            )
            for removed in target_bundle
        )
    )


def threshold_matching_expression(values, own, desired, payment, cell):
    bundles = ((cell["x"],), (cell["y"],), payment)
    p_safe = dominates_threshold(values, 0, desired, payment)
    matchings = []
    for assignment in itertools.permutations(bundles):
        edges = []
        for agent, own_bundle in zip((1, 2, 3), assignment):
            edges.append(dominates_threshold(values, agent, own_bundle, desired))
            if own_bundle != payment:
                edges.append(dominates_threshold(values, agent, own_bundle, payment))
        matchings.append(z3.And(*edges))
    return z3.And(p_safe, z3.Or(*matchings))


def anchored_handoff_candidates(cell):
    residual = tuple(
        good for good in range(cell["m"])
        if good not in (cell["x"], cell["y"])
    )
    for source, payment_observer in ((3, 1), (2, 3)):
        for active in powerset(residual):
            if not active:
                continue
            available = tuple(good for good in residual if good not in active)
            for payment in powerset(available):
                yield source, payment_observer, active, payment


def anchored_handoff_expression(
    values, own, source, payment_observer, active, payment
):
    return z3.And(
        desired_expression(values, own, source, active),
        safe_expression(values, own, payment),
        *(
            subset_sum(values, payment_observer, payment)
            >= subset_sum(
                values,
                payment_observer,
                tuple(good for good in active if good != removed),
            )
            for removed in active
        ),
    )


def decide(sizes, timeout_seconds):
    cell = make_cell(sizes)
    solver, values, own = structural_solver(cell)
    _tr, _br, tq, bq = cell["packets"]
    desired_s = tq + (cell["floater"],)
    reservoir = cell["base_bundles"][1] + bq

    solver.add(subset_sum(values, 3, desired_s) < own[3])
    solver.add(
        *(
            z3.Not(desired_expression(values, own, 2, candidate))
            for candidate in powerset(reservoir)
        )
    )
    q_deletions = tuple(
        subset_sum(
            values,
            3,
            tuple(good for good in desired_s if good != removed),
        )
        for removed in desired_s
    )
    for payment in powerset(reservoir):
        solver.add(
            z3.Not(
                z3.And(
                    safe_expression(values, own, payment),
                    *(
                        subset_sum(values, 3, payment) >= deletion
                        for deletion in q_deletions
                    ),
                )
            )
        )

    candidates = tuple(promoted_matching_candidates(cell))
    for desired, payment in candidates:
        solver.add(
            z3.Or(
                z3.Not(desired_expression(values, own, 0, desired)),
                z3.Not(
                    threshold_matching_expression(
                        values, own, desired, payment, cell
                    )
                ),
            )
        )
    anchored_candidates = tuple(anchored_handoff_candidates(cell))
    for source, payment_observer, active, payment in anchored_candidates:
        solver.add(
            z3.Not(
                anchored_handoff_expression(
                    values,
                    own,
                    source,
                    payment_observer,
                    active,
                    payment,
                )
            )
        )
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    checked = solver.check()
    result = {
        "schema": SCHEMA,
        "status": (
            "SAT_EXTENSION_OR_HANDOFF_GATE_REFUTED"
            if checked == z3.sat
            else "UNSAT_EXTENSION_OR_HANDOFF_GATE"
            if checked == z3.unsat
            else "UNKNOWN"
        ),
        "solver_status": str(checked),
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "agent_order": list(ORDER),
        "agent_order_names": [AGENTS[agent] for agent in ORDER],
        "candidate_count": len(candidates),
        "anchored_candidate_count": len(anchored_candidates),
        "hard_branch": {
            "q_values_Tq_plus_f_below_base": True,
            "no_s_desired_subset_in_Xr_plus_Bq": True,
            "no_common_safe_q_threshold_payment_in_Xr_plus_Bq": True,
        },
        "claim_boundary": {
            "sat": "refutes only the extension-or-suffix-handoff gate under the displayed hard premises in this exact packet cell",
            "unsat": "proves only that combined gate under the displayed hard premises in this exact packet cell; a cap-free proof is still required",
            "unknown": "no mathematical decision",
        },
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
        },
    }
    if checked == z3.sat:
        result["values"] = [list(row) for row in integerize(solver.model(), values)]
    elif checked == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": sha256(script),
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        raise ValueError("--sizes must contain four positive integers")
    result = decide(sizes, args.timeout_seconds)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
