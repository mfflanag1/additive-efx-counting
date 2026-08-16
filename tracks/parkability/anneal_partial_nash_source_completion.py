#!/usr/bin/env python3
"""Search against source-substitution completion of a maximum-Nash state."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

try:
    from .anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from .anneal_lexmax_all_orders import load_values
    from .fast_count import FastParkability
    from .scan_partial_nash_source_completion import audit_profile
except ImportError:
    from anneal import append_jsonl, atomic_json, has_universal_min, mutate
    from anneal_lexmax_all_orders import load_values
    from fast_count import FastParkability
    from scan_partial_nash_source_completion import audit_profile


SCHEMA = "partial-nash-source-completion-anneal-v1"


def completion_target_count(audit: dict) -> int:
    return sum(
        record["source_completion"][
            "insertable_eligible_rematched_state_count"
        ]
        for record in audit["maximizers"]
        if not record["directly_insertable"]
    )


def best_key(audit: dict) -> tuple[int, int, float]:
    if audit["directly_insertable_maximum_count"]:
        return 2, audit["directly_insertable_maximum_count"], 1.0
    if not audit["selector_survives"]:
        return 0, 0, -1.0
    margin = audit["best_source_completion_normalized_margin"]
    if margin is None:
        raise AssertionError("surviving source selector has no eligible margin")
    return 1, completion_target_count(audit), margin


def score(audit: dict) -> float:
    category, count, margin = best_key(audit)
    return category * 2.0 + count * 0.01 + max(margin, -1.0)


def run(
    *,
    seed_path: Path,
    iterations: int,
    random_seed: int,
    initial_temperature: float,
    final_temperature: float,
    output_path: Path,
    trace_path: Path | None,
) -> dict:
    if (
        iterations < 1
        or initial_temperature <= 0
        or final_temperature <= 0
        or output_path.exists()
        or (trace_path is not None and trace_path.exists())
    ):
        raise ValueError("valid parameters and new outputs are required")
    seed = load_values(seed_path)
    if has_universal_min(seed):
        raise ValueError("seed has a universal-minimum good")
    evaluator = FastParkability(len(seed), len(seed[0]))
    rng = random.Random(random_seed)
    current = [row[:] for row in seed]
    current_audit = audit_profile(current, evaluator)
    best = [row[:] for row in current]
    best_audit = current_audit
    accepted = 0
    improvements = 0
    started = time.time()

    for iteration in range(1, iterations + 1):
        candidate = mutate(
            current,
            current_audit["eligible_base_count"],
            rng,
        )
        if candidate == current or has_universal_min(candidate):
            continue
        candidate_audit = audit_profile(candidate, evaluator)
        progress = (iteration - 1) / max(iterations - 1, 1)
        temperature = initial_temperature * (
            final_temperature / initial_temperature
        ) ** progress
        change = score(candidate_audit) - score(current_audit)
        if change <= 0 or rng.random() < math.exp(-change / temperature):
            current = candidate
            current_audit = candidate_audit
            accepted += 1
        if best_key(candidate_audit) < best_key(best_audit):
            best = [row[:] for row in candidate]
            best_audit = candidate_audit
            improvements += 1
            append_jsonl(
                trace_path,
                {
                    "iteration": iteration,
                    "elapsed_seconds": round(time.time() - started, 6),
                    "values": best,
                    "selector_survives": best_audit["selector_survives"],
                    "directly_insertable_maximum_count": best_audit[
                        "directly_insertable_maximum_count"
                    ],
                    "source_completion_target_count": completion_target_count(
                        best_audit
                    ),
                    "best_source_completion_normalized_margin": best_audit[
                        "best_source_completion_normalized_margin"
                    ],
                },
            )
            print(
                f"iteration={iteration} key={best_key(best_audit)}",
                flush=True,
            )
            if not best_audit["selector_survives"]:
                break

    result = {
        "schema": SCHEMA,
        "status": (
            "SOURCE_COMPLETION_COUNTEREXAMPLE"
            if not best_audit["selector_survives"]
            else "NO_COUNTEREXAMPLE"
        ),
        "meaning": (
            "A counterexample refutes only the maximum-Nash source-"
            "substitution completion selector, not complete additive EFX; "
            "any discovery requires independent exact replay."
        ),
        "seed_path": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "iterations_requested": iterations,
        "iterations_completed": iteration,
        "random_seed": random_seed,
        "initial_temperature": initial_temperature,
        "final_temperature": final_temperature,
        "accepted_moves": accepted,
        "improvements": improvements,
        "elapsed_seconds": round(time.time() - started, 6),
        "values": best,
        "audit": best_audit,
        "claim_boundary": (
            "This adversarial search concerns a proof selector. It does not "
            "search for or certify a complete-EFX counterexample."
        ),
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=1200)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--initial-temperature", type=float, default=0.001)
    parser.add_argument("--final-temperature", type=float, default=0.0000001)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    result = run(
        seed_path=args.seed,
        iterations=args.iterations,
        random_seed=args.random_seed,
        initial_temperature=args.initial_temperature,
        final_temperature=args.final_temperature,
        output_path=args.output,
        trace_path=args.trace,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
