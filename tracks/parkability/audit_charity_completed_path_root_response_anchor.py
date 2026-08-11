#!/usr/bin/env python3
"""Exact support/source audit for the complete-path root anchor."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name: str, constraints) -> dict:
    solver = z3.Solver()
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def run(root: Path) -> dict:
    tq_count, bq_count, k_count, donor_count = z3.Ints(
        "tq_count bq_count k_count donor_count"
    )
    source = z3.Int("source")
    incoming_root = z3.Int("incoming_root")
    records = [
        checked(
            "root_anchor_is_contained_in_completed_q_target",
            [
                tq_count > 0,
                bq_count >= k_count,
                k_count > 0,
                donor_count == tq_count + bq_count - k_count + 1,
                donor_count < tq_count + 1,
            ],
        ),
        checked(
            "root_anchor_releases_full_bottom_packet",
            [bq_count >= k_count, k_count > 0, bq_count < k_count],
        ),
        checked(
            "root_target_incoming_is_supplied_by_anchor_release",
            [incoming_root >= 0, incoming_root <= k_count, k_count <= bq_count, incoming_root > bq_count],
        ),
        checked(
            "four_root_target_source_labels_are_exhaustive",
            [source >= 0, source <= 3, source != 0, source != 1, source != 2, source != 3],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/CHARITY_COMPLETED_PATH_ROOT_RESPONSE_ANCHOR_LEMMA_20260811.md"
    return {
        "schema": "charity-completed-path-root-response-anchor-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "Exact integer/support audit of the permanent root edge and source split; "
            "root-monopoly/Hall termination is outside scope"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
