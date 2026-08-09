#!/usr/bin/env python3
"""Regression test for the alternating reservoir-exchange construction."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

try:
    from .audit_alternating_reservoir_exchange import audit_profile, load_profiles
except ImportError:
    from audit_alternating_reservoir_exchange import audit_profile, load_profiles


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
        "low_reservoir": 1,
        "threshold_minimal_safe": 13,
        "unsafe_threshold_subset_reversal": 4,
    }
    assert {record["source"] for record in records} <= {"r", "s"}
    assert min(record["q_slack"] for record in records) >= 0


def test_adaptive_root_countermodel() -> None:
    payload = json.loads(
        (RESULTS / "alternating_adaptive_root_or_two_good_bridge.json").read_text()
    )
    values = tuple(tuple(row) for row in payload["values"])
    record = audit_profile(values, "adaptive_root_countermodel", (1, 1, 1, 1))
    assert record["branch"] == "threshold_minimal_safe"
    assert record["source"] == "s"
    assert record["active_bundle"] == ["tq", "f"]
    assert record["payment_bundle"] == ["br", "bq"]
    assert record["q_slack"] == 2


if __name__ == "__main__":
    test_frozen_profiles()
    test_adaptive_root_countermodel()
    print("alternating reservoir-exchange tests passed")
