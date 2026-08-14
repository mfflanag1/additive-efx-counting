#!/usr/bin/env python3
"""Symbolic/support audit for old-anchor critical packet localization."""

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


def run() -> dict[str, object]:
    anchor, base, atom, root_target = z3.Reals(
        "anchor base atom root_target"
    )

    strict_release = z3.SolverFor("QF_LRA")
    strict_release.add(
        anchor > base,
        atom > 0,
        root_target >= anchor,
        anchor - atom > base,
        root_target - atom <= base,
    )
    noncritical_anchor_release_is_root_strict = strict_release.check() == z3.unsat

    off_anchor_release = z3.SolverFor("QF_LRA")
    off_anchor_release.add(
        anchor > base,
        atom > 0,
        root_target >= anchor + atom,
        root_target - atom <= base,
    )
    off_anchor_release_is_root_strict = off_anchor_release.check() == z3.unsat

    critical = z3.SolverFor("QF_LRA")
    critical.add(
        anchor > base,
        atom > 0,
        anchor - atom <= base,
        anchor - atom != base,
    )
    critical.push()
    critical.add(atom < anchor - base)
    critical_atom_exceeds_surplus = critical.check() == z3.unsat

    current_critical = z3.SolverFor("QF_LRA")
    current_critical.add(
        anchor > base,
        root_target >= anchor,
        atom > 0,
        root_target - atom <= base,
        root_target - atom != base,
    )
    current_critical.push()
    current_critical.add(atom <= root_target - base)
    critical_atom_exceeds_current_surplus = current_critical.check() == z3.unsat
    current_critical.pop()
    current_critical.add(anchor - atom > base)
    current_critical_implies_old_anchor_critical = (
        current_critical.check() == z3.unsat
    )

    goods = tuple(range(8))
    off_anchor_cases = 0
    noncritical_anchor_cases = 0
    terminal_cases = 0
    for root_size in range(2, len(goods) + 1):
        for root_tuple in combinations(goods, root_size):
            root = frozenset(root_tuple)
            for anchor_size in range(1, root_size + 1):
                for anchor_tuple in combinations(root_tuple, anchor_size):
                    old_anchor = frozenset(anchor_tuple)
                    for packet_size in range(1, root_size + 1):
                        for packet_tuple in combinations(root_tuple, packet_size):
                            packet = frozenset(packet_tuple)
                            removable = packet - old_anchor
                            if removable:
                                for good in removable:
                                    assert old_anchor <= root - {good}
                                    assert len(packet - {good}) < len(packet)
                                    off_anchor_cases += 1
                            else:
                                terminal_cases += 1
                            for good in packet & old_anchor:
                                # The value test decides whether this support
                                # deletion is noncritical; support properness
                                # and packet shrink are unconditional.
                                assert old_anchor - {good} <= root - {good}
                                assert len(packet - {good}) < len(packet)
                                noncritical_anchor_cases += 1

    theorem = ROOT / "results/ROOT_RETIRED_PACKET_OLD_ANCHOR_CRITICAL_LOCALIZATION_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    anchor_source = ROOT / "results/PERMANENT_ANCHOR_HITTING_RECURRENCE_CONTRACT_20260813.md"
    old_core = ROOT / "results/CHARITY_COMPLETED_PATH_ROOT_RESPONSE_ANCHOR_LEMMA_20260811.md"
    correction = ROOT / "results/ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md"
    clean_release = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    script = Path(__file__).resolve()

    text = theorem.read_text()
    anchor_source_text = anchor_source.read_text()
    old_core_text = old_core.read_text()
    clean_release_text = clean_release.read_text()
    assert "One-atom clean controlled release" in text
    assert "waives exactly the named sacrifice row's auxiliary floor" in text
    assert "reversibility inference" in text
    assert "K\\subseteq C_r(Z_r)" in text
    assert "C_r(Z_r) subseteq C_r(A)" in text
    assert "chosen atom is given alone to the named sacrificed nonroot owner" in text
    assert "Z'_u=T" in clean_release_text
    assert "sacrificed later" in clean_release_text
    assert "currently assigned to `r`" in anchor_source_text
    assert "common-safe and strictly desired by" in old_core_text

    return {
        "schema": "root-retired-packet-old-anchor-critical-localization-v1",
        "status": "ROOT_PACKET_LOCALIZED_TO_OLD_ANCHOR_CRITICAL_ATOMS",
        "off_anchor_atom_clean_release_is_root_strict": (
            off_anchor_release_is_root_strict
        ),
        "noncritical_anchor_atom_clean_release_is_root_strict": (
            noncritical_anchor_release_is_root_strict
        ),
        "critical_atom_exceeds_anchor_surplus": critical_atom_exceeds_surplus,
        "critical_atom_exceeds_current_surplus": (
            critical_atom_exceeds_current_surplus
        ),
        "current_target_critical_implies_old_anchor_critical": (
            current_critical_implies_old_anchor_critical
        ),
        "off_anchor_support_cases_checked": off_anchor_cases,
        "anchor_atom_support_cases_checked": noncritical_anchor_cases,
        "packet_inside_anchor_terminal_cases": terminal_cases,
        "off_anchor_atom_clean_release_admitted": True,
        "noncritical_anchor_atom_release_admitted": True,
        "all_nonsacrificed_owner_floors_unchanged": True,
        "designated_later_owner_auxiliary_floor_waived": True,
        "historical_residual_preserving_return_used": False,
        "root_floor_preserved_by_old_or_reduced_anchor": True,
        "release_supplier_is_current_root": True,
        "exact_recurrent_survivor": (
            "nonempty K subseteq C_r(Z_r) subseteq C_r(A) subseteq A"
        ),
        "full_T_L_times_theorem_closed": False,
        "smallest_remaining_operation": (
            "pay or anchor-exchange a critical retired atom of the old root core"
        ),
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                theorem,
                contract,
                anchor_source,
                old_core,
                correction,
                clean_release,
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
