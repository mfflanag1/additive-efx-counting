#!/usr/bin/env python3
"""Regression check for backward hole pushing."""

from .audit_backward_hole_pushing_d_capture import audit


def test_backward_hole_pushing_d_capture():
    result = audit()
    assert result["status"] == "PATH_TERMINATION_AND_D_CAPTURE_VERIFIED"
    assert result["matching_records"] == 96
    assert result["path_edge_length_counts"] == {
        "0": 24, "1": 24, "2": 24, "3": 24,
    }
    assert "remain open" in result["claim_boundary"]
