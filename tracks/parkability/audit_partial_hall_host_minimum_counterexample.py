#!/usr/bin/env python3
"""Audit nested move families on the host-minimum aggregate realization."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .search_partial_hall_pair_extraction import (
        candidate_partitions,
        classify_candidate_family,
        graph_for_partition,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from search_partial_hall_pair_extraction import (
        candidate_partitions,
        classify_candidate_family,
        graph_for_partition,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_pair(pair):
    if pair is None:
        return None
    masks, graph, agents, neighbors, operation = pair
    return {
        "masks": list(masks),
        "graph": [list(row) for row in graph],
        "agents": list(agents),
        "neighbors": list(neighbors),
        "operation": operation,
    }


def family_record(totals, thresholds, candidates):
    completion = None
    for masks, operation in candidates:
        graph = graph_for_partition(totals, thresholds, masks)
        matching = next(
            (
                permutation
                for permutation in itertools.permutations(range(4))
                if all(permutation[agent] in graph[agent] for agent in range(4))
            ),
            None,
        )
        if matching is not None:
            completion = {
                "masks": list(masks),
                "graph": [list(row) for row in graph],
                "matching": list(matching),
                "operation": operation,
            }
            break
    complete, pair, _ = classify_candidate_family(totals, thresholds, candidates)
    return {
        "candidate_count": len(candidates),
        "completion_exists": complete,
        "completion_witness": completion,
        "pair_witness_exists_if_blocked": not complete and pair is not None,
        "pair_witness": public_pair(pair) if not complete else None,
    }


def run(source: Path, output: Path) -> dict:
    document = json.loads(source.read_text())
    values = core.validate_values(document["values"], expected_n=4, lower=1)
    masks = tuple(document["base_masks"])
    floater = document["floater"]
    totals, thresholds = core._subset_tables(values)
    eligible = all(
        totals[agent][masks[agent]] >= values[agent][floater]
        and all(
            target == agent
            or totals[agent][masks[agent]] >= thresholds[agent][masks[target]]
            for target in range(4)
        )
        for agent in range(4)
    )
    state = {"masks": masks, "floater": floater}
    candidates = candidate_partitions(state, len(values[0]))
    owner_minima = {}
    for owner, mask in enumerate(masks):
        goods = [good for good in range(len(values[0])) if mask & (1 << good)]
        least = min(values[owner][good] for good in goods)
        owner_minima[owner] = {
            good for good in goods if values[owner][good] == least
        }
    owner_minimum = [
        candidate
        for candidate in candidates
        if candidate[1]["moved_good"] is None
        or candidate[1]["moved_good"]
        in owner_minima[candidate[1]["move_source"]]
    ]
    host_minimum = [
        candidate
        for candidate in owner_minimum
        if candidate[1]["moved_good"] is None
        or candidate[1]["move_source"] == candidate[1]["floater_host"]
    ]
    direct = [
        candidate for candidate in candidates if candidate[1]["moved_good"] is None
    ]
    families = {
        "direct": family_record(totals, thresholds, direct),
        "host_owner_minimum": family_record(totals, thresholds, host_minimum),
        "any_source_owner_minimum": family_record(
            totals, thresholds, owner_minimum
        ),
        "unrestricted_radius_one": family_record(totals, thresholds, candidates),
    }
    artifact = {
        "schema": "partial-hall-host-minimum-counterexample-audit-v1",
        "source": str(source),
        "source_sha256": sha256(source),
        "base_is_eligible_one_floater_efx": eligible,
        "families": families,
        "host_minimum_conjecture_refuted": (
            eligible
            and not families["host_owner_minimum"]["completion_exists"]
            and not families["host_owner_minimum"]["pair_witness_exists_if_blocked"]
        ),
        "owner_minimum_conjecture_refuted": (
            eligible
            and not families["any_source_owner_minimum"]["completion_exists"]
            and not families["any_source_owner_minimum"]["pair_witness_exists_if_blocked"]
        ),
        "radius_one_conjecture_refuted": (
            eligible
            and not families["unrestricted_radius_one"]["completion_exists"]
            and not families["unrestricted_radius_one"]["pair_witness_exists_if_blocked"]
        ),
        "claim_boundary": (
            "A refutation flag concerns only the named pair-extraction move "
            "family, not complete EFX existence."
        ),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2))


if __name__ == "__main__":
    main()
