"""Regression for captured-q anchored residual rotation."""

import json
from pathlib import Path

from .audit_captured_q_margin_anchored_residual_rotation import run


ROOT = Path(__file__).resolve().parents[2]


def test_captured_q_rotation_replays():
    expected = json.loads(
        (ROOT / "results/captured_q_margin_anchored_residual_rotation_audit.json").read_text()
    )
    assert run(ROOT) == expected
    assert expected["status"] == "ALL_FORCED"


def test_claim_boundary_keeps_response_termination_open():
    theorem = (
        ROOT / "results/CAPTURED_Q_MARGIN_ANCHORED_RESIDUAL_ROTATION_LEMMA_20260811.md"
    ).read_text()
    assert "never resets the global" in theorem.replace("\n", " ")
    assert "does not eliminate" in theorem.replace("\n", " ")
