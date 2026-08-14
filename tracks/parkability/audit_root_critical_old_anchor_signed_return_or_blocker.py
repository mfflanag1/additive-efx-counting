#!/usr/bin/env python3
"""Exact scalar/support audit of the critical-anchor signed-return fork."""

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
    plus, minus, packet, delta = z3.Reals("plus minus packet delta")
    margin = z3.SolverFor("QF_LRA")
    margin.add(
        plus - minus == delta,
        plus > packet,
        delta > 0,
        z3.Not(delta - packet + minus > 0),
    )
    proper_signed_return_is_strict = margin.check() == z3.unsat

    equality = z3.SolverFor("QF_LRA")
    equality.add(
        plus - minus == delta,
        packet == plus,
        delta - packet + minus != 0,
    )
    complete_signed_return_is_equality = equality.check() == z3.unsat

    goods = tuple(range(8))
    support_cases = 0
    proper_cases = 0
    equality_cases = 0
    containment_failures = 0
    for base_root in subsets(goods):
        exterior = frozenset(goods) - base_root
        for current_root in subsets(goods):
            plus_support = current_root - base_root
            for anchor in subsets(tuple(plus_support)):
                if not anchor:
                    continue
                for packet_support in subsets(tuple(anchor)):
                    if not packet_support:
                        continue
                    support_cases += 1
                    containment_failures += int(
                        not packet_support <= anchor <= plus_support
                    )
                    if packet_support < plus_support:
                        proper_cases += 1
                    elif packet_support == plus_support:
                        equality_cases += 1
                    assert anchor <= exterior

    assert support_cases > 0
    assert proper_cases > 0 and equality_cases > 0
    assert containment_failures == 0

    theorem = ROOT / "results/ROOT_CRITICAL_OLD_ANCHOR_SIGNED_RETURN_OR_BLOCKER_THEOREM_20260814.md"
    localization = ROOT / "results/ROOT_RETIRED_PACKET_OLD_ANCHOR_CRITICAL_LOCALIZATION_THEOREM_20260814.md"
    signed = ROOT / "results/SIGNED_MISSING_BASE_PACKET_CHARGE_OR_BASE_CONTAINMENT_THEOREM_20260814.md"
    clean = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    equality_theorem = ROOT / "results/ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()

    theorem_text = theorem.read_text()
    assert "K\\subseteq A\\subseteq S^+" in theorem_text
    assert "exact repeated blocker" in theorem_text
    assert "all-donor global supplier star" in theorem_text

    return {
        "schema": "root-critical-old-anchor-signed-return-or-blocker-audit-v1",
        "status": "CRITICAL_OLD_ANCHOR_PACKET_REDUCED_TO_SIGNED_RETURN_BLOCKER",
        "proper_signed_return_is_strict": proper_signed_return_is_strict,
        "complete_signed_return_is_equality": complete_signed_return_is_equality,
        "support_cases_checked": support_cases,
        "proper_signed_return_support_cases": proper_cases,
        "equality_signed_return_support_cases": equality_cases,
        "anchor_packet_in_signed_plus_containment_failures": containment_failures,
        "historical_reversibility_used": False,
        "global_supplier_star_used": False,
        "repeated_blocker_well_foundedness_proved": False,
        "full_T_L_times_theorem_closed": False,
        "smallest_remaining_operation": (
            "terminate or refute the exact repeated signed-return blocker"
        ),
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                theorem,
                localization,
                signed,
                clean,
                equality_theorem,
                contract,
                script,
            )
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
