#!/usr/bin/env python3
"""Regression test for the alternating global-lex atomic cores."""

from __future__ import annotations

try:
    from .audit_alternating_global_lex_atomic_core import audit
except ImportError:
    from audit_alternating_global_lex_atomic_core import audit


def test_audit() -> None:
    result = audit()
    assert result["status"] == "ALL_24_PRIORITY_ORDERS_UNSAT"
    assert result["priority_order_count"] == 24
    assert result["single_rival_order_count"] == 16
    assert result["maximum_core_size"] == 5


if __name__ == "__main__":
    test_audit()
    print("alternating global-lex atomic core test passed")
