"""Focused regression for the permanent rank-two flower anchor."""

import json
from pathlib import Path

try:
    from .audit_flower_external_bottom_edge_rank_two_anchor import run
except ImportError:
    from audit_flower_external_bottom_edge_rank_two_anchor import run


ROOT = Path(__file__).resolve().parents[2]


def test_permanent_rank_two_anchor_replays():
    expected = json.loads(
        (ROOT / "results/flower_external_bottom_edge_rank_two_anchor_audit.json").read_text()
    )
    replay = run(ROOT)
    assert replay == expected
    assert expected["sources_distinct"]
    assert expected["parent_supports_disjoint"]
    assert expected["two_by_two_uncovered_count"] == 0


def test_claim_boundary_keeps_reset_recurrence_open():
    theorem = (
        ROOT / "results/FLOWER_EXTERNAL_BOTTOM_EDGE_RANK_TWO_ANCHOR_LEMMA_20260811.md"
    ).read_text()
    assert "not a terminal state" in theorem.replace("\n", " ")
    assert "root-monopoly relation" in theorem
    assert "does not prove" in theorem
