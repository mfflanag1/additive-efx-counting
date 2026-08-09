#!/usr/bin/env python3
"""Replay exact fixed-cell checks for the adjacent safe-repartition theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .decide_adjacent_large_safe_repartition_gate import run
    from .run_adjacent_large_variable_packet_global_lex_cegar import atomic_json
except ImportError:
    from decide_adjacent_large_safe_repartition_gate import run
    from run_adjacent_large_variable_packet_global_lex_cegar import atomic_json


SCHEMA = "adjacent-large-safe-repartition-cells-audit-v1"
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
    records = []
    for sizes in CELLS:
        result = run(sizes, timeout_seconds)
        records.append(
            {
                "packet_sizes": list(sizes),
                "status": result["status"],
                "solver": result["solver"],
            }
        )
        if result["status"] != "unsat":
            raise AssertionError(("safe-repartition replay failed", sizes, result))
    script = Path(__file__).resolve()
    gate = script.with_name("decide_adjacent_large_safe_repartition_gate.py")
    return {
        "schema": SCHEMA,
        "status": "ALL_FIXED_CELLS_UNSAT",
        "records": records,
        "claim_boundary": (
            "Exact fixed-cell corroboration only. The cap-free conclusion is "
            "proved analytically in ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md."
        ),
        "provenance": {
            "audit_script": str(script.relative_to(script.parents[2])),
            "audit_script_sha256": sha256(script),
            "gate_script": str(gate.relative_to(gate.parents[2])),
            "gate_script_sha256": sha256(gate),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.timeout_seconds)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
