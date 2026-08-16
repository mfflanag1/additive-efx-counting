#!/usr/bin/env python3
"""Build a frozen QF_LRA master from a restricted split-packet rival pool."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .run_alternating_anchored_or_promoted_split_cegar import load_pool
    from .run_alternating_split_packet_cegar import concrete_rival_blocker, structural_solver
except ImportError:
    from run_alternating_anchored_or_promoted_split_cegar import load_pool
    from run_alternating_split_packet_cegar import concrete_rival_blocker, structural_solver


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-order", required=True)
    parser.add_argument("--promotion-mode", choices=("none", "selected", "any-desired"), required=True)
    parser.add_argument("--anchor-mode", choices=("root-only", "root-return"), required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.metadata.exists():
        parser.error("output and metadata paths must be new")
    order = tuple(int(field) for field in args.agent_order.split(","))
    rivals = load_pool(args.pool, order, args.promotion_mode, args.anchor_mode)
    solver, values, own = structural_solver()
    solver.add(*(concrete_rival_blocker(values, own, rival, order) for rival in rivals))
    rendered = (solver.sexpr() + "\n(check-sat)\n").encode()
    args.output.write_bytes(rendered)
    metadata = {
        "schema": "alternating-restricted-split-master-v1",
        "agent_order": list(order),
        "promotion_mode": args.promotion_mode,
        "anchor_mode": args.anchor_mode,
        "pool": str(args.pool),
        "pool_sha256": sha256(args.pool.read_bytes()),
        "rival_count": len(rivals),
        "output": str(args.output),
        "output_sha256": sha256(rendered),
    }
    args.metadata.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
