#!/usr/bin/env python3
"""Regression check for paid-hole trimming/double capture."""

from .audit_paid_hole_core_trimming_or_double_capture import audit


def test_paid_hole_core_trimming_or_double_capture():
    result = audit()
    assert result["status"] == "MINIMAL_REPAIR_AND_DOUBLE_CAPTURE_VERIFIED"
    assert result["finite_minimal_repair_records"] == 9205
    assert "active theorem remain open" in result["claim_boundary"]
