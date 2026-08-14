#!/usr/bin/env python3
"""Independent QF_LRA audit of the minimal-d-core terminal polarity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "results" / "MINIMAL_D_CORE_FULL_RETENTION_OR_TWO_FLOOR_POLARITY_LEMMA_20260813.md"


def audit():
    core, floor, retained, current, chi = z3.Reals(
        "core floor retained current chi"
    )
    margin = core - floor

    proper = z3.SolverFor("QF_LRA")
    proper.add(
        core > floor, floor >= 0, current >= 0, chi >= 0,
        retained >= 0, retained <= floor,
        retained > margin + current + chi,
    )
    proper.add(z3.Not(core + current + chi < 2 * floor))
    assert proper.check() == z3.unsat

    deficit = floor - current - chi
    margin_deficit = z3.SolverFor("QF_LRA")
    margin_deficit.add(
        core > floor, current >= 0, chi >= 0,
        core + current + chi < 2 * floor,
    )
    margin_deficit.add(z3.Or(deficit <= 0, z3.Not(core - floor < deficit)))
    assert margin_deficit.check() == z3.unsat

    full = z3.SolverFor("QF_LRA")
    full.add(core > floor, retained == core)
    full.add(
        (retained > margin + current + chi)
        != (current + chi < floor)
    )
    assert full.check() == z3.unsat

    return {
        "schema": "minimal-d-core-full-retention-two-floor-audit-v1",
        "status": "FULL_RETENTION_AND_TWO_FLOOR_POLARITY_VERIFIED",
        "proper_retention_status": "unsat",
        "full_retention_equivalence_status": "unsat",
        "proper_margin_below_bare_deficit_status": "unsat",
        "document_sha256": hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Cap-free scalar consequence of minimality and terminal capture. "
            "The two-target root-wall contradiction and active theorem remain open."
        ),
    }


def main():
    result = audit()
    output = ROOT / "results" / "minimal_d_core_full_retention_two_floor_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
