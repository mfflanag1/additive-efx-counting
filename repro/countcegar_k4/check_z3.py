#!/usr/bin/env python3
"""Independent Z3 checker/exporter for a counting-CEGAR K=4 master."""

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import z3


N, M, SLOTS = 4, 7, 3
ROOT = Path(__file__).resolve().parents[2]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pool(path):
    raw = json.loads(path.read_text())
    if not isinstance(raw, list):
        raise ValueError("pool must be a JSON list")
    unique = []
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
            unique.append(assign)
    return raw, unique


def lex_ge(xs, ys):
    greater_at = []
    for index in range(len(xs)):
        greater_at.append(
            z3.And(
                *[xs[prefix] == ys[prefix] for prefix in range(index)],
                xs[index] > ys[index],
            )
        )
    return z3.Or(*greater_at, z3.And(*[x == y for x, y in zip(xs, ys)]))


def total(terms):
    return z3.Sum(terms) if terms else z3.IntVal(0)


def build_lia_master(K, pool):
    solver = z3.Solver()
    values = [
        [z3.Int(f"v_{i}_{g}") for g in range(M)] for i in range(N)
    ]
    slots = [
        [z3.Int(f"slot_{t}_{g}") for g in range(M)] for t in range(SLOTS)
    ]
    for row in values:
        for value in row:
            solver.add(value >= 1, value <= K)
    for slot in slots:
        for owner in slot:
            solver.add(owner >= 0, owner < N)
    for i in range(N - 1):
        solver.add(lex_ge(values[i], values[i + 1]))
    for g in range(M - 1):
        solver.add(
            lex_ge(
                [values[i][g] for i in range(N)],
                [values[i][g + 1] for i in range(N)],
            )
        )

    for assign in pool:
        bundles = [[] for _ in range(N)]
        for g, owner in enumerate(assign):
            bundles[owner].append(g)
        disjuncts = []
        for g, owner in enumerate(assign):
            for observer in range(N):
                if observer == owner:
                    continue
                disjuncts.append(
                    total(values[observer][h] for h in bundles[observer])
                    + values[observer][g]
                    + 1
                    <= total(values[observer][h] for h in bundles[owner])
                )
        for slot in slots:
            disjuncts.append(
                z3.And(*[slot[g] == owner for g, owner in enumerate(assign)])
            )
        solver.add(z3.Or(*disjuncts))
    return solver, values, slots


def build_lia_cardinality_master(K, pool):
    solver = z3.Solver()
    values = [
        [z3.Int(f"v_{i}_{g}") for g in range(M)] for i in range(N)
    ]
    for row in values:
        for value in row:
            solver.add(value >= 1, value <= K)
    for i in range(N - 1):
        solver.add(lex_ge(values[i], values[i + 1]))
    for g in range(M - 1):
        solver.add(
            lex_ge(
                [values[i][g] for i in range(N)],
                [values[i][g + 1] for i in range(N)],
            )
        )
    survivors = []
    for assign in pool:
        bundles = [[] for _ in range(N)]
        for g, owner in enumerate(assign):
            bundles[owner].append(g)
        conditions = []
        for g, owner in enumerate(assign):
            for observer in range(N):
                if observer == owner:
                    continue
                conditions.append(
                    total(values[observer][h] for h in bundles[observer])
                    >= total(
                        values[observer][h]
                        for h in bundles[owner]
                        if h != g
                    )
                )
        survivors.append(z3.And(*conditions))
    solver.add(z3.Sum(*[z3.If(alive, 1, 0) for alive in survivors]) <= SLOTS)
    return solver, values, None


def exactly_one(solver, variables):
    solver.add(z3.PbEq([(variable, 1) for variable in variables], 1))


def pb_ge(terms, bound):
    return z3.PbGe(terms, bound) if terms else z3.BoolVal(0 >= bound)


def pb_le(terms, bound):
    return z3.PbLe(terms, bound) if terms else z3.BoolVal(0 <= bound)


def fd_equal(left, right):
    return z3.Or(*[z3.And(x, y) for x, y in zip(left, right)])


def fd_greater(left, right):
    return z3.Or(
        *[
            z3.And(left[x], right[y])
            for x in range(len(left))
            for y in range(x)
        ]
    )


def fd_lex_ge(xs, ys):
    greater_at = []
    for index in range(len(xs)):
        greater_at.append(
            z3.And(
                *[
                    fd_equal(xs[prefix], ys[prefix])
                    for prefix in range(index)
                ],
                fd_greater(xs[index], ys[index]),
            )
        )
    return z3.Or(
        *greater_at,
        z3.And(*[fd_equal(x, y) for x, y in zip(xs, ys)]),
    )


def build_pb_master(K, pool):
    solver = z3.SolverFor("QF_FD")
    values = [
        [
            [z3.Bool(f"v_{i}_{g}_{value}") for value in range(1, K + 1)]
            for g in range(M)
        ]
        for i in range(N)
    ]
    slots = [
        [
            [z3.Bool(f"slot_{t}_{g}_{owner}") for owner in range(N)]
            for g in range(M)
        ]
        for t in range(SLOTS)
    ]
    for row in values:
        for value in row:
            exactly_one(solver, value)
    for slot in slots:
        for owner in slot:
            exactly_one(solver, owner)
    for i in range(N - 1):
        solver.add(fd_lex_ge(values[i], values[i + 1]))
    for g in range(M - 1):
        solver.add(
            fd_lex_ge(
                [values[i][g] for i in range(N)],
                [values[i][g + 1] for i in range(N)],
            )
        )

    for assign in pool:
        bundles = [[] for _ in range(N)]
        for g, owner in enumerate(assign):
            bundles[owner].append(g)
        disjuncts = []
        for g, owner in enumerate(assign):
            for observer in range(N):
                if observer == owner:
                    continue
                terms = []
                for h in bundles[owner]:
                    if h != g:
                        terms.extend(
                            (values[observer][h][value - 1], value)
                            for value in range(1, K + 1)
                        )
                for h in bundles[observer]:
                    terms.extend(
                        (values[observer][h][value - 1], -value)
                        for value in range(1, K + 1)
                    )
                disjuncts.append(pb_ge(terms, 1))
        for slot in slots:
            disjuncts.append(
                z3.And(
                    *[slot[g][owner] for g, owner in enumerate(assign)]
                )
            )
        solver.add(z3.Or(*disjuncts))
    return solver, values, slots


def build_pb_cardinality_master(K, pool):
    solver = z3.SolverFor("QF_FD")
    values = [
        [
            [z3.Bool(f"v_{i}_{g}_{value}") for value in range(1, K + 1)]
            for g in range(M)
        ]
        for i in range(N)
    ]
    for row in values:
        for value in row:
            exactly_one(solver, value)
    for i in range(N - 1):
        solver.add(fd_lex_ge(values[i], values[i + 1]))
    for g in range(M - 1):
        solver.add(
            fd_lex_ge(
                [values[i][g] for i in range(N)],
                [values[i][g + 1] for i in range(N)],
            )
        )
    survivors = []
    for assign in pool:
        bundles = [[] for _ in range(N)]
        for g, owner in enumerate(assign):
            bundles[owner].append(g)
        conditions = []
        for g, owner in enumerate(assign):
            for observer in range(N):
                if observer == owner:
                    continue
                terms = []
                for h in bundles[observer]:
                    terms.extend(
                        (values[observer][h][value - 1], value)
                        for value in range(1, K + 1)
                    )
                for h in bundles[owner]:
                    if h != g:
                        terms.extend(
                            (values[observer][h][value - 1], -value)
                            for value in range(1, K + 1)
                        )
                conditions.append(pb_ge(terms, 0))
        survivors.append(z3.And(*conditions))
    solver.add(pb_le([(alive, 1) for alive in survivors], SLOTS))
    return solver, values, None


def model_matrix(model, variables):
    return [
        [model.eval(value, model_completion=True).as_long() for value in row]
        for row in variables
    ]


def model_one_hot_matrix(model, variables):
    return [
        [
            next(
                index
                for index, variable in enumerate(domain)
                if z3.is_true(model.eval(variable, model_completion=True))
            )
            for domain in row
        ]
        for row in variables
    ]


def run(args):
    raw, pool = load_pool(args.pool)
    started = time.time()
    if args.encoding == "pb" and args.formulation == "cardinality":
        solver, values, slots = build_pb_cardinality_master(args.K, pool)
    elif args.encoding == "pb":
        solver, values, slots = build_pb_master(args.K, pool)
    elif args.formulation == "cardinality":
        solver, values, slots = build_lia_cardinality_master(args.K, pool)
    else:
        solver, values, slots = build_lia_master(args.K, pool)
    if args.timeout_ms:
        solver.set(timeout=args.timeout_ms)
    if args.threads:
        solver.set(threads=args.threads)
    export_hash = None
    if args.export:
        args.export.parent.mkdir(parents=True, exist_ok=True)
        args.export.write_text(solver.to_smt2())
        export_hash = sha256(args.export)
    status = solver.check()
    result = {
        "schema": 1,
        "status": str(status).upper(),
        "encoding": (
            "independent Z3 finite-domain pseudo-Boolean re-encoding"
            if args.encoding == "pb"
            else "independent Z3 QF_LIA re-encoding"
        ),
        "formulation": args.formulation,
        "threads": args.threads,
        "K": args.K,
        "raw_pool_size": len(raw),
        "unique_pool_size": len(pool),
        "duplicates_dropped": len(raw) - len(pool),
        "pool_sha256": sha256(args.pool),
        "seconds": round(time.time() - started, 3),
        "command": " ".join(sys.argv),
        "environment": {
            "python": platform.python_version(),
            "z3": z3.get_version_string(),
            "platform": platform.platform(),
        },
    }
    if args.export:
        result["smt2_path"] = str(args.export)
        result["smt2_sha256"] = export_hash
    if status == z3.sat:
        model = solver.model()
        if args.encoding == "pb":
            result["values"] = [
                [value + 1 for value in row]
                for row in model_one_hot_matrix(model, values)
            ]
            if slots is not None:
                result["slots"] = model_one_hot_matrix(model, slots)
        else:
            result["values"] = model_matrix(model, values)
            if slots is not None:
                result["slots"] = model_matrix(model, slots)
    if status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    if args.result_out:
        args.result_out.parent.mkdir(parents=True, exist_ok=True)
        args.result_out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if args.expect and str(status) != args.expect:
        return 1
    return 0 if status != z3.unknown else 2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pool",
        type=Path,
        default=ROOT / "results/countpool_K4_complete.json",
    )
    parser.add_argument("--K", type=int, default=4, choices=[4])
    parser.add_argument("--encoding", choices=["pb", "lia"], default="pb")
    parser.add_argument(
        "--formulation",
        choices=["cardinality", "slots"],
        default="cardinality",
    )
    parser.add_argument("--timeout-ms", type=int, default=0)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--export", type=Path)
    parser.add_argument("--result-out", type=Path)
    parser.add_argument("--expect", choices=["sat", "unsat", "unknown"])
    args = parser.parse_args()
    if args.threads < 1 or args.timeout_ms < 0:
        parser.error("threads must be positive and timeout-ms nonnegative")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
