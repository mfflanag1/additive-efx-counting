#!/usr/bin/env python3
"""Independent, literal verifier for parkable-deletion triples.

This module deliberately does not import the optimized evaluator.  Every EFX0
check expands the removed-good inequalities directly.
"""

from __future__ import annotations

from itertools import product
from typing import Sequence


Triple = tuple[int, tuple[int | None, ...], int]
ValueMatrix = tuple[tuple[int, ...], ...]


def _valid_owner(owner: object, n: int) -> bool:
    return isinstance(owner, int) and not isinstance(owner, bool) and 0 <= owner < n


def _normalize_values(values: Sequence[Sequence[int]]) -> ValueMatrix:
    if not values:
        raise ValueError("values must contain at least one agent")
    matrix = tuple(tuple(row) for row in values)
    m = len(matrix[0])
    if m == 0:
        raise ValueError("values must contain at least one good")
    if any(len(row) != m for row in matrix):
        raise ValueError("all valuation rows must have the same length")
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value < 0
        for row in matrix
        for value in row
    ):
        raise ValueError("valuations must be nonnegative integers")
    return matrix


def _literal_efx0(
    values: ValueMatrix,
    assignment: Sequence[int | None],
    *,
    removed_good: int | None,
) -> bool:
    n = len(values)
    m = len(values[0])
    owners = tuple(assignment)
    if len(owners) != m:
        raise ValueError(f"assignment has length {len(owners)}, expected {m}")

    if removed_good is None:
        if any(not _valid_owner(owner, n) for owner in owners):
            raise ValueError("a complete assignment must use owners 0,...,n-1")
    else:
        if (
            isinstance(removed_good, bool)
            or not isinstance(removed_good, int)
            or removed_good < 0
            or removed_good >= m
        ):
            raise ValueError(f"removed good {removed_good} is outside 0,...,{m - 1}")
        if owners[removed_good] is not None:
            raise ValueError("the removed good must have owner None")
        if any(
            not _valid_owner(owner, n)
            for good, owner in enumerate(owners)
            if good != removed_good
        ):
            raise ValueError("every nonremoved good must use an owner 0,...,n-1")

    bundles = [
        [good for good, owner in enumerate(owners) if owner == target]
        for target in range(n)
    ]
    for observer in range(n):
        own_value = sum(values[observer][good] for good in bundles[observer])
        for target in range(n):
            if observer == target:
                continue
            target_value = sum(values[observer][good] for good in bundles[target])
            for removed_from_target in bundles[target]:
                if own_value < target_value - values[observer][removed_from_target]:
                    return False
    return True


def is_complete_efx0(
    values: Sequence[Sequence[int]], assignment: Sequence[int | None]
) -> bool:
    """Check a complete allocation using every removed-good inequality."""
    return _literal_efx0(_normalize_values(values), assignment, removed_good=None)


def is_removed_good_efx0(
    values: Sequence[Sequence[int]],
    assignment: Sequence[int | None],
    removed_good: int,
) -> bool:
    """Check an EFX0 base in which exactly ``removed_good`` is unassigned."""
    return _literal_efx0(
        _normalize_values(values), assignment, removed_good=removed_good
    )


def is_parkable_triple(
    values: Sequence[Sequence[int]],
    removed_good: int,
    base_assignment: Sequence[int | None],
    host: int,
) -> bool:
    """Check that a base is EFX0 and remains EFX0 after parking at ``host``."""
    matrix = _normalize_values(values)
    n = len(matrix)
    if not _valid_owner(host, n):
        raise ValueError(f"host {host} is outside 0,...,{n - 1}")
    if not _literal_efx0(matrix, base_assignment, removed_good=removed_good):
        return False
    completion = list(base_assignment)
    completion[removed_good] = host
    return _literal_efx0(matrix, completion, removed_good=None)


def count_complete_efx0(values: Sequence[Sequence[int]]) -> int:
    """Count complete EFX0 allocations by direct labeled enumeration."""
    matrix = _normalize_values(values)
    n = len(matrix)
    m = len(matrix[0])
    return sum(
        _literal_efx0(matrix, assignment, removed_good=None)
        for assignment in product(range(n), repeat=m)
    )


def count_removed_good_efx0_bases(
    values: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    """Count EFX0 deletion bases separately for every removed good."""
    matrix = _normalize_values(values)
    n = len(matrix)
    m = len(matrix[0])
    counts = []
    for removed_good in range(m):
        remaining = [good for good in range(m) if good != removed_good]
        count = 0
        for assigned_owners in product(range(n), repeat=m - 1):
            base: list[int | None] = [None] * m
            for good, owner in zip(remaining, assigned_owners):
                base[good] = owner
            if _literal_efx0(matrix, base, removed_good=removed_good):
                count += 1
        counts.append(count)
    return tuple(counts)


def enumerate_base_first(values: Sequence[Sequence[int]]) -> list[Triple]:
    """Enumerate triples by deleted good, then EFX0 base, then host."""
    matrix = _normalize_values(values)
    n = len(matrix)
    m = len(matrix[0])
    triples: list[Triple] = []

    for removed_good in range(m):
        remaining = [good for good in range(m) if good != removed_good]
        for assigned_owners in product(range(n), repeat=m - 1):
            base: list[int | None] = [None] * m
            for good, owner in zip(remaining, assigned_owners):
                base[good] = owner
            if not _literal_efx0(matrix, base, removed_good=removed_good):
                continue
            for host in range(n):
                completion = base.copy()
                completion[removed_good] = host
                if _literal_efx0(matrix, completion, removed_good=None):
                    triples.append((removed_good, tuple(base), host))

    return sorted(triples)


def enumerate_completion_first(
    values: Sequence[Sequence[int]],
) -> list[Triple]:
    """Enumerate complete EFX0 allocations before testing their deletions."""
    matrix = _normalize_values(values)
    n = len(matrix)
    m = len(matrix[0])
    triples: list[Triple] = []

    for completion_tuple in product(range(n), repeat=m):
        if not _literal_efx0(matrix, completion_tuple, removed_good=None):
            continue
        for removed_good in range(m):
            base = list(completion_tuple)
            host = base[removed_good]
            assert host is not None
            base[removed_good] = None
            if _literal_efx0(matrix, base, removed_good=removed_good):
                triples.append((removed_good, tuple(base), host))

    return sorted(triples)
