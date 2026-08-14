#!/usr/bin/env python3
"""Lift the seven-endpoint R3 core to arbitrary named packet tails.

Each of the twelve named symbols is treated as a nonempty physical packet.
For every observer it has an independent total ``v`` and least-good value
``ell``.  Tails of unions of whole named packets are therefore exact:

    tau_i(union P) = sum_P v_i(P) - min_P ell_i(P).

Only 0 < ell <= v is imposed (and ell=v for singleton charity P).  This is a
relaxation of physical realizability because a genuine nonsingleton packet
also has v >= 2*ell.  Hence UNSAT under this relaxation proves the whole-
named-packet tail lift for every physically realizable packet cardinality.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, PACKETS, SUPPORT_STATE
from .run_full_capture_rank_three_cegar import FORMS


ROOT = Path(__file__).resolve().parents[2]
TARGETS = (*OWNERS, "charity")


def total(value, observer, pieces):
    pieces = tuple(pieces)
    return z3.Sum(*(value[piece, observer] for piece in pieces)) if pieces else z3.RealVal(0)


def minimum(expressions):
    expressions = tuple(expressions)
    if not expressions:
        raise ValueError("minimum of empty family")
    result = expressions[0]
    for expression in expressions[1:]:
        result = z3.If(result <= expression, result, expression)
    return result


def tail(value, least, observer, pieces):
    pieces = tuple(pieces)
    if not pieces:
        return z3.RealVal(0)
    return total(value, observer, pieces) - minimum(
        least[piece, observer] for piece in pieces
    )


def response(value, least, source, pieces):
    pieces = tuple(pieces)
    return z3.And(
        total(value, source, pieces) > 1,
        *(tail(value, least, observer, pieces) <= 1 for observer in OWNERS),
    )


def nonempty_subsets(pieces):
    pieces = tuple(pieces)
    for size in range(1, len(pieces) + 1):
        yield from itertools.combinations(pieces, size)


def ordinary_pi_free(value, least):
    edges = {}
    for source in OWNERS:
        for target in OWNERS:
            if source == target:
                continue
            edges[source, target] = z3.Or(*(
                response(value, least, source, pieces)
                for pieces in nonempty_subsets(ALLOCATED_E_BASE[target])
            ))
    constraints = []
    for length in range(2, len(OWNERS) + 1):
        for subset in itertools.combinations(OWNERS, length):
            anchor = min(subset)
            for rest in itertools.permutations(owner for owner in subset if owner != anchor):
                cycle = (anchor, *rest)
                constraints.append(z3.Not(z3.And(*(
                    edges[cycle[index], cycle[(index + 1) % length]]
                    for index in range(length)
                ))))
    return constraints


def generalized_self_pi_free(value, least):
    constraints = []
    charity = tuple(ALLOCATED_E_BASE["charity"])
    for owner in OWNERS:
        universe = (*ALLOCATED_E_BASE[owner], *charity)
        for pieces in nonempty_subsets(universe):
            if set(pieces) & set(charity):
                constraints.append(z3.Not(response(value, least, owner, pieces)))
    return constraints


def anchored_pi_free(value, least):
    fixed = {"r": PACKETS["A"], "q": PACKETS["Q"], "s": PACKETS["E"]}
    base_owner = {
        piece: owner for owner, pieces in ALLOCATED_E_BASE.items() for piece in pieces
    }
    excluded = set()
    for source in OWNERS:
        available = tuple(owner for owner in fixed if owner != source)
        for size in range(1, len(available) + 1):
            for fixed_subset in itertools.combinations(available, size):
                vertices = set(fixed_subset) | {source}
                fixed_union = set().union(*(set(fixed[owner]) for owner in fixed_subset))
                if any(base_owner[piece] not in vertices | {"charity"} for piece in fixed_union):
                    continue
                complement = tuple(piece for piece in GOODS if piece not in fixed_union)
                for pieces in nonempty_subsets(complement):
                    if all(base_owner[piece] in vertices | {"charity"} for piece in pieces):
                        excluded.add((source, tuple(sorted(pieces))))
    return [z3.Not(response(value, least, source, pieces))
            for source, pieces in sorted(excluded)]


def pairwise_pi_free(value, least):
    constraints = []
    for left, right in itertools.combinations(OWNERS, 2):
        allowed = tuple(
            piece for owner in (left, right, "charity")
            for piece in ALLOCATED_E_BASE[owner]
        )
        for assignment in itertools.product(range(3), repeat=len(allowed)):
            left_core = tuple(piece for piece, slot in zip(allowed, assignment) if slot == 1)
            right_core = tuple(piece for piece, slot in zip(allowed, assignment) if slot == 2)
            if left_core and right_core:
                constraints.append(z3.Not(z3.And(
                    response(value, least, left, left_core),
                    response(value, least, right, right_core),
                )))
    return constraints


def response_edges(value, least):
    current = {owner: total(value, owner, SUPPORT_STATE[owner]) for owner in OWNERS}
    edges = {}
    for source in OWNERS:
        for target in TARGETS:
            if source == target:
                edges[source, target] = z3.BoolVal(False)
                continue
            alternatives = []
            for pieces in nonempty_subsets(SUPPORT_STATE[target]):
                alternatives.append(response(value, least, source, pieces))
                alternatives.append(z3.And(
                    total(value, source, pieces) > current[source],
                    *(tail(value, least, observer, pieces) <= current[observer]
                      for observer in OWNERS),
                ))
            edges[source, target] = z3.Or(*alternatives) if alternatives else z3.BoolVal(False)
    return edges


def rank_four_exists(edges):
    return z3.Or(*(
        z3.And(*(edges[source, target] for source, target in zip(OWNERS, targets)))
        for targets in itertools.permutations(TARGETS, len(OWNERS))
    ))


def endpoint_efx(value, least, allocation):
    utility = {owner: total(value, owner, allocation[owner]) for owner in OWNERS}
    return z3.And(*(
        utility[observer] >= tail(value, least, observer, allocation[target])
        for observer in OWNERS for target in OWNERS if target != observer
    ))


def build_packet_master():
    value = {(piece, observer): z3.Real(f"pl_v_{piece}_{observer}")
             for piece in GOODS for observer in OWNERS}
    least = {(piece, observer): z3.Real(f"pl_l_{piece}_{observer}")
             for piece in GOODS for observer in OWNERS}
    solver = z3.SolverFor("QF_LRA")
    for key in value:
        solver.add(value[key] > 0, value[key] < 16)
        solver.add(least[key] > 0, least[key] <= value[key])
    # The support charity P={p} is a physical singleton.
    for observer in OWNERS:
        solver.add(least["p", observer] == value["p", observer])

    for owner in OWNERS:
        solver.add(total(value, owner, ALLOCATED_E_BASE[owner]) == 1)
        solver.add(total(value, owner, ALLOCATED_E_BASE["charity"]) <= 1)
        for target in OWNERS:
            if target != owner:
                solver.add(tail(value, least, owner, ALLOCATED_E_BASE[target]) <= 1)
    solver.add(*ordinary_pi_free(value, least))
    solver.add(*generalized_self_pi_free(value, least))
    for source, packet in (("r", "A"), ("q", "Q"), ("s", "E")):
        solver.add(response(value, least, source, PACKETS[packet]))
    solver.add(*anchored_pi_free(value, least))
    solver.add(*pairwise_pi_free(value, least))

    selected = set(PACKETS["A"]) | set(PACKETS["Q"]) | set(PACKETS["E"])
    complement = tuple(piece for piece in GOODS if piece not in selected)
    for pieces in nonempty_subsets(complement):
        solver.add(z3.Not(response(value, least, "d", pieces)))

    solver.add(response(value, least, "d", PACKETS["Q"]))
    for piece in PACKETS["Q"]:
        solver.add(total(
            value, "d",
            (*tuple(other for other in PACKETS["Q"] if other != piece), *PACKETS["H"]),
        ) <= 1)
    d_floor = total(value, "d", PACKETS["W"])
    solver.add(d_floor < tail(value, least, "d", PACKETS["A"]))
    solver.add(d_floor >= tail(value, least, "d", PACKETS["Q"]))
    solver.add(d_floor >= tail(value, least, "d", PACKETS["E"]))
    solver.add(d_floor >= total(value, "d", PACKETS["P"]))

    edges = response_edges(value, least)
    solver.add(z3.Not(rank_four_exists(edges)))
    expected = set(FORMS[2])
    for source in OWNERS:
        for target in TARGETS:
            if source == target:
                continue
            solver.add(edges[source, target] if (source, target) in expected
                       else z3.Not(edges[source, target]))
    return solver, value, least


def serialize(model, variables):
    return {
        observer: {
            piece: str(model.eval(variables[piece, observer], model_completion=True))
            for piece in GOODS
        }
        for observer in OWNERS
    }


def run(core_source: Path, output: Path, timeout_seconds: int, random_seed: int):
    core_source = core_source.resolve()
    core = json.loads(core_source.read_text())
    signatures = [
        tuple((source, tuple(pieces)) for source, pieces in signature)
        for signature in core["pi_signatures"]
    ]
    allocations = core["allocations"]
    solver, value, least = build_packet_master()
    for signature in signatures:
        solver.add(z3.Or(*(
            z3.Not(response(value, least, source, pieces))
            for source, pieces in signature
        )))
    for allocation in allocations:
        solver.add(z3.Not(endpoint_efx(value, least, allocation)))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    started = time.monotonic()
    status = solver.check()
    result = {
        "schema": "allocated-e-seven-endpoint-packet-tail-lift-v1",
        "status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "elapsed_seconds": time.monotonic() - started,
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "pi_clause_count": len(signatures),
        "endpoint_count": len(allocations),
        "packet_model": "independent total and least-good value per named piece/observer",
        "physical_relaxation": "0 < least <= total; singleton equality imposed only for P",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "UNSAT proves the seven-endpoint whole-named-packet tail lift under "
            "a relaxation containing every physically realizable cardinality. "
            "It does not show that every saturated state admits the named piece "
            "decomposition or cover arbitrary subpacket responses. SAT may be "
            "spurious unless total/least pairs are physically realizable."
        ),
    }
    if status == z3.sat:
        model = solver.model()
        result["totals"] = serialize(model, value)
        result["least_values"] = serialize(model, least)
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=65537)
    args = parser.parse_args()
    result = run(args.core_source, args.output, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "pi_clauses": result["pi_clause_count"],
        "endpoints": result["endpoint_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
