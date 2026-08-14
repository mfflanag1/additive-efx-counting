#!/usr/bin/env python3
"""One-shot exact radius-four decision for the rank-three root wall cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_rank_three_global_lex_cegar import (
        CURRENT,
        GOODS,
        RECIPIENTS,
        build_master,
        endpoint_formula,
    )
except ImportError:
    from run_rank_three_global_lex_cegar import (
        CURRENT,
        GOODS,
        RECIPIENTS,
        build_master,
        endpoint_formula,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def allocations(maximum_radius: int):
    old_holder = {
        good: recipient
        for recipient, goods in CURRENT.items()
        for good in goods
    }
    seen = set()
    for radius in range(1, maximum_radius + 1):
        for moved in itertools.combinations(GOODS, radius):
            choices = [
                tuple(recipient for recipient in RECIPIENTS if recipient != old_holder[good])
                for good in moved
            ]
            for destinations in itertools.product(*choices):
                holder = dict(old_holder)
                holder.update(zip(moved, destinations, strict=True))
                allocation = {
                    recipient: tuple(sorted(
                        good for good in GOODS if holder[good] == recipient
                    ))
                    for recipient in RECIPIENTS
                }
                if not allocation["charity"]:
                    continue
                key = tuple(allocation[recipient] for recipient in RECIPIENTS)
                if key in seen:
                    continue
                seen.add(key)
                yield allocation


def run(output: Path, maximum_radius: int, timeout_seconds: int) -> dict:
    solver, value = build_master()
    solver.set(timeout=timeout_seconds * 1000)
    count = 0
    by_radius = {str(radius): 0 for radius in range(1, maximum_radius + 1)}
    old_holder = {
        good: recipient
        for recipient, goods in CURRENT.items()
        for good in goods
    }
    for allocation in allocations(maximum_radius):
        radius = sum(
            old_holder[good] != recipient
            for recipient, goods in allocation.items()
            for good in goods
        )
        by_radius[str(radius)] += 1
        solver.add(z3.Not(endpoint_formula(allocation, value, root_only=True)))
        count += 1

    status = solver.check()
    script = Path(__file__).resolve()
    result = {
        "schema": "rank-three-radius4-global-root-decision-v1",
        "status": str(status),
        "maximum_moved_good_radius": maximum_radius,
        "candidate_allocation_count": count,
        "candidate_count_by_exact_radius": by_radius,
        "solver": f"Z3 {z3.get_version_string()}",
        "claim_boundary": (
            "exact fixed eleven-good positive-additive response-wall cell and "
            "every root-improving EFX allocation within the declared moved-good "
            "radius; UNSAT is bounded-atom/radius evidence only, while SAT is a "
            "countermodel only to that bounded menu"
        ),
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
        },
    }
    if status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-radius", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    args = parser.parse_args()
    result = run(args.output, args.maximum_radius, args.timeout_seconds)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
