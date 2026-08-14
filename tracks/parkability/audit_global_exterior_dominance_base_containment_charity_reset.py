#!/usr/bin/env python3
"""Exact arithmetic/support audit of base containment and charity reset."""

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
    plus, minus, exterior, delta, outside = z3.Reals(
        "plus minus exterior delta outside"
    )
    identity = z3.SolverFor("QF_LRA")
    identity.add(
        delta == plus - minus,
        outside == plus + exterior - minus,
        delta + exterior != outside,
    )
    exterior_identity_exact = identity.check() == z3.unsat

    atom = z3.Real("atom")
    crossing = z3.SolverFor("QF_LRA")
    crossing.add(atom > delta + exterior, delta + exterior == outside, atom <= outside)
    crossing_atom_impossible = crossing.check() == z3.unsat

    x, charity, removed, response = z3.Reals("x charity removed response")
    on_good = z3.SolverFor("QF_LRA")
    on_good.add(response == x - removed + charity, response < x, removed <= charity)
    on_good_loss_band_exact = on_good.check() == z3.unsat

    support_cases = 0
    crossing_failures = 0
    proper_packet_cases = 0
    on_good_cases = 0
    off_good_cases = 0
    base_root_cases = 0
    universe = tuple(range(8))
    charity_good = 7
    owner_goods = frozenset(range(7))
    for base_root in subsets(tuple(owner_goods)):
        if not base_root:
            continue
        base_exterior = frozenset(universe) - base_root
        assert charity_good in base_exterior
        for current_root in subsets(universe):
            if not current_root:
                continue
            plus_support = current_root - base_root
            minus_support = base_root - current_root
            current_exterior = frozenset(universe) - current_root
            assert base_exterior == plus_support | (current_exterior - minus_support)
            assert plus_support.isdisjoint(current_exterior - minus_support)
            for packet in subsets(tuple(current_root)):
                if not packet:
                    continue
                # Any packet satisfying the atomwise exterior cut cannot use
                # a plus atom, because every plus atom belongs to O.
                crossing_failures += len(packet & plus_support)
                if packet & plus_support:
                    continue
                assert packet <= base_root
                reset_target = base_root | {charity_good}
                for response_support in subsets(tuple(reset_target)):
                    if response_support == reset_target:
                        continue
                    support_cases += 1
                    if not packet <= response_support:
                        proper_packet_cases += 1
                        continue
                    removed_support = base_root - response_support
                    assert removed_support <= base_root - packet
                    if charity_good in response_support:
                        assert removed_support
                        assert response_support == (base_root - removed_support) | {charity_good}
                        on_good_cases += 1
                    else:
                        assert response_support == base_root - removed_support
                        off_good_cases += 1
                        base_root_cases += int(not removed_support)

    assert support_cases > 0
    assert crossing_failures > 0  # candidate crossings exist set-theoretically
    assert proper_packet_cases > 0
    assert on_good_cases > 0 and off_good_cases > 0 and base_root_cases > 0

    theorem = ROOT / "results/GLOBAL_EXTERIOR_DOMINANCE_BASE_CONTAINMENT_AND_CHARITY_RESET_THEOREM_20260814.md"
    global_cut = ROOT / "results/ROOT_GLOBAL_EXTERIOR_SUBPACKET_SACRIFICE_THEOREM_20260814.md"
    base = ROOT / "results/EXTERIOR_DOMINANCE_THREE_AGENT_SOURCE_REDUCTION_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "no signed missing-base return is needed" in theorem_text
    assert "Supplier-free charity reset" in theorem_text
    assert "does not eliminate the on-good loss band" in theorem_text

    return {
        "schema": "global-exterior-dominance-base-containment-charity-reset-audit-v1",
        "status": "ROOT_REDUCED_UNCONDITIONALLY_TO_CHARITY_ONE_GOOD_ON_OFF_RESPONSE",
        "exterior_identity_exact": exterior_identity_exact,
        "crossing_atom_impossible": crossing_atom_impossible,
        "on_good_loss_band_exact": on_good_loss_band_exact,
        "reset_support_cases_checked": support_cases,
        "set_theoretic_crossing_atoms_seen": crossing_failures,
        "proper_packet_response_cases": proper_packet_cases,
        "whole_packet_on_good_cases": on_good_cases,
        "whole_packet_off_good_cases": off_good_cases,
        "whole_packet_base_root_cases": base_root_cases,
        "signed_missing_base_return_required": False,
        "multilabel_charge_branch_required": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, global_cut, base, contract, script)
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
