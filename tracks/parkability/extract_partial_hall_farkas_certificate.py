#!/usr/bin/env python3
"""Extract a rational Farkas certificate from a frozen Hall-cell core."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "partial-hall-farkas-certificate-v1"


def mask_vector(agent, mask, sign, n, m):
    vector = [Fraction() for _ in range(n * m)]
    for good in range(m):
        if mask & (1 << good):
            vector[agent * m + good] += sign
    return vector


def add_vectors(*vectors):
    return [sum(items, Fraction()) for items in zip(*vectors)]


def constraint(record, fixed_masks, n, m):
    kind = record["kind"]
    zero = [Fraction() for _ in range(n * m)]
    if kind == "row_normalization":
        agent = record["agent"]
        vector = zero[:]
        for good in range(m):
            vector[agent * m + good] = Fraction(1)
        return vector, Fraction(-1), "equality"
    if kind == "strict_positivity":
        vector = zero[:]
        vector[record["agent"] * m + record["good"]] = Fraction(1)
        return vector, Fraction(), "strict"
    if kind in {"eligible_comparison", "true_edge_comparison"}:
        return (
            add_vectors(
                mask_vector(record["agent"], record["left_mask"], 1, n, m),
                mask_vector(record["agent"], record["right_mask"], -1, n, m),
            ),
            Fraction(),
            "weak",
        )
    if kind in {"ineligible_witness", "false_edge_witness"}:
        return (
            add_vectors(
                mask_vector(record["agent"], record["right_mask"], 1, n, m),
                mask_vector(record["agent"], record["left_mask"], -1, n, m),
            ),
            Fraction(),
            "strict",
        )
    if kind == "maximality":
        rival_masks = record["masks"]
        vectors = []
        for agent in range(n):
            vectors.append(mask_vector(agent, fixed_masks[agent], 1, n, m))
            vectors.append(mask_vector(agent, rival_masks[agent], -1, n, m))
        return add_vectors(*vectors), Fraction(), "weak"
    raise ValueError(f"unsupported core constraint kind: {kind}")


def rational(value):
    value = z3.simplify(value)
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def public_fraction(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def run(source, output):
    document = json.loads(source.read_text())
    records = document.get("deletion_irreducible_unsat_core") or document["unsat_core"]
    fixed_masks = tuple(map(int, document["fixed_state"]["masks"]))
    n = len(fixed_masks)
    m = 9
    rows = [constraint(record, fixed_masks, n, m) for record in records]
    multipliers = [z3.Real(f"lambda_{index}") for index in range(len(rows))]
    solver = z3.Solver()
    for multiplier, (_, _, relation) in zip(multipliers, rows):
        if relation != "equality":
            solver.add(multiplier >= 0)
    for coordinate in range(n * m):
        solver.add(
            z3.Sum(
                *(
                    multiplier * z3.RealVal(vector[coordinate].numerator)
                    / z3.RealVal(vector[coordinate].denominator)
                    for multiplier, (vector, _, _) in zip(multipliers, rows)
                )
            )
            == 0
        )
    solver.add(
        z3.Sum(
            *(
                multiplier * z3.RealVal(constant.numerator)
                / z3.RealVal(constant.denominator)
                for multiplier, (_, constant, _) in zip(multipliers, rows)
            )
        )
        == 0
    )
    solver.add(
        z3.Sum(
            *(
                multiplier
                for multiplier, (_, _, relation) in zip(multipliers, rows)
                if relation == "strict"
            )
        )
        == 1
    )
    if solver.check() != z3.sat:
        raise RuntimeError("core has no normalized Farkas multiplier certificate")
    model = solver.model()
    weights = [rational(model.eval(item, model_completion=True)) for item in multipliers]
    combined_vector = [
        sum(weight * vector[index] for weight, (vector, _, _) in zip(weights, rows))
        for index in range(n * m)
    ]
    combined_constant = sum(
        weight * constant for weight, (_, constant, _) in zip(weights, rows)
    )
    strict_weight = sum(
        weight
        for weight, (_, _, relation) in zip(weights, rows)
        if relation == "strict"
    )
    if any(combined_vector) or combined_constant != 0 or strict_weight <= 0:
        raise RuntimeError("invalid extracted Farkas certificate")
    terms = [
        {
            "constraint": record,
            "relation": relation,
            "multiplier": public_fraction(weight),
        }
        for record, (_, _, relation), weight in zip(records, rows, weights)
        if weight
    ]
    artifact = {
        "schema": SCHEMA,
        "status": "EXACT_FARKAS_CONTRADICTION",
        "meaning": (
            "The weighted sum of the listed weak/strict inequalities and "
            "equalities is identically zero, while the total multiplier on "
            "strict inequalities is positive. Hence the frozen core is "
            "infeasible."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "core_constraint_count": len(records),
        "nonzero_multiplier_count": len(terms),
        "strict_multiplier_sum": public_fraction(strict_weight),
        "combined_constant": public_fraction(combined_constant),
        "combined_vector_is_zero": not any(combined_vector),
        "terms": terms,
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = run(args.source, args.output)
    print(json.dumps(artifact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
