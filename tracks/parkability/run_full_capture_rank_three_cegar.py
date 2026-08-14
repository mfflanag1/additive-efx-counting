#!/usr/bin/env python3
r"""Exact CEGAR for the missing full-capture K=Q rank-three atomization.

This deliberately changes base provenance while retaining the same support
packets.  Every good of Q is payment-critical for d when combined with H,
so the old positive q0=Q\K shortcut is absent.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
)
from .run_fixed_u_full_packet_terminal_cegar import (
    GOODS, OWNERS, PACKETS, SUPPORT_STATE, allocation_formula, fractions,
    tail, total,
)
from .run_fixed_u_rank_three_relation_cegar import (
    base_response, rank_four_exists, response_edges,
)


FULL_CAPTURE_BASE = {
    "r": ("a0", "m"),
    "q": ("gq", "a1"),
    "d": ("h", "k", "q0"),
    "s": ("e", "p"),
    "charity": ("j", "l", "gr"),
}


FORMS = {
    0: (("r", "q"), ("q", "r"), ("s", "d"), ("d", "q"), ("d", "r")),
    2: (("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r")),
}


def ordinary_pi_free_constraints(value, base):
    edge = {}
    for source in OWNERS:
        for target in OWNERS:
            if source == target:
                continue
            edge[source, target] = z3.Or(*(
                base_response(value, source, goods)
                for size in range(1, len(base[target]) + 1)
                for goods in itertools.combinations(base[target], size)
            ))
    constraints = []
    for length in range(2, len(OWNERS) + 1):
        for subset in itertools.combinations(OWNERS, length):
            anchor = min(subset)
            for tail_order in itertools.permutations(
                    tuple(owner for owner in subset if owner != anchor)):
                cycle = (anchor, *tail_order)
                constraints.append(z3.Not(z3.And(*(
                    edge[cycle[index], cycle[(index + 1) % length]]
                    for index in range(length)
                ))))
    return constraints


def generalized_self_pi_free_constraints(value, base):
    constraints = []
    charity = tuple(base["charity"])
    for owner in OWNERS:
        universe = (*tuple(base[owner]), *charity)
        for size in range(1, len(universe) + 1):
            for goods in itertools.combinations(universe, size):
                if not set(goods) & set(charity):
                    continue
                constraints.append(z3.Not(base_response(value, owner, goods)))
    return constraints


def build_master(form_index):
    value = {
        (good, observer): z3.Real(f"fc_v_{good}_{observer}")
        for good in GOODS for observer in OWNERS
    }
    solver = z3.SolverFor("QF_LRA")
    for variable in value.values():
        solver.add(variable > 0, variable < 16)
    for owner in OWNERS:
        solver.add(total(value, owner, FULL_CAPTURE_BASE[owner]) == 1)
        solver.add(total(value, owner, FULL_CAPTURE_BASE["charity"]) <= 1)
        for target in OWNERS:
            if target != owner:
                solver.add(tail(value, owner, FULL_CAPTURE_BASE[target]) <= 1)
    solver.add(*ordinary_pi_free_constraints(value, FULL_CAPTURE_BASE))
    solver.add(*generalized_self_pi_free_constraints(value, FULL_CAPTURE_BASE))

    # Three represented common-safe desired cores.
    for source, packet in (("r", "A"), ("q", "Q"), ("s", "E")):
        solver.add(base_response(value, source, PACKETS[packet]))

    # Full-capture K=Q: Q+H repairs d, but deleting any Q-good destroys the
    # repair. Q itself remains the blocked common-safe desired core.
    solver.add(base_response(value, "d", PACKETS["Q"]))
    q_goods = PACKETS["Q"]
    for good in q_goods:
        solver.add(total(
            value, "d", (*tuple(g for g in q_goods if g != good), *PACKETS["H"])
        ) <= 1)

    # Root-facing unique wall at residual W.
    d_floor = total(value, "d", PACKETS["W"])
    solver.add(d_floor < tail(value, "d", PACKETS["A"]))
    solver.add(d_floor >= tail(value, "d", PACKETS["Q"]))
    solver.add(d_floor >= tail(value, "d", PACKETS["E"]))
    solver.add(d_floor >= total(value, "d", PACKETS["P"]))

    # Corrected exact five-edge nonself support response relation and rank 3.
    edge = response_edges(value, SUPPORT_STATE, include_current=True, exclude_self=True)
    solver.add(z3.Not(rank_four_exists(edge)))
    expected = set(FORMS[form_index])
    for source in OWNERS:
        for target in (*OWNERS, "charity"):
            if source == target:
                continue
            solver.add(edge[source, target] if (source, target) in expected
                       else z3.Not(edge[source, target]))
    return solver, value


def serialize_values(values):
    return {
        owner: {good: str(amount) for good, amount in row.items()}
        for owner, row in values.items()
    }


def run(output, form_index, maximum_iterations, timeout_seconds, random_seed,
        maximum_cuts_per_round):
    solver, value = build_master(form_index)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    menu = tuple(
        allocation for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE)
        if all(allocation[owner] for owner in OWNERS)
    )
    result = {
        "schema": "full-capture-rank-three-four-edge-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "base": {owner: list(goods) for owner, goods in FULL_CAPTURE_BASE.items()},
        "support": {owner: list(goods) for owner, goods in SUPPORT_STATE.items()},
        "full_capture": "K=Q; every Q-good is critical in Q-good+H for d",
        "allocation_menu_count": len(menu),
        "maximum_cuts_per_round": maximum_cuts_per_round,
        "rounds": [],
        "claim_boundary": (
            "twelve-atom full-capture necessary-premise CEGAR. It includes base "
            "EFX, common-safe cores, the unique root-facing wall, and the exact "
            "five-edge response form, but omits full signed reachability and all "
            "saturation selectors. A no-go profile is not a universal countermodel; "
            "UNSAT is not a cap-free theorem."
        ),
        "provenance": {
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
    }
    for iteration in range(maximum_iterations):
        status = solver.check()
        if status != z3.sat:
            result["status"] = str(status)
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            break
        values = fractions(solver.model(), value)
        witnesses = [
            allocation for allocation in menu if complete_efx(values, allocation)
        ]
        minimum_edges = None
        if witnesses:
            supplier = {
                good: source for source, goods in SUPPORT_STATE.items() for good in goods
            }
            minimum_edges = min(len({
                (supplier[good], recipient)
                for recipient, goods in allocation.items() if recipient != "charity"
                for good in goods if supplier[good] != recipient
            }) for allocation in witnesses)
        record = {
            "iteration": iteration,
            "values": serialize_values(values),
            "complete_efx_count": len(witnesses),
            "minimum_support_edges": minimum_edges,
            "blocking_allocations": witnesses[:maximum_cuts_per_round],
        }
        result["rounds"].append(record)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        if not witnesses:
            result["status"] = "SAT_BOUNDED_FOUR_EDGE_OBSTRUCTION"
            break
        for allocation in witnesses[:maximum_cuts_per_round]:
            solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    else:
        result["status"] = "ITERATION_LIMIT"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--maximum-iterations", type=int, default=20)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-cuts-per-round", type=int, default=100)
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.maximum_iterations,
        args.timeout_seconds, args.random_seed, args.maximum_cuts_per_round,
    )
    print(json.dumps({
        "status": result["status"], "rounds": len(result["rounds"]),
        "last": result["rounds"][-1] if result["rounds"] else None,
    }, indent=2))


if __name__ == "__main__":
    main()
