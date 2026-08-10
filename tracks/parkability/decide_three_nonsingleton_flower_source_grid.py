#!/usr/bin/env python3
"""Enumerate the source cells closed by direct flower matchings."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict:
    records = []
    for arm, envier, left_bottom, right_bottom in itertools.product(
        ("r", "q", "s"),
        ("r", "q", "c"),
        ("c", "s"),
        ("c", "s"),
    ):
        sources = (arm, envier, left_bottom, right_bottom)
        if arm == "s" and envier == "c":
            status = "CLOSED_DIRECT_CS_SWAP"
        elif len(set(sources)) == 4:
            status = "CLOSED_FOUR_SOURCE_MATCHING"
        else:
            status = "OPEN"
        records.append({
            "arm_source": arm,
            "singleton_envier": envier,
            "left_bottom_source": left_bottom,
            "right_bottom_source": right_bottom,
            "status": status,
        })
    counts = {
        status: sum(record["status"] == status for record in records)
        for status in (
            "CLOSED_DIRECT_CS_SWAP",
            "CLOSED_FOUR_SOURCE_MATCHING",
            "OPEN",
        )
    }
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-source-grid-v1",
        "status": "EXHAUSTIVE" if len(records) == 36 and counts == {
            "CLOSED_DIRECT_CS_SWAP": 4,
            "CLOSED_FOUR_SOURCE_MATCHING": 4,
            "OPEN": 28,
        } else "FAILED",
        "counts": counts,
        "records": records,
        "claim_boundary": "combinatorial source-cell cover by two direct analytic allocations; the 28 open cells require reservoir or PI routing",
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
