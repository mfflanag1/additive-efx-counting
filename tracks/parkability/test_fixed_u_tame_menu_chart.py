#!/usr/bin/env python3
"""Regression tests for the chart-level tame-covering-menu results."""

from __future__ import annotations

from fractions import Fraction

import pytest

from .audit_fixed_u_chart_structure import (
    base_block_allocation,
    edges_of,
    efx_failures,
    lemma_d_disjunction,
    supplier_home_allocation,
    tail,
    wall_premise_holds,
)
from .run_fixed_u_tame_menu_chart_theorem import whole_role_certificate
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, PACKETS


def flat(total, minimum):
    totals = {o: {g: total for g in GOODS} for o in OWNERS}
    minima = {o: {g: minimum for g in GOODS} for o in OWNERS}
    return totals, minima


# --- Lemma T: the physical tail is strictly monotone in the role set -------

def test_tail_grows_when_a_role_is_added():
    totals, minima = flat(Fraction(3), Fraction(1))
    small = tail(totals, minima, "d", ("a0",))
    large = tail(totals, minima, "d", ("a0", "a1"))
    assert small == Fraction(2)
    assert large == Fraction(5)
    assert large >= small + totals["d"]["a1"]


def test_tail_grows_even_when_the_added_role_carries_the_new_minimum():
    """The bound of Lemma T is tail(S) + v(g), and it survives a new minimum."""
    totals = {o: {g: Fraction(4) for g in GOODS} for o in OWNERS}
    minima = {o: {g: Fraction(2) for g in GOODS} for o in OWNERS}
    minima["d"]["a1"] = Fraction(1, 2)   # the added role takes over the minimum
    before = tail(totals, minima, "d", ("a0",))
    after = tail(totals, minima, "d", ("a0", "a1"))
    assert before == Fraction(2)
    assert after == Fraction(4) + Fraction(4) - Fraction(1, 2)
    assert after >= before + totals["d"]["a1"]
    assert after > before


@pytest.mark.parametrize("count", (1, 2, 3))
def test_tail_is_monotone_along_a_chain_of_roles(count):
    totals, minima = flat(Fraction(5, 2), Fraction(1, 3))
    chain = GOODS[:count]
    longer = GOODS[:count + 1]
    assert tail(totals, minima, "r", longer) > tail(totals, minima, "r", chain)


# --- the wall premise Lemma D rests on ------------------------------------

def test_wall_premise_detects_both_directions():
    totals, minima = flat(Fraction(1), Fraction(1))
    # A flat profile has v_d(W) = 3 and tail_d(A) = 1, so the wall fails.
    assert not wall_premise_holds(totals, minima)
    for role in PACKETS["W"]:
        totals["d"][role] = Fraction(1, 100)
        minima["d"][role] = Fraction(1, 100)
    # Now v_d(W) = 3/100 while tail_d(A) = 1, so the wall holds.
    assert wall_premise_holds(totals, minima)


# --- Lemma D ---------------------------------------------------------------

def test_lemma_d_rejects_exactly_the_forbidden_shape():
    """d confined to W while a0 and a1 sit together is the forbidden shape."""
    role_owner = {role: "r" for role in GOODS}
    for role in PACKETS["W"]:
        role_owner[role] = "d"
    assert role_owner["a0"] == role_owner["a1"] == "r"
    assert not lemma_d_disjunction(role_owner)

    escaped = dict(role_owner)
    escaped["a1"] = "q"                      # separate a0 from a1
    assert lemma_d_disjunction(escaped)

    escaped = dict(role_owner)
    escaped["h"] = "d"                       # give d a role outside W
    assert lemma_d_disjunction(escaped)


def test_the_forbidden_shape_really_breaks_efx_for_d():
    """Lemma D is not merely combinatorial: EFX fails where it says."""
    totals, minima = flat(Fraction(1), Fraction(1))
    for role in PACKETS["W"]:
        totals["d"][role] = Fraction(1, 100)
        minima["d"][role] = Fraction(1, 100)
    assert wall_premise_holds(totals, minima)
    role_owner = {role: "r" for role in GOODS}
    for role in PACKETS["W"]:
        role_owner[role] = "d"
    assert not lemma_d_disjunction(role_owner)
    assert ("d", "r") in efx_failures(role_owner, totals, minima)


# --- the two refuted constructions ----------------------------------------

@pytest.mark.parametrize("host", OWNERS)
def test_base_block_construction_is_over_the_edge_budget(host):
    assert len(edges_of(base_block_allocation(host))) > 4


@pytest.mark.parametrize("host", OWNERS)
def test_supplier_home_construction_is_cheap_but_forbidden(host):
    role_owner = supplier_home_allocation(host)
    assert len(edges_of(role_owner)) == 1
    # d's support home is exactly W and A sits whole with r, so Lemma D bites
    # unless charity's p happens to land on d.
    if host != "d":
        assert not lemma_d_disjunction(role_owner)


# --- seed certificates are verified, not trusted ---------------------------

def test_seed_certificate_accepts_a_legal_allocation():
    role_owner = supplier_home_allocation("s")
    certificate = whole_role_certificate(role_owner, edge_cap=4)
    assert certificate["branch"] == "W"
    assert certificate["split_role"] is None
    placed = sorted(
        role
        for pieces in certificate["allocations"]["whole"].values()
        for role, _ in pieces
    )
    assert placed == sorted(GOODS)


def test_seed_certificate_rejects_an_over_budget_allocation():
    with pytest.raises(AssertionError):
        whole_role_certificate(base_block_allocation("r"), edge_cap=4)


def test_seed_certificate_rejects_an_incomplete_allocation():
    role_owner = supplier_home_allocation("s")
    role_owner.pop("a0")
    with pytest.raises(AssertionError):
        whole_role_certificate(role_owner, edge_cap=4)
