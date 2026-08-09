#!/usr/bin/env python3
"""Regression tests for the alternating dual-reservoir trichotomy."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

try:
    from .audit_alternating_dual_reservoir_trichotomy import (
        audit_profile,
        load_profiles,
    )
except ImportError:
    from audit_alternating_dual_reservoir_trichotomy import (
        audit_profile,
        load_profiles,
    )


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"


def test_frozen_profiles() -> None:
    profile_paths = [
        RESULTS / "alternating_bottom_partition_dichotomy_2222_audit.json",
        RESULTS / "alternating_any_root_subset_dichotomy_2222_audit.json",
        RESULTS / "alternating_any_cross_subset_dichotomy_2222_audit.json",
        RESULTS / "alternating_base_q_remainder_gate_2222.json",
        RESULTS / "alternating_base_q_remainder_recipient_relaxed_gate_2222.json",
        RESULTS / "alternating_base_q_remainder_exact_efx_gate_2222.json",
    ]
    profiles = load_profiles(
        RESULTS / "alternating_singleton_return_0213_session1.json",
        profile_paths,
    )
    records = [
        audit_profile(values, label, (2, 2, 2, 2))
        for label, values in profiles
    ]
    assert len(records) == 18
    assert Counter(record["branch"] for record in records) == {
        "same_offer_extension": 16,
        "unsafe_threshold_reversal": 2,
    }
    assert Counter(record["mode"] for record in records) == {
        "same_offer_promotion": 16,
        "anchored_q_handoff": 1,
        "opposite_reservoir_promotion": 1,
    }
    assert min(record["r_slack"] for record in records) >= 0
    assert all(record["same_offer_pair"] is not None for record in records)


def test_cross_source_strict_probe() -> None:
    import json

    payload = json.loads(
        (RESULTS / "alternating_cross_source_no_same_offer_pair_2222.json").read_text()
    )
    values = tuple(tuple(row) for row in payload["values"])
    record = audit_profile(values, "cross_source_strict_probe", (2, 2, 2, 2))
    assert record["mode"] == "opposite_reservoir_promotion"
    assert record["source"] == "p"
    assert record["same_offer_pair"] is None


if __name__ == "__main__":
    test_frozen_profiles()
    test_cross_source_strict_probe()
    print("alternating dual-reservoir trichotomy tests passed")
