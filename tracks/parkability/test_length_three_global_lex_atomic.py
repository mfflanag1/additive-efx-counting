#!/usr/bin/env python3
"""Regression test for the length-three atomic motif sweep."""

from pathlib import Path

try:
    from .audit_length_three_global_lex_atomic_sweep import audit
except ImportError:
    from audit_length_three_global_lex_atomic_sweep import audit


ROOT = Path(__file__).resolve().parents[2]


def test_atomic_sweep() -> None:
    result = audit(ROOT / "results" / "length_three_global_lex_atomic_sweep.json")
    assert result["status"] == "ALL_72_ATOMIC_SOURCE_ORDER_CORES_UNSAT"
    assert result["total_cell_count"] == 72
    assert result["maximum_core_size"] == 3


def test_selected_residual_sweep() -> None:
    result = audit(
        ROOT / "results" / "length_three_selected_residual_atomic_cores.json"
    )
    assert result["status"] == "ALL_9_ATOMIC_SOURCE_ORDER_CORES_UNSAT"
    assert result["structural_mode"] == "selected"
    assert result["total_cell_count"] == 9
    assert result["maximum_core_size"] == 6


if __name__ == "__main__":
    test_atomic_sweep()
    test_selected_residual_sweep()
    print("length-three global-lex atomic sweep test passed")
