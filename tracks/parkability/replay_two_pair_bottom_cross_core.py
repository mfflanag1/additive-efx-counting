#!/usr/bin/env python3
"""Replay a mined cross-pair partition core in a chosen threshold encoding."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from .anneal import atomic_json
    from .shrink_two_pair_bottom_cross_core import build_base
except ImportError:
    from anneal import atomic_json
    from shrink_two_pair_bottom_cross_core import build_base


SCHEMA = "two-pair-bottom-cross-core-replay-v1"


def run(source_path, result_path, formula_path, threshold_encoding, time_limit):
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    if source.get("core_size") != len(source.get("core_partitions", [])):
        raise ValueError("source does not contain a complete partition core")
    master, _, _, _, orbit_count = build_base(
        source["pattern"],
        source["matching_orbit_index"],
        threshold_encoding,
    )
    core = tuple(
        tuple(tuple(bundle) for bundle in partition)
        for partition in source["core_partitions"]
    )
    for partition in core:
        master.add_partition_obstruction(partition)
    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": (
            "CORE_REPLAY_UNSAT"
            if solved.status == "UNSAT"
            else "CORE_REPLAY_SAT"
            if solved.status == "SAT"
            else "CORE_REPLAY_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "pattern": source["pattern"],
        "matching_orbit_index": source["matching_orbit_index"],
        "matching_orbit_count": orbit_count,
        "partition_family": source["partition_family"],
        "threshold_encoding": threshold_encoding,
        "core_size": len(core),
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "values": [list(row) for row in solved.values] if solved.values else None,
        "smt2_path": str(formula_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "UNSAT proves only the fixed matching-orbit core and requires "
            "independent replay before theorem status."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument(
        "--threshold-encoding",
        choices=("cardinal", "sorting"),
        required=True,
    )
    parser.add_argument("--time-limit", type=float, default=600)
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    print(
        json.dumps(
            run(
                args.source,
                args.result,
                args.formula,
                args.threshold_encoding,
                args.time_limit,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
