#!/usr/bin/env python3
"""Decide the terminal-to-six-orbit exchange implication."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import (
        canonical_partition,
        feasible_graph,
        matching_rank,
    )
    from .audit_distinct_half_rank_augmentation import build_state_graph
    from .decide_distinct_half_hall_layers import add_branch
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import (
        SIX_ORBIT_SIGNATURES,
        add_no_full_hall_cell,
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import (
        canonical_partition,
        feasible_graph,
        matching_rank,
    )
    from audit_distinct_half_rank_augmentation import build_state_graph
    from decide_distinct_half_hall_layers import add_branch
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import (
        SIX_ORBIT_SIGNATURES,
        add_no_full_hall_cell,
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )


SCHEMA = "distinct-half-terminal-exchange-decision-v1"
N = 4
M = 9
FAVORITE = 0
REPRESENTATIVES = frozenset(range(1, 5))
UNREPRESENTED = frozenset(range(5, 9))
TERMINAL_PARTITIONS = {
    "R": ((0, 1), (2, 3, 4), (5, 6), (7, 8)),
    "U": ((0, 5), (1, 2, 3), (4, 6), (7, 8)),
}
TERMINAL_MATCHING_REPRESENTATIVES = {
    "R": ((0, 1, 2, 3), (1, 0, 2, 3), (2, 0, 1, 3)),
    "U": ((1, 2, 3, 0), (0, 2, 3, 1), (0, 1, 3, 2), (0, 1, 2, 3)),
}


def parse_low_pair(raw):
    try:
        pair = tuple(int(value) for value in raw.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("low pair must have form a,b") from error
    if len(pair) != 2 or not 1 <= pair[0] < pair[1] < M:
        raise argparse.ArgumentTypeError("low pair must satisfy 1 <= a < b < 9")
    return pair


def exchange_neighbors(partition):
    triple = next(bundle for bundle in partition if len(bundle) == 3)
    neighbors = set()
    for representative in triple:
        if representative not in REPRESENTATIVES:
            continue
        for low in UNREPRESENTED.difference(triple):
            bundles = [list(bundle) for bundle in partition]
            triple_index = next(
                index
                for index, bundle in enumerate(bundles)
                if representative in bundle
            )
            low_index = next(
                index for index, bundle in enumerate(bundles) if low in bundle
            )
            bundles[triple_index].remove(representative)
            bundles[triple_index].append(low)
            bundles[low_index].remove(low)
            bundles[low_index].append(representative)
            neighbor = canonical_partition(bundles)
            if favorite_pair_orbit_signature(neighbor) not in SIX_ORBIT_SIGNATURES:
                raise AssertionError("exchange left the six-orbit family")
            neighbors.add(neighbor)
    return tuple(sorted(neighbors))


def matching_efx(master, partition, matching):
    inequalities = []
    for observer, own_bundle in enumerate(matching):
        own = master._sum(observer, partition[own_bundle])
        for target_bundle, target in enumerate(partition):
            if target_bundle == own_bundle:
                continue
            for removed in target:
                remainder = tuple(good for good in target if good != removed)
                inequalities.append(own >= master._sum(observer, remainder))
    return z3.And(*inequalities)


def matching_efx_comparisons(master, partition, matching):
    comparisons = []
    for observer, own_bundle in enumerate(matching):
        own = master._sum(observer, partition[own_bundle])
        for target_bundle, target in enumerate(partition):
            if target_bundle == own_bundle:
                continue
            for removed in target:
                remainder = tuple(good for good in target if good != removed)
                comparisons.append((own, master._sum(observer, remainder)))
    return tuple(comparisons)


def add_terminal_slack_branch(master, partition, matching, branch):
    if branch == "any":
        return
    comparisons = matching_efx_comparisons(master, partition, matching)
    if branch == "strict":
        master.solver.add(*(own > target for own, target in comparisons))
    elif branch == "boundary":
        master.solver.add(
            z3.Or(*(own == target for own, target in comparisons))
        )
    else:
        raise ValueError("unknown terminal slack branch")


def terminal_stabilizer_good_permutations(case, matching):
    """Good relabelings induced by symmetries of a fixed terminal allocation."""
    partition = TERMINAL_PARTITIONS[case]
    permutations = set()
    for agent_permutation in itertools.permutations(range(N)):
        representative_map = {
            agent + 1: agent_permutation[agent] + 1 for agent in range(N)
        }
        for free_permutation in itertools.permutations(UNREPRESENTED):
            good_map = {0: 0, **representative_map}
            good_map.update(zip(sorted(UNREPRESENTED), free_permutation))
            if all(
                tuple(sorted(good_map[good] for good in partition[matching[agent]]))
                == partition[matching[agent_permutation[agent]]]
                for agent in range(N)
            ):
                permutations.add(tuple(good_map[good] for good in range(M)))
    return tuple(sorted(permutations))


def target_partition_orbits(case, matching, target):
    """Partition target orbits under the fixed terminal allocation stabilizer."""
    target_set = set(target_partitions(target, TERMINAL_PARTITIONS[case]))
    universe = set(target_set)
    permutations = terminal_stabilizer_good_permutations(case, matching)
    orbits = []
    while universe:
        representative = min(universe)
        orbit = frozenset(
            canonical_partition(
                [[permutation[good] for good in bundle] for bundle in representative]
            )
            for permutation in permutations
        )
        if not orbit.issubset(target_set):
            raise AssertionError("terminal stabilizer left the target family")
        universe.difference_update(orbit)
        orbits.append(orbit)
    return tuple(orbits)


def require_partition_efx(master, partition, matching=None):
    if matching is not None:
        master.solver.add(matching_efx(master, partition, matching))
        return
    matchings = []
    for matching in itertools.permutations(range(N)):
        matchings.append(matching_efx(master, partition, matching))
    master.solver.add(z3.Or(*matchings))


def supported(values, partition):
    return matching_rank(feasible_graph(values, partition)) == N


def matching_slacks(values, partition, matching):
    return tuple(
        sum(values[observer][good] for good in partition[own_bundle])
        - sum(values[observer][good] for good in target if good != removed)
        for observer, own_bundle in enumerate(matching)
        for target_bundle, target in enumerate(partition)
        if target_bundle != own_bundle
        for removed in target
    )


def target_partitions(target, terminal_partition):
    if target == "local_swap":
        return exchange_neighbors(terminal_partition)
    if target in (
        "radius2",
        "radius2_same_favorite",
        "radius2_new_favorite_partner",
        "radius2_triple_partner",
    ):
        universe, neighbors = build_state_graph()
        index = {partition: position for position, partition in enumerate(universe)}
        start = index[canonical_partition(terminal_partition)]
        reached = {start}
        frontier = {start}
        for _ in range(2):
            frontier = {
                neighbor
                for position in frontier
                for neighbor in neighbors[position]
                if neighbor not in reached
            }
            reached.update(frontier)
        candidates = tuple(
            partition
            for position, partition in enumerate(universe)
            if position in reached
            and position != start
            and favorite_pair_orbit_signature(partition)[1] < 3
        )
        if target == "radius2":
            return candidates
        favorite_bundle = next(
            bundle for bundle in terminal_partition if FAVORITE in bundle
        )
        same_favorite = tuple(
            partition
            for partition in candidates
            if next(bundle for bundle in partition if FAVORITE in bundle)
            == favorite_bundle
        )
        if target == "radius2_same_favorite":
            return same_favorite
        new_partner = tuple(
            partition for partition in candidates if partition not in same_favorite
        )
        if target == "radius2_new_favorite_partner":
            return new_partner
        terminal_triple = next(
            bundle for bundle in terminal_partition if len(bundle) == 3
        )
        return tuple(
            partition
            for partition in new_partner
            if next(
                good
                for bundle in partition
                if FAVORITE in bundle
                for good in bundle
                if good != FAVORITE
            )
            in terminal_triple
        )
    if target == "same_favorite":
        favorite_bundle = next(
            bundle for bundle in terminal_partition if FAVORITE in bundle
        )
        return tuple(
            partition
            for partition in favorite_pair_universe("eight_orbit")
            if next(bundle for bundle in partition if FAVORITE in bundle)
            == favorite_bundle
        )
    return favorite_pair_universe(target)


def run(
    case,
    target,
    matching_orbit,
    result_path,
    smt2_path,
    time_limit,
    integer_cap=None,
    target_pool_path=None,
    require_no_full_cell=True,
    threshold_encoding="cardinal",
    terminal_slack_branch="any",
    forbidden_full_cell_pairs=None,
):
    partition = TERMINAL_PARTITIONS[case]
    matching = (
        None
        if matching_orbit is None
        else TERMINAL_MATCHING_REPRESENTATIVES[case][matching_orbit]
    )
    target_universe = target_partitions(target, partition)
    if target_pool_path is None:
        targets = target_universe
    else:
        payload = json.loads(target_pool_path.read_text())
        if payload.get("case", case) != case or payload.get("target", target) != target:
            raise ValueError("target pool metadata does not match the requested case")
        if payload.get("terminal_matching_orbit", matching_orbit) != matching_orbit:
            raise ValueError("target pool metadata has a different matching orbit")
        targets = tuple(
            canonical_partition(item) for item in payload["core_partitions"]
        )
        if not targets or not set(targets).issubset(target_universe):
            raise ValueError("target pool is not a nonempty target-family subset")
    master = ParkabilityLRAMaster(N, M, integer_upper=integer_cap)
    add_branch(master, None, threshold_encoding=threshold_encoding)
    if require_no_full_cell and forbidden_full_cell_pairs is not None:
        raise ValueError("cannot forbid all and selected full Hall cells together")
    full_cell_encoding = (
        add_no_full_hall_cell(master)
        if require_no_full_cell
        else add_no_full_hall_cell(master, forbidden_full_cell_pairs)
        if forbidden_full_cell_pairs is not None
        else None
    )
    require_partition_efx(master, partition, matching)
    if matching is None and terminal_slack_branch != "any":
        raise ValueError("terminal slack split requires a fixed matching orbit")
    if matching is not None:
        add_terminal_slack_branch(
            master, partition, matching, terminal_slack_branch
        )
    for target_partition in targets:
        master.add_partition_obstruction(target_partition)

    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    values = solved.values
    orbit_histogram = None
    model_full_cells = set()
    if values is not None:
        model_full_cells = {tuple(cell) for cell in full_hall_cells(values)}
        if require_no_full_cell and model_full_cells:
            raise AssertionError("model has a forbidden full Hall cell")
        if forbidden_full_cell_pairs is not None and model_full_cells.intersection(
            forbidden_full_cell_pairs
        ):
            raise AssertionError("model has a selected forbidden full Hall cell")
        if not supported(values, partition):
            raise AssertionError("terminal partition is not EFX")
        if matching is not None:
            terminal_slacks = matching_slacks(values, partition, matching)
            if (
                terminal_slack_branch == "strict"
                and min(terminal_slacks) <= 0
            ) or (
                terminal_slack_branch == "boundary"
                and 0 not in terminal_slacks
            ):
                raise AssertionError("terminal slack branch changed")
        if any(supported(values, target_partition) for target_partition in targets):
            raise AssertionError("a forbidden target partition remains EFX")
        universe = favorite_pair_universe("all")
        orbit_histogram = {
            repr(signature): count
            for signature, count in sorted(
                Counter(
                    favorite_pair_orbit_signature(candidate)
                    for candidate in universe
                    if supported(values, candidate)
                ).items(),
                key=lambda item: repr(item[0]),
            )
        }

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    encoded_targets = json.dumps(
        [[list(bundle) for bundle in item] for item in targets],
        separators=(",", ":"),
    ).encode()
    result = {
        "schema": SCHEMA,
        "status": (
            "TERMINAL_SELECTOR_COUNTEREXAMPLE"
            if solved.status == "SAT"
            else "UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "case": case,
        "target": target,
        "terminal_matching_orbit": matching_orbit,
        "terminal_matching_representative": list(matching) if matching else None,
        "terminal_matching_orbit_count": len(
            TERMINAL_MATCHING_REPRESENTATIVES[case]
        ),
        "terminal_slack_branch": terminal_slack_branch,
        "domain": (
            f"positive integers at most {integer_cap}"
            if integer_cap is not None
            else "strictly positive reals normalized per row"
        ),
        "integer_cap": integer_cap,
        "n": N,
        "m": M,
        "terminal_partition": [list(bundle) for bundle in partition],
        "terminal_signature": list(favorite_pair_orbit_signature(partition)),
        "target_partition_count": len(targets),
        "target_pool_source": (
            str(target_pool_path) if target_pool_path is not None else None
        ),
        "target_pool_source_sha256": (
            hashlib.sha256(target_pool_path.read_bytes()).hexdigest()
            if target_pool_path is not None
            else None
        ),
        "target_partitions_sha256": hashlib.sha256(encoded_targets).hexdigest(),
        "target_partition_sample": [
            [list(bundle) for bundle in target_partition]
            for target_partition in targets[:12]
        ],
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "universal_threshold_encoding": threshold_encoding,
        "full_hall_cell_forbidden": require_no_full_cell,
        "full_hall_cell_forbidden_pairs": (
            [list(pair) for pair in forbidden_full_cell_pairs]
            if forbidden_full_cell_pairs is not None
            else None
        ),
        "full_hall_cells": (
            [list(pair) for pair in sorted(model_full_cells)]
            if values is not None
            else None
        ),
        "full_cell_encoding": full_cell_encoding,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "values": [list(row) for row in values] if values is not None else None,
        "favorite_pair_efx_orbit_histogram": orbit_histogram,
        "smt2_path": str(smt2_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "SAT refutes the selected terminal-to-target implication for this "
            "orbit. UNSAT requires independent replay before theorem status."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(TERMINAL_PARTITIONS), required=True)
    parser.add_argument(
        "--target",
        choices=(
            "local_swap",
            "radius2",
            "radius2_same_favorite",
            "radius2_new_favorite_partner",
            "radius2_triple_partner",
            "same_favorite",
            "six_orbit",
            "eight_orbit",
        ),
        default="local_swap",
    )
    parser.add_argument("--matching-orbit", type=int)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--integer-cap", type=int)
    parser.add_argument("--target-pool", type=Path)
    parser.add_argument("--allow-full-hall-cell", action="store_true")
    parser.add_argument(
        "--only-forbid-full-cell", type=parse_low_pair, action="append"
    )
    parser.add_argument(
        "--threshold-encoding", choices=("cardinal", "sorting"), default="cardinal"
    )
    parser.add_argument(
        "--terminal-slack-branch",
        choices=("any", "strict", "boundary"),
        default="any",
    )
    args = parser.parse_args()
    if args.matching_orbit is not None and not (
        0
        <= args.matching_orbit
        < len(TERMINAL_MATCHING_REPRESENTATIVES[args.case])
    ):
        parser.error("matching orbit is outside the canonical case range")
    if args.integer_cap is not None and args.integer_cap < 1:
        parser.error("integer cap must be positive")
    if args.allow_full_hall_cell and args.only_forbid_full_cell:
        parser.error("cannot combine --allow-full-hall-cell with a selected cell")
    result = run(
        args.case,
        args.target,
        args.matching_orbit,
        args.result,
        args.smt2,
        args.time_limit,
        args.integer_cap,
        args.target_pool,
        not args.allow_full_hall_cell and args.only_forbid_full_cell is None,
        args.threshold_encoding,
        args.terminal_slack_branch,
        tuple(args.only_forbid_full_cell) if args.only_forbid_full_cell else None,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
