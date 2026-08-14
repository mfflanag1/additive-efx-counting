#!/usr/bin/env python3

from pathlib import Path

from .audit_shared_target_double_response_overlap import run


def test_shared_target_dichotomy():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "DISJOINT_OR_FULL_MARGIN_CAPTURE"
    assert result["checks"]["weak_capture_implication"] == "unsat"
    assert result["checks"]["strict_capture_when_outside_strictly_below_floor"] == "unsat"
    assert result["checks"]["packet_partition"]["partition_exact"]
