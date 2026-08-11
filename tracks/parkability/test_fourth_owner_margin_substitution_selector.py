import json
from pathlib import Path

from .audit_fourth_owner_margin_substitution_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_fourth_owner_margin_substitution_replays():
    expected = json.loads(
        (ROOT / "results/fourth_owner_margin_substitution_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_fourth_owner_margin_substitution_is_exact():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert set(result["selectors"]) == {"J_star", "L_star"}
