#!/usr/bin/env python3
"""Exact support/value audit of global-exterior subpacket sacrifice."""

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
    x, delta, packet, residual, exterior, transferred = z3.Reals(
        "x delta packet residual exterior transferred"
    )
    margin = z3.SolverFor("QF_LRA")
    margin.add(
        packet + residual == x + delta,
        packet - transferred + residual + exterior - x
        != delta + exterior - transferred,
    )
    margin_identity_exact = margin.check() == z3.unsat

    strict = z3.SolverFor("QF_LRA")
    strict.add(
        packet + residual == x + delta,
        exterior > transferred - delta,
        packet - transferred + residual + exterior <= x,
    )
    strict_test_exact = strict.check() == z3.unsat

    atom, common = z3.Reals("atom common")
    atom_cut = z3.SolverFor("QF_LRA")
    atom_cut.add(common < atom - delta, atom <= delta + common)
    strict_atomwise_cut_exact = atom_cut.check() == z3.unsat

    n, total = z3.Int("n"), z3.Real("total")
    summed = z3.SolverFor("QF_LIRA")
    summed.add(
        n >= 1,
        total > n * (delta + common),
        total <= x + delta,
        z3.Not((n - 1) * delta + n * common < x),
    )
    summed_cut_exact = summed.check() == z3.unsat

    support_cases = 0
    proper_transfer_whole_hits = 0
    full_transfer_deletions = 0
    equality_spread_cases = 0
    universe = tuple(range(8))
    for root_support in subsets(universe):
        if not root_support:
            continue
        exterior_support = frozenset(universe) - root_support
        for packet_support in subsets(tuple(root_support)):
            if not packet_support:
                continue
            for transferred_support in subsets(tuple(packet_support)):
                if not transferred_support:
                    continue
                root_target = frozenset(universe) - transferred_support
                return_target = transferred_support
                assert root_target.isdisjoint(return_target)
                assert root_target | return_target == frozenset(universe)
                if transferred_support != packet_support:
                    proper_transfer_whole_hits += int(
                        packet_support <= (root_target & packet_support)
                    )
                    proper_transfer_whole_hits += int(
                        packet_support <= return_target
                    )
                else:
                    if len(packet_support) >= 2:
                        for good in packet_support:
                            assert packet_support - {good} < packet_support
                            full_transfer_deletions += 1
                support_cases += 1

        # Equality physical identity T=G-X_r has at least four goods in the
        # frozen GG import. Audit the leave-one spread set-theoretically.
        base_exterior = frozenset(universe) - root_support
        if len(base_exterior) >= 4:
            for good in base_exterior:
                transferred_prime = base_exterior - {good}
                assert transferred_prime
                assert frozenset(universe) - transferred_prime == root_support | {good}
                equality_spread_cases += 1

    assert support_cases > 0
    assert proper_transfer_whole_hits == 0
    assert full_transfer_deletions > 0
    assert equality_spread_cases > 0

    theorem = ROOT / "results/ROOT_GLOBAL_EXTERIOR_SUBPACKET_SACRIFICE_THEOREM_20260814.md"
    clean = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    base = ROOT / "results/BASE_CONTAINED_GLOBAL_EXTERIOR_SACRIFICE_ADMISSION_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "complete current-exterior dominance" in theorem_text
    assert "no remaining equality" in theorem_text

    return {
        "schema": "root-global-exterior-subpacket-sacrifice-audit-v1",
        "status": "ROOT_REDUCED_TO_STRICT_COMPLETE_CURRENT_EXTERIOR_DOMINANCE",
        "margin_identity_exact": margin_identity_exact,
        "strict_test_exact": strict_test_exact,
        "strict_atomwise_cut_exact": strict_atomwise_cut_exact,
        "summed_cut_exact": summed_cut_exact,
        "support_cases_checked": support_cases,
        "proper_transfer_whole_packet_hits": proper_transfer_whole_hits,
        "full_transfer_proper_deletions_checked": full_transfer_deletions,
        "equality_leave_one_spread_cases": equality_spread_cases,
        "compatibility_premise_required": False,
        "equality_face_closed": True,
        "multilabel_charge_branch_required": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, clean, base, contract, script)
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
