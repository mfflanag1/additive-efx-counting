"""Regression for the frozen strict-separated dual-anchor profile."""

import json
from pathlib import Path

from .audit_dual_anchor_strict_separated_profile import run


ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "results/three_nonsingleton_flower_full_capture_no_hub_no_safe_gate.json"


def test_strict_separated_profile_replays():
    expected = json.loads(
        (ROOT / "results/dual_anchor_strict_separated_profile_audit.json").read_text()
    )
    assert run(ROOT, PROFILE) == expected
    assert expected["strict_separated_q_order"]
    assert expected["root_payable"]
    assert expected["status"] == "PI_RESPONSE_MATCHING"


def test_matching_has_exact_release_support():
    expected = json.loads(
        (ROOT / "results/dual_anchor_strict_separated_profile_audit.json").read_text()
    )
    assert expected["incoming_disjoint"]
    assert expected["all_incoming_supplied"]
    assert expected["all_intended_owners_strictly_improve"]
