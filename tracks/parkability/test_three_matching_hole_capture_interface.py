#!/usr/bin/env python3
"""Regression checks for the three-matching hole-capture interface."""

from .audit_three_matching_hole_capture_interface import audit


def test_three_matching_hole_capture_interface():
    result = audit()
    assert result["status"] == "ALL_NEAR_PERFECT_MATCHINGS_VERIFIED"
    assert result["matching_records"] == 96
    assert result["maximum_support_edges"] == 4
    assert "Simultaneous capture reversal" in result["claim_boundary"]
