from pathlib import Path

from .audit_allocated_e_pi_free_payment_counterprofile import run


def test_allocated_e_pi_free_payment_counterprofile(tmp_path: Path):
    result = run(tmp_path / "audit.json")
    assert result["fixed_master_replay"] == "sat"
    assert result["generalized_pi_family_count"] == 0
    assert result["paid_matching_witness_count"] == 0
    assert result["unrestricted_efx_witness_count"] == 78
    assert result["minimum_efx_edge_count"] == 2
