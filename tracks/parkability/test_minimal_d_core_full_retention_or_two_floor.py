#!/usr/bin/env python3
"""Regression check for the minimal-d-core terminal polarity."""

from .audit_minimal_d_core_full_retention_or_two_floor import audit


def test_minimal_d_core_full_retention_or_two_floor():
    result = audit()
    assert result["status"] == "FULL_RETENTION_AND_TWO_FLOOR_POLARITY_VERIFIED"
    assert "active theorem remain open" in result["claim_boundary"]
