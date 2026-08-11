import json
from pathlib import Path

from .audit_compensated_fourth_owner_residual_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_compensated_fourth_owner_selector_replays():
    expected = json.loads(
        (ROOT / "results/compensated_fourth_owner_residual_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_compensated_fourth_owner_selector_is_exact():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["support_conserved"]
    assert result["canonical_M"].startswith("maximize s(M)")
