#!/usr/bin/env python3
"""Integrity and graph audit for the referee-corrected GG composition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


NODES = tuple([f"G{i}" for i in range(11)] + ["EFX", "PI", "T*"])
EDGES = (
    ("G0", "EFX"), ("G0", "PI"), ("G0", "G1"),
    ("G1", "EFX"), ("G1", "G2"),
    ("G2", "PI"), ("G2", "G3"), ("G2", "G4"),
    ("G3", "EFX"), ("G3", "G4"),
    ("G4", "EFX"), ("G4", "PI"), ("G4", "G5"),
    ("G5", "EFX"), ("G5", "G6"),
    ("G6", "EFX"), ("G6", "G7"),
    ("G7", "EFX"), ("G7", "G8"),
    ("G8", "EFX"), ("G8", "G9"), ("G8", "T*"),
    ("G9", "PI"), ("G9", "G10"),
    ("G10", "EFX"), ("G10", "PI"), ("G10", "T*"),
)


def reachable(start: str) -> set[str]:
    seen = {start}
    frontier = [start]
    while frontier:
        node = frontier.pop()
        for left, right in EDGES:
            if left == node and right not in seen:
                seen.add(right)
                frontier.append(right)
    return seen


def run(root: Path) -> dict:
    result_dir = root / "results"
    dependencies = (
        "GG_RETAINED_SUPPORT_CONNECTED_PATH_COMPOSITION_CHECKPOINT_20260811.md",
        "gg_retained_support_connected_path_composition_audit.json",
        "CLOSING_SOURCE_DELETION_RETURN_RESIDUAL_COMPLETION_LEMMA_20260811.md",
        "CLOSING_SOURCE_DELETION_RETURN_REFEREE_REPORT_20260812.md",
        "closing_source_deletion_return_referee_audit.json",
        "GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md",
        "gg_rank_reset_raw_potential_refutation_audit.json",
        "GG_HISTORICAL_SUPPORT_LEDGER_STAGNATION_REFUTATION_20260811.md",
        "gg_historical_support_ledger_stagnation_audit.json",
        "PAID_RESPONSE_PATH_CORE_ROTATION_LEMMA_20260813.md",
        "paid_response_path_core_rotation_audit.json",
        "RESIDUAL_ESSENTIAL_PATH_CORE_TOPUP_LEMMA_20260813.md",
        "residual_essential_path_core_topup_audit.json",
        "ENDPOINT_HOLE_CORE_EXCHANGE_SELECTOR_LEMMA_20260813.md",
        "endpoint_hole_core_exchange_selector_audit.json",
        "FOUR_OLD_CORE_SHORTCUT_AND_INTERFACE_REFUTATION_20260813.md",
        "four_old_core_shortcut_interface_audit.json",
        "GENUINE_MIXED_EDGE_HAMILTONIAN_INTERFACE_20260813.md",
        "genuine_mixed_edge_hamiltonian_interface_audit.json",
        "GENERAL_MIXED_EDGE_DELETION_RETURN_COMPOSITION_20260813.md",
        "general_mixed_edge_deletion_return_composition_audit.json",
        "SIGNED_SURPLUS_PREFIX_RECRUITMENT_LEMMA_20260813.md",
        "signed_surplus_prefix_recruitment_audit.json",
        "FORWARD_CHORD_CORE_SPLIT_OR_ANCHOR_CAPTURE_LEMMA_20260813.md",
        "forward_chord_core_split_or_anchor_capture_audit.json",
        "BACKWARD_RESPONSE_CYCLE_OR_BOUNDARY_CAPTURE_LEMMA_20260813.md",
        "backward_response_cycle_or_boundary_capture_audit.json",
        "ANCHOR_TARGET_NONOVERLAP_GROWTH_OR_NESTED_EDGE_LEMMA_20260813.md",
        "anchor_target_nonoverlap_growth_or_nested_edge_audit.json",
        "SELECTED_POOL_SIGNED_SURPLUS_RECRUITMENT_RESOLUTION_20260813.md",
        "selected_pool_signed_surplus_recruitment_resolution_audit.json",
        "ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md",
        "root_sourced_complete_signed_residual_compensation_audit.json",
        "SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md",
        "supplier_saturation_does_not_force_mixed_cycle_payment_audit.json",
        "SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md",
        "supplier_saturated_payment_refutation_independent_audit.json",
        "MIXED_CYCLE_DECORATED_HEAD_LOCALIZATION_LEMMA_20260813.md",
        "mixed_cycle_decorated_head_localization_audit.json",
        "DECORATED_HEAD_ALTERNATING_MINIMAL_RESPONSE_LEMMA_20260813.md",
        "decorated_head_alternating_minimal_response_audit.json",
        "DECORATED_HEAD_PROTECTED_BUNDLE_HALL_DICHOTOMY_20260813.md",
        "decorated_head_protected_bundle_hall_dichotomy_audit.json",
        "ONE_HEAD_PROTECTED_SPLIT_OR_CAPTURE_LEMMA_20260813.md",
        "one_head_protected_split_or_capture_audit.json",
        "ONE_HEAD_NONROOT_COMPRESSION_STAR_HANDOFF_LEMMA_20260813.md",
        "one_head_nonroot_compression_star_handoff_audit.json",
        "ALTERNATING_TWO_HEAD_ROOT_COVERED_COMPRESSION_LEMMA_20260813.md",
        "alternating_two_head_root_covered_compression_audit.json",
        "ROOT_ANCHORED_ONE_HEAD_TWO_HOLE_SELECTOR_LEMMA_20260813.md",
        "root_anchored_one_head_two_hole_selector_audit.json",
        "ROOT_SOURCED_ANCHOR_RETAINING_SACRIFICE_HANDOFF_LEMMA_20260813.md",
        "root_sourced_anchor_retaining_sacrifice_handoff_audit.json",
        "ENLARGED_ROOT_TARGET_ANCHOR_HITTING_TRICHOTOMY_20260813.md",
        "enlarged_root_target_anchor_hitting_trichotomy_audit.json",
        "PERMANENT_ANCHOR_HITTING_RECURRENCE_CONTRACT_20260813.md",
        "PERMANENT_ANCHOR_MINIMAL_RESPONSE_PEEL_OR_RESELECT_THEOREM_20260813.md",
        "permanent_anchor_minimal_response_peel_or_reselect_audit.json",
        "permanent_anchor_minimal_response_peel_or_reselect_independent_audit.json",
        "GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md",
        "GLOBAL_RETIRED_ROOT_SUPPORT_G0_G10_TRANSITION_AUDIT_20260813.md",
        "RETIRED_PACKET_SELECTOR_COLLISION_NORMALIZATION_LEMMA_20260813.md",
        "GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md",
        "GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_RESOLUTION_20260813.md",
        "GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPLETION_AUDIT_20260813.md",
        "global_retired_root_support_transition_contract_audit.json",
        "retired_packet_selector_collision_normalization_audit.json",
        "global_retired_root_support_ledger_composition_audit.json",
        "global_retired_root_support_ledger_composition_independent_audit.json",
        "RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_RESOLUTION_20260814.md",
        "GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md",
        "retired_packet_charge_anchor_resolution_20260814_audit.json",
        "gg_old_root_core_exterior_dominance_audit.json",
        "gg_old_root_core_exterior_dominance_independent_audit.json",
        "ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md",
        "root_global_supplier_star_floor_admissibility_gap_audit.json",
        "ROOT_RETIRED_PACKET_OLD_ANCHOR_CRITICAL_LOCALIZATION_THEOREM_20260814.md",
        "root_retired_packet_old_anchor_critical_localization_audit.json",
        "root_retired_packet_old_anchor_critical_localization_independent_audit.json",
    )
    records = [
        {"path": f"results/{name}", "sha256": sha256(result_dir / name)}
        for name in dependencies
    ]
    reached = reachable("G0")
    assert set(NODES) == reached
    continuing = {right for _, right in EDGES if right not in {"EFX", "PI"}}
    terminal_nodes = sorted(node for node in reached if node not in {left for left, _ in EDGES})
    assert terminal_nodes == ["EFX", "PI", "T*"]
    assert "T*" in continuing

    referee = json.loads(
        (result_dir / "closing_source_deletion_return_referee_audit.json").read_text()
    )
    assert referee["status"] == "TERMINATION_GAP_FOUND"
    assert referee["rational_local_countermodel"]["response_source_rank"] == 1
    assert referee["minimal_trimmed_countermodel"]["response_source_rank"] == 1
    assert referee["minimal_trimmed_countermodel"]["residual_partition_family_size"] == 4096
    assert referee["minimal_trimmed_countermodel"]["efx_floor_feasible_residual_partitions"] == 0

    rotation = json.loads(
        (result_dir / "paid_response_path_core_rotation_audit.json").read_text()
    )
    assert rotation["outcome_counts"] == {
        "internally_supplied_segment_cycle": 3,
        "rank_four": 2,
        "endpoint_hole_core_exchange": 1,
    }
    assert all(
        replay["efx"] for replay in rotation["frozen_witness_replays"].values()
    )
    mixed = json.loads(
        (result_dir / "residual_essential_path_core_topup_audit.json").read_text()
    )
    assert mixed["status"] == (
        "ALL_RESPONSES_REDUCED_TO_TARGET_COMPENSATION_OR_CORE_ROTATION"
    )
    exchange = json.loads(
        (result_dir / "endpoint_hole_core_exchange_selector_audit.json").read_text()
    )
    assert exchange["status"] == "EXACT_TRICHOTOMY_WITH_LOCAL_HOLE_SEPARATOR"
    shortcut = json.loads(
        (result_dir / "four_old_core_shortcut_interface_audit.json").read_text()
    )
    assert shortcut["status"] == "STATED_SPLICE_NORMAL_FORM_VACUOUS"
    genuine = json.loads(
        (result_dir / "genuine_mixed_edge_hamiltonian_interface_audit.json").read_text()
    )
    assert genuine["status"] == "INTERFACE_RECONSTRUCTED_WITH_KAPPA_BRANCH"
    general = json.loads(
        (result_dir / "general_mixed_edge_deletion_return_composition_audit.json").read_text()
    )
    assert general["status"] == "ALL_KAPPA_SCALAR_REDUCTION_POOL_WITNESS_NOT_TERMINAL"
    recruitment = json.loads(
        (result_dir / "signed_surplus_prefix_recruitment_audit.json").read_text()
    )
    assert recruitment["status"] == "RECRUITMENT_WELL_FOUNDED_POOL_SEPARATOR_SUPERSEDED"
    forward = json.loads(
        (result_dir / "forward_chord_core_split_or_anchor_capture_audit.json").read_text()
    )
    assert forward["status"] == "FORWARD_CHORD_REDUCED_TO_TWO_ANCHOR_INTERFACES"
    backward = json.loads(
        (result_dir / "backward_response_cycle_or_boundary_capture_audit.json").read_text()
    )
    assert backward["status"] == "BACKWARD_RESPONSE_REDUCED_TO_DECORATED_HEAD_EXCHANGE"
    anchor_target = json.loads(
        (result_dir / "anchor_target_nonoverlap_growth_or_nested_edge_audit.json").read_text()
    )
    assert anchor_target["status"] == "ANCHOR_TARGET_INEQUALITY_ELIMINATED_TO_NESTED_EDGE"
    resolution = json.loads(
        (result_dir / "selected_pool_signed_surplus_recruitment_resolution_audit.json").read_text()
    )
    assert resolution["status"] == "SELECTED_POOL_RECRUITMENT_GOAL_RESOLVED"
    anchor_resolution = json.loads(
        (result_dir / "permanent_anchor_minimal_response_peel_or_reselect_audit.json").read_text()
    )
    assert anchor_resolution["status"] == (
        "PERMANENT_ANCHOR_RECURRENCE_RESOLVED_BY_OUTCOMES_3_OR_4"
    )
    ledger_resolution = json.loads(
        (result_dir / "global_retired_root_support_ledger_composition_audit.json").read_text()
    )
    assert ledger_resolution["status"] == (
        "T_L_TIMES_CRITICAL_OLD_ANCHOR_PACKET_GATE_OPEN"
    )
    assert not ledger_resolution["collision_T_L_times_closed"]

    script = Path(__file__).resolve()
    theorem = result_dir / "GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md"
    return {
        "schema": "gg-cycle-class-referee-composition-audit-v1",
        "status": "T_L_TIMES_CRITICAL_OLD_ANCHOR_PACKET_GATE_OPEN",
        "node_count": len(NODES),
        "edge_count": len(EDGES),
        "reachable_nodes": sorted(reached),
        "terminal_nodes": terminal_nodes,
        "smallest_named_terminal": "generic rank-completing paid-response splice outside the enlarged-root contract",
        "historical_global_typed_terminal": "T^dagger = T_0^* dot-union T_L^*",
        "global_typed_terminal": "T^dagger = T_0^* dot-union T_L^*",
        "pre_ledger_terminal": "T_0^*",
        "post_ledger_terminal": "T_L^*",
        "post_ledger_terminal_subtypes": ledger_resolution[
            "post_ledger_terminal_subtypes"
        ],
        "post_ledger_terminal_requirements": ledger_resolution[
            "surviving_terminal_requirements"
        ],
        "closed_post_ledger_subtypes": ledger_resolution[
            "closed_post_ledger_subtypes"
        ],
        "collision_T_L_times_closed": False,
        "collision_T_L_times_conditional_scalar_contradiction": True,
        "collision_T_L_times_root_packet_localized_to_critical_old_anchor": True,
        "stated_four_old_core_normal_form_vacuous": True,
        "core_rotation_outcome_counts": rotation["outcome_counts"],
        "frozen_witnesses_escape_by_efx_rotation": True,
        "residual_essential_separator": mixed["surviving_separator"],
        "endpoint_exchange_separator": exchange["smallest_remaining_operation"],
        "well_founded_order_status": "REFUTED_FOR_CURRENT_COORDINATES",
        "local_recurrence_response_rank": 1,
        "residual_partition_family_size": 4096,
        "efx_floor_feasible_residual_partitions": 0,
        "uncovered_premise_count": 3,
        "open_obligations": [
            "close the generic empty-ledger T_0^* recurrence",
            "project, activate, or otherwise close collision-free parked support T_{L,perp}^*",
            "pay or anchor-exchange a critical old-anchor atom in root-held T_{L,times}^*",
        ],
        "dependencies": records,
        "claim_boundary": (
            "critical-old-anchor collision localization inside the branch-complete "
            "GG reduction, not a GG closure theorem, collision theorem, or "
            "four-agent/general EFX proof"
        ),
        "provenance": {
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
    print(json.dumps({
        "status": result["status"],
        "smallest_named_terminal": result["smallest_named_terminal"],
        "uncovered_premise_count": result["uncovered_premise_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
