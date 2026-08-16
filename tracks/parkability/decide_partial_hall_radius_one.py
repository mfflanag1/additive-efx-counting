#!/usr/bin/env python3
"""Decide a fixed-shape radius-one Hall-completion cell in QF_LRA."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "partial-hall-radius-one-lra-v1"


def candidate_partitions(base, floater):
    n = len(base)
    old_owner = {good: owner for owner, bundle in enumerate(base) for good in bundle}
    moves = [(None, None)] + [
        (good, destination)
        for good, source in old_owner.items()
        for destination in range(n)
        if destination != source
    ]
    seen = set()
    for floater_host in range(n):
        for moved_good, destination in moves:
            bundles = [set(bundle) for bundle in base]
            bundles[floater_host].add(floater)
            source = None
            if moved_good is not None:
                source = old_owner[moved_good]
                bundles[source].remove(moved_good)
                bundles[destination].add(moved_good)
            if any(not bundle for bundle in bundles):
                continue
            partition = tuple(tuple(sorted(bundle)) for bundle in bundles)
            if partition in seen:
                continue
            seen.add(partition)
            yield {
                "floater_host": floater_host,
                "moved_good": moved_good,
                "move_source": source,
                "move_destination": destination,
                "partition": partition,
            }


def bundle_value(row, bundle):
    return z3.Sum([row[good] for good in bundle])


def efx_constraints(values, owned_bundles):
    constraints = []
    n = len(values)
    for agent in range(n):
        own = bundle_value(values[agent], owned_bundles[agent])
        for target in range(n):
            if target == agent:
                continue
            for removed in owned_bundles[target]:
                residual = tuple(
                    good for good in owned_bundles[target] if good != removed
                )
                constraints.append(own >= bundle_value(values[agent], residual))
    return constraints


def matching_failure(values, partition, matching):
    violations = []
    n = len(values)
    for agent in range(n):
        own_bundle = partition[matching[agent]]
        own = bundle_value(values[agent], own_bundle)
        for target in range(n):
            if target == matching[agent]:
                continue
            for removed in partition[target]:
                residual = tuple(good for good in partition[target] if good != removed)
                violations.append(own < bundle_value(values[agent], residual))
    return z3.Or(violations)


def eligible_constraints(values, bundles, floater):
    constraints = efx_constraints(values, bundles)
    constraints.extend(
        bundle_value(values[agent], bundles[agent]) >= values[agent][floater]
        for agent in range(len(values))
    )
    return constraints


def rational(value):
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def integerize(model, values):
    fractions = [
        [rational(model.eval(value, model_completion=True)) for value in row]
        for row in values
    ]
    denominator = math.lcm(
        *(entry.denominator for row in fractions for entry in row)
    )
    integers = [
        [int(entry * denominator) for entry in row]
        for row in fractions
    ]
    return [
        [entry // math.gcd(*row) for entry in row]
        for row in integers
    ]


def run(
    output,
    smt2_output,
    forbid_improving_floater_swaps,
    forbid_improving_bundle_swaps,
    forbid_improving_exchange_cycles,
    forbid_improving_floater_paths,
):
    n = 4
    m = 9
    floater = 8
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    values = [[z3.Real(f"v_{agent}_{good}") for good in range(m)] for agent in range(n)]
    solver = z3.Solver()
    for row in values:
        solver.add(z3.Sum(row) == 1)
        solver.add(*(entry > 0 for entry in row))
    solver.add(*eligible_constraints(values, base, floater))

    improving_swap_exclusion_count = 0
    if forbid_improving_floater_swaps:
        for host, bundle in enumerate(base):
            for removed in bundle:
                swapped = [tuple(items) for items in base]
                swapped[host] = tuple(
                    sorted(good for good in bundle if good != removed) + [floater]
                )
                swap_eligible = eligible_constraints(values, tuple(swapped), removed)
                solver.add(
                    z3.Or(
                        values[host][floater] <= values[host][removed],
                        z3.Or(*(z3.Not(constraint) for constraint in swap_eligible)),
                    )
                )
                improving_swap_exclusion_count += 1

    improving_bundle_swap_exclusion_count = 0
    if forbid_improving_bundle_swaps:
        base_utilities = [
            bundle_value(values[agent], base[agent]) for agent in range(n)
        ]
        for left in range(n):
            for right in range(left + 1, n):
                for left_good in base[left]:
                    for right_good in base[right]:
                        swapped = [tuple(items) for items in base]
                        swapped[left] = tuple(
                            right_good if good == left_good else good
                            for good in base[left]
                        )
                        swapped[right] = tuple(
                            left_good if good == right_good else good
                            for good in base[right]
                        )
                        left_utility = bundle_value(values[left], swapped[left])
                        right_utility = bundle_value(values[right], swapped[right])
                        dominates = z3.And(
                            left_utility >= base_utilities[left],
                            right_utility >= base_utilities[right],
                            z3.Or(
                                left_utility > base_utilities[left],
                                right_utility > base_utilities[right],
                            ),
                        )
                        swap_eligible = eligible_constraints(
                            values, tuple(swapped), floater
                        )
                        solver.add(
                            z3.Or(
                                z3.Not(dominates),
                                z3.Or(
                                    *(z3.Not(constraint) for constraint in swap_eligible)
                                ),
                            )
                        )
                        improving_bundle_swap_exclusion_count += 1

    improving_exchange_cycle_exclusion_count = 0
    if forbid_improving_exchange_cycles:
        base_utilities = [
            bundle_value(values[agent], base[agent]) for agent in range(n)
        ]
        for length in range(2, n + 1):
            for agent_set in itertools.combinations(range(n), length):
                anchor = min(agent_set)
                for tail in itertools.permutations(
                    agent for agent in agent_set if agent != anchor
                ):
                    cycle = (anchor,) + tail
                    if length == 2 and cycle[0] > cycle[1]:
                        continue
                    for selected_goods in itertools.product(
                        *(base[agent] for agent in cycle)
                    ):
                        exchanged = [list(bundle) for bundle in base]
                        for position, source in enumerate(cycle):
                            destination = cycle[(position + 1) % length]
                            good = selected_goods[position]
                            exchanged[source].remove(good)
                            exchanged[destination].append(good)
                        exchanged = tuple(
                            tuple(sorted(bundle)) for bundle in exchanged
                        )
                        exchanged_utilities = [
                            bundle_value(values[agent], exchanged[agent])
                            for agent in range(n)
                        ]
                        dominates = z3.And(
                            *(
                                exchanged_utilities[agent] >= base_utilities[agent]
                                for agent in cycle
                            ),
                            z3.Or(
                                *(
                                    exchanged_utilities[agent]
                                    > base_utilities[agent]
                                    for agent in cycle
                                )
                            ),
                        )
                        exchange_eligible = eligible_constraints(
                            values, exchanged, floater
                        )
                        solver.add(
                            z3.Or(
                                z3.Not(dominates),
                                z3.Or(
                                    *(
                                        z3.Not(constraint)
                                        for constraint in exchange_eligible
                                    )
                                ),
                            )
                        )
                        improving_exchange_cycle_exclusion_count += 1

    improving_floater_path_exclusion_count = 0
    if forbid_improving_floater_paths:
        base_utilities = [
            bundle_value(values[agent], base[agent]) for agent in range(n)
        ]
        for length in range(1, n + 1):
            for path in itertools.permutations(range(n), length):
                for selected_goods in itertools.product(
                    *(base[agent] for agent in path)
                ):
                    exchanged = [list(bundle) for bundle in base]
                    exchanged[path[0]].remove(selected_goods[0])
                    exchanged[path[0]].append(floater)
                    for position in range(1, length):
                        exchanged[path[position]].remove(selected_goods[position])
                        exchanged[path[position]].append(selected_goods[position - 1])
                    new_floater = selected_goods[-1]
                    exchanged = tuple(
                        tuple(sorted(bundle)) for bundle in exchanged
                    )
                    exchanged_utilities = [
                        bundle_value(values[agent], exchanged[agent])
                        for agent in range(n)
                    ]
                    dominates = z3.And(
                        *(
                            exchanged_utilities[agent] >= base_utilities[agent]
                            for agent in path
                        ),
                        z3.Or(
                            *(
                                exchanged_utilities[agent] > base_utilities[agent]
                                for agent in path
                            )
                        ),
                    )
                    exchange_eligible = eligible_constraints(
                        values, exchanged, new_floater
                    )
                    solver.add(
                        z3.Or(
                            z3.Not(dominates),
                            z3.Or(
                                *(
                                    z3.Not(constraint)
                                    for constraint in exchange_eligible
                                )
                            ),
                        )
                    )
                    improving_floater_path_exclusion_count += 1

    partitions = list(candidate_partitions(base, floater))
    matchings = list(itertools.permutations(range(n)))
    for move in partitions:
        partition = move["partition"]
        for matching in matchings:
            solver.add(matching_failure(values, partition, matching))

    if smt2_output:
        smt2_output.write_text(solver.to_smt2())
    verdict = solver.check()
    result = {
        "schema": SCHEMA,
        "status": str(verdict).upper(),
        "meaning": (
            "SAT is an exact eligible partial state with no radius-one Hall "
            "completion; UNSAT proves the fixed canonical base-shape cell."
        ),
        "n": n,
        "m": m,
        "floater": floater,
        "base_bundles": [list(bundle) for bundle in base],
        "candidate_partition_count": len(partitions),
        "matching_count_per_partition": len(matchings),
        "blocked_matching_clause_count": len(partitions) * len(matchings),
        "forbid_improving_floater_swaps": forbid_improving_floater_swaps,
        "improving_floater_swap_exclusion_count": improving_swap_exclusion_count,
        "forbid_improving_bundle_swaps": forbid_improving_bundle_swaps,
        "improving_bundle_swap_exclusion_count": improving_bundle_swap_exclusion_count,
        "forbid_improving_exchange_cycles": forbid_improving_exchange_cycles,
        "improving_exchange_cycle_exclusion_count": improving_exchange_cycle_exclusion_count,
        "forbid_improving_floater_paths": forbid_improving_floater_paths,
        "improving_floater_path_exclusion_count": improving_floater_path_exclusion_count,
        "values": integerize(solver.model(), values) if verdict == z3.sat else None,
        "solver_statistics": str(solver.statistics()),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2-output", type=Path)
    parser.add_argument("--forbid-improving-floater-swaps", action="store_true")
    parser.add_argument("--forbid-improving-bundle-swaps", action="store_true")
    parser.add_argument("--forbid-improving-exchange-cycles", action="store_true")
    parser.add_argument("--forbid-improving-floater-paths", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output,
        args.smt2_output,
        args.forbid_improving_floater_swaps,
        args.forbid_improving_bundle_swaps,
        args.forbid_improving_exchange_cycles,
        args.forbid_improving_floater_paths,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
