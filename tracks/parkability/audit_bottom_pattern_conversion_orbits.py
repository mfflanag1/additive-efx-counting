#!/usr/bin/env python3
"""Audit conversion-family orbits under bottom-pattern automorphisms."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_bottom_pattern_conversion_selector import conversion_closure
    from .decide_common_bottom_pairing_conversion import canonical_partition
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
except ImportError:
    from anneal import atomic_json
    from decide_bottom_pattern_conversion_selector import conversion_closure
    from decide_common_bottom_pairing_conversion import canonical_partition
    from run_bottom_pair_pattern_selector_cegar import goods_pattern


SCHEMA = "bottom-pattern-conversion-orbit-audit-v1"
M = 9
FAVORITE = 0


def automorphisms(pattern):
    target = tuple(sorted(tuple(sorted(edge)) for edge in pattern))
    result = []
    for residual_image in itertools.permutations(range(1, M)):
        image = (FAVORITE, *residual_image)
        mapped = tuple(
            sorted(
                tuple(sorted((image[left], image[right])))
                for left, right in pattern
            )
        )
        if mapped == target:
            result.append(image)
    return tuple(result)


def map_partition(partition, image):
    return canonical_partition(
        *(tuple(image[good] for good in bundle) for bundle in partition)
    )


def partition_orbits(partitions, group):
    remaining = set(partitions)
    result = []
    while remaining:
        representative = min(remaining)
        orbit = {
            map_partition(representative, image) for image in group
        }
        if not orbit <= set(partitions):
            raise AssertionError("conversion family is not orbit closed")
        remaining.difference_update(orbit)
        result.append((representative, tuple(sorted(orbit))))
    return tuple(result)


def shape(partition):
    return "".join(map(str, sorted(map(len, partition), reverse=True)))


def run(pattern_index, output):
    pattern = goods_pattern(pattern_index)
    selected_pairs = tuple(dict.fromkeys(pattern))
    family, source_pairing_count = conversion_closure(selected_pairs)
    group = automorphisms(pattern)
    orbits = partition_orbits(family, group)
    result = {
        "schema": SCHEMA,
        "pattern_index": pattern_index,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "automorphism_count": len(group),
        "source_pairing_count": source_pairing_count,
        "conversion_partition_count": len(family),
        "conversion_partition_shape_census": dict(
            sorted(Counter(map(shape, family)).items())
        ),
        "conversion_orbit_count": len(orbits),
        "conversion_orbits": [
            {
                "representative": [
                    list(bundle) for bundle in representative
                ],
                "size": len(orbit),
            }
            for representative, orbit in orbits
        ],
        "claim_boundary": (
            "This is an exact symmetry census of the conversion family, "
            "not an EFX existence proof."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern-index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.pattern_index, args.output)


if __name__ == "__main__":
    main()
