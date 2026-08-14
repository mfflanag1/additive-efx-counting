"""Regression tests for nonroot three-placement collision elimination."""

import json
from pathlib import Path

from .audit_nonroot_three_placement_relay_collision_elimination import run


ROOT = Path(__file__).resolve().parents[2]


def test_nonroot_three_placement_replays():
    expected = json.loads(
        (ROOT / "results/nonroot_three_placement_relay_collision_elimination_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_root_holder_dependency_is_absent():
    result = run(ROOT)
    assert result["status"] == "ROOT_HOLDER_DEPENDENCY_ELIMINATED"
    assert not result["imported_complete_collision_theorem_required"]
    assert all(not record["root_holder"] for record in result["nonroot_probe_records"])
    assert "remain open" in result["claim_boundary"]
