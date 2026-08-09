#!/usr/bin/env python3
"""Exact global-lex CEGAR for two-good alternating top/bottom packets."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import AGENTS, atomic_json, lex_gt
except ImportError:
    from run_alternating_global_lex_cegar import AGENTS, atomic_json, lex_gt


SCHEMA = "alternating-split-packet-cegar-v1"
POOL_SCHEMA = "alternating-split-packet-rival-pool-v1"
N = 4
M = 11
GOODS = (
    "tr0", "tr1", "br0", "br1",
    "tq0", "tq1", "bq0", "bq1",
    "x", "y", "f",
)
BASE_OWNER = (1, 1, 1, 1, 3, 3, 3, 3, 0, 2, None)
BASE_BUNDLES = ((8,), (0, 1, 2, 3), (9,), (4, 5, 6, 7))
TOP_R = (0, 1)
BOTTOM_R = (2, 3)
TOP_Q = (4, 5)
BOTTOM_Q = (6, 7)
FLOATER = 10
EXPECTED_ENVY = {(1, 2), (3, 0)}
EXPECTED_DESIRED = {
    (0, 1): TOP_R + (FLOATER,),
    (1, 2): (9,),
    (2, 3): TOP_Q + (FLOATER,),
    (3, 0): (8,),
}
Owner = tuple[int | None, ...]


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


def structural_solver() -> tuple[
    z3.Solver,
    tuple[tuple[z3.ArithRef, ...], ...],
    tuple[z3.ArithRef, ...],
]:
    values = tuple(
        tuple(z3.Real(f"u_{agent}_{good}") for good in range(M))
        for agent in range(N)
    )
    own = tuple(
        subset_sum(values, agent, BASE_BUNDLES[agent]) for agent in range(N)
    )
    solver = z3.SolverFor("QF_LRA")
    for agent in range(N):
        solver.add(*(entry > 0 for entry in values[agent]))
        solver.add(z3.Sum(*values[agent]) == 1)
    # One global swap per packet can order the two goods for one reference
    # row.  Ordering them independently in every row would impose a false
    # comonotonicity restriction rather than break a genuine symmetry.
    solver.add(values[0][0] < values[0][1])
    solver.add(values[0][2] < values[0][3])
    solver.add(values[0][4] < values[0][5])
    solver.add(values[0][6] < values[0][7])

    for observer in range(N):
        solver.add(own[observer] > values[observer][FLOATER])
        for target in range(N):
            if observer != target:
                target_value = subset_sum(values, observer, BASE_BUNDLES[target])
                solver.add(
                    target_value > own[observer]
                    if (observer, target) in EXPECTED_ENVY
                    else own[observer] > target_value
                )
            for removed in BASE_BUNDLES[target]:
                solver.add(
                    own[observer]
                    > subset_sum(
                        values,
                        observer,
                        tuple(good for good in BASE_BUNDLES[target] if good != removed),
                    )
                )

    for source in range(N):
        for target in range(N):
            offer = BASE_BUNDLES[target] + (FLOATER,)
            expected = EXPECTED_DESIRED.get((source, target))
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    relation = desired_expression(values, own, source, candidate)
                    if candidate == expected:
                        solver.add(relation)
                    elif expected is None or candidate == offer:
                        solver.add(z3.Not(relation))

    compatible_families = (
        (1, 3, BOTTOM_R),
        (2, 3, BOTTOM_R),
        (3, 1, BOTTOM_Q),
        (0, 1, BOTTOM_Q),
    )
    for source, target, incoming in compatible_families:
        target_bundle = BASE_BUNDLES[target]
        for incoming_size in range(len(incoming) + 1):
            for incoming_subset in itertools.combinations(incoming, incoming_size):
                for release_size in range(len(target_bundle) + 1):
                    for release in itertools.combinations(target_bundle, release_size):
                        offer = tuple(
                            good for good in target_bundle if good not in release
                        ) + incoming_subset
                        for size in range(1, len(offer) + 1):
                            for candidate in itertools.combinations(offer, size):
                                solver.add(
                                    z3.Not(
                                        desired_expression(
                                            values, own, source, candidate
                                        )
                                    )
                                )

    return solver, values, own


def concrete_rival_blocker(
    values: tuple[tuple[z3.ArithRef, ...], ...],
    base_own: tuple[z3.ArithRef, ...],
    owner: Owner,
    order: tuple[int, ...],
) -> z3.BoolRef:
    assigned = bundles(owner)
    rival_own = tuple(
        subset_sum(values, agent, assigned[agent]) for agent in range(N)
    )
    failures = tuple(
        rival_own[observer]
        < subset_sum(
            values,
            observer,
            tuple(good for good in assigned[target] if good != removed),
        )
        for observer in range(N)
        for target in range(N)
        for removed in assigned[target]
    )
    return z3.Or(*failures, z3.Not(lex_gt(rival_own, base_own, order)))


def rational(model: z3.ModelRef, expression: z3.ArithRef) -> Fraction:
    result = model.eval(expression, model_completion=True)
    if not z3.is_rational_value(result):
        raise TypeError(result)
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


def numeric_utilities(values: tuple[tuple[int, ...], ...], owner: Owner) -> tuple[int, ...]:
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


def find_dominating_rivals(
    values: tuple[tuple[int, ...], ...],
    order: tuple[int, ...],
    timeout_seconds: int,
    limit: int,
) -> tuple[str, list[Owner], list[tuple[int, ...]], str | None]:
    owner = tuple(z3.Int(f"owner_{good}") for good in range(M))
    solver = z3.SolverFor("QF_LIA")
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(*(z3.And(variable >= 0, variable <= N) for variable in owner))
    utilities = tuple(
        z3.Sum(
            *(z3.If(owner[good] == agent, values[agent][good], 0) for good in range(M))
        )
        for agent in range(N)
    )
    target_values = tuple(
        tuple(
            z3.Sum(
                *(z3.If(owner[good] == target, values[observer][good], 0) for good in range(M))
            )
            for target in range(N)
        )
        for observer in range(N)
    )
    for observer in range(N):
        for target in range(N):
            for removed in range(M):
                solver.add(
                    z3.Implies(
                        owner[removed] == target,
                        utilities[observer]
                        >= target_values[observer][target] - values[observer][removed],
                    )
                )
    base_utility = numeric_utilities(values, BASE_OWNER)
    solver.add(
        z3.Or(
            *(
                z3.And(
                    *(
                        utilities[order[prefix]] == base_utility[order[prefix]]
                        for prefix in range(index)
                    ),
                    utilities[agent] > base_utility[agent],
                )
                for index, agent in enumerate(order)
            )
        )
    )
    found = []
    found_utilities = []
    while len(found) < limit:
        checked = solver.check()
        if checked == z3.unsat:
            return ("unsat" if not found else "sat"), found, found_utilities, None
        if checked != z3.sat:
            return ("unknown" if not found else "sat"), found, found_utilities, solver.reason_unknown()
        model = solver.model()
        concrete = tuple(
            None if model.eval(variable).as_long() == N else model.eval(variable).as_long()
            for variable in owner
        )
        if not numeric_efx(values, concrete):
            raise AssertionError("symbolic rival finder returned a non-EFX allocation")
        utility = numeric_utilities(values, concrete)
        if tuple(utility[agent] for agent in order) <= tuple(
            base_utility[agent] for agent in order
        ):
            raise AssertionError("symbolic rival finder returned a non-dominator")
        found.append(concrete)
        found_utilities.append(utility)
        solver.add(
            z3.Or(
                *(
                    variable != (N if assigned is None else assigned)
                    for variable, assigned in zip(owner, concrete)
                )
            )
        )
    return "sat", found, found_utilities, None


def load_pool(path: Path, order: tuple[int, ...]) -> list[Owner]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if payload.get("schema") != POOL_SCHEMA or payload.get("agent_order") != list(order):
        raise ValueError("pool metadata mismatch")
    return [tuple(owner) for owner in payload["rivals"]]


def save_pool(path: Path, order: tuple[int, ...], rivals: list[Owner]) -> None:
    atomic_json(
        path,
        {"schema": POOL_SCHEMA, "agent_order": list(order), "rivals": [list(owner) for owner in rivals]},
    )


def run(
    order: tuple[int, ...],
    pool_path: Path,
    result_path: Path,
    max_iterations: int,
    master_timeout_seconds: int,
    rival_timeout_seconds: int,
    rivals_per_iteration: int,
) -> dict:
    solver, values, own = structural_solver()
    solver.set(timeout=master_timeout_seconds * 1000)
    rivals = load_pool(pool_path, order)
    rival_set = set(rivals)
    for owner in rivals:
        solver.add(concrete_rival_blocker(values, own, owner, order))
    save_pool(pool_path, order, rivals)

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_SPLIT_PACKET_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values = integerize_model(solver.model(), values)
        rival_status, found_rivals, rival_utilities, rival_reason = find_dominating_rivals(
            model_values, order, rival_timeout_seconds, rivals_per_iteration
        )
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "rival_status": rival_status,
                "rival_count": len(found_rivals),
                "rival_owners": [list(rival) for rival in found_rivals],
                "rival_utilities": [list(utility) for utility in rival_utilities],
                "values": [list(row) for row in model_values],
            }
        )
        print(
            f"iteration={iteration} pool={len(rivals)} rival={rival_status} "
            f"found={len(found_rivals)}",
            flush=True,
        )
        if rival_status == "unsat":
            status = "SAT_GLOBAL_LEXMAX_SPLIT_PACKET"
            final_values = model_values
            break
        if rival_status == "unknown":
            status = "RIVAL_UNKNOWN"
            reason_unknown = rival_reason
            break
        if any(rival in rival_set for rival in found_rivals):
            raise AssertionError("pooled rival still dominates")
        for rival in found_rivals:
            solver.add(concrete_rival_blocker(values, own, rival, order))
            rivals.append(rival)
            rival_set.add(rival)
        save_pool(pool_path, order, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "claim_boundary": {
            "sat": "refutes the priority-sensitive alternating escape lemma for this exact split-packet cell but not complete EFX",
            "unsat": "closes the exact two-good-per-packet cell for this order; a cap-free lift is still required",
        },
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "iterations": len(trace),
        "pool_size": len(rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason_unknown,
        "values": None if final_values is None else [list(row) for row in final_values],
        "trace": trace,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logics": ["QF_LRA", "QF_LIA"]},
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-order", default="0,2,1,3")
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument("--master-timeout-seconds", type=int, default=300)
    parser.add_argument("--rival-timeout-seconds", type=int, default=60)
    parser.add_argument("--rivals-per-iteration", type=int, default=64)
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
        args.master_timeout_seconds,
        args.rival_timeout_seconds,
        args.rivals_per_iteration,
    )
    print(json.dumps({key: result[key] for key in ("status", "iterations", "pool_size", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
