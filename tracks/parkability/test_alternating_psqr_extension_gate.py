#!/usr/bin/env python3
"""Focused tests for the psqr extension-or-handoff checkpoint."""

try:
    from .audit_alternating_psqr_unrestricted_refutation import (
        audit as audit_refutation,
    )
    from .decide_alternating_psqr_threshold_matching_gate import decide
    from .extract_alternating_psqr_atomic_walls import extract
except ImportError:
    from audit_alternating_psqr_unrestricted_refutation import audit as audit_refutation
    from decide_alternating_psqr_threshold_matching_gate import decide
    from extract_alternating_psqr_atomic_walls import extract


def test_atomic_failure_walls_are_jointly_unsat():
    result = extract()
    assert result["status"] == "ALL_PSQR_ATOMIC_BLOCKER_SELECTIONS_UNSAT"
    assert result["blocker_selection_count"] == 6


def test_atomic_extension_or_suffix_handoff_gate_is_unsat():
    result = decide((1, 1, 1, 1), 30)
    assert result["status"] == "UNSAT_EXTENSION_OR_HANDOFF_GATE"


def test_unrestricted_dichotomy_is_refuted_in_both_half_turns():
    result = audit_refutation()
    assert (
        result["status"]
        == "UNRESTRICTED_EXTENSION_OR_HANDOFF_REFUTED_BOTH_HALF_TURNS"
    )
    for profile in result["profiles"]:
        assert profile["target_qf_lia_status"] == "unsat"
        assert profile["exhaustive"]["anchored_lex_improving_efx_count"] == 0
        assert profile["exhaustive"]["desired_promoted_efx_count"] == 0
        assert profile["exhaustive"]["unrestricted_lex_improving_efx_count"] > 0


if __name__ == "__main__":
    test_atomic_failure_walls_are_jointly_unsat()
    test_atomic_extension_or_suffix_handoff_gate_is_unsat()
    test_unrestricted_dichotomy_is_refuted_in_both_half_turns()
