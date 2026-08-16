#!/usr/bin/env python3
"""CEGAR for a cap-free one-least-good split four-edge selector.

Each selected nonsingleton named role C may be split as {g} and C\{g}, where
g is a least physical good for every observer in the totals/minima abstraction.
Both pieces are conservatively assigned least-good value M.  Hence any EFX
allocation found by the symbolic cut is valid for every physical realization
of those totals/minima, not merely for the canonical two-good realization.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import support_supplier
from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


def piece_value(total, minimum, observer, piece):
    role, kind = piece
    if kind == "whole":
        return total[role, observer]
    if kind == "low":
        return minimum[role, observer]
    if kind == "rest":
        return total[role, observer] - minimum[role, observer]
    raise ValueError(kind)


def numeric_piece_value(totals, minima, observer, piece):
    role, kind = piece
    if kind == "whole":
        return totals[observer][role]
    if kind == "low":
        return minima[observer][role]
    return totals[observer][role] - minima[observer][role]


def pieces_for(split_role):
    return tuple(
        piece
        for role in GOODS
        for piece in (
            ((role, "low"), (role, "rest"))
            if role == split_role else ((role, "whole"),)
        )
    )


def numeric_oracle(totals, minima, split_role, edge_cap=4):
    pieces = pieces_for(split_role)
    supplier = support_supplier()
    x = {(piece, owner): z3.Bool(f"o_{piece[0]}_{piece[1]}_{owner}")
         for piece in pieces for owner in OWNERS}
    edge = {(source, target): z3.Bool(f"oe_{source}_{target}")
            for source in SUPPORT_STATE for target in OWNERS if source != target}
    solver = z3.Solver()
    for piece in pieces:
        solver.add(z3.PbEq([(x[piece, owner], 1) for owner in OWNERS], 1))
        source = supplier[piece[0]]
        for target in OWNERS:
            if target != source:
                solver.add(z3.Implies(x[piece, target], edge[source, target]))
    solver.add(z3.PbLe([(flag, 1) for flag in edge.values()], edge_cap))
    utility = {
        (observer, target): z3.Sum(*(
            z3.If(x[piece, target], z3.RealVal(str(numeric_piece_value(
                totals, minima, observer, piece))), z3.RealVal(0))
            for piece in pieces
        ))
        for observer in OWNERS for target in OWNERS
    }
    for observer in OWNERS:
        for target in OWNERS:
            if target == observer:
                continue
            for piece in pieces:
                # M is a valid lower bound on the minimum physical good in
                # either the isolated least-good piece or its complement.
                deletion_floor = minima[observer][piece[0]]
                solver.add(z3.Implies(
                    x[piece, target],
                    utility[observer, observer] >= utility[observer, target]
                    - z3.RealVal(str(deletion_floor)),
                ))
    if solver.check() != z3.sat:
        return None
    model = solver.model()
    return {
        owner: [list(piece) for piece in pieces if z3.is_true(model.eval(x[piece, owner]))]
        for owner in OWNERS
    }


def symbolic_efx(allocation, total, minimum, split_role):
    bundles = {
        owner: [tuple(piece) for piece in allocation[owner]] for owner in OWNERS
    }
    utility = {
        (observer, target): z3.Sum(*(
            piece_value(total, minimum, observer, piece)
            for piece in bundles[target]
        )) if bundles[target] else z3.RealVal(0)
        for observer in OWNERS for target in OWNERS
    }
    clauses = []
    if split_role is not None:
        clauses.append(z3.And(*(
            2 * minimum[split_role, observer] <= total[split_role, observer]
            for observer in OWNERS
        )))
    for observer in OWNERS:
        for target in OWNERS:
            if target == observer:
                continue
            for role, _ in bundles[target]:
                clauses.append(
                    utility[observer, observer] >= utility[observer, target]
                    - minimum[role, observer]
                )
    return z3.And(*clauses)


def topology(allocation):
    supplier = support_supplier()
    return sorted({
        (supplier[role], owner)
        for owner, pieces in allocation.items()
        for role, _ in pieces
        if supplier[role] != owner
    })


def run(output, form_index, maximum_rounds, timeout_seconds, random_seed):
    solver, total, minimum = build_physical_master(form_index)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    result = {
        "schema": "exact-response-one-minimum-split-cegar-v1",
        "status": "RUNNING",
        "form_index": form_index,
        "edge_cap": 4,
        "split_cap": 1,
        "split_semantics": (
            "one named multi-good role may be split into a least physical good "
            "and its complement; both pieces use the original role minimum as "
            "a conservative physical deletion floor"
        ),
        "rounds": [],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "UNSAT proves the one-minimum-split selector for the declared exact "
            "response chart. SAT refutes only that selector, not arbitrary packet "
            "splits or the universal fixed-U theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for iteration in range(maximum_rounds):
        status = solver.check()
        if status != z3.sat:
            result["status"] = "UNSAT_ONE_MINIMUM_SPLIT_CHART_THEOREM" if status == z3.unsat else "UNKNOWN"
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result
        model = solver.model()
        totals = {o: {g: Fraction(str(model.eval(total[g, o], model_completion=True))) for g in GOODS} for o in OWNERS}
        minima = {o: {g: Fraction(str(model.eval(minimum[g, o], model_completion=True))) for g in GOODS} for o in OWNERS}
        multi = [g for g in GOODS if all(totals[o][g] >= 2 * minima[o][g] for o in OWNERS)]
        witness = None
        selected_split = None
        for split_role in (None, *multi):
            allocation = numeric_oracle(totals, minima, split_role)
            if allocation is not None:
                witness = allocation
                selected_split = split_role
                break
        if witness is None:
            result["status"] = "SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION"
            result["countermodel_totals"] = serialize(model, total)
            result["countermodel_minima"] = serialize(model, minimum)
            result["countermodel_iteration"] = iteration
            output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result
        solver.add(z3.Not(symbolic_efx(witness, total, minimum, selected_split)))
        result["rounds"].append({
            "iteration": iteration,
            "split_role": selected_split,
            "allocation": witness,
            "topology": [list(edge) for edge in topology(witness)],
            "totals": serialize(model, total),
            "minima": serialize(model, minimum),
        })
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    result["status"] = "ITERATION_LIMIT"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--maximum-rounds", type=int, default=50)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(args.output, args.form_index, args.maximum_rounds,
                 args.timeout_seconds, args.random_seed)
    print(json.dumps({"status": result["status"], "rounds": len(result["rounds"])}, indent=2))


if __name__ == "__main__":
    main()
