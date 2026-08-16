#!/usr/bin/env python3
"""Summarize exact frozen-cell Hall core mechanisms."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "partial-hall-frozen-core-census-v1"


def run(sources, output):
    records = []
    for source in sources:
        document = json.loads(source.read_text())
        if document.get("status") != "UNSAT":
            raise ValueError(f"frozen cell is not UNSAT: {source}")
        core = document.get("deletion_irreducible_unsat_core") or document["unsat_core"]
        kinds = Counter(item["kind"] for item in core)
        records.append(
            {
                "source": str(source),
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "seed_path": document["seed_path"],
                "core_size": len(core),
                "constraint_kind_counts": dict(sorted(kinds.items())),
                "maximality_rival_count": kinds["maximality"],
                "uses_hall_edge_literal": bool(
                    kinds["true_edge_comparison"] or kinds["false_edge_witness"]
                ),
            }
        )
    artifact = {
        "schema": SCHEMA,
        "status": "AUDITED",
        "meaning": (
            "This is a census of exact UNSAT comparison cells, not a cover "
            "of all Hall obstructions. maximality_rival_count measures the "
            "number of explicit eligible rivals needed in each core."
        ),
        "cell_count": len(records),
        "maximum_core_size": max(record["core_size"] for record in records),
        "maximum_maximality_rival_count": max(
            record["maximality_rival_count"] for record in records
        ),
        "hall_edge_literal_cell_count": sum(
            record["uses_hall_edge_literal"] for record in records
        ),
        "records": records,
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = run(args.source, args.output)
    print(json.dumps(artifact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
