#!/usr/bin/env python3
"""Exact rooted CEGAR for alternating atoms with variable packet sizes."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import z3


SCHEMA = "alternating-variable-packet-rooted-cegar-v1"
POOL_SCHEMA = "alternating-variable-packet-rooted-pool-v1"
AGENTS = ("p", "r", "s", "q")
N = 4
Owner = tuple[int | None, ...]


def atomic_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def make_cell(sizes: tuple[int, int, int, int]) -> dict:
    labels = ("tr", "br", "tq", "bq")
    goods = []
    packets = []
    for label, size in zip(labels, sizes):
        packet = tuple(range(len(goods), len(goods) + size))
        packets.append(packet)
        goods.extend(label if size == 1 else f"{label}{index}" for index in range(size))
    x = len(goods)
    goods.append("x")
    y = len(goods)
    goods.append("y")
    floater = len(goods)
    goods.append("f")
    tr, br, tq, bq = packets
    base_bundles = ((x,), tr + br, (y,), tq + bq)
    base_owner = tuple(
        next((agent for agent, bundle in enumerate(base_bundles) if good in bundle), None)
        for good in range(len(goods))
    )
    return {
        "sizes": sizes,
        "goods": tuple(goods),
        "packets": tuple(packets),
        "x": x,
        "y": y,
        "floater": floater,
        "base_bundles": base_bundles,
        "base_owner": base_owner,
        "m": len(goods),
    }


def bundles(owner: Owner) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(N)
    )


def subset_sum(values, observer: int, goods: tuple[int, ...]):
    return z3.Sum(*(values[observer][good] for good in goods)) if goods else z3.RealVal(0)


def desired_expression(values, own, source: int, candidate: tuple[int, ...]):
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


def lex_gt(left, right, order):
    return z3.Or(
        *(
            z3.And(
                *(left[order[prefix]] == right[order[prefix]] for prefix in range(index)),
                left[agent] > right[agent],
            )
            for index, agent in enumerate(order)
        )
    )


def structural_solver(cell):
    m = cell["m"]
    tr, br, tq, bq = cell["packets"]
    x, y, floater = cell["x"], cell["y"], cell["floater"]
    base_bundles = cell["base_bundles"]
    values = tuple(
        tuple(z3.Real(f"vp_{agent}_{good}") for good in range(m)) for agent in range(N)
    )
    own = tuple(subset_sum(values, agent, base_bundles[agent]) for agent in range(N))
    solver = z3.SolverFor("QF_LRA")
    for agent in range(N):
        solver.add(*(entry > 0 for entry in values[agent]))
        solver.add(z3.Sum(*values[agent]) == 1)
    # Relabeling within a packet can sort one reference row only.  Sorting
    # every row would incorrectly require all agents to agree on that order.
    for packet in cell["packets"]:
        for left, right in zip(packet, packet[1:]):
            solver.add(values[0][left] < values[0][right])

    expected_envy = {(1, 2), (3, 0)}
    for observer in range(N):
        solver.add(own[observer] > values[observer][floater])
        for target in range(N):
            if observer != target:
                target_value = subset_sum(values, observer, base_bundles[target])
                solver.add(
                    target_value > own[observer]
                    if (observer, target) in expected_envy
                    else own[observer] > target_value
                )
            for removed in base_bundles[target]:
                solver.add(
                    own[observer]
                    > subset_sum(
                        values,
                        observer,
                        tuple(good for good in base_bundles[target] if good != removed),
                    )
                )

    expected_desired = {
        (0, 1): tr + (floater,),
        (1, 2): (y,),
        (2, 3): tq + (floater,),
        (3, 0): (x,),
    }
    for source in range(N):
        for target in range(N):
            offer = base_bundles[target] + (floater,)
            expected = expected_desired.get((source, target))
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    relation = desired_expression(values, own, source, candidate)
                    if candidate == expected:
                        solver.add(relation)
                    elif expected is None or candidate == offer:
                        solver.add(z3.Not(relation))

    compatible_families = (
        (1, 3, br),
        (2, 3, br),
        (3, 1, bq),
        (0, 1, bq),
    )
    for source, target, incoming in compatible_families:
        target_bundle = base_bundles[target]
        for incoming_size in range(len(incoming) + 1):
            for incoming_subset in itertools.combinations(incoming, incoming_size):
                for release_size in range(len(target_bundle) + 1):
                    for release in itertools.combinations(target_bundle, release_size):
                        offer = tuple(good for good in target_bundle if good not in release) + incoming_subset
                        for size in range(1, len(offer) + 1):
                            for candidate in itertools.combinations(offer, size):
                                solver.add(
                                    z3.Not(desired_expression(values, own, source, candidate))
                                )
    return solver, values, own


def numeric_utilities(values, owner: Owner):
    assigned = bundles(owner)
    return tuple(sum(values[agent][good] for good in assigned[agent]) for agent in range(N))


def numeric_efx(values, owner: Owner) -> bool:
    assigned = bundles(owner)
    own = numeric_utilities(values, owner)
    return all(
        own[observer]
        >= sum(values[observer][good] for good in assigned[target] if good != removed)
        for observer in range(N)
        for target in range(N)
        for removed in assigned[target]
    )


def rival_blocker(values, base_own, owner: Owner, order):
    assigned = bundles(owner)
    rival_own = tuple(subset_sum(values, agent, assigned[agent]) for agent in range(N))
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


def integerize(model, symbolic):
    rows = []
    for row in symbolic:
        fractions = []
        for expression in row:
            result = model.eval(expression, model_completion=True)
            fractions.append(Fraction(result.numerator_as_long(), result.denominator_as_long()))
        denominator = math.lcm(*(entry.denominator for entry in fractions))
        integers = tuple(int(entry * denominator) for entry in fractions)
        divisor = math.gcd(*integers)
        rows.append(tuple(entry // divisor for entry in integers))
    return tuple(rows)


def rooted_candidates(cell, root: int) -> tuple[Owner, ...]:
    root_good = cell["base_bundles"][root][0]
    remaining = tuple(good for good in range(cell["m"]) if good != root_good)
    destinations = tuple(agent for agent in range(N) if agent != root) + (None,)
    candidates = []
    for assignment in itertools.product(destinations, repeat=len(remaining)):
        owner = [None] * cell["m"]
        owner[root_good] = root
        for good, destination in zip(remaining, assignment):
            owner[good] = destination
        candidates.append(tuple(owner))
    return tuple(candidates)


def dominating(values, cell, order, candidates):
    base = numeric_utilities(values, cell["base_owner"])
    base_key = tuple(base[agent] for agent in order)
    found = []
    efx_count = 0
    for owner in candidates:
        if not numeric_efx(values, owner):
            continue
        efx_count += 1
        utility = numeric_utilities(values, owner)
        key = tuple(utility[agent] for agent in order)
        if key > base_key:
            found.append((key, owner))
    found.sort(reverse=True, key=lambda record: (record[0], str(record[1])))
    return found, efx_count


def load_pool(path, cell, order):
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("packet_sizes") != list(cell["sizes"])
        or payload.get("agent_order") != list(order)
    ):
        raise ValueError("pool metadata mismatch")
    return [tuple(owner) for owner in payload["rivals"]]


def save_pool(path, cell, order, rivals):
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "packet_sizes": list(cell["sizes"]),
            "agent_order": list(order),
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(sizes, order, pool_path, result_path, max_iterations, add_per_iteration, timeout):
    cell = make_cell(sizes)
    candidates = rooted_candidates(cell, order[0])
    solver, values, own = structural_solver(cell)
    solver.set(timeout=timeout * 1000)
    rivals = load_pool(pool_path, cell, order)
    rival_set = set(rivals)
    for rival in rivals:
        solver.add(rival_blocker(values, own, rival, order))
    save_pool(pool_path, cell, order, rivals)

    trace = []
    started = time.time()
    status = "ITERATION_LIMIT"
    final_values = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_ROOTED_VARIABLE_PACKET_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values = integerize(solver.model(), values)
        found, efx_count = dominating(model_values, cell, order, candidates)
        unseen = [owner for _, owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "efx_count": efx_count,
                "dominating_count": len(found),
                "new_count": len(unseen),
                "values": [list(row) for row in model_values],
            }
        )
        print(
            f"sizes={sizes} iteration={iteration} pool={len(rivals)} "
            f"efx={efx_count} dominating={len(found)} new={len(unseen)}",
            flush=True,
        )
        if not found:
            status = "SAT_NO_ROOTED_LEX_ESCAPE"
            final_values = model_values
            break
        if not unseen:
            raise AssertionError("pooled rival still dominates")
        for owner in unseen[:add_per_iteration]:
            solver.add(rival_blocker(values, own, owner, order))
            rivals.append(owner)
            rival_set.add(owner)
        save_pool(pool_path, cell, order, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "claim_boundary": {
            "sat": "refutes the rooted external-observer lemma in this exact variable-packet cell only",
            "unsat": "proves the rooted lemma only in this exact variable-packet cell until a cap-free proof is supplied",
        },
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "candidate_count": len(candidates),
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
    parser.add_argument("--packet-sizes", required=True)
    parser.add_argument("--agent-order", default="0,2,1,3")
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--add-per-iteration", type=int, default=64)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    sizes = tuple(int(field) for field in args.packet_sizes.split(","))
    order = tuple(int(field) for field in args.agent_order.split(","))
    if len(sizes) != 4 or min(sizes) < 1:
        parser.error("packet sizes must be four positive integers")
    if sorted(order) != list(range(N)) or order[0] not in (0, 2):
        parser.error("order must be a permutation rooted at p=0 or s=2")
    if args.result.exists():
        parser.error("result path must not exist")
    result = run(
        sizes,
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
