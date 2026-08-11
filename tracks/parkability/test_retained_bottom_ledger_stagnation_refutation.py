import json
from pathlib import Path

from .audit_retained_bottom_ledger_stagnation_refutation import run


ROOT = Path(__file__).resolve().parents[2]


def test_retained_bottom_plateau_replays():
    expected = json.loads(
        (ROOT / "results/retained_bottom_ledger_stagnation_refutation_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_retained_bottom_plateau_is_exact_and_support_disjoint():
    result = run(ROOT)
    assert result["status"] == "EXACT_BOTTOM_TAIL_PLATEAU"
    assert result["support_disjoint"]
    assert result["ledger_identical_across_all_states"]
