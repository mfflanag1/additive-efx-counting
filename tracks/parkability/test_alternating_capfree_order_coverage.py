#!/usr/bin/env python3
"""Check that the cap-free alternating lemmas cover all priority orders."""

from __future__ import annotations

import itertools


AGENTS = ("p", "r", "s", "q")


def test_all_orders_are_covered_once() -> None:
    orders = set(itertools.permutations(AGENTS))
    easy = {
        order
        for order in orders
        if order[0] in {"r", "q"}
        or order[:2] == ("p", "r")
        or order[:2] == ("s", "q")
    }
    root_flip = {("p", "q", "r", "s"), ("s", "r", "q", "p")}
    reservoir = {("p", "s", "r", "q"), ("s", "p", "q", "r")}
    dual_reservoir = {
        ("p", "s", "q", "r"),
        ("p", "q", "s", "r"),
        ("s", "p", "r", "q"),
        ("s", "r", "p", "q"),
    }
    families = (easy, root_flip, reservoir, dual_reservoir)
    assert [len(family) for family in families] == [16, 2, 2, 4]
    assert set().union(*families) == orders
    assert sum(len(family) for family in families) == len(orders)


if __name__ == "__main__":
    test_all_orders_are_covered_once()
    print("alternating cap-free order coverage test passed")
