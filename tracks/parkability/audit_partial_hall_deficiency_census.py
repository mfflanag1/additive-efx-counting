#!/usr/bin/env python3
"""Census minimal Hall-deficiency sizes in blocked radius-one cells."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_partial_hall_completion import hall_witnesses, perfect_matchings
    from .decide_partial_hall_radius_one import candidate_partitions
except ImportError:
    from anneal import atomic_json
    from audit_partial_hall_completion import hall_witnesses, perfect_matchings
    from decide_partial_hall_radius_one import candidate_partitions


BASE = ((6, 7), (1, 2, 3), (0, 4), (5,))
FLOATER = 8


def run(paths: list[Path], output: Path) -> dict:
    records = []
    aggregate = Counter()
    for path in paths:
        document = json.loads(path.read_text())
        values = document["values"]
        base = tuple(
            tuple(good for good in range(9) if mask & (1 << good))
            for mask in document.get("fixed_state", {}).get(
                "masks", (192, 14, 17, 32)
            )
        )
        floater = document.get("fixed_state", {}).get("floater", FLOATER)
        partitions = []
        counts = Counter()
        for index, move in enumerate(candidate_partitions(base, floater)):
            masks = tuple(
                sum(1 << good for good in bundle) for bundle in move["partition"]
            )
            graph, matchings = perfect_matchings(values, masks)
            witnesses = hall_witnesses(graph)
            minimum = min((len(agents) for agents, _ in witnesses), default=None)
            if matchings or minimum is None:
                raise ValueError(f"profile is not radius-one Hall blocked: {path}")
            counts[minimum] += 1
            aggregate[minimum] += 1
            if move["moved_good"] is None:
                partitions.append(
                    {
                        "partition_index": index,
                        "floater_host": move["floater_host"],
                        "minimum_deficient_agent_count": minimum,
                        "minimum_witnesses": [
                            {"agents": list(agents), "neighbors": list(neighbors)}
                            for agents, neighbors in witnesses
                            if len(agents) == minimum
                        ],
                        "graph": [list(row) for row in graph],
                    }
                )
        records.append(
            {
                "source": str(path),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "deficiency_size_counts": {
                    str(size): counts[size] for size in range(1, 5)
                },
                "direct_addition_partitions": partitions,
            }
        )
    artifact = {
        "schema": "partial-hall-deficiency-census-v1",
        "status": "AUDITED",
        "meaning": (
            "Exact census of the least Hall-deficient agent-set size for all "
            "91 blocked radius-one partitions in each stored profile."
        ),
        "source_count": len(records),
        "aggregate_deficiency_size_counts": {
            str(size): aggregate[size] for size in range(1, 5)
        },
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
