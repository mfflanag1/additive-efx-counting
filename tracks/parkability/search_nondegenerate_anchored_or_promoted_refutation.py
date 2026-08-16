#!/usr/bin/env python3
"""Search a robust perturbation of a restricted split-packet refutation."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

import z3

try:
    from .run_alternating_anchored_or_promoted_split_cegar import find_restricted_rivals
    from .run_alternating_split_packet_cegar import find_dominating_rivals, structural_solver
except ImportError:
    from run_alternating_anchored_or_promoted_split_cegar import find_restricted_rivals
    from run_alternating_split_packet_cegar import find_dominating_rivals, structural_solver


SCHEMA = "alternating-anchored-or-promoted-nondegenerate-refutation-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin_structural(values) -> bool:
    solver, symbolic, _ = structural_solver()
    solver.add(
        *(symbolic[agent][good] * sum(values[agent]) == values[agent][good]
          for agent in range(4) for good in range(11))
    )
    return solver.check() == z3.sat


def subset_nondegenerate(values) -> list[bool]:
    answer = []
    for row in values:
        sums = {
            sum(row[good] for good in range(11) if mask & (1 << good))
            for mask in range(1 << 11)
        }
        answer.append(len(sums) == 1 << 11)
    return answer


def search(source: Path, output: Path, seed: int, iterations: int, timeout: int) -> dict:
    payload = json.loads(source.read_text())
    base = tuple(tuple(row) for row in payload["values"])
    order = tuple(payload["agent_order"])
    rng = random.Random(seed)
    multiplier = 4096

    for iteration in range(1, iterations + 1):
        rows = []
        for row in base:
            corrections = [1 << exponent for exponent in range(11)]
            rng.shuffle(corrections)
            rows.append(tuple(multiplier * entry + correction for entry, correction in zip(row, corrections)))
        values = tuple(rows)
        if not pin_structural(values):
            continue
        restricted_status, restricted, _, _, restricted_reason = find_restricted_rivals(
            values, order, timeout, 1
        )
        if restricted_status != "unsat":
            continue
        global_status, global_rivals, global_utilities, global_reason = find_dominating_rivals(
            values, order, timeout, 1
        )
        if global_status != "sat" or not global_rivals:
            continue
        nondegenerate = subset_nondegenerate(values)
        if nondegenerate != [True] * 4:
            raise AssertionError("binary perturbation was not subset-nondegenerate")
        result = {
            "schema": SCHEMA,
            "status": "NONDEGENERATE_ANCHORED_OR_PROMOTED_TARGET_REFUTED",
            "claim_boundary": {
                "refuted": "the anchored-or-canonical-promoted dichotomy in the exact eleven-good split-packet cell for the recorded order",
                "not_refuted": "the unrestricted alternating lexicographic escape, two-large closure, or complete EFX",
            },
            "agent_order": list(order),
            "values": [list(row) for row in values],
            "subset_nondegenerate_by_agent": nondegenerate,
            "restricted_rival_status": restricted_status,
            "restricted_reason_unknown": restricted_reason,
            "unrestricted_rival_status": global_status,
            "unrestricted_rival": list(global_rivals[0]),
            "unrestricted_rival_utilities": list(global_utilities[0]),
            "unrestricted_reason_unknown": global_reason,
            "construction": {
                "source": str(source),
                "multiplier": multiplier,
                "random_seed": seed,
                "accepted_iteration": iteration,
            },
            "provenance": {
                "script": str(Path(__file__).resolve().relative_to(Path(__file__).resolve().parents[2])),
                "script_sha256": sha256(Path(__file__).resolve()),
                "source_sha256": sha256(source),
            },
        }
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return result
    raise RuntimeError(f"no robust perturbation found in {iterations} iterations")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--timeout-seconds", type=int, default=10)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output path must not exist")
    result = search(args.source, args.output, args.seed, args.iterations, args.timeout_seconds)
    print(json.dumps({key: result[key] for key in ("status", "construction")}, indent=2))


if __name__ == "__main__":
    main()
