#!/usr/bin/env python3
"""Prove a designated pair trap among 17 canonical radius-one moves."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import candidate_partitions
    from .partial_hall_factored_master import build_factored_master
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import candidate_partitions
    from partial_hall_factored_master import build_factored_master


SELECTED_PARTITIONS = (13, 16, 19, 23, 26, 39, 42, 46, 49, 52, 55, 58, 69, 72, 88, 89, 90)


def designated_bundle(move: dict) -> int:
    return (
        move["move_destination"]
        if move["moved_good"] == 5
        else move["floater_host"]
    )


def run(output: Path, smt2: Path, timeout_seconds: int) -> dict:
    solver, _, base, floater, partitions, edges = build_factored_master(
        timeout_seconds * 1000, hall_encoding="witness"
    )
    moves = list(candidate_partitions(base, floater))
    move_records = []
    designated_traps = []
    for partition_index in SELECTED_PARTITIONS:
        move = moves[partition_index]
        designated = designated_bundle(move)
        witnesses = []
        for pair in itertools.combinations(range(4), 2):
            witness = z3.And(
                *(
                    z3.Not(edges[partition_index][agent][bundle])
                    for agent in pair
                    for bundle in range(4)
                    if bundle != designated
                )
            )
            witnesses.append(witness)
            designated_traps.append(witness)
        move_records.append(
            {
                "partition_index": partition_index,
                "floater_host": move["floater_host"],
                "moved_good": move["moved_good"],
                "move_source": move["move_source"],
                "move_destination": move["move_destination"],
                "designated_bundle": designated,
                "partition": [list(bundle) for bundle in move["partition"]],
            }
        )
    solver.add(z3.Not(z3.Or(*designated_traps)))
    started = time.time()
    verdict = solver.check()
    elapsed = time.time() - started
    smt2.write_text(solver.to_smt2())
    artifact = {
        "schema": "partial-hall-designated-pair-trap-v1",
        "status": "PROVED" if verdict == z3.unsat else str(verdict).upper(),
        "meaning": (
            "UNSAT proves that every eligible radius-one Hall obstruction in "
            "the fixed canonical cell has, among the 17 listed moves, two "
            "agents whose sole acceptable bundle is the move's designated "
            "enlarged host or evacuated-singleton destination."
        ),
        "candidate_partition_count": len(partitions),
        "selected_partition_count": len(SELECTED_PARTITIONS),
        "designated_pair_witness_count": len(designated_traps),
        "moves": move_records,
        "solver_verdict": str(verdict),
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "elapsed_seconds": round(elapsed, 6),
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
