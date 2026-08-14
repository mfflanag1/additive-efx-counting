from pathlib import Path

from .audit_root_facing_holder_price_duality import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_facing_holder_price_duality_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "ROOT_BAND_IDENTIFIED_WITH_BOUNDED_HOLDER_PRICE_SEPARATOR"
    )
    assert result["root_balance_identity"]
    assert result["weak_compensation_threshold"]
    assert result["strict_compensation_threshold"]
    assert result["band_price_identity"]
    assert result["band_price_bounds"]
    assert not result["full_T_L_times_theorem_closed"]

