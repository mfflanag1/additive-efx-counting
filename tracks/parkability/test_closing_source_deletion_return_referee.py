"""Regression tests for the independent deletion-return referee audit."""

import json
from pathlib import Path

from .audit_closing_source_deletion_return_referee import run


ROOT = Path(__file__).resolve().parents[2]


def test_referee_audit_replays():
    expected = json.loads(
        (ROOT / "results/closing_source_deletion_return_referee_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_scalar_parts_hold_but_termination_fails():
    result = run(ROOT)
    assert result["status"] == "TERMINATION_GAP_FOUND"
    assert all(result["scalar_checks"].values())
    witness = result["rational_local_countermodel"]
    assert witness["response_source_rank"] == 1
    assert witness["failed_efx"]["observer_utility"] == "3"
    assert witness["failed_efx"]["target_threshold"] == "4"


def test_report_does_not_claim_full_gg_counterexample():
    report = (ROOT / "results/CLOSING_SOURCE_DELETION_RETURN_REFEREE_REPORT_20260812.md").read_text()
    assert "not a full GG counterexample" in report
    assert "rank-completing paid-response splice" in report
