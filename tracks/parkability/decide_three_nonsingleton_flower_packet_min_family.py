#!/usr/bin/env python3
"""Summarize the cap-free packet-minimum support theorem for a=c."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from .decide_three_nonsingleton_flower_packet_min_support import run as run_pattern
except ImportError:
    from decide_three_nonsingleton_flower_packet_min_support import run as run_pattern


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def before(order, first, second):
    return order.index(first) < order.index(second)


def predicted(record, left_source: str, right_source: str):
    if record["aq_support"] != "both" or record["ar_support"] != "both":
        return False
    empty = set(record["empty_rest"])
    full_q = {"tq_rest", "bq_rest"} <= empty
    full_r = {"br_rest", "tr_rest"} <= empty
    if left_source != right_source:
        return True
    order = record["priority_order"]
    if left_source == "c":
        return full_q or (full_r and before(order, "c", "r"))
    return full_q or (
        full_r
        and before(order, "s", "r")
        and before(order, "s", "c")
    )


def run() -> dict:
    summaries = []
    total_impossible = 0
    total_sat = 0
    for left, right in (("c", "c"), ("s", "s"), ("c", "s"), ("s", "c")):
        result = run_pattern("r", left, right)
        classification_ok = all(
            (record["status"] == "sat") == predicted(record, left, right)
            for record in result["records"]
        )
        signatures = Counter(
            (
                record["aq_support"],
                record["ar_support"],
                tuple(record["empty_rest"]),
            )
            for record in result["survivors"]
        )
        summaries.append({
            "left_bottom_source": left,
            "right_bottom_source": right,
            "counts": result["counts"],
            "classification_verified": classification_ok,
            "survivor_signature_counts": [
                {
                    "aq_support": signature[0],
                    "ar_support": signature[1],
                    "empty_rest": list(signature[2]),
                    "order_count": count,
                }
                for signature, count in sorted(signatures.items())
            ],
        })
        total_impossible += result["counts"]["IMPOSSIBLE"]
        total_sat += result["counts"]["sat"]
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    dependency = root / "tracks" / "parkability" / "decide_three_nonsingleton_flower_packet_min_support.py"
    return {
        "schema": "three-nonsingleton-flower-packet-min-family-v1",
        "status": "CLASSIFIED" if all(summary["classification_verified"] for summary in summaries) else "FAILED",
        "arm_source": "r",
        "singleton_envier": "c",
        "cell_count": total_impossible + total_sat,
        "counts": {"IMPOSSIBLE": total_impossible, "sat": total_sat},
        "summaries": summaries,
        "dual_symmetry": "swapping r and q gives the four arm-source-q patterns",
        "claim_boundary": (
            "cap-free packet-total/minimum classification of all support masks and priorities for the four "
            "arm-source-r, singleton-envier-c bottom-source patterns; it is a structural normal form, not "
            "closure of the surviving cross-packet capture classes"
        ),
        "provenance": {
            "dependency": str(dependency.relative_to(root)),
            "dependency_sha256": sha256(dependency),
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
    print(json.dumps({
        "status": result["status"],
        "cells": result["cell_count"],
        "counts": result["counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
