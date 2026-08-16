#!/usr/bin/env python3
"""Decide the aggregate, cap-free direct Hall-pair extraction conjecture."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "partial-hall-direct-pair-extraction-aggregate-v1"


def residual(total, minimum, floater=None):
    if floater is None:
        return total - minimum
    return total + floater - z3.If(minimum <= floater, minimum, floater)


def run(output: Path, smt2: Path, timeout_seconds: int) -> dict:
    totals = [[z3.Real(f"t_{agent}_{bundle}") for bundle in range(4)] for agent in range(4)]
    minima = [[z3.Real(f"q_{agent}_{bundle}") for bundle in range(4)] for agent in range(4)]
    floaters = [z3.Real(f"f_{agent}") for agent in range(4)]
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)

    for agent in range(4):
        solver.add(floaters[agent] > 0)
        solver.add(sum(totals[agent]) + floaters[agent] == 1)
        for bundle in range(4):
            solver.add(minima[agent][bundle] > 0)
            solver.add(totals[agent][bundle] >= minima[agent][bundle])
        solver.add(totals[agent][agent] >= floaters[agent])
        for target in range(4):
            if target != agent:
                solver.add(
                    totals[agent][agent]
                    >= residual(totals[agent][target], minima[agent][target])
                )

    edges = {}
    for host in range(4):
        for agent in range(4):
            thresholds = [
                residual(
                    totals[agent][target],
                    minima[agent][target],
                    floaters[agent] if target == host else None,
                )
                for target in range(4)
            ]
            for bundle in range(4):
                candidate = totals[agent][bundle] + (
                    floaters[agent] if bundle == host else 0
                )
                edge = z3.Bool(f"e_{host}_{agent}_{bundle}")
                solver.add(
                    edge
                    == z3.And(
                        *(
                            candidate >= thresholds[target]
                            for target in range(4)
                            if target != bundle
                        )
                    )
                )
                edges[host, agent, bundle] = edge

        for permutation in itertools.permutations(range(4)):
            solver.add(
                z3.Not(
                    z3.And(
                        *(edges[host, agent, permutation[agent]] for agent in range(4))
                    )
                )
            )
        for first, second in itertools.combinations(range(4), 2):
            sole_host = z3.And(
                edges[host, first, host],
                edges[host, second, host],
                *(
                    z3.Not(edges[host, agent, bundle])
                    for agent in (first, second)
                    for bundle in range(4)
                    if bundle != host
                ),
            )
            solver.add(z3.Not(sole_host))

    verdict = solver.check()
    smt2.write_text(solver.to_smt2())
    model = solver.model() if verdict == z3.sat else None
    artifact = {
        "schema": SCHEMA,
        "status": (
            "DIRECT_HOST_PAIR_FORCED"
            if verdict == z3.unsat
            else "AGGREGATE_COUNTEREXAMPLE"
            if verdict == z3.sat
            else "UNKNOWN"
        ),
        "meaning": (
            "UNSAT proves that arbitrary four-agent positive-additive "
            "one-floater EFX states either complete after direct insertion and "
            "rematching, or some direct-insertion graph has two agents whose "
            "sole neighbor is the enlarged host. SAT may be an aggregate "
            "counterexample and must be checked for realization by item values."
        ),
        "abstraction": (
            "Each agent-bundle pair retains only total value and least-item "
            "value, which exactly determine additive EFX thresholds. Constraints "
            "allow a relaxation of bundle-minimum realizability, so UNSAT is sound."
        ),
        "solver_verdict": str(verdict),
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "model": (
            {
                "totals": [
                    [model.evaluate(value).sexpr() for value in row] for row in totals
                ],
                "minima": [
                    [model.evaluate(value).sexpr() for value in row] for row in minima
                ],
                "floaters": [model.evaluate(value).sexpr() for value in floaters],
                "graphs": {
                    str(host): [
                        [
                            bundle
                            for bundle in range(4)
                            if z3.is_true(model.evaluate(edges[host, agent, bundle]))
                        ]
                        for agent in range(4)
                    ]
                    for host in range(4)
                },
            }
            if model is not None
            else None
        ),
        "timeout_seconds": timeout_seconds,
        "smt2": str(smt2),
        "smt2_sha256": hashlib.sha256(smt2.read_bytes()).hexdigest(),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--smt2", required=True, type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.smt2, args.timeout_seconds), indent=2))


if __name__ == "__main__":
    main()
