#!/usr/bin/env python3
"""Cold replay of an exported parkability terminal DIMACS formula."""

from __future__ import annotations

import argparse
import json
import math
import platform
import shlex
import sys
import time
from pathlib import Path

import pysat
from pysat.formula import CNF

try:
    from . import terminal_cnf
except ImportError:
    import terminal_cnf


def run(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    source_path = Path(__file__).resolve()
    source_hash = terminal_cnf.sha256(source_path)
    input_hash = terminal_cnf.sha256(args.dimacs)
    if args.expect_sha256 is not None and input_hash != args.expect_sha256:
        raise ValueError(
            f"DIMACS SHA-256 is {input_hash}, expected {args.expect_sha256}"
        )

    load_started = time.perf_counter()
    cnf = CNF(from_file=str(args.dimacs))
    load_seconds = time.perf_counter() - load_started
    solve_started = time.perf_counter()
    solved, unknown_reason = terminal_cnf.solve_with_timeout(
        cnf.clauses, args.solver, args.timeout_seconds
    )
    solve_seconds = time.perf_counter() - solve_started
    if terminal_cnf.sha256(args.dimacs) != input_hash:
        raise RuntimeError("DIMACS changed during cold replay")
    if terminal_cnf.sha256(source_path) != source_hash:
        raise RuntimeError("cold replay source changed during solving")

    if solved is None:
        solver_status = "UNKNOWN"
        status = "UNKNOWN"
    else:
        solver_status = "SAT" if solved["status"] else "UNSAT"
        status = "SAT" if solved["status"] else "UNSAT_SOLVER_RESULT"
    result = {
        "schema": "parkability-terminal-cnf-replay-v1",
        "status": status,
        "replay": "cold solve of frozen DIMACS without rebuilding the master",
        "dimacs_path": str(args.dimacs.resolve()),
        "dimacs_sha256": input_hash,
        "dimacs_bytes": args.dimacs.stat().st_size,
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "solver": {
            "status": solver_status,
            "requested": args.solver,
            "backend": solved["backend"] if solved else None,
            "timeout_seconds": args.timeout_seconds,
            "statistics": solved["statistics"] if solved else None,
            "cpu_seconds": (solved["solver_cpu_seconds"] if solved else None),
        },
        "seconds": {
            "load_dimacs": round(load_seconds, 6),
            "solve_wall": round(solve_seconds, 6),
            "total": round(time.perf_counter() - started, 6),
        },
        "command": shlex.join(sys.argv),
        "source_sha256": source_hash,
        "environment": {
            "python": platform.python_version(),
            "python_sat": pysat.__version__,
            "platform": platform.platform(),
        },
    }
    if unknown_reason is not None:
        result["reason_unknown"] = unknown_reason
    if solver_status == "SAT":
        assignment = {abs(literal): literal > 0 for literal in solved["model"]}
        clauses_valid = all(
            any(
                assignment.get(abs(literal), False) == (literal > 0)
                for literal in clause
            )
            for clause in cnf.clauses
        )
        if not clauses_valid:
            raise RuntimeError("cold replay SAT model fails the DIMACS")
        result["model"] = solved["model"]
        result["model_verified"] = {"all_dimacs_clauses": True}
    terminal_cnf.atomic_json(args.result_out, result)
    print(json.dumps(result, indent=2), flush=True)
    if args.expect is not None and solver_status.lower() != args.expect:
        return 1
    return 2 if solver_status == "UNKNOWN" else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimacs", type=Path, required=True)
    parser.add_argument("--expect-sha256")
    parser.add_argument(
        "--solver",
        choices=("cadical195", "kissat404"),
        default="cadical195",
    )
    parser.add_argument("--timeout-seconds", type=float, default=0)
    parser.add_argument("--result-out", type=Path, required=True)
    parser.add_argument("--expect", choices=("sat", "unsat", "unknown"))
    args = parser.parse_args()
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds < 0:
        parser.error("timeout-seconds must be finite and nonnegative")
    if args.dimacs.resolve() == args.result_out.resolve():
        parser.error("DIMACS and result paths must be distinct")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
