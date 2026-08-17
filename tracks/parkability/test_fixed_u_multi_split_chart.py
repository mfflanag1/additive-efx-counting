#!/usr/bin/env python3
"""Regression tests for the multi-tame-split chart oracle.

The central test is `test_narrowing_a_certificate_to_visited_patterns_is_rejected`:
it reproduces the exact defect that produced the superseded obstruction -- a cut
justified only on the patterns a search happened to visit -- and asserts the
driver refuses it.  The instrument must not be able to repeat that class of
error quietly.
"""

from __future__ import annotations

import itertools

import pytest

from .run_fixed_u_multi_split_chart_theorem import (
    CAP_BOUND,
    CLOSED,
    HALT_VERDICT,
    OBSTRUCTION_STATUSES,
    WIDE_FAMILY_FAILED,
    WIDE_FAMILY_INCONCLUSIVE,
    PatternCoverageError,
    audit_pattern_coverage,
    carries_witness,
    expected_pattern_keys,
    pattern_key,
    pieces_for_set,
    role_patterns,
    side_pattern_vectors,
    whole_role_certificate,
)
from .run_identity_aware_one_minimum_split_cegar import HIGH, LOW, WHOLE
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


def supplier_home_map(host):
    role_owner = {}
    for owner, roles in SUPPORT_STATE.items():
        for role in roles:
            role_owner[role] = host if owner == "charity" else owner
    return role_owner


def stub_certificate(split_roles):
    """A certificate whose allocations are placeholders; only keys matter here."""
    split_roles = tuple(sorted(split_roles))
    return {
        "branch": "W" if not split_roles else "M",
        "split_roles": list(split_roles),
        "allocations": {
            pattern_key(split_roles, vector): {}
            for vector in side_pattern_vectors(split_roles)
        },
    }


# --- the side-pattern product is the full 8^k --------------------------------

def test_one_role_has_the_eight_relabelling_classes():
    patterns = role_patterns()
    assert len(patterns) == 8
    assert all(p["r"] == 0 for p in patterns)
    seen = set()
    for bits in itertools.product((0, 1), repeat=len(OWNERS)):
        seen.add(min(bits, tuple(1 - b for b in bits)))
    assert seen == {tuple(p[o] for o in OWNERS) for p in patterns}


@pytest.mark.parametrize("k", (0, 1, 2, 3))
def test_the_pattern_product_has_exactly_eight_to_the_k_vectors(k):
    split_roles = GOODS[:k]
    vectors = side_pattern_vectors(split_roles)
    assert len(vectors) == 8 ** k
    assert len({pattern_key(split_roles, v) for v in vectors}) == 8 ** k
    assert len(expected_pattern_keys(split_roles)) == 8 ** k


def test_every_split_role_varies_independently():
    """The product is a product: fixing one role still leaves 8 for the other."""
    split_roles = ("a0", "l")
    vectors = side_pattern_vectors(split_roles)
    fixed = [v for v in vectors if v["a0"] == role_patterns()[0]]
    assert len(fixed) == 8
    assert len({pattern_key(split_roles, v) for v in fixed}) == 8


# --- the coverage audit ------------------------------------------------------

@pytest.mark.parametrize("split_roles", ((), ("a0",), ("a0", "l"), ("a0", "l", "m")))
def test_a_complete_certificate_passes_the_coverage_audit(split_roles):
    certificate = stub_certificate(split_roles)
    assert audit_pattern_coverage(certificate) == 8 ** len(split_roles)


@pytest.mark.parametrize("split_roles", (("a0",), ("a0", "l"), ("a0", "l", "m")))
def test_narrowing_a_certificate_to_visited_patterns_is_rejected(split_roles):
    """The defect that produced the superseded obstruction, caught.

    A search that visits some pattern vectors and emits a cut justified only on
    those is unsound: an unvisited vector is a realization the certificate never
    covered.  Narrow a complete certificate to a 'visited' subset and the audit
    must refuse it.
    """
    certificate = stub_certificate(split_roles)
    visited = dict(itertools.islice(certificate["allocations"].items(), 3))
    assert len(visited) < len(certificate["allocations"])
    narrowed = {**certificate, "allocations": visited}
    with pytest.raises(PatternCoverageError) as caught:
        audit_pattern_coverage(narrowed)
    assert "missing" in str(caught.value)


def test_dropping_a_single_pattern_is_still_rejected():
    """Off-by-one coverage is the dangerous case, so it must not slip through."""
    split_roles = ("a0", "l")
    certificate = stub_certificate(split_roles)
    allocations = dict(certificate["allocations"])
    allocations.pop(sorted(allocations)[0])
    assert len(allocations) == 8 ** 2 - 1
    with pytest.raises(PatternCoverageError):
        audit_pattern_coverage({**certificate, "allocations": allocations})


def test_a_certificate_cannot_vouch_for_its_own_coverage():
    """Keys for the wrong split set are rejected, not accepted as 'complete'."""
    certificate = stub_certificate(("a0", "l"))
    impostor = {
        "branch": "M",
        "split_roles": ["a0", "l", "m"],       # claims three, carries two roles'
        "allocations": certificate["allocations"],
    }
    with pytest.raises(PatternCoverageError):
        audit_pattern_coverage(impostor)


def test_padding_with_unexpected_keys_does_not_satisfy_the_audit():
    split_roles = ("a0",)
    certificate = stub_certificate(split_roles)
    allocations = dict(certificate["allocations"])
    allocations.pop(sorted(allocations)[0])
    allocations["a0:9999"] = {}                # right count, wrong key
    assert len(allocations) == 8
    with pytest.raises(PatternCoverageError) as caught:
        audit_pattern_coverage({**certificate, "allocations": allocations})
    assert "unexpected" in str(caught.value)


# --- pieces and witness sides ------------------------------------------------

def test_pieces_cover_every_role_and_split_exactly_the_split_set():
    split_roles = ("a0", "l")
    pieces = pieces_for_set(split_roles)
    assert sorted({role for role, _ in pieces}) == sorted(GOODS)
    assert len(pieces) == len(GOODS) + len(split_roles)
    for role in split_roles:
        assert sorted(k for r, k in pieces if r == role) == [LOW, HIGH]
    for role in GOODS:
        if role not in split_roles:
            assert [k for r, k in pieces if r == role] == [WHOLE]


def test_exactly_one_side_carries_the_witness():
    for bit in (0, 1):
        assert carries_witness(LOW, bit) != carries_witness(HIGH, bit)
    assert carries_witness(LOW, 0) and not carries_witness(HIGH, 0)
    assert carries_witness(HIGH, 1) and not carries_witness(LOW, 1)


# --- seeds -------------------------------------------------------------------

def test_a_seed_is_a_zero_split_certificate_and_passes_the_audit():
    certificate = whole_role_certificate(supplier_home_map("s"), edge_cap=4)
    assert certificate["split_roles"] == []
    assert certificate["pattern_count"] == 1
    assert audit_pattern_coverage(certificate) == 1


# --- a search limit must never be reported as an obstruction -----------------

def test_only_a_genuine_wide_family_failure_counts_as_an_obstruction():
    """The defect that produced the second false SAT, caught by construction.

    A pattern budget too small to express the closing menu, or an inconclusive
    wide-family run, are limits of the instrument.  Neither may be dressed up
    as a countermodel.
    """
    assert OBSTRUCTION_STATUSES == {WIDE_FAMILY_FAILED}
    assert CAP_BOUND not in OBSTRUCTION_STATUSES
    assert WIDE_FAMILY_INCONCLUSIVE not in OBSTRUCTION_STATUSES
    for status in (CAP_BOUND, WIDE_FAMILY_INCONCLUSIVE):
        verdict = HALT_VERDICT[status]
        assert verdict.startswith("HALTED_")
        assert "SAT" not in verdict.replace("NOT_AN_OBSTRUCTION", "")
    assert HALT_VERDICT[WIDE_FAMILY_FAILED].startswith("SAT_")


def test_every_negative_outcome_has_a_distinct_verdict():
    assert set(HALT_VERDICT) == {
        WIDE_FAMILY_FAILED, CAP_BOUND, WIDE_FAMILY_INCONCLUSIVE
    }
    assert len(set(HALT_VERDICT.values())) == 3
    assert CLOSED not in HALT_VERDICT


@pytest.mark.parametrize("budget,expected_sizes", (
    (1, []), (8, [1]), (64, [1, 2]), (512, [1, 2, 3]),
))
def test_the_pattern_budget_admits_exactly_the_affordable_split_sizes(
    budget, expected_sizes
):
    """8^k <= budget is the rule; sizes above it are unaffordable, not absent."""
    affordable = [k for k in range(1, 5) if 8 ** k <= budget]
    assert affordable == expected_sizes


def test_a_seed_over_the_edge_budget_is_refused():
    role_owner = supplier_home_map("s")
    role_owner["a0"] = "q"
    role_owner["a1"] = "d"
    role_owner["h"] = "s"
    role_owner["l"] = "r"
    with pytest.raises(AssertionError):
        whole_role_certificate(role_owner, edge_cap=1)
