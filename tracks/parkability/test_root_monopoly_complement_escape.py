"""Focused regression for the root-monopoly complement escape."""

import json
from pathlib import Path

try:
    from .audit_root_monopoly_complement_escape import run
except ImportError:
    from audit_root_monopoly_complement_escape import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_monopoly_complement_escape_replays():
    expected = json.loads(
        (ROOT / "results/root_monopoly_complement_escape_audit.json").read_text()
    )
    replay = run(ROOT)
    for field in (
        "status",
        "scalar_records",
        "support_record",
        "claim_boundary",
        "provenance",
    ):
        assert replay[field] == expected[field]
    assert set(expected["scalar_records"].values()) == {"unsat"}


def test_claim_boundary_keeps_compensation_open():
    theorem = (
        ROOT / "results/ROOT_MONOPOLY_COMPLEMENT_ESCAPE_LEMMA_20260811.md"
    ).read_text()
    assert "v_r(U)" in theorem
    assert "v_q(D)" in theorem
    assert "two-row certificate" in theorem
    assert "does not convert" in theorem
