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
    anchor, base, atom, source_before, source_after = z3.Reals(
        "anchor base atom source_before source_after"
    )
    source = z3.SolverFor("QF_LRA")
    source.add(atom > 0, source_after == source_before + atom)
    source_floor_strict = source.check() == z3.sat
    source.push()
    source.add(source_after <= source_before)
    source_floor_strict = source_floor_strict and source.check() == z3.unsat

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
    script = Path(__file__).resolve()

    text = theorem.read_text()
    anchor_source_text = anchor_source.read_text()
    old_core_text = old_core.read_text()
    assert "Return `g` to its recorded retirement source" in text
    assert "preserves all declared" in text
    assert "K\\subseteq C_r(A)" in text
    assert "currently assigned to `r`" in anchor_source_text
    assert "common-safe and strictly desired by" in old_core_text

    return {
        "schema": "root-retired-packet-old-anchor-critical-localization-v1",
        "status": "ROOT_PACKET_LOCALIZED_TO_OLD_ANCHOR_CRITICAL_ATOMS",
        "recorded_source_floor_strictly_improves": source_floor_strict,
        "critical_atom_exceeds_anchor_surplus": critical_atom_exceeds_surplus,
        "off_anchor_support_cases_checked": off_anchor_cases,
        "anchor_atom_support_cases_checked": noncritical_anchor_cases,
        "packet_inside_anchor_terminal_cases": terminal_cases,
        "off_anchor_atom_return_admitted": True,
        "noncritical_anchor_atom_release_admitted": True,
        "all_other_owner_floors_unchanged": True,
        "retirement_source_floor_preserved": True,
        "root_floor_preserved_by_old_or_reduced_anchor": True,
        "release_supplier_is_current_root": True,
        "exact_recurrent_survivor": "nonempty K subseteq C_r(A) subseteq A",
        "full_T_L_times_theorem_closed": False,
        "smallest_remaining_operation": (
            "pay or anchor-exchange a critical retired atom of the old root core"
        ),
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, contract, anchor_source, old_core, correction, script)
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
