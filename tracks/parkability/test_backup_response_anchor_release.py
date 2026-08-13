from pathlib import Path

from .audit_backup_response_anchor_release import run


ROOT = Path(__file__).resolve().parents[2]


def test_backup_response_anchor_release_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "CONDITIONAL_ANCHOR_RELEASE_LOCALIZATION_VERIFIED"
    assert result["root_paid_and_old_targets_safe"]
    assert result["residual_owner_strictly_improves"]
    assert result["support_partition_valid"]
    assert result["only_possible_new_wall_target"] == "W+K"
    assert result["permanent_anchor_released"]
