#!/usr/bin/env python3
"""Decide the zero-heavy pair-Hall master by token/core equality pattern."""

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
    from .run_minimum_slot_orbit_cegar import CANONICAL_HEAVY_TOKEN_EDGES, CORES
except ImportError:
    from anneal import atomic_json
    from run_minimum_slot_orbit_cegar import CANONICAL_HEAVY_TOKEN_EDGES, CORES


SCHEMA = "pair-hall-zero-heavy-equality-case-decision-v1"
WORKER_SOLVER = None
WORKER_VALUES = None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational_text(value):
    if z3.is_rational_value(value):
        return str(Fraction(value.numerator_as_long(), value.denominator_as_long()))
    return str(value)


def initialize_worker(source: str, timeout_seconds: int, solver_profile: str):
    global WORKER_SOLVER, WORKER_VALUES
    if solver_profile == "qf_lra":
        WORKER_SOLVER = z3.SolverFor("QF_LRA")
    elif solver_profile == "sls_smt":
        WORKER_SOLVER = z3.Tactic("sls-smt").solver()
    else:
        WORKER_SOLVER = z3.Solver()
    WORKER_SOLVER.set(timeout=timeout_seconds * 1000)
    if solver_profile == "arith2":
        WORKER_SOLVER.set("smt.arith.solver", 2)
    WORKER_SOLVER.from_file(source)
    WORKER_VALUES = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]


def equality_constraints(values, mask):
    return tuple(
        (
            values[owner][token] == values[owner][CORES[owner]]
            if (mask >> position) & 1
            else values[owner][token] < values[owner][CORES[owner]]
        )
        for position, (owner, token) in enumerate(CANONICAL_HEAVY_TOKEN_EDGES)
    )


def decide_mask(mask: int):
    solver = WORKER_SOLVER
    values = WORKER_VALUES
    solver.push()
    solver.add(*equality_constraints(values, mask))
    started = time.monotonic()
    verdict = solver.check()
    model_values = None
    if verdict == z3.sat:
        model = solver.model()
        model_values = [
            [
                rational_text(model.eval(value, model_completion=True))
                for value in row
            ]
            for row in values
        ]
    result = {
        "mask": mask,
        "equality_count": mask.bit_count(),
        "equal_edges": [
            list(edge)
            for position, edge in enumerate(CANONICAL_HEAVY_TOKEN_EDGES)
            if (mask >> position) & 1
        ],
        "verdict": str(verdict),
        "reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "elapsed_seconds": time.monotonic() - started,
        "values": model_values,
    }
    solver.pop()
    return result


def run(
    source,
    output,
    timeout_seconds,
    workers,
    solver_profile,
    masks=(),
    smt2_output=None,
):
    if (
        not source.is_file()
        or output.exists()
        or timeout_seconds <= 0
        or workers <= 0
        or solver_profile not in {"default", "qf_lra", "arith2", "sls_smt"}
    ):
        raise ValueError("existing source, new output, positive bounds, and supported profile required")
    all_masks = tuple(range(1 << len(CANONICAL_HEAVY_TOKEN_EDGES)))
    masks = tuple(dict.fromkeys(masks)) if masks else all_masks
    if any(mask not in all_masks for mask in masks):
        raise ValueError("equality masks must lie in [0,127]")
    if smt2_output is not None:
        if len(masks) != 1 or smt2_output.exists():
            raise ValueError("SMT2 export requires one selected mask and a new path")
        export_solver = z3.Solver()
        export_solver.from_file(str(source))
        export_values = [
            [z3.Real(f"v_{agent}_{good}") for good in range(9)]
            for agent in range(4)
        ]
        export_solver.add(*equality_constraints(export_values, masks[0]))
        smt2_output.write_text(export_solver.to_smt2())
    started = time.monotonic()
    if workers == 1:
        initialize_worker(str(source), timeout_seconds, solver_profile)
        cases = list(map(decide_mask, masks))
    else:
        with ProcessPoolExecutor(
            max_workers=workers,
            initializer=initialize_worker,
            initargs=(str(source), timeout_seconds, solver_profile),
        ) as executor:
            cases = list(executor.map(decide_mask, masks))
    verdicts = sorted({case["verdict"] for case in cases})
    histogram = {
        verdict: sum(case["verdict"] == verdict for case in cases)
        for verdict in verdicts
    }
    by_equality_count = {
        str(count): {
            verdict: sum(
                case["equality_count"] == count and case["verdict"] == verdict
                for case in cases
            )
            for verdict in verdicts
        }
        for count in range(len(CANONICAL_HEAVY_TOKEN_EDGES) + 1)
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "SOURCE_UNSAT"
            if masks == all_masks and histogram == {"unsat": len(cases)}
            else "SELECTED_CASES_UNSAT"
            if histogram == {"unsat": len(cases)}
            else "SOURCE_SAT"
            if histogram.get("sat", 0)
            else "INCOMPLETE"
        ),
        "meaning": (
            "Under the source's seven weak token-at-most-core inequalities, "
            "equality versus strict inequality forms an exact 128-case cover."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "solver": "z3",
        "solver_version": z3.get_version_string(),
        "solver_profile": solver_profile,
        "timeout_seconds_per_case": timeout_seconds,
        "workers": workers,
        "elapsed_seconds": time.monotonic() - started,
        "edge_order": [
            {"position": position, "owner": owner, "token": token}
            for position, (owner, token) in enumerate(CANONICAL_HEAVY_TOKEN_EDGES)
        ],
        "case_count": len(cases),
        "exact_source_cover": masks == all_masks,
        "selected_masks": list(masks),
        "smt2_output": str(smt2_output) if smt2_output is not None else None,
        "smt2_output_sha256": (
            sha256(smt2_output) if smt2_output is not None else None
        ),
        "verdict_histogram": histogram,
        "verdicts_by_equality_count": by_equality_count,
        "cases": cases,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--mask", type=int, action="append", default=[])
    parser.add_argument("--smt2-output", type=Path)
    parser.add_argument(
        "--solver-profile",
        choices=("default", "qf_lra", "arith2", "sls_smt"),
        default="arith2",
    )
    args = parser.parse_args()
    result = run(
        args.source,
        args.output,
        args.timeout_seconds,
        args.workers,
        args.solver_profile,
        args.mask,
        args.smt2_output,
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "elapsed_seconds",
                    "case_count",
                    "verdict_histogram",
                    "verdicts_by_equality_count",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
