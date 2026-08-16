#!/usr/bin/env python3
"""Adversarially search the distinct-half branch for a trapped rank plateau."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import (
        FAVORITE,
        M,
        N,
        build_state_graph,
        half_matching,
        universal_threshold_failure,
    )
    from .decide_distinct_half_pair_cover import balanced_state_universe
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import (
        FAVORITE,
        M,
        N,
        build_state_graph,
        half_matching,
        universal_threshold_failure,
    )
    from decide_distinct_half_pair_cover import balanced_state_universe


SCHEMA = "distinct-half-rank-augmentation-anneal-v1"
NORMALIZED_FAVORITE = 100
REPRESENTATIVE_GOODS = frozenset(range(1, 5))
SIX_ORBIT_SIGNATURES = frozenset(
    {
        ("R", 0, ("RR", "RU")),
        ("R", 1, ("RR", "UU")),
        ("R", 1, ("RU", "RU")),
        ("R", 2, ("RU", "UU")),
        ("U", 2, ("RR", "UU")),
        ("U", 2, ("RU", "RU")),
    }
)


def favorite_pair_orbit_signature(partition):
    favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
    if len(favorite_bundle) != 2:
        return None
    partner = next(good for good in favorite_bundle if good != FAVORITE)
    triple = next(bundle for bundle in partition if len(bundle) == 3)
    pairs = tuple(
        bundle
        for bundle in partition
        if len(bundle) == 2 and FAVORITE not in bundle
    )

    def pair_type(bundle):
        representatives = sum(good in REPRESENTATIVE_GOODS for good in bundle)
        return "R" * representatives + "U" * (2 - representatives)

    return (
        "R" if partner in REPRESENTATIVE_GOODS else "U",
        sum(good in REPRESENTATIVE_GOODS for good in triple),
        tuple(sorted(pair_type(bundle) for bundle in pairs)),
    )


def favorite_triple_cell_counts(values):
    counts = Counter()
    for low_goods in itertools.combinations(range(1, M), 2):
        residual = tuple(
            good for good in range(1, M) if good not in low_goods
        )
        for matching in perfect_pairings(residual):
            masks = tuple(
                sum(
                    1 << agent
                    for agent, row in enumerate(values)
                    if (
                        sum(row[good] for good in pair)
                        >= row[FAVORITE]
                        + max(row[good] for good in low_goods)
                    )
                )
                for pair in matching
            )
            if any(
                all(
                    masks[position] & (1 << agent)
                    for position, agent in enumerate(agents)
                )
                for agents in itertools.permutations(range(N), 3)
            ):
                counts[low_goods] += 1
    return counts


def normalize(values):
    return tuple(
        (NORMALIZED_FAVORITE,)
        + tuple(
            max(
                1,
                min(
                    NORMALIZED_FAVORITE - 1,
                    round(NORMALIZED_FAVORITE * value / row[FAVORITE]),
                ),
            )
            for value in row[1:]
        )
        for row in values
    )


@lru_cache(maxsize=None)
def perfect_pairings(goods):
    if not goods:
        return ((),)
    first = goods[0]
    result = []
    for partner in goods[1:]:
        remaining = tuple(
            good for good in goods if good not in (first, partner)
        )
        for rest in perfect_pairings(remaining):
            result.append(((first, partner),) + rest)
    return tuple(result)


def load_values(path: Path):
    payload = json.loads(path.read_text())
    raw = payload.get("values")
    if raw is None:
        raw = payload["trace"][-1]["values"]
    return normalize(tuple(tuple(map(int, row)) for row in raw))


def branch_valid(values):
    return (
        all(universal_threshold_failure(row) for row in values)
        and half_matching(values) is not None
    )


@lru_cache(maxsize=1 << 16)
def maximum_matching_rank(graph_masks):
    reachable = {0}
    for mask in graph_masks:
        reachable |= {
            used | (1 << bundle)
            for used in tuple(reachable)
            for bundle in range(N)
            if mask & (1 << bundle) and not used & (1 << bundle)
        }
    return max(mask.bit_count() for mask in reachable)


class Landscape:
    def __init__(self, universe_name="favorite_pair"):
        if universe_name == "favorite_pair":
            self.universe, self.neighbors = build_state_graph()
        else:
            self.universe = tuple(balanced_state_universe())
            index = {
                partition: position
                for position, partition in enumerate(self.universe)
            }
            neighbors = []
            for partition in self.universe:
                adjacent = set()
                for left, right in itertools.combinations(range(N), 2):
                    for left_good in partition[left]:
                        for right_good in partition[right]:
                            bundles = [list(bundle) for bundle in partition]
                            bundles[left].remove(left_good)
                            bundles[left].append(right_good)
                            bundles[right].remove(right_good)
                            bundles[right].append(left_good)
                            candidate = tuple(
                                sorted(
                                    tuple(sorted(bundle)) for bundle in bundles
                                )
                            )
                            adjacent.add(index[candidate])
                neighbors.append(tuple(sorted(adjacent)))
            self.neighbors = tuple(neighbors)
            if (
                len(self.universe) != 1260
                or sum(map(len, self.neighbors)) != 2 * 15120
                or {len(items) for items in self.neighbors} != {24}
            ):
                raise AssertionError("balanced single-swap graph census changed")
        self.bundle_masks = tuple(
            tuple(sum(1 << good for good in bundle) for bundle in partition)
            for partition in self.universe
        )
        self.row_cache = {}

    @staticmethod
    def row_tables(row):
        sums = [0] * (1 << M)
        minima = [10**9] * (1 << M)
        for mask in range(1, 1 << M):
            low_bit = mask & -mask
            good = low_bit.bit_length() - 1
            previous = mask ^ low_bit
            sums[mask] = sums[previous] + row[good]
            minima[mask] = min(minima[previous], row[good])
        return sums, minima

    def row_graph_masks(self, row):
        cached = self.row_cache.get(row)
        if cached is not None:
            return cached
        sums, minima = self.row_tables(row)
        result = []
        for bundle_masks in self.bundle_masks:
            thresholds = tuple(
                sums[mask] - minima[mask] for mask in bundle_masks
            )
            required = max(thresholds)
            result.append(
                sum(
                    1 << bundle
                    for bundle, mask in enumerate(bundle_masks)
                    if sums[mask] >= required
                )
            )
        cached = tuple(result)
        self.row_cache[row] = cached
        return cached

    def ranks(self, values):
        graph_rows = tuple(self.row_graph_masks(row) for row in values)
        return tuple(
            maximum_matching_rank(tuple(row[position] for row in graph_rows))
            for position in range(len(self.universe))
        )

    def audit(self, values):
        ranks = self.ranks(values)
        favorite_pair_perfect = 0
        six_orbit_perfect = 0
        favorite_triple_perfect = 0
        favorite_triple_cells = Counter()
        common_low_triple_repairs = 0
        for position, partition in enumerate(self.universe):
            favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
            if ranks[position] == N:
                if len(favorite_bundle) == 2:
                    favorite_pair_perfect += 1
                    if (
                        favorite_pair_orbit_signature(partition)
                        in SIX_ORBIT_SIGNATURES
                    ):
                        six_orbit_perfect += 1
                elif len(favorite_bundle) == 3:
                    favorite_triple_perfect += 1
                    favorite_triple_cells[
                        tuple(good for good in favorite_bundle if good != FAVORITE)
                    ] += 1
            if len(favorite_bundle) != 3:
                continue
            low_goods = tuple(good for good in favorite_bundle if good != FAVORITE)
            pairs = tuple(bundle for bundle in partition if bundle != favorite_bundle)
            if all(
                all(
                    sum(row[good] for good in pair)
                    >= row[FAVORITE] + max(row[good] for good in low_goods)
                    for pair in pairs
                )
                for row in values
            ):
                common_low_triple_repairs += 1
        if not favorite_triple_cells:
            favorite_triple_cells = favorite_triple_cell_counts(values)
            favorite_triple_perfect = sum(favorite_triple_cells.values())
        robust_low_pairs = []
        two_core_tutte_low_pairs = []
        for low_goods in itertools.combinations(range(1, M), 2):
            residual = tuple(
                good for good in range(1, M) if good not in low_goods
            )
            edge_masks = {
                pair: sum(
                    (1 << agent)
                    for agent, row in enumerate(values)
                    if (
                        sum(row[good] for good in pair)
                        >= row[FAVORITE]
                        + max(row[good] for good in low_goods)
                    )
                )
                for pair in itertools.combinations(residual, 2)
            }
            minimum_accepting_agents = min(
                mask.bit_count() for mask in edge_masks.values()
            )
            if minimum_accepting_agents >= N - 1:
                robust_low_pairs.append(
                    {
                        "low_goods": list(low_goods),
                        "minimum_accepting_agents": minimum_accepting_agents,
                    }
                )
            for core_agents in itertools.combinations(range(N), 2):
                core_mask = sum(1 << agent for agent in core_agents)
                if any(
                    mask & core_mask != core_mask
                    for mask in edge_masks.values()
                ):
                    continue
                outsider_mask = ((1 << N) - 1) ^ core_mask
                bad_edges = {
                    pair
                    for pair, mask in edge_masks.items()
                    if not mask & outsider_mask
                }
                bad_has_perfect_matching = any(
                    all(tuple(sorted(pair)) in bad_edges for pair in matching)
                    for matching in perfect_pairings(residual)
                )
                if not bad_has_perfect_matching:
                    two_core_tutte_low_pairs.append(
                        {
                            "low_goods": list(low_goods),
                            "core_agents": list(core_agents),
                            "bad_edge_count": len(bad_edges),
                        }
                    )
        radius_two_rank_three_exits = []
        for start, rank in enumerate(ranks):
            if rank != N - 1:
                continue
            exits = {
                neighbor
                for neighbor in self.neighbors[start]
                if ranks[neighbor] == N
            }
            for middle in self.neighbors[start]:
                if ranks[middle] != N - 1:
                    continue
                exits.update(
                    neighbor
                    for neighbor in self.neighbors[middle]
                    if ranks[neighbor] == N
                )
            radius_two_rank_three_exits.append((len(exits), start))
        seen = set()
        trapped = []
        exit_counts = []
        component_sizes = []
        for start, rank in enumerate(ranks):
            if rank == N or start in seen:
                continue
            component = []
            higher = set()
            stack = [start]
            seen.add(start)
            while stack:
                current = stack.pop()
                component.append(current)
                for neighbor in self.neighbors[current]:
                    if ranks[neighbor] > rank:
                        higher.add(neighbor)
                    elif ranks[neighbor] == rank and neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            exit_counts.append(len(higher))
            component_sizes.append(len(component))
            if not higher:
                trapped.append(
                    {
                        "rank": rank,
                        "component_size": len(component),
                        "partition": [
                            list(bundle) for bundle in self.universe[component[0]]
                        ],
                    }
                )
        histogram = Counter(ranks)
        minimum_radius_two = min(radius_two_rank_three_exits, default=(None, None))
        three_observer_cells = []
        for parked in itertools.combinations(range(1, M), 2):
            remaining = tuple(
                good for good in range(1, M) if good not in parked
            )
            agent_slacks = tuple(
                min(
                    row[left] + row[right]
                    - row[FAVORITE]
                    - max(row[good] for good in parked)
                    for left, right in itertools.combinations(remaining, 2)
                )
                for row in values
            )
            three_observer_cells.append(
                (sorted(agent_slacks, reverse=True)[2], parked, agent_slacks)
            )
        best_cell_slack, best_cell_parked, best_cell_agent_slacks = max(
            three_observer_cells
        )
        representatives = half_matching(values)
        canonical_two_core_tutte_low_pairs = tuple(
            witness
            for witness in two_core_tutte_low_pairs
            if set(witness["low_goods"]).issubset(representatives)
            and set(witness["core_agents"])
            == {
                agent
                for agent, representative in enumerate(representatives)
                if representative not in witness["low_goods"]
            }
        )
        return {
            "matching_rank_histogram": {
                str(rank): count for rank, count in sorted(histogram.items())
            },
            "perfect_partition_count": histogram[N],
            "favorite_pair_perfect_partition_count": favorite_pair_perfect,
            "six_orbit_perfect_partition_count": six_orbit_perfect,
            "favorite_triple_perfect_partition_count": favorite_triple_perfect,
            "maximum_favorite_triple_cell_count": max(
                favorite_triple_cells.values(), default=0
            ),
            "full_favorite_triple_cell_count": sum(
                count == 15 for count in favorite_triple_cells.values()
            ),
            "maximum_three_observer_cell_slack": best_cell_slack,
            "best_three_observer_cell_parked_goods": list(best_cell_parked),
            "best_three_observer_cell_agent_slacks": list(
                best_cell_agent_slacks
            ),
            "common_low_triple_repair_partition_count": (
                common_low_triple_repairs
            ),
            "robust_low_pair_count": len(robust_low_pairs),
            "robust_low_pairs": robust_low_pairs,
            "two_core_tutte_low_pair_count": len(two_core_tutte_low_pairs),
            "two_core_tutte_low_pairs": two_core_tutte_low_pairs,
            "canonical_two_core_tutte_low_pair_count": len(
                canonical_two_core_tutte_low_pairs
            ),
            "canonical_two_core_tutte_low_pairs": list(
                canonical_two_core_tutte_low_pairs
            ),
            "minimum_higher_rank_exit_count": min(exit_counts, default=None),
            "minimum_deficient_component_size": min(component_sizes, default=None),
            "minimum_radius_two_rank_three_exit_count": minimum_radius_two[0],
            "minimum_radius_two_rank_three_exit_partition": (
                [
                    list(bundle)
                    for bundle in self.universe[minimum_radius_two[1]]
                ]
                if minimum_radius_two[1] is not None
                else None
            ),
            "trapped_nonperfect_plateau_count": len(trapped),
            "trapped_nonperfect_plateau_sample": trapped[:1],
        }


def score(record, objective_name):
    if (
        objective_name
        not in (
            "balanced", "dichotomy", "full_cell", "gate", "robust",
            "three_observer", "triple", "two_core", "canonical_two_core",
            "orbit_gate"
        )
        and record["trapped_nonperfect_plateau_count"]
    ):
        return (-1, 0, record["perfect_partition_count"])
    if objective_name == "perfect":
        return (
            record["perfect_partition_count"],
            record["minimum_higher_rank_exit_count"] or 10**9,
            record["minimum_radius_two_rank_three_exit_count"] or 0,
        )
    if objective_name == "dichotomy":
        return (
            record["favorite_pair_perfect_partition_count"],
            record["common_low_triple_repair_partition_count"],
            record["favorite_triple_perfect_partition_count"],
        )
    if objective_name == "gate":
        return (
            record["favorite_pair_perfect_partition_count"],
            record["favorite_triple_perfect_partition_count"],
            record["common_low_triple_repair_partition_count"],
        )
    if objective_name == "full_cell":
        return (
            record["favorite_pair_perfect_partition_count"],
            record["maximum_favorite_triple_cell_count"],
            record["favorite_triple_perfect_partition_count"],
        )
    if objective_name == "orbit_gate":
        return (
            record["full_favorite_triple_cell_count"],
            record["six_orbit_perfect_partition_count"],
            record["favorite_pair_perfect_partition_count"],
        )
    if objective_name == "three_observer":
        return (
            record["favorite_pair_perfect_partition_count"],
            record["maximum_three_observer_cell_slack"],
            record["favorite_triple_perfect_partition_count"],
        )
    if objective_name == "robust":
        return (
            record["favorite_pair_perfect_partition_count"],
            record["robust_low_pair_count"],
            record["favorite_triple_perfect_partition_count"],
        )
    if objective_name == "two_core":
        return (
            record["favorite_pair_perfect_partition_count"],
            record["two_core_tutte_low_pair_count"],
            record["favorite_triple_perfect_partition_count"],
        )
    if objective_name == "canonical_two_core":
        return (
            record["favorite_pair_perfect_partition_count"],
            record["canonical_two_core_tutte_low_pair_count"],
            record["favorite_triple_perfect_partition_count"],
        )
    if objective_name == "balanced":
        return (
            record["perfect_partition_count"],
            record["favorite_pair_perfect_partition_count"],
            record["common_low_triple_repair_partition_count"],
        )
    if objective_name == "triple":
        return (
            record["favorite_triple_perfect_partition_count"],
            record["favorite_pair_perfect_partition_count"],
            record["perfect_partition_count"],
        )
    radius_two = record["minimum_radius_two_rank_three_exit_count"]
    if radius_two is None:
        radius_two = 10**9
    return (
        radius_two,
        record["minimum_higher_rank_exit_count"] or 10**9,
        record["perfect_partition_count"],
    )


def scalar(record, objective_name):
    key = score(record, objective_name)
    if objective_name in (
        "balanced", "perfect", "dichotomy", "full_cell", "gate", "robust",
        "three_observer", "triple", "two_core", "canonical_two_core",
        "orbit_gate"
    ):
        return key[0] + 0.0001 * key[1] + 0.0000001 * key[2]
    return key[0] + 0.0001 * key[1] + 0.0000001 * key[2]


def mutate(values, rng, scale):
    candidate = [list(row) for row in values]
    agent = rng.randrange(N)
    good = rng.randrange(1, M)
    if rng.random() < 0.75:
        delta = rng.choice((-1, 1)) * rng.randint(1, max(scale, 2))
        candidate[agent][good] = max(
            1,
            min(NORMALIZED_FAVORITE - 1, candidate[agent][good] + delta),
        )
    else:
        candidate[agent][good] = rng.randint(1, NORMALIZED_FAVORITE - 1)
    return tuple(tuple(row) for row in candidate)


def random_profile(rng):
    while True:
        values = tuple(
            (NORMALIZED_FAVORITE,)
            + tuple(rng.randint(1, NORMALIZED_FAVORITE - 1) for _ in range(M - 1))
            for _ in range(N)
        )
        if branch_valid(values):
            return values


def run(seed_paths, iterations, random_seed, restart_every, initial_temperature,
        final_temperature, objective_name, universe_name):
    rng = random.Random(random_seed)
    landscape = Landscape(universe_name)
    seeds = [load_values(path) for path in seed_paths]
    seeds.extend(random_profile(rng) for _ in range(max(4, len(seeds))))
    seeds = [values for values in seeds if branch_valid(values)]
    evaluated = [(landscape.audit(values), values) for values in seeds]
    evaluated.sort(key=lambda item: score(item[0], objective_name))
    current_record, current = evaluated[0]
    best_record, best = current_record, current
    started = time.time()
    completed = 0

    for iteration in range(1, iterations + 1):
        completed = iteration
        if iteration > 1 and (iteration - 1) % restart_every == 0:
            current_record, current = evaluated[
                ((iteration - 1) // restart_every) % len(evaluated)
            ]
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        scale = max(
            2,
            round(
                (NORMALIZED_FAVORITE / 5)
                * temperature
                / initial_temperature
            ),
        )
        candidate = mutate(current, rng, scale)
        if not branch_valid(candidate):
            continue
        candidate_record = landscape.audit(candidate)
        change = (
            scalar(candidate_record, objective_name)
            - scalar(current_record, objective_name)
        )
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current, current_record = candidate, candidate_record
        if score(candidate_record, objective_name) < score(
            best_record, objective_name
        ):
            best, best_record = candidate, candidate_record
            print(
                f"iteration={iteration} "
                f"score={score(best_record, objective_name)}",
                flush=True,
            )
            if (
                (
                    objective_name
                    not in (
                        "balanced", "dichotomy", "full_cell", "gate",
                        "robust", "three_observer", "triple", "two_core",
                        "canonical_two_core", "orbit_gate"
                    )
                    and best_record["trapped_nonperfect_plateau_count"]
                )
                or (
                    objective_name == "balanced"
                    and best_record["perfect_partition_count"] == 0
                )
                or (
                    objective_name == "full_cell"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["maximum_favorite_triple_cell_count"] < 15
                )
                or (
                    objective_name == "orbit_gate"
                    and best_record["six_orbit_perfect_partition_count"] == 0
                    and best_record["maximum_favorite_triple_cell_count"] < 15
                )
                or (
                    objective_name == "three_observer"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["maximum_three_observer_cell_slack"] < 0
                )
                or (
                    objective_name == "gate"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["favorite_triple_perfect_partition_count"] == 0
                )
                or (
                    objective_name == "robust"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["robust_low_pair_count"] == 0
                )
                or (
                    objective_name == "two_core"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["two_core_tutte_low_pair_count"] == 0
                )
                or (
                    objective_name == "canonical_two_core"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record[
                        "canonical_two_core_tutte_low_pair_count"
                    ]
                    == 0
                )
                or (
                    objective_name == "dichotomy"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["common_low_triple_repair_partition_count"] == 0
                )
                or (
                    objective_name == "triple"
                    and best_record["favorite_triple_perfect_partition_count"] == 0
                )
            ):
                break

    return {
        "schema": SCHEMA,
        "status": (
            "COUNTEREXAMPLE"
            if (
                (
                    objective_name
                    not in (
                        "balanced", "dichotomy", "full_cell", "gate",
                        "robust", "three_observer", "triple", "two_core",
                        "canonical_two_core", "orbit_gate"
                    )
                    and best_record["trapped_nonperfect_plateau_count"]
                )
                or (
                    objective_name == "balanced"
                    and best_record["perfect_partition_count"] == 0
                )
                or (
                    objective_name == "full_cell"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["maximum_favorite_triple_cell_count"] < 15
                )
                or (
                    objective_name == "orbit_gate"
                    and best_record["six_orbit_perfect_partition_count"] == 0
                    and best_record["maximum_favorite_triple_cell_count"] < 15
                )
                or (
                    objective_name == "three_observer"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["maximum_three_observer_cell_slack"] < 0
                )
                or (
                    objective_name == "gate"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["favorite_triple_perfect_partition_count"] == 0
                )
                or (
                    objective_name == "robust"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["robust_low_pair_count"] == 0
                )
                or (
                    objective_name == "two_core"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["two_core_tutte_low_pair_count"] == 0
                )
                or (
                    objective_name == "canonical_two_core"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record[
                        "canonical_two_core_tutte_low_pair_count"
                    ]
                    == 0
                )
                or (
                    objective_name == "dichotomy"
                    and best_record["favorite_pair_perfect_partition_count"] == 0
                    and best_record["common_low_triple_repair_partition_count"] == 0
                )
                or (
                    objective_name == "triple"
                    and best_record["favorite_triple_perfect_partition_count"] == 0
                )
            )
            else "CHECKPOINT"
        ),
        "scope": (
            "integer profiles normalized to favorite 100 satisfying the exact "
            "universal-threshold branch and a half-favorite SDR"
        ),
        "iterations_completed": completed,
        "elapsed_seconds": time.time() - started,
        "random_seed": random_seed,
        "objective": objective_name,
        "universe": universe_name,
        "values": [list(row) for row in best],
        "half_favorite_representatives": list(half_matching(best)),
        "audit": best_record,
        "warning": "A checkpoint is finite falsification evidence, not a proof.",
    }


def main():
    global NORMALIZED_FAVORITE
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--iterations", type=int, default=10_000)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--restart-every", type=int, default=1_000)
    parser.add_argument("--initial-temperature", type=float, default=4.0)
    parser.add_argument("--final-temperature", type=float, default=0.02)
    parser.add_argument(
        "--objective",
        choices=(
            "radius", "perfect", "balanced", "dichotomy", "full_cell",
            "gate", "robust", "three_observer", "triple", "two_core",
            "canonical_two_core", "orbit_gate"
        ),
        default="radius",
    )
    parser.add_argument(
        "--universe",
        choices=("favorite_pair", "balanced"),
        default="favorite_pair",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--normalized-favorite", type=int, default=100)
    args = parser.parse_args()
    if (
        args.iterations < 1
        or args.restart_every < 1
        or args.normalized_favorite < 4
    ):
        parser.error("positive iteration and restart limits are required")
    NORMALIZED_FAVORITE = args.normalized_favorite
    result = run(
        args.seed,
        args.iterations,
        args.random_seed,
        args.restart_every,
        args.initial_temperature,
        args.final_temperature,
        args.objective,
        args.universe,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
