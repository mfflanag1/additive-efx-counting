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
        ROOT / "results/nonroot_safe_whole_hit_envelope_descent_audit.json",
        ROOT / "results/root_safe_whole_hit_complete_pool_reduction_audit.json",
        ROOT / "results/retirement_supplier_root_packet_release_or_underpayment_audit.json",
        ROOT / "results/retirement_supplier_subpacket_release_or_atomwise_pool_dominance_audit.json",
        ROOT / "results/root_equality_base_restoration_packet_spread_admission_audit.json",
        ROOT / "results/signed_missing_base_packet_charge_or_base_containment_audit.json",
        ROOT / "results/base_contained_global_exterior_sacrifice_admission_audit.json",
        ROOT / "results/exterior_dominance_three_agent_source_reduction_audit.json",
        ROOT / "results/base_contained_signed_reset_one_good_root_normal_form_audit.json",
        Path(__file__).resolve(),
    ]
    checkpoint = files[0].read_text()
    for phrase in (
        "theorem not yet proved or refuted",
        "Nonroot branch: closed",
        "strict clean subpacket release",
        "strict atomwise exterior-pool dominance terminal",
        "Signed base-support fork",
        "complete exterior dominance",
        "three named source topologies",
        "one-good form",
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
            "STRICT_GLOBAL_EXTERIOR_SACRIFICE_ADMITTED_DOMINANCE_REMAINS",
        "exterior_dominance_three_agent_source_reduction_audit.json":
            "EXTERIOR_DOMINANCE_REDUCED_TO_AT_MOST_TWO_SOURCES",
        "base_contained_signed_reset_one_good_root_normal_form_audit.json":
            "BASE_CONTAINED_PACKET_NORMALIZED_TO_ONE_GOOD_ON_OFF_RESPONSE",
    }
    statuses = {}
    for name, status in expected.items():
        data = json.loads((ROOT / "results" / name).read_text())
        assert data["status"] == status
        assert not data["full_T_L_times_theorem_closed"]
        statuses[name] = status

    return {
        "schema": "retired-packet-charge-anchor-second-checkpoint-20260814-audit-v1",
        "status": "ROOT_REDUCED_TO_ONE_GOOD_ON_OFF_SOURCE_DEBT_OR_CHARGE",
        "dependency_statuses": statuses,
        "nonroot_safe_whole_hit_closed": True,
        "proper_donor_free_equality_closed": False,
        "root_packet_price_equality_closed": True,
        "historical_supplier_return_admitted": False,
        "strict_clean_subpacket_release_admitted": True,
        "strict_atomwise_pool_dominance_unconditional": True,
        "signed_missing_base_support_fork_proved": True,
        "base_contained_exterior_sacrifice_admitted": True,
        "exterior_dominance_source_topology_reduced": True,
        "one_good_root_normal_form_proved": True,
        "remaining_separator": "one_good_on_off_response_source_debt_or_multilabel_charge_recurrence",
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
