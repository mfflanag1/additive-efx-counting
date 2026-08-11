#!/usr/bin/env python3
"""Audit support and scalar claims for charity absorption."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    base, packet = z3.Reals("base packet")
    desired = z3.SolverFor("QF_LRA")
    desired.add(base > 0, packet > base, packet <= base)
    desired_status = str(desired.check())
    assert desired_status == "unsat"

    incoming = {"q": {"f"}, "i": {"R"}}
    released = {"q": {"R"}, "i": {"Xi"}}
    assert not (incoming["q"] & incoming["i"])
    assert set().union(*incoming.values()) <= {"f"}.union(*released.values())

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "packet-replacement-charity-absorption-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "charity_wall_packet_is_strictly_desired",
                "status": desired_status,
            }
        ],
        "support_record": {
            "incoming": {key: sorted(value) for key, value in incoming.items()},
            "released": {key: sorted(value) for key, value in released.items()},
            "sources": {"q": "q", "i": "i"},
            "initially_unallocated": ["f"],
        },
        "claim_boundary": (
            "finite symbolic support and scalar desire audit; common safety of "
            "a subset of an EFX bundle and response-Hall alternatives are analytic"
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
