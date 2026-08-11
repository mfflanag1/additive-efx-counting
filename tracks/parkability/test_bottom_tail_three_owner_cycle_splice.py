import json
from pathlib import Path

from .audit_bottom_tail_three_owner_cycle_splice import run


ROOT = Path(__file__).resolve().parents[2]


def test_bottom_tail_cycle_splice_replays():
    expected = json.loads(
        (ROOT / "results/bottom_tail_three_owner_cycle_splice_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_bottom_tail_cycle_splice_has_exact_efx_escape():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["support_conserved"]
    assert result["exact_plateau_escape_is_efx"]
