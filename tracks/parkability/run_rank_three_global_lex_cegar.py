#!/usr/bin/env python3
"""Search an exact global-lex witness for the minimal rank-three gate."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import z3


OWNERS = ("r", "q", "c", "s")
RECIPIENTS = (*OWNERS, "charity")
GOODS = (
    "r0", "r1", "q0", "q1", "q2",
    "c0", "c1", "c2", "c3", "s0", "f",
)
BASE = {
    "r": ("r0", "r1"),
    "q": ("q0", "q1", "q2"),
    "c": ("c0", "c1", "c2", "c3"),
    "s": ("s0",),
    "charity": ("f",),
}
CURRENT = {
    "r": ("c1", "c2", "f"),
    "q": ("q0", "r0", "c0"),
    "c": ("q1",),
    "s": ("s0", "q2"),
    "charity": ("r1", "c3"),
}
EXPECTED_WALLS = {
    ("r", "q"),
    ("q", "charity"),
    ("c", "q"),
    ("s", "r"),
}


def total(value, observer, goods):
    return z3.Sum(*(value[good, observer] for good in goods))


def tail(value, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return z3.RealVal(0)
    entries = [value[good, observer] for good in goods]
    minimum = entries[0]
    for entry in entries[1:]:
        minimum = z3.If(minimum <= entry, minimum, entry)
    return z3.Sum(*entries) - minimum


def lex_improves(utilities):
    clauses = []
    for position, owner in enumerate(OWNERS):
        clauses.append(z3.And(
            *(utilities[OWNERS[index]] == 1 for index in range(position)),
            utilities[owner] > 1,
        ))
    return z3.Or(*clauses)


def improvement_formula(utilities, root_only):
    return utilities["r"] > 1 if root_only else lex_improves(utilities)


def endpoint_formula(allocation, value, root_only):
    utility = {
        observer: total(value, observer, allocation[observer])
        for observer in OWNERS
    }
    conditions = [improvement_formula(utility, root_only), bool(allocation["charity"])]
    for observer in OWNERS:
        for target in OWNERS:
            if target != observer:
                conditions.append(
                    utility[observer] >= tail(value, observer, allocation[target])
                )
        conditions.append(
            utility[observer] >= total(value, observer, allocation["charity"])
        )
    return z3.And(*conditions)


def build_master():
    value = {
        (good, observer): z3.Real(f"v_{good}_{observer}")
        for good in GOODS for observer in OWNERS
    }
    solver = z3.SolverFor("QF_LRA")
    for variable in value.values():
        solver.add(variable > 0, variable < 4)
    for observer in OWNERS:
        solver.add(total(value, observer, BASE[observer]) == 1)
        solver.add(total(value, observer, BASE["charity"]) <= 1)
        for target in OWNERS:
            if target != observer:
                solver.add(tail(value, observer, BASE[target]) <= 1)

    current_utility = {
        observer: total(value, observer, CURRENT[observer])
        for observer in OWNERS
    }
    solver.add(current_utility["r"] > 1)
    solver.add(current_utility["q"] >= 1)
    solver.add(current_utility["s"] > 1)
    solver.add(current_utility["c"] < 1)

    for observer in OWNERS:
        for target in RECIPIENTS:
            if target == observer:
                continue
            threshold = (
                total(value, observer, CURRENT["charity"])
                if target == "charity"
                else tail(value, observer, CURRENT[target])
            )
            if (observer, target) in EXPECTED_WALLS:
                solver.add(threshold > current_utility[observer])
            else:
                solver.add(threshold <= current_utility[observer])
    return solver, value


def fractions(model, value):
    return {
        observer: {
            good: Fraction(str(model.eval(value[good, observer], model_completion=True)))
            for good in GOODS
        }
        for observer in OWNERS
    }


def oracle(values, root_only, minimize_moves):
    holder = {good: z3.Int(f"holder_{good}") for good in GOODS}
    solver = z3.Optimize() if minimize_moves else z3.Solver()
    for variable in holder.values():
        solver.add(variable >= 0, variable < len(RECIPIENTS))
    solver.add(z3.Or(*(holder[good] == 4 for good in GOODS)))

    utility = {}
    for observer in OWNERS:
        for recipient_index, recipient in enumerate(RECIPIENTS):
            utility[observer, recipient] = z3.Sum(*(
                z3.If(
                    holder[good] == recipient_index,
                    z3.RealVal(str(values[observer][good])),
                    0,
                )
                for good in GOODS
            ))

    own = {observer: utility[observer, observer] for observer in OWNERS}
    solver.add(improvement_formula(own, root_only))
    for observer in OWNERS:
        for target_index, target in enumerate(OWNERS):
            if target == observer:
                continue
            for good in GOODS:
                solver.add(z3.Implies(
                    holder[good] == target_index,
                    own[observer]
                    >= utility[observer, target]
                    - z3.RealVal(str(values[observer][good])),
                ))
        solver.add(own[observer] >= utility[observer, "charity"])

    if minimize_moves:
        current_holder = {
            good: RECIPIENTS.index(recipient)
            for recipient, goods in CURRENT.items()
            for good in goods
        }
        solver.minimize(z3.Sum(*(
            z3.If(holder[good] == current_holder[good], 0, 1)
            for good in GOODS
        )))

    if solver.check() != z3.sat:
        return None
    model = solver.model()
    allocation = {recipient: [] for recipient in RECIPIENTS}
    for good in GOODS:
        index = model.eval(holder[good], model_completion=True).as_long()
        allocation[RECIPIENTS[index]].append(good)
    for goods in allocation.values():
        goods.sort()
    return allocation


def checkpoint(path: Path, result: dict) -> None:
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(
    output: Path,
    maximum_iterations: int,
    timeout_seconds: int,
    root_only: bool,
    resume: bool,
    minimize_moves: bool,
) -> dict:
    master, value = build_master()
    master.set(timeout=timeout_seconds * 1000)
    expected_schema = (
        "rank-three-global-root-cegar-v1"
        if root_only else "rank-three-global-lex-cegar-v1"
    )
    previous = None
    if resume and output.exists():
        previous = json.loads(output.read_text())
        if previous.get("schema") != expected_schema:
            raise ValueError("resume schema/mode mismatch")
        for record in previous.get("iterations", []):
            allocation = record.get("blocking_efx_lex_allocation")
            if allocation is not None:
                master.add(z3.Not(endpoint_formula(allocation, value, root_only)))
    iterations = list(previous.get("iterations", [])) if previous else []
    result = {
        "schema": expected_schema,
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "goods": list(GOODS),
        "base": {key: list(goods) for key, goods in BASE.items()},
        "current": {key: list(goods) for key, goods in CURRENT.items()},
        "expected_current_walls": [list(edge) for edge in sorted(EXPECTED_WALLS)],
        "iterations": iterations,
        "improvement_objective": "root-strict" if root_only else "full-lex",
        "oracle_policy": "minimum-moved-goods-from-current" if minimize_moves else "arbitrary",
        "claim_boundary": (
            "exact eleven-good global root-coordinate decision for one minimal "
            "rank-three two-hole response normal form; SAT would establish a "
            "root-maximal positive-additive local obstruction, not the complete "
            "fixed-U packet premises or an EFX counterexample"
            if root_only else
            "exact eleven-good global-lex decision for one minimal rank-three "
            "two-hole response normal form; SAT would establish a globally "
            "lex-maximal positive-additive local obstruction, not the complete "
            "fixed-U packet premises or an EFX counterexample"
        ),
    }
    checkpoint(output, result)
    start = len(iterations)
    for iteration in range(start, maximum_iterations):
        status = master.check()
        record = {"iteration": iteration, "master_status": str(status)}
        iterations.append(record)
        if status != z3.sat:
            result["status"] = str(status)
            if status == z3.unknown:
                result["reason_unknown"] = master.reason_unknown()
            checkpoint(output, result)
            return result
        model = master.model()
        values = fractions(model, value)
        escape = oracle(values, root_only, minimize_moves)
        if escape is None:
            result["status"] = "sat_global_lex_obstruction"
            result["countermodel_iteration"] = iteration
            result["values"] = {
                observer: {good: str(amount) for good, amount in row.items()}
                for observer, row in values.items()
            }
            checkpoint(output, result)
            return result
        record["blocking_efx_lex_allocation"] = escape
        master.add(z3.Not(endpoint_formula(escape, value, root_only)))
        checkpoint(output, result)
        print(json.dumps({"iteration": iteration, "escape": escape}), flush=True)
    result["status"] = "iteration_limit"
    checkpoint(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=1000)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--root-only", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--minimize-moves", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output,
        args.maximum_iterations,
        args.timeout_seconds,
        args.root_only,
        args.resume,
        args.minimize_moves,
    )
    print(json.dumps({"status": result["status"], "iterations": len(result["iterations"])}, indent=2))


if __name__ == "__main__":
    main()
