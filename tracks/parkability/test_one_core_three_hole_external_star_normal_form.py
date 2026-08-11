"""Focused regression for the rank-one external-star normal form."""

import json
from pathlib import Path

try:
    from .audit_one_core_three_hole_external_star_normal_form import run
except ImportError:
    from audit_one_core_three_hole_external_star_normal_form import run


ROOT = Path(__file__).resolve().parents[2]


def test_rank_one_external_star_replays():
    expected = json.loads(
        (ROOT / "results/one_core_three_hole_external_star_normal_form_audit.json").read_text()
    )
    replay = run(ROOT)
    for field in (
        "status",
        "scalar_records",
        "wall_localization",
        "reciprocal_support",
        "reciprocal_support_disjoint",
        "raw_signed_star_count",
        "nonreciprocal_signed_star_count",
        "reciprocal_containing_signed_star_count",
        "claim_boundary",
        "provenance",
    ):
        assert replay[field] == expected[field]
    assert expected["raw_signed_star_count"] == 64
    assert expected["nonreciprocal_signed_star_count"] == 27
    assert expected["reciprocal_containing_signed_star_count"] == 37


def test_claim_boundary_names_flower_selector():
    theorem = (
        ROOT / "results/ONE_CORE_THREE_HOLE_EXTERNAL_STAR_NORMAL_FORM_20260811.md"
    ).read_text()
    assert "three-agent additive EFX theorem" in theorem
    assert "4^3=64" in theorem
    assert "3^3=27" in theorem
    assert "flower-specific external-star selector" in theorem
    assert "does not prove" in theorem
