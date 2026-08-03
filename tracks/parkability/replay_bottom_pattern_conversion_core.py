#!/usr/bin/env python3
"""Replay a mined bottom-pattern conversion core in either encoding."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from .anneal import atomic_json
    from .extract_bottom_pattern_conversion_core import build_base
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
except ImportError:
    from anneal import atomic_json
    from extract_bottom_pattern_conversion_core import build_base
    from run_bottom_pair_pattern_selector_cegar import goods_pattern


SCHEMA = "bottom-pattern-conversion-core-replay-v1"


def run(source_path, result_path, formula_path, threshold_encoding, time_limit):
    if result_path.exists() or formula_path.exists():
        raise ValueError("new output paths are required")
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    if (
        source.get("schema") != "bottom-pattern-conversion-core-lra-v1"
        or source.get("core_size") != len(source.get("core_partitions", []))
    ):
        raise ValueError("source does not contain a complete conversion core")
    pattern = goods_pattern(source["pattern_index"])
    master, _, selected_cell_encoding, symmetry_encoding = build_base(
        pattern,
        source.get("symmetry_breaking", "none"),
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
        "pattern_index": source["pattern_index"],
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "selected_cell_encoding": selected_cell_encoding,
        "symmetry_breaking": source.get("symmetry_breaking", "none"),
        "symmetry_encoding": symmetry_encoding,
        "conversion_orbit": source.get("conversion_orbit"),
        "threshold_encoding": threshold_encoding,
        "core_size": len(core),
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "values": [list(row) for row in solved.values] if solved.values else None,
        "smt2_path": str(formula_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "UNSAT establishes only the conditional bottom-pattern "
            "conversion formula and still requires independent replay."
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
