#!/usr/bin/env python3
"""Exhaustive small-instance checks for injective multi-floater parking."""

from __future__ import annotations

import itertools
import json
import time


def bundle_value(
    values: tuple[tuple[int, ...], ...], observer: int, bundle: list[int]
) -> int:
    return sum(values[observer][good] for good in bundle)


def tau(
    values: tuple[tuple[int, ...], ...], observer: int, bundle: list[int]
) -> int:
    if not bundle:
        return 0
    total = bundle_value(values, observer, bundle)
    return total - min(values[observer][good] for good in bundle)


def is_efx0(
    values: tuple[tuple[int, ...], ...], bundles: list[list[int]]
) -> bool:
    for observer in range(len(bundles)):
        own = bundle_value(values, observer, bundles[observer])
        for target in range(len(bundles)):
            if observer == target:
                continue
            for removed in bundles[target]:
                remainder = sum(
                    values[observer][good]
                    for good in bundles[target]
                    if good != removed
                )
                if own < remainder:
                    return False
    return True


def is_envy_free(
    values: tuple[tuple[int, ...], ...], bundles: list[list[int]]
) -> bool:
    for observer in range(len(bundles)):
        own = bundle_value(values, observer, bundles[observer])
        for target in range(len(bundles)):
            if observer != target and own < bundle_value(
                values, observer, bundles[target]
            ):
                return False
    return True


def base_bundles(n: int, base_assignment: tuple[int, ...]) -> list[list[int]]:
    bundles = [[] for _ in range(n)]
    for good, owner in enumerate(base_assignment):
        bundles[owner].append(good)
    return bundles


def complete_bundles(
    base: list[list[int]],
    leftovers: tuple[int, ...],
    hosts: tuple[int, ...],
) -> list[list[int]]:
    bundles = [bundle.copy() for bundle in base]
    for leftover, host in zip(leftovers, hosts):
        bundles[host].append(leftover)
    return bundles


def single_slack(
    values: tuple[tuple[int, ...], ...],
    base: list[list[int]],
    leftover: int,
    observer: int,
    host: int,
) -> int:
    return bundle_value(
        values, observer, base[observer]
    ) - parking_threshold(
        values, observer, base[host], leftover
    )


def parking_threshold(
    values: tuple[tuple[int, ...], ...],
    observer: int,
    host_bundle: list[int],
    leftover: int,
) -> int:
    if not host_bundle:
        return 0
    host_value = bundle_value(values, observer, host_bundle)
    host_minimum = min(values[observer][good] for good in host_bundle)
    return host_value + max(
        0, values[observer][leftover] - host_minimum
    )


def exact_criterion(
    values: tuple[tuple[int, ...], ...],
    base: list[list[int]],
    leftovers: tuple[int, ...],
    hosts: tuple[int, ...],
) -> bool:
    hosted = dict(zip(hosts, leftovers))
    for host, leftover in zip(hosts, leftovers):
        for observer in range(len(base)):
            if observer == host:
                continue
            bonus = (
                values[observer][hosted[observer]]
                if observer in hosted
                else 0
            )
            if single_slack(
                values, base, leftover, observer, host
            ) + bonus < 0:
                return False
    return True


def safe_edge(
    values: tuple[tuple[int, ...], ...],
    base: list[list[int]],
    leftover: int,
    host: int,
) -> bool:
    return all(
        observer == host
        or single_slack(values, base, leftover, observer, host) >= 0
        for observer in range(len(base))
    )


def base_universal_minimum(
    values: tuple[tuple[int, ...], ...],
    base_goods: tuple[int, ...],
    leftovers: tuple[int, ...],
) -> bool:
    return all(
        values[observer][leftover] <= values[observer][good]
        for observer in range(len(values))
        for leftover in leftovers
        for good in base_goods
    )


def allocation_assignment(
    base_assignment: tuple[int, ...], hosts: tuple[int, ...]
) -> tuple[int, ...]:
    return base_assignment + hosts


def check_family(
    n: int,
    max_base_goods: int,
    max_leftovers: int,
    domain: tuple[int, ...],
) -> dict[str, int]:
    statistics = {
        "valuation_matrices": 0,
        "efx0_bases": 0,
        "injective_placements": 0,
        "safe_matchings": 0,
        "hall_feasible_graphs": 0,
        "empty_host_edges": 0,
        "universal_minimum_bases": 0,
        "rescued_unsafe_placements": 0,
    }
    for base_count in range(max_base_goods + 1):
        base_goods = tuple(range(base_count))
        for leftover_count in range(min(max_leftovers, n) + 1):
            leftovers = tuple(
                range(base_count, base_count + leftover_count)
            )
            good_count = base_count + leftover_count
            entries = n * good_count
            for flat_values in itertools.product(domain, repeat=entries):
                values = tuple(
                    tuple(
                        flat_values[
                            observer * good_count : (observer + 1) * good_count
                        ]
                    )
                    for observer in range(n)
                )
                statistics["valuation_matrices"] += 1
                for assignment in itertools.product(
                    range(n), repeat=base_count
                ):
                    base = base_bundles(n, assignment)
                    if not is_efx0(values, base):
                        continue
                    statistics["efx0_bases"] += 1
                    injections = list(
                        itertools.permutations(range(n), leftover_count)
                    )
                    safe_injections = []
                    direct_efx0 = []
                    seen_allocations = set()
                    for hosts in injections:
                        complete = complete_bundles(base, leftovers, hosts)
                        direct = is_efx0(values, complete)
                        exact = exact_criterion(
                            values, base, leftovers, hosts
                        )
                        assert direct == exact, (
                            "exact criterion",
                            n,
                            values,
                            base,
                            leftovers,
                            hosts,
                            direct,
                            exact,
                        )
                        statistics["injective_placements"] += 1
                        all_safe = all(
                            safe_edge(values, base, leftover, host)
                            for leftover, host in zip(leftovers, hosts)
                        )
                        if all_safe:
                            assert direct
                            safe_injections.append(hosts)
                            statistics["safe_matchings"] += 1
                        if direct:
                            direct_efx0.append(hosts)
                        if direct and not all_safe:
                            statistics["rescued_unsafe_placements"] += 1
                        encoded = allocation_assignment(assignment, hosts)
                        assert encoded not in seen_allocations
                        seen_allocations.add(encoded)

                    assert len(direct_efx0) >= len(safe_injections)
                    assert len(seen_allocations) == len(injections)

                    neighborhoods = {
                        leftover: {
                            host
                            for host in range(n)
                            if safe_edge(values, base, leftover, host)
                        }
                        for leftover in leftovers
                    }
                    hall_feasible = all(
                        len(
                            set().union(
                                *(
                                    neighborhoods[leftover]
                                    for leftover in subset
                                )
                            )
                        )
                        >= len(subset)
                        for subset_size in range(len(leftovers) + 1)
                        for subset in itertools.combinations(
                            leftovers, subset_size
                        )
                    )
                    assert hall_feasible == bool(safe_injections)
                    if hall_feasible:
                        statistics["hall_feasible_graphs"] += 1

                    for host in range(n):
                        for leftover in leftovers:
                            for observer in range(n):
                                assert parking_threshold(
                                    values,
                                    observer,
                                    base[host],
                                    leftover,
                                ) == tau(
                                    values,
                                    observer,
                                    base[host] + [leftover],
                                )

                    for host, bundle in enumerate(base):
                        if bundle:
                            continue
                        for leftover in leftovers:
                            assert safe_edge(values, base, leftover, host)
                            statistics["empty_host_edges"] += 1

                    if is_envy_free(
                        values, base
                    ) and base_universal_minimum(
                        values, base_goods, leftovers
                    ):
                        statistics["universal_minimum_bases"] += 1
                        assert all(
                            safe_edge(values, base, leftover, host)
                            for leftover in leftovers
                            for host in range(n)
                        )
                        assert len(direct_efx0) == len(injections)
    return statistics


def explicit_rescue_regression() -> None:
    values = ((0, 0, 0), (1, 1, 1))
    base = [[0], []]
    leftovers = (1, 2)
    hosts = (0, 1)
    assert is_efx0(values, base)
    assert single_slack(values, base, 1, 1, 0) == -1
    assert not safe_edge(values, base, 1, 0)
    assert exact_criterion(values, base, leftovers, hosts)
    assert is_efx0(values, complete_bundles(base, leftovers, hosts))


def main() -> None:
    started = time.perf_counter()
    explicit_rescue_regression()
    families = {
        "n2_values_0_1_2": check_family(
            n=2,
            max_base_goods=2,
            max_leftovers=2,
            domain=(0, 1, 2),
        ),
        "n3_values_0_1": check_family(
            n=3,
            max_base_goods=1,
            max_leftovers=2,
            domain=(0, 1),
        ),
    }
    assert sum(
        family["rescued_unsafe_placements"] for family in families.values()
    ) > 0
    result = {
        "status": "PASS",
        "theorem": "injective multi-floater exact and safe-edge criteria",
        "families": families,
        "explicit_unsafe_edge_rescue": "PASS",
        "seconds": round(time.perf_counter() - started, 6),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
