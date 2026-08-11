#!/usr/bin/env python3
"""Exact classification of anchored Hamiltonian paths and hole pivots."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = ("r", "q", "c", "s")
ROOT = "r"
Q = "q"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    paths = tuple(
        path for path in itertools.permutations(OWNERS)
        if any(path[index] == ROOT and path[index + 1] == Q for index in range(3))
    )
    assert len(paths) == 6
    assert all(path[0] != Q for path in paths)

    records = []
    counts = {"anchor_release": 0, "external_cycle": 0, "anchor_cycle": 0}
    for path in paths:
        hole = path[0]
        for position, source in enumerate(path[1:], start=1):
            prefix = path[:position + 1]
            if source == ROOT:
                outcome = "anchor_release"
            elif ROOT in prefix and Q in prefix:
                outcome = "anchor_cycle"
            else:
                outcome = "external_cycle"
                assert set(prefix) == {"c", "s"}
            counts[outcome] += 1
            records.append({
                "path": list(path),
                "hole": hole,
                "source": source,
                "prefix_cycle": list(prefix),
                "outcome": outcome,
            })

    assert counts == {
        "anchor_release": 4,
        "external_cycle": 2,
        "anchor_cycle": 12,
    }

    script = Path(__file__).resolve()
    theorem = root / "results/ANCHORED_MIXED_MARGIN_PATH_TERMINAL_CLASSIFICATION_LEMMA_20260811.md"
    return {
        "schema": "anchored-mixed-margin-path-terminal-classification-audit-v1",
        "status": "ALL_EXHAUSTED",
        "anchored_path_count": len(paths),
        "nonself_hole_pivot_count": len(records),
        "outcome_counts": counts,
        "q_hole_excluded": True,
        "records": records,
        "stable_full_owner_terminal": "anchor-containing prefix cycle",
        "remaining_gate": (
            "use the GG root/q reservoir to pay the critical top-up on an "
            "anchor-containing cycle"
        ),
        "claim_boundary": (
            "anchored path/source classification only; anchor-cycle payment, "
            "mixed-margin closure, and EFX remain open"
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
    print(json.dumps({
        "status": result["status"],
        "anchored_path_count": result["anchored_path_count"],
        "outcome_counts": result["outcome_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
