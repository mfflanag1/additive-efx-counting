#!/usr/bin/env python3
"""Test singleton packet-replacement eligibility on every flower hard cell."""

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
    records = []
    index = 0
    for left, right in (("c", "c"), ("s", "s"), ("c", "s"), ("s", "c")):
        for order in itertools.permutations(AGENTS):
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
                    checked = checked_mask(
                        index,
                        "r",
                        left,
                        right,
                        order,
                        aq_support,
                        ar_support,
                        empty_rest,
                        "all",
                    )
                    forced_owners = []
                    for owner in AGENTS:
                        owner_checked = checked_mask(
                            index,
                            "r",
                            left,
                            right,
                            order,
                            aq_support,
                            ar_support,
                            empty_rest,
                            owner,
                        )
                        if owner_checked["status"] == "IMPOSSIBLE":
                            forced_owners.append(owner)
                    records.append({
                        "left_bottom_source": left,
                        "right_bottom_source": right,
                        "individually_forced_owners": forced_owners,
                        **checked,
                    })
                    index += 1

    counts = Counter(record["status"] for record in records)
    survivors = [record for record in records if record["status"] != "IMPOSSIBLE"]
    forced_owner_counts = Counter(
        owner for record in records for owner in record["individually_forced_owners"]
    )
    disjunctive_only = sum(not record["individually_forced_owners"] for record in records)
    classification_counts = Counter()
    for record in records:
        empty = set(record["empty_rest"])
        normal_form = (
            "full_q_and_r"
            if {"tq_rest", "bq_rest", "tr_rest", "br_rest"} <= empty
            else "full_q"
            if {"tq_rest", "bq_rest"} <= empty
            else "full_r"
            if {"tr_rest", "br_rest"} <= empty
            else "crossing"
        )
        order = record["priority_order"]
        priority = "r_before_q" if order.index("r") < order.index("q") else "q_before_r"
        classification_counts[(
            normal_form,
            priority,
            record["left_bottom_source"] + record["right_bottom_source"],
            "+".join(record["individually_forced_owners"]),
        )] += 1
    script = Path(__file__).resolve()
    root = script.parents[2]
    dependency = root / "tracks" / "parkability" / "decide_three_nonsingleton_flower_packet_min_support.py"
    return {
        "schema": "three-nonsingleton-flower-single-replacement-selector-family-v1",
        "status": "ALL_FORCED" if records and not survivors else "OPEN",
        "hard_cell_count": len(records),
        "counts": dict(sorted(counts.items())),
        "individually_forced_owner_counts": dict(sorted(forced_owner_counts.items())),
        "disjunctive_only_count": disjunctive_only,
        "classification_counts": [
            {
                "normal_form": key[0],
                "mutual_owner_priority": key[1],
                "bottom_sources": key[2],
                "individually_forced_owners": key[3].split("+") if key[3] else [],
                "count": count,
            }
            for key, count in sorted(classification_counts.items())
        ],
        "survivors": survivors,
        "claim_boundary": (
            "cap-free packet-total/minimum audit of the four arm-source-r, "
            "singleton-envier-c hard normal-form families; ALL_FORCED means "
            "simultaneous cover failure forces at least one owner to value f "
            "above the minimum good of her current bundle, not that the resulting "
            "packet-for-charity dependency closes"
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
        "counts": result["counts"],
        "survivors": len(result["survivors"]),
    }, indent=2))


if __name__ == "__main__":
    main()
