#!/usr/bin/env python3
"""Replay the finite adjacent dual-payment gate across atomic/split cells."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .decide_adjacent_large_dual_payment_gate import run
except ImportError:
    from decide_adjacent_large_dual_payment_gate import run


SCHEMA = "adjacent-large-dual-payment-cells-audit-v1"
CELLS = (
    (1, 1, 1, 1),
    (2, 1, 1, 1),
    (1, 2, 1, 1),
    (1, 1, 2, 1),
    (1, 1, 1, 2),
    (2, 2, 2, 2),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(timeout_seconds):
    records = [run(sizes, timeout_seconds) for sizes in CELLS]
    statuses = {tuple(record["packet_sizes"]): record["status"] for record in records}
    expected = {sizes: ("sat" if sizes == (2, 2, 2, 2) else "unsat") for sizes in CELLS}
    if statuses != expected:
        raise AssertionError((statuses, expected))
    script = Path(__file__).resolve()
    decision = script.with_name("decide_adjacent_large_dual_payment_gate.py")
    return {
        "schema": SCHEMA,
        "status": "DUAL_PAYMENT_FIRST_FAILS_IN_FULL_BINARY_CELL",
        "records": records,
        "claim_boundary": (
            "The dichotomy is exact only in the listed finite cells. The binary SAT "
            "profile is not an unrestricted escape counterexample."
        ),
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
            "decision_script": str(decision.relative_to(decision.parents[2])),
            "decision_script_sha256": sha256(decision),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.timeout_seconds)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
