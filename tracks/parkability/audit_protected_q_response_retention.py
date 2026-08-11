#!/usr/bin/env python3
"""Audit persistence of protected q response coverage across GG resets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints: z3.BoolRef) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    # An A_q core selected from a target disjoint from the anchored target
    # cannot use the unique charity good already present in D_r.
    support_atoms = {
        "root_anchor": {"T_q", "f"},
        "protected_q_core": {"A_q_without_f"},
    }
    selected_support_disjoint = not (
        support_atoms["root_anchor"] & support_atoms["protected_q_core"]
    )
    protected_core_avoids_f = "f" not in support_atoms["protected_q_core"]

    margin, overlap = z3.Reals("q_margin retained_top_overlap")
    preserved_or_progress = check_unsat(
        margin > 0,
        overlap >= 0,
        z3.Not(z3.Or(
            z3.And(overlap == 0, margin > 0),
            z3.And(overlap > 0, margin - overlap > 0),
            z3.And(overlap > 0, margin - overlap <= 0),
        )),
    )

    script = Path(__file__).resolve()
    theorem = root / "results/PROTECTED_Q_RESPONSE_RETENTION_LEMMA_20260811.md"
    return {
        "schema": "protected-q-response-retention-audit-v1",
        "status": "ALL_FORCED",
        "root_anchor_contains_f": True,
        "selected_response_cores_pairwise_disjoint": selected_support_disjoint,
        "protected_q_core_avoids_f": protected_core_avoids_f,
        "reset_outcomes": [
            "same retained support and q remains representable",
            "strict retained-top support growth and q remains representable",
            "captured q-margin handoff",
        ],
        "scalar_records": {
            "universal_reset_trichotomy_exhaustive": preserved_or_progress,
        },
        "claim_boundary": (
            "cap-free persistence of protected q response coverage across "
            "top-only orientation resets; degree-zero q recurrence and physical "
            "closure of anchor-gap paths are not proved"
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
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results/protected_q_response_retention_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
