#!/usr/bin/env python3
"""Exact audit of four-placement singleton response transport."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    base = {owner: z3.Real(f"b_{owner}") for owner in OWNERS}
    p = {owner: z3.Real(f"p_{owner}") for owner in OWNERS}
    e = {owner: z3.Real(f"e_{owner}") for owner in OWNERS}
    tau = {owner: z3.Real(f"tau_{owner}") for owner in OWNERS}
    common = [
        *(base[owner] >= 0 for owner in OWNERS),
        *(p[owner] > 0 for owner in OWNERS),
        *(e[owner] >= 0 for owner in OWNERS),
        *(tau[owner] >= 0 for owner in OWNERS),
    ]

    desire_checks = {}
    for selected, source, placement in itertools.product(OWNERS, repeat=3):
        selected_floor = base[source] + (p[source] if selected == source else 0)
        placement_floor = base[source] + (p[source] if placement == source else 0)
        if placement == source:
            continue
        desire_checks[f"{selected}_{source}_{placement}"] = prove(
            common + [e[source] > selected_floor],
            e[source] > placement_floor,
        )
    assert all(desire_checks.values())

    safety_checks = {}
    for selected, placement, observer in itertools.product(OWNERS, repeat=3):
        selected_floor = base[observer] + (p[observer] if selected == observer else 0)
        placement_floor = base[observer] + (p[observer] if placement == observer else 0)
        if selected == observer and placement != observer:
            # This is the only possibly lower floor.  Unsafety here is not
            # algebraically impossible; it yields the strict smaller-response
            # witness used by the theorem.
            safety_checks[f"{selected}_{placement}_{observer}_localized"] = prove(
                common + [tau[observer] <= selected_floor, tau[observer] > placement_floor],
                z3.And(base[observer] < tau[observer], tau[observer] <= base[observer] + p[observer]),
            )
        else:
            safety_checks[f"{selected}_{placement}_{observer}_persists"] = prove(
                common + [tau[observer] <= selected_floor],
                tau[observer] <= placement_floor,
            )
    assert all(safety_checks.values())

    bi, pi, ei = z3.Reals("bi pi ei")
    parking_band = prove(
        [bi >= 0, pi > 0, ei > bi, ei <= bi + pi],
        z3.And(bi < ei, ei <= bi + pi),
    )
    assert parking_band

    script = Path(__file__).resolve()
    theorem = root / "results" / "FOUR_PLACEMENT_SINGLETON_RESPONSE_TRANSPORT_LEMMA_20260814.md"
    return {
        "schema": "four-placement-singleton-response-transport-audit-v1",
        "status": "CAP_FREE_TRANSPORT_PROVED",
        "desire_transport_cases": len(desire_checks),
        "desire_transport_checks": desire_checks,
        "safety_floor_cases": len(safety_checks),
        "safety_floor_checks": safety_checks,
        "parking_band_forced": parking_band,
        "minimum_cardinality_descent_step": (
            "if the sole lowered observer floor makes E unsafe, a one-good "
            "deletion is desired and global extraction has size at most |E|-1"
        ),
        "remaining_gate": (
            "matching/Hall compression of universally safe minimum cores, or "
            "closure of the p-hitting branch"
        ),
        "claim_boundary": (
            "four-placement response transport only; matching compression, "
            "fixed-U, GG, and EFX remain open"
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
    print(json.dumps({"status": result["status"], "remaining_gate": result["remaining_gate"]}, indent=2))


if __name__ == "__main__":
    main()
