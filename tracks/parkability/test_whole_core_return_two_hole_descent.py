"""Focused regression for whole-core return rank descent."""

import json
from pathlib import Path

try:
    from .audit_whole_core_return_two_hole_descent import run
except ImportError:
    from audit_whole_core_return_two_hole_descent import run


ROOT = Path(__file__).resolve().parents[2]


def test_whole_core_descent_replays():
    expected = json.loads(
        (ROOT / "results/whole_core_return_two_hole_descent_audit.json").read_text()
    )
    replay = run(ROOT)
    for field in (
        "status",
        "scalar_records",
        "support_partition",
        "support_partition_valid",
        "two_by_two_relation_count",
        "two_by_two_uncovered_count",
        "claim_boundary",
        "provenance",
    ):
        assert replay[field] == expected[field]
    assert expected["two_by_two_uncovered_count"] == 0


def test_claim_boundary_names_rank_one_gate():
    theorem = (
        ROOT / "results/WHOLE_CORE_RETURN_TWO_HOLE_DESCENT_LEMMA_20260811.md"
    ).read_text()
    assert "never needs a hole pivot" in theorem
    assert "one-core/three-hole state" in theorem
    assert "exact dimension-descent gate" in theorem.replace("\n", " ")
