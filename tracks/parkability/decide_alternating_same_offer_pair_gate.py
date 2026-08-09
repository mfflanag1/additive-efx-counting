#!/usr/bin/env python3
"""Short exact probe for the same-offer promoted two-safe-pair condition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_alternating_two_safe_bundle_gate import (
        pair_expression,
        powerset,
        safe_expression,
    )
    from .run_alternating_variable_packet_rooted_cegar import (
        desired_expression,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from decide_alternating_two_safe_bundle_gate import (
        pair_expression,
        powerset,
        safe_expression,
    )
    from run_alternating_variable_packet_rooted_cegar import (
        desired_expression,
        integerize,
        make_cell,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-same-offer-pair-gate-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def observer_pair_expression(values, own, source, observer, active, payment):
    return z3.And(
        desired_expression(values, own, source, active),
        safe_expression(values, own, payment),
        *(
            subset_sum(values, observer, payment)
            >= subset_sum(
                values,
                observer,
                tuple(good for good in active if good != removed),
            )
            for removed in active
        ),
    )


def decide(
    sizes,
    timeout_seconds,
    block_anchored_s_pairs,
    block_anchored_q_pairs,
):
    cell = make_cell(sizes)
    offer = cell["base_bundles"][1] + (cell["floater"],)
    residual = tuple(
        good for good in range(cell["m"]) if good not in (cell["x"], cell["y"])
    )
    solver, values, own = structural_solver(cell)
    candidate_count = 0
    for active in powerset(offer):
        if not active:
            continue
        available = tuple(good for good in residual if good not in active)
        for payment in powerset(available):
            condition = z3.And(
                desired_expression(values, own, 0, active),
                safe_expression(values, own, payment),
                *(
                    subset_sum(values, 1, payment)
                    >= subset_sum(
                        values,
                        1,
                        tuple(good for good in active if good != removed),
                    )
                    for removed in active
                ),
            )
            solver.add(z3.Not(condition))
            candidate_count += 1
    anchored_candidate_count = 0
    if block_anchored_s_pairs:
        for active in powerset(residual):
            if not active:
                continue
            available = tuple(good for good in residual if good not in active)
            for payment in powerset(available):
                solver.add(
                    z3.Not(pair_expression(values, own, 2, active, payment))
                )
                anchored_candidate_count += 1
    anchored_q_candidate_count = 0
    if block_anchored_q_pairs:
        for active in powerset(residual):
            if not active:
                continue
            available = tuple(good for good in residual if good not in active)
            for payment in powerset(available):
                solver.add(
                    z3.Not(
                        observer_pair_expression(
                            values,
                            own,
                            3,
                            1,
                            active,
                            payment,
                        )
                    )
                )
                anchored_q_candidate_count += 1
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    status = solver.check()
    result = {
        "schema": SCHEMA,
        "packet_sizes": list(sizes),
        "candidate_count": candidate_count,
        "anchored_s_candidate_count": anchored_candidate_count,
        "anchored_q_candidate_count": anchored_q_candidate_count,
        "block_anchored_s_pairs": block_anchored_s_pairs,
        "block_anchored_q_pairs": block_anchored_q_pairs,
        "solver_status": str(status),
        "claim_boundary": {
            "sat": "refutes only the sufficient same-offer two-safe-pair condition in this cell",
            "unsat": "proves only this bounded sufficient condition; no cap-free claim",
            "unknown": "no mathematical decision",
        },
    }
    if status == z3.sat:
        model = integerize(solver.model(), values)
        result.update(
            {
                "status": "SAME_OFFER_PAIR_GATE_REFUTED",
                "values": [list(row) for row in model],
            }
        )
    elif status == z3.unsat:
        result["status"] = "UNSAT_SAME_OFFER_PAIR_GATE"
    else:
        result.update({"status": "UNKNOWN", "reason_unknown": solver.reason_unknown()})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--block-anchored-s-pairs", action="store_true")
    parser.add_argument("--block-anchored-q-pairs", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    result = decide(
        sizes,
        args.timeout_seconds,
        args.block_anchored_s_pairs,
        args.block_anchored_q_pairs,
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
