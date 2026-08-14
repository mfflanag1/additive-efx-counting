#!/usr/bin/env python3
r"""Exact CEGAR for the first two-bare closed-support rank-three cell.

Unlike the superseded full-capture provenance, the seed-d closure has three
owners and exactly two receive no base-charity/outside-owner packet. This is
the first bounded cell satisfying the cap-free PI-free provenance separator.
"""

from __future__ import annotations

import argparse
import hashlib
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
from .run_full_capture_rank_three_cegar import (
    generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
)


TWO_BARE_BASE = {
    "r": ("a0", "m"),
    "q": ("gq", "a1", "j"),
    "d": ("h", "k", "q0"),
    "s": ("e", "p"),
    "charity": ("l", "gr"),
}


FORMS = {
    0: (("r", "q"), ("q", "r"), ("s", "d"), ("d", "q"), ("d", "r")),
    2: (("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r")),
}


def build_master(form_index):
    value = {
        (good, observer): z3.Real(f"tb_v_{good}_{observer}")
        for good in GOODS for observer in OWNERS
    }
    solver = z3.SolverFor("QF_LRA")
    for variable in value.values():
        solver.add(variable > 0, variable < 16)
    for owner in OWNERS:
        solver.add(total(value, owner, TWO_BARE_BASE[owner]) == 1)
        solver.add(total(value, owner, TWO_BARE_BASE["charity"]) <= 1)
        for target in OWNERS:
            if target != owner:
                solver.add(tail(value, owner, TWO_BARE_BASE[target]) <= 1)
    solver.add(*ordinary_pi_free_constraints(value, TWO_BARE_BASE))
    solver.add(*generalized_self_pi_free_constraints(value, TWO_BARE_BASE))

    # Three represented common-safe desired cores in the physical state.
    for source, packet in (("r", "A"), ("q", "Q"), ("s", "E")):
        solver.add(base_response(value, source, PACKETS[packet]))

    # Full-capture Q repair for d, now without the old external-retention
    # shortcut: every Q good is critical after adding H.
    solver.add(base_response(value, "d", PACKETS["Q"]))
    for good in PACKETS["Q"]:
        solver.add(total(
            value, "d",
            (*tuple(g for g in PACKETS["Q"] if g != good), *PACKETS["H"]),
        ) <= 1)

    # Root-facing unique wall at W.
    d_floor = total(value, "d", PACKETS["W"])
    solver.add(d_floor < tail(value, "d", PACKETS["A"]))
    solver.add(d_floor >= tail(value, "d", PACKETS["Q"]))
    solver.add(d_floor >= tail(value, "d", PACKETS["E"]))
    solver.add(d_floor >= total(value, "d", PACKETS["P"]))

    # Exact corrected five-edge response relation and rank three.
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
        "schema": "two-bare-closure-rank-three-four-edge-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "base": {owner: list(goods) for owner, goods in TWO_BARE_BASE.items()},
        "support": {owner: list(goods) for owner, goods in SUPPORT_STATE.items()},
        "closure": ["d", "q", "r"],
        "bare_closure_owners": ["q", "r"],
        "external_closure_packets": {"d": ["gr"], "q": [], "r": []},
        "allocation_menu_count": len(menu),
        "maximum_cuts_per_round": maximum_cuts_per_round,
        "rounds": [],
        "claim_boundary": (
            "twelve-atom two-bare necessary-premise CEGAR. It includes base "
            "EFX, full-capture criticality, unique root wall, and the exact "
            "rank-three response form, but not full signed reachability, "
            "generalized PI-freeness, or every saturation exclusion. SAT is "
            "not a full recurrence countermodel; UNSAT is not cap-free."
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
        witnesses = [a for a in menu if complete_efx(values, a)]
        supplier = {
            good: source for source, goods in SUPPORT_STATE.items() for good in goods
        }
        edge_counts = [len({
            (supplier[good], recipient)
            for recipient, goods in allocation.items() if recipient != "charity"
            for good in goods if supplier[good] != recipient
        }) for allocation in witnesses]
        record = {
            "iteration": iteration,
            "values": serialize_values(values),
            "complete_efx_count": len(witnesses),
            "minimum_support_edges": min(edge_counts) if edge_counts else None,
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
    result = run(args.output, args.form_index, args.maximum_iterations,
                 args.timeout_seconds, args.random_seed,
                 args.maximum_cuts_per_round)
    print(json.dumps({
        "status": result["status"], "rounds": len(result["rounds"]),
        "last": result["rounds"][-1] if result["rounds"] else None,
    }, indent=2))


if __name__ == "__main__":
    main()
