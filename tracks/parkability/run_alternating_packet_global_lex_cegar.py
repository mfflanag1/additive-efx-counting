#!/usr/bin/env python3
"""Global-lex CEGAR over a sound whole-packet EFX relaxation."""

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
    from .run_alternating_global_lex_cegar import (
        AGENTS,
        ALL_OWNERS,
        BASE_BUNDLES,
        BASE_OWNER,
        EXPECTED_DESIRED,
        EXPECTED_ENVY,
        M,
        N,
        V_STAR,
        atomic_json,
        bundles,
        lex_gt,
        subset_sum,
    )
except ImportError:
    from run_alternating_global_lex_cegar import (
        AGENTS,
        ALL_OWNERS,
        BASE_BUNDLES,
        BASE_OWNER,
        EXPECTED_DESIRED,
        EXPECTED_ENVY,
        M,
        N,
        V_STAR,
        atomic_json,
        bundles,
        lex_gt,
        subset_sum,
    )


SCHEMA = "alternating-packet-global-lex-cegar-v1"
POOL_SCHEMA = "alternating-packet-global-lex-rival-pool-v1"
PACKETS = (0, 1, 2, 3)
Owner = tuple[int | None, ...]


def deletion_remainder(
    values: tuple[tuple[z3.ArithRef, ...], ...],
    packet_remainders: tuple[tuple[z3.ArithRef, ...], ...],
    observer: int,
    atom_bundle: tuple[int, ...],
    removed_atom: int,
) -> z3.ArithRef:
    other = tuple(atom for atom in atom_bundle if atom != removed_atom)
    base = subset_sum(values, observer, other)
    if removed_atom not in PACKETS:
        return base
    return base + packet_remainders[observer][removed_atom]


def packet_desired_expression(
    values: tuple[tuple[z3.ArithRef, ...], ...],
    packet_remainders: tuple[tuple[z3.ArithRef, ...], ...],
    own: tuple[z3.ArithRef, ...],
    source: int,
    candidate: tuple[int, ...],
) -> z3.BoolRef:
    return z3.And(
        subset_sum(values, source, candidate) > own[source],
        *(
            own[observer]
            >= deletion_remainder(
                values,
                packet_remainders,
                observer,
                candidate,
                removed_atom,
            )
            for observer in range(N)
            for removed_atom in candidate
        ),
    )


def packet_structural_solver() -> tuple[
    z3.Solver,
    tuple[tuple[z3.ArithRef, ...], ...],
    tuple[tuple[z3.ArithRef, ...], ...],
    tuple[z3.ArithRef, ...],
]:
    values = tuple(
        tuple(z3.Real(f"w_{agent}_{atom}") for atom in range(M))
        for agent in range(N)
    )
    packet_remainders = tuple(
        tuple(z3.Real(f"rho_{agent}_{packet}") for packet in PACKETS)
        for agent in range(N)
    )
    own = tuple(
        subset_sum(values, agent, BASE_BUNDLES[agent]) for agent in range(N)
    )
    packet_is_multi = tuple(
        z3.Bool(f"packet_{packet}_is_multi") for packet in PACKETS
    )
    solver = z3.SolverFor("QF_LRA")
    for agent in range(N):
        solver.add(*(entry > 0 for entry in values[agent]))
        solver.add(z3.Sum(*values[agent]) == 1)
        for packet in PACKETS:
            solver.add(packet_remainders[agent][packet] >= 0)
            solver.add(packet_remainders[agent][packet] < values[agent][packet])
            solver.add(
                z3.If(
                    packet_is_multi[packet],
                    2 * packet_remainders[agent][packet]
                    >= values[agent][packet],
                    packet_remainders[agent][packet] == 0,
                )
            )

    for observer in range(N):
        solver.add(own[observer] > values[observer][6])
        for target in range(N):
            if observer != target:
                comparison = subset_sum(values, observer, BASE_BUNDLES[target])
                if (observer, target) in EXPECTED_ENVY:
                    solver.add(comparison > own[observer])
                else:
                    solver.add(own[observer] > comparison)
            for removed_atom in BASE_BUNDLES[target]:
                solver.add(
                    own[observer]
                    > deletion_remainder(
                        values,
                        packet_remainders,
                        observer,
                        BASE_BUNDLES[target],
                        removed_atom,
                    )
                )

    for source in range(N):
        for target in range(N):
            offer = BASE_BUNDLES[target] + (6,)
            expected = EXPECTED_DESIRED.get((source, target), set())
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    relation = packet_desired_expression(
                        values,
                        packet_remainders,
                        own,
                        source,
                        candidate,
                    )
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
    for source, target, incoming_packet in compatible_families:
        target_bundle = BASE_BUNDLES[target]
        for use_incoming in (False, True):
            for release_size in range(len(target_bundle) + 1):
                for release in itertools.combinations(target_bundle, release_size):
                    offer = tuple(
                        atom for atom in target_bundle if atom not in release
                    ) + ((incoming_packet,) if use_incoming else ())
                    for size in range(1, len(offer) + 1):
                        for candidate in itertools.combinations(offer, size):
                            solver.add(
                                z3.Not(
                                    packet_desired_expression(
                                        values,
                                        packet_remainders,
                                        own,
                                        source,
                                        candidate,
                                    )
                                )
                            )

    return solver, values, packet_remainders, own


def packet_rival_blocker(
    values: tuple[tuple[z3.ArithRef, ...], ...],
    packet_remainders: tuple[tuple[z3.ArithRef, ...], ...],
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
        < deletion_remainder(
            values,
            packet_remainders,
            observer,
            assigned[target],
            removed_atom,
        )
        for observer in range(N)
        for target in range(N)
        for removed_atom in assigned[target]
    )
    return z3.Or(*failures, z3.Not(lex_gt(rival_own, base_own, order)))


def rational(model: z3.ModelRef, expression: z3.ArithRef) -> Fraction:
    result = model.eval(expression, model_completion=True)
    if not z3.is_rational_value(result):
        raise TypeError(result)
    return Fraction(result.numerator_as_long(), result.denominator_as_long())


def integerize_packet_model(
    model: z3.ModelRef,
    symbolic_values: tuple[tuple[z3.ArithRef, ...], ...],
    symbolic_remainders: tuple[tuple[z3.ArithRef, ...], ...],
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    values = []
    remainders = []
    for agent in range(N):
        row_values = tuple(rational(model, item) for item in symbolic_values[agent])
        row_remainders = tuple(
            rational(model, item) for item in symbolic_remainders[agent]
        )
        denominator = math.lcm(
            *(entry.denominator for entry in row_values + row_remainders)
        )
        integers = tuple(int(entry * denominator) for entry in row_values)
        integer_remainders = tuple(
            int(entry * denominator) for entry in row_remainders
        )
        divisor = math.gcd(*(integers + integer_remainders))
        values.append(tuple(entry // divisor for entry in integers))
        remainders.append(
            tuple(entry // divisor for entry in integer_remainders)
        )
    return tuple(values), tuple(remainders)


def numeric_utilities(
    values: tuple[tuple[int, ...], ...], owner: Owner
) -> tuple[int, ...]:
    assigned = bundles(owner)
    return tuple(
        sum(values[agent][atom] for atom in assigned[agent]) for agent in range(N)
    )


def numeric_packet_efx(
    values: tuple[tuple[int, ...], ...],
    remainders: tuple[tuple[int, ...], ...],
    owner: Owner,
) -> bool:
    assigned = bundles(owner)
    own = numeric_utilities(values, owner)
    return all(
        own[observer]
        >= sum(
            values[observer][atom]
            for atom in assigned[target]
            if atom != removed_atom
        )
        + (
            remainders[observer][removed_atom]
            if removed_atom in PACKETS
            else 0
        )
        for observer in range(N)
        for target in range(N)
        for removed_atom in assigned[target]
    )


def dominating_packet_rivals(
    values: tuple[tuple[int, ...], ...],
    remainders: tuple[tuple[int, ...], ...],
    order: tuple[int, ...],
) -> tuple[list[tuple[tuple[int, ...], Owner]], int]:
    base = numeric_utilities(values, BASE_OWNER)
    base_key = tuple(base[agent] for agent in order)
    found = []
    efx_count = 0
    for owner in ALL_OWNERS:
        if not numeric_packet_efx(values, remainders, owner):
            continue
        efx_count += 1
        utility = numeric_utilities(values, owner)
        key = tuple(utility[agent] for agent in order)
        if key > base_key:
            found.append((key, owner))
    found.sort(reverse=True, key=lambda record: (record[0], str(record[1])))
    return found, efx_count


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
        {
            "schema": POOL_SCHEMA,
            "agent_order": list(order),
            "rivals": [list(owner) for owner in rivals],
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
    solver, values, remainders, own = packet_structural_solver()
    solver.set(timeout=timeout_seconds * 1000)
    rivals = load_pool(pool_path, order)
    rival_set = set(rivals)
    zero_remainders = tuple(tuple(0 for _ in PACKETS) for _ in range(N))
    seed, _ = dominating_packet_rivals(V_STAR, zero_remainders, order)
    for _, owner in seed:
        if owner not in rival_set:
            rivals.append(owner)
            rival_set.add(owner)
    for owner in rivals:
        solver.add(packet_rival_blocker(values, remainders, own, owner, order))
    save_pool(pool_path, order, rivals)

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    final_remainders = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_WHOLE_PACKET_RELAXATION"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values, model_remainders = integerize_packet_model(
            solver.model(), values, remainders
        )
        found, efx_count = dominating_packet_rivals(
            model_values, model_remainders, order
        )
        unseen = [owner for _, owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "efx_assignment_count": efx_count,
                "dominating_rival_count": len(found),
                "new_rival_count": len(unseen),
                "values": [list(row) for row in model_values],
                "packet_max_deletion_remainders": [
                    list(row) for row in model_remainders
                ],
            }
        )
        print(
            f"iteration={iteration} pool={len(rivals)} efx={efx_count} "
            f"dominating={len(found)} new={len(unseen)}",
            flush=True,
        )
        if not found:
            status = "SAT_WHOLE_PACKET_GLOBAL_LEXMAX"
            final_values = model_values
            final_remainders = model_remainders
            break
        if not unseen:
            raise AssertionError("a pooled whole-packet rival still dominates")
        for owner in unseen[:add_per_iteration]:
            solver.add(packet_rival_blocker(values, remainders, own, owner, order))
            rivals.append(owner)
            rival_set.add(owner)
        save_pool(pool_path, order, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "claim_boundary": {
            "unsat": "proves a whole-packet priority escape for this order under the stated sound packet relaxation",
            "sat": "shows that whole-packet reallocations do not suffice in the relaxation; it is not necessarily realizable by item valuations",
        },
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "iterations": len(trace),
        "pool_size": len(rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason_unknown,
        "values": None if final_values is None else [list(row) for row in final_values],
        "packet_max_deletion_remainders": (
            None
            if final_remainders is None
            else [list(row) for row in final_remainders]
        ),
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
    print(
        json.dumps(
            {key: result[key] for key in ("status", "iterations", "pool_size", "elapsed_seconds")},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
