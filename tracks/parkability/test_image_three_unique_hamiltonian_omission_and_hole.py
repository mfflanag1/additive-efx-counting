"""Regression test for the canonical image-three path omission."""

import json
from pathlib import Path

from .audit_image_three_unique_hamiltonian_omission_and_hole import run


ROOT = Path(__file__).resolve().parents[2]


def test_every_image_three_map_has_one_path_omission():
    result = run()
    expected = json.loads(
        (ROOT / "results/image_three_unique_hamiltonian_omission_and_hole_audit.json").read_text()
    )
    assert result == expected
    assert result["map_count"] == 48
    assert result["valid_hamiltonian_choice_histogram"] == {"1": 48}
    assert result["missing_target_duplicate_class_histogram"] == {
        "missing_supplies_duplicate": 24,
        "foreign_duplicate": 24,
    }
    assert result["all_paths_start_at_missing_source"]
    assert result["all_paths_end_at_omitted_target"]
    assert result["represented_sources_paid_by_desire"]
    assert result["only_missing_owner_can_be_unpaid"]
    assert not result["frozen_supplier_edge_bound_proved"]
    assert not result["missing_owner_payment_proved"]
    assert not result["fixed_u_theorem_proved"]
