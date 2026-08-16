#!/usr/bin/env python3
"""Prove equivalence of plain and comparison-factored rival blockers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_utilitarian_local import local_rivals
    from .run_partial_hall_utilitarian_cegar import (
        base_stabilizer,
        symmetry_images,
        utilitarian_blocker,
    )
    from .run_partial_hall_utilitarian_local_cegar import (
        factored_utilitarian_blocker,
        improving_local_rivals,
    )
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_utilitarian_local import local_rivals
    from run_partial_hall_utilitarian_cegar import (
        base_stabilizer,
        symmetry_images,
        utilitarian_blocker,
    )
    from run_partial_hall_utilitarian_local_cegar import (
        factored_utilitarian_blocker,
        improving_local_rivals,
    )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_selected(checkpoint, base, floater, m, radius):
    saved = json.loads(checkpoint.read_text())
    templates = local_rivals(base, floater, m, radius)
    batch_size = saved["batch_size"]
    learned = set()
    selected = []
    for record in saved["trace"]:
        _, found = improving_local_rivals(record["values"], base, templates)
        new = [
            rival
            for rival in found
            if (rival["floater"], tuple(rival["masks"])) not in learned
        ]
        if len(new) != record["new_improving_local_rival_count"]:
            raise ValueError("checkpoint trace does not replay")
        for rival in new[:batch_size]:
            learned.add((rival["floater"], tuple(rival["masks"])))
            selected.append(rival)
    if len(learned) != saved["learned_rival_count"]:
        raise ValueError("checkpoint learned count does not replay")
    stabilizer = base_stabilizer(base, m)
    orbit = {}
    for rival in selected:
        for image in symmetry_images(rival, stabilizer):
            orbit[(image["floater"], tuple(image["masks"]))] = image
    return selected, tuple(orbit[key] for key in sorted(orbit))


def run(checkpoint, output, timeout_seconds):
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    floater = 8
    m = 9
    radius = 5
    selected, rivals = replay_selected(checkpoint, base, floater, m, radius)
    values = [
        [z3.Real(f"audit_v_{agent}_{good}") for good in range(m)]
        for agent in range(4)
    ]
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    cache = {}
    differences = []
    for rival in rivals:
        plain = utilitarian_blocker(values, base, rival)
        factored = factored_utilitarian_blocker(
            solver, values, base, rival, cache
        )
        differences.append(plain != factored)
    solver.add(z3.Or(*differences))
    verdict = solver.check()
    result = {
        "schema": "partial-hall-rival-factoring-audit-v1",
        "status": (
            "EXACT_EQUIVALENCE"
            if verdict == z3.unsat
            else "COUNTEREXAMPLE"
            if verdict == z3.sat
            else "UNKNOWN"
        ),
        "meaning": (
            "UNSAT proves that every plain normalized-utilitarian rival "
            "blocker in the symmetry-closed seed is logically equivalent "
            "to its shared-comparison factored encoding."
        ),
        "checkpoint": str(checkpoint),
        "checkpoint_sha256": sha256(checkpoint),
        "seed_rival_count": len(selected),
        "orbit_rival_count": len(rivals),
        "factored_comparison_count": len(cache),
        "solver_verdict": str(verdict),
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "timeout_seconds": timeout_seconds,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    result = run(args.checkpoint, args.output, args.timeout_seconds)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
