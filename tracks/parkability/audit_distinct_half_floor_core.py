#!/usr/bin/env python3
"""Replay the minimized 22-partition distinct-half owner-floor core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import (
        N,
        add_branch_constraints,
        add_floor_state_obstruction,
        favorite_pair_balanced_universe,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import (
        N,
        add_branch_constraints,
        add_floor_state_obstruction,
        favorite_pair_balanced_universe,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "distinct-half-floor-core-replay-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(core_path: Path, theorem_audit_path: Path) -> dict:
    source = json.loads(core_path.read_text())
    theorem = json.loads(theorem_audit_path.read_text())
    if (
        source.get("schema") != "distinct-half-floor-assumption-core-v1"
        or source.get("status") != "UNSAT_CORE"
        or source.get("universe_size") != 840
        or source.get("core_size") != 22
        or source.get("core_minimization") is not True
        or theorem.get("status")
        != "DISTINCT_HALF_FLOOR_DUAL_ENCODING_AUDIT_PASSED"
    ):
        raise ValueError("core or theorem metadata changed")
    partitions = tuple(
        tuple(tuple(bundle) for bundle in partition)
        for partition in source["partitions"]
    )
    universe = set(favorite_pair_balanced_universe())
    if len(partitions) != len(set(partitions)) or not set(partitions) <= universe:
        raise ValueError("core contains invalid or duplicate partitions")
    master = ParkabilityLRAMaster(N, 9)
    add_branch_constraints(master)
    for partition in partitions:
        add_floor_state_obstruction(master, partition)
    solved = master.solve(time_limit_s=60)
    if solved.status != "UNSAT":
        raise AssertionError("22-partition replay is no longer UNSAT")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_FLOOR_CORE_REPLAY_PASSED",
        "core": str(core_path.resolve()),
        "core_sha256": sha256(core_path),
        "theorem_audit": str(theorem_audit_path.resolve()),
        "theorem_audit_sha256": sha256(theorem_audit_path),
        "universe_size": len(universe),
        "core_size": len(partitions),
        "solver_status": solved.raw_status,
        "interpretation": (
            "The frozen 22 favorite-pair partitions alone reproduce the "
            "matching-clause QF_LRA contradiction under the exact branch "
            "constraints. This is a proof-mining core, not a human proof."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--theorem-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.core, args.theorem_audit)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
