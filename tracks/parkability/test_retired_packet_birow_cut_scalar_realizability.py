from pathlib import Path

from .audit_retired_packet_birow_cut_scalar_realizability import run


ROOT = Path(__file__).resolve().parents[2]


def test_retired_packet_birow_cut_scalar_realizability() -> None:
    result = run(ROOT)
    assert result["status"] == "BIROW_CUT_CAPFREE_SCALAR_REALIZABILITY"
    assert result["branches"] == ["strict", "equality"]
    assert result["all_cases_verified"]
    assert result["all_root_band_cases_verified"]
    assert len(result["cases"]) == 16
    assert not result["full_T_L_times_theorem_refuted"]
