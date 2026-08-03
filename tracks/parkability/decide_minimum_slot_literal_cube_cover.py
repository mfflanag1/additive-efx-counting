#!/usr/bin/env python3
"""Decide branches of an exact minimum-slot QF_LRA cube cover in parallel."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "minimum-slot-literal-cube-cover-decision-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational_text(value):
    if z3.is_rational_value(value):
        return str(Fraction(value.numerator_as_long(), value.denominator_as_long()))
    return str(value)


def decide_branch(task):
    index, path_text, expected_hash, timeout_seconds, solver_profile = task
    path = Path(path_text)
    if sha256(path) != expected_hash:
        raise ValueError(f"branch hash mismatch: {path}")
    solver = z3.SolverFor("QF_LRA") if solver_profile == "qf_lra" else z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    solver.from_file(str(path))
    started = time.monotonic()
    verdict = solver.check()
    values = None
    if verdict == z3.sat:
        model = solver.model()
        values = [
            [
                rational_text(
                    model.eval(z3.Real(f"v_{agent}_{good}"), model_completion=True)
                )
                for good in range(9)
            ]
            for agent in range(4)
        ]
    return {
        "branch": index,
        "path": path_text,
        "sha256": expected_hash,
        "verdict": str(verdict),
        "reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "elapsed_seconds": time.monotonic() - started,
        "values": values,
    }


def run(manifest, output, timeout_seconds, workers, solver_profile):
    if (
        output.exists()
        or timeout_seconds <= 0
        or workers <= 0
        or solver_profile not in {"default", "qf_lra"}
    ):
        raise ValueError("a new output and supported solver profile are required")
    cover = json.loads(manifest.read_text())
    if (
        cover.get("schema") != "minimum-slot-literal-cube-cover-v1"
        or cover.get("status") != "EXACT_CUBE_COVER"
        or cover.get("branch_count") != len(cover.get("branches", ()))
    ):
        raise ValueError("invalid exact cube-cover manifest")
    tasks = [
        (
            branch["branch"],
            branch["path"],
            branch["sha256"],
            timeout_seconds,
            solver_profile,
        )
        for branch in cover["branches"]
    ]
    started = time.monotonic()
    if workers == 1:
        branches = list(map(decide_branch, tasks))
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            branches = list(executor.map(decide_branch, tasks))
    verdicts = {branch["verdict"] for branch in branches}
    if "sat" in verdicts:
        status = "SOURCE_SAT"
    elif verdicts == {"unsat"}:
        status = "SOURCE_UNSAT"
    else:
        status = "INCOMPLETE"
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "Decision results for every branch in an exact cube cover. The "
            "source is UNSAT only when every branch is UNSAT."
        ),
        "manifest": str(manifest),
        "manifest_sha256": sha256(manifest),
        "source": cover["source"],
        "source_sha256": cover["source_sha256"],
        "solver": "z3",
        "solver_version": z3.get_version_string(),
        "solver_profile": solver_profile,
        "timeout_seconds_per_branch": timeout_seconds,
        "workers": workers,
        "elapsed_seconds": time.monotonic() - started,
        "branch_count": len(branches),
        "verdict_histogram": {
            verdict: sum(branch["verdict"] == verdict for branch in branches)
            for verdict in sorted(verdicts)
        },
        "branches": branches,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--solver-profile", choices=("default", "qf_lra"), default="qf_lra")
    args = parser.parse_args()
    result = run(
        args.manifest,
        args.output,
        args.timeout_seconds,
        args.workers,
        args.solver_profile,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
