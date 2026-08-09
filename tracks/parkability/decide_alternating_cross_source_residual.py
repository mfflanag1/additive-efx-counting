#!/usr/bin/env python3
"""Target the p/r cross-source residual left by the two reservoir reversals."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_alternating_two_safe_bundle_gate import powerset, safe_expression
    from .run_alternating_variable_packet_rooted_cegar import (
        desired_expression,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from decide_alternating_two_safe_bundle_gate import powerset, safe_expression
    from run_alternating_variable_packet_rooted_cegar import (
        desired_expression,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-cross-source-residual-gate-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tau_constraints(values, observer, active, payment):
    return tuple(
        subset_sum(values, observer, payment)
        >= subset_sum(
            values,
            observer,
            tuple(good for good in active if good != removed),
        )
        for removed in active
    )


def decide(
    sizes,
    timeout_seconds,
    block_all_same_offer_pairs,
    block_s_augmented_reversal,
):
    cell = make_cell(sizes)
    tr, br, tq, bq = cell["packets"]
    floater = cell["floater"]
    d_p = tr + (floater,)
    d_s = tq + (floater,)
    w = cell["base_bundles"][3] + br
    u = cell["base_bundles"][1] + bq
    solver, values, own = structural_solver(cell)

    for payment in powerset(w):
        solver.add(
            z3.Not(
                z3.And(
                    safe_expression(values, own, payment),
                    *tau_constraints(values, 1, d_p, payment),
                )
            )
        )
    for payment in powerset(u):
        solver.add(
            z3.Not(
                z3.And(
                    safe_expression(values, own, payment),
                    *tau_constraints(values, 3, d_s, payment),
                )
            )
        )

    p_reversals = []
    q_reversals = []
    for active in powerset(w):
        if not active:
            continue
        p_reversals.append(
            z3.And(
                desired_expression(values, own, 0, active),
                z3.Or(
                    *(
                    subset_sum(values, 1, active)
                    < subset_sum(
                        values,
                        1,
                        tuple(good for good in d_p if good != removed),
                    )
                    for removed in d_p
                    )
                ),
            )
        )
        if block_s_augmented_reversal:
            solver.add(
                z3.Implies(
                    p_reversals[-1],
                    subset_sum(values, 2, active + (floater,)) <= own[2],
                )
            )
        q_reversals.append(
            z3.And(
                desired_expression(values, own, 3, active),
                z3.Or(
                    *(
                        subset_sum(values, 1, active)
                        < subset_sum(
                            values,
                            1,
                            tuple(good for good in d_p if good != removed),
                        )
                        for removed in d_p
                    )
                ),
            )
        )
    r_reversals = []
    s_reversals = []
    for active in powerset(u):
        if not active:
            continue
        r_reversals.append(
            z3.And(
                desired_expression(values, own, 1, active),
                z3.Or(
                    *(
                    subset_sum(values, 3, active)
                    < subset_sum(
                        values,
                        3,
                        tuple(good for good in d_s if good != removed),
                    )
                    for removed in d_s
                    )
                ),
            )
        )
        s_reversals.append(
            z3.And(
                desired_expression(values, own, 2, active),
                z3.Or(
                    *(
                        subset_sum(values, 3, active)
                        < subset_sum(
                            values,
                            3,
                            tuple(good for good in d_s if good != removed),
                        )
                        for removed in d_s
                    )
                ),
            )
        )
    solver.add(z3.Or(*p_reversals))
    solver.add(z3.Or(*r_reversals))
    solver.add(*(z3.Not(reversal) for reversal in q_reversals))
    solver.add(*(z3.Not(reversal) for reversal in s_reversals))
    solver.add(subset_sum(values, 3, d_s) < own[3])

    same_offer_pair_count = 0
    if block_all_same_offer_pairs:
        residual = tuple(
            good
            for good in range(cell["m"])
            if good not in (cell["x"], cell["y"])
        )
        for active in powerset(cell["base_bundles"][1] + (floater,)):
            if not active:
                continue
            available = tuple(good for good in residual if good not in active)
            for payment in powerset(available):
                solver.add(
                    z3.Not(
                        z3.And(
                            desired_expression(values, own, 0, active),
                            safe_expression(values, own, payment),
                            *tau_constraints(values, 1, active, payment),
                        )
                    )
                )
                same_offer_pair_count += 1

    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    status = solver.check()
    result = {
        "schema": SCHEMA,
        "packet_sizes": list(sizes),
        "solver_status": str(status),
        "p_reversal_candidate_count": len(p_reversals),
        "r_reversal_candidate_count": len(r_reversals),
        "block_all_same_offer_pairs": block_all_same_offer_pairs,
        "block_s_augmented_reversal": block_s_augmented_reversal,
        "same_offer_pair_count": same_offer_pair_count,
        "tested_strengthening": (
            "when block_s_augmented_reversal is true, every qualifying "
            "p-reversal P is additionally forced to satisfy v_s(P+f)<=b_s"
        ),
        "claim_boundary": {
            "sat": (
                "realizes only the selected-set cross-source residual under the "
                "recorded optional blockers"
            ),
            "unsat": (
                "proves only the corresponding bounded implication in this packet "
                "cell; no cap-free or unrestricted dichotomy follows"
            ),
            "unknown": "no mathematical decision",
        },
    }
    if status == z3.sat:
        model = integerize(solver.model(), values)
        result.update(
            {
                "status": "SAT_CROSS_SOURCE_RESIDUAL",
                "values": [list(row) for row in model],
            }
        )
    elif status == z3.unsat:
        result["status"] = "UNSAT_CROSS_SOURCE_RESIDUAL"
    else:
        result.update({"status": "UNKNOWN", "reason_unknown": solver.reason_unknown()})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--block-all-same-offer-pairs", action="store_true")
    parser.add_argument("--block-s-augmented-reversal", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    result = decide(
        sizes,
        args.timeout_seconds,
        args.block_all_same_offer_pairs,
        args.block_s_augmented_reversal,
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
