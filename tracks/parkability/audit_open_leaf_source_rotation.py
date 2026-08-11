#!/usr/bin/env python3
"""Audit the open-leaf source rotation capture and release support."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    captured, retained, source_bundle, unused = z3.Reals(
        "captured retained source_bundle unused"
    )
    capture = z3.SolverFor("QF_LRA")
    capture.add(
        captured > 0,
        retained >= 0,
        source_bundle > 0,
        unused >= 0,
        source_bundle + retained + unused <= captured + retained,
        captured != source_bundle + unused,
        captured <= source_bundle + unused,
    )
    capture_status = str(capture.check())
    assert capture_status == "unsat"

    incoming = {
        "q": {"f"},
        "b": {"S", "J"},
        "a": {"Xb", "E_minus_J"},
    }
    released = {
        "q": {"J", "E_minus_J"},
        "b": {"Xb"},
        "a": {"S"},
    }
    assert sum(map(len, incoming.values())) == len(set().union(*incoming.values()))
    assert set().union(*incoming.values()) <= {"f"}.union(*released.values())

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "open-leaf-source-rotation-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "failed_old_leaf_payment_forces_strict_capture",
                "status": capture_status,
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
            "QF_LRA old-leaf capture implication and exact packet support; "
            "source desire and nondegenerate strictness are analytic"
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
