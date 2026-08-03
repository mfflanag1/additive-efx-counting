#!/usr/bin/env python3
"""Decide zero-heavy pair-Hall master by next-triple nonedge witnesses."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import time

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "pair-hall-zero-heavy-next-triple-case-decision-v1"
CORES = (0, 2, 4, 6)
TOKENS = (1, 3, 5, 7)
FLOATER = 8
WITNESS_NAMES = ("next_core_next_token", "next_core_floater", "next_token_floater")
WORKER_SOLVER = None
WORKER_VALUES = None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selections(case: int):
    result = []
    for _ in range(4):
        result.append(case % 3)
        case //= 3
    return tuple(result)


def witness_constraint(values, observer: int, selection: int):
    next_owner = (observer + 1) % 4
    own = values[observer][CORES[observer]] + values[observer][TOKENS[observer]]
    next_core = values[observer][CORES[next_owner]]
    next_token = values[observer][TOKENS[next_owner]]
    floater = values[observer][FLOATER]
    terms = (
        next_core + next_token,
        next_core + floater,
        next_token + floater,
    )
    return terms[selection] > own


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


def decide_case(case: int):
    solver = WORKER_SOLVER
    choices = selections(case)
    solver.push()
    solver.add(
        *(witness_constraint(WORKER_VALUES, observer, choice)
          for observer, choice in enumerate(choices))
    )
    started = time.monotonic()
    verdict = solver.check()
    elapsed = time.monotonic() - started
    result = {
        "case": case,
        "selections": list(choices),
        "witnesses": [WITNESS_NAMES[choice] for choice in choices],
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
    case_ids = range(3 ** 4)
    if workers == 1:
        initialize_worker(str(source), timeout_seconds, solver_profile)
        cases = list(map(decide_case, case_ids))
    else:
        with ProcessPoolExecutor(
            max_workers=workers,
            initializer=initialize_worker,
            initargs=(str(source), timeout_seconds, solver_profile),
        ) as executor:
            cases = list(executor.map(decide_case, case_ids))
    verdicts = sorted({case["verdict"] for case in cases})
    histogram = {
        verdict: sum(case["verdict"] == verdict for case in cases)
        for verdict in verdicts
    }
    artifact = {
        "schema": SCHEMA,
        "status": (
            "SOURCE_UNSAT" if histogram == {"unsat": len(cases)}
            else "SOURCE_SAT" if histogram.get("sat", 0)
            else "INCOMPLETE"
        ),
        "meaning": (
            "For observer i, pair-Hall makes its own base pair a nonedge when "
            "host i+1 receives the floater. Base eligibility leaves only the "
            "three leave-one thresholds of that next triple as strict failure "
            "witnesses. Choosing one witness for each observer gives this "
            "exhaustive, possibly overlapping, 3^4 cover."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "solver": "z3",
        "solver_version": z3.get_version_string(),
        "solver_profile": solver_profile,
        "timeout_seconds_per_case": timeout_seconds,
        "workers": workers,
        "elapsed_seconds": time.monotonic() - started,
        "witness_order": list(WITNESS_NAMES),
        "case_count": len(cases),
        "verdict_histogram": histogram,
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
    artifact = run(args.source, args.output, args.timeout_seconds, args.workers, args.solver_profile)
    print(
        json.dumps(
            {
                key: artifact[key]
                for key in ("status", "elapsed_seconds", "case_count", "verdict_histogram")
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
