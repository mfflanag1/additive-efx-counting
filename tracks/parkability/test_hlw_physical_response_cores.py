from fractions import Fraction

from .analyze_hlw_physical_response_cores import (
    CURRENT_TARGET_PIECES,
    SUPPLIER_PIECES,
    TARGET_PIECES,
    enumerate_cores,
)


def test_hlw_supplier_partition():
    assert set().union(*SUPPLIER_PIECES.values()) == set(TARGET_PIECES)
    assert sum(map(len, SUPPLIER_PIECES.values())) == len(TARGET_PIECES)
    assert CURRENT_TARGET_PIECES["d"] == TARGET_PIECES


def test_current_threshold_can_remove_a_merely_base_desired_core():
    values = {
        owner: {"h": Fraction(3, 5), "gr": Fraction(3, 5)}
        for owner in ("r", "q", "d", "s")
    }
    goods = ("h", "gr")
    pieces = {"h": "h", "gr": "gr"}
    base = {owner: Fraction(1) for owner in values}
    current = dict(base)
    current["q"] = Fraction(5, 4)
    assert enumerate_cores(values, goods, pieces, base)
    rows = enumerate_cores(values, goods, pieces, current)
    assert all("q" not in row["desired_sources"] for row in rows)
