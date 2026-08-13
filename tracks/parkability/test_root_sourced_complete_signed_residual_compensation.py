from pathlib import Path

from .audit_root_sourced_complete_signed_residual_compensation import run


ROOT = Path(__file__).resolve().parents[2]


def test_complete_residual_pool_supersedes_rq_only_gate() -> None:
    result = run(ROOT)
    assert result["status"] == "RQ_ONLY_GATE_STRICTLY_SUPERSEDED_BY_COMPLETE_RESIDUAL_POOL"
    witness = result["strictness_witness"]
    assert witness["a_A"] == "12"
    assert witness["a_after_Rq"] == "5"
    assert witness["a_after_complete_residual"] == "11"
    assert witness["root_E"] == "13"


def test_full_pool_failure_has_exact_capture_certificate() -> None:
    result = run(ROOT)
    assert all(result["symbolic_checks"].values())
    assert result["correct_separator"] == "full signed-residual pool capture"
    assert len(result["support_records"]) == 16
    assert all(record["disjoint_from_selected_cores"] for record in result["support_records"])
