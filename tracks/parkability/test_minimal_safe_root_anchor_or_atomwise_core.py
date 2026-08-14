from pathlib import Path

from .audit_minimal_safe_root_anchor_or_atomwise_core import run


ROOT = Path(__file__).resolve().parents[2]


def test_minimal_safe_root_anchor_or_atomwise_core() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "ROOT_RESELECTS_PROPER_SAFE_CORE_OR_IS_ATOMWISE_BASE_CRITICAL"
    )
    assert result["critical_good_bound"]
    assert result["multiplicity_bound"]
    assert result["protected_cut_exceeds_root_slack"]
    assert result["terminal"] == (
        "recipient_indivisibility_or_root_double_atomic_birow_cut"
    )
    assert not result["full_T_L_times_theorem_closed"]
