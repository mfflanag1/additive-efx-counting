#!/usr/bin/env python3
"""Test whether a guarded conversion core survives without symmetry cuts."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from .anneal import atomic_json
    from .extract_bottom_pattern_conversion_core import build_base
except ImportError:
    from anneal import atomic_json
    from extract_bottom_pattern_conversion_core import build_base


SCHEMA = "bottom-pattern-core-without-symmetry-boundary-v1"


def decode(raw):
    return tuple(tuple(bundle) for bundle in raw)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source, output, time_limit):
    payload = json.loads(source.read_text())
    if not (
        payload.get("schema") == "bottom-pattern-conversion-core-lra-v1"
        and payload.get("status") == "CORE_UNSAT_CANDIDATE"
    ):
        raise ValueError("source is not a replayed UNSAT conversion core")
    pattern_index = payload["pattern_index"]
    threshold_encoding = payload["universal_threshold_encoding"]
    core = tuple(map(decode, payload["core_partitions"]))
    master, _, selected_cell_encoding, _ = build_base(
        pattern_index, "none", threshold_encoding
    )
    for partition in core:
        master.add_partition_obstruction(partition)
    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    result = {
        "schema": SCHEMA,
        "status": "SAT_BOUNDARY" if solved.status == "SAT" else solved.status,
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "pattern_index": pattern_index,
        "core_size": len(core),
        "source": str(source),
        "source_sha256": sha256(source),
        "source_symmetry_breaking": payload["symmetry_breaking"],
        "tested_symmetry_breaking": "none",
        "universal_threshold_encoding": threshold_encoding,
        "selected_cell_encoding": selected_cell_encoding,
        "values": solved.values,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "claim_boundary": (
            "SAT shows only that these fixed core partitions need the WLOG "
            "canonicalization; UNSAT would strengthen the compact theorem."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    print(json.dumps(run(args.source, args.output, args.time_limit), indent=2))


if __name__ == "__main__":
    main()
