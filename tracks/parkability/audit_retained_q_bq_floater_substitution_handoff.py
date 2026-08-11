#!/usr/bin/env python3
"""Exact audit of the retained-q Bq floater-substitution handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    q_top, q_f, q_bq, q_base = z3.Reals("q_top q_f q_bq q_base")
    q_substitution = prove(
        [
            q_top >= 0,
            q_f > 0,
            q_bq > 0,
            q_base > 0,
            q_top + q_f > q_base,
            q_bq >= q_f,
        ],
        q_top + q_bq > q_base,
    )

    r_kt, r_rem, r_kb, r_br = z3.Reals("r_kt r_rem r_kb r_br")
    root_bottom_capture = prove(
        [
            r_kt >= 0,
            r_rem >= 0,
            r_kb >= 0,
            r_br > 0,
            r_kt + r_kb > r_kt + r_rem + r_br,
        ],
        z3.And(r_kb > 0, r_kb > r_rem + r_br),
    )

    q_e, q_o, q_anchor_gain = z3.Reals("q_e q_o q_anchor_gain")
    anchor_return_identity = prove(
        [
            q_e >= 0,
            q_o >= 0,
            q_e + q_o == q_top + q_bq,
            q_anchor_gain == q_f + q_o - q_bq,
        ],
        q_anchor_gain == q_top + q_f - q_e,
    )
    paid_return_or_q_response = prove(
        [
            q_top + q_f > q_base,
            q_e >= 0,
            q_base > 0,
        ],
        z3.Or(q_e <= q_top + q_f, q_e > q_base),
    )

    checks = {
        "bq_substitution_strictly_pays_q": q_substitution,
        "root_response_forces_nonempty_bq_capture": root_bottom_capture,
        "anchor_return_q_gain_identity": anchor_return_identity,
        "anchor_return_pays_or_same_core_is_q_response": paid_return_or_q_response,
    }
    assert all(checks.values())

    root_anchor = {"tq0", "tq1", "f"}
    substituted_q_target = {"tr0", "tr1", "bq0", "bq1"}
    assert root_anchor.isdisjoint(substituted_q_target)
    q_target = {"tq0", "tq1", "bq0", "bq1"}
    root_core = {"tq0", "tq1", "f"}
    assert q_target - root_core == {"bq0", "bq1"}

    script = Path(__file__).resolve()
    theorem = (
        root
        / "results"
        / "RETAINED_Q_BQ_FLOATER_SUBSTITUTION_HANDOFF_LEMMA_20260811.md"
    )
    return {
        "schema": "retained-q-bq-floater-substitution-handoff-audit-v1",
        "status": "ALL_FORCED",
        "checks": checks,
        "root_anchor_and_substituted_q_target_disjoint": True,
        "root_anchor_releases_complete_bq": True,
        "remaining_separator": "q-source role collision and rank-two continuation",
        "claim_boundary": (
            "Bq substitution and root-source anchor return only; rank-two "
            "termination, q-source collision, mixed-margin closure, and EFX "
            "remain open"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
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
                "remaining_separator": result["remaining_separator"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
