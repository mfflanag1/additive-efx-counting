#!/usr/bin/env python3
"""Decide a cap-free-shaped safe-pair menu in one alternating packet cell."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_alternating_two_safe_bundle_gate import pair_expression, powerset
    from .run_alternating_variable_packet_rooted_cegar import AGENTS, make_cell, structural_solver
except ImportError:
    from decide_alternating_two_safe_bundle_gate import pair_expression, powerset
    from run_alternating_variable_packet_rooted_cegar import AGENTS, make_cell, structural_solver


SCHEMA = "alternating-safe-pair-schema-gate-v2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_records(cell, q_face_payment):
    tr, br, tq, bq = cell["packets"]
    del tr
    floater = cell["floater"]
    x_r = tuple(cell["base_bundles"][1])
    x_q = tuple(cell["base_bundles"][3])

    for q_face_subset in powerset(x_q):
        if len(q_face_subset) == len(x_q):
            continue
        desired_bundle = tuple(q_face_subset) + (floater,)
        available = tuple(good for good in x_q if good not in desired_bundle)
        q_bundles = (
            (available,)
            if q_face_payment == "remainder"
            else powerset(tuple(good for good in x_r + available))
        )
        for q_bundle in q_bundles:
            if q_bundle:
                yield "q_face", 2, desired_bundle, q_bundle

    for bottom_good in bq:
        q_bundle = tuple(good for good in x_q if good != bottom_good)
        optional = x_r + (floater,)
        for chosen in powerset(optional):
            desired_bundle = tuple(chosen) + (bottom_good,)
            for source in (2, 1):
                yield "bottom_return", source, desired_bundle, q_bundle

def decide(sizes, timeout_seconds, q_face_payment):
    cell = make_cell(sizes)
    records = tuple(schema_records(cell, q_face_payment))
    solver, values, own = structural_solver(cell)
    solver.add(
        *(
            z3.Not(pair_expression(values, own, source, desired_bundle, q_bundle))
            for _, source, desired_bundle, q_bundle in records
        )
    )
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    status = solver.check()
    if status == z3.unsat:
        decision = "UNSAT_SAFE_PAIR_SCHEMA"
    elif status == z3.sat:
        decision = "SAFE_PAIR_SCHEMA_REFUTED"
    else:
        decision = "UNKNOWN"
    result = {
        "schema": SCHEMA,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "candidate_count": len(records),
        "q_face_payment": q_face_payment,
        "family_counts": {
            family: sum(record[0] == family for record in records)
            for family in ("q_face", "bottom_return")
        },
        "solver_status": str(status),
        "status": decision,
        "claim_boundary": {
            "unsat": "the stated schema suffices only in this exact packet cell",
            "sat": "only this restricted schema is refuted; the broader safe-pair lemma remains open",
            "unknown": "no mathematical decision",
        },
    }
    if status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    elif status == z3.sat:
        result["model"] = [
            [str(solver.model().eval(entry, model_completion=True)) for entry in row]
            for row in values
        ]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--q-face-payment", choices=("any", "remainder"), default="any")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        raise ValueError("--sizes must contain four positive integers")
    result = decide(sizes, args.timeout_seconds, args.q_face_payment)
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
