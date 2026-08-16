#!/usr/bin/env python3
"""Extract one exact valuation profile from a designated-trap screen."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


def run(source: Path, output: Path, record_index: int) -> dict:
    document = json.loads(source.read_text())
    record = document["records"][record_index]
    if "values" not in record:
        raise ValueError("selected screen record has no valuation model")
    artifact = {
        "schema": "partial-hall-screen-profile-v1",
        "status": "EXTRACTED",
        "meaning": (
            "Exact valuation profile extracted from the selected SAT screen "
            "record for independent cell and model audits."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "record_index": record_index,
        "fixed_state": {"floater": 8, "masks": [192, 14, 17, 32]},
        "screen_cell": {
            key: record[key]
            for key in ("partition_index", "deficient_agents", "designated_bundle")
            if key in record
        },
        "values": record["values"],
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--record-index", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output, args.record_index), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
