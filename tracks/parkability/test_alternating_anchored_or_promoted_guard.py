#!/usr/bin/env python3
"""Regression test for the desired-set guard in promoted CEGAR cuts."""

import z3

try:
    from .run_alternating_anchored_or_promoted_split_cegar import (
        restricted_rival_blocker,
    )
    from .run_alternating_split_packet_cegar import concrete_rival_blocker
except ImportError:
    from run_alternating_anchored_or_promoted_split_cegar import (
        restricted_rival_blocker,
    )
    from run_alternating_split_packet_cegar import concrete_rival_blocker


def test_non_desired_promoted_allocation_does_not_cut_master_model():
    values = [[0] * 11 for _ in range(4)]
    values[0][0] = values[0][1] = 1
    values[1][1] = 2
    values[1][2] = 3
    symbolic = tuple(tuple(z3.RealVal(entry) for entry in row) for row in values)
    base_own = tuple(z3.RealVal(1) for _ in range(4))
    owner = (0, 0, 1, None, None, None, None, None, None, None, None)
    order = (0, 2, 3, 1)

    assert z3.is_false(z3.simplify(concrete_rival_blocker(symbolic, base_own, owner, order)))
    assert z3.is_true(
        z3.simplify(
            restricted_rival_blocker(
                symbolic, base_own, owner, order, "any-desired"
            )
        )
    )


if __name__ == "__main__":
    test_non_desired_promoted_allocation_does_not_cut_master_model()
