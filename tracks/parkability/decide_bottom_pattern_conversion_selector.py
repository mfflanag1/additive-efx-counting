#!/usr/bin/env python3
"""Decide the full local-conversion closure for one bottom-pair pattern."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .decide_common_bottom_pairing_conversion import canonical_partition
    from .decide_two_pair_bottom_cross_conversion import add_bottom_orders
    from .lra_master import ParkabilityLRAMaster, lex_ge
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
    from .run_distinct_half_full_cell_cegar import (
        add_no_full_hall_cell,
        favorite_pair_universe,
        full_hall_cells,
    )
    from .run_distinct_half_two_core_cegar import perfect_pairings
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )
except ImportError:
    import independent
    from anneal import atomic_json
    from decide_common_bottom_pairing_conversion import canonical_partition
    from decide_two_pair_bottom_cross_conversion import add_bottom_orders
    from lra_master import ParkabilityLRAMaster, lex_ge
    from run_bottom_pair_pattern_selector_cegar import goods_pattern
    from run_distinct_half_full_cell_cegar import (
        add_no_full_hall_cell,
        favorite_pair_universe,
        full_hall_cells,
    )
    from run_distinct_half_two_core_cegar import perfect_pairings
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )


SCHEMA = "bottom-pattern-conversion-selector-lra-v1"
N = 4
M = 9
FAVORITE = 0


def compose_symmetry_action(left, right):
    return (
        tuple(left[0][right[0][agent]] for agent in range(N)),
        tuple(left[1][right[1][good]] for good in range(M)),
    )


def generated_symmetry_group(generators):
    identity = (tuple(range(N)), tuple(range(M)))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            image = compose_symmetry_action(current, generator)
            if image not in group:
                group.add(image)
                frontier.append(image)
    return tuple(sorted(group))


def all_distinct_pattern_symmetry_actions(pattern):
    if len(set(pattern)) != N:
        raise ValueError("all-distinct symmetry requires four distinct pairs")
    pair_to_agent = {pair: agent for agent, pair in enumerate(pattern)}
    actions = []
    for residual_image in itertools.permutations(range(1, M)):
        goods = (FAVORITE, *residual_image)
        mapped_pairs = tuple(
            tuple(sorted(goods[good] for good in pair))
            for pair in pattern
        )
        if all(pair in pair_to_agent for pair in mapped_pairs):
            agents = tuple(pair_to_agent[pair] for pair in mapped_pairs)
            actions.append((agents, goods))
    if len(actions) != len({action for action in actions}):
        raise AssertionError("all-distinct symmetry actions are not unique")
    return tuple(sorted(actions))


def symmetry_generators(actions):
    generators = []
    group = generated_symmetry_group(generators)
    for action in actions:
        if action not in group:
            generators.append(action)
            group = generated_symmetry_group(generators)
    if set(group) != set(actions):
        raise AssertionError("symmetry generators do not close to the full group")
    return tuple(generators)


def add_all_distinct_pattern_symmetry(master, pattern_index):
    """Break the exact relabeling group of one all-distinct pattern."""
    pattern = goods_pattern(pattern_index)
    actions = all_distinct_pattern_symmetry_actions(pattern)
    generators = symmetry_generators(actions)
    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    for agents, goods in generators:
        transformed = [
            master.values[agents[agent]][goods[good]]
            for agent in range(N)
            for good in range(M)
        ]
        master.solver.add(lex_ge(original, transformed))
    return {
        "group_size": len(actions),
        "goods_automorphism_count": len({goods for _, goods in actions}),
        "generator_count": len(generators),
        "generator_agent_images": [list(agents) for agents, _ in generators],
        "generator_good_images": [list(goods) for _, goods in generators],
    }


def add_overlap_pattern_symmetry(master):
    """Break the row/good symmetries of canonical overlap pattern zero."""
    for upper, lower in ((0, 1), (2, 3)):
        master.solver.add(
            lex_ge(master.values[upper], master.values[lower])
        )
    for left, right in zip(range(4, 8), range(5, 9)):
        master.solver.add(
            lex_ge(
                [master.values[agent][left] for agent in range(N)],
                [master.values[agent][right] for agent in range(N)],
            )
        )

    agent_image = (2, 3, 0, 1)
    good_image = (0, 1, 3, 2, 4, 5, 6, 7, 8)
    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    side_swapped = [
        master.values[agent_image[agent]][good_image[good]]
        for agent in range(N)
        for good in range(M)
    ]
    master.solver.add(lex_ge(original, side_swapped))
    return {
        "within_pair_agent_orders": [[0, 1], [2, 3]],
        "free_good_order": [4, 5, 6, 7, 8],
        "side_swap_agent_image": list(agent_image),
        "side_swap_good_image": list(good_image),
        "group_size": 960,
    }


def add_triangle_repeated_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern two."""
    master.solver.add(lex_ge(master.values[0], master.values[1]))
    for left, right in zip(range(4, 8), range(5, 9)):
        master.solver.add(
            lex_ge(
                [master.values[agent][left] for agent in range(N)],
                [master.values[agent][right] for agent in range(N)],
            )
        )

    agent_image = (0, 1, 3, 2)
    good_image = (0, 2, 1, 3, 4, 5, 6, 7, 8)
    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    reflected = [
        master.values[agent_image[agent]][good_image[good]]
        for agent in range(N)
        for good in range(M)
    ]
    master.solver.add(lex_ge(original, reflected))
    return {
        "repeated_pair_agent_order": [0, 1],
        "free_good_order": [4, 5, 6, 7, 8],
        "reflection_agent_image": list(agent_image),
        "reflection_good_image": list(good_image),
        "group_size": 480,
    }


def add_star_repeated_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern one."""
    master.solver.add(lex_ge(master.values[0], master.values[1]))
    for left, right in zip(range(5, 8), range(6, 9)):
        master.solver.add(
            lex_ge(
                [master.values[agent][left] for agent in range(N)],
                [master.values[agent][right] for agent in range(N)],
            )
        )

    agent_image = (0, 1, 3, 2)
    good_image = (0, 1, 2, 4, 3, 5, 6, 7, 8)
    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    reflected = [
        master.values[agent_image[agent]][good_image[good]]
        for agent in range(N)
        for good in range(M)
    ]
    master.solver.add(lex_ge(original, reflected))
    return {
        "repeated_pair_agent_order": [0, 1],
        "free_good_order": [5, 6, 7, 8],
        "reflection_agent_image": list(agent_image),
        "reflection_good_image": list(good_image),
        "group_size": 96,
    }


def add_path_repeated_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern three."""
    master.solver.add(lex_ge(master.values[0], master.values[1]))
    for left, right in zip(range(5, 8), range(6, 9)):
        master.solver.add(
            lex_ge(
                [master.values[agent][left] for agent in range(N)],
                [master.values[agent][right] for agent in range(N)],
            )
        )

    agent_image = (0, 1, 3, 2)
    good_image = (0, 2, 1, 4, 3, 5, 6, 7, 8)
    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    reflected = [
        master.values[agent_image[agent]][good_image[good]]
        for agent in range(N)
        for good in range(M)
    ]
    master.solver.add(lex_ge(original, reflected))
    return {
        "repeated_pair_agent_order": [0, 1],
        "free_good_order": [5, 6, 7, 8],
        "reflection_agent_image": list(agent_image),
        "reflection_good_image": list(good_image),
        "group_size": 96,
    }


def add_end_repeated_path_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern four."""
    master.solver.add(lex_ge(master.values[0], master.values[1]))
    for left, right in zip(range(5, 8), range(6, 9)):
        master.solver.add(
            lex_ge(
                [master.values[agent][left] for agent in range(N)],
                [master.values[agent][right] for agent in range(N)],
            )
        )
    return {
        "repeated_pair_agent_order": [0, 1],
        "free_good_order": [5, 6, 7, 8],
        "group_size": 48,
    }


def add_detached_edge_repeated_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern five."""
    master.solver.add(lex_ge(master.values[0], master.values[1]))
    for left, right in zip(range(6, 8), range(7, 9)):
        master.solver.add(
            lex_ge(
                [master.values[agent][left] for agent in range(N)],
                [master.values[agent][right] for agent in range(N)],
            )
        )

    good_image = (0, 1, 2, 3, 5, 4, 6, 7, 8)
    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    endpoint_swapped = [
        master.values[agent][good_image[good]]
        for agent in range(N)
        for good in range(M)
    ]
    master.solver.add(lex_ge(original, endpoint_swapped))
    return {
        "repeated_pair_agent_order": [0, 1],
        "free_good_order": [6, 7, 8],
        "endpoint_swap_good_image": list(good_image),
        "group_size": 24,
    }


def add_disconnected_fork_repeated_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern seven."""
    master.solver.add(lex_ge(master.values[0], master.values[1]))
    for left, right in zip(range(6, 8), range(7, 9)):
        master.solver.add(
            lex_ge(
                [master.values[agent][left] for agent in range(N)],
                [master.values[agent][right] for agent in range(N)],
            )
        )

    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    repeated_endpoint_image = (0, 2, 1, 3, 4, 5, 6, 7, 8)
    repeated_endpoint_swapped = [
        master.values[agent][repeated_endpoint_image[good]]
        for agent in range(N)
        for good in range(M)
    ]
    master.solver.add(lex_ge(original, repeated_endpoint_swapped))

    agent_image = (0, 1, 3, 2)
    arm_good_image = (0, 1, 2, 3, 5, 4, 6, 7, 8)
    arm_swapped = [
        master.values[agent_image[agent]][arm_good_image[good]]
        for agent in range(N)
        for good in range(M)
    ]
    master.solver.add(lex_ge(original, arm_swapped))
    return {
        "repeated_pair_agent_order": [0, 1],
        "free_good_order": [6, 7, 8],
        "repeated_endpoint_swap_good_image": list(repeated_endpoint_image),
        "arm_swap_agent_image": list(agent_image),
        "arm_swap_good_image": list(arm_good_image),
        "group_size": 48,
    }


def add_three_disconnected_edges_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern eight."""
    master.solver.add(lex_ge(master.values[0], master.values[1]))
    master.solver.add(
        lex_ge(
            [master.values[agent][7] for agent in range(N)],
            [master.values[agent][8] for agent in range(N)],
        )
    )

    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    endpoint_images = (
        (0, 2, 1, 3, 4, 5, 6, 7, 8),
        (0, 1, 2, 4, 3, 5, 6, 7, 8),
        (0, 1, 2, 3, 4, 6, 5, 7, 8),
    )
    for good_image in endpoint_images:
        swapped = [
            master.values[agent][good_image[good]]
            for agent in range(N)
            for good in range(M)
        ]
        master.solver.add(lex_ge(original, swapped))

    agent_image = (0, 1, 3, 2)
    component_good_image = (0, 1, 2, 5, 6, 3, 4, 7, 8)
    component_swapped = [
        master.values[agent_image[agent]][component_good_image[good]]
        for agent in range(N)
        for good in range(M)
    ]
    master.solver.add(lex_ge(original, component_swapped))
    return {
        "repeated_pair_agent_order": [0, 1],
        "free_good_order": [7, 8],
        "endpoint_swap_good_images": [list(image) for image in endpoint_images],
        "component_swap_agent_image": list(agent_image),
        "component_swap_good_image": list(component_good_image),
        "group_size": 64,
    }


def add_four_disconnected_edges_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern nineteen."""
    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    endpoint_images = []
    for left in (1, 3, 5, 7):
        good_image = list(range(M))
        good_image[left], good_image[left + 1] = (
            good_image[left + 1],
            good_image[left],
        )
        endpoint_images.append(tuple(good_image))
        swapped = [
            master.values[agent][good_image[good]]
            for agent in range(N)
            for good in range(M)
        ]
        master.solver.add(lex_ge(original, swapped))

    component_agent_images = []
    component_good_images = []
    for left_agent in range(N - 1):
        right_agent = left_agent + 1
        agent_image = list(range(N))
        agent_image[left_agent], agent_image[right_agent] = (
            agent_image[right_agent],
            agent_image[left_agent],
        )
        left_goods = (2 * left_agent + 1, 2 * left_agent + 2)
        right_goods = (2 * right_agent + 1, 2 * right_agent + 2)
        good_image = list(range(M))
        for left, right in zip(left_goods, right_goods):
            good_image[left], good_image[right] = (
                good_image[right],
                good_image[left],
            )
        component_agent_images.append(tuple(agent_image))
        component_good_images.append(tuple(good_image))
        swapped = [
            master.values[agent_image[agent]][good_image[good]]
            for agent in range(N)
            for good in range(M)
        ]
        master.solver.add(lex_ge(original, swapped))
    return {
        "endpoint_swap_good_images": [list(image) for image in endpoint_images],
        "component_swap_agent_images": [
            list(image) for image in component_agent_images
        ],
        "component_swap_good_images": [
            list(image) for image in component_good_images
        ],
        "group_size": 384,
    }


def add_four_cycle_pattern_symmetry(master):
    """Break the symmetries of canonical bottom pattern fourteen."""
    for left, right in zip(range(5, 8), range(6, 9)):
        master.solver.add(
            lex_ge(
                [master.values[agent][left] for agent in range(N)],
                [master.values[agent][right] for agent in range(N)],
            )
        )

    original = [
        master.values[agent][good]
        for agent in range(N)
        for good in range(M)
    ]
    agent_images = (
        (1, 3, 0, 2),
        (2, 3, 0, 1),
    )
    good_images = (
        (0, 3, 1, 4, 2, 5, 6, 7, 8),
        (0, 4, 2, 3, 1, 5, 6, 7, 8),
    )
    for agent_image, good_image in zip(agent_images, good_images):
        transformed = [
            master.values[agent_image[agent]][good_image[good]]
            for agent in range(N)
            for good in range(M)
        ]
        master.solver.add(lex_ge(original, transformed))
    return {
        "free_good_order": [5, 6, 7, 8],
        "dihedral_agent_images": [list(image) for image in agent_images],
        "dihedral_good_images": [list(image) for image in good_images],
        "group_size": 192,
    }


def add_pattern_symmetry(master, pattern_index, symmetry_breaking):
    """Add one supported pattern symmetry and return its audit metadata."""
    pattern = goods_pattern(pattern_index)
    dispatch = {
        "overlap_canonical": (0, add_overlap_pattern_symmetry),
        "triangle_repeated_canonical": (
            2,
            add_triangle_repeated_pattern_symmetry,
        ),
        "star_repeated_canonical": (1, add_star_repeated_pattern_symmetry),
        "path_repeated_canonical": (3, add_path_repeated_pattern_symmetry),
        "end_repeated_path_canonical": (
            4,
            add_end_repeated_path_pattern_symmetry,
        ),
        "detached_edge_repeated_canonical": (
            5,
            add_detached_edge_repeated_pattern_symmetry,
        ),
        "disconnected_fork_repeated_canonical": (
            7,
            add_disconnected_fork_repeated_pattern_symmetry,
        ),
        "three_disconnected_edges_canonical": (
            8,
            add_three_disconnected_edges_pattern_symmetry,
        ),
        "four_disconnected_edges_canonical": (
            19,
            add_four_disconnected_edges_pattern_symmetry,
        ),
        "four_cycle_canonical": (14, add_four_cycle_pattern_symmetry),
    }
    if symmetry_breaking == "none":
        return None
    if symmetry_breaking == "all_distinct_canonical":
        if len(set(pattern)) != N:
            raise ValueError(
                "all-distinct canonical symmetry requires four distinct pairs"
            )
        return add_all_distinct_pattern_symmetry(master, pattern_index)
    if symmetry_breaking not in dispatch:
        raise ValueError("unknown symmetry breaking")
    required_index, add_symmetry = dispatch[symmetry_breaking]
    if pattern_index != required_index:
        raise ValueError(
            f"{symmetry_breaking} symmetry requires pattern index "
            f"{required_index}"
        )
    return add_symmetry(master)


def conversions(lows, matching):
    return tuple(
        canonical_partition(
            (FAVORITE, high),
            (*edge, low),
            *(pair for pair in matching if pair != edge),
        )
        for high, low in (lows, tuple(reversed(lows)))
        for edge in matching
    )


def conversion_closure(selected_pairs):
    partitions = set()
    source_count = 0
    for lows in selected_pairs:
        residual = tuple(
            good for good in range(1, M) if good not in lows
        )
        for matching in perfect_pairings(residual):
            source_count += 1
            partitions.update(conversions(lows, matching))
    return tuple(sorted(partitions)), source_count


def pattern_conversion_orbits(pattern, conversion_family):
    target = tuple(sorted(tuple(sorted(edge)) for edge in pattern))
    goods_actions = []
    for residual_image in itertools.permutations(range(1, M)):
        image = (FAVORITE, *residual_image)
        mapped = tuple(
            sorted(
                tuple(sorted((image[left], image[right])))
                for left, right in pattern
            )
        )
        if mapped == target:
            goods_actions.append(image)
    remaining = set(conversion_family)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {
            canonical_partition(
                *(tuple(goods[good] for good in bundle) for bundle in representative)
            )
            for goods in goods_actions
        }
        if not orbit <= set(conversion_family):
            raise AssertionError("conversion orbit left its family")
        remaining.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))
    return tuple(orbits)


def overlap_conversion_orbits(conversion_family):
    orbits = pattern_conversion_orbits(goods_pattern(0), conversion_family)
    if tuple(map(len, orbits)) != (15, 60, 30, 60):
        raise AssertionError("overlap conversion-orbit census changed")
    return orbits


def reconstruct_cegar_pool(payload, conversion_family):
    pool = set()
    prior_add = payload["add_per_iteration"]
    for record in payload.get("trace", []):
        candidate = record["values"]
        survivors = tuple(
            partition
            for partition in supported_partitions(
                candidate, list(conversion_family)
            )
            if partition not in pool
        )
        if len(survivors) != record["conversion_efx_survivors"]:
            raise AssertionError("resume trace survivor count changed")
        pool.update(survivors[:prior_add])
    if len(pool) != payload["pool_size"]:
        raise AssertionError("resume pool reconstruction changed")
    return pool


def run(
    result_path,
    formula_path,
    pattern_index,
    time_limit,
    cegar=False,
    max_iterations=1,
    add_per_iteration=16,
    resume_path=None,
    threshold_encoding="cardinal",
    symmetry_breaking="none",
    conversion_orbit=None,
):
    pattern = goods_pattern(pattern_index)
    selected_pairs = tuple(dict.fromkeys(pattern))
    full_conversion_family, source_pairing_count = conversion_closure(
        selected_pairs
    )
    if conversion_orbit is None:
        conversion_family = full_conversion_family
        conversion_orbit_count = None
    else:
        conversion_orbits = pattern_conversion_orbits(
            pattern, full_conversion_family
        )
        conversion_orbit_count = len(conversion_orbits)
        if conversion_orbit not in range(conversion_orbit_count):
            raise ValueError("conversion orbit is out of range")
        conversion_family = conversion_orbits[conversion_orbit]
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    if threshold_encoding == "cardinal":
        add_universal_threshold_failure_cardinal(master)
    elif threshold_encoding == "sorting":
        add_universal_threshold_failure(master)
    else:
        raise ValueError("unknown threshold encoding")
    for agent, lows in enumerate(pattern):
        add_bottom_orders(master, lows, (agent,))
    symmetry_encoding = add_pattern_symmetry(
        master, pattern_index, symmetry_breaking
    )
    selected_cell_encoding = add_no_full_hall_cell(
        master, low_pairs=selected_pairs
    )
    pool = set() if cegar else set(conversion_family)
    resume_source = None
    if resume_path is not None:
        if not cegar:
            raise ValueError("resume requires CEGAR mode")
        resumed = json.loads(resume_path.read_text())
        if (
            resumed.get("pattern_index") != pattern_index
            or not resumed.get("cegar")
            or resumed.get("conversion_orbit") != conversion_orbit
        ):
            raise ValueError("incompatible conversion-selector resume")
        pool = reconstruct_cegar_pool(resumed, conversion_family)
        resume_source = {
            "path": str(resume_path),
            "sha256": hashlib.sha256(resume_path.read_bytes()).hexdigest(),
            "reconstructed_pool_size": len(pool),
        }
    for partition in pool:
        master.add_partition_obstruction(partition)

    started = time.time()
    status = "ITERATION_LIMIT"
    raw_status = None
    reason_unknown = None
    values = None
    trace = []
    iteration = 0
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit)
        raw_status = solved.raw_status
        if solved.status == "UNSAT":
            status = "UNSAT_CANDIDATE"
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            reason_unknown = solved.reason_unknown
            break
        candidate = solved.values
        audit_threshold_failure(candidate)
        for agent, lows in enumerate(pattern):
            residual = tuple(
                good for good in range(1, M) if good not in lows
            )
            if any(
                candidate[agent][low] > candidate[agent][good]
                for low in lows
                for good in residual
            ):
                raise AssertionError("model lost its selected bottom pair")
        cells = full_hall_cells(candidate)
        if any(list(pair) in cells for pair in selected_pairs):
            raise AssertionError("model gained a selected full Hall cell")
        survivors = tuple(
            partition
            for partition in supported_partitions(
                candidate, list(conversion_family)
            )
            if partition not in pool
        )
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(pool),
                "conversion_efx_survivors": len(survivors),
                "values": [list(row) for row in candidate],
            }
        )
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"survivors={len(survivors)}",
            flush=True,
        )
        if not survivors:
            status = "CONVERSION_SELECTOR_COUNTEREXAMPLE"
            values = candidate
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(partition)
            pool.add(partition)

    favorite_pair_repairs = None
    literal_count = None
    if values is not None:
        if supported_partitions(values, list(conversion_family)):
            raise AssertionError("model gained a conversion repair")
        favorite_pair_repairs = len(
            supported_partitions(
                values, list(favorite_pair_universe("all"))
            )
        )
        literal_count = independent.count_complete_efx0(values)

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": raw_status,
        "reason_unknown": reason_unknown,
        "pattern_index": pattern_index,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "distinct_selected_bottom_pairs": [
            list(pair) for pair in selected_pairs
        ],
        "selected_cell_encoding": selected_cell_encoding,
        "source_pairing_count": source_pairing_count,
        "raw_conversion_count": 6 * source_pairing_count,
        "full_distinct_conversion_partition_count": len(
            full_conversion_family
        ),
        "distinct_conversion_partition_count": len(conversion_family),
        "conversion_orbit": conversion_orbit,
        "conversion_orbit_count": conversion_orbit_count,
        "cegar": cegar,
        "threshold_encoding": threshold_encoding,
        "symmetry_breaking": symmetry_breaking,
        "symmetry_encoding": symmetry_encoding,
        "resume_source": resume_source,
        "seeded_pool_size": (
            len(pool) if not trace else trace[0]["pool_size_before"]
        ),
        "pool_size": len(pool),
        "max_iterations": max_iterations,
        "iterations": iteration,
        "add_per_iteration": add_per_iteration,
        "trace": trace,
        "favorite_pair_partition_count": len(
            favorite_pair_universe("all")
        ),
        "favorite_pair_efx_partition_count": favorite_pair_repairs,
        "literal_complete_efx_count": literal_count,
        "values": [list(row) for row in values] if values else None,
        "elapsed_seconds": time.time() - started,
        "time_limit_seconds_per_solve": time_limit,
        "smt2_path": str(formula_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "UNSAT would prove the selected-cell conclusion for this one "
            "bottom-pair pattern using only its conversion closure, subject "
            "to independent replay. SAT refutes only that conversion-family "
            "selector, not the full favorite-pair selector or EFX."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--pattern-index", type=int, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--cegar", action="store_true")
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--add", type=int, default=16)
    parser.add_argument("--resume", type=Path)
    parser.add_argument(
        "--threshold-encoding",
        choices=("cardinal", "sorting"),
        default="cardinal",
    )
    parser.add_argument(
        "--symmetry-breaking",
        choices=(
            "all_distinct_canonical",
            "detached_edge_repeated_canonical",
            "disconnected_fork_repeated_canonical",
            "end_repeated_path_canonical",
            "four_disconnected_edges_canonical",
            "four_cycle_canonical",
            "none",
            "overlap_canonical",
            "path_repeated_canonical",
            "star_repeated_canonical",
            "three_disconnected_edges_canonical",
            "triangle_repeated_canonical",
        ),
        default="none",
    )
    parser.add_argument("--conversion-orbit", type=int)
    args = parser.parse_args()
    if args.time_limit <= 0 or args.max_iterations < 1 or args.add < 1:
        parser.error("time limit must be positive")
    print(
        json.dumps(
            run(
                args.result,
                args.formula,
                args.pattern_index,
                args.time_limit,
                args.cegar,
                args.max_iterations if args.cegar else 1,
                args.add,
                args.resume,
                args.threshold_encoding,
                args.symmetry_breaking,
                args.conversion_orbit,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
