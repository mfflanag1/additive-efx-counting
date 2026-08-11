import json
from pathlib import Path

from .audit_direct_safe_target_subbundle_or_critical_topup import run


ROOT = Path(__file__).resolve().parents[2]


def test_direct_safe_target_subbundle_or_critical_topup_replays():
    expected = json.loads(
        (ROOT / "results/direct_safe_target_subbundle_or_critical_topup_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_direct_safe_target_subbundle_or_critical_topup_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["critical_set_records"] > 0
    assert result["minimal_feasible_sets_every_good_critical"]
    assert len(result["outcomes"]) == 3
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
