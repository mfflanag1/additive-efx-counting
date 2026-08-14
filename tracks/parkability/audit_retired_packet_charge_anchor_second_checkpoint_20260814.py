#!/usr/bin/env python3
"""Integrity audit for the second Aug-14 charge/anchor checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    files = [
        ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_SECOND_CHECKPOINT_20260814.md",
        ROOT / "results/NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md",
        ROOT / "results/ROOT_SAFE_WHOLE_HIT_COMPLETE_POOL_REDUCTION_THEOREM_20260814.md",
        ROOT / "results/RETIREMENT_SUPPLIER_ROOT_PACKET_RELEASE_OR_UNDERPAYMENT_THEOREM_20260814.md",
        ROOT / "results/RETIREMENT_SUPPLIER_SUBPACKET_RELEASE_OR_ATOMWISE_POOL_DOMINANCE_THEOREM_20260814.md",
        ROOT / "results/RETIREMENT_SUPPLIER_RETURN_ADMISSIBILITY_CORRECTION_20260814.md",
        ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md",
        ROOT / "results/ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md",
        ROOT / "results/SIGNED_MISSING_BASE_PACKET_CHARGE_OR_BASE_CONTAINMENT_THEOREM_20260814.md",
        ROOT / "results/BASE_CONTAINED_GLOBAL_EXTERIOR_SACRIFICE_ADMISSION_THEOREM_20260814.md",
        ROOT / "results/EXTERIOR_DOMINANCE_THREE_AGENT_SOURCE_REDUCTION_THEOREM_20260814.md",
        ROOT / "results/BASE_CONTAINED_SIGNED_RESET_ONE_GOOD_ROOT_NORMAL_FORM_THEOREM_20260814.md",
        ROOT / "results/ROOT_GLOBAL_EXTERIOR_SUBPACKET_SACRIFICE_THEOREM_20260814.md",
        ROOT / "results/root_global_exterior_subpacket_sacrifice_independent_audit.json",
        ROOT / "results/GLOBAL_EXTERIOR_DOMINANCE_BASE_CONTAINMENT_AND_CHARITY_RESET_THEOREM_20260814.md",
        ROOT / "results/TWO_SOURCE_ROOT_THRESHOLD_DEBT_DERANGEMENT_THEOREM_20260814.md",
        ROOT / "results/TWO_SOURCE_SINGLETON_SOURCE_ELIMINATION_AND_GGS_SWITCH_THEOREM_20260814.md",
        ROOT / "results/FORCED_GGS_OFF_GOOD_RESPONSE_PI_REDUCTION_THEOREM_20260814.md",
        ROOT / "results/GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md",
        ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_RESOLUTION_20260814.md",
        ROOT / "results/gg_old_root_core_exterior_dominance_audit.json",
        ROOT / "results/gg_old_root_core_exterior_dominance_independent_audit.json",
        ROOT / "results/retired_packet_charge_anchor_resolution_20260814_audit.json",
        ROOT / "results/nonroot_safe_whole_hit_envelope_descent_audit.json",
        ROOT / "results/root_safe_whole_hit_complete_pool_reduction_audit.json",
        ROOT / "results/retirement_supplier_root_packet_release_or_underpayment_audit.json",
        ROOT / "results/retirement_supplier_subpacket_release_or_atomwise_pool_dominance_audit.json",
        ROOT / "results/root_equality_base_restoration_packet_spread_admission_audit.json",
        ROOT / "results/signed_missing_base_packet_charge_or_base_containment_audit.json",
        ROOT / "results/base_contained_global_exterior_sacrifice_admission_audit.json",
        ROOT / "results/exterior_dominance_three_agent_source_reduction_audit.json",
        ROOT / "results/base_contained_signed_reset_one_good_root_normal_form_audit.json",
        ROOT / "results/root_global_exterior_subpacket_sacrifice_audit.json",
        ROOT / "results/global_exterior_dominance_base_containment_charity_reset_audit.json",
        ROOT / "results/two_source_root_threshold_debt_derangement_audit.json",
        ROOT / "results/two_source_singleton_source_elimination_ggs_switch_audit.json",
        ROOT / "results/forced_ggs_off_good_response_pi_reduction_audit.json",
        Path(__file__).resolve(),
    ]
    checkpoint = files[0].read_text()
    for phrase in (
        "Audit correction",
        "theorem not yet proved or refuted",
        "Nonroot branch: closed",
        "strict clean subpacket release",
        "strict complete-current-exterior dominance terminal",
        "Base containment and supplier-free one-good reset",
        "no signed-return blocker",
        "single-edge two-source hard champion pattern",
        "charity one-good response",
        "debt map on three owners",
        "only source pair is `{c,q}`",
        "Three external-source off-good profiles",
        "does not prove or refute",
    ):
        assert phrase in checkpoint

    expected = {
        "nonroot_safe_whole_hit_envelope_descent_audit.json":
            "ALL_COMMON_SAFE_NONROOT_WHOLE_HITS_TERMINATE",
        "root_safe_whole_hit_complete_pool_reduction_audit.json":
            "ALL_TYPED_SAFE_WHOLE_HITS_REDUCED_TO_ROOT_POOL_UNDERPAYMENT_OR_EQUALITY",
        "retirement_supplier_root_packet_release_or_underpayment_audit.json":
            "STRICT_ROOT_PACKET_RELEASE_ADMITTED_EQUALITY_OPEN",
        "retirement_supplier_subpacket_release_or_atomwise_pool_dominance_audit.json":
            "STRICT_SUBPACKET_RELEASE_ADMITTED_WEAK_ATOMWISE_EQUALITY_OPEN",
        "root_equality_base_restoration_packet_spread_admission_audit.json":
            "ROOT_PACKET_PRICE_EQUALITY_ELIMINATED_STRICT_UNDERPAYMENT_REMAINS",
        "signed_missing_base_packet_charge_or_base_containment_audit.json":
            "ROOT_PACKET_BASE_CONTAINED_OR_SIGNED_RETURN_HAS_NAMED_BLOCKER",
        "base_contained_global_exterior_sacrifice_admission_audit.json":
            "STRICT_GLOBAL_EXTERIOR_SACRIFICE_FLOOR_ADMISSION_OPEN",
        "exterior_dominance_three_agent_source_reduction_audit.json":
            "EXTERIOR_DOMINANCE_REDUCED_TO_TWO_SOURCE_ROOT_THRESHOLD_DEBT",
        "base_contained_signed_reset_one_good_root_normal_form_audit.json":
            "BASE_CONTAINED_PACKET_NORMALIZED_TO_ONE_GOOD_ON_OFF_RESPONSE",
        "root_global_exterior_subpacket_sacrifice_audit.json":
            "CONDITIONAL_ROOT_EXTERIOR_DOMINANCE_FLOOR_ADMISSION_OPEN",
        "root_global_exterior_subpacket_sacrifice_independent_audit.json":
            "INDEPENDENT_INTEGER_REPLAY_CONFIRMS_GLOBAL_ROOT_CUT_AND_BASE_CONTAINMENT",
        "global_exterior_dominance_base_containment_charity_reset_audit.json":
            "ROOT_REDUCED_UNCONDITIONALLY_TO_CHARITY_ONE_GOOD_ON_OFF_RESPONSE",
        "two_source_root_threshold_debt_derangement_audit.json":
            "TWO_SOURCE_FACE_REDUCED_TO_SINGLE_EDGE_HARD_CHAMPIONS_CYCLIC_DEBT",
        "two_source_singleton_source_elimination_ggs_switch_audit.json":
            "SINGLETON_SOURCE_PAIR_CLOSED_SOLE_SURVIVOR_FORCES_NONROOT_GGS",
        "forced_ggs_off_good_response_pi_reduction_audit.json":
            "OFF_GOOD_Q_AND_Q_TO_S_SOURCE_PROFILES_PI_CLOSED",
    }
    statuses = {}
    for name, status in expected.items():
        data = json.loads((ROOT / "results" / name).read_text())
        assert data["status"] == status
        assert not data["full_T_L_times_theorem_closed"]
        statuses[name] = status

    return {
        "schema": "retired-packet-charge-anchor-second-checkpoint-20260814-audit-v1",
        "status": "CONDITIONAL_GGS_FRONTIER_ROOT_FLOOR_ADMISSION_OPEN",
        "dependency_statuses": statuses,
        "nonroot_safe_whole_hit_closed": True,
        "proper_donor_free_equality_closed": False,
        "root_packet_price_equality_closed": True,
        "historical_supplier_return_admitted": False,
        "strict_clean_subpacket_release_admitted": True,
        "strict_atomwise_pool_dominance_unconditional": True,
        "signed_missing_base_support_fork_proved": True,
        "base_contained_exterior_sacrifice_admitted": False,
        "base_contained_exterior_sacrifice_scalar_cut_conditional": True,
        "exterior_dominance_source_topology_reduced": True,
        "one_good_root_normal_form_proved": True,
        "global_exterior_supplier_star_admitted": False,
        "global_exterior_supplier_star_scalar_cut_conditional": True,
        "global_exterior_independent_integer_replay_passed": True,
        "base_containment_unconditional": True,
        "signed_missing_base_return_required": False,
        "multilabel_charge_branch_required": False,
        "unique_source_face_closed": True,
        "double_edge_two_source_face_closed": True,
        "cyclic_cross_completion_debt_proved": True,
        "debt_cycle_release_compatible_pi_proved": False,
        "singleton_source_pair_closed": True,
        "forced_nonroot_GGS_cycle_proved": True,
        "off_good_profiles_remaining": 3,
        "on_good_profiles_closed": False,
        "remaining_separator": "controlled_floor_reset_or_floor_paying_supplier_star",
        "old_root_core_exterior_contradiction_conditional": True,
        "full_T_L_times_theorem_closed": False,
        "full_T_L_times_theorem_refuted": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path) for path in files
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
