#!/usr/bin/env python3
"""Classify q's donor/source role in every stable anchored hole pivot."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


OWNERS = ("r", "q", "c", "s")
ROOT = "r"
Q = "q"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    retained = {"tr0", "tr1", "f"}
    anchor = {"tq0", "tq1", "f"}
    protected_anchor_intersection = retained & anchor
    assert protected_anchor_intersection == {"f"}
    paths = tuple(
        path
        for path in itertools.permutations(OWNERS)
        if any(path[index : index + 2] == (ROOT, Q) for index in range(3))
    )
    assert len(paths) == 6

    records = []
    for path in paths:
        hole = path[0]
        for position, source in enumerate(path[1:], start=1):
            prefix = path[: position + 1]
            if ROOT not in prefix or Q not in prefix:
                continue
            if source == ROOT:
                continue
            if source == Q:
                role = "q_source_collision"
                donor_eligible = False
            else:
                role = "q_donor_available"
                donor_eligible = Q not in {ROOT, hole, source}
                assert donor_eligible
            records.append(
                {
                    "path": list(path),
                    "hole": hole,
                    "closing_source": source,
                    "prefix_cycle": list(prefix),
                    "cycle_length": len(prefix),
                    "q_role": role,
                    "q_distinct_donor_eligible": donor_eligible,
                }
            )

    role_counts = Counter(record["q_role"] for record in records)
    length_counts = {
            role: {
                str(length): count
                for length, count in
                sorted(
                    Counter(
                        record["cycle_length"]
                        for record in records
                        if record["q_role"] == role
                    ).items()
                )
            }
        for role in ("q_donor_available", "q_source_collision")
    }
    assert len(records) == 12
    assert role_counts == {
        "q_donor_available": 6,
        "q_source_collision": 6,
    }
    assert length_counts == {
        "q_donor_available": {"3": 2, "4": 4},
        "q_source_collision": {"2": 2, "3": 2, "4": 2},
    }

    script = Path(__file__).resolve()
    theorem = (
        root
        / "results"
        / "ANCHORED_Q_DONOR_OR_SOURCE_COLLISION_REDUCTION_20260811.md"
    )
    return {
        "schema": "anchored-q-donor-or-source-collision-audit-v1",
        "status": "ALL_EXHAUSTED",
        "anchored_path_count": len(paths),
        "stable_anchor_cycle_count": len(records),
        "role_counts": dict(role_counts),
        "cycle_length_counts": length_counts,
        "all_non_q_source_cases_have_distinct_q_donor": all(
            record["q_distinct_donor_eligible"]
            for record in records
            if record["q_role"] == "q_donor_available"
        ),
        "protected_q_core_and_root_anchor_intersection": sorted(
            protected_anchor_intersection
        ),
        "direct_protected_q_donor_is_physically_disjoint": False,
        "records": records,
        "smallest_missing_operation": (
            "support-conserving floater substitution and two-core q rerouting "
            "across the closing, displaced-path, and protected split-support cores"
        ),
        "claim_boundary": (
            "role classification only; q-core availability, q-source collision "
            "payment, mixed-margin closure, and EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "stable_anchor_cycle_count": result["stable_anchor_cycle_count"],
                "role_counts": result["role_counts"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
