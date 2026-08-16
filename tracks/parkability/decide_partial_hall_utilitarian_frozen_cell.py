#!/usr/bin/env python3
"""Decide a frozen eligibility/Hall cell around a near-maximal obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import numbers
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import candidate_partitions
    from .fast_count import FastParkability
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import candidate_partitions
    from fast_count import FastParkability


SCHEMA = "partial-hall-utilitarian-frozen-cell-v1"


def load_seed(path: Path):
    if path.suffix == ".jsonl":
        lines = [line for line in path.read_text().splitlines() if line.strip()]
        document = json.loads(lines[-1])
    else:
        document = json.loads(path.read_text())
    return document, [list(map(int, row)) for row in document["values"]]


def mask_goods(mask: int, goods: int):
    return tuple(good for good in range(goods) if mask & (1 << good))


def value(integer_values, agent: int, mask: int):
    return sum(
        integer_values[agent][good]
        for good in range(len(integer_values[agent]))
        if mask & (1 << good)
    )


def symbolic_value(variables, agent: int, mask: int):
    return z3.Sum(
        *(variables[agent][good] for good in mask_goods(mask, len(variables[agent])))
    )


def eligibility_comparisons(masks, floater, goods):
    comparisons = []
    for agent, own in enumerate(masks):
        for target, target_mask in enumerate(masks):
            if target == agent:
                continue
            for removed in mask_goods(target_mask, goods):
                comparisons.append((agent, own, target_mask & ~(1 << removed)))
        comparisons.append((agent, own, 1 << floater))
    return tuple(comparisons)


def edge_comparisons(partition, agent, bundle, goods):
    own = sum(1 << good for good in partition[bundle])
    comparisons = []
    for target, target_bundle in enumerate(partition):
        if target == bundle:
            continue
        target_mask = sum(1 << good for good in target_bundle)
        for removed in target_bundle:
            comparisons.append((agent, own, target_mask & ~(1 << removed)))
    return tuple(comparisons)


def comparison_holds(integer_values, comparison):
    agent, left, right = comparison
    return value(integer_values, agent, left) >= value(integer_values, agent, right)


def violated_witness(integer_values, comparisons):
    violated = [
        comparison
        for comparison in comparisons
        if not comparison_holds(integer_values, comparison)
    ]
    return min(
        violated,
        key=lambda comparison: (
            value(integer_values, comparison[0], comparison[1])
            - value(integer_values, comparison[0], comparison[2]),
            comparison,
        ),
    )


def model_fraction(model, expression):
    result = model.eval(expression, model_completion=True)
    return {"numerator": result.numerator_as_long(), "denominator": result.denominator_as_long()}


def owner_vector(masks, floater, goods, agents):
    owners = [agents] * goods
    owners[floater] = agents
    for agent, bundle_mask in enumerate(masks):
        for good in mask_goods(bundle_mask, goods):
            owners[good] = agent
    return tuple(owners)


def run(
    seed,
    output,
    smt2_output,
    model_output,
    timeout_seconds,
    track_unsat_core=False,
    maximum_owner_distance=None,
    maximality_menu=None,
    require_positive_complementary_sum=False,
):
    seed_document, integer_values = load_seed(seed)
    agents = len(integer_values)
    goods = len(integer_values[0])
    if agents != 4 or goods != 9:
        raise ValueError("the frozen-cell decision currently targets (n,m)=(4,9)")
    fixed = seed_document.get("fixed_state")
    if fixed is None and seed_document.get("base_bundles") is not None:
        fixed = {
            "floater": seed_document["floater"],
            "masks": [
                sum(1 << good for good in part)
                for part in seed_document["base_bundles"]
            ],
        }
    if fixed is None:
        raise ValueError("seed must contain fixed_state or base_bundles")
    fixed_masks = tuple(map(int, fixed["masks"]))
    fixed_floater = int(fixed["floater"])
    fixed_owners = owner_vector(fixed_masks, fixed_floater, goods, agents)
    evaluator = FastParkability(agents, goods)
    variables = [
        [z3.Real(f"v_{agent}_{good}") for good in range(goods)]
        for agent in range(agents)
    ]
    solver = z3.Solver()
    solver.set(timeout=int(timeout_seconds * 1000))
    tracked = []
    tracked_expressions = []

    def json_safe(value):
        if isinstance(value, numbers.Integral):
            return int(value)
        if isinstance(value, (list, tuple)):
            return [json_safe(item) for item in value]
        return value

    def add_constraint(expression, kind, **details):
        if track_unsat_core:
            label = z3.Bool(f"track_{len(tracked)}")
            solver.assert_and_track(expression, label)
            tracked.append(
                {
                    "label": str(label),
                    "kind": kind,
                    **{key: json_safe(value) for key, value in details.items()},
                }
            )
            tracked_expressions.append(expression)
        else:
            solver.add(expression)

    for agent, row in enumerate(variables):
        add_constraint(z3.Sum(*row) == 1, "row_normalization", agent=agent)
        for good, entry in enumerate(row):
            add_constraint(entry > 0, "strict_positivity", agent=agent, good=good)

    eligible_states = []
    ineligible_witnesses = set()
    for floater in range(goods):
        for masks in evaluator.base_masks[floater]:
            comparisons = eligibility_comparisons(masks, floater, goods)
            if all(comparison_holds(integer_values, item) for item in comparisons):
                eligible_states.append((floater, tuple(map(int, masks)), comparisons))
            else:
                ineligible_witnesses.add(violated_witness(integer_values, comparisons))

    eligible_comparisons = {
        comparison
        for _, _, comparisons in eligible_states
        for comparison in comparisons
    }
    for agent, left, right in sorted(eligible_comparisons):
        add_constraint(
            symbolic_value(variables, agent, left)
            >= symbolic_value(variables, agent, right),
            "eligible_comparison",
            agent=agent,
            left_mask=left,
            right_mask=right,
        )
    for agent, left, right in sorted(ineligible_witnesses):
        add_constraint(
            symbolic_value(variables, agent, left)
            < symbolic_value(variables, agent, right),
            "ineligible_witness",
            agent=agent,
            left_mask=left,
            right_mask=right,
        )

    fixed_score = z3.Sum(
        *(
            symbolic_value(variables, agent, fixed_masks[agent])
            for agent in range(agents)
        )
    )
    if require_positive_complementary_sum:
        add_constraint(
            variables[0][0]
            + variables[0][4]
            - variables[0][6]
            - variables[0][7]
            + variables[2][6]
            + variables[2][7]
            - variables[2][0]
            - variables[2][4]
            > 0,
            "positive_complementary_swap_sum",
        )
    eligible_by_key = {
        (floater, masks): (floater, masks, comparisons)
        for floater, masks, comparisons in eligible_states
    }
    menu_candidate_count = None
    menu_ineligible_count = None
    maximality_candidates = eligible_states
    if maximality_menu is not None:
        menu_document = json.loads(maximality_menu.read_text())
        menu_records = menu_document.get("selected_rivals", menu_document.get("rivals"))
        if menu_records is None:
            raise ValueError("maximality menu has neither selected_rivals nor rivals")
        menu_keys = [
            (int(record["floater"]), tuple(map(int, record["masks"])))
            for record in menu_records
        ]
        menu_candidate_count = len(menu_keys)
        maximality_candidates = [
            eligible_by_key[key] for key in menu_keys if key in eligible_by_key
        ]
        menu_ineligible_count = menu_candidate_count - len(maximality_candidates)
    maximality_state_count = 0
    for floater, masks, _ in maximality_candidates:
        rival_owners = owner_vector(masks, floater, goods, agents)
        owner_distance = sum(
            left != right for left, right in zip(fixed_owners, rival_owners)
        )
        if (
            maximum_owner_distance is not None
            and owner_distance > maximum_owner_distance
        ):
            continue
        maximality_state_count += 1
        rival_score = z3.Sum(
            *(symbolic_value(variables, agent, masks[agent]) for agent in range(agents))
        )
        add_constraint(
            fixed_score >= rival_score,
            "maximality",
            floater=floater,
            masks=list(masks),
            owner_distance=owner_distance,
        )

    base = tuple(mask_goods(mask, goods) for mask in fixed_masks)
    partitions = list(candidate_partitions(base, fixed_floater))
    edge_truths = []
    false_edge_witnesses = set()
    true_edge_comparisons = set()
    for partition_index, move in enumerate(partitions):
        partition = move["partition"]
        graph = []
        for agent in range(agents):
            row = []
            for bundle in range(agents):
                comparisons = edge_comparisons(partition, agent, bundle, goods)
                truth = all(
                    comparison_holds(integer_values, item) for item in comparisons
                )
                row.append(truth)
                if truth:
                    true_edge_comparisons.update(comparisons)
                else:
                    false_edge_witnesses.add(
                        violated_witness(integer_values, comparisons)
                    )
            graph.append(row)
        edge_truths.append(graph)
    for agent, left, right in sorted(true_edge_comparisons):
        add_constraint(
            symbolic_value(variables, agent, left)
            >= symbolic_value(variables, agent, right),
            "true_edge_comparison",
            agent=agent,
            left_mask=left,
            right_mask=right,
        )
    for agent, left, right in sorted(false_edge_witnesses):
        add_constraint(
            symbolic_value(variables, agent, left)
            < symbolic_value(variables, agent, right),
            "false_edge_witness",
            agent=agent,
            left_mask=left,
            right_mask=right,
        )

    if smt2_output is not None:
        export_solver = z3.Solver()
        export_solver.add(*solver.assertions())
        if track_unsat_core:
            export_solver.add(
                *(z3.Bool(record["label"]) for record in tracked)
            )
        smt2_output.write_text(export_solver.to_smt2())
    started = time.time()
    result = solver.check()
    elapsed = time.time() - started
    artifact = {
        "schema": SCHEMA,
        "status": str(result).upper(),
        "meaning": (
            "SAT would refute the normalized-utilitarian radius-one Hall "
            "selector; UNSAT eliminates only this frozen combinatorial cell. "
            "Neither outcome by itself refutes complete additive EFX."
        ),
        "seed_path": str(seed),
        "seed_sha256": hashlib.sha256(seed.read_bytes()).hexdigest(),
        "fixed_state": {"floater": fixed_floater, "masks": list(fixed_masks)},
        "eligible_state_count": len(eligible_states),
        "maximality_state_count": maximality_state_count,
        "maximum_owner_distance": maximum_owner_distance,
        "maximality_menu": str(maximality_menu) if maximality_menu is not None else None,
        "menu_candidate_count": menu_candidate_count,
        "menu_ineligible_count": menu_ineligible_count,
        "require_positive_complementary_sum": require_positive_complementary_sum,
        "eligible_comparison_count": len(eligible_comparisons),
        "ineligible_witness_count": len(ineligible_witnesses),
        "candidate_partition_count": len(partitions),
        "true_edge_comparison_count": len(true_edge_comparisons),
        "false_edge_witness_count": len(false_edge_witnesses),
        "elapsed_seconds": elapsed,
        "timeout_seconds": timeout_seconds,
    }
    if result == z3.sat:
        model = solver.model()
        rational_values = [
            [model_fraction(model, variables[agent][good]) for good in range(goods)]
            for agent in range(agents)
        ]
        artifact["model_values"] = rational_values
        artifact["fixed_score"] = model_fraction(model, fixed_score)
        if model_output is not None:
            model_output.write_text(str(model) + "\n")
    elif result == z3.unsat and track_unsat_core:
        core_labels = {str(label) for label in solver.unsat_core()}
        core_indices = [
            index
            for index, record in enumerate(tracked)
            if record["label"] in core_labels
        ]
        artifact["unsat_core"] = [tracked[index] for index in core_indices]
        artifact["unsat_core_size"] = len(artifact["unsat_core"])
        position = 0
        while position < len(core_indices):
            trial = core_indices[:position] + core_indices[position + 1 :]
            minimizer = z3.Solver()
            minimizer.add(*(tracked_expressions[index] for index in trial))
            if minimizer.check() == z3.unsat:
                core_indices = trial
            else:
                position += 1
        artifact["deletion_irreducible_unsat_core"] = [
            tracked[index] for index in core_indices
        ]
        artifact["deletion_irreducible_unsat_core_size"] = len(core_indices)
    if smt2_output is not None:
        artifact["smt2_path"] = str(smt2_output)
        artifact["smt2_sha256"] = hashlib.sha256(smt2_output.read_bytes()).hexdigest()
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2-output", type=Path)
    parser.add_argument("--model-output", type=Path)
    parser.add_argument("--timeout-seconds", type=float, default=600)
    parser.add_argument("--track-unsat-core", action="store_true")
    parser.add_argument("--maximum-owner-distance", type=int)
    parser.add_argument("--maximality-menu", type=Path)
    parser.add_argument("--require-positive-complementary-sum", action="store_true")
    args = parser.parse_args()
    artifact = run(
        args.seed,
        args.output,
        args.smt2_output,
        args.model_output,
        args.timeout_seconds,
        args.track_unsat_core,
        args.maximum_owner_distance,
        args.maximality_menu,
        args.require_positive_complementary_sum,
    )
    print(json.dumps(artifact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
