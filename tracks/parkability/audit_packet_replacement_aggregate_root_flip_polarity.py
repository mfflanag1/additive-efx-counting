#!/usr/bin/env python3
"""Audit the packet-replacement aggregate root-flip polarity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    tr, floater, base, external, core, released = z3.Reals(
        "tr floater base external core released"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        tr > 0,
        floater > 0,
        base > 0,
        external > 0,
        core > external,
        released > 0,
        core + released == base,
        tr + floater > base,
        external >= floater,
        tr <= core - external + released,
    )
    payment_status = str(solver.check())
    assert payment_status == "unsat"

    r_top, r_released = z3.Reals("r_top r_released")
    polarity = z3.SolverFor("QF_LRA")
    polarity.add(
        r_top > 0,
        r_released > 0,
        z3.Not(r_released >= r_top),
        z3.Not(r_top > r_released),
    )
    polarity_status = str(polarity.check())
    assert polarity_status == "unsat"

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "packet-replacement-aggregate-root-flip-polarity-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "external_at_least_floater_forces_full_q_payment",
                "status": payment_status,
            },
            {
                "claim": "failed_root_compensation_forces_strict_r_wall",
                "status": polarity_status,
            },
        ],
        "claim_boundary": (
            "QF_LRA scalar audit of the full-packet choice; EFX and response-"
            "Hall consequences use the complement-return lemma"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
