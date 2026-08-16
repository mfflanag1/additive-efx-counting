#!/usr/bin/env python3
"""Expand a variable-packet rooted core into the full two-per-packet cell."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FULL_GOODS = (
    "tr0", "tr1", "br0", "br1", "tq0", "tq1", "bq0", "bq1", "x", "y", "f"
)
PACKET_PREFIXES = ("tr", "br", "tq", "bq")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output path must be new")
    payload = json.loads(args.core.read_text())
    old_goods = payload["goods"]
    rivals = []
    for record in payload["rivals"]:
        old_owner = dict(zip(old_goods, record["owner_by_good"]))
        owner = []
        for good in FULL_GOODS:
            if good in old_owner:
                owner.append(old_owner[good])
                continue
            prefix = next(prefix for prefix in PACKET_PREFIXES if good.startswith(prefix))
            if prefix not in old_owner:
                raise ValueError(("cannot expand good", good, old_goods))
            owner.append(old_owner[prefix])
        rivals.append(owner)
    output = {
        "schema": "alternating-anchored-or-promoted-split-pool-v1",
        "agent_order": payload["agent_order"],
        "promotion_mode": "none",
        "anchor_mode": "root-only",
        "rivals": rivals,
        "seed_provenance": {
            "variable_core": str(args.core),
            "expansion": "each atomic packet good is replaced by its two full-cell children with the same owner",
        },
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"expanded_rival_count": len(rivals), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
