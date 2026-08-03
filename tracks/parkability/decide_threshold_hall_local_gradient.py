#!/usr/bin/env python3
"""Decide a fixed 4x9 threshold--Hall local-gradient cell in QF_LRA."""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .fast_count import FastParkability
except ImportError:
    from anneal import atomic_json
    from fast_count import FastParkability


SCHEMA = "threshold-hall-local-gradient-4x9-v1"
BASE = ((0, 1), (2, 3), (4, 5), (6, 7))
FLOATER = 8


def minimum(terms):
    terms = tuple(terms)
    result = terms[0]
    for term in terms[1:]:
        result = z3.If(result <= term, result, term)
    return result


def maximum(terms):
    terms = tuple(terms)
    result = terms[0]
    for term in terms[1:]:
        result = z3.If(result >= term, result, term)
    return result


def total(row, bundle):
    return z3.Sum(*(row[good] for good in bundle))


def threshold(row, bundle):
    return total(row, bundle) - minimum(row[good] for good in bundle)


def eligible(values, bundles, floater):
    constraints = []
    for observer in range(4):
        own = total(values[observer], bundles[observer])
        constraints.append(own >= values[observer][floater])
        constraints.extend(
            own >= threshold(values[observer], bundles[target])
            for target in range(4)
            if target != observer
        )
    return z3.And(*constraints)


def completion_margins(values, bundles, floater):
    margins = []
    for host in range(4):
        complete = list(bundles)
        complete[host] = tuple(sorted((*complete[host], floater)))
        complete = tuple(complete)
        for permutation in itertools.permutations(range(4)):
            observer_slacks = []
            for observer in range(4):
                assigned = permutation[observer]
                required = maximum(
                    threshold(values[observer], complete[target])
                    for target in range(4)
                    if target != assigned
                )
                observer_slacks.append(
                    total(values[observer], complete[assigned]) - required
                )
            margins.append(minimum(observer_slacks))
    return tuple(margins)


def completion_margin(values, bundles, floater):
    return maximum(completion_margins(values, bundles, floater))


def rational(value):
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def integer_values(model, values):
    rows = [
        [rational(model.eval(entry, model_completion=True)) for entry in row]
        for row in values
    ]
    integers = []
    for row in rows:
        denominator = math.lcm(*(entry.denominator for entry in row))
        scaled = [int(entry * denominator) for entry in row]
        divisor = math.gcd(*scaled)
        integers.append([entry // divisor for entry in scaled])
    return integers


def fixed_masks():
    return tuple(sum(1 << good for good in bundle) for bundle in BASE)


def global_audit(raw_values):
    evaluator = FastParkability(4, 9)
    landscape = evaluator.partial_linear_potential_landscape(
        raw_values,
        potential="normalized_threshold",
    )
    masks = fixed_masks()
    fixed = next(
        (
            winner
            for winner in landscape["maximizers"]
            if winner["floater"] == FLOATER
            and tuple(
                int(mask)
                for mask in evaluator.base_masks[FLOATER][winner["base_index"]]
            )
            == masks
        ),
        None,
    )
    return {
        "eligible_state_count": landscape["eligible_base_count"],
        "maximum_threshold_state_count": landscape["maximizer_count"],
        "hall_insertable_maximum_threshold_state_count": landscape[
            "hall_insertable_maximizer_count"
        ],
        "fixed_base_is_global_threshold_maximum": fixed is not None,
        "fixed_base_global_record": fixed,
    }


def run(
    output: Path,
    smt2: Path,
    timeout_seconds: int,
    base_witness_index: int | None,
):
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for row in values:
        solver.add(z3.Sum(*row) == 1)
        solver.add(*(entry > 0 for entry in row))
    solver.add(eligible(values, BASE, FLOATER))

    base_margins = completion_margins(values, BASE, FLOATER)
    if base_witness_index is None:
        base_margin = maximum(base_margins)
    else:
        if not 0 <= base_witness_index < len(base_margins):
            raise ValueError("base witness index must lie in [0,95]")
        base_margin = base_margins[base_witness_index]
        solver.add(*(base_margin >= margin for margin in base_margins))
    solver.add(base_margin < 0)

    local_constraints = 0
    for owner, bundle in enumerate(BASE):
        old_threshold = threshold(values[owner], bundle)
        for outgoing in bundle:
            is_owner_minimum = z3.And(
                *(
                    values[owner][outgoing] <= values[owner][other]
                    for other in bundle
                )
            )
            swapped = list(BASE)
            swapped[owner] = tuple(
                sorted(
                    good for good in (*bundle, FLOATER) if good != outgoing
                )
            )
            swapped = tuple(swapped)
            swap_eligible = eligible(values, swapped, outgoing)
            premise = z3.And(is_owner_minimum, swap_eligible)
            solver.add(
                z3.Implies(
                    premise,
                    threshold(values[owner], swapped[owner]) <= old_threshold,
                )
            )
            for swap_margin in completion_margins(values, swapped, outgoing):
                solver.add(z3.Implies(premise, swap_margin <= base_margin))
            local_constraints += 97

    verdict = solver.check()
    smt2.write_text(solver.to_smt2())
    model = solver.model() if verdict == z3.sat else None
    integers = integer_values(model, values) if model is not None else None
    artifact = {
        "schema": SCHEMA,
        "status": (
            "LOCAL_GRADIENT_COUNTERMODEL"
            if verdict == z3.sat
            else "CANONICAL_LOCAL_GRADIENT_FORCED"
            if verdict == z3.unsat
            else "UNKNOWN"
        ),
        "meaning": (
            "SAT refutes the fixed-cell local-gradient statement, but refutes "
            "the global threshold selector only if the exact global audit says "
            "the fixed base is globally threshold-maximal. UNSAT proves only "
            "the canonical four-pair local cell."
        ),
        "base_bundles": [list(bundle) for bundle in BASE],
        "floater": FLOATER,
        "local_implication_count": local_constraints,
        "base_witness_index": base_witness_index,
        "solver_verdict": str(verdict),
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "timeout_seconds": timeout_seconds,
        "values": integers,
        "global_audit": global_audit(integers) if integers is not None else None,
        "smt2": str(smt2),
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--base-witness-index", type=int)
    args = parser.parse_args()
    result = run(
        args.output,
        args.smt2,
        args.timeout_seconds,
        args.base_witness_index,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
