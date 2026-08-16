#!/usr/bin/env python3
"""Exhaust a second transfer after deliberately crossing a Hall-cell wall."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .anneal_partial_hall_utilitarian_maximality import record
    from .fast_count import FastParkability
except ImportError:
    from anneal import atomic_json
    from anneal_partial_hall_utilitarian_maximality import record
    from fast_count import FastParkability


SCHEMA = "partial-hall-cell-crossing-search-v1"


def parse_move(text):
    fields = tuple(map(int, text.split(",")))
    if len(fields) != 4:
        raise ValueError("move must be agent,source,destination,delta")
    return fields


def transfer(values, move):
    agent, source, destination, delta = move
    candidate = [row[:] for row in values]
    if source == destination or candidate[agent][source] <= delta:
        return None
    candidate[agent][source] -= delta
    candidate[agent][destination] += delta
    return candidate


def run(seed, first_move, max_delta, output):
    document = json.loads(seed.read_text())
    values = [list(map(int, row)) for row in document["values"]]
    state = document["fixed_state"]
    crossed = transfer(values, first_move)
    if crossed is None:
        raise ValueError("invalid first move")
    evaluator = FastParkability(4, len(values[0]))
    best = None
    valid = 0
    tested = 0
    for agent in range(4):
        for source in range(len(values[0])):
            for destination in range(len(values[0])):
                if source == destination:
                    continue
                for delta in range(1, max_delta + 1):
                    candidate = transfer(
                        crossed, (agent, source, destination, delta)
                    )
                    if candidate is None:
                        continue
                    tested += 1
                    candidate_record = record(candidate, state, evaluator)
                    if candidate_record is None:
                        continue
                    valid += 1
                    ratio = candidate_record["candidate_to_maximum_ratio"]
                    if best is None or ratio > best["record"]["candidate_to_maximum_ratio"]:
                        best = {
                            "second_move": [agent, source, destination, delta],
                            "values": candidate,
                            "record": candidate_record,
                        }
                    if candidate_record["is_global_maximizer"]:
                        break
                if best is not None and best["record"]["is_global_maximizer"]:
                    break
            if best is not None and best["record"]["is_global_maximizer"]:
                break
        if best is not None and best["record"]["is_global_maximizer"]:
            break
    artifact = {
        "schema": SCHEMA,
        "status": (
            "COUNTEREXAMPLE" if best is not None and best["record"]["is_global_maximizer"]
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes the normalized-utilitarian radius-one Hall "
            "selector, not complete additive EFX."
        ),
        "seed_path": str(seed),
        "seed_sha256": hashlib.sha256(seed.read_bytes()).hexdigest(),
        "first_move": list(first_move),
        "max_second_delta": max_delta,
        "tested_candidate_count": tested,
        "valid_obstruction_count": valid,
        "fixed_state": state,
        "best": best,
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--first-move", type=parse_move, required=True)
    parser.add_argument("--max-delta", type=int, default=16)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = run(args.seed, args.first_move, args.max_delta, args.output)
    print(json.dumps(artifact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
