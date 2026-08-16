#!/usr/bin/env python3
"""Decide whether every blocked fixed cell exposes a size-two Hall defect."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import integerize
    from .partial_hall_factored_master import (
        build_factored_master,
        hall_witnesses_by_size,
    )
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import integerize
    from partial_hall_factored_master import (
        build_factored_master,
        hall_witnesses_by_size,
    )


def run(output: Path, smt2: Path, timeout_seconds: int) -> dict:
    solver, values, base, floater, partitions, edges = build_factored_master(
        timeout_seconds * 1000, hall_encoding="witness"
    )
    for partition_edges in edges:
        pair_witnesses = hall_witnesses_by_size(partition_edges)[1]
        solver.add(z3.Not(z3.Or(*pair_witnesses)))
    verdict = solver.check()
    smt2.write_text(solver.to_smt2())
    model_values = integerize(solver.model(), values) if verdict == z3.sat else None
    artifact = {
        "schema": "partial-hall-pair-deficiency-gate-v1",
        "status": (
            "PAIR_DEFICIENCY_FORCED"
            if verdict == z3.unsat
            else "COUNTEREXAMPLE"
            if verdict == z3.sat
            else "UNKNOWN"
        ),
        "meaning": (
            "UNSAT proves that every eligible radius-one Hall obstruction in "
            "the fixed canonical cell has a candidate partition with a "
            "two-agent, one-neighbor Hall witness. SAT supplies a profile "
            "whose 91 blocked partitions all avoid that motif."
        ),
        "candidate_partition_count": len(partitions),
        "base_bundles": [list(bundle) for bundle in base],
        "floater": floater,
        "solver_verdict": str(verdict),
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "values": model_values,
        "timeout_seconds": timeout_seconds,
        "smt2": str(smt2),
        "smt2_sha256": hashlib.sha256(smt2.read_bytes()).hexdigest(),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.smt2, args.timeout_seconds), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
