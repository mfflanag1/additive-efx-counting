#!/usr/bin/env python3
"""Regression tests for the strict extension-or-handoff reduction artifacts."""

from __future__ import annotations

from pathlib import Path

try:
    from .audit_alternating_boosted_handoff_profiles import audit
    from .audit_alternating_no_same_offer_promotion import audit as audit_no_promotion
    from .audit_alternating_variable_extension_counterexample import (
        audit as audit_variable_extension,
    )
except ImportError:
    from audit_alternating_boosted_handoff_profiles import audit
    from audit_alternating_no_same_offer_promotion import audit as audit_no_promotion
    from audit_alternating_variable_extension_counterexample import (
        audit as audit_variable_extension,
    )


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
PROFILE_PATHS = [
    RESULTS / "alternating_bottom_partition_dichotomy_2222_audit.json",
    RESULTS / "alternating_any_root_subset_dichotomy_2222_audit.json",
    RESULTS / "alternating_any_cross_subset_dichotomy_2222_audit.json",
    RESULTS / "alternating_base_q_remainder_gate_2222.json",
    RESULTS / "alternating_base_q_remainder_recipient_relaxed_gate_2222.json",
    RESULTS / "alternating_base_q_remainder_exact_efx_gate_2222.json",
    RESULTS / "alternating_three_pair_residual_gate_2222.json",
    RESULTS / "alternating_cross_source_no_same_offer_pair_2222.json",
    RESULTS / "alternating_no_same_offer_promotion_dominance_2222.json",
]


def test_boosted_handoff_profiles() -> None:
    result = audit(
        RESULTS / "alternating_singleton_return_0213_session1.json",
        PROFILE_PATHS,
        (2, 2, 2, 2),
    )
    assert result["status"] == "ALL_PROFILES_HAVE_BOOSTED_HANDOFF"
    assert result["profile_count"] == 21


def test_no_promotion_boundary() -> None:
    result = audit_no_promotion(
        RESULTS / "alternating_no_same_offer_promotion_dominance_2222.json"
    )
    assert result["promotion_search_status"] == "unsat"
    assert result["anchor_search_status"] == "sat"


def test_variable_extension_refutation() -> None:
    import json

    payload = json.loads(
        (RESULTS / "alternating_variable_extension_1121_refutation.json").read_text()
    )
    result = audit_variable_extension(payload)
    assert result["status"] == "EXACT_STRICT_BRIDGE_COUNTEREXAMPLE"
    assert result["allocations_exhausted"] == 390625
    assert result["allocation_counts"]["anchored"] == 0
    assert result["allocation_counts"]["promoted_original_offer"] == 0
    assert result["allocation_counts"]["outside"] == 162
    assert result["smallest_missing_operation"]["changed_good_count"] == 4


if __name__ == "__main__":
    test_boosted_handoff_profiles()
    test_no_promotion_boundary()
    test_variable_extension_refutation()
    print("alternating extension-or-handoff tests passed")
