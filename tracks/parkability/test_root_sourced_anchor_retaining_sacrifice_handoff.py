from pathlib import Path

from .audit_root_sourced_anchor_retaining_sacrifice_handoff import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_sourced_anchor_retaining_sacrifice_handoff_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "FULL_POOL_PAYMENT_SUPERSEDED_BY_PRIORITY_VALID_SACRIFICE"
    assert result["root_strict_after_anchor_response_union"]
    assert len(result["physical_records"]) == 4
    assert all(result["wall_exclusions"].values())
    assert result["full_pool_failure_consistent"]


def test_root_sourced_handoff_has_only_labeled_wall_forms() -> None:
    result = run(ROOT)
    assert result["surviving_wall_forms"] == [
        "sacrificed owner to retained core or enlarged root target",
        "represented source to residual",
        "represented nonroot source to enlarged root target",
    ]

