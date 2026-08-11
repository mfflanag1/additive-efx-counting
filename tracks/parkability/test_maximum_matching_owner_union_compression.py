#!/usr/bin/env python3
"""Focused regression tests for maximum-matching response compression."""

import json
from pathlib import Path

try:
    from .audit_maximum_matching_owner_union_compression import run as run_audit
except ImportError:
    from audit_maximum_matching_owner_union_compression import run as run_audit


ROOT = Path(__file__).resolve().parents[2]


def test_maximum_matching_combinatorics_replay():
    expected = json.loads(
        (
            ROOT
            / "results/maximum_matching_owner_union_compression_audit.json"
        ).read_text()
    )
    assert run_audit() == expected
    assert expected["status"] == "ALL_FORCED"
    assert expected["owner_union_identity_failures"] == 0


def test_both_hardened_censuses_close():
    for filename, boundary_count in (
        ("two_external_weighted_hall_owner_union_compression_census.json", 243),
        ("two_external_weighted_hall_radius2_owner_union_compression_census.json", 81),
    ):
        payload = json.loads((ROOT / "results" / filename).read_text())
        assert payload["status"] == "ALL_CLOSED"
        assert payload["counts"]["BOUNDARIES"] == boundary_count
        assert payload["counts"].get("NO_COMPRESSION_CLOSURE", 0) == 0


def test_corrected_claim_boundary_is_explicit():
    theorem = (
        ROOT
        / "results/MAXIMUM_MATCHING_OWNER_UNION_COMPRESSION_LEMMA_20260811.md"
    ).read_text()
    assert "maximum matching `mu` of the full target--source relation" in theorem
    assert "flower-specific reverse" in theorem
