#!/usr/bin/env python3
"""Exact set/value audit of the signed missing-base packet fork."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subsets(items: tuple[int, ...]):
    for size in range(len(items) + 1):
        for chosen in combinations(items, size):
            yield frozenset(chosen)


def run() -> dict[str, object]:
    plus, minus, delta, transferred = z3.Reals(
        "plus minus delta transferred"
    )
    strict = z3.SolverFor("QF_LRA")
    strict.add(
        plus - minus == delta,
        plus > transferred,
        z3.Not(delta - transferred + minus > 0),
    )
    proper_intersection_strict_margin = strict.check() == z3.unsat

    support_cases = 0
    proper_cases = 0
    complete_cases = 0
    empty_cases = 0
    base_containment_failures = 0
    universe = tuple(range(7))
    for base in subsets(universe):
        for current in subsets(universe):
            plus_support = current - base
            minus_support = base - current
            if not plus_support:
                continue
            assert plus_support.isdisjoint(minus_support)
            for packet in subsets(tuple(current)):
                if not packet:
                    continue
                intersection = packet & plus_support
                if not intersection:
                    empty_cases += 1
                    base_containment_failures += int(not packet <= base)
                elif intersection == plus_support:
                    complete_cases += 1
                    assert plus_support <= packet
                else:
                    proper_cases += 1
                    assert intersection < plus_support
                support_cases += 1

    assert support_cases > 0
    assert proper_cases > 0 and complete_cases > 0 and empty_cases > 0
    assert base_containment_failures == 0

    theorem = ROOT / "results/SIGNED_MISSING_BASE_PACKET_CHARGE_OR_BASE_CONTAINMENT_THEOREM_20260814.md"
    clean = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    equality = ROOT / "results/ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md"
    signed = ROOT / "results/FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md"
    contract = ROOT / "results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "base-contained retired-anchor face" in theorem_text
    assert "global multi-label recurrence" in theorem_text

    return {
        "schema": "signed-missing-base-packet-charge-or-base-containment-audit-v1",
        "status": "ROOT_PACKET_BASE_CONTAINED_OR_SIGNED_RETURN_HAS_NAMED_BLOCKER",
        "proper_intersection_strict_margin": proper_intersection_strict_margin,
        "support_cases_checked": support_cases,
        "proper_incoming_intersection_cases": proper_cases,
        "complete_incoming_intersection_cases": complete_cases,
        "empty_incoming_intersection_cases": empty_cases,
        "empty_intersection_base_containment_failures": base_containment_failures,
        "failed_return_charge_is_progress_by_itself": False,
        "global_multilabel_well_foundedness_proved": False,
        "base_contained_face_closed": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, clean, equality, signed, contract, script)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
