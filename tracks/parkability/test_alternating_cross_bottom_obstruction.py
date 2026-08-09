#!/usr/bin/env python3
"""Regression test for the alternating cross-bottom obstruction."""

from __future__ import annotations

try:
    from .audit_alternating_cross_bottom_obstruction import audit
except ImportError:
    from audit_alternating_cross_bottom_obstruction import audit


def test_audit() -> None:
    result = audit()
    assert result["status"] == "PASSED"
    assert result["exhaustive_census"]["efx_assignment_count"] == 2263
    assert result["exhaustive_census"]["pareto_dominating_efx_count"] == 0
    assert set(result["exhaustive_census"]["first_priority_escapes"]) == {
        "p",
        "r",
        "s",
        "q",
    }


if __name__ == "__main__":
    test_audit()
    print("alternating cross-bottom obstruction test passed")
