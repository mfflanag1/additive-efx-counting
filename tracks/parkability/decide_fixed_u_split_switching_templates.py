#!/usr/bin/env python3
"""Exact decision of the two terminal split-switching allocation families.

Every role except the designated split role is treated cap-free through its
immutable total and minimum.  A labelled realization of the split role is
accepted iff at least one assignment of its goods to the template's two
recipient bundles satisfies every individual-deletion EFX inequality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")
TEMPLATES = {
    "A_split_a1": {
        "split_role": "a1",
        "recipients": ("d", "q"),
        "whole_roles": {
            "d": ("h", "m", "gq", "gr"),
            "q": ("j",),
            "r": ("a0", "k", "q0"),
            "s": ("l", "e", "p"),
        },
    },
    "B_split_k": {
        "split_role": "k",
        "recipients": ("q", "r"),
        "whole_roles": {
            "d": ("l", "m", "gq", "gr"),
            "q": ("j", "q0", "p"),
            "r": ("a0", "a1"),
            "s": ("h", "e"),
        },
    },
}


def rv(amount):
    amount = Fraction(amount)
    return z3.RealVal(f"{amount.numerator}/{amount.denominator}")


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def load_profile(path):
    raw = json.loads(path.read_text())
    totals = {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw["profile_totals"].items()
    }
    minima = {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw["profile_minima"].items()
    }
    return raw, totals, minima


def realization_domain(solver, variables, role, cardinality, totals, minima):
    for observer in OWNERS:
        row = [variables[observer, index] for index in range(cardinality)]
        minimum = rv(minima[observer][role])
        solver.add(*(entry >= minimum for entry in row))
        solver.add(z3.Sum(*row) == rv(totals[observer][role]))
        solver.add(z3.Or(*(entry == minimum for entry in row)))


def assignment_efx_formula(template, mask, cardinality, variables, totals, minima):
    """Necessary-and-sufficient EFX inequalities for one packet assignment."""
    first, second = template["recipients"]
    assigned = {
        first: tuple(index for index in range(cardinality) if mask & (1 << index)),
        second: tuple(index for index in range(cardinality) if not mask & (1 << index)),
    }
    bundle_total = {}
    deletion_values = {}
    for observer in OWNERS:
        for owner in OWNERS:
            whole = template["whole_roles"][owner]
            split_indices = assigned.get(owner, ())
            terms = [rv(totals[observer][role]) for role in whole]
            terms.extend(variables[observer, index] for index in split_indices)
            bundle_total[observer, owner] = z3.Sum(*terms)
            # For a whole role, checking its prescribed minimum is equivalent
            # to checking deletion of every one of its physical goods.
            candidates = [rv(minima[observer][role]) for role in whole]
            candidates.extend(variables[observer, index] for index in split_indices)
            assert candidates
            deletion_values[observer, owner] = candidates
    inequalities = []
    for observer in OWNERS:
        own = bundle_total[observer, observer]
        for target in OWNERS:
            if target == observer:
                continue
            gross = bundle_total[observer, target]
            inequalities.extend(
                own >= gross - deletion
                for deletion in deletion_values[observer, target]
            )
    return z3.And(*inequalities)


def family_formula(template, cardinality, variables, totals, minima):
    return z3.Or(*(
        assignment_efx_formula(
            template, mask, cardinality, variables, totals, minima
        )
        for mask in range(1 << cardinality)
    ))


def exact_fraction(model, expression):
    value = model.eval(expression, model_completion=True)
    assert z3.is_rational_value(value)
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def witness_pattern(values, minima, role):
    return {
        observer: [index for index, value in enumerate(row)
                   if value == minima[observer][role]]
        for observer, row in values.items()
    }


def check_realization(values, role, totals, minima):
    cardinality = len(next(iter(values.values())))
    for observer in OWNERS:
        row = values[observer]
        assert len(row) == cardinality
        assert sum(row, Fraction()) == totals[observer][role]
        assert min(row) == minima[observer][role]


def evaluate_assignment(template, mask, values, totals, minima):
    """Independent Fraction evaluation of the same displayed inequalities."""
    cardinality = len(next(iter(values.values())))
    first, second = template["recipients"]
    assigned = {
        first: tuple(index for index in range(cardinality) if mask & (1 << index)),
        second: tuple(index for index in range(cardinality) if not mask & (1 << index)),
    }
    minimum_slack = None
    for observer in OWNERS:
        bundle_total = {}
        candidates = {}
        for owner in OWNERS:
            whole = template["whole_roles"][owner]
            indices = assigned.get(owner, ())
            bundle_total[owner] = (
                sum((totals[observer][role] for role in whole), Fraction())
                + sum((values[observer][index] for index in indices), Fraction())
            )
            candidates[owner] = (
                [minima[observer][role] for role in whole]
                + [values[observer][index] for index in indices]
            )
            assert candidates[owner]
        for target in OWNERS:
            if target == observer:
                continue
            for deletion in candidates[target]:
                slack = bundle_total[observer] - bundle_total[target] + deletion
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
                if slack < 0:
                    return False, minimum_slack
    return True, minimum_slack


def accepted_masks(template, values, totals, minima):
    cardinality = len(next(iter(values.values())))
    return [
        mask for mask in range(1 << cardinality)
        if evaluate_assignment(template, mask, values, totals, minima)[0]
    ]


def decide_lane(template_name, cardinality, totals, minima, timeout_seconds):
    template = TEMPLATES[template_name]
    role = template["split_role"]
    variables = {
        (observer, index): z3.Real(f"{template_name}_{cardinality}_{observer}_{index}")
        for observer in OWNERS for index in range(cardinality)
    }
    solver = z3.SolverFor("QF_LRA")
    solver.set(timeout=timeout_seconds * 1000)
    realization_domain(solver, variables, role, cardinality, totals, minima)
    solver.add(z3.Not(family_formula(
        template, cardinality, variables, totals, minima
    )))
    status = solver.check()
    result = {
        "template": template_name,
        "split_role": role,
        "cardinality": cardinality,
        "assignment_count": 1 << cardinality,
        "status": str(status),
    }
    if status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    elif status == z3.sat:
        model = solver.model()
        values = {
            observer: [exact_fraction(model, variables[observer, index])
                       for index in range(cardinality)]
            for observer in OWNERS
        }
        check_realization(values, role, totals, minima)
        assert accepted_masks(template, values, totals, minima) == []
        result["counterexample_values"] = {
            observer: [str(value) for value in row]
            for observer, row in values.items()
        }
        result["minimum_witness_pattern"] = witness_pattern(
            values, minima, role
        )
    return result


def run(profile_path, output_path, timeout_seconds):
    profile, totals, minima = load_profile(profile_path)
    lanes = []
    for cardinality in range(2, 8):
        lanes.append(decide_lane(
            "A_split_a1", cardinality, totals, minima, timeout_seconds
        ))
    for cardinality in range(2, 4):
        lanes.append(decide_lane(
            "B_split_k", cardinality, totals, minima, timeout_seconds
        ))
    statuses = {lane["status"] for lane in lanes}
    if "unknown" in statuses:
        status = "UNKNOWN_LANE"
    else:
        a_universal = all(
            lane["status"] == "unsat" for lane in lanes
            if lane["template"] == "A_split_a1"
        )
        b_universal = all(
            lane["status"] == "unsat" for lane in lanes
            if lane["template"] == "B_split_k"
        )
        status = (
            "UNSAT_NO_SPLIT_SWITCHING_SELECTOR_COUNTERMODEL"
            if a_universal or b_universal
            else "SAT_SPLIT_SWITCHING_SELECTOR_COUNTERMODEL"
        )
    result = {
        "schema": "fixed-u-split-switching-template-decision-v1",
        "status": status,
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "templates": TEMPLATES,
        "exact_acceptance_criterion": (
            "For each labelled subset assignment, every ordered observer-target "
            "pair satisfies own bundle total minus target bundle total plus each "
            "split-good value in the target and each whole-role prescribed minimum "
            "in the target >= 0. Their conjunction is necessary and sufficient for "
            "EFX; the family is the disjunction over all 2^cardinality assignments."
        ),
        "logical_factorization": (
            "A depends only on a1 and B only on k. Hence forall(a1,k), A(a1) or "
            "B(k) iff forall(a1) A(a1) or forall(k) B(k)."
        ),
        "lanes": lanes,
        "claim_boundary": (
            "SAT refutes only coverage by templates A and B. It is not a four-edge "
            "EFX countermodel until an unrestricted allocation oracle returns UNSAT."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    result = run(args.profile, args.output, args.timeout_seconds)
    print(json.dumps({
        "status": result["status"],
        "lanes": [
            [lane["template"], lane["cardinality"], lane["status"]]
            for lane in result["lanes"]
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
