#!/usr/bin/env python3
"""Regression tests for the realization-free slack-two results."""

from __future__ import annotations

import itertools
from fractions import Fraction

import pytest

from .run_identity_aware_one_minimum_split_cegar import (
    HIGH,
    LOW,
    WHOLE,
    numeric_piece_floor,
    numeric_piece_value,
    pieces_for,
    role_is_multi,
    role_slack_is_two,
    side_patterns,
)
from .run_identity_aware_witness_side_batch import slack
from .run_realization_free_universality_cegar import classify_roles
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def spread(total, minimum, count):
    """A cardinality-`count` value column with this total and this minimum.

    The Lemma A construction: one good attains the minimum, the remainder is
    shared evenly, and every value stays at or above the minimum exactly when
    `total >= count * minimum`.
    """
    assert total >= count * minimum
    if count == 1:
        assert total == minimum
        return (minimum,)
    rest = Fraction(total - minimum, count - 1)
    return (minimum, *((rest,) * (count - 1)))


def flat(values):
    return {observer: dict(values) for observer in OWNERS}


# --- the cardinality-free form of Lemma C ---------------------------------

@pytest.mark.parametrize("count", (1, 2, 3, 4, 5, 9))
def test_a_column_of_any_width_keeps_its_total_and_its_minimum(count):
    minimum = Fraction(3, 11)
    total = count * minimum + Fraction(5, 4) if count > 1 else minimum
    column = spread(total, minimum, count)
    assert len(column) == count
    assert sum(column) == total
    assert min(column) == minimum
    assert all(value >= minimum for value in column)


@pytest.mark.parametrize("count", (2, 3, 4, 7))
def test_an_unsplit_role_matches_its_two_good_stand_in(count):
    """The stand-in `{M, T-M}` reproduces the total and the deletion floor."""
    minimum, total = Fraction(1, 5), Fraction(9, 5)
    wide = spread(total, minimum, count)
    stand_in = (minimum, total - minimum)
    assert sum(wide) == sum(stand_in) == total
    assert min(wide) == min(stand_in) == minimum
    # Every deletion candidate of the wide column is at least the stand-in's
    # smallest, so the binding EFX constraint is the same one.
    assert all(value >= min(stand_in) for value in wide)


def test_the_two_good_stand_in_is_forced_at_slack_two():
    """Lemma B: a slack-two multi-good role has no other value column."""
    minimum, total = Fraction(2, 7), Fraction(4, 7)
    assert total < 3 * minimum and total >= 2 * minimum
    with pytest.raises(AssertionError):
        spread(total, minimum, 3)
    assert spread(total, minimum, 2) == (minimum, total - minimum)


# --- tame / wild classification -------------------------------------------

def profile(per_role):
    totals = {o: {} for o in OWNERS}
    minima = {o: {} for o in OWNERS}
    for role in GOODS:
        total, minimum = per_role[role]
        for observer in OWNERS:
            totals[observer][role] = total
            minima[observer][role] = minimum
    return totals, minima


def test_classify_roles_splits_exactly_at_slack_three():
    one = Fraction(1)
    per_role = {}
    for index, role in enumerate(GOODS):
        # cycle singleton / tame / wild across the twelve roles
        per_role[role] = ((one, one), (2 * one, one), (5 * one, one))[index % 3]
    totals, minima = profile(per_role)
    _, multi, tame, wild = classify_roles(totals, minima)
    for role in tame:
        assert slack(totals, minima, role) == 2
    for role in wild:
        assert slack(totals, minima, role) >= 3
    assert set(tame) | set(wild) == set(multi)
    assert not set(tame) & set(wild)
    assert all(slack(totals, minima, r) == 1 for r in GOODS if r not in multi)


def test_role_slack_predicates_agree_with_the_slack_statistic():
    totals, minima = profile({role: (Fraction(7, 2), Fraction(1)) for role in GOODS})
    for role in GOODS:
        assert role_is_multi(totals, minima, role)
        assert not role_slack_is_two(totals, minima, role)
        assert slack(totals, minima, role) == 3
    totals, minima = profile({role: (Fraction(5, 2), Fraction(1)) for role in GOODS})
    for role in GOODS:
        assert role_slack_is_two(totals, minima, role)


# --- the eight side patterns ----------------------------------------------

def test_side_patterns_are_the_eight_relabelling_classes():
    patterns = side_patterns()
    assert len(patterns) == 8
    assert all(p["r"] == 0 for p in patterns)
    assert len({tuple(p[o] for o in OWNERS) for p in patterns}) == 8
    # Every pattern of the four observers is one of these up to a global flip.
    seen = set()
    for bits in itertools.product((0, 1), repeat=len(OWNERS)):
        flipped = tuple(1 - b for b in bits)
        seen.add(min(bits, flipped))
    assert seen == {tuple(p[o] for o in OWNERS) for p in patterns}


def test_the_split_pieces_carry_the_forced_column_and_their_own_floor():
    """Witness side is worth M, the other side T-M, and each is one good."""
    totals, minima = profile({role: (Fraction(5, 2), Fraction(1)) for role in GOODS})
    role = GOODS[0]
    for pattern in side_patterns():
        for observer in OWNERS:
            values = {
                kind: numeric_piece_value(
                    totals, minima, observer, (role, kind), pattern
                )
                for kind in (LOW, HIGH)
            }
            assert sum(values.values()) == totals[observer][role]
            assert min(values.values()) == minima[observer][role]
            for kind in (LOW, HIGH):
                # A single good deletes at its own value, not at the role's.
                assert numeric_piece_floor(
                    totals, minima, observer, (role, kind), pattern
                ) == values[kind]
        witness = LOW if pattern[observer] == 0 else HIGH
        assert values[witness] == minima[observer][role]


def test_a_whole_role_always_deletes_at_the_role_minimum():
    totals, minima = profile({role: (Fraction(9, 2), Fraction(1)) for role in GOODS})
    trivial = {o: 0 for o in OWNERS}
    for role in GOODS:
        for observer in OWNERS:
            piece = (role, WHOLE)
            assert numeric_piece_value(
                totals, minima, observer, piece, trivial
            ) == totals[observer][role]
            assert numeric_piece_floor(
                totals, minima, observer, piece, trivial
            ) == minima[observer][role]


@pytest.mark.parametrize("split_role", (None, "a0", "l"))
def test_the_move_family_covers_every_role_exactly_once(split_role):
    pieces = pieces_for(split_role)
    roles = [role for role, _ in pieces]
    assert sorted(set(roles)) == sorted(GOODS)
    assert len(pieces) == len(GOODS) + (1 if split_role else 0)
    if split_role is not None:
        assert sorted(k for r, k in pieces if r == split_role) == [LOW, HIGH]
