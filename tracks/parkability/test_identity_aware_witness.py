#!/usr/bin/env python3
"""Regression tests for the identity-aware minimum-witness abstraction."""

from __future__ import annotations

import itertools
from fractions import Fraction

import pytest

from .audit_identity_aware_witness_realizability import (
    OBSERVERS,
    check_realization,
    realize,
    set_partitions,
    slack_ratio,
)
from .run_identity_aware_witness_side_cegar import (
    concrete_values,
    role_layout,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


PARTITIONS = tuple(sorted(set(set_partitions(OBSERVERS)), key=lambda p: (len(p), p)))


def flat(totals, minima):
    return (
        {o: dict(totals) for o in OBSERVERS},
        {o: dict(minima) for o in OBSERVERS},
    )


def test_four_observers_have_fifteen_partitions():
    assert len(PARTITIONS) == 15
    assert sorted(len(p) for p in PARTITIONS) == [1] + [2] * 7 + [3] * 6 + [4]


@pytest.mark.parametrize("blocks", (1, 2, 3, 4))
def test_block_count_threshold_is_exactly_b_times_the_minimum(blocks):
    """A b-block partition is admitted iff T >= b*M, and shape never matters."""
    minimum = Fraction(1, 7)
    for numerator in range(1, 6):
        total = numerator * minimum
        totals, minima = flat({"g": total}, {"g": minimum})
        for partition in PARTITIONS:
            if len(partition) != blocks:
                continue
            values, blocked = realize(totals, minima, "g", partition)
            admitted = values is not None
            assert admitted == (total >= blocks * minimum), (numerator, partition)
            if admitted:
                assert check_realization(values, totals, minima, "g", partition)
            else:
                assert blocked["blocks"] == blocks


def test_admission_is_blind_to_partition_shape():
    totals, minima = flat({"g": Fraction(10, 3)}, {"g": Fraction(1, 3)})
    by_width = {}
    for partition in PARTITIONS:
        values, _ = realize(totals, minima, "g", partition)
        by_width.setdefault(len(partition), set()).add(values is not None)
    assert all(len(outcomes) == 1 for outcomes in by_width.values())


def test_role_cardinality_is_bounded_by_the_slack_ratio():
    """Any physical role with k goods forces T >= k*M, so k <= slack."""
    totals, minima = flat({"g": Fraction(5, 2)}, {"g": Fraction(1, 2)})
    assert slack_ratio(totals, minima, "g") == 5
    for partition in PARTITIONS:
        values, _ = realize(totals, minima, "g", partition)
        assert values is not None
        assert len(values) <= 5


def test_singleton_role_admits_only_the_one_block_partition():
    totals, minima = flat({"g": Fraction(2, 5)}, {"g": Fraction(2, 5)})
    for partition in PARTITIONS:
        values, blocked = realize(totals, minima, "g", partition)
        assert (values is not None) == (len(partition) == 1)
        if values is None:
            assert blocked["reason"].startswith("singleton role")


def test_every_side_pattern_preserves_totals_and_minima():
    """The witness-side family is a family over one totals/minima profile."""
    totals = {o: {g: Fraction(3 + index, 4) for index, g in enumerate(GOODS)}
              for o in OWNERS}
    minima = {o: {g: Fraction(1, 4) for g in GOODS} for o in OWNERS}
    role_goods, multi = role_layout(totals, minima)
    assert set(multi) == set(GOODS)
    for pattern in itertools.islice(
        itertools.product((False, True), repeat=len(OWNERS)), 16
    ):
        sides = {
            (role, observer): pattern[index]
            for role in multi
            for index, observer in enumerate(OWNERS)
        }
        physical = concrete_values(totals, minima, role_goods, sides)
        for observer in OWNERS:
            for role in GOODS:
                column = [physical[observer, g] for g in role_goods[role]]
                assert sum(column) == totals[observer][role]
                assert min(column) == minima[observer][role]
