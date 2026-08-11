#!/usr/bin/env python3
"""QF_LRA checks for the removed-top retention potential."""

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
    mu0, used, fresh, margin, next_margin = z3.Reals(
        "mu0 used fresh margin next_margin"
    )
    positive = [mu0 > 0, used >= 0, fresh > 0]
    records = [
        checked("current_margin_identity", positive + [margin == mu0 - used, margin != mu0 - used]),
        checked("terminal_failure_captures_original_margin", positive + [mu0 - used <= 0, used < mu0]),
        checked("fresh_packet_margin_identity", positive + [
            margin == mu0 - used,
            next_margin == mu0 - used - fresh,
            next_margin != margin - fresh,
        ]),
        checked("surviving_fresh_packet_strictly_descends", positive + [
            margin == mu0 - used,
            next_margin == mu0 - used - fresh,
            next_margin > 0,
            next_margin >= margin,
        ]),
        checked("failed_fresh_packet_captures_margin", positive + [
            mu0 - used > 0,
            mu0 - used - fresh <= 0,
            used + fresh < mu0,
        ]),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/FLOWER_REMOVED_TOP_RETENTION_POTENTIAL_LEMMA_20260811.md"
    return {
        "schema": "flower-removed-top-retention-potential-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of persistent q-margin descent and terminal capture; "
            "support retention across root detours is the analytic construction"
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
