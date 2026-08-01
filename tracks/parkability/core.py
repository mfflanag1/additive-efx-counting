#!/usr/bin/env python3
"""Exact, solver-free primitives for the parkable-deletion landscape."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Callable, Iterator, Sequence


LANDSCAPE_SCHEMA = "parkability-landscape-v1"


@dataclass(frozen=True, order=True)
class Triple:
    floater: int
    base_owner: tuple[int | None, ...]
    host: int

    def to_dict(self) -> dict:
        return {
            "floater": self.floater,
            "base_owner": list(self.base_owner),
            "host": self.host,
        }


@dataclass(frozen=True)
class ThresholdRotationResult:
    assignment: tuple[int, ...]
    rotations: tuple[tuple[int, ...], ...]
    threshold_potential_trace: tuple[int, ...]
    removable_pairs: tuple[tuple[int, int], ...]


def validate_values(
    values: Sequence[Sequence[int]],
    *,
    expected_n: int | None = None,
    expected_m: int | None = None,
    lower: int = 0,
    upper: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError("values must be a nonempty matrix")
    if any(not isinstance(row, (list, tuple)) or not row for row in values):
        raise ValueError("every value row must be a nonempty sequence")
    n = len(values)
    m = len(values[0])
    if any(len(row) != m for row in values):
        raise ValueError("all value rows must have the same length")
    if expected_n is not None and n != expected_n:
        raise ValueError(f"expected {expected_n} agents, found {n}")
    if expected_m is not None and m != expected_m:
        raise ValueError(f"expected {expected_m} goods, found {m}")

    normalized = []
    for row in values:
        normalized_row = []
        for value in row:
            if type(value) is not int:
                raise ValueError("values must be integers")
            if value < lower or (upper is not None and value > upper):
                interval = (
                    f"[{lower},{upper}]" if upper is not None else f"[{lower},inf)"
                )
                raise ValueError(f"value {value} lies outside {interval}")
            normalized_row.append(value)
        normalized.append(tuple(normalized_row))
    return tuple(normalized)


def validate_instance(raw: dict) -> tuple[tuple[int, ...], ...]:
    if not isinstance(raw, dict):
        raise ValueError("instance must be a JSON object")
    if type(raw.get("n")) is not int or type(raw.get("m")) is not int:
        raise ValueError("instance n and m must be integers")
    return validate_values(
        raw.get("values"),
        expected_n=raw["n"],
        expected_m=raw["m"],
    )


def validate_triple(raw: Triple | dict, n: int, m: int) -> Triple:
    if isinstance(raw, Triple):
        triple = raw
    elif isinstance(raw, dict):
        owner = raw.get("base_owner")
        if not isinstance(owner, list):
            raise ValueError("base_owner must be a JSON list")
        triple = Triple(
            floater=raw.get("floater"),
            base_owner=tuple(owner),
            host=raw.get("host"),
        )
    else:
        raise ValueError("triple must be a Triple or JSON object")

    if type(triple.floater) is not int or not 0 <= triple.floater < m:
        raise ValueError("floater is outside the goods range")
    if type(triple.host) is not int or not 0 <= triple.host < n:
        raise ValueError("host is outside the agent range")
    if len(triple.base_owner) != m:
        raise ValueError(f"base_owner must have length {m}")
    for good, owner in enumerate(triple.base_owner):
        if good == triple.floater:
            if owner is not None:
                raise ValueError("base_owner must be null exactly at the floater")
        elif type(owner) is not int or not 0 <= owner < n:
            raise ValueError("assigned base owners must be agent indices")
    return triple


def bundles_of_base_owner(
    base_owner: Sequence[int | None], n: int
) -> tuple[tuple[int, ...], ...]:
    bundles: list[list[int]] = [[] for _ in range(n)]
    for good, owner in enumerate(base_owner):
        if owner is not None:
            if type(owner) is not int or not 0 <= owner < n:
                raise ValueError("invalid base owner")
            bundles[owner].append(good)
    return tuple(tuple(bundle) for bundle in bundles)


def assignment_to_masks(assignment: Sequence[int], n: int) -> tuple[int, ...]:
    masks = [0] * n
    for good, owner in enumerate(assignment):
        if type(owner) is not int or not 0 <= owner < n:
            raise ValueError("invalid allocation owner")
        masks[owner] |= 1 << good
    return tuple(masks)


def iter_unlabeled_nonempty_partitions(
    n: int,
    m: int,
) -> Iterator[tuple[tuple[int, ...], ...]]:
    if type(n) is not int or type(m) is not int or not 1 <= n <= m:
        raise ValueError("partition dimensions must satisfy 1 <= n <= m")
    assignment = [0] * m

    def visit(good: int, largest_block: int) -> Iterator[tuple[tuple[int, ...], ...]]:
        if good == m:
            if largest_block == n - 1:
                yield tuple(
                    tuple(
                        item
                        for item, block in enumerate(assignment)
                        if block == target
                    )
                    for target in range(n)
                )
            return
        remaining_after = m - good - 1
        for block in range(min(largest_block + 1, n - 1) + 1):
            next_largest = max(largest_block, block)
            if next_largest + remaining_after < n - 1:
                continue
            assignment[good] = block
            yield from visit(good + 1, next_largest)

    yield from visit(1, 0)


def favorite_pair_allocation(
    values: Sequence[Sequence[int]],
) -> tuple[int, ...] | None:
    """Construct a 2-per-agent EFX0 allocation from distinct favorite goods."""
    matrix = validate_values(values)
    n = len(matrix)
    m = len(matrix[0])
    if m != 2 * n:
        raise ValueError("favorite-pair construction requires exactly 2n goods")
    favorites = [
        tuple(good for good, value in enumerate(row) if value == max(row))
        for row in matrix
    ]
    matching = next(
        (
            goods
            for goods in itertools.permutations(range(m), n)
            if all(goods[agent] in favorites[agent] for agent in range(n))
        ),
        None,
    )
    if matching is None:
        return None
    unmatched = iter(good for good in range(m) if good not in matching)
    assignment = [-1] * m
    for agent, favorite in enumerate(matching):
        assignment[favorite] = agent
        assignment[next(unmatched)] = agent
    return tuple(assignment)


def _subset_tables(
    values: tuple[tuple[int, ...], ...],
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    m = len(values[0])
    subset_count = 1 << m
    totals = []
    thresholds = []
    for row in values:
        row_totals = [0] * subset_count
        row_minima = [0] * subset_count
        row_thresholds = [0] * subset_count
        for mask in range(1, subset_count):
            bit = mask & -mask
            good = bit.bit_length() - 1
            rest = mask ^ bit
            row_totals[mask] = row_totals[rest] + row[good]
            row_minima[mask] = (
                row[good] if rest == 0 else min(row_minima[rest], row[good])
            )
            row_thresholds[mask] = row_totals[mask] - row_minima[mask]
        totals.append(tuple(row_totals))
        thresholds.append(tuple(row_thresholds))
    return tuple(totals), tuple(thresholds)


def _is_efx0_masks(
    masks: Sequence[int],
    totals: Sequence[Sequence[int]],
    thresholds: Sequence[Sequence[int]],
) -> bool:
    n = len(masks)
    for observer in range(n):
        own = totals[observer][masks[observer]]
        for target in range(n):
            if observer != target and own < thresholds[observer][masks[target]]:
                return False
    return True


def _base_owner_from_choices(
    m: int, floater: int, goods: Sequence[int], choices: Sequence[int]
) -> tuple[int | None, ...]:
    owner: list[int | None] = [None] * m
    for good, agent in zip(goods, choices):
        owner[good] = agent
    owner[floater] = None
    return tuple(owner)


def efx0_slack_matrix(
    values: Sequence[Sequence[int]],
    bundles: Sequence[Sequence[int]],
) -> list[list[int | None]]:
    normalized = validate_values(values)
    n = len(normalized)
    if len(bundles) != n:
        raise ValueError("one bundle is required per agent")
    matrix: list[list[int | None]] = []
    for observer in range(n):
        own = sum(normalized[observer][good] for good in bundles[observer])
        row: list[int | None] = []
        for target in range(n):
            if observer == target:
                row.append(None)
                continue
            target_bundle = bundles[target]
            threshold = (
                sum(normalized[observer][good] for good in target_bundle)
                - min(normalized[observer][good] for good in target_bundle)
                if target_bundle
                else 0
            )
            row.append(own - threshold)
        matrix.append(row)
    return matrix


def parking_slack_matrix(
    values: Sequence[Sequence[int]],
    bundles: Sequence[Sequence[int]],
    floater: int,
) -> list[list[int | None]]:
    normalized = validate_values(values)
    n = len(normalized)
    m = len(normalized[0])
    if len(bundles) != n or not 0 <= floater < m:
        raise ValueError("invalid bundles or floater")
    matrix: list[list[int | None]] = []
    for observer in range(n):
        own = sum(normalized[observer][good] for good in bundles[observer])
        row: list[int | None] = []
        for host in range(n):
            if observer == host:
                row.append(None)
                continue
            enlarged = tuple(bundles[host]) + (floater,)
            threshold = sum(normalized[observer][good] for good in enlarged) - min(
                normalized[observer][good] for good in enlarged
            )
            row.append(own - threshold)
        matrix.append(row)
    return matrix


def classify_base(
    values: Sequence[Sequence[int]],
    floater: int,
    base_owner: Sequence[int | None],
) -> dict:
    normalized = validate_values(values)
    n = len(normalized)
    m = len(normalized[0])
    triple = validate_triple(
        {"floater": floater, "base_owner": list(base_owner), "host": 0},
        n,
        m,
    )
    bundles = bundles_of_base_owner(triple.base_owner, n)
    base_slacks = efx0_slack_matrix(normalized, bundles)
    parking_slacks = parking_slack_matrix(normalized, bundles, floater)
    finite_base_slacks = [
        slack for row in base_slacks for slack in row if slack is not None
    ]
    own_values = [
        sum(normalized[agent][good] for good in bundles[agent]) for agent in range(n)
    ]
    plain_envy_edges = []
    for observer in range(n):
        for target in range(n):
            if observer == target:
                continue
            target_value = sum(normalized[observer][good] for good in bundles[target])
            if own_values[observer] < target_value:
                plain_envy_edges.append([observer, target])
    host_min_slack = [
        min(parking_slacks[observer][host] for observer in range(n) if observer != host)
        for host in range(n)
    ]
    obstruction_edges = [
        {"observer": observer, "host": host, "slack": parking_slacks[observer][host]}
        for observer in range(n)
        for host in range(n)
        if observer != host and parking_slacks[observer][host] < 0
    ]
    return {
        "floater": floater,
        "base_owner": list(triple.base_owner),
        "bundles": [list(bundle) for bundle in bundles],
        "shape": sorted((len(bundle) for bundle in bundles), reverse=True),
        "own_values": own_values,
        "base_min_efx_slack": min(finite_base_slacks),
        "plain_envy_edges": plain_envy_edges,
        "parking_slack_matrix": parking_slacks,
        "host_min_slack": host_min_slack,
        "parkable_hosts": [
            host for host, slack in enumerate(host_min_slack) if slack >= 0
        ],
        "obstruction_edges": obstruction_edges,
    }


def iter_efx_bases(values: Sequence[Sequence[int]], floater: int) -> Iterator[dict]:
    normalized = validate_values(values, lower=0)
    n = len(normalized)
    m = len(normalized[0])
    if not 0 <= floater < m:
        raise ValueError("floater is outside the goods range")
    totals, thresholds = _subset_tables(normalized)
    goods = tuple(good for good in range(m) if good != floater)
    for choices in itertools.product(range(n), repeat=m - 1):
        masks = [0] * n
        for good, owner in zip(goods, choices):
            masks[owner] |= 1 << good
        if _is_efx0_masks(masks, totals, thresholds):
            owner = _base_owner_from_choices(m, floater, goods, choices)
            yield classify_base(normalized, floater, owner)


def iter_parkable_triples(
    values: Sequence[Sequence[int]], limit: int | None = None
) -> Iterator[Triple]:
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive")
    normalized = validate_values(values, lower=0)
    yielded = 0
    for floater in range(len(normalized[0])):
        for base in iter_efx_bases(normalized, floater):
            owner = tuple(base["base_owner"])
            for host in base["parkable_hosts"]:
                yield Triple(floater, owner, host)
                yielded += 1
                if limit is not None and yielded >= limit:
                    return


def iter_one_nonsingleton_triples(n: int, m: int) -> Iterator[Triple]:
    """Enumerate reverse certificates with one nonsingleton and n-1 singletons."""
    if type(n) is not int or n < 2 or type(m) is not int or m < n:
        raise ValueError("n >= 2 and m >= n are required")
    big_size = m - n + 1
    if big_size < 2:
        return
    goods = tuple(range(m))
    for host in range(n):
        other_agents = tuple(agent for agent in range(n) if agent != host)
        for big_bundle in itertools.combinations(goods, big_size):
            singleton_goods = tuple(
                good for good in goods if good not in big_bundle
            )
            for singleton_owners in itertools.permutations(other_agents):
                completion = [host] * m
                for good, owner in zip(singleton_goods, singleton_owners):
                    completion[good] = owner
                for floater in big_bundle:
                    base_owner: list[int | None] = list(completion)
                    base_owner[floater] = None
                    yield Triple(floater, tuple(base_owner), host)


def triple_is_parkable(
    values: Sequence[Sequence[int]], raw_triple: Triple | dict
) -> bool:
    normalized = validate_values(values, lower=0)
    n = len(normalized)
    m = len(normalized[0])
    triple = validate_triple(raw_triple, n, m)
    totals, thresholds = _subset_tables(normalized)
    bundles = bundles_of_base_owner(triple.base_owner, n)
    masks = tuple(sum(1 << good for good in bundle) for bundle in bundles)
    if not _is_efx0_masks(masks, totals, thresholds):
        return False
    enlarged = masks[triple.host] | (1 << triple.floater)
    for observer in range(n):
        if observer != triple.host and (
            totals[observer][masks[observer]] < thresholds[observer][enlarged]
        ):
            return False
    return True


def threshold_cycle_normal_form(
    values: Sequence[Sequence[int]],
    assignment: Sequence[int],
) -> ThresholdRotationResult:
    normalized = validate_values(values, lower=1)
    n = len(normalized)
    m = len(normalized[0])
    if m < n:
        raise ValueError("threshold-cycle normalization requires at least n goods")
    current = tuple(assignment)
    if len(current) != m:
        raise ValueError(f"assignment must have length {m}")
    totals, thresholds = _subset_tables(normalized)
    masks = assignment_to_masks(current, n)
    if not _is_efx0_masks(masks, totals, thresholds):
        raise ValueError("threshold-cycle normalization requires an EFX0 allocation")

    rotations: list[tuple[int, ...]] = []
    potential_trace: list[int] = []
    seen_assignments: set[tuple[int, ...]] = set()
    while True:
        masks = assignment_to_masks(current, n)
        potential = sum(
            thresholds[owner][masks[owner]] for owner in range(n)
        )
        potential_trace.append(potential)
        best_targets = [
            max(
                range(n),
                key=lambda target: (
                    thresholds[owner][masks[target]],
                    -target,
                ),
            )
            for owner in range(n)
        ]
        if any(
            thresholds[owner][masks[owner]]
            >= thresholds[owner][masks[best_targets[owner]]]
            for owner in range(n)
        ):
            break
        if current in seen_assignments:
            raise AssertionError("threshold-cycle rotation repeated an allocation")
        seen_assignments.add(current)

        path: list[int] = []
        path_index: dict[int, int] = {}
        owner = 0
        while owner not in path_index:
            path_index[owner] = len(path)
            path.append(owner)
            owner = best_targets[owner]
        cycle = tuple(path[path_index[owner] :])
        updated = list(current)
        for receiver in cycle:
            donor = best_targets[receiver]
            for good, prior_owner in enumerate(current):
                if prior_owner == donor:
                    updated[good] = receiver
        next_assignment = tuple(updated)
        next_masks = assignment_to_masks(next_assignment, n)
        if not _is_efx0_masks(next_masks, totals, thresholds):
            raise AssertionError("threshold-cycle rotation did not preserve EFX0")
        next_potential = sum(
            thresholds[owner][next_masks[owner]] for owner in range(n)
        )
        if next_potential <= potential:
            raise AssertionError("threshold-cycle potential did not increase")
        rotations.append(cycle)
        current = next_assignment

    removable_pairs = []
    for good, host in enumerate(current):
        base: list[int | None] = list(current)
        base[good] = None
        triple = Triple(good, tuple(base), host)
        if triple_is_parkable(normalized, triple):
            removable_pairs.append((host, good))
    if not removable_pairs:
        raise AssertionError("threshold-cycle normal form has no removable good")
    return ThresholdRotationResult(
        assignment=current,
        rotations=tuple(rotations),
        threshold_potential_trace=tuple(potential_trace),
        removable_pairs=tuple(removable_pairs),
    )


def count_efx0_allocations(values: Sequence[Sequence[int]]) -> int:
    normalized = validate_values(values, lower=0)
    n = len(normalized)
    m = len(normalized[0])
    totals, thresholds = _subset_tables(normalized)
    count = 0
    for assignment in itertools.product(range(n), repeat=m):
        if _is_efx0_masks(assignment_to_masks(assignment, n), totals, thresholds):
            count += 1
    return count


def iter_efx0_assignments(
    values: Sequence[Sequence[int]],
) -> Iterator[tuple[int, ...]]:
    normalized = validate_values(values, lower=0)
    n = len(normalized)
    m = len(normalized[0])
    totals, thresholds = _subset_tables(normalized)
    for assignment in itertools.product(range(n), repeat=m):
        if _is_efx0_masks(
            assignment_to_masks(assignment, n),
            totals,
            thresholds,
        ):
            yield assignment


def complete_efx0_source_census(
    values: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    normalized = validate_values(values, lower=0)
    n = len(normalized)
    m = len(normalized[0])
    totals, thresholds = _subset_tables(normalized)
    census = [0] * (n + 1)
    for assignment in itertools.product(range(n), repeat=m):
        masks = assignment_to_masks(assignment, n)
        if not _is_efx0_masks(masks, totals, thresholds):
            continue
        source_count = sum(
            all(
                observer == host
                or totals[observer][masks[observer]]
                >= totals[observer][masks[host]]
                for observer in range(n)
            )
            for host in range(n)
        )
        census[source_count] += 1
    return tuple(census)


def bottom_pair_kernel_census(
    values: Sequence[Sequence[int]],
    bottom_goods: Sequence[int],
) -> dict:
    normalized = validate_values(values, lower=0)
    n = len(normalized)
    m = len(normalized[0])
    bottom = tuple(bottom_goods)
    if (
        len(bottom) != 2
        or len(set(bottom)) != 2
        or any(type(good) is not int or not 0 <= good < m for good in bottom)
    ):
        raise ValueError("bottom_goods must contain two distinct valid indices")
    outside = tuple(good for good in range(m) if good not in bottom)
    for observer in range(n):
        if any(
            normalized[observer][low] > normalized[observer][good]
            for low in bottom
            for good in outside
        ):
            raise ValueError("bottom_goods are not a bottom set for every observer")

    reduced = tuple(
        tuple(row[good] for good in outside) for row in normalized
    )
    totals, thresholds = _subset_tables(reduced)
    source_census = [0] * (n + 1)
    equalizations = 0
    efx_count = 0
    for assignment in itertools.product(range(n), repeat=len(outside)):
        masks = assignment_to_masks(assignment, n)
        if not _is_efx0_masks(masks, totals, thresholds):
            continue
        efx_count += 1
        sources = tuple(
            host
            for host in range(n)
            if all(
                observer == host
                or totals[observer][masks[observer]]
                >= totals[observer][masks[host]]
                for observer in range(n)
            )
        )
        source_census[len(sources)] += 1
        bundles = tuple(
            tuple(
                outside[index]
                for index, owner in enumerate(assignment)
                if owner == host
            )
            for host in range(n)
        )
        for host in sources:
            for inserted in bottom:
                enlarged = tuple(
                    bundle + ((inserted,) if target == host else ())
                    for target, bundle in enumerate(bundles)
                )
                if all(
                    sum(normalized[observer][good] for good in enlarged[observer])
                    >= sum(
                        normalized[observer][good] for good in enlarged[target]
                    )
                    for observer in range(n)
                    for target in range(n)
                ):
                    equalizations += 1
    return {
        "efx0_count": efx_count,
        "source_count_census": tuple(source_census),
        "two_source_allocation_count": sum(source_census[2:]),
        "source_equalization_count": equalizations,
    }


def landscape(
    values: Sequence[Sequence[int]],
    *,
    sample_limit: int = 32,
    stop_after: int | None = None,
    detail_sink: Callable[[dict], None] | None = None,
    include_complete_count: bool = True,
) -> dict:
    if sample_limit < 0:
        raise ValueError("sample_limit must be nonnegative")
    if stop_after is not None and stop_after < 1:
        raise ValueError("stop_after must be positive")
    normalized = validate_values(values, lower=0)
    n = len(normalized)
    m = len(normalized[0])
    totals, thresholds = _subset_tables(normalized)
    checked = 0
    host_checks = 0
    base_counts = [0] * m
    triple_counts_by_floater = [0] * m
    triple_counts_by_host = [0] * n
    triple_count = 0
    samples: list[dict] = []

    for floater in range(m):
        goods = tuple(good for good in range(m) if good != floater)
        for choices in itertools.product(range(n), repeat=m - 1):
            checked += 1
            masks = [0] * n
            for good, owner in zip(goods, choices):
                masks[owner] |= 1 << good
            if not _is_efx0_masks(masks, totals, thresholds):
                continue

            base_counts[floater] += 1
            base_owner = _base_owner_from_choices(m, floater, goods, choices)
            base = classify_base(normalized, floater, base_owner)
            host_checks += n
            if detail_sink is not None:
                detail_sink(base)
            for host in base["parkable_hosts"]:
                triple = Triple(floater, base_owner, host)
                triple_count += 1
                triple_counts_by_floater[floater] += 1
                triple_counts_by_host[host] += 1
                if len(samples) < sample_limit:
                    samples.append(triple.to_dict())
                if stop_after is not None and triple_count >= stop_after:
                    return {
                        "schema": LANDSCAPE_SCHEMA,
                        "n": n,
                        "m": m,
                        "exhaustive": False,
                        "deletion_allocations_checked": checked,
                        "deletion_allocations_total": m * n ** (m - 1),
                        "efx0_base_count": sum(base_counts),
                        "efx0_base_count_by_floater": base_counts,
                        "host_checks": host_checks,
                        "parkable_triple_count": triple_count,
                        "parkable_triple_count_by_floater": (triple_counts_by_floater),
                        "parkable_triple_count_by_host": triple_counts_by_host,
                        "triple_sample": samples,
                        "complete_efx0_count": None,
                    }

    complete_count = (
        count_efx0_allocations(normalized) if include_complete_count else None
    )
    return {
        "schema": LANDSCAPE_SCHEMA,
        "n": n,
        "m": m,
        "exhaustive": True,
        "deletion_allocations_checked": checked,
        "deletion_allocations_total": m * n ** (m - 1),
        "efx0_base_count": sum(base_counts),
        "efx0_base_count_by_floater": base_counts,
        "host_checks": host_checks,
        "parkable_triple_count": triple_count,
        "parkable_triple_count_by_floater": triple_counts_by_floater,
        "parkable_triple_count_by_host": triple_counts_by_host,
        "triple_sample": samples,
        "complete_efx0_count": complete_count,
    }
