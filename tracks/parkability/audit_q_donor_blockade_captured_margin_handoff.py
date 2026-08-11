#!/usr/bin/env python3
"""Symbolic audit of the protected-q donor-blockade handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(assumptions, negated) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, negated)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    mu, qk, qg, delta = z3.Reals("mu qk qg delta")
    checks = {
        "weak_equality_pays_donor": prove(
            [mu > 0, qk - qg == mu], mu - qk + qg != 0
        ),
        "strict_blockade_captures_margin": prove(
            [mu > 0, qg >= 0, qk - qg > mu], qk <= mu
        ),
        "strict_blockade_packet_nonempty": prove(
            [mu > 0, qg >= 0, qk - qg > mu], qk <= 0
        ),
        "nonpositive_root_gap_has_empty_success": prove(
            [mu > 0, delta <= 0], z3.Or(0 < delta, 0 > mu)
        ),
    }
    theorem = root / "results/Q_DONOR_BLOCKADE_CAPTURED_MARGIN_HANDOFF_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "q-donor-blockade-captured-margin-handoff-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "handoff": {
            "K_without_f": "strict retained-top growth and captured-q-margin rotation",
            "K_with_f": "floater-consuming reset source trichotomy",
        },
        "claim_boundary": (
            "protected-q donor blockade is a captured-margin handoff; "
            "successful-fork safety, floater termination, repeated-bottom "
            "Hall closure, and GG remain open"
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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
