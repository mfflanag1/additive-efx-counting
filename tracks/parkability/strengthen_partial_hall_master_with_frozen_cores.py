#!/usr/bin/env python3
"""Inject sound frozen-core theory clauses into a radius-five Hall master."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .run_partial_hall_utilitarian_cegar import base_stabilizer
except ImportError:
    from anneal import atomic_json
    from run_partial_hall_utilitarian_cegar import base_stabilizer


SCHEMA = "partial-hall-frozen-core-strengthening-v1"


def mask_sum(values, agent, mask, goods):
    return z3.Sum(
        *(values[agent][good] for good in range(goods) if mask & (1 << good))
    )


def expression(record, values, fixed_masks, goods):
    kind = record["kind"]
    if kind == "row_normalization":
        return z3.Sum(*values[record["agent"]]) == 1, True
    if kind == "strict_positivity":
        return values[record["agent"]][record["good"]] > 0, True
    if kind in {"eligible_comparison", "true_edge_comparison"}:
        return (
            mask_sum(values, record["agent"], record["left_mask"], goods)
            >= mask_sum(values, record["agent"], record["right_mask"], goods),
            False,
        )
    if kind in {"ineligible_witness", "false_edge_witness"}:
        return (
            mask_sum(values, record["agent"], record["left_mask"], goods)
            < mask_sum(values, record["agent"], record["right_mask"], goods),
            False,
        )
    if kind == "maximality":
        base_score = z3.Sum(
            *(mask_sum(values, agent, fixed_masks[agent], goods) for agent in range(4))
        )
        rival_score = z3.Sum(
            *(
                mask_sum(values, agent, record["masks"][agent], goods)
                for agent in range(4)
            )
        )
        return base_score >= rival_score, False
    raise ValueError(f"unsupported core kind: {kind}")


def permute_mask(mask, permutation):
    image = 0
    for good, image_good in enumerate(permutation):
        if mask & (1 << good):
            image |= 1 << image_good
    return image


def permute_record(record, permutation):
    image = dict(record)
    if "good" in image:
        image["good"] = permutation[image["good"]]
    for key in ("left_mask", "right_mask"):
        if key in image:
            image[key] = permute_mask(image[key], permutation)
    if "masks" in image:
        image["masks"] = [
            permute_mask(mask, permutation) for mask in image["masks"]
        ]
    if "floater" in image:
        image["floater"] = permutation[image["floater"]]
    return image


def run(source, cores, output, manifest, symmetry_close=False):
    source_text = source.read_text()
    solver = z3.Solver()
    solver.from_string(source_text)
    goods = 9
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(goods)]
        for agent in range(4)
    ]
    records = []
    learned_clauses = set()
    stabilizer = base_stabilizer(((6, 7), (1, 2, 3), (0, 4), (5,)), goods)
    for core_path in cores:
        document = json.loads(core_path.read_text())
        if document.get("status") != "UNSAT":
            raise ValueError(f"core is not UNSAT: {core_path}")
        core = document.get("deletion_irreducible_unsat_core") or document["unsat_core"]
        fixed_masks = tuple(map(int, document["fixed_state"]["masks"]))
        permutations = stabilizer if symmetry_close else (tuple(range(goods)),)
        added = 0
        for permutation in permutations:
            image_core = [permute_record(item, permutation) for item in core]
            expressions = []
            global_expressions = []
            for item in image_core:
                formula, globally_asserted = expression(
                    item, values, fixed_masks, goods
                )
                (global_expressions if globally_asserted else expressions).append(
                    formula
                )
            audit = z3.Solver()
            audit.add(*global_expressions, *expressions)
            verdict = audit.check()
            if verdict != z3.unsat:
                raise RuntimeError(
                    f"core image does not replay independently: {core_path}: {verdict}"
                )
            clause = z3.Not(z3.And(*expressions))
            key = clause.sexpr()
            if key not in learned_clauses:
                learned_clauses.add(key)
                solver.add(clause)
                added += 1
        records.append(
            {
                "core": str(core_path),
                "core_sha256": hashlib.sha256(core_path.read_bytes()).hexdigest(),
                "core_size": len(core),
                "global_assumption_count": len(global_expressions),
                "clause_literal_count": len(expressions),
                "symmetry_image_count": len(permutations),
                "distinct_clause_count": added,
                "independent_verdict": str(verdict),
            }
        )
    output.write_text(solver.to_smt2())
    artifact = {
        "schema": SCHEMA,
        "status": "EXACT_STRENGTHENING",
        "meaning": (
            "Each injected clause is the negation of a conjunction proved "
            "infeasible under row normalization and strict positivity, both "
            "already asserted by the source master. Satisfiability is "
            "therefore preserved."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "output": str(output),
        "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "seed_core_count": len(records),
        "injected_clause_count": len(learned_clauses),
        "symmetry_close": symmetry_close,
        "records": records,
    }
    atomic_json(manifest, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--core", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--symmetry-close", action="store_true")
    args = parser.parse_args()
    artifact = run(
        args.source,
        args.core,
        args.output,
        args.manifest,
        args.symmetry_close,
    )
    print(json.dumps(artifact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
