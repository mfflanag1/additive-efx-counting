"""Regression tests for nonroot singleton safe-envelope descent."""

import json
from pathlib import Path

from .audit_nonroot_singleton_hit_safe_envelope_descent import run


ROOT = Path(__file__).resolve().parents[2]


def test_nonroot_singleton_descent_replays():
    expected = json.loads(
        (ROOT / "results/nonroot_singleton_hit_safe_envelope_descent_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_nonroot_singleton_descent_boundary():
    result = run(ROOT)
    assert result["status"] == "NONROOT_SINGLETON_HIT_DESCENT_PROVED"
    assert result["root_reselection_preserves_strict_base"]
    assert result["nonroot_source_strictly_improves"]
    assert not result["root_holder_supplier_star_imported"]
    assert "remain open" in result["claim_boundary"]
