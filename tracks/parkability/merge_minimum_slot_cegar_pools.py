#!/usr/bin/env python3
"""Merge logically portable cut pools from minimum-slot CEGAR sessions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "minimum-slot-orbit-global-threshold-cegar-v1"


def unique(records, key):
    result = []
    seen = set()
    for record in records:
        record_key = key(record)
        if record_key in seen:
            continue
        seen.add(record_key)
        result.append(record)
    return result


def run(sources, values_source, output):
    documents = [json.loads(source.read_text()) for source in sources]
    if any(document.get("schema") != SCHEMA for document in documents):
        raise ValueError("all sources must be minimum-slot CEGAR sessions")
    values_document = json.loads(values_source.read_text())
    values = values_document.get("values", values_document)
    global_cuts = unique(
        [record for document in documents for record in document.get("global_cuts", ())],
        lambda record: (int(record["floater"]), tuple(int(x) for x in record["masks"])),
    )
    completion_cuts = unique(
        [
            record
            for document in documents
            for record in document.get("completion_cuts", ())
        ],
        lambda record: (
            tuple(int(x) for x in record["assignment"]),
            int(record["host"]),
            tuple(int(x) for x in record["permutation"]),
        ),
    )
    orbit_hall_cuts = unique(
        [
            record
            for document in documents
            for record in document.get("orbit_hall_cuts", ())
        ],
        lambda record: tuple(int(x) for x in record["assignment"]),
    )
    result = {
        "schema": SCHEMA,
        "status": "MERGED_CUT_POOL",
        "meaning": (
            "Union of global-maximality and all-blocked-orbit consequences from "
            "multiple exact CEGAR sessions. The cuts are logically portable across "
            "edge subcells with the same canonical base hypotheses."
        ),
        "claim_boundary": (
            "This artifact is a solver seed, not an UNSAT or EFX theorem verdict."
        ),
        "sources": [
            {
                "path": str(source),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
            for source in sources
        ],
        "values_source": str(values_source),
        "values_source_sha256": hashlib.sha256(values_source.read_bytes()).hexdigest(),
        "values": values,
        "total_iterations": sum(
            int(document.get("total_iterations", 0)) for document in documents
        ),
        "global_cut_count": len(global_cuts),
        "completion_cut_count": len(completion_cuts),
        "orbit_hall_cut_count": len(orbit_hall_cuts),
        "global_cuts": global_cuts,
        "completion_cuts": completion_cuts,
        "orbit_hall_cuts": orbit_hall_cuts,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--values-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.values_source, args.output)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "schema",
                    "status",
                    "global_cut_count",
                    "completion_cut_count",
                    "orbit_hall_cut_count",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
