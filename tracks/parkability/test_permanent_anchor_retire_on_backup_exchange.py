from pathlib import Path

from .audit_permanent_anchor_retire_on_backup_exchange import run


ROOT = Path(__file__).resolve().parents[2]


def test_permanent_anchor_retire_on_backup_exchange_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "CONDITIONAL_EXCHANGE_VERIFIED_PREMISE_NOT_SUPPLIED"
    assert result["root_priority_and_unchanged_target_payment"]
    assert result["original_supplier_strictly_improves"]
    assert result["unchanged_wall_monotonicity"]
    assert result["shrunken_root_target_current_safe"]
    assert result["physical_partition_and_signed_return_valid"]
    assert result["only_genuinely_new_wall_target"] == "Q+K"
    assert result["old_anchor_retired"]
