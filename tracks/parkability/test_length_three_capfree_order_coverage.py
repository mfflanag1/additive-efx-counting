#!/usr/bin/env python3
"""Check the source/order coverage of the proved length-three lemmas."""

import itertools


AGENTS = ("p", "r", "q", "s")
EXPECTED_REMAINDER = {
    "p": set(),
    "r": {
        ("s", "r", "p", "q"),
        ("s", "r", "q", "p"),
    },
    "q": {
        ("p", "r", "q", "s"),
        ("p", "r", "s", "q"),
        ("p", "s", "r", "q"),
        ("s", "p", "r", "q"),
    },
}


def easy(source, order):
    return (
        order[0] in {"q", source}
        or (source != "p" and order[:2] == ("p", source))
        or order[:2] == ("s", "q")
    )


def covered(source, order):
    if easy(source, order):
        return True
    if order.index("q") < order.index("r"):
        return True
    if source == "p" and order == ("s", "p", "r", "q"):
        return True
    if source == "r" and order in {("p", "s", "r", "q"), ("s", "p", "r", "q")}:
        return True
    return source in {"p", "q"} and order.index("r") < order.index("p")


def test_coverage():
    for source in ("p", "r", "q"):
        remainder = {
            order for order in itertools.permutations(AGENTS) if not covered(source, order)
        }
        assert remainder == EXPECTED_REMAINDER[source]


if __name__ == "__main__":
    test_coverage()
    print("length-three cap-free order coverage test passed")
