#!/usr/bin/env python3
"""Regression tests for the alternating root-flip proof-mining artifacts."""

from __future__ import annotations

from pathlib import Path

try:
    from .audit_alternating_anchored_or_promoted_atom import audit as audit_atom
    from .audit_alternating_anchored_or_promoted_refutation import (
        audit as audit_refutation,
    )
    from .audit_alternating_root_flip_split_core import audit as audit_root_flip
except ImportError:
    from audit_alternating_anchored_or_promoted_atom import audit as audit_atom
    from audit_alternating_anchored_or_promoted_refutation import (
        audit as audit_refutation,
    )
    from audit_alternating_root_flip_split_core import audit as audit_root_flip


ROOT = Path(__file__).resolve().parents[2]


def test_audits() -> None:
    atom = audit_atom()
    assert atom["status"] == "ATOMIC_ANCHORED_OR_PROMOTED_DICHOTOMY_UNSAT"
    assert len(atom["dichotomy_orders"]) == 8
    assert len(atom["anchored_countermodels"]) == 6

    root_flip = audit_root_flip()
    assert root_flip["status"] == "TWO_RIVAL_ROOT_FLIP_CORE_UNSAT"
    assert root_flip["core_size"] == 2
    assert root_flip["single_deletion_statuses"] == ["sat", "sat"]

    refutation = audit_refutation(
        ROOT / "results/alternating_anchored_or_promoted_0321_nondegenerate_refutation.json"
    )
    assert refutation["status"] == "NONDEGENERATE_CANONICAL_TWO_BRANCH_TARGET_REFUTED"
    assert refutation["subset_nondegenerate_by_agent"] == [True] * 4
    assert refutation["root_bundle_is_alternate_desired_set"] is True


if __name__ == "__main__":
    test_audits()
    print("alternating root-flip tests passed")
