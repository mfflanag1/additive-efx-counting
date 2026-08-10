#!/usr/bin/env python3
"""Regression checks for the three-nonsingleton frontier census."""

try:
    from .decide_three_nonsingleton_cycle_census import run as run_census
    from .audit_three_nonsingleton_length_two_return_wall import run as run_return_wall
    from .decide_three_nonsingleton_flower_direct_swap import run as run_direct_swap
    from .decide_three_nonsingleton_flower_source_grid import run as run_source_grid
    from .decide_three_nonsingleton_flower_one_unpaid_cover import run as run_one_unpaid
    from .decide_three_nonsingleton_flower_one_unpaid_lra import run as run_one_unpaid_lra
    from .decide_three_nonsingleton_flower_abstract_low_wall import run as run_low_wall
    from .decide_three_nonsingleton_flower_payment_menu import run as run_payment_menu
except ImportError:
    from decide_three_nonsingleton_cycle_census import run as run_census
    from audit_three_nonsingleton_length_two_return_wall import run as run_return_wall
    from decide_three_nonsingleton_flower_direct_swap import run as run_direct_swap
    from decide_three_nonsingleton_flower_source_grid import run as run_source_grid
    from decide_three_nonsingleton_flower_one_unpaid_cover import run as run_one_unpaid
    from decide_three_nonsingleton_flower_one_unpaid_lra import run as run_one_unpaid_lra
    from decide_three_nonsingleton_flower_abstract_low_wall import run as run_low_wall
    from decide_three_nonsingleton_flower_payment_menu import run as run_payment_menu

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    census = run_census()
    assert census["status"] == "EXHAUSTIVE"
    assert census["class_count"] == 8
    assert {
        (record["cycle_length"], record["cycle_pattern"], tuple(record["external_types"]))
        for record in census["classes"]
    } == {
        (2, "GG", ("L", "S")),
        (3, "GGL", ("S",)),
        (3, "GGS", ("L",)),
        (3, "GGG", ("S",)),
        (4, "GGLS", ()),
        (4, "GGSL", ()),
        (4, "GLGS", ()),
        (4, "GGGS", ()),
    }

    wall = run_return_wall()
    assert wall["status"] == "VERIFIED"
    assert all(wall["checks"].values())
    assert "not asserted globally maximal" in wall["claim_boundary"]

    direct = run_direct_swap()
    assert direct["status"] == "FORCED"
    assert direct["source_cell"] == {
        "third_arm_source": "s",
        "singleton_envier": "c",
    }

    source_grid = run_source_grid()
    assert source_grid["status"] == "EXHAUSTIVE"
    assert source_grid["counts"] == {
        "CLOSED_DIRECT_CS_SWAP": 4,
        "CLOSED_FOUR_SOURCE_MATCHING": 4,
        "OPEN": 28,
    }

    one_unpaid = run_one_unpaid()
    assert one_unpaid["status"] == "EXHAUSTIVE"
    assert one_unpaid["cell_count"] == 864
    assert one_unpaid["all_fixed_or_improving_count"] == 432
    assert one_unpaid["one_unpaid_count"] == 432
    assert not one_unpaid["uncovered"]
    for record in one_unpaid["records"]:
        if record["status"] == "ONE_UNPAID":
            assert record["unpaid_agent"] in ("r", "q")
            assert record["assignment"][record["unpaid_agent"]] in ("A_q", "A_r")

    one_unpaid_lra = run_one_unpaid_lra()
    assert one_unpaid_lra["status"] == "ALL_FORCED"
    assert one_unpaid_lra["case_count"] == 864

    low_wall = run_low_wall()
    assert low_wall["status"] == "COMPLETE"
    assert low_wall["counts"] == {"IMPOSSIBLE": 148, "sat": 284, "unknown": 0}

    payment_menu = run_payment_menu()
    assert payment_menu["status"] == "ALL_MINIMAL"
    assert payment_menu["record_count"] == 148
    assert payment_menu["menu_sizes"] == {"4": 148}
    assert sorted(entry["count"] for entry in payment_menu["canonical_menu_types"]) == [12, 12, 18, 18, 44, 44]

    theorem = (
        ROOT
        / "results"
        / "THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md"
    ).read_text()
    for word in ("`GG`", "`GGL`", "`GGS`", "`GGG`", "`GGLS`", "`GGSL`", "`GLGS`", "`GGGS`"):
        assert word in theorem
    assert "Length-two flower reduction" in theorem
    assert "36 source cells" in theorem
    assert "Direct flower swap" in theorem
    assert "Four-source packet matching" in theorem
    assert "One-unpaid cover theorem" in theorem
    assert "432" in theorem
    assert "Four-cover strict-cycle lemma" in theorem
    assert "284" in theorem
    assert "not asserted globally maximal" in theorem
    print("three-nonsingleton cycle census tests passed")


if __name__ == "__main__":
    main()
