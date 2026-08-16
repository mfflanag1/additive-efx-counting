#!/usr/bin/env python3
"""Record the transfer graphs of the exact radius-two-through-five ladder."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


BASE_MASKS = (192, 14, 17, 32)
BASE_FLOATER = 8


def owners(masks, floater):
    result = {good: None for good in range(9)}
    for owner, mask in enumerate(masks):
        for good in range(9):
            if mask & (1 << good):
                result[good] = owner
    result[floater] = None
    return result


def run(paths: list[Path], output: Path) -> dict:
    base_owners = owners(BASE_MASKS, BASE_FLOATER)
    records = []
    for path in paths:
        document = json.loads(path.read_text())
        rival = document["nearest_normalized_utilitarian_improver"]
        rival_owners = owners(rival["masks"], rival["floater"])
        transfers = [
            {
                "good": good,
                "source": base_owners[good],
                "destination": rival_owners[good],
            }
            for good in range(9)
            if base_owners[good] != rival_owners[good]
        ]
        if len(transfers) != rival["owner_distance"]:
            raise AssertionError("owner distance does not equal transfer count")
        records.append(
            {
                "source": str(path),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "owner_distance": rival["owner_distance"],
                "new_floater": rival["floater"],
                "rival_masks": rival["masks"],
                "transfers": transfers,
            }
        )
    artifact = {
        "schema": "partial-hall-improver-transfer-ladder-v1",
        "status": "AUDITED",
        "meaning": (
            "Exact transfer graphs of the nearest normalized-utilitarian "
            "improvers in the certified radius-two-through-five obstruction "
            "ladder. These four profiles are structural evidence, not a cover."
        ),
        "base_masks": list(BASE_MASKS),
        "base_floater": BASE_FLOATER,
        "record_count": len(records),
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
