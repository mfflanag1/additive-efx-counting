#!/usr/bin/env python3
"""Audit the top-core root exchange scalar and packet support claims."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    top_core, floater, full_top, base = z3.Reals(
        "top_core floater full_top base"
    )
    existence = z3.SolverFor("QF_LRA")
    existence.add(
        top_core > 0,
        floater > 0,
        full_top > 0,
        base > top_core,
        full_top + floater > base,
        full_top + floater <= top_core,
    )
    existence_status = str(existence.check())
    assert existence_status == "unsat"

    incoming = {"q": {"P", "f"}, "r": {"K_T"}}
    released = {"q": {"K_T"}, "r": {"P"}}
    assert not (incoming["q"] & incoming["r"])
    assert set().union(*incoming.values()) <= {"f"}.union(*released.values())

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "top-core-root-exchange-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "full_top_plus_floater_pays_top_core",
                "status": existence_status,
            }
        ],
        "support_record": {
            "incoming": {
                key: sorted(value) for key, value in incoming.items()
            },
            "released": {
                key: sorted(value) for key, value in released.items()
            },
            "initially_unallocated": ["f"],
        },
        "claim_boundary": (
            "QF_LRA payment existence and exact two-edge support; finite "
            "inclusion-minimal selection and reverse-order strictness are analytic"
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
