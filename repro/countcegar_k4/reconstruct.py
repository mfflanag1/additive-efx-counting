#!/usr/bin/env python3
"""Reconstruct a complete K=4 counting-CEGAR pool without altering the archive."""

import argparse
import hashlib
import json
import os
import platform
import sys
import tempfile
import time
from pathlib import Path

from ortools import __version__ as ortools_version
from ortools.sat.python import cp_model


N, M, SLOTS = 4, 7, 3
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from verify import enumerate_all  # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(value, f, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise


def atomic_text(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(value)
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise


def validate_pool(raw):
    if not isinstance(raw, list):
        raise ValueError("pool must be a JSON list")
    pool = []
    seen = set()
    for index, assign in enumerate(raw):
        if (
            not isinstance(assign, list)
            or len(assign) != M
            or any(type(a) is not int or not 0 <= a < N for a in assign)
        ):
            raise ValueError(f"invalid allocation at pool index {index}")
        key = tuple(assign)
        if key not in seen:
            seen.add(key)
            pool.append(assign)
    return pool


def lex_ge(model, xs, ys):
    prefix_equal = []
    for x, y in zip(xs, ys):
        equal = model.NewBoolVar("")
        model.Add(x == y).OnlyEnforceIf(equal)
        model.Add(x != y).OnlyEnforceIf(equal.Not())
        prefix_equal.append(equal)
    model.Add(xs[0] >= ys[0])
    for index in range(1, len(xs)):
        model.Add(xs[index] >= ys[index]).OnlyEnforceIf(prefix_equal[:index])


def build_master(K, pool):
    model = cp_model.CpModel()
    values = [
        [model.NewIntVar(1, K, f"v_{i}_{g}") for g in range(M)]
        for i in range(N)
    ]
    for i in range(N - 1):
        lex_ge(model, values[i], values[i + 1])
    for g in range(M - 1):
        lex_ge(
            model,
            [values[i][g] for i in range(N)],
            [values[i][g + 1] for i in range(N)],
        )

    slots = [
        [model.NewIntVar(0, N - 1, f"slot_{t}_{g}") for g in range(M)]
        for t in range(SLOTS)
    ]
    for assign in pool:
        bundles = [[] for _ in range(N)]
        for g, owner in enumerate(assign):
            bundles[owner].append(g)
        disjuncts = []
        for g, owner in enumerate(assign):
            for observer in range(N):
                if observer == owner:
                    continue
                violation = model.NewBoolVar("")
                model.Add(
                    sum(values[observer][h] for h in bundles[observer])
                    + values[observer][g]
                    + 1
                    <= sum(values[observer][h] for h in bundles[owner])
                ).OnlyEnforceIf(violation)
                disjuncts.append(violation)
        for t in range(SLOTS):
            protected = model.NewBoolVar("")
            for g, owner in enumerate(assign):
                model.Add(slots[t][g] == owner).OnlyEnforceIf(protected)
            disjuncts.append(protected)
        model.AddBoolOr(disjuncts)
    return model, values


def result_record(args, status, pool, started, rounds, **extra):
    record = {
        "schema": 1,
        "status": status,
        "claim": "every 4x7 valuation matrix over {1,2,3,4} has at least 4 EFX0 allocations",
        "K": args.K,
        "pool_size": len(pool),
        "pool_sha256": sha256(args.pool_out),
        "rounds_this_invocation": rounds,
        "seconds_this_invocation": round(time.time() - started, 3),
        "command": " ".join(sys.argv),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools_version,
            "platform": platform.platform(),
        },
        "solver_parameters": {
            "num_search_workers": args.workers,
            "max_time_in_seconds": args.max_time,
            "random_seed": args.random_seed,
        },
    }
    record.update(extra)
    return record


def export_terminal_solver_artifacts(args, model, solver):
    atomic_text(args.model_out, str(model.Proto()))
    atomic_text(args.response_out, str(solver.ResponseProto()))
    atomic_text(args.stats_out, solver.ResponseStats() + "\n")
    return {
        "cp_model_pbtxt": str(args.model_out),
        "cp_model_sha256": sha256(args.model_out),
        "cp_solver_response_pbtxt": str(args.response_out),
        "cp_solver_response_sha256": sha256(args.response_out),
        "cp_solver_stats": str(args.stats_out),
        "cp_solver_stats_sha256": sha256(args.stats_out),
    }


def run(args):
    source = args.pool_out if args.pool_out.exists() else args.seed_pool
    raw = json.loads(source.read_text())
    pool = validate_pool(raw)
    dropped = len(raw) - len(pool)
    atomic_json(args.pool_out, pool)
    print(
        json.dumps(
            {
                "event": "resume",
                "source": str(source),
                "raw_pool_size": len(raw),
                "unique_pool_size": len(pool),
                "duplicates_dropped": dropped,
            }
        ),
        flush=True,
    )

    known = {tuple(assign) for assign in pool}
    started = time.time()
    rounds = 0
    while args.max_rounds == 0 or rounds < args.max_rounds:
        rounds += 1
        round_started = time.time()
        model, values = build_master(args.K, pool)
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = args.workers
        solver.parameters.max_time_in_seconds = args.max_time
        solver.parameters.random_seed = args.random_seed
        status = solver.Solve(model)
        status_name = solver.StatusName(status)

        if status == cp_model.INFEASIBLE:
            exports = export_terminal_solver_artifacts(
                args, model, solver
            )
            record = result_record(
                args,
                "UNSAT",
                pool,
                started,
                rounds,
                cp_sat_status=status_name,
                **exports,
            )
            atomic_json(args.result_out, record)
            print(json.dumps({"event": "terminal", **record}), flush=True)
            return 0
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            record = result_record(
                args,
                "INCOMPLETE",
                pool,
                started,
                rounds,
                cp_sat_status=status_name,
            )
            atomic_json(args.result_out, record)
            print(json.dumps({"event": "terminal", **record}), flush=True)
            return 2

        valuation = [
            [solver.Value(values[i][g]) for g in range(M)] for i in range(N)
        ]
        checked = enumerate_all(N, M, valuation, collect=args.add)
        count = checked["efx0_count"]
        if count <= SLOTS:
            record = result_record(
                args,
                "WITNESS",
                pool,
                started,
                rounds,
                cp_sat_status=status_name,
                efx0_count=count,
                values=valuation,
            )
            atomic_json(args.result_out, record)
            print(json.dumps({"event": "terminal", **record}), flush=True)
            return 1

        additions = []
        for assign in checked["examples_efx0"]:
            key = tuple(assign)
            if key not in known:
                known.add(key)
                additions.append(assign)
        if not additions:
            raise RuntimeError("SAT master produced no new EFX0 allocation")
        pool.extend(additions)
        atomic_json(args.pool_out, pool)
        trace = {
            "round": rounds,
            "cp_sat_status": status_name,
            "solve_seconds": round(time.time() - round_started, 3),
            "efx0_count": count,
            "values": valuation,
            "added": additions,
            "pool_size": len(pool),
            "pool_sha256": sha256(args.pool_out),
        }
        args.trace_out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.trace_out, "a") as f:
            f.write(json.dumps(trace, separators=(",", ":")) + "\n")
        print(json.dumps({"event": "cut", **trace}), flush=True)

    record = result_record(
        args,
        "CHECKPOINT",
        pool,
        started,
        rounds,
        cp_sat_status="not_run_after_last_cut",
    )
    atomic_json(args.result_out, record)
    print(json.dumps({"event": "checkpoint", **record}), flush=True)
    return 2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--K", type=int, default=4, choices=[4])
    parser.add_argument(
        "--seed-pool", type=Path, default=ROOT / "results/countpool_K4.json"
    )
    parser.add_argument(
        "--pool-out",
        type=Path,
        default=ROOT / "results/countpool_K4_complete.json",
    )
    parser.add_argument(
        "--result-out",
        type=Path,
        default=ROOT / "results/countcegar_K4_reconstructed.json",
    )
    parser.add_argument(
        "--trace-out",
        type=Path,
        default=ROOT / "results/countcegar_K4_reconstruction.jsonl",
    )
    parser.add_argument(
        "--model-out",
        type=Path,
        default=ROOT / "results/countcegar_K4_complete_model.pbtxt",
    )
    parser.add_argument(
        "--response-out",
        type=Path,
        default=ROOT / "results/countcegar_K4_complete_response.pbtxt",
    )
    parser.add_argument(
        "--stats-out",
        type=Path,
        default=ROOT / "results/countcegar_K4_complete_stats.txt",
    )
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--max-time", type=float, default=10800)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--add", type=int, default=16)
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=0,
        help="0 means continue until a terminal solver status",
    )
    args = parser.parse_args()
    if args.workers < 1 or args.max_time <= 0 or args.add < SLOTS + 1:
        parser.error("workers/max-time must be positive and add must be at least 4")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
