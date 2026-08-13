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
    assert backward["status"] == "BACKWARD_RESPONSE_REDUCED_TO_MIXED_CYCLE_PAYMENT"
    anchor_target = json.loads(
        (result_dir / "anchor_target_nonoverlap_growth_or_nested_edge_audit.json").read_text()
    )
    assert anchor_target["status"] == "ANCHOR_TARGET_INEQUALITY_ELIMINATED_TO_NESTED_EDGE"
    resolution = json.loads(
        (result_dir / "selected_pool_signed_surplus_recruitment_resolution_audit.json").read_text()
    )
    assert resolution["status"] == "SELECTED_POOL_RECRUITMENT_GOAL_RESOLVED"

    script = Path(__file__).resolve()
    theorem = result_dir / "GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md"
    return {
        "schema": "gg-cycle-class-referee-composition-audit-v1",
        "status": "SELECTED_POOL_RECRUITMENT_RESOLVED",
        "node_count": len(NODES),
        "edge_count": len(EDGES),
        "reachable_nodes": sorted(reached),
        "terminal_nodes": terminal_nodes,
        "smallest_named_terminal": "post-recruitment mixed-cycle/root-source payment",
        "stated_four_old_core_normal_form_vacuous": True,
        "core_rotation_outcome_counts": rotation["outcome_counts"],
        "frozen_witnesses_escape_by_efx_rotation": True,
        "residual_essential_separator": mixed["surviving_separator"],
        "endpoint_exchange_separator": exchange["smallest_remaining_operation"],
        "well_founded_order_status": "REFUTED_FOR_CURRENT_COORDINATES",
        "local_recurrence_response_rank": 1,
        "residual_partition_family_size": 4096,
        "efx_floor_feasible_residual_partitions": 0,
        "uncovered_premise_count": 7,
        "dependencies": records,
        "claim_boundary": (
            "branch-complete reduction of the current GG architecture, not a GG "
            "closure theorem or four-agent/general EFX proof"
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
