#!/usr/bin/env python3
"""Audit the 960-element symmetry break for overlap bottom pattern zero."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .canonicalize_overlap_bottom_profile import AGENT_ORDER, GOOD_ORDER
    from .decide_bottom_pattern_conversion_selector import conversion_closure
    from .decide_common_bottom_pairing_conversion import canonical_partition
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
    from .run_distinct_half_full_cell_cegar import (
        FAVORITE,
        favorite_pair_universe,
        full_hall_cells,
    )
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import audit_threshold_failure
except ImportError:
    import independent
    from anneal import atomic_json
    from canonicalize_overlap_bottom_profile import AGENT_ORDER, GOOD_ORDER
    from decide_bottom_pattern_conversion_selector import conversion_closure
    from decide_common_bottom_pairing_conversion import canonical_partition
    from run_bottom_pair_pattern_selector_cegar import goods_pattern
    from run_distinct_half_full_cell_cegar import (
        FAVORITE,
        favorite_pair_universe,
        full_hall_cells,
    )
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import audit_threshold_failure


SCHEMA = "overlap-pattern-symmetry-audit-v1"
N = 4
M = 9


def symmetry_actions():
    actions = []
    for side_swap in (False, True):
        for first in ((0, 1), (1, 0)):
            for second in ((2, 3), (3, 2)):
                agents = first + second
                if side_swap:
                    agents = second + first
                for free_goods in itertools.permutations(range(4, M)):
                    goods = (0, 1, 2, 3, *free_goods)
                    if side_swap:
                        goods = (0, 1, 3, 2, *free_goods)
                    actions.append((agents, goods))
    if len(actions) != 960 or len(set(actions)) != 960:
        raise AssertionError("overlap symmetry action census changed")
    return tuple(actions)


def transform(values, action):
    agents, goods = action
    return tuple(
        tuple(values[agents[agent]][goods[good]] for good in range(M))
        for agent in range(N)
    )


def normalized(values):
    return tuple(
        tuple(Fraction(value, sum(row)) for value in row) for row in values
    )


def satisfies_symmetry(values):
    rows = normalized(values)
    if rows[0] < rows[1] or rows[2] < rows[3]:
        return False
    columns = tuple(
        tuple(rows[agent][good] for agent in range(N))
        for good in range(4, M)
    )
    if any(left < right for left, right in zip(columns, columns[1:])):
        return False
    agents = (2, 3, 0, 1)
    goods = (0, 1, 3, 2, 4, 5, 6, 7, 8)
    return sum(rows, ()) >= sum(transform(rows, (agents, goods)), ())


def canonicalize(values, actions):
    return max(
        ((transform(values, action), action) for action in actions),
        key=lambda entry: sum(normalized(entry[0]), ()),
    )


def map_partition(partition, goods):
    return canonical_partition(
        *(tuple(goods[good] for good in bundle) for bundle in partition)
    )


def audit_action_invariance(actions, pattern, conversion_family):
    family = set(conversion_family)
    for agents, goods in actions:
        for new_agent, lows in enumerate(pattern):
            mapped_lows = tuple(sorted(goods[good] for good in lows))
            if mapped_lows != pattern[agents[new_agent]]:
                raise AssertionError("symmetry action changed the bottom pattern")
        mapped_family = {
            map_partition(partition, goods) for partition in conversion_family
        }
        if mapped_family != family:
            raise AssertionError("symmetry action changed the conversion closure")


def conversion_orbits(actions, conversion_family):
    goods_actions = tuple(sorted({goods for _, goods in actions}))
    if len(goods_actions) != 240:
        raise AssertionError("overlap goods-automorphism census changed")
    remaining = set(conversion_family)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {
            map_partition(representative, goods) for goods in goods_actions
        }
        if not orbit <= set(conversion_family):
            raise AssertionError("conversion orbit left its family")
        remaining.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))
    if tuple(map(len, orbits)) != (15, 60, 30, 60):
        raise AssertionError("overlap conversion-orbit sizes changed")
    return tuple(orbits)


def canonical_pattern_values(raw_values):
    return tuple(
        tuple(
            raw_values[old_agent][old_good] for old_good in GOOD_ORDER
        )
        for old_agent in AGENT_ORDER
    )


def audit_source(path, actions, pattern, conversion_family, orbit_position):
    payload = json.loads(path.read_text())
    raw_values = tuple(tuple(row) for row in payload["values"])
    pattern_values = canonical_pattern_values(raw_values)
    canonical_values, action = canonicalize(pattern_values, actions)
    if not satisfies_symmetry(canonical_values):
        raise AssertionError("canonical representative violates symmetry cuts")
    if any(row[FAVORITE] <= max(row[1:]) for row in canonical_values):
        raise AssertionError("strict common favorite changed")
    audit_threshold_failure(canonical_values)
    for agent, lows in enumerate(pattern):
        if max(canonical_values[agent][low] for low in lows) > min(
            canonical_values[agent][good]
            for good in range(1, M)
            if good not in lows
        ):
            raise AssertionError("canonical representative lost bottom order")
    selected_pairs = tuple(dict.fromkeys(pattern))
    cells = full_hall_cells(canonical_values)
    if any(list(lows) in cells for lows in selected_pairs):
        raise AssertionError("canonical representative gained a selected full cell")
    repairs = tuple(
        supported_partitions(
            canonical_values, list(favorite_pair_universe("all"))
        )
    )
    conversion_repairs = tuple(
        partition for partition in repairs if partition in conversion_family
    )
    literal_count = independent.count_complete_efx0(canonical_values)
    if len(repairs) != 3 or len(conversion_repairs) != 3 or literal_count != 180:
        raise AssertionError("canonical representative changed exact EFX counts")
    repair_orbits = [orbit_position[partition] for partition in repairs]
    return {
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "canonical_agent_image_new_to_old": list(action[0]),
        "canonical_good_image_new_to_old": list(action[1]),
        "favorite_pair_repair_count": len(repairs),
        "conversion_repair_count": len(conversion_repairs),
        "conversion_repair_orbits": repair_orbits,
        "literal_complete_efx_count": literal_count,
        "values": [list(row) for row in canonical_values],
    }


def run(sources, output):
    if len(sources) < 2:
        raise ValueError("at least two exact boundary profiles are required")
    pattern = goods_pattern(0)
    selected_pairs = tuple(dict.fromkeys(pattern))
    conversion_family, source_pairing_count = conversion_closure(selected_pairs)
    actions = symmetry_actions()
    audit_action_invariance(actions, pattern, conversion_family)
    orbits = conversion_orbits(actions, conversion_family)
    orbit_position = {
        partition: position
        for position, orbit in enumerate(orbits)
        for partition in orbit
    }
    records = [
        audit_source(
            path,
            actions,
            pattern,
            set(conversion_family),
            orbit_position,
        )
        for path in sources
    ]
    if any(
        record["conversion_repair_orbits"] != [3, 3, 3]
        for record in records
    ):
        raise AssertionError("sharp repairs left conversion orbit three")
    result = {
        "schema": SCHEMA,
        "status": "OVERLAP_PATTERN_SYMMETRY_AUDITED",
        "pattern_index": 0,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "group_size": len(actions),
        "conversion_partition_count": len(conversion_family),
        "conversion_orbit_sizes": list(map(len, orbits)),
        "sharp_profile_repair_orbit": 3,
        "source_pairing_count": source_pairing_count,
        "action_invariance_checked": True,
        "canonical_boundary_profile_count": len(records),
        "profiles": records,
        "claim_boundary": (
            "This deterministically checks the finite relabeling group, its "
            "bottom-pattern and conversion-family invariance, and canonical "
            "representatives of exact positive boundaries. The general WLOG "
            "step is the finite-orbit lexicographic-maximum argument."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(tuple(args.source), args.output), indent=2))


if __name__ == "__main__":
    main()
