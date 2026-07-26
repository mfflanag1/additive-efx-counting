#!/usr/bin/env python3
"""Cold replay of the exported counting-CEGAR K=4 DIMACS formula."""

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

import check_sat


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_DIMACS_SHA256 = (
    "ccc2aa45a5710d967a166abf7bc56a2026c517f4157730872b99524027baa166"
)


def run(args):
    started = time.perf_counter()
    input_hash = check_sat.sha256(args.dimacs)
    if args.expect_sha256 and input_hash != args.expect_sha256:
        raise ValueError(
            f"DIMACS SHA-256 is {input_hash}, expected {args.expect_sha256}"
        )

    load_started = time.perf_counter()
    cnf = CNF(from_file=str(args.dimacs))
    load_seconds = time.perf_counter() - load_started
    solve_started = time.perf_counter()
    solved, unknown_reason = check_sat.solve_with_timeout(
        cnf.clauses, args.solver, args.timeout_seconds
    )
    solve_seconds = time.perf_counter() - solve_started
    if check_sat.sha256(args.dimacs) != input_hash:
        raise RuntimeError("DIMACS file changed during replay")

    if solved is None:
        status = "UNKNOWN"
    else:
        status = "SAT" if solved["status"] else "UNSAT"
    result = {
        "schema": 1,
        "status": status,
        "replay": "cold solve of existing DIMACS without rebuilding the master",
        "dimacs_path": str(args.dimacs),
        "dimacs_sha256": input_hash,
        "dimacs_bytes": args.dimacs.stat().st_size,
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "solver": {
            "requested": args.solver,
            "backend": solved["backend"] if solved else None,
            "timeout_seconds": args.timeout_seconds,
            "timeout_mechanism": (
                "isolated child process with wall-clock termination"
                if args.timeout_seconds
                else None
            ),
            "statistics": solved["statistics"] if solved else None,
            "cpu_seconds": solved["solver_cpu_seconds"] if solved else None,
        },
        "seconds": {
            "load_dimacs": round(load_seconds, 6),
            "solve_wall": round(solve_seconds, 6),
            "total": round(time.perf_counter() - started, 6),
        },
        "command": shlex.join(sys.argv),
        "environment": {
            "python": platform.python_version(),
            "python_sat": pysat.__version__,
            "platform": platform.platform(),
        },
    }
    if unknown_reason:
        result["reason_unknown"] = unknown_reason
    check_sat.atomic_json(args.result_out, result)
    print(json.dumps(result, indent=2), flush=True)
    if args.expect and status.lower() != args.expect:
        return 1
    return 2 if status == "UNKNOWN" else 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dimacs",
        type=Path,
        default=ROOT / "results/countcegar_K4_sat.cnf",
    )
    parser.add_argument(
        "--expect-sha256", default=EXPECTED_DIMACS_SHA256
    )
    parser.add_argument(
        "--solver",
        choices=["cadical195", "kissat404"],
        default="cadical195",
    )
    parser.add_argument("--timeout-seconds", type=float, default=10800)
    parser.add_argument(
        "--result-out",
        type=Path,
        default=ROOT / "results/countcegar_K4_sat_replay.json",
    )
    parser.add_argument(
        "--expect", choices=["sat", "unsat", "unknown"], default="unsat"
    )
    args = parser.parse_args()
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds < 0:
        parser.error("timeout-seconds must be finite and nonnegative")
    if args.dimacs.resolve() == args.result_out.resolve():
        parser.error("DIMACS input and result JSON paths must differ")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
