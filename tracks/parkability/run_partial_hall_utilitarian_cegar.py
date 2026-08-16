#!/usr/bin/env python3
"""CEGAR for a normalized-utilitarian-maximal radius-one Hall obstruction."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import bundle_value, eligible_constraints, integerize
    from .run_partial_hall_pareto_cegar import build_master, masks_to_bundles
except ImportError:
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json
    from decide_partial_hall_radius_one import bundle_value, eligible_constraints, integerize
    from run_partial_hall_pareto_cegar import build_master, masks_to_bundles


SCHEMA = "partial-hall-utilitarian-cegar-v1"


def base_stabilizer(base, m):
    groups = [tuple(bundle) for bundle in base]
    permutations = []
    for group_orders in itertools.product(
        *(tuple(itertools.permutations(group)) for group in groups)
    ):
        image = list(range(m))
        for group, order in zip(groups, group_orders):
            for source, destination in zip(group, order):
                image[source] = destination
        permutations.append(tuple(image))
    return tuple(permutations)


def symmetry_images(rival, stabilizer):
    images = []
    for permutation in stabilizer:
        masks = []
        for mask in rival["masks"]:
            image_mask = 0
            for good, image_good in enumerate(permutation):
                if mask & (1 << good):
                    image_mask |= 1 << image_good
            masks.append(image_mask)
        images.append(
            {"floater": permutation[rival["floater"]], "masks": tuple(masks)}
        )
    return images


def add_good_symmetry_breaking(solver, values, base):
    for bundle in base:
        for left, right in zip(bundle, bundle[1:]):
            solver.add(values[0][left] <= values[0][right])


def improving_rivals(integer_values, base):
    row_totals = tuple(map(sum, integer_values))
    base_score = sum(
        Fraction(
            sum(integer_values[agent][good] for good in base[agent]),
            row_totals[agent],
        )
        for agent in range(4)
    )
    records = [
        state
        for state in enumerate_states(integer_values)
        if sum(state["normalized"], Fraction()) > base_score
    ]
    records.sort(
        key=lambda state: (
            -sum(state["normalized"], Fraction()),
            state["floater"],
            state["base_index"],
        )
    )
    return base_score, records


def utilitarian_blocker(values, base, rival):
    bundles = masks_to_bundles(rival["masks"], len(values[0]))
    rival_eligible = z3.And(
        *eligible_constraints(values, bundles, rival["floater"])
    )
    base_score = z3.Sum(
        *(bundle_value(values[agent], base[agent]) for agent in range(4))
    )
    rival_score = z3.Sum(
        *(bundle_value(values[agent], bundles[agent]) for agent in range(4))
    )
    return z3.Not(z3.And(rival_eligible, rival_score > base_score))


def add_rivals(solver, values, base, learned, rivals, symmetry_close):
    stabilizer = base_stabilizer(base, len(values[0])) if symmetry_close else None
    for rival in rivals:
        images = symmetry_images(rival, stabilizer) if symmetry_close else (rival,)
        for image in images:
            key = (image["floater"], tuple(image["masks"]))
            if key in learned:
                continue
            learned.add(key)
            solver.add(utilitarian_blocker(values, base, image))


def replay_trace(solver, values, base, trace, batch_size, symmetry_close):
    learned = set()
    for record in trace:
        _, found = improving_rivals(record["values"], base)
        new = [
            state
            for state in found
            if (state["floater"], tuple(state["masks"])) not in learned
        ]
        if len(new) != record["new_improving_rival_count"]:
            raise ValueError(
                f"checkpoint replay mismatch at iteration {record['iteration']}"
            )
        add_rivals(
            solver, values, base, learned, new[:batch_size], symmetry_close
        )
    return learned


def run(
    output,
    checkpoint,
    max_iterations,
    batch_size,
    timeout_seconds,
    resume_from=None,
    symmetry_close=False,
    smt2_output=None,
    break_good_symmetry=False,
):
    solver, values, base, floater, partitions = build_master(
        int(timeout_seconds * 1000)
    )
    if break_good_symmetry:
        add_good_symmetry_breaking(solver, values, base)
    trace = []
    learned = set()
    if resume_from is not None:
        saved = json.loads(resume_from.read_text())
        if saved.get("schema") != SCHEMA:
            raise ValueError(f"unsupported checkpoint schema: {saved.get('schema')}")
        if saved.get("batch_size", batch_size) != batch_size:
            raise ValueError("resume batch size must match checkpoint batch size")
        if saved.get("symmetry_close", False) != symmetry_close:
            raise ValueError("resume symmetry setting must match checkpoint")
        if saved.get("break_good_symmetry", False) != break_good_symmetry:
            raise ValueError("resume symmetry-break setting must match checkpoint")
        trace = saved["trace"]
        learned = replay_trace(
            solver, values, base, trace, batch_size, symmetry_close
        )
        if saved.get("learned_rival_count") != len(learned):
            raise ValueError("checkpoint learned-rival count does not replay")
    started = time.time()
    terminal_values = None
    status = "ITERATION_LIMIT"
    iteration = len(trace)
    for iteration in range(iteration + 1, max_iterations + 1):
        verdict = solver.check()
        if verdict == z3.unsat:
            status = "UNSAT"
            break
        if verdict == z3.unknown:
            status = "MASTER_UNKNOWN"
            break
        integer_values = integerize(solver.model(), values)
        base_score, found = improving_rivals(integer_values, base)
        new = [
            state
            for state in found
            if (state["floater"], tuple(state["masks"])) not in learned
        ]
        record = {
            "iteration": iteration,
            "elapsed_seconds": round(time.time() - started, 6),
            "base_score": {
                "numerator": base_score.numerator,
                "denominator": base_score.denominator,
            },
            "improving_rival_count": len(found),
            "new_improving_rival_count": len(new),
            "learned_rival_count_before": len(learned),
            "values": integer_values,
        }
        trace.append(record)
        print(json.dumps(record, sort_keys=True), flush=True)
        if not found:
            terminal_values = integer_values
            status = "UTILITARIAN_RADIUS_ONE_COUNTEREXAMPLE"
            break
        if not new:
            raise AssertionError("model retains only already-blocked improving rivals")
        add_rivals(
            solver, values, base, learned, new[:batch_size], symmetry_close
        )
        atomic_json(
            checkpoint,
            {
                "schema": SCHEMA,
                "status": "RUNNING",
                "iteration": iteration,
                "batch_size": batch_size,
                "symmetry_close": symmetry_close,
                "break_good_symmetry": break_good_symmetry,
                "learned_rival_count": len(learned),
                "trace": trace,
            },
        )
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "A SAT counterexample refutes normalized-utilitarian-maximal "
            "radius-one Hall completion, not complete additive EFX; UNSAT "
            "proves this fixed base cell."
        ),
        "n": 4,
        "m": 9,
        "floater": floater,
        "base_bundles": [list(bundle) for bundle in base],
        "candidate_partition_count": len(partitions),
        "max_iterations": max_iterations,
        "batch_size": batch_size,
        "symmetry_close": symmetry_close,
        "break_good_symmetry": break_good_symmetry,
        "timeout_seconds_per_master": timeout_seconds,
        "iterations_completed": iteration,
        "learned_rival_count": len(learned),
        "elapsed_seconds": round(time.time() - started, 6),
        "values": terminal_values,
        "trace": trace,
        "solver_reason_unknown": (
            solver.reason_unknown() if status == "MASTER_UNKNOWN" else None
        ),
        "solver_statistics": str(solver.statistics()),
    }
    if smt2_output is not None:
        smt2_output.write_text(solver.to_smt2())
        result["smt2_output"] = str(smt2_output)
    atomic_json(output, result)
    atomic_json(checkpoint, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--resume-from", type=Path)
    parser.add_argument("--symmetry-close", action="store_true")
    parser.add_argument("--smt2-output", type=Path)
    parser.add_argument("--break-good-symmetry", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output,
        args.checkpoint,
        args.max_iterations,
        args.batch_size,
        args.timeout_seconds,
        args.resume_from,
        args.symmetry_close,
        args.smt2_output,
        args.break_good_symmetry,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
