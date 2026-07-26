#!/usr/bin/env python3
"""Exact-real protected-slot counting CEGAR for the positive 4x7 cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import shlex
import sys
import tempfile
import time
import uuid
from fractions import Fraction
from pathlib import Path

import z3


N, M, SLOTS = 4, 7, 3
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from verify import (  # noqa: E402
    check_allocation,
    enumerate_all,
    masks_from_assign,
    precompute,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write(value)
        os.replace(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise


def validate_pool(raw: object) -> list[list[int]]:
    if not isinstance(raw, list):
        raise ValueError("pool must be a JSON list")
    unique: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for index, assignment in enumerate(raw):
        if (
            not isinstance(assignment, list)
            or len(assignment) != M
            or any(
                type(owner) is not int or not 0 <= owner < N
                for owner in assignment
            )
        ):
            raise ValueError(f"invalid allocation at pool index {index}")
        key = tuple(assignment)
        if key not in seen:
            seen.add(key)
            unique.append(assignment)
    return unique


def load_pool(path: Path) -> tuple[list[list[int]], str]:
    contents = path.read_bytes()
    pool = validate_pool(json.loads(contents))
    return pool, hashlib.sha256(contents).hexdigest()


def load_trace_state(path: Path) -> tuple[int, int | None, str | None]:
    if not path.exists():
        return 0, None, None
    records = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"invalid trace JSON at {path}:{line_number}"
            ) from error
        if (
            not isinstance(record, dict)
            or type(record.get("pool_size")) is not int
            or not isinstance(record.get("pool_sha256"), str)
        ):
            raise ValueError(f"invalid trace record at {path}:{line_number}")
        records.append(record)
    if not records:
        return 0, None, None
    return (
        len(records),
        records[-1]["pool_size"],
        records[-1]["pool_sha256"],
    )


def bundles_of(assignment: list[int]) -> list[list[int]]:
    bundles = [[] for _ in range(N)]
    for good, owner in enumerate(assignment):
        bundles[owner].append(good)
    return bundles


def total(terms) -> z3.ArithRef:
    terms = list(terms)
    return z3.Sum(terms) if terms else z3.RealVal(0)


def lex_margin_ge(xs, ys) -> z3.BoolRef:
    """Lexicographic xs >= ys with every strict first difference at least one."""
    if len(xs) != len(ys) or not xs:
        raise ValueError("lexicographic sequences must have equal positive length")
    branches = []
    for index in range(len(xs)):
        branches.append(
            z3.And(
                *[xs[prefix] == ys[prefix] for prefix in range(index)],
                xs[index] >= ys[index] + 1,
            )
        )
    return z3.Or(
        z3.And(*[left == right for left, right in zip(xs, ys)]),
        *branches,
    )


def add_exactly_one(solver: z3.Solver, literals: list[z3.BoolRef]) -> None:
    solver.add(z3.Or(*literals))
    for left in range(len(literals)):
        for right in range(left + 1, len(literals)):
            solver.add(z3.Or(z3.Not(literals[left]), z3.Not(literals[right])))


def as_fraction(value: z3.RatNumRef) -> Fraction:
    if not z3.is_rational_value(value):
        raise ValueError(f"expected rational model value, got {value}")
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def primitive_integer_row(row: list[Fraction]) -> list[int]:
    denominator = 1
    for value in row:
        denominator = math.lcm(denominator, value.denominator)
    integers = [value.numerator * (denominator // value.denominator) for value in row]
    divisor = 0
    for value in integers:
        divisor = math.gcd(divisor, abs(value))
    divisor = max(divisor, 1)
    return [value // divisor for value in integers]


class RealCountingMaster:
    """Incremental exact QF_LRA master with slots or pooled cardinality."""

    def __init__(
        self,
        *,
        formulation: str = "slots",
        symmetry: bool = True,
        fixed_values: list[list[int]] | None = None,
    ):
        if formulation not in {"slots", "cardinality"}:
            raise ValueError("formulation must be slots or cardinality")
        self.formulation = formulation
        self.symmetry = symmetry
        self.solver = z3.SolverFor("QF_LRA")
        self.values = [
            [z3.Real(f"x_{observer}_{good}") for good in range(M)]
            for observer in range(N)
        ]
        self.row_total = z3.Real("row_total")
        self.solver.add(self.row_total >= M)
        for row in self.values:
            for value in row:
                self.solver.add(value >= 1)
            self.solver.add(z3.Sum(row) == self.row_total)

        if symmetry:
            for observer in range(N - 1):
                self.solver.add(
                    lex_margin_ge(
                        self.values[observer], self.values[observer + 1]
                    )
                )
            for good in range(M - 1):
                self.solver.add(
                    lex_margin_ge(
                        [self.values[observer][good] for observer in range(N)],
                        [
                            self.values[observer][good + 1]
                            for observer in range(N)
                        ],
                    )
                )

        self.slots = None
        if formulation == "slots":
            self.slots = [
                [
                    [
                        z3.Bool(
                            f"slot_{slot}_{good}_owner_{owner}"
                        )
                        for owner in range(N)
                    ]
                    for good in range(M)
                ]
                for slot in range(SLOTS)
            ]
            for slot in self.slots:
                for owners in slot:
                    add_exactly_one(self.solver, owners)

        if fixed_values is not None:
            self._fix_semantic_values(fixed_values)

        self.pool: list[list[int]] = []
        self.known: set[tuple[int, ...]] = set()
        self.alive: list[z3.BoolRef] = []

    def _fix_semantic_values(self, fixed_values: list[list[int]]) -> None:
        if (
            not isinstance(fixed_values, list)
            or len(fixed_values) != N
            or any(
                not isinstance(row, list) or len(row) != M
                for row in fixed_values
            )
            or any(
                type(value) is not int or value <= 0
                for row in fixed_values
                for value in row
            )
        ):
            raise ValueError("fixed values must be a positive 4x7 integer matrix")
        for observer, row in enumerate(fixed_values):
            row_sum = sum(row)
            for good, value in enumerate(row):
                self.solver.add(
                    row_sum * self.values[observer][good]
                    == value * self.row_total
                )

    def efx_conditions(self, assignment: list[int]) -> list[z3.BoolRef]:
        bundles = bundles_of(assignment)
        conditions = []
        for removed_good, owner in enumerate(assignment):
            target_remainder = [
                good
                for good in bundles[owner]
                if good != removed_good
            ]
            for observer in range(N):
                if observer == owner:
                    continue
                own = total(
                    self.values[observer][good]
                    for good in bundles[observer]
                )
                target = total(
                    self.values[observer][good]
                    for good in target_remainder
                )
                conditions.append(own >= target)
        return conditions

    def add_allocation(self, assignment: list[int]) -> bool:
        validate_pool([assignment])
        key = tuple(assignment)
        if key in self.known:
            return False
        self.known.add(key)
        allocation_index = len(self.pool)
        stored_assignment = list(assignment)
        self.pool.append(stored_assignment)
        bundles = bundles_of(stored_assignment)

        if self.formulation == "cardinality":
            alive = z3.Bool(f"pool_{allocation_index}_is_efx0")
            self.solver.add(
                alive == z3.And(*self.efx_conditions(stored_assignment))
            )
            self.alive.append(alive)
            if len(self.alive) > SLOTS:
                self.solver.add(z3.AtMost(*self.alive, SLOTS))
            return True

        disjuncts = []
        for removed_good, owner in enumerate(assignment):
            target_remainder = [
                good
                for good in bundles[owner]
                if good != removed_good
            ]
            for observer in range(N):
                if observer == owner:
                    continue
                violation = z3.Bool(
                    f"pool_{allocation_index}_remove_{removed_good}"
                    f"_observer_{observer}_strong_envy"
                )
                own = total(
                    self.values[observer][good]
                    for good in bundles[observer]
                )
                target = total(
                    self.values[observer][good]
                    for good in target_remainder
                )
                self.solver.add(z3.Implies(violation, target - own >= 1))
                disjuncts.append(violation)

        assert self.slots is not None
        for slot_index, slot in enumerate(self.slots):
            match = z3.Bool(
                f"pool_{allocation_index}_matches_slot_{slot_index}"
            )
            self.solver.add(
                z3.Implies(
                    match,
                    z3.And(
                        *[
                            slot[good][owner]
                            for good, owner in enumerate(stored_assignment)
                        ]
                    ),
                )
            )
            disjuncts.append(match)
        self.solver.add(z3.Or(*disjuncts))
        return True

    def decode_integer_values(self, model: z3.ModelRef) -> list[list[int]]:
        rational_rows = [
            [
                as_fraction(model.eval(value, model_completion=True))
                for value in row
            ]
            for row in self.values
        ]
        if any(value <= 0 for row in rational_rows for value in row):
            raise ValueError("model contains a nonpositive value")
        return [primitive_integer_row(row) for row in rational_rows]

    def model_record(self, model: z3.ModelRef) -> dict:
        return {
            "row_total": str(
                model.eval(self.row_total, model_completion=True)
            ),
            "integer_values": self.decode_integer_values(model),
        }


def run(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    invocation_id = uuid.uuid4().hex
    source_pool = (
        args.pool_out
        if args.resume and args.pool_out.exists()
        else args.seed_pool
    )
    pool, source_hash = load_pool(source_pool)
    trace_offset = 0
    if args.resume:
        trace_offset, trace_pool_size, trace_pool_hash = load_trace_state(
            args.trace_out
        )
        if trace_pool_size is not None and (
            trace_pool_size != len(pool) or trace_pool_hash != source_hash
        ):
            raise ValueError(
                "resume trace does not end at the selected source pool"
            )
    atomic_json(args.pool_out, pool)
    if not args.resume:
        atomic_text(args.trace_out, "")

    master = RealCountingMaster(
        formulation=args.formulation,
        symmetry=not args.no_symmetry,
    )
    for assignment in pool:
        master.add_allocation(assignment)
    if args.timeout_ms:
        master.solver.set(timeout=args.timeout_ms)

    if args.export:
        atomic_text(args.export, master.solver.to_smt2())

    known = {tuple(assignment) for assignment in pool}
    rounds = 0
    while args.max_rounds == 0 or rounds < args.max_rounds:
        rounds += 1
        check_started = time.perf_counter()
        status = master.solver.check()
        check_seconds = time.perf_counter() - check_started

        base_record = {
            "schema": 1,
            "status": str(status).upper(),
            "claim": (
                "every positive-real 4x7 additive valuation matrix has "
                "at least four EFX0 allocations"
            ),
            "formulation": args.formulation,
            "symmetry": not args.no_symmetry,
            "source_pool": str(source_pool),
            "source_pool_sha256": source_hash,
            "checked_pool_size": len(pool),
            "checked_pool_sha256": sha256(args.pool_out),
            "pool_path": str(args.pool_out),
            "pool_size": len(pool),
            "pool_sha256": sha256(args.pool_out),
            "cuts_added_after_last_check": 0,
            "export_formula_checked": bool(args.export),
            "export_formula_stage": "checked_pool" if args.export else None,
            "rounds_this_invocation": rounds,
            "prior_trace_records": trace_offset,
            "invocation_id": invocation_id,
            "last_check_seconds": round(check_seconds, 6),
            "seconds_this_invocation": round(
                time.perf_counter() - started, 6
            ),
            "command": shlex.join(sys.argv),
            "environment": {
                "python": platform.python_version(),
                "z3": z3.get_version_string(),
                "platform": platform.platform(),
            },
        }

        if status == z3.unsat:
            base_record["status"] = "UNSAT"
            if args.export:
                atomic_text(args.export, master.solver.to_smt2())
            atomic_json(args.result_out, base_record)
            print(json.dumps(base_record, indent=2), flush=True)
            return 0
        if status == z3.unknown:
            base_record["status"] = "UNKNOWN"
            base_record["reason_unknown"] = master.solver.reason_unknown()
            if args.export:
                atomic_text(args.export, master.solver.to_smt2())
            atomic_json(args.result_out, base_record)
            print(json.dumps(base_record, indent=2), flush=True)
            return 2

        model = master.solver.model()
        values = master.decode_integer_values(model)
        val, minall, minpos = precompute(N, M, values)
        pooled_survivors = sum(
            check_allocation(
                N,
                masks_from_assign(N, assignment),
                val,
                minall,
                minpos,
            )[0]
            for assignment in pool
        )
        if pooled_survivors > SLOTS:
            raise RuntimeError(
                "decoded model has more than three pooled EFX0 allocations"
            )
        checked = enumerate_all(N, M, values, collect=args.add)
        count = checked["efx0_count"]
        candidate = {
            **master.model_record(model),
            "efx0_count": count,
            "pooled_efx0_count": pooled_survivors,
        }
        if count <= SLOTS:
            base_record["status"] = "WITNESS"
            base_record["candidate"] = candidate
            if args.export:
                atomic_text(args.export, master.solver.to_smt2())
            atomic_json(args.result_out, base_record)
            print(json.dumps(base_record, indent=2), flush=True)
            return 1

        additions = []
        for assignment in checked["examples_efx0"]:
            key = tuple(assignment)
            if key not in known:
                known.add(key)
                additions.append(assignment)
        if not additions:
            raise RuntimeError("SAT master produced no fresh EFX0 allocation")
        for assignment in additions:
            pool.append(assignment)
            master.add_allocation(assignment)
        atomic_json(args.pool_out, pool)
        trace_record = {
            "round": rounds,
            "invocation_id": invocation_id,
            "invocation_round": rounds,
            "cumulative_round": trace_offset + rounds,
            "checked_pool_size": base_record["checked_pool_size"],
            "checked_pool_sha256": base_record["checked_pool_sha256"],
            "check_seconds": round(check_seconds, 6),
            "candidate": candidate,
            "added": additions,
            "pool_size": len(pool),
            "pool_sha256": sha256(args.pool_out),
        }
        args.trace_out.parent.mkdir(parents=True, exist_ok=True)
        with args.trace_out.open("a") as stream:
            stream.write(json.dumps(trace_record, separators=(",", ":")) + "\n")
        print(json.dumps({"event": "cut", **trace_record}), flush=True)

    result = {
        **base_record,
        "status": "CHECKPOINT",
        "pool_size": len(pool),
        "pool_sha256": sha256(args.pool_out),
        "cuts_added_after_last_check": len(additions),
        "export_formula_checked": False if args.export else None,
        "export_formula_stage": "post_cut_pool" if args.export else None,
        "rounds_this_invocation": rounds,
        "seconds_this_invocation": round(
            time.perf_counter() - started, 6
        ),
        "command": shlex.join(sys.argv),
        "trace_path": str(args.trace_out),
        "export_path": str(args.export) if args.export else None,
        "last_candidate": candidate,
    }
    if args.export:
        atomic_text(args.export, master.solver.to_smt2())
    atomic_json(args.result_out, result)
    print(json.dumps(result, indent=2), flush=True)
    return 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed-pool",
        type=Path,
        default=ROOT / "results/countpool_K4_complete.json",
    )
    parser.add_argument(
        "--pool-out",
        type=Path,
        default=ROOT / "results/countpool_real_4x7.json",
    )
    parser.add_argument(
        "--result-out",
        type=Path,
        default=ROOT / "results/countcegar_real_4x7.json",
    )
    parser.add_argument(
        "--trace-out",
        type=Path,
        default=ROOT / "results/countcegar_real_4x7.jsonl",
    )
    parser.add_argument("--export", type=Path)
    parser.add_argument(
        "--formulation",
        choices=["slots", "cardinality"],
        default="slots",
    )
    parser.add_argument("--add", type=int, default=16)
    parser.add_argument("--timeout-ms", type=int, default=300000)
    parser.add_argument("--max-rounds", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--no-symmetry", action="store_true")
    args = parser.parse_args()
    if args.add < SLOTS + 1:
        parser.error("add must be at least four")
    if args.timeout_ms < 0 or args.max_rounds < 0:
        parser.error("timeouts and round limits must be nonnegative")
    resolved = [
        args.seed_pool.resolve(),
        args.pool_out.resolve(),
        args.result_out.resolve(),
        args.trace_out.resolve(),
    ]
    if args.export:
        resolved.append(args.export.resolve())
    if len(set(resolved)) != len(resolved):
        parser.error("seed, output, trace, result, and export paths must differ")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
