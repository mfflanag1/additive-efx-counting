"""Focused regression for the root-critical alternating frontier."""

import json
from pathlib import Path

try:
    from .audit_root_critical_alternating_frontier import run
except ImportError:
    from audit_root_critical_alternating_frontier import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_critical_frontier_replays():
    expected = json.loads(
        (ROOT / "results/root_critical_alternating_frontier_audit.json").read_text()
    )
    replay = run(ROOT)
    for field in (
        "status",
        "scalar_records",
        "finite_growth",
        "claim_boundary",
        "provenance",
    ):
        assert replay[field] == expected[field]
    assert set(expected["scalar_records"].values()) == {"unsat"}


def test_frontier_routes_to_named_flower_handoffs():
    theorem = (
        ROOT / "results/ROOT_CRITICAL_ALTERNATING_FRONTIER_LEMMA_20260811.md"
    ).read_text()
    assert "strictly enlarges both packet sets" in theorem
    assert "R_A\\cap T_q" in theorem
    assert "captured-bottom handoff" in theorem
    assert "does not" in theorem
