#!/usr/bin/env python3
"""Classify a bottom-pattern conversion core by exact symmetry orbit."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_bottom_pattern_conversion_orbits import (
        automorphisms,
        partition_orbits,
    )
    from .decide_bottom_pattern_conversion_selector import conversion_closure
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
except ImportError:
    from anneal import atomic_json
    from audit_bottom_pattern_conversion_orbits import (
        automorphisms,
        partition_orbits,
    )
    from decide_bottom_pattern_conversion_selector import conversion_closure
    from run_bottom_pair_pattern_selector_cegar import goods_pattern


SCHEMA = "bottom-pattern-conversion-core-analysis-v1"
FAVORITE = 0


def decode(raw):
    return tuple(tuple(bundle) for bundle in raw)


def run(source, output):
    payload = json.loads(source.read_text())
    if payload.get("schema") != "bottom-pattern-conversion-core-lra-v1":
        raise ValueError("source is not a bottom-pattern conversion core")
    pattern_index = payload["pattern_index"]
    pattern = goods_pattern(pattern_index)
    selected_pairs = tuple(dict.fromkeys(pattern))
    family, _ = conversion_closure(selected_pairs)
    core = tuple(map(decode, payload["core_partitions"]))
    if len(core) != len(set(core)) or not set(core) <= set(family):
        raise AssertionError("invalid conversion core")
    group = automorphisms(pattern)
    orbits = partition_orbits(family, group)
    orbit_by_partition = {
        partition: orbit_index
        for orbit_index, (_, orbit) in enumerate(orbits)
        for partition in orbit
    }
    favorite_partners = []
    for partition in core:
        bundle = next(bundle for bundle in partition if FAVORITE in bundle)
        if len(bundle) != 2:
            raise AssertionError("conversion lost its favorite pair")
        favorite_partners.append(next(good for good in bundle if good != FAVORITE))
    result = {
        "schema": SCHEMA,
        "source": str(source),
        "pattern_index": pattern_index,
        "core_size": len(core),
        "conversion_family_size": len(family),
        "automorphism_count": len(group),
        "conversion_orbit_count": len(orbits),
        "core_count_by_conversion_orbit": dict(
            sorted(Counter(orbit_by_partition[item] for item in core).items())
        ),
        "core_count_by_favorite_partner": dict(
            sorted(Counter(favorite_partners).items())
        ),
        "favorite_partner_goods": sorted(set(favorite_partners)),
        "claim_boundary": (
            "This classifies a sufficient solver core. It does not establish "
            "deletion minimality or replace the independent UNSAT proof."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
