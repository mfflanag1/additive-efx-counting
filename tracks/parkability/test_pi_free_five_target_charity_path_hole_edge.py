import json
from pathlib import Path

from .audit_pi_free_five_target_charity_path_hole_edge import run


ROOT = Path(__file__).resolve().parents[2]


def test_pi_free_five_target_charity_path_hole_edge_replays():
    expected = json.loads(
        (ROOT / "results/pi_free_five_target_charity_path_hole_edge_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_pi_free_five_target_charity_path_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["rank_four_matching_count"] == 120
    assert result["classification_counts"] == {
        "charity_hole_with_owner_cycle": 24,
        "owner_hole_with_owner_cycle": 72,
        "owner_hole_hamiltonian_charity_path": 24,
    }
    assert result["hole_edge_pivot_count"] == 96
    assert result["pivot_cycle_length_counts"] == {
        "1": 24,
        "2": 24,
        "3": 24,
        "4": 24,
    }
