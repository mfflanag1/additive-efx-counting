#!/usr/bin/env python3
"""Audit remove-one-good releases of observed designated pair traps."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_partial_hall_completion import perfect_matchings
    from .decide_partial_hall_designated_pair_trap import (
        SELECTED_PARTITIONS,
        designated_bundle,
    )
    from .decide_partial_hall_radius_one import candidate_partitions
except ImportError:
    from anneal import atomic_json
    from audit_partial_hall_completion import perfect_matchings
    from decide_partial_hall_designated_pair_trap import (
        SELECTED_PARTITIONS,
        designated_bundle,
    )
    from decide_partial_hall_radius_one import candidate_partitions


BASE = ((6, 7), (1, 2, 3), (0, 4), (5,))


def run(paths: list[Path], output: Path) -> dict:
    moves = list(candidate_partitions(BASE, 8))
    records = []
    totals = Counter()
    for path in paths:
        document = json.loads(path.read_text())
        values = document["values"]
        row_totals = tuple(map(sum, values))
        base_score = sum(
            Fraction(
                sum(values[agent][good] for good in BASE[agent]),
                row_totals[agent],
            )
            for agent in range(4)
        )
        traps = []
        for partition_index in SELECTED_PARTITIONS:
            move = moves[partition_index]
            designated = designated_bundle(move)
            masks = tuple(
                sum(1 << good for good in bundle) for bundle in move["partition"]
            )
            graph, _ = perfect_matchings(values, masks)
            for pair in itertools.combinations(range(4), 2):
                if set(graph[pair[0]]) | set(graph[pair[1]]) != {designated}:
                    continue
                releases = []
                for good in move["partition"][designated]:
                    residual_masks = list(masks)
                    residual_masks[designated] ^= 1 << good
                    if residual_masks[designated] == 0:
                        continue
                    release_graph, matchings = perfect_matchings(
                        values, tuple(residual_masks)
                    )
                    for matching in matchings:
                        utilities = tuple(
                            sum(
                                values[agent][item]
                                for item in range(9)
                                if residual_masks[matching[agent]] & (1 << item)
                            )
                            for agent in range(4)
                        )
                        parked = all(
                            utilities[agent] >= values[agent][good]
                            for agent in range(4)
                        )
                        score = sum(
                            Fraction(utilities[agent], row_totals[agent])
                            for agent in range(4)
                        )
                        releases.append(
                            {
                                "new_floater": good,
                                "matching": list(matching),
                                "utilities": list(utilities),
                                "parked": parked,
                                "potential_gain": {
                                    "numerator": (score - base_score).numerator,
                                    "denominator": (score - base_score).denominator,
                                },
                                "improving": score > base_score,
                            }
                        )
                efx_release = bool(releases)
                parked_release = any(item["parked"] for item in releases)
                improving_release = any(
                    item["parked"] and item["improving"] for item in releases
                )
                totals["trap"] += 1
                totals["efx_release"] += efx_release
                totals["parked_release"] += parked_release
                totals["improving_release"] += improving_release
                traps.append(
                    {
                        "partition_index": partition_index,
                        "floater_host": move["floater_host"],
                        "moved_good": move["moved_good"],
                        "designated_bundle": designated,
                        "deficient_agents": list(pair),
                        "owner_source_exception": set(pair)
                        == {designated, move["move_source"]},
                        "efx_release": efx_release,
                        "parked_release": parked_release,
                        "improving_parked_release": improving_release,
                        "best_release": max(
                            releases,
                            key=lambda item: Fraction(
                                item["potential_gain"]["numerator"],
                                item["potential_gain"]["denominator"],
                            ),
                            default=None,
                        ),
                    }
                )
        records.append(
            {
                "source": str(path),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "trap_count": len(traps),
                "efx_release_count": sum(item["efx_release"] for item in traps),
                "parked_release_count": sum(item["parked_release"] for item in traps),
                "improving_parked_release_count": sum(
                    item["improving_parked_release"] for item in traps
                ),
                "traps": traps,
            }
        )
    artifact = {
        "schema": "partial-hall-designated-trap-release-audit-v1",
        "status": "AUDITED",
        "meaning": (
            "Finite-profile audit of removing one good from the contested "
            "designated bundle, rematching, parking that good, and improving "
            "normalized-utilitarian potential. Absence or coverage is not a theorem."
        ),
        "source_count": len(records),
        "trap_count": totals["trap"],
        "efx_release_count": totals["efx_release"],
        "parked_release_count": totals["parked_release"],
        "improving_parked_release_count": totals["improving_release"],
        "records": records,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
