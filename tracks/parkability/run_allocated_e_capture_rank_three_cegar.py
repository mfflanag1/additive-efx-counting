#!/usr/bin/env python3
"""Exact generalized-PI CEGAR for the allocated-E captured-support cell.

This repairs the vacuous former residual atomization by making the external
good ``l`` in the paid common-safe core E={e,l} base-owned by sacrificed
owner d rather than unallocated.  Thus the required s self-splice depends on
release of allocated d-support and is not itself a one-edge PI cycle.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

from .decide_two_survivor_named_topology_family import (
    R2_TOPOLOGIES, R3_TOPOLOGIES, allocations_supported_by, canonical,
)
from .find_generalized_pi_cycle import find_closed_core_families
from .run_fixed_u_full_packet_terminal_cegar import (
    GOODS, OWNERS, PACKETS, SUPPORT_STATE, allocation_formula, fractions,
    tail, total,
)
from .run_fixed_u_rank_three_relation_cegar import (
    base_response, rank_four_exists, response_edges,
)
from .run_full_capture_rank_three_cegar import (
    FORMS, ordinary_pi_free_constraints,
)
from .run_generalized_pi_named_selector_cegar import (
    cycle_signature, generalized_pi_cut,
)


ALLOCATED_E_BASE = {
    "r": ("a0", "m"),
    "q": ("gq", "a1", "j"),
    "d": ("h", "k", "q0", "l"),
    "s": ("e", "p"),
    "charity": ("gr",),
}


def linear_base_response(value, source, goods):
    """Exactly ``base_response`` without min/ITE terms.

    For additive values, tail(B)<=1 iff B-g has value <=1 for every g in B.
    """
    goods = tuple(goods)
    return z3.And(
        total(value, source, goods) > 1,
        *(
            total(value, observer, tuple(other for other in goods if other != removed)) <= 1
            for observer in OWNERS for removed in goods
        ),
    )


FIXED_CORES = {
    "r": PACKETS["A"],
    "q": PACKETS["Q"],
    "s": PACKETS["E"],
}


def fixed_core_anchored_pi_free_constraints(value):
    """Forbid every alternative core closing with fixed selected cores."""
    base_owner = {
        good: owner
        for owner, goods in ALLOCATED_E_BASE.items()
        for good in goods
    }
    excluded = set()
    fixed_sources = tuple(FIXED_CORES)
    for source in OWNERS:
        available_fixed = tuple(owner for owner in fixed_sources if owner != source)
        for subset_size in range(1, len(available_fixed) + 1):
            for fixed_subset in itertools.combinations(available_fixed, subset_size):
                vertices = set(fixed_subset) | {source}
                fixed_union = set().union(*(set(FIXED_CORES[owner]) for owner in fixed_subset))
                if any(
                    base_owner[good] not in vertices | {"charity"}
                    for good in fixed_union
                ):
                    continue
                complement = tuple(good for good in GOODS if good not in fixed_union)
                for mask in range(1, 1 << len(complement)):
                    goods = tuple(
                        good for index, good in enumerate(complement)
                        if mask & (1 << index)
                    )
                    if any(
                        base_owner[good] not in vertices | {"charity"}
                        for good in goods
                    ):
                        continue
                    excluded.add((source, tuple(sorted(goods))))
    return tuple(
        z3.Not(linear_base_response(value, source, goods))
        for source, goods in sorted(excluded)
    ), len(excluded)


def pairwise_closed_core_pi_free_constraints(value):
    """Forbid every closed disjoint desired-core family on two owners."""
    constraints = []
    for left, right in itertools.combinations(OWNERS, 2):
        allowed = tuple(
            good for owner in (left, right, "charity")
            for good in ALLOCATED_E_BASE[owner]
        )
        # Each allowed good is unused, in left's core, or in right's core.
        for assignment in itertools.product(range(3), repeat=len(allowed)):
            left_core = tuple(
                good for good, slot in zip(allowed, assignment, strict=True)
                if slot == 1
            )
            right_core = tuple(
                good for good, slot in zip(allowed, assignment, strict=True)
                if slot == 2
            )
            if not left_core or not right_core:
                continue
            constraints.append(z3.Not(z3.And(
                linear_base_response(value, left, left_core),
                linear_base_response(value, right, right_core),
            )))
    return tuple(constraints)


def generalized_self_pi_free_constraints(value):
    constraints = []
    charity = tuple(ALLOCATED_E_BASE["charity"])
    charity_set = set(charity)
    for owner in OWNERS:
        universe = (*tuple(ALLOCATED_E_BASE[owner]), *charity)
        for mask in range(1, 1 << len(universe)):
            goods = tuple(
                good for index, good in enumerate(universe)
                if mask & (1 << index)
            )
            if not set(goods) & charity_set:
                continue
            constraints.append(z3.Not(linear_base_response(value, owner, goods)))
    return constraints


def build_master(form_index):
    value = {
        (good, observer): z3.Real(f"aec_v_{good}_{observer}")
        for good in GOODS for observer in OWNERS
    }
    solver = z3.SolverFor("QF_LRA")
    for variable in value.values():
        solver.add(variable > 0, variable < 16)
    for owner in OWNERS:
        solver.add(total(value, owner, ALLOCATED_E_BASE[owner]) == 1)
        solver.add(total(value, owner, ALLOCATED_E_BASE["charity"]) <= 1)
        for target in OWNERS:
            if target != owner:
                solver.add(tail(value, owner, ALLOCATED_E_BASE[target]) <= 1)
    solver.add(*ordinary_pi_free_constraints(value, ALLOCATED_E_BASE))
    solver.add(*generalized_self_pi_free_constraints(value))

    for source, packet in (("r", "A"), ("q", "Q"), ("s", "E")):
        solver.add(linear_base_response(value, source, PACKETS[packet]))

    anchored_constraints, _ = fixed_core_anchored_pi_free_constraints(value)
    solver.add(*anchored_constraints)
    solver.add(*pairwise_closed_core_pi_free_constraints(value))

    # Cap-free closed-disjoint-core PI lemma: A,Q,E are fixed pairwise-
    # disjoint minimal/common-safe desired cores for r,q,s. If d had any
    # desired common-safe core disjoint from their union, the four cores
    # would form a generalized PI cycle. Enumerate the exact complement in
    # this atomization rather than rediscovering that family by CEGAR.
    selected_union = set(PACKETS["A"]) | set(PACKETS["Q"]) | set(PACKETS["E"])
    complement = tuple(good for good in GOODS if good not in selected_union)
    for mask in range(1, 1 << len(complement)):
        goods = tuple(
            good for index, good in enumerate(complement)
            if mask & (1 << index)
        )
        solver.add(z3.Not(linear_base_response(value, "d", goods)))

    solver.add(base_response(value, "d", PACKETS["Q"]))
    for good in PACKETS["Q"]:
        solver.add(total(
            value, "d",
            (*tuple(g for g in PACKETS["Q"] if g != good), *PACKETS["H"]),
        ) <= 1)

    d_floor = total(value, "d", PACKETS["W"])
    solver.add(d_floor < tail(value, "d", PACKETS["A"]))
    solver.add(d_floor >= tail(value, "d", PACKETS["Q"]))
    solver.add(d_floor >= tail(value, "d", PACKETS["E"]))
    solver.add(d_floor >= total(value, "d", PACKETS["P"]))

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


def run(output, form_index, timeout_seconds, random_seed, maximum_iterations,
        negate_named_selector=True, resume=None, maximum_families_per_round=10000):
    solver, value = build_master(form_index)
    seen = set()
    if negate_named_selector:
        topologies = R2_TOPOLOGIES if form_index == 0 else R3_TOPOLOGIES
        for topology in topologies:
            for allocation in allocations_supported_by(topology):
                key = canonical(allocation)
                if key in seen:
                    continue
                seen.add(key)
                solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    signatures = set()
    resume_record = None
    if resume is not None:
        resume_payload = json.loads(resume.read_text())
        if resume_payload.get("form_index") != form_index:
            raise ValueError("resume form does not match requested form")
        for record in resume_payload.get("iterations", []):
            witnesses = record.get("pi_witnesses")
            if witnesses is None:
                witness = record.get("pi_witness")
                witnesses = () if witness is None else (witness,)
            for witness in witnesses:
                signature = cycle_signature(witness)
                if signature in signatures:
                    continue
                signatures.add(signature)
                solver.add(generalized_pi_cut(value, witness))
        resume_record = {
            "source": f"results/{resume.name}",
            "source_sha256": hashlib.sha256(resume.read_bytes()).hexdigest(),
            "loaded_cut_count": len(signatures),
        }

    result = {
        "schema": "allocated-e-capture-rank-three-generalized-pi-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "base": {owner: list(goods) for owner, goods in ALLOCATED_E_BASE.items()},
        "support": {owner: list(goods) for owner, goods in SUPPORT_STATE.items()},
        "e_external_supplier": "d",
        "negate_named_selector": negate_named_selector,
        "allocation_count": len(seen),
        "timeout_seconds_per_check": timeout_seconds,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "random_seed": random_seed,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "resume": resume_record,
        "iterations": [],
        "claim_boundary": (
            "Exact twelve-good allocated-E captured-support cell with complete "
            "ordinary and generalized self-PI exclusions plus iterative cuts "
            "for every canonical generalized PI cycle found. Any result is a "
            "bounded-atom theorem or counterprofile, not the cap-free theorem."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["generalized_pi_cut_count"] = len(signatures)
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {"iteration": iteration, "solver_status": str(checked)}
        if checked == z3.unsat:
            result["status"] = "UNSAT"
            result["iterations"].append(record)
            checkpoint()
            break
        if checked == z3.unknown:
            record["reason_unknown"] = solver.reason_unknown()
            result["status"] = "UNKNOWN"
            result["iterations"].append(record)
            checkpoint()
            break
        values = fractions(solver.model(), value)
        result["last_values"] = {
            owner: {good: str(amount) for good, amount in row.items()}
            for owner, row in values.items()
        }
        witnesses, minimal = find_closed_core_families(
            values, ALLOCATED_E_BASE, maximum=maximum_families_per_round,
        )
        record["minimal_common_safe_desired_counts"] = {
            owner: len(rows) for owner, rows in minimal.items()
        }
        if not witnesses:
            result["status"] = "SAT_NO_GENERALIZED_PI"
            result["values"] = {
                owner: {good: str(amount) for good, amount in row.items()}
                for owner, row in values.items()
            }
            result["iterations"].append(record)
            checkpoint()
            break
        fresh = []
        for witness in witnesses:
            signature = cycle_signature(witness)
            if signature in signatures:
                continue
            signatures.add(signature)
            fresh.append(witness)
            solver.add(generalized_pi_cut(value, witness))
        if not fresh:
            raise AssertionError("generalized PI batch contained no fresh cut")
        record["pi_witnesses"] = fresh
        record["pi_cycle_count"] = len(witnesses)
        record["fresh_cut_count"] = len(fresh)
        result["iterations"].append(record)
        checkpoint()
    else:
        result["status"] = "ITERATION_LIMIT"
    checkpoint()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-iterations", type=int, default=100)
    parser.add_argument("--master-only", action="store_true")
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--maximum-families-per-round", type=int, default=10000)
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.timeout_seconds, args.random_seed,
        args.maximum_iterations, negate_named_selector=not args.master_only,
        resume=args.resume,
        maximum_families_per_round=args.maximum_families_per_round,
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "iterations": len(result["iterations"]),
        "allocations": result["allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
