#!/usr/bin/env python3
"""Regression checks for the exact fixed-U radius-three exchange no-go."""

import json
from pathlib import Path

from .audit_fixed_u_radius_three_exchange_no_go import audit


ROOT = Path(__file__).resolve().parents[2]


def test_exact_radius_three_no_go():
    result = audit(ROOT / "results/fixed_u_full_packet_batch_cegar.json", 10)
    assert result["all_premises_hold"]
    assert result["efx_lex_escapes_by_exact_radius"] == {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 52,
    }
    assert result["recorded_menu_matches_exact_radius_four_set"]
    assert result["radius_three_no_go_verified"]
    assert "does not encode response saturation" in result["claim_boundary"]


def test_exact_audit_replays():
    expected = json.loads(
        (ROOT / "results/fixed_u_radius_three_exchange_no_go_audit.json").read_text()
    )
    assert audit(ROOT / "results/fixed_u_full_packet_batch_cegar.json", 10) == expected


if __name__ == "__main__":
    test_exact_radius_three_no_go()
    print("fixed-U radius-three exchange no-go tests passed")
