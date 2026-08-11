import json
from pathlib import Path

from .audit_gg_rank_reset_raw_potential_globality_gap import run


ROOT = Path(__file__).resolve().parents[2]


def test_raw_potential_witness_globality_gap_replays():
    expected = json.loads(
        (ROOT / "results/gg_rank_reset_raw_potential_globality_gap_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_raw_potential_witness_is_not_full_gg_countermodel():
    result = run(ROOT)
    assert result["status"] == "GLOBALITY_GAP_CONFIRMED"
    assert result["allocation_space"] == 5 ** 9
    assert result["priority_count"] == 24
    assert result["globally_maximal_priorities"] == []
