"""Regression tests for the anchored q-role classification."""

import json
from pathlib import Path

from .audit_anchored_q_donor_or_source_collision import run


ROOT = Path(__file__).resolve().parents[2]


def test_anchored_q_role_audit_replays():
    expected = json.loads(
        (ROOT / "results/anchored_q_donor_or_source_collision_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_anchored_q_role_split_is_exact():
    result = run(ROOT)
    assert result["stable_anchor_cycle_count"] == 12
    assert result["role_counts"] == {
        "q_donor_available": 6,
        "q_source_collision": 6,
    }
    assert result["cycle_length_counts"] == {
        "q_donor_available": {"3": 2, "4": 4},
        "q_source_collision": {"2": 2, "3": 2, "4": 2},
    }
    assert result["all_non_q_source_cases_have_distinct_q_donor"]
    assert result["protected_q_core_and_root_anchor_intersection"] == ["f"]
    assert not result["direct_protected_q_donor_is_physically_disjoint"]


def test_q_role_claim_boundary_stays_open():
    result = run(ROOT)
    assert "mixed-margin closure" in result["claim_boundary"]
    assert "remain open" in result["claim_boundary"]
