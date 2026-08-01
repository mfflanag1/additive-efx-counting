#!/usr/bin/env python3
"""Census Hall-failure witnesses on the certified cap-6 boundaries."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_distinct_half_full_cell_cegar import full_hall_cells
    from .run_distinct_half_two_core_cegar import perfect_pairings
except ImportError:
    from anneal import atomic_json
    from run_distinct_half_full_cell_cegar import full_hall_cells
    from run_distinct_half_two_core_cegar import perfect_pairings


SCHEMA = "distinct-half-full-cell-hall-witness-census-v2"
SOURCE_SCHEMA = "distinct-half-full-cell-threshold-cnf-minimal-core-v1"
N = 4
M = 9
FAVORITE = 0


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def acceptance_masks(values, lows, matching):
    return tuple(
        sum(
            1 << agent
            for agent, row in enumerate(values)
            if sum(row[good] for good in edge)
            >= row[FAVORITE] + max(row[low] for low in lows)
        )
        for edge in matching
    )


def minimum_witness_size(masks):
    for size in (1, 2, 3):
        for indices in itertools.combinations(range(3), size):
            neighborhood = 0
            for index in indices:
                neighborhood |= masks[index]
            if neighborhood.bit_count() < size:
                return size
    return None


def low_type(lows):
    return "".join("R" if low <= 4 else "U" for low in lows)


def singleton_witness_edges(values, lows):
    residual = tuple(good for good in range(1, M) if good not in lows)
    return tuple(
        edge
        for edge in itertools.combinations(residual, 2)
        if all(
            sum(row[good] for good in edge)
            < row[FAVORITE] + max(row[low] for low in lows)
            for row in values
        )
    )


def minimum_edge_cover(witnesses_by_cell):
    candidates = sorted(set().union(*witnesses_by_cell.values()))
    for size in range(1, len(candidates) + 1):
        for selected in itertools.combinations(candidates, size):
            if all(
                any(edge in witnesses for edge in selected)
                for witnesses in witnesses_by_cell.values()
            ):
                return selected
    raise AssertionError("RR cells unexpectedly lack a singleton witness")


def canonical_second_smallest_map(mapping):
    representatives = range(4)
    conjugates = []
    for permutation in itertools.permutations(representatives):
        transformed = [None] * 4
        for agent, representative in enumerate(mapping):
            transformed[permutation[agent]] = permutation[representative]
        conjugates.append(tuple(transformed))
    return min(conjugates)


def second_smallest_map_orbits(values):
    choices = []
    for row in values:
        representative_values = row[1:5]
        second_smallest = sorted(representative_values)[1]
        choices.append(
            tuple(
                position
                for position, value in enumerate(representative_values)
                if value == second_smallest
            )
        )
    return tuple(
        sorted(
            {
                canonical_second_smallest_map(mapping)
                for mapping in itertools.product(*choices)
            }
        )
    )


def run(source_path, output_path):
    source = json.loads(source_path.read_text())
    if (
        source.get("schema") != SOURCE_SCHEMA
        or source.get("status") != "DELETION_MINIMAL_UNSAT_CORE_VERIFIED"
        or source.get("cap") != 6
        or source.get("core_size") != 21
        or len(source.get("removal_boundaries", ())) != 21
    ):
        raise ValueError("source is not the verified cap-6 minimal core")

    failed_pairing_witness_sizes = Counter()
    cell_minimum_witness_sizes = Counter()
    cell_minimum_by_low_type = Counter()
    failed_pairings_per_cell = []
    rr_edge_type_occurrences = Counter()
    rr_minimum_cover_sizes = Counter()
    rr_profiles_with_common_unrepresented_edge = 0
    common_uu_second_smallest_orbit_profiles = Counter()
    profiles = []
    for boundary in source["removal_boundaries"]:
        values = tuple(tuple(row) for row in boundary["values"])
        if full_hall_cells(values):
            raise AssertionError("deletion boundary has a full Hall cell")
        profile_cell_minima = Counter()
        profile_failed_pairings = []
        for lows in itertools.combinations(range(1, M), 2):
            residual = tuple(good for good in range(1, M) if good not in lows)
            witness_sizes = []
            for matching in perfect_pairings(residual):
                size = minimum_witness_size(
                    acceptance_masks(values, lows, matching)
                )
                if size is not None:
                    witness_sizes.append(size)
                    failed_pairing_witness_sizes[size] += 1
            if not witness_sizes:
                raise AssertionError("boundary unexpectedly has a full cell")
            minimum = min(witness_sizes)
            cell_minimum_witness_sizes[minimum] += 1
            cell_minimum_by_low_type[low_type(lows), minimum] += 1
            profile_cell_minima[minimum] += 1
            profile_failed_pairings.append(len(witness_sizes))
            failed_pairings_per_cell.append(len(witness_sizes))
        rr_witnesses = {
            lows: singleton_witness_edges(values, lows)
            for lows in itertools.combinations(range(1, 5), 2)
        }
        if any(not witnesses for witnesses in rr_witnesses.values()):
            raise AssertionError("cap-6 boundary lost an RR singleton witness")
        for witnesses in rr_witnesses.values():
            rr_edge_type_occurrences.update(low_type(edge) for edge in witnesses)
        minimum_cover = minimum_edge_cover(rr_witnesses)
        rr_minimum_cover_sizes[len(minimum_cover)] += 1
        common_edges = set.intersection(
            *(set(witnesses) for witnesses in rr_witnesses.values())
        )
        common_unrepresented = tuple(
            sorted(edge for edge in common_edges if low_type(edge) == "UU")
        )
        rr_profiles_with_common_unrepresented_edge += bool(common_unrepresented)
        second_smallest_orbits = second_smallest_map_orbits(values)
        if common_unrepresented:
            common_uu_second_smallest_orbit_profiles.update(
                second_smallest_orbits
            )
        profiles.append(
            {
                "removed_position": boundary["removed_position"],
                "cell_minimum_witness_size_counts": {
                    str(size): profile_cell_minima[size]
                    for size in sorted(profile_cell_minima)
                },
                "failed_pairings_per_cell_minimum": min(
                    profile_failed_pairings
                ),
                "failed_pairings_per_cell_maximum": max(
                    profile_failed_pairings
                ),
                "failed_pairing_count": sum(profile_failed_pairings),
                "rr_singleton_witness_edge_count_by_type": {
                    kind: sum(
                        low_type(edge) == kind
                        for witnesses in rr_witnesses.values()
                        for edge in witnesses
                    )
                    for kind in ("RR", "RU", "UU")
                },
                "rr_cells_with_witness_type": {
                    kind: sum(
                        any(low_type(edge) == kind for edge in witnesses)
                        for witnesses in rr_witnesses.values()
                    )
                    for kind in ("RR", "RU", "UU")
                },
                "minimum_rr_cell_witness_edge_cover_size": len(minimum_cover),
                "minimum_rr_cell_witness_edge_cover_example": [
                    list(edge) for edge in minimum_cover
                ],
                "common_unrepresented_witness_edges": [
                    list(edge) for edge in common_unrepresented
                ],
                "second_smallest_representative_map_orbits": [
                    [representative + 1 for representative in mapping]
                    for mapping in second_smallest_orbits
                ],
            }
        )

    payload = {
        "schema": SCHEMA,
        "meaning": (
            "Exact descriptive census of Hall failures in the 21 cap-6 "
            "deletion boundaries; observed frequencies are not cap-free theorems."
        ),
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "profile_count": len(profiles),
        "low_pair_cell_count": len(profiles) * 28,
        "failed_pairing_count": sum(failed_pairing_witness_sizes.values()),
        "failed_pairing_minimum_witness_size_counts": {
            str(size): failed_pairing_witness_sizes[size]
            for size in sorted(failed_pairing_witness_sizes)
        },
        "cell_minimum_witness_size_counts": {
            str(size): cell_minimum_witness_sizes[size]
            for size in sorted(cell_minimum_witness_sizes)
        },
        "cell_minimum_witness_size_by_low_type": {
            low_kind: {
                str(size): cell_minimum_by_low_type[low_kind, size]
                for size in (1, 2, 3)
                if cell_minimum_by_low_type[low_kind, size]
            }
            for low_kind in ("RR", "RU", "UU")
        },
        "profiles_with_only_singleton_cell_witnesses": sum(
            profile["cell_minimum_witness_size_counts"] == {"1": 28}
            for profile in profiles
        ),
        "rr_singleton_structure": {
            "witness_edge_occurrences_by_type": {
                kind: rr_edge_type_occurrences[kind]
                for kind in ("RR", "RU", "UU")
            },
            "minimum_cell_cover_size_histogram": {
                str(size): count
                for size, count in sorted(rr_minimum_cover_sizes.items())
            },
            "profiles_with_one_unrepresented_edge_witnessing_all_six_cells": (
                rr_profiles_with_common_unrepresented_edge
            ),
            "second_smallest_representative_map_orbit_count": len(
                {
                    canonical_second_smallest_map(mapping)
                    for mapping in itertools.product(range(4), repeat=4)
                }
            ),
            "common_uu_unobserved_second_smallest_orbits": [
                [representative + 1 for representative in mapping]
                for mapping in sorted(
                    {
                        canonical_second_smallest_map(mapping)
                        for mapping in itertools.product(range(4), repeat=4)
                    }
                    - set(common_uu_second_smallest_orbit_profiles)
                )
            ],
            "common_uu_profile_second_smallest_orbits": [
                {
                    "representative_map": [
                        representative + 1 for representative in mapping
                    ],
                    "profile_count": count,
                }
                for mapping, count in sorted(
                    common_uu_second_smallest_orbit_profiles.items()
                )
            ],
            "meaning": (
                "Descriptive compression of the singleton witnesses in the "
                "six representative-pair cells; it is not a cap-free lemma."
            ),
        },
        "failed_pairings_per_cell": {
            "minimum": min(failed_pairings_per_cell),
            "maximum": max(failed_pairings_per_cell),
            "mean": sum(failed_pairings_per_cell) / len(failed_pairings_per_cell),
        },
        "profiles": profiles,
        "analytic_target": {
            "name": "singleton Hall-cell selector",
            "statement": (
                "In the cap-free hard branch, if every residual low pair "
                "admits a disjoint pair rejected by all four agents at the "
                "favorite-triple threshold, then an eight-orbit favorite-pair "
                "partition supports EFX."
            ),
            "status": "candidate pending exact-real decision",
            "residual_case": (
                "At least one low-pair cell has no zero-neighbor edge, so its "
                "Hall failure needs a two- or three-edge witness."
            ),
        },
    }
    atomic_json(output_path, payload)
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = run(args.source, args.output)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
