#!/usr/bin/env python3
"""Exact set/value audit of equality packet-spread admission."""

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
    plus, minus, delta, atom = z3.Reals("plus minus delta atom")
    multigood = z3.SolverFor("QF_LRA")
    multigood.add(
        plus - minus == delta,
        atom > 0,
        z3.Not(minus > plus - atom - delta),
    )
    leave_one_strict_identity = multigood.check() == z3.unsat

    donated = z3.SolverFor("QF_LRA")
    donated.add(atom > 0, z3.Not(atom > 0))
    singleton_offpacket_root_gain = donated.check() == z3.unsat

    atom_value, common = z3.Reals("atom_value common")
    strict_cut = z3.SolverFor("QF_LRA")
    strict_cut.add(common < atom_value - delta, atom_value <= delta + common)
    strict_atomwise_charge_exact = strict_cut.check() == z3.unsat

    packet_spread_cases = 0
    whole_hits = 0
    singleton_offpacket_cases = 0
    universe = tuple(range(8))
    for base_root in subsets(universe):
        outside = frozenset(universe) - base_root
        if len(outside) < 4:
            continue
        for plus_support in subsets(tuple(outside)):
            if not plus_support:
                continue
            current_root = base_root | plus_support
            packet = plus_support | frozenset(
                list(sorted(base_root))[: min(2, len(base_root))]
            )
            if len(plus_support) >= 2:
                good = min(plus_support)
                released = plus_support - {good}
                root_hit = packet - released
                return_hit = released
                assert root_hit < packet and return_hit < packet
                whole_hits += int(packet <= root_hit) + int(packet <= return_hit)
                packet_spread_cases += 1
            else:
                candidates = outside - packet
                assert len(candidates) >= 3
                h = min(candidates)
                assert h not in current_root and h not in packet
                restored_hit = packet & base_root
                return_hit = plus_support
                if len(packet) > 1:
                    assert restored_hit < packet and return_hit < packet
                else:
                    assert not restored_hit and return_hit == packet
                singleton_offpacket_cases += 1

    assert packet_spread_cases > 0
    assert singleton_offpacket_cases > 0
    assert whole_hits == 0

    theorem = ROOT / "results/ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md"
    equality = ROOT / "results/NONDEGENERATE_ROOT_EQUALITY_BASE_RESTORATION_LEMMA_20260814.md"
    strict = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    base_spread = ROOT / "results/SUPPLIER_ALIGNED_BASE_DONATION_PACKET_SPREAD_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "No equality instance of the packet-price cut survives" in theorem_text
    assert "strict aggregate underpayment" in theorem_text

    return {
        "schema": "root-equality-base-restoration-packet-spread-admission-audit-v1",
        "status": "ROOT_PACKET_PRICE_EQUALITY_ELIMINATED_STRICT_UNDERPAYMENT_REMAINS",
        "leave_one_strict_identity": leave_one_strict_identity,
        "singleton_offpacket_root_gain": singleton_offpacket_root_gain,
        "packet_spread_cases_checked": packet_spread_cases,
        "proper_split_whole_packet_hits": whole_hits,
        "singleton_offpacket_cases_checked": singleton_offpacket_cases,
        "strict_atomwise_charge_exact": strict_atomwise_charge_exact,
        "other_retired_label_may_change": True,
        "global_multilabel_well_foundedness_proved": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, equality, strict, base_spread, script)
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
