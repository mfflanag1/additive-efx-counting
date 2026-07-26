#!/usr/bin/env python3
"""Regression test for the three-slot off-by-one boundary."""

import argparse
import hashlib
import itertools
import json
import platform
import sys
import time
from pathlib import Path

from ortools import __version__ as ortools_version
from ortools.sat.python import cp_model


N, M, SLOTS = 4, 7, 3
ROOT = Path(__file__).resolve().parents[2]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_efx0(values, assign):
    bundles = [[] for _ in range(N)]
    for good, owner in enumerate(assign):
        bundles[owner].append(good)
    for observer in range(N):
        own = sum(values[observer][good] for good in bundles[observer])
        for owner in range(N):
            if owner == observer:
                continue
            other = sum(values[observer][good] for good in bundles[owner])
            for good in bundles[owner]:
                if own < other - values[observer][good]:
                    return False
    return True


def enumerate_efx0(values):
    return [
        list(assign)
        for assign in itertools.product(range(N), repeat=M)
        if is_efx0(values, assign)
    ]


def fixed_master_status(values, pool):
    model = cp_model.CpModel()
    fixed = [
        [
            model.NewIntVar(values[i][g], values[i][g], f"v_{i}_{g}")
            for g in range(M)
        ]
        for i in range(N)
    ]
    slots = [
        [model.NewIntVar(0, N - 1, f"slot_{t}_{g}") for g in range(M)]
        for t in range(SLOTS)
    ]
    for assign in pool:
        bundles = [[] for _ in range(N)]
        for good, owner in enumerate(assign):
            bundles[owner].append(good)
        disjuncts = []
        for good, owner in enumerate(assign):
            for observer in range(N):
                if observer == owner:
                    continue
                violation = model.NewBoolVar("")
                model.Add(
                    sum(fixed[observer][h] for h in bundles[observer])
                    + fixed[observer][good]
                    + 1
                    <= sum(fixed[observer][h] for h in bundles[owner])
                ).OnlyEnforceIf(violation)
                disjuncts.append(violation)
        for slot in slots:
            protected = model.NewBoolVar("")
            for good, owner in enumerate(assign):
                model.Add(slot[good] == owner).OnlyEnforceIf(protected)
            disjuncts.append(protected)
        model.AddBoolOr(disjuncts)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    return solver.StatusName(solver.Solve(model))


def run(args):
    started = time.time()
    instance = json.loads(args.instance.read_text())
    if instance.get("n") != N or instance.get("m") != M:
        raise ValueError("expected a 4x7 instance")
    values = instance["values"]
    if len(values) != N or any(len(row) != M for row in values):
        raise ValueError("malformed valuation matrix")
    allocations = enumerate_efx0(values)
    statuses = {
        "empty_pool": fixed_master_status(values, []),
        "three_distinct_efx0": fixed_master_status(values, allocations[:3]),
        "all_four_efx0": fixed_master_status(values, allocations),
    }
    passed = (
        len(allocations) == 4
        and len({tuple(assign) for assign in allocations[:3]}) == 3
        and statuses["empty_pool"] in {"OPTIMAL", "FEASIBLE"}
        and statuses["three_distinct_efx0"] in {"OPTIMAL", "FEASIBLE"}
        and statuses["all_four_efx0"] == "INFEASIBLE"
    )
    result = {
        "schema": 1,
        "status": "PASS" if passed else "FAIL",
        "test": "fixed t47 three-slot boundary",
        "instance": str(args.instance),
        "instance_sha256": sha256(args.instance),
        "efx0_count": len(allocations),
        "efx0_allocations": allocations,
        "master_status": statuses,
        "seconds": round(time.time() - started, 3),
        "command": " ".join(sys.argv),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools_version,
            "platform": platform.platform(),
        },
    }
    args.result_out.parent.mkdir(parents=True, exist_ok=True)
    args.result_out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--instance", type=Path, default=ROOT / "results/t47.json"
    )
    parser.add_argument(
        "--result-out",
        type=Path,
        default=ROOT / "results/countcegar_slot_boundary.json",
    )
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
