#!/usr/bin/env python3
"""Extract one hash-addressed valuation profile from the Hall corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


def run(source: Path, output: Path, value_sha256: str) -> dict:
    document = json.loads(source.read_text())
    matches = [
        record for record in document["records"]
        if record["value_sha256"] == value_sha256
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one profile for {value_sha256}, found {len(matches)}")
    record = matches[0]
    artifact = {
        "schema": "partial-hall-corpus-profile-v1",
        "status": "EXTRACTED",
        "meaning": "Hash-addressed exact valuation profile extracted from the Hall corpus.",
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "value_sha256": value_sha256,
        "fixed_state": {"floater": 8, "masks": [192, 14, 17, 32]},
        "values": record["values"],
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--value-sha256", required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output, args.value_sha256), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
