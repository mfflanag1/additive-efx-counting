#!/usr/bin/env python3
"""Decide the canonical pair-Hall master by heavy-token sign pattern."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import itertools
import json
from pathlib import Path
import time

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "pair-hall-heavy-token-case-decision-v1"
CORES = (0, 2, 4, 6)
HEAVY_EDGES = (
    (0, 5),
    (1, 5),
    (1, 7),
    (2, 7),
    (2, 1),
    (3, 1),
    (3, 3),
)
TOKENS = (1, 3, 5, 7)
WORKER_SOLVER = None
WORKER_VALUES = None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_edges(mask: int):
    return tuple(
        edge
        for position, edge in enumerate(HEAVY_EDGES)
        if (mask >> position) & 1
    )


def maximum_matching_size(edges) -> int:
    edge_set = set(edges)
    for size in range(4, -1, -1):
        for owners in itertools.combinations(range(4), size):
            for tokens in itertools.permutations(TOKENS, size):
                if all((owner, token) in edge_set for owner, token in zip(owners, tokens)):
                    return size
    raise AssertionError("empty matching was not found")


def minimum_hall_witness(edges):
    edge_set = set(edges)
    witnesses = []
    for size in range(1, 5):
        for owners in itertools.combinations(range(4), size):
            neighbors = tuple(
                token
                for token in TOKENS
                if any((owner, token) in edge_set for owner in owners)
            )
            if len(neighbors) < len(owners):
                witnesses.append((owners, neighbors))
        if witnesses:
            return min(witnesses, key=lambda witness: (len(witness[1]), witness))
    return None


def initialize_worker(source: str, timeout_seconds: int, solver_profile: str):
    global WORKER_SOLVER, WORKER_VALUES
    WORKER_SOLVER = z3.SolverFor("QF_LRA") if solver_profile == "qf_lra" else z3.Solver()
    WORKER_SOLVER.set(timeout=timeout_seconds * 1000)
    if solver_profile == "arith2":
        WORKER_SOLVER.set("smt.arith.solver", 2)
    WORKER_SOLVER.from_file(source)
    WORKER_VALUES = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]


def decide_mask(mask: int):
    solver = WORKER_SOLVER
    values = WORKER_VALUES
    solver.push()
    for position, (owner, token) in enumerate(HEAVY_EDGES):
        heavy = values[owner][token] > values[owner][CORES[owner]]
        solver.add(heavy if (mask >> position) & 1 else z3.Not(heavy))
    started = time.monotonic()
    verdict = solver.check()
    elapsed = time.monotonic() - started
    edges = selected_edges(mask)
    witness = minimum_hall_witness(edges)
    result = {
        "mask": mask,
        "bits": [int(bool((mask >> position) & 1)) for position in range(len(HEAVY_EDGES))],
        "heavy_edges": [list(edge) for edge in edges],
        "maximum_matching_size": maximum_matching_size(edges),
        "minimum_hall_witness": (
            {"owners": list(witness[0]), "tokens": list(witness[1])}
            if witness is not None
            else None
        ),
        "verdict": str(verdict),
        "reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "elapsed_seconds": elapsed,
    }
    solver.pop()
    return result


def run(source: Path, output: Path, timeout_seconds: int, workers: int, solver_profile: str):
    if (
        not source.is_file()
        or output.exists()
        or timeout_seconds <= 0
        or workers <= 0
        or solver_profile not in {"default", "qf_lra", "arith2"}
    ):
        raise ValueError("existing source, new output, positive bounds, and supported profile required")
    started = time.monotonic()
    if workers == 1:
        initialize_worker(str(source), timeout_seconds, solver_profile)
        cases = list(map(decide_mask, range(1 << len(HEAVY_EDGES))))
    else:
        with ProcessPoolExecutor(
            max_workers=workers,
            initializer=initialize_worker,
            initargs=(str(source), timeout_seconds, solver_profile),
        ) as executor:
            cases = list(executor.map(decide_mask, range(1 << len(HEAVY_EDGES))))
    verdicts = sorted({case["verdict"] for case in cases})
    histogram = {
        verdict: sum(case["verdict"] == verdict for case in cases)
        for verdict in verdicts
    }
    by_witness_size = {}
    for case in cases:
        witness = case["minimum_hall_witness"]
        key = "none" if witness is None else str(len(witness["owners"]))
        by_witness_size.setdefault(key, {verdict: 0 for verdict in verdicts})
        by_witness_size[key][case["verdict"]] += 1
    matching_at_least_two_cases = [
        case for case in cases if case["maximum_matching_size"] >= 2
    ]
    matching_at_least_two_histogram = {
        verdict: sum(case["verdict"] == verdict for case in matching_at_least_two_cases)
        for verdict in verdicts
    }
    matching_number_at_most_one_proved = all(
        case["verdict"] == "unsat" for case in matching_at_least_two_cases
    )
    artifact = {
        "schema": SCHEMA,
        "status": (
            "SOURCE_UNSAT" if histogram == {"unsat": len(cases)}
            else "SOURCE_SAT" if histogram.get("sat", 0)
            else "INCOMPLETE"
        ),
        "meaning": (
            "The seven signs form an exact cover after the proved owner-minimum, "
            "floater, predecessor-token, and canonical next-token walls remove "
            "all other possible strict token-above-core edges."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "solver": "z3",
        "solver_version": z3.get_version_string(),
        "solver_profile": solver_profile,
        "timeout_seconds_per_case": timeout_seconds,
        "workers": workers,
        "elapsed_seconds": time.monotonic() - started,
        "heavy_edge_order": [
            {"position": position, "owner": owner, "token": token}
            for position, (owner, token) in enumerate(HEAVY_EDGES)
        ],
        "case_count": len(cases),
        "verdict_histogram": histogram,
        "verdicts_by_minimum_hall_witness_size": by_witness_size,
        "matching_at_least_two_case_count": len(matching_at_least_two_cases),
        "matching_at_least_two_verdict_histogram": matching_at_least_two_histogram,
        "matching_number_at_most_one_proved": matching_number_at_most_one_proved,
        "cases": cases,
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=10)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--solver-profile", choices=("default", "qf_lra", "arith2"), default="arith2")
    args = parser.parse_args()
    artifact = run(
        args.source,
        args.output,
        args.timeout_seconds,
        args.workers,
        args.solver_profile,
    )
    print(
        json.dumps(
            {
                key: artifact[key]
                for key in (
                    "status",
                    "elapsed_seconds",
                    "case_count",
                    "verdict_histogram",
                    "verdicts_by_minimum_hall_witness_size",
                    "matching_at_least_two_case_count",
                    "matching_at_least_two_verdict_histogram",
                    "matching_number_at_most_one_proved",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
