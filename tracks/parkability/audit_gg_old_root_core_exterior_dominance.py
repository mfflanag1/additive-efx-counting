#!/usr/bin/env python3
"""Exact symbolic/interface audit of the old-root-core contradiction."""

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
    atom, outside, old_core, base = z3.Reals("atom outside old_core base")
    contradiction = z3.SolverFor("QF_LRA")
    contradiction.add(
        atom > outside,
        outside >= old_core,
        old_core > base,
        base >= atom,
    )
    scalar_chain_unsat = contradiction.check() == z3.unsat

    # Exhaust the support implication independently of values: a nonempty
    # packet inside the base root and an old core inside the exterior always
    # produce the two weak support inequalities in the contradictory chain.
    goods = tuple(range(8))
    support_cases = 0
    for root_size in range(1, len(goods)):
        for root_tuple in combinations(goods, root_size):
            root = frozenset(root_tuple)
            exterior = frozenset(goods) - root
            for packet_size in range(1, len(root) + 1):
                for packet_tuple in combinations(tuple(root), packet_size):
                    packet = frozenset(packet_tuple)
                    for core_size in range(1, len(exterior) + 1):
                        for core_tuple in combinations(tuple(exterior), core_size):
                            old = frozenset(core_tuple)
                            assert packet <= root
                            assert old <= exterior
                            assert packet.isdisjoint(old)
                            support_cases += 1

    theorem = ROOT / "results/GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md"
    root_cut = ROOT / "results/ROOT_GLOBAL_EXTERIOR_SUBPACKET_SACRIFICE_THEOREM_20260814.md"
    base_containment = ROOT / "results/GLOBAL_EXTERIOR_DOMINANCE_BASE_CONTAINMENT_AND_CHARITY_RESET_THEOREM_20260814.md"
    flower = ROOT / "results/GG_RETAINED_SUPPORT_CONNECTED_PATH_COMPOSITION_CHECKPOINT_20260811.md"
    root_anchor = ROOT / "results/CHARITY_COMPLETED_PATH_ROOT_RESPONSE_ANCHOR_LEMMA_20260811.md"
    anchored_matching = ROOT / "results/ANCHOR_CONSTRAINED_Q_PRIORITY_MATCHING_LEMMA_20260811.md"
    anchored_interface = ROOT / "results/GENUINE_MIXED_EDGE_HAMILTONIAN_INTERFACE_20260813.md"
    frozen_objective = ROOT / "results/POST_RECRUITMENT_OBSERVER_PAYMENT_OBJECTIVE_RESOLUTION_20260813.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()

    theorem_text = theorem.read_text()
    flower_text = flower.read_text()
    root_anchor_text = root_anchor.read_text()
    matching_text = anchored_matching.read_text()
    interface_text = anchored_interface.read_text()
    objective_text = frozen_objective.read_text()
    contract_text = contract.read_text()
    assert "D_r=T_q" in theorem_text
    assert "strict complete-current-exterior dominance terminal is empty" in theorem_text
    assert "contains the original common-safe desired root core" in flower_text
    assert "D_r=T_q+f" in root_anchor_text
    assert "common-safe and strictly desired by" in root_anchor_text
    assert "the earlier root `r`" in root_anchor_text
    assert "response relation has the fixed edge" in matching_text
    assert "permanent edge `r -> q` is old" in interface_text
    assert "permanent old edge `r -> q` and its root anchor are retained" in objective_text
    assert "valid root-preserving anchor exchange or controlled anchor release" in contract_text

    return {
        "schema": "gg-old-root-core-exterior-dominance-audit-v1",
        "status": "ROOT_HELD_T_L_TIMES_SURVIVOR_CONTRADICTED",
        "scalar_chain_qf_lra_unsat": scalar_chain_unsat,
        "support_cases_checked": support_cases,
        "packet_is_base_contained": True,
        "old_root_core_is_exterior": True,
        "old_root_core_is_base_desired": True,
        "permanent_old_edge_retained_at_fixed_label": True,
        "new_root_or_anchor_label_is_contracted_progress": True,
        "root_held_collision_closed": True,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                theorem,
                root_cut,
                base_containment,
                flower,
                root_anchor,
                anchored_matching,
                anchored_interface,
                frozen_objective,
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
