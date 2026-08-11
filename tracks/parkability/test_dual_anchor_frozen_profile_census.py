"""Regression for the frozen dual-anchor profile census."""

import json
from pathlib import Path

from .audit_dual_anchor_frozen_profile_census import run


ROOT = Path(__file__).resolve().parents[2]


def test_frozen_dual_anchor_census_replays():
    expected = json.loads(
        (ROOT / "results/dual_anchor_frozen_profile_census.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["profile_count"] == 10
    assert expected["strict_separated_count"] == 5
    assert expected["status"] == "ALL_PI_RESPONSE_MATCHING"


def test_every_profile_has_supported_matching():
    expected = json.loads(
        (ROOT / "results/dual_anchor_frozen_profile_census.json").read_text()
    )
    assert all(record["root_payable"] for record in expected["records"])
    assert all(record["internal_matching_count"] > 0 for record in expected["records"])
    assert all(record["incoming_disjoint"] for record in expected["records"])
    assert all(record["all_incoming_supplied"] for record in expected["records"])
