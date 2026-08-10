#!/usr/bin/env python3
"""Check the two-orientation cover of the length-three reservoir theorem."""

import itertools


AGENTS = ("p", "r", "q", "s")
EXPECTED_REMAINDER = {
    "p": set(),
    "r": set(),
    "q": set(),
}


def covered(_source, order):
    return (
        order.index("q") < order.index("r")
        or order.index("r") < order.index("q")
    )


def test_coverage():
    orders = set(itertools.permutations(AGENTS))
    q_before_r = {order for order in orders if order.index("q") < order.index("r")}
    r_before_q = {order for order in orders if order.index("r") < order.index("q")}
    assert q_before_r.isdisjoint(r_before_q)
    assert q_before_r | r_before_q == orders
    assert len(q_before_r) == len(r_before_q) == 12
    for source in ("p", "r", "q"):
        remainder = {
            order for order in itertools.permutations(AGENTS) if not covered(source, order)
        }
        assert remainder == EXPECTED_REMAINDER[source]


if __name__ == "__main__":
    test_coverage()
    print("length-three cap-free order coverage test passed")
