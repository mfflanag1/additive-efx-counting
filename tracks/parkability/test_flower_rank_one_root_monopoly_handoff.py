"""Focused regression for the flower rank-one root-monopoly handoff."""

import json
from pathlib import Path

try:
    from .audit_flower_rank_one_root_monopoly_handoff import run
except ImportError:
    from audit_flower_rank_one_root_monopoly_handoff import run


ROOT = Path(__file__).resolve().parents[2]


def test_rank_one_root_monopoly_handoff_replays():
    expected = json.loads(
        (ROOT / "results/flower_rank_one_root_monopoly_handoff_audit.json").read_text()
    )
    replay = run(ROOT)
    for field in (
        "status",
        "scalar_records",
        "response_relation_count",
        "rank_two_relation_count",
        "root_monopoly_relation_count",
        "support_record",
        "claim_boundary",
        "provenance",
    ):
        assert replay[field] == expected[field]
    assert expected["rank_two_relation_count"] == 14
    assert expected["root_monopoly_relation_count"] == 1


def test_claim_boundary_names_bottom_capture():
    theorem = (
        ROOT / "results/FLOWER_RANK_ONE_ROOT_MONOPOLY_HANDOFF_LEMMA_20260811.md"
    ).read_text()
    assert "v_q(U)>v_q(X_q)" in theorem
    assert "K_B:=D_r\\cap B_q\\ne\\varnothing" in theorem
    assert "abstract monopoly branch cannot" in theorem.replace("\n", " ")
