"""Focused regression for common-safe response rigidity."""

import json
from pathlib import Path

try:
    from .audit_common_safe_target_response_rigidity import run
except ImportError:
    from audit_common_safe_target_response_rigidity import run


ROOT = Path(__file__).resolve().parents[2]


def test_common_safe_response_rigidity_replays():
    expected = json.loads(
        (ROOT / "results/common_safe_target_response_rigidity_audit.json").read_text()
    )
    replay = run(ROOT)
    for field in (
        "status",
        "scalar_records",
        "simplified_pivot_support",
        "simplified_pivot_partition_valid",
        "claim_boundary",
        "provenance",
    ):
        assert replay[field] == expected[field]
    assert expected["simplified_pivot_partition_valid"]


def test_rigidity_is_used_by_cross_star_pivot():
    theorem = (
        ROOT / "results/COMMON_SAFE_TARGET_RESPONSE_RIGIDITY_LEMMA_20260811.md"
    ).read_text()
    cross_star = (
        ROOT / "results/CROSS_STAR_HOLE_PIVOT_LEMMA_20260811.md"
    ).read_text()
    assert "D=A" in theorem
    assert "C_d=A_j" in cross_star
    assert "W'=(W\\setminus D_i)" in cross_star
