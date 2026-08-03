#!/usr/bin/env python3
"""Adversarially search for a counterexample to the charity selector."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random

try:
    from .anneal import atomic_json
    from .scan_charity_threshold_absorption import scan_profile
except ImportError:
    from anneal import atomic_json
    from scan_charity_threshold_absorption import scan_profile


SCHEMA = "charity-selector-anneal-v1"


def source_records(document):
    return [
        record
        for record in document.get("records", ())
        if record.get("values") is not None
        and record.get("best_absorption_margin") is not None
    ]


def mutate(values, cap, rng):
    candidate = [list(row) for row in values]
    agent = rng.randrange(len(candidate))
    good = rng.randrange(len(candidate[agent]))
    old_value = candidate[agent][good]
    new_value = rng.randrange(1, cap)
    if new_value >= old_value:
        new_value += 1
    candidate[agent][good] = new_value
    return tuple(tuple(row) for row in candidate)


def run(source, output, charity_size, cap, steps, restarts, seed):
    if output.exists():
        raise ValueError("output must be new")
    if min(cap, steps, restarts) < 1:
        raise ValueError("cap, steps, and restarts must be positive")
    source_document = json.loads(source.read_text())
    records = source_records(source_document)
    if not records:
        raise ValueError("source contains no selector records")
    records.sort(key=lambda record: Fraction(record["best_absorption_margin"]))
    starts = [tuple(tuple(row) for row in record["values"]) for record in records[:restarts]]
    rng = random.Random(seed)
    cache = {}

    def evaluate(values):
        if values not in cache:
            cache[values] = scan_profile(values, charity_size)
        result = cache[values]
        margin = result.get("best_absorption_margin")
        return None if margin is None else Fraction(margin), result

    best_values = starts[0]
    best_margin, best_result = evaluate(best_values)
    assert best_margin is not None
    accepted = 0
    counterexample = None
    trace = []
    for restart in range(restarts):
        current = starts[restart % len(starts)]
        for _ in range(restart):
            current = mutate(current, cap, rng)
        current_margin, current_result = evaluate(current)
        if current_margin is None:
            current = starts[0]
            current_margin, current_result = evaluate(current)
        assert current_margin is not None
        for step in range(steps):
            candidate = mutate(current, cap, rng)
            candidate_margin, candidate_result = evaluate(candidate)
            if candidate_margin is None:
                continue
            progress = step / max(1, steps - 1)
            temperature = 0.05 * (0.001 / 0.05) ** progress
            delta = float(candidate_margin - current_margin)
            if delta <= 0 or rng.random() < math.exp(-delta / temperature):
                current = candidate
                current_margin = candidate_margin
                current_result = candidate_result
                accepted += 1
            if current_margin < best_margin:
                best_values = current
                best_margin = current_margin
                best_result = current_result
                trace.append(
                    {
                        "restart": restart,
                        "step": step,
                        "margin": str(best_margin),
                    }
                )
                print(
                    f"restart={restart} step={step} best_margin={best_margin}",
                    flush=True,
                )
            if current_result["status"] == "BLOCKED_SELECTOR_COUNTEREXAMPLE":
                counterexample = {
                    "values": [list(row) for row in current],
                    **current_result,
                }
                break
        if counterexample is not None:
            break
    result = {
        "schema": SCHEMA,
        "status": (
            "BLOCKED_SELECTOR_COUNTEREXAMPLE_FOUND"
            if counterexample is not None
            else "NO_COUNTEREXAMPLE_IN_ANNEAL"
        ),
        "meaning": (
            "Simulated annealing over positive integer valuation profiles, "
            "using the exact global-selector absorption margin as objective."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "charity_size": charity_size,
        "cap": cap,
        "steps_per_restart": steps,
        "restart_count": restarts,
        "seed": seed,
        "evaluated_profile_count": len(cache),
        "accepted_move_count": accepted,
        "best_margin": str(best_margin),
        "best_values": [list(row) for row in best_values],
        "best_result": best_result,
        "improvement_trace": trace,
        "counterexample": counterexample,
        "claim_boundary": (
            "Failure to find a counterexample is heuristic evidence only. A "
            "counterexample would refute the selector, not EFX existence."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--charity-size", type=int, required=True)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--restarts", type=int, default=1)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    result = run(
        args.source,
        args.output,
        args.charity_size,
        args.cap,
        args.steps,
        args.restarts,
        args.seed,
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in ("status", "evaluated_profile_count", "best_margin")
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
