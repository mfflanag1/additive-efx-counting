#!/usr/bin/env python3
"""QF_LRA checks for same-source top-switch margin descent."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name: str, constraints) -> dict:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def run(root: Path) -> dict:
    margin, fresh, next_margin = z3.Reals("margin fresh next_margin")
    positive = [margin > 0, fresh > 0]
    records = [
        checked(
            "fresh_switch_margin_identity",
            positive + [next_margin == margin - fresh, next_margin != margin - fresh],
        ),
        checked(
            "successful_fresh_switch_strictly_descends_margin",
            positive
            + [next_margin == margin - fresh, next_margin > 0, next_margin >= margin],
        ),
        checked(
            "failed_fresh_switch_captures_current_margin",
            positive + [margin - fresh <= 0, fresh < margin],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/SAME_SOURCE_TOP_SWITCH_MARGIN_DESCENT_LEMMA_20260811.md"
    return {
        "schema": "same-source-top-switch-margin-descent-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of fresh-packet response-margin descent; it does not "
            "eliminate reuse of previously removed top support"
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
