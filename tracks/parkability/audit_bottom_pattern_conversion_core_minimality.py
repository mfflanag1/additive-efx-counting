#!/usr/bin/env python3
"""Check deletion minimality of a compact bottom-pattern conversion core."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from .anneal import atomic_json
    from .extract_bottom_pattern_conversion_core import build_base
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    from anneal import atomic_json
    from extract_bottom_pattern_conversion_core import build_base
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "bottom-pattern-conversion-core-minimality-audit-v1"


def decode(raw):
    return tuple(tuple(bundle) for bundle in raw)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source, output, time_limit):
    payload = json.loads(source.read_text())
    if not (
        payload.get("schema") == "bottom-pattern-conversion-core-lra-v1"
        and payload.get("status") == "CORE_UNSAT_CANDIDATE"
        and payload.get("replay_solver_status") == "unsat"
    ):
        raise ValueError("source is not a replayed UNSAT conversion core")
    pattern_index = payload["pattern_index"]
    symmetry_breaking = payload["symmetry_breaking"]
    threshold_encoding = payload["universal_threshold_encoding"]
    core = tuple(map(decode, payload["core_partitions"]))
    checks = []
    for omitted_index, omitted in enumerate(core):
        master, _, _, _ = build_base(
            pattern_index, symmetry_breaking, threshold_encoding
        )
        for retained_index, partition in enumerate(core):
            if retained_index != omitted_index:
                master.add_partition_obstruction(partition)
        started = time.time()
        solved = master.solve(time_limit_s=time_limit)
        elapsed = time.time() - started
        omitted_supported = (
            len(supported_partitions(solved.values, [omitted])) == 1
            if solved.status == "SAT"
            else None
        )
        checks.append(
            {
                "omitted_index": omitted_index,
                "omitted_partition": [list(bundle) for bundle in omitted],
                "status": solved.status,
                "solver_status": solved.raw_status,
                "reason_unknown": solved.reason_unknown,
                "omitted_partition_supports_efx": omitted_supported,
                "values": solved.values,
                "elapsed_seconds": elapsed,
            }
        )
    deletion_minimal = all(
        check["status"] == "SAT"
        and check["omitted_partition_supports_efx"] is True
        for check in checks
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "DELETION_MINIMAL_CORE_AUDITED"
            if deletion_minimal
            else "DELETION_MINIMALITY_INCOMPLETE"
        ),
        "pattern_index": pattern_index,
        "core_size": len(core),
        "deletion_minimal": deletion_minimal,
        "source": str(source),
        "source_sha256": sha256(source),
        "symmetry_breaking": symmetry_breaking,
        "universal_threshold_encoding": threshold_encoding,
        "time_limit_seconds_per_deletion": time_limit,
        "checks": checks,
        "claim_boundary": (
            "Deletion minimality means every listed partition is necessary "
            "for this fixed canonical core. It is not a uniqueness claim."
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
