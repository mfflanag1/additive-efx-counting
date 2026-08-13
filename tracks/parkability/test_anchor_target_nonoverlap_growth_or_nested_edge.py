from pathlib import Path

from .audit_anchor_target_nonoverlap_growth_or_nested_edge import run


ROOT = Path(__file__).resolve().parents[2]


def test_all_anchor_target_orders_are_covered() -> None:
    result = run(ROOT)
    assert result["status"] == "ANCHOR_TARGET_INEQUALITY_ELIMINATED_TO_NESTED_EDGE"
    assert result["anchor_target_order_count"] == 12
    assert result["direction_counts"] == {"forward": 6, "backward": 6}


def test_nonoverlap_and_nested_algebra() -> None:
    result = run(ROOT)
    assert all(result["symbolic_checks"].values())
    assert result["smallest_terminal"] == "old nested root-facing response edge"
