#!/usr/bin/env python3
"""Exact CEGAR for a globally lex-max alternating 2+2+1+1 EFX atom."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import z3


SCHEMA = "alternating-global-lex-cegar-v1"
POOL_SCHEMA = "alternating-global-lex-rival-pool-v1"
N = 4
M = 7
AGENTS = ("p", "r", "s", "q")
GOODS = ("tr", "br", "tq", "bq", "x", "y", "f")
BASE_OWNER = (1, 1, 3, 3, 0, 2, None)
BASE_BUNDLES = ((4,), (0, 1), (5,), (2, 3))
EXPECTED_ENVY = {(1, 2), (3, 0)}
EXPECTED_DESIRED = {
    (0, 1): {(0, 6)},
    (1, 2): {(5,)},
    (2, 3): {(2, 6)},
    (3, 0): {(4,)},
}
V_STAR = (
    (5002, 1008, 4004, 1016, 10064, 1032, 6001),
    (9001, 1064, 1004, 1008, 1016, 11032, 1002),
    (4004, 1008, 5002, 1016, 1032, 10064, 6001),
    (1004, 1008, 9001, 1064, 11032, 1016, 1002),
)


Owner = tuple[int | None, ...]


def atomic_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def bundles(owner: Owner) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(N)
    )


def subset_sum(
    values: tuple[tuple[z3.ArithRef, ...], ...],
    observer: int,
    goods: tuple[int, ...],
) -> z3.ArithRef:
    if not goods:
        return z3.RealVal(0)
    return z3.Sum(*(values[observer][good] for good in goods))


def desired_expression(
    values: tuple[tuple[z3.ArithRef, ...], ...],
    own: tuple[z3.ArithRef, ...],
    source: int,
    candidate: tuple[int, ...],
) -> z3.BoolRef:
    return z3.And(
        subset_sum(values, source, candidate) > own[source],
        *(
            own[observer]
            >= subset_sum(
                values,
                observer,
                tuple(good for good in candidate if good != removed),
            )
            for observer in range(N)
            for removed in candidate
        ),
    )


def lex_gt(
    left: tuple[z3.ArithRef, ...],
    right: tuple[z3.ArithRef, ...],
    order: tuple[int, ...],
) -> z3.BoolRef:
    return z3.Or(
        *(
            z3.And(
                *(left[order[prefix]] == right[order[prefix]] for prefix in range(index)),
                left[agent] > right[agent],
            )
            for index, agent in enumerate(order)
        )
    )


def structural_solver() -> tuple[
    z3.Solver,
    tuple[tuple[z3.ArithRef, ...], ...],
    tuple[z3.ArithRef, ...],
]:
    values = tuple(
        tuple(z3.Real(f"v_{agent}_{good}") for good in range(M))
        for agent in range(N)
    )
    own = tuple(
        subset_sum(values, agent, BASE_BUNDLES[agent]) for agent in range(N)
    )
    solver = z3.SolverFor("QF_LRA")
    for agent in range(N):
        solver.add(*(entry > 0 for entry in values[agent]))
        solver.add(z3.Sum(*values[agent]) == 1)

    for observer in range(N):
        solver.add(own[observer] > values[observer][6])
        for target in range(N):
            if observer != target:
                comparison = subset_sum(values, observer, BASE_BUNDLES[target])
                if (observer, target) in EXPECTED_ENVY:
                    solver.add(comparison > own[observer])
                else:
                    solver.add(own[observer] > comparison)
            for removed in BASE_BUNDLES[target]:
                remainder = tuple(
                    good for good in BASE_BUNDLES[target] if good != removed
                )
                solver.add(
                    own[observer] > subset_sum(values, observer, remainder)
                )

    for source in range(N):
        for target in range(N):
            offer = BASE_BUNDLES[target] + (6,)
            expected = EXPECTED_DESIRED.get((source, target), set())
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    relation = desired_expression(values, own, source, candidate)
                    if candidate in expected:
                        solver.add(relation)
                    elif not expected or candidate == offer:
                        solver.add(z3.Not(relation))

    compatible_families = (
        (1, 3, 1),
        (2, 3, 1),
        (3, 1, 3),
        (0, 1, 3),
    )
    for source, target, incoming_good in compatible_families:
        target_bundle = BASE_BUNDLES[target]
        for use_incoming in (False, True):
            for release_size in range(len(target_bundle) + 1):
                for release in itertools.combinations(target_bundle, release_size):
                    offer = tuple(
                        good for good in target_bundle if good not in release
                    ) + ((incoming_good,) if use_incoming else ())
                    for size in range(1, len(offer) + 1):
                        for candidate in itertools.combinations(offer, size):
                            solver.add(
                                z3.Not(
                                    desired_expression(
                                        values,
                                        own,
                                        source,
                                        candidate,
                                    )
                                )
                            )

    return solver, values, own


def rival_utilities_symbolic(
    values: tuple[tuple[z3.ArithRef, ...], ...], owner: Owner
) -> tuple[z3.ArithRef, ...]:
    rival_bundles = bundles(owner)
    return tuple(
        subset_sum(values, agent, rival_bundles[agent]) for agent in range(N)
    )


def rival_blocker(
    values: tuple[tuple[z3.ArithRef, ...], ...],
    base_own: tuple[z3.ArithRef, ...],
    owner: Owner,
    order: tuple[int, ...],
) -> z3.BoolRef:
    rival_bundles = bundles(owner)
    rival_own = rival_utilities_symbolic(values, owner)
    efx_failures = tuple(
        rival_own[observer]
        < subset_sum(
            values,
            observer,
            tuple(good for good in rival_bundles[target] if good != removed),
        )
        for observer in range(N)
        for target in range(N)
        for removed in rival_bundles[target]
    )
    return z3.Or(*efx_failures, z3.Not(lex_gt(rival_own, base_own, order)))


def rational(model: z3.ModelRef, expression: z3.ArithRef) -> Fraction:
    result = model.eval(expression, model_completion=True)
    if not z3.is_rational_value(result):
        raise TypeError(f"non-rational model value: {result}")
    return Fraction(result.numerator_as_long(), result.denominator_as_long())


def integerize_model(
    model: z3.ModelRef,
    symbolic: tuple[tuple[z3.ArithRef, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    rows = []
    for row in symbolic:
        fractions = tuple(rational(model, expression) for expression in row)
        denominator = math.lcm(*(entry.denominator for entry in fractions))
        integers = tuple(int(entry * denominator) for entry in fractions)
        divisor = math.gcd(*integers)
        rows.append(tuple(entry // divisor for entry in integers))
    return tuple(rows)


def numeric_utilities(
    values: tuple[tuple[int, ...], ...], owner: Owner
) -> tuple[int, ...]:
    assigned = bundles(owner)
    return tuple(
        sum(values[agent][good] for good in assigned[agent]) for agent in range(N)
    )


def numeric_efx(values: tuple[tuple[int, ...], ...], owner: Owner) -> bool:
    assigned = bundles(owner)
    own = numeric_utilities(values, owner)
    return all(
        own[observer]
        >= sum(
            values[observer][good]
            for good in assigned[target]
            if good != removed
        )
        for observer in range(N)
        for target in range(N)
        for removed in assigned[target]
    )


def all_owners() -> tuple[Owner, ...]:
    return tuple(
        tuple(None if assigned == N else assigned for assigned in raw)
        for raw in itertools.product(range(N + 1), repeat=M)
    )


ALL_OWNERS = all_owners()


def dominating_rivals(
    values: tuple[tuple[int, ...], ...], order: tuple[int, ...]
) -> tuple[list[tuple[tuple[int, ...], Owner]], int]:
    base_utility = numeric_utilities(values, BASE_OWNER)
    base_key = tuple(base_utility[agent] for agent in order)
    found = []
    efx_count = 0
    for owner in ALL_OWNERS:
        if not numeric_efx(values, owner):
            continue
        efx_count += 1
        utility = numeric_utilities(values, owner)
        key = tuple(utility[agent] for agent in order)
        if key > base_key:
            found.append((key, owner))
    found.sort(reverse=True, key=lambda record: (record[0], str(record[1])))
    return found, efx_count


def encode_owner(owner: Owner) -> list[int | None]:
    return list(owner)


def load_pool(path: Path, order: tuple[int, ...]) -> list[Owner]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("agent_order") != list(order)
        or payload.get("base_owner") != list(BASE_OWNER)
    ):
        raise ValueError("pool metadata mismatch")
    owners = [tuple(record) for record in payload["rivals"]]
    if len(owners) != len(set(owners)):
        raise ValueError("duplicate rival in pool")
    return owners


def save_pool(path: Path, order: tuple[int, ...], rivals: list[Owner]) -> None:
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "agent_order": list(order),
            "base_owner": list(BASE_OWNER),
            "rivals": [encode_owner(owner) for owner in rivals],
        },
    )


def run(
    order: tuple[int, ...],
    pool_path: Path,
    result_path: Path,
    max_iterations: int,
    add_per_iteration: int,
    timeout_seconds: int,
) -> dict:
    solver, values, base_own = structural_solver()
    solver.set(timeout=timeout_seconds * 1000)
    rivals = load_pool(pool_path, order)
    rival_set = set(rivals)

    seed_rivals, _ = dominating_rivals(V_STAR, order)
    for _, owner in seed_rivals:
        if owner not in rival_set:
            rivals.append(owner)
            rival_set.add(owner)
    save_pool(pool_path, order, rivals)
    for owner in rivals:
        solver.add(rival_blocker(values, base_own, owner, order))

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_STRUCTURAL_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values = integerize_model(solver.model(), values)
        found, efx_count = dominating_rivals(model_values, order)
        unseen = [owner for _, owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "efx_assignment_count": efx_count,
                "dominating_rival_count": len(found),
                "new_rival_count": len(unseen),
                "values": [list(row) for row in model_values],
            }
        )
        print(
            f"iteration={iteration} pool={len(rivals)} efx={efx_count} "
            f"dominating={len(found)} new={len(unseen)}",
            flush=True,
        )
        if not found:
            status = "SAT_GLOBAL_LEXMAX_ALTERNATING_ATOM"
            final_values = model_values
            break
        if not unseen:
            raise AssertionError("a pooled rival still dominates the model")
        for owner in unseen[:add_per_iteration]:
            solver.add(rival_blocker(values, base_own, owner, order))
            rivals.append(owner)
            rival_set.add(owner)
        save_pool(pool_path, order, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "claim_boundary": {
            "sat": "refutes the priority-sensitive alternating escape lemma in this exact seven-atom structural cell; does not refute complete EFX",
            "unsat": "closes only this seven-atom structural cell until a cap-free analytic core is proved",
        },
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "iterations": len(trace),
        "pool_size": len(rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason_unknown,
        "values": None if final_values is None else [list(row) for row in final_values],
        "trace": trace,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-order", default="0,1,2,3")
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=200)
    parser.add_argument("--add-per-iteration", type=int, default=64)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    order = tuple(int(field) for field in args.agent_order.split(","))
    if sorted(order) != list(range(N)):
        parser.error("agent order must be a permutation of 0,1,2,3")
    if args.result.exists():
        parser.error("result path must not exist")
    result = run(
        order,
        args.pool,
        args.result,
        args.max_iterations,
        args.add_per_iteration,
        args.timeout_seconds,
    )
    print(json.dumps({key: result[key] for key in ("status", "iterations", "pool_size", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
