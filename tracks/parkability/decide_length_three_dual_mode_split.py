#!/usr/bin/env python3
"""Decide the fixed-root dual-mode payment disjunction in a split packet cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import (
        atomic_json,
        bundles,
        desired_expression,
        integerize_model,
        subset_sum,
    )
except ImportError:
    from run_alternating_global_lex_cegar import (
        atomic_json,
        bundles,
        desired_expression,
        integerize_model,
        subset_sum,
    )


SCHEMA = "length-three-dual-mode-split-v1"
P, R, Q, S = range(4)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_cell(sizes):
    names = ("tr", "br", "tq", "bq")
    goods = []
    packets = []
    for name, size in zip(names, sizes):
        packet = tuple(range(len(goods), len(goods) + size))
        packets.append(packet)
        goods.extend(name if size == 1 else f"{name}{index}" for index in range(size))
    x = len(goods)
    goods.append("x")
    y = len(goods)
    goods.append("y")
    f = len(goods)
    goods.append("f")
    tr, br, tq, bq = packets
    base_bundles = ((x,), tr + br, tq + bq, (y,))
    return {
        "goods": tuple(goods),
        "packets": tuple(packets),
        "x": x,
        "y": y,
        "f": f,
        "base_bundles": base_bundles,
        "m": len(goods),
    }


def efx_failures(values, owner):
    assigned = bundles(owner)
    own = tuple(subset_sum(values, agent, assigned[agent]) for agent in range(4))
    return tuple(
        own[observer]
        < subset_sum(
            values,
            observer,
            tuple(good for good in assigned[target] if good != removed),
        )
        for observer in range(4)
        for target in range(4)
        for removed in assigned[target]
    )


def structural_solver(cell):
    values = tuple(
        tuple(z3.Real(f"l3s_v_{agent}_{good}") for good in range(cell["m"]))
        for agent in range(4)
    )
    base_bundles = cell["base_bundles"]
    own = tuple(subset_sum(values, agent, base_bundles[agent]) for agent in range(4))
    solver = z3.SolverFor("QF_LRA")
    expected_envy = {(Q, P), (R, S)}
    for agent in range(4):
        solver.add(*(entry > 0 for entry in values[agent]))
        solver.add(z3.Sum(*values[agent]) == 1)
    for observer in range(4):
        solver.add(own[observer] > values[observer][cell["f"]])
        for target in range(4):
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

    tr, _br, tq, _bq = cell["packets"]
    expected = {
        (P, R): tr + (cell["f"],),
        (R, Q): tq + (cell["f"],),
        (Q, P): (cell["x"],),
        (R, S): (cell["y"],),
    }
    for source in range(4):
        for target in range(4):
            offer = base_bundles[target] + (cell["f"],)
            selected = expected.get((source, target))
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    relation = desired_expression(values, own, source, candidate)
                    if candidate == selected:
                        solver.add(relation)
                    elif selected is None or candidate == offer:
                        solver.add(z3.Not(relation))
    return solver, values, own


def payment_owner(cell, payment, mode):
    owner = [None] * cell["m"]
    tr, _br, _tq, _bq = cell["packets"]
    for good in tr + (cell["f"],):
        owner[good] = P
    owner[cell["x"]] = Q
    if mode == "r":
        owner[cell["y"]] = S
        for good in payment:
            owner[good] = R
    else:
        owner[cell["y"]] = R
        for good in payment:
            owner[good] = S
    return tuple(owner)


def subset_tables(values, m):
    size = 1 << m
    totals = [[0] * size for _ in range(4)]
    tails = [[0] * size for _ in range(4)]
    minimums = [[None] * size for _ in range(4)]
    for mask in range(1, size):
        bit = mask & -mask
        good = bit.bit_length() - 1
        rest = mask ^ bit
        for agent in range(4):
            totals[agent][mask] = totals[agent][rest] + values[agent][good]
            old = minimums[agent][rest]
            minimums[agent][mask] = values[agent][good] if old is None else min(old, values[agent][good])
            tails[agent][mask] = totals[agent][mask] - minimums[agent][mask]
    return totals, tails


def submasks(mask):
    current = mask
    while True:
        yield current
        if current == 0:
            return
        current = (current - 1) & mask


def mask_labels(mask, goods):
    return [goods[good] for good in range(len(goods)) if mask & (1 << good)]


def find_alternative_dual_mode(values, cell):
    totals, tails = subset_tables(values, cell["m"])
    base_masks = tuple(sum(1 << good for good in bundle) for bundle in cell["base_bundles"])
    base = tuple(totals[agent][base_masks[agent]] for agent in range(4))
    base_owner = [None] * cell["m"]
    for agent, bundle in enumerate(cell["base_bundles"]):
        for good in bundle:
            base_owner[good] = agent
    y_mask = 1 << cell["y"]
    available = ((1 << cell["m"]) - 1) ^ y_mask
    best = None
    for p_mask in submasks(available):
        if totals[P][p_mask] <= base[P]:
            continue
        after_p = available ^ p_mask
        for q_mask in submasks(after_p):
            if totals[Q][q_mask] <= base[Q]:
                continue
            after_q = after_p ^ q_mask
            for payment in submasks(after_q):
                for mode, payment_agent, singleton_agent in (("r", R, S), ("s", S, R)):
                    if totals[payment_agent][payment] < base[payment_agent]:
                        continue
                    assigned = [p_mask, 0, q_mask, 0]
                    assigned[payment_agent] = payment
                    assigned[singleton_agent] = y_mask
                    if not all(
                        totals[observer][assigned[observer]] >= tails[observer][assigned[target]]
                        for observer in range(4)
                        for target in range(4)
                    ):
                        continue
                    owner = [None] * cell["m"]
                    for agent, mask in enumerate(assigned):
                        for good in range(cell["m"]):
                            if mask & (1 << good):
                                owner[good] = agent
                    changed = sum(owner[good] != base_owner[good] for good in range(cell["m"]))
                    allocated = sum(mask.bit_count() for mask in assigned)
                    key = (changed, allocated, tuple(4 if entry is None else entry for entry in owner))
                    if best is None or key < best[0]:
                        best = (
                            key,
                            {
                                "mode": mode,
                                "changed_good_count": changed,
                                "allocated_good_count": allocated,
                                "owner_by_good": owner,
                                "bundles": {
                                    name: mask_labels(assigned[agent], cell["goods"])
                                    for agent, name in enumerate(("p", "r", "q", "s"))
                                },
                                "utilities": [totals[agent][assigned[agent]] for agent in range(4)],
                            },
                        )
    return None if best is None else best[1]


def run(sizes, timeout):
    cell = make_cell(sizes)
    solver, values, own = structural_solver(cell)
    solver.set(timeout=timeout * 1000)
    _tr, br, tq, bq = cell["packets"]
    residual = br + tq + bq
    candidates = []
    for size in range(1, len(residual) + 1):
        for payment in itertools.combinations(residual, size):
            for mode, recipient in (("r", R), ("s", S)):
                owner = payment_owner(cell, payment, mode)
                candidates.append((mode, payment, owner))
                solver.add(
                    z3.Or(
                        subset_sum(values, recipient, payment) < own[recipient],
                        *efx_failures(values, owner),
                    )
                )
    checked = solver.check()
    result = {
        "schema": SCHEMA,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "candidate_count": len(candidates),
        "solver_status": str(checked),
        "status": (
            "FIXED_ROOT_DUAL_MODE_FORCED"
            if checked == z3.unsat
            else "FIXED_ROOT_DUAL_MODE_REFUTED"
            if checked == z3.sat
            else "UNKNOWN"
        ),
        "reason_unknown": solver.reason_unknown() if checked == z3.unknown else None,
        "values": None,
        "claim_boundary": {
            "unsat": "the fixed-root dual-mode disjunction in this exact split-packet cell only",
            "sat": "a strict split-packet countermodel to the fixed-root disjunction, not to EFX",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(Path(__file__).resolve().parents[2])),
            "script_sha256": sha256(Path(__file__).resolve()),
            "z3_version": z3.get_version_string(),
        },
    }
    if checked == z3.sat:
        integer_values = integerize_model(solver.model(), values)
        result["values"] = [list(row) for row in integer_values]
        result["minimum_alternative_dual_mode_escape"] = find_alternative_dual_mode(
            integer_values, cell
        )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(entry) for entry in args.sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        parser.error("sizes must contain four positive integers")
    result = run(sizes, args.timeout_seconds)
    atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("status", "packet_sizes", "candidate_count", "reason_unknown")}, indent=2))


if __name__ == "__main__":
    main()
