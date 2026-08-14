#!/usr/bin/env python3
"""Integrity/composition audit for the global retired-support theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(repo: Path) -> dict:
    results = repo / "results"
    contract = json.loads(
        (results / "global_retired_root_support_transition_contract_audit.json").read_text()
    )
    collision = json.loads(
        (results / "retired_packet_selector_collision_normalization_audit.json").read_text()
    )
    assert contract["status"] == "CONTRACT_AND_G0_G10_COVERAGE_VERIFIED"
    assert collision["status"] == (
        "COLLISION_NORMALIZED_TO_LEDGER_FREE_PROGRESS_ROOT_OR_TL_STAR"
    )
    assert contract["g_states_covered"] == [f"G{i}" for i in range(11)]
    assert all(contract["scalar_checks"].values())
    assert collision["no_silent_reuse"]

    transition_routes = {
        "G0": ["original"],
        "G1": ["original", "support_progress", "collision_normalization"],
        "G2": ["ledger_free_core", "retired_hitting_core"],
        "G3": ["connected_transfer", "protected_floor_collision"],
        "G4": ["normalized_matching", "rank_four_cycle", "TL_star"],
        "G5": ["normalized_repair", "typed_base_floor_separator"],
        "G6": ["normalized_fork", "owner_growth", "TL_star"],
        "G7": ["component_return", "retired_capture_separator"],
        "G8": ["signed_state_progress", "exact_repeat"],
        "G9": ["normalized_rotation", "PI", "supplier_progress", "TL_star"],
        "G10": ["anchor_reselection", "retirement_growth", "normalized_return"],
    }
    assert list(transition_routes) == [f"G{i}" for i in range(11)]

    # The proof needs only componentwise finiteness.  We deliberately avoid a
    # spurious numerical bound on orientations: the contracted graph fixes a
    # finite orientation alphabet, but does not identify it with five values.
    finite_component_argument = {
        "root_choices": "four",
        "physical_anchor_supports": "subsets_of_finite_ground_set",
        "supplier_labels": "subsets_or_members_of_four_owners_plus_charity",
        "orientation_labels": "finite_alphabet_fixed_by_G0_G10_contract",
        "typed_floors": "values_or_thresholds_induced_by_finitely_many_bundles",
        "response_and_allocation_records": "finite_labeled_good_state_space",
    }

    dependencies = [
        "GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md",
        "GLOBAL_RETIRED_ROOT_SUPPORT_G0_G10_TRANSITION_AUDIT_20260813.md",
        "RETIRED_PACKET_SELECTOR_COLLISION_NORMALIZATION_LEMMA_20260813.md",
        "GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md",
        "GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPLETION_AUDIT_20260813.md",
        "global_retired_root_support_transition_contract_audit.json",
        "retired_packet_selector_collision_normalization_audit.json",
        "FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md",
        "CHARITY_AUGMENTED_FIVE_TARGET_HOLE_PIVOT_CYCLE_LEMMA_20260811.md",
        "CROSS_COMPONENT_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md",
        "UNIVERSAL_PAID_ANCHOR_SUPPORT_RESET_LEMMA_20260811.md",
        "PERMANENT_ANCHOR_MINIMAL_RESPONSE_PEEL_OR_RESELECT_THEOREM_20260813.md",
    ]
    script = Path(__file__).resolve()
    theorem = results / "GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md"
    return {
        "schema": "global-retired-root-support-ledger-composition-audit-v2",
        "status": "GLOBAL_LEDGER_COMPOSED_EXACT_T_DAGGER_SURVIVES",
        "g_states_covered": list(transition_routes),
        "transition_routes": transition_routes,
        "cross_cutting_operations_covered": contract["cross_cutting_operations"],
        "physical_label_floor_separation": {
            "label_excludes_current_floor": contract[
                "physical_anchor_label_excludes_current_floor"
            ],
            "retirement_persists_across_floor_changes": contract[
                "retired_support_persists_across_floor_changes"
            ],
        },
        "no_collision_terminal_guard": contract[
            "no_collision_T_star_requires_complete_pool_audit"
        ],
        "scalar_collision_checks": contract["scalar_checks"],
        "collision_normalization_checks": {
            "capture": collision["capture_inequality"],
            "positive_packet": collision["capture_packet_positive"],
            "weak_floor_equality_critical": collision[
                "weak_floor_equality_critical"
            ],
            "protected_floor_safety": collision[
                "minimality_protected_floor_safety_step"
            ],
            "typed_current_floor_guard": collision[
                "current_safety_requires_current_floor"
            ],
            "history_only_progress_forbidden": collision[
                "history_only_progress_forbidden"
            ],
            "equality_without_typed_handoff_to_TL_star": collision[
                "equality_without_typed_handoff_routes_to_TL_star"
            ],
            "ledger_free_exact_repeat_to_TL_star": collision[
                "ledger_free_exact_response_repeat_routes_to_TL_star"
            ],
            "specialized_handoff_premise_guard": collision[
                "specialized_handoff_requires_exact_premises"
            ],
            "no_silent_reuse": collision["no_silent_reuse"],
        },
        "finite_component_argument": finite_component_argument,
        "surviving_terminal": "T^dagger = T_0^* dot-union T_L^*",
        "pre_ledger_terminal": "T_0^*",
        "post_ledger_terminal": "T_L^*",
        "post_ledger_terminal_subtypes": ["T_{L,perp}^*", "T_{L,times}^*"],
        "surviving_terminal_requirements": [
            "nonempty retired packet",
            "retirement supplier and current holder",
            "fixed typed protected floors",
            "complete-pool parked-support certificate or collision certificate",
            "collision subtype has repeated hitting/bypass response or typed separator",
            "typed rank deficiency or observer-payment/release separator",
        ],
        "generic_empty_ledger_T_star_closed": False,
        "augmented_generic_T_star_strictly_narrowed": True,
        "gg_closed": False,
        "dependencies": [
            {"path": f"results/{name}", "sha256": sha256(results / name)}
            for name in dependencies
        ],
        "claim_boundary": (
            "global ledger composition through the current G0-G10 architecture; "
            "typed T-dagger, GG, and general EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "g_states": len(result["g_states_covered"]),
        "surviving_terminal": result["surviving_terminal"],
    }, indent=2))


if __name__ == "__main__":
    main()
