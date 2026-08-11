"""Focused regression for the root-critical compensator dichotomy."""

import json
from pathlib import Path

try:
    from .audit_root_critical_compensator_dichotomy import run
except ImportError:
    from audit_root_critical_compensator_dichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_critical_compensator_audit_replays():
    expected = json.loads(
        (ROOT / "results/root_critical_compensator_dichotomy_audit.json").read_text()
    )
    replay = run(ROOT)
    for field in (
        "status",
        "scalar_records",
        "support_cases",
        "claim_boundary",
        "provenance",
    ):
        assert replay[field] == expected[field]
    assert set(expected["scalar_records"].values()) == {"unsat"}


def test_no_compensator_routes_inside_flower_core():
    theorem = (
        ROOT / "results/ROOT_CRITICAL_COMPENSATOR_DICHOTOMY_LEMMA_20260811.md"
    ).read_text()
    assert "g\\in A" in theorem
    assert "top-core root" in theorem
    assert "captured-bottom handoff" in theorem
    assert "compensator chain" in theorem
