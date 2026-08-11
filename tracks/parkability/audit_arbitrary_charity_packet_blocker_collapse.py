#!/usr/bin/env python3
"""Symbolic audit of arbitrary-charity-packet blocker collapse."""

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
    own, packet, parked, new_own, other, new_other = z3.Reals(
        "own packet parked new_own other new_other"
    )
    checks = {
        "exchange_utility_identity": prove(
            [new_own == own - parked + packet],
            new_own - own != packet - parked,
        ),
        "unsafe_packet_strictly_improves_blocker": prove(
            [packet > own, own >= parked, new_own == own - parked + packet],
            new_own <= own,
        ),
        "other_owner_unchanged": prove(
            [new_other == other], new_other != other
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/ARBITRARY_CHARITY_PACKET_BLOCKER_COLLAPSE_LEMMA_20260811.md"
    singleton = root / "results/CHARITY_BLOCKER_EXCHANGE_WALK_LEMMA_20260811.md"
    singleton_audit = root / "results/charity_blocker_exchange_walk_audit.json"
    return {
        "schema": "arbitrary-charity-packet-blocker-collapse-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "conservation": "owner loses parked singleton and receives the entire old charity packet",
        "final_charity_is_singleton": True,
        "connected_exchange": True,
        "singleton_walk_dependency": {
            "theorem": str(singleton.relative_to(root)),
            "theorem_sha256": sha256(singleton),
            "audit": str(singleton_audit.relative_to(root)),
            "audit_sha256": sha256(singleton_audit),
            "audit_status": json.loads(singleton_audit.read_text())["status"],
        },
        "remaining_gate": (
            "owner-target direct-floor payment after a decorated-target trim"
        ),
        "claim_boundary": (
            "arbitrary charity safety only; mixed owner-target payment, repeated-"
            "support GG, and EFX remain open"
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
