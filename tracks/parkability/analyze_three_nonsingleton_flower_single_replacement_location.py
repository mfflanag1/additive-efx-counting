#!/usr/bin/env python3
"""Locate the forced later-owner replacement good across hard flower cells."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS
    from .decide_three_nonsingleton_flower_packet_min_family import predicted
    from .decide_three_nonsingleton_flower_packet_min_support import checked_mask
    from .decide_three_nonsingleton_flower_support_mask_audit import RESTS, valid
except ImportError:
    from decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS
    from decide_three_nonsingleton_flower_packet_min_family import predicted
    from decide_three_nonsingleton_flower_packet_min_support import checked_mask
    from decide_three_nonsingleton_flower_support_mask_audit import RESTS, valid


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict:
    counts = Counter()
    records = []
    index = 0
    for left, right in (("c", "c"), ("s", "s"), ("c", "s"), ("s", "c")):
        for order in itertools.permutations(AGENTS):
            later = "q" if order.index("r") < order.index("q") else "r"
            for aq_support, ar_support in itertools.product(
                ("tq", "br", "both"), ("tr", "bq", "both")
            ):
                for mask in range(1 << len(RESTS)):
                    empty_rest = tuple(
                        rest for bit, rest in enumerate(RESTS) if mask & (1 << bit)
                    )
                    if not valid(aq_support, ar_support, empty_rest):
                        continue
                    structural = {
                        "priority_order": list(order),
                        "aq_support": aq_support,
                        "ar_support": ar_support,
                        "empty_rest": list(empty_rest),
                    }
                    if not predicted(structural, left, right):
                        continue
                    bottom = checked_mask(
                        index, "r", left, right, order, aq_support, ar_support,
                        empty_rest, f"{later}_bottom",
                    )["status"]
                    top = checked_mask(
                        index, "r", left, right, order, aq_support, ar_support,
                        empty_rest, f"{later}_top",
                    )["status"]
                    bottom_forced = bottom == "IMPOSSIBLE"
                    top_forced = top == "IMPOSSIBLE"
                    counts[f"{later}_bottom_forced_{str(bottom_forced).lower()}"] += 1
                    counts[f"{later}_top_forced_{str(top_forced).lower()}"] += 1
                    if not bottom_forced or top_forced:
                        records.append({
                            "cell_index": index,
                            "later_owner": later,
                            "priority_order": list(order),
                            "left_bottom_source": left,
                            "right_bottom_source": right,
                            "aq_support": aq_support,
                            "ar_support": ar_support,
                            "empty_rest": list(empty_rest),
                            "bottom_status": bottom,
                            "top_status": top,
                        })
                    index += 1

    script = Path(__file__).resolve()
    root = script.parents[2]
    dependency = (
        root / "tracks" / "parkability"
        / "decide_three_nonsingleton_flower_packet_min_support.py"
    )
    bottom_forced = (
        counts["q_bottom_forced_true"] + counts["r_bottom_forced_true"]
    )
    return {
        "schema": "three-nonsingleton-flower-replacement-location-v1",
        "status": "CLASSIFIED",
        "hard_cell_count": index,
        "bottom_forced_count": bottom_forced,
        "top_or_bottom_disjunction_count": index - bottom_forced,
        "counts": dict(sorted(counts.items())),
        "exception_records": records,
        "claim_boundary": (
            "cap-free packet-minimum location census for the later-owner "
            "singleton-replacement selector; bottom-forced means every eligible "
            "good lies in the displayed bottom packet, not that dependency "
            "termination is proved"
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
        "hard_cells": result["hard_cell_count"],
        "bottom_forced": result["bottom_forced_count"],
        "disjunctive": result["top_or_bottom_disjunction_count"],
        "counts": result["counts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
