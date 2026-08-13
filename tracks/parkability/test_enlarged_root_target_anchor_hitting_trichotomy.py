from pathlib import Path

from .audit_enlarged_root_target_anchor_hitting_trichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_enlarged_root_target_anchor_hitting_trichotomy_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "ROOT_TARGET_RESPONSES_REDUCED_TO_SUPPORT_OR_ANCHOR_HITTING"
    assert [record["kind"] for record in result["support_types"]] == [
        "response_side", "anchor_side", "mixed_anchor_hitting"
    ]
    assert all(result["mixed_checks"].values())
    assert all(result["anchor_side_checks"].values())

