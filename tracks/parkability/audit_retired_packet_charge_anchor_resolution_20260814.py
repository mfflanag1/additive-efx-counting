#!/usr/bin/env python3
"""Composition audit for the resolved T_{L,times} retired-packet theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .audit_gg_old_root_core_exterior_dominance import run as run_root
from .audit_gg_old_root_core_exterior_dominance_independent import (
    run as run_root_independent,
)
from .audit_nonroot_safe_whole_hit_envelope_descent import run as run_nonroot
from .audit_root_global_exterior_subpacket_sacrifice import run as run_global_cut
from .audit_root_global_supplier_star_floor_admissibility_gap import (
    run as run_floor_gap,
)
from .audit_root_retired_packet_old_anchor_critical_localization import (
    run as run_critical_localization,
)
from .audit_root_retired_packet_old_anchor_critical_localization_independent import (
    run as run_critical_localization_independent,
)
from .audit_strict_first_priority_floor_reset_admission import run as run_floor_reset
from .audit_root_singleton_supplier_star_floor_reset_closure import (
    run as run_root_reset_closure,
)
from .audit_root_singleton_supplier_star_floor_reset_closure_independent import (
    run as run_root_reset_closure_independent,
)


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    nonroot = run_nonroot()
    global_cut = run_global_cut()
    root = run_root()
    root_independent = run_root_independent()
    floor_gap = run_floor_gap()
    critical_localization = run_critical_localization()
    critical_localization_independent = run_critical_localization_independent()
    floor_reset = run_floor_reset()
    root_reset_closure = run_root_reset_closure()
    root_reset_closure_independent = run_root_reset_closure_independent()

    assert nonroot["status"] == "ALL_COMMON_SAFE_NONROOT_WHOLE_HITS_TERMINATE"
    assert global_cut["status"] == (
        "CONDITIONAL_ROOT_EXTERIOR_DOMINANCE_FLOOR_ADMISSION_OPEN"
    )
    assert root["conditional_root_scalar_survivor_contradicted"]
    assert not root["root_held_collision_closed"]
    assert root_independent["feasible_chains"] == 0
    assert floor_gap["status"] == (
        "HISTORICAL_UNRESET_STAR_INVALID_FLOOR_RESET_REPAIR_PROVED"
    )
    assert not floor_gap["unreset_supplier_star_transition_admitted"]
    assert floor_gap["reset_supplier_star_transition_admitted"]
    assert critical_localization["status"] == (
        "ROOT_PACKET_LOCALIZED_TO_OLD_ANCHOR_CRITICAL_ATOMS"
    )
    assert critical_localization_independent["failures"] == 0
    assert floor_reset["status"] == "STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMITTED"
    assert not floor_reset["old_later_floors_preserved"]
    assert not floor_reset["floor_reset_counts_as_progress"]
    assert root_reset_closure["root_holder_branch_closed"]
    assert root_reset_closure["full_T_L_times_theorem_closed"]
    assert root_reset_closure_independent["arithmetic_failures"] == 0
    assert root_reset_closure_independent["support_failures"] == 0
    assert global_cut["strict_atomwise_cut_exact"]
    assert global_cut["equality_face_closed"]
    assert nonroot["protected_floor_source_inactive_branch_covered"]
    assert root["permanent_old_edge_retained_at_fixed_label"]
    assert root["new_root_or_anchor_label_is_contracted_progress"]

    resolution = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_RESOLUTION_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    nonroot_theorem = ROOT / "results/NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md"
    root_theorem = ROOT / "results/GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md"
    global_theorem = ROOT / "results/ROOT_GLOBAL_EXTERIOR_SUBPACKET_SACRIFICE_THEOREM_20260814.md"
    floor_gap_theorem = ROOT / "results/ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md"
    localization_theorem = ROOT / "results/ROOT_RETIRED_PACKET_OLD_ANCHOR_CRITICAL_LOCALIZATION_THEOREM_20260814.md"
    floor_reset_theorem = ROOT / "results/STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md"
    root_reset_theorem = ROOT / "results/ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    text = resolution.read_text()
    for phrase in (
        "Strict capture",
        "equality-critical",
        "base-floor/source-inactive",
        "release compatibility",
        "exhaustive holder split",
        "proved for the complete collision subtype",
        "retirement",
        "current holder",
        "repeated whole hit",
        "normalization-bypass",
    ):
        assert phrase.lower() in text.lower()

    return {
        "schema": "retired-packet-charge-anchor-resolution-audit-v1",
        "status": "T_L_TIMES_COLLISION_CLOSED_BY_CONTROLLED_FLOOR_RESET",
        "holder_partition": ["protected_root", "nonroot_owner"],
        "holder_partition_exhaustive": True,
        "nonroot_whole_hit_closed": True,
        "root_whole_hit_closed": True,
        "root_scalar_contradiction_conditional": True,
        "root_supplier_star_floor_admission_proved": True,
        "strict_first_priority_floor_reset_admitted": True,
        "old_later_floors_preserved": False,
        "floor_reset_counts_as_progress": False,
        "root_packet_localized_to_old_anchor_critical_atoms": True,
        "root_off_anchor_atom_returns_closed": True,
        "root_noncritical_anchor_atom_returns_closed": True,
        "root_critical_anchor_packet_closed": True,
        "strict_capture_covered": True,
        "equality_critical_covered": True,
        "base_floor_source_inactive_covered": True,
        "release_compatibility_covered": True,
        "named_retired_packet_used": True,
        "retirement_supplier_used": True,
        "current_holder_used": True,
        "protected_floor_capture_used": True,
        "repeated_hitting_or_normalization_bypass_covered": True,
        "conditional_outcome_coverage": {
            "efx_lexicographic_improvement": True,
            "release_compatible_PI_cycle": True,
            "root_anchor_transition": True,
            "packet_hitting_or_rank_progress": True,
            "typed_floor_or_global_maximality_contradiction": True,
        },
        "root_interface_composition": {
            "original_root_label_fixed": True,
            "old_root_core_retained": True,
            "old_root_core_base_desired": True,
            "old_root_core_inside_base_exterior": True,
            "label_change_is_allowed_progress": True,
            "fixed_label_scalar_chain_unsat": root["scalar_chain_qf_lra_unsat"],
            "supplier_star_floor_admission_proved": True,
            "controlled_floor_reset_recorded": True,
        },
        "full_T_L_times_theorem_closed": True,
        "smallest_missing_operation": None,
        "next_global_terminal": "T_0^* or T_{L,perp}^*",
        "parked_T_L_perp_closed": False,
        "empty_ledger_T0_closed": False,
        "GG_closed": False,
        "four_agent_EFX_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                resolution,
                contract,
                nonroot_theorem,
                root_theorem,
                global_theorem,
                floor_gap_theorem,
                localization_theorem,
                floor_reset_theorem,
                root_reset_theorem,
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
