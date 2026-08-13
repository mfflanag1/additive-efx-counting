from pathlib import Path

from .audit_permanent_anchor_retire_on_backup_exchange_independent import run


ROOT = Path(__file__).resolve().parents[2]


def test_permanent_anchor_retire_on_backup_exchange_independent_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "INDEPENDENT_EXACT_REPLAY_PASSED"
    assert result["root_priority_cases"] > 0
    assert result["supplier_return_cases"] > 0
    assert result["unchanged_wall_implication_cases"] == 625
    assert result["shrunken_root_target_cases"] > 0
    assert result["physical_replay_passed"]

