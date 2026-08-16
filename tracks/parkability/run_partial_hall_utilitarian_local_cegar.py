#!/usr/bin/env python3
"""CEGAR for the owner-distance-two utilitarian Hall-improvement lemma."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import integerize
    from .decide_partial_hall_utilitarian_local import local_rivals
    from .run_partial_hall_pareto_cegar import build_master
    from .partial_hall_factored_master import build_factored_master
    from .run_partial_hall_utilitarian_cegar import (
        add_good_symmetry_breaking,
        base_stabilizer,
        symmetry_images,
        utilitarian_blocker,
    )
except ImportError:
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json
    from decide_partial_hall_radius_one import integerize
    from decide_partial_hall_utilitarian_local import local_rivals
    from run_partial_hall_pareto_cegar import build_master
    from partial_hall_factored_master import build_factored_master
    from run_partial_hall_utilitarian_cegar import (
        add_good_symmetry_breaking,
        base_stabilizer,
        symmetry_images,
        utilitarian_blocker,
    )


SCHEMA = "partial-hall-utilitarian-local-cegar-v1"


def improving_local_rivals(integer_values, base, templates):
    row_totals = tuple(map(sum, integer_values))
    base_score = sum(
        Fraction(
            sum(integer_values[agent][good] for good in base[agent]),
            row_totals[agent],
        )
        for agent in range(4)
    )
    eligible = {
        (state["floater"], tuple(state["masks"])): state
        for state in enumerate_states(integer_values)
    }
    found = []
    for template in templates:
        state = eligible.get((template["floater"], tuple(template["masks"])))
        if state is None:
            continue
        score = sum(state["normalized"], Fraction())
        if score > base_score:
            found.append((score - base_score, template))
    found.sort(
        key=lambda pair: (
            -pair[0], pair[1]["floater"], tuple(pair[1]["masks"])
        )
    )
    return base_score, [template for _, template in found]


def add_local_rivals(
    solver,
    values,
    base,
    learned,
    rivals,
    symmetry_close,
    comparison_cache=None,
):
    stabilizer = (
        base_stabilizer(base, len(values[0])) if symmetry_close else None
    )
    for rival in rivals:
        images = symmetry_images(rival, stabilizer) if symmetry_close else (rival,)
        for image in images:
            key = (image["floater"], tuple(image["masks"]))
            if key not in learned:
                learned.add(key)
                blocker = (
                    factored_utilitarian_blocker(
                        solver, values, base, image, comparison_cache
                    )
                    if comparison_cache is not None
                    else utilitarian_blocker(values, base, image)
                )
                solver.add(blocker)


def mask(bundle):
    return sum(1 << good for good in bundle)


def factored_comparison(solver, values, cache, agent, left, right):
    key = (agent, mask(left), mask(right))
    atom = cache.get(key)
    if atom is None:
        atom = z3.Bool(f"rival_cmp_{agent}_{key[1]}_{key[2]}")
        solver.add(
            atom
            == (
                z3.Sum(*(values[agent][good] for good in left))
                >= z3.Sum(*(values[agent][good] for good in right))
            )
        )
        cache[key] = atom
    return atom


def factored_utilitarian_blocker(solver, values, base, rival, cache):
    bundles = tuple(
        tuple(good for good in range(len(values[0])) if bundle & (1 << good))
        for bundle in rival["masks"]
    )
    eligibility = []
    for agent in range(len(values)):
        own = bundles[agent]
        for target in range(len(values)):
            if target == agent:
                continue
            for removed in bundles[target]:
                residual = tuple(
                    good for good in bundles[target] if good != removed
                )
                eligibility.append(
                    factored_comparison(
                        solver, values, cache, agent, own, residual
                    )
                )
        eligibility.append(
            factored_comparison(
                solver,
                values,
                cache,
                agent,
                own,
                (rival["floater"],),
            )
        )
    base_score = z3.Sum(
        *(z3.Sum(*(values[agent][good] for good in base[agent])) for agent in range(4))
    )
    rival_score = z3.Sum(
        *(z3.Sum(*(values[agent][good] for good in bundles[agent])) for agent in range(4))
    )
    return z3.Not(z3.And(*eligibility, rival_score > base_score))


def run(
    output,
    checkpoint,
    smt2_output,
    max_iterations,
    batch_size,
    timeout_seconds,
    break_good_symmetry,
    radius,
    resume_from=None,
    random_seed=0,
    factored_hall=False,
    seed_from=None,
    symmetry_close=False,
    factor_rival_eligibility=False,
    hall_witness=False,
    trap_partition=None,
    trap_agents=(),
    trap_bundle=None,
    connected_rivals=False,
    project_seed=False,
):
    if factored_hall:
        solver, values, base, floater, partitions, hall_edges = build_factored_master(
            int(timeout_seconds * 1000),
            hall_encoding="witness" if hall_witness else "matching",
        )
    else:
        solver, values, base, floater, partitions = build_master(
            int(timeout_seconds * 1000)
        )
        hall_edges = None
    if trap_partition is not None:
        if hall_edges is None or len(trap_agents) != 2 or trap_bundle is None:
            raise ValueError("a designated trap requires factored Hall and two agents")
        if break_good_symmetry:
            raise ValueError("fixed labeled traps cannot use base-good symmetry breaking")
        if not 0 <= trap_partition < len(hall_edges) or not 0 <= trap_bundle < 4:
            raise ValueError("trap partition and bundle are out of range")
        for agent in trap_agents:
            solver.add(hall_edges[trap_partition][agent][trap_bundle])
            solver.add(
                *(
                    z3.Not(hall_edges[trap_partition][agent][bundle])
                    for bundle in range(4)
                    if bundle != trap_bundle
                )
            )
    solver.set(random_seed=random_seed)
    if break_good_symmetry:
        add_good_symmetry_breaking(solver, values, base)
    templates = local_rivals(
        base,
        floater,
        len(values[0]),
        radius,
        connected_only=connected_rivals,
    )
    comparison_cache = {} if factor_rival_eligibility else None
    learned = set()
    trace = []
    seed_learned_count = 0
    if seed_from is not None:
        saved = json.loads(seed_from.read_text())
        if saved.get("schema") != SCHEMA:
            raise ValueError(f"unsupported seed schema: {saved.get('schema')}")
        if saved.get("owner_distance_radius") != radius:
            raise ValueError("seed radius must match")
        if not project_seed and saved.get("connected_rivals", False) != connected_rivals:
            raise ValueError("seed connected-rival setting must match")
        seed_batch_size = saved.get("batch_size")
        selected = []
        original_learned = set()
        for record in saved["trace"]:
            _, found = improving_local_rivals(record["values"], base, templates)
            new = [
                rival
                for rival in found
                if (rival["floater"], tuple(rival["masks"]))
                not in original_learned
            ]
            if (
                not project_seed
                and len(new) != record["new_improving_local_rival_count"]
            ):
                raise ValueError(
                    f"seed replay mismatch at iteration {record['iteration']}"
                )
            for rival in new[:seed_batch_size]:
                original_learned.add(
                    (rival["floater"], tuple(rival["masks"]))
                )
                selected.append(rival)
        if (
            not project_seed
            and saved.get("learned_rival_count") != len(original_learned)
        ):
            raise ValueError("seed learned-rival count does not replay")
        add_local_rivals(
            solver,
            values,
            base,
            learned,
            selected,
            symmetry_close,
            comparison_cache,
        )
        seed_learned_count = len(original_learned)
    if resume_from is not None:
        saved = json.loads(resume_from.read_text())
        if saved.get("schema") != SCHEMA:
            raise ValueError(f"unsupported checkpoint schema: {saved.get('schema')}")
        if saved.get("owner_distance_radius", radius) != radius:
            raise ValueError("resume radius must match checkpoint")
        if saved.get("batch_size", batch_size) != batch_size:
            raise ValueError("resume batch size must match checkpoint")
        if saved.get("break_good_symmetry", False) != break_good_symmetry:
            raise ValueError("resume symmetry setting must match checkpoint")
        if "factored_hall" in saved and saved["factored_hall"] != factored_hall:
            raise ValueError("resume Hall encoding must match checkpoint")
        if saved.get("hall_witness", False) != hall_witness:
            raise ValueError("resume Hall witness setting must match checkpoint")
        if saved.get("trap_partition") != trap_partition:
            raise ValueError("resume trap partition must match checkpoint")
        if tuple(saved.get("trap_agents", ())) != tuple(trap_agents):
            raise ValueError("resume trap agents must match checkpoint")
        if saved.get("trap_bundle") != trap_bundle:
            raise ValueError("resume trap bundle must match checkpoint")
        if saved.get("connected_rivals", False) != connected_rivals:
            raise ValueError("resume connected-rival setting must match checkpoint")
        if saved.get("symmetry_close", False) != symmetry_close:
            raise ValueError("resume symmetry closure must match checkpoint")
        if (
            saved.get("factor_rival_eligibility", False)
            != factor_rival_eligibility
        ):
            raise ValueError("resume rival factoring must match checkpoint")
        trace = saved["trace"]
        for record in trace:
            _, found = improving_local_rivals(record["values"], base, templates)
            new = [
                rival
                for rival in found
                if (rival["floater"], tuple(rival["masks"])) not in learned
            ]
            if len(new) != record["new_improving_local_rival_count"]:
                raise ValueError(
                    f"checkpoint replay mismatch at iteration {record['iteration']}"
                )
            add_local_rivals(
                solver,
                values,
                base,
                learned,
                new[:batch_size],
                symmetry_close,
                comparison_cache,
            )
        if saved.get("learned_rival_count") != len(learned):
            raise ValueError("checkpoint learned-rival count does not replay")
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
        base_score, found = improving_local_rivals(
            integer_values, base, templates
        )
        new = [
            rival
            for rival in found
            if (rival["floater"], tuple(rival["masks"])) not in learned
        ]
        record = {
            "iteration": iteration,
            "base_score": {
                "numerator": base_score.numerator,
                "denominator": base_score.denominator,
            },
            "improving_local_rival_count": len(found),
            "new_improving_local_rival_count": len(new),
            "learned_rival_count_before": len(learned),
            "values": integer_values,
        }
        trace.append(record)
        print(json.dumps(record, sort_keys=True), flush=True)
        if not found:
            terminal_values = integer_values
            status = "SAT_LOCAL_MAXIMAL_OBSTRUCTION"
            break
        if not new:
            raise AssertionError("model retains only learned improving rivals")
        add_local_rivals(
            solver,
            values,
            base,
            learned,
            new[:batch_size],
            symmetry_close,
            comparison_cache,
        )
        atomic_json(
            checkpoint,
            {
                "schema": SCHEMA,
                "status": "RUNNING",
                "iteration": iteration,
                "batch_size": batch_size,
                "owner_distance_radius": radius,
                "break_good_symmetry": break_good_symmetry,
                "factored_hall": factored_hall,
                "hall_witness": hall_witness,
                "trap_partition": trap_partition,
                "trap_agents": list(trap_agents),
                "trap_bundle": trap_bundle,
                "connected_rivals": connected_rivals,
                "symmetry_close": symmetry_close,
                "seed_from": str(seed_from) if seed_from is not None else None,
                "seed_learned_rival_count": seed_learned_count,
                "factor_rival_eligibility": factor_rival_eligibility,
                "factored_rival_comparison_count": (
                    len(comparison_cache)
                    if comparison_cache is not None
                    else None
                ),
                "learned_rival_count": len(learned),
                "trace": trace,
            },
        )
    smt2_output.write_text(solver.to_smt2())
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "SAT refutes the stated bounded-owner-distance normalized-utilitarian "
            "improvement lemma; UNSAT proves it for the fixed base cell."
        ),
        "n": 4,
        "m": 9,
        "base_bundles": [list(bundle) for bundle in base],
        "floater": floater,
        "candidate_partition_count": len(partitions),
        "local_rival_template_count": len(templates),
        "owner_distance_radius": radius,
        "max_iterations": max_iterations,
        "batch_size": batch_size,
        "timeout_seconds_per_master": timeout_seconds,
        "random_seed": random_seed,
        "factored_hall": factored_hall,
        "hall_witness": hall_witness,
        "trap_partition": trap_partition,
        "trap_agents": list(trap_agents),
        "trap_bundle": trap_bundle,
        "connected_rivals": connected_rivals,
        "break_good_symmetry": break_good_symmetry,
        "symmetry_close": symmetry_close,
        "seed_from": str(seed_from) if seed_from is not None else None,
        "project_seed": project_seed,
        "seed_learned_rival_count": seed_learned_count,
        "factor_rival_eligibility": factor_rival_eligibility,
        "factored_rival_comparison_count": (
            len(comparison_cache) if comparison_cache is not None else None
        ),
        "iterations_completed": iteration,
        "learned_rival_count": len(learned),
        "values": terminal_values,
        "trace": trace,
        "smt2_output": str(smt2_output),
        "solver_reason_unknown": (
            solver.reason_unknown() if status == "MASTER_UNKNOWN" else None
        ),
        "solver_statistics": str(solver.statistics()),
    }
    atomic_json(output, result)
    atomic_json(checkpoint, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--smt2-output", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--break-good-symmetry", action="store_true")
    parser.add_argument("--radius", type=int, choices=range(1, 10), default=3)
    parser.add_argument("--resume-from", type=Path)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--factored-hall", action="store_true")
    parser.add_argument("--hall-witness", action="store_true")
    parser.add_argument("--trap-partition", type=int)
    parser.add_argument("--trap-agent", type=int, action="append", default=[])
    parser.add_argument("--trap-bundle", type=int)
    parser.add_argument("--seed-from", type=Path)
    parser.add_argument("--symmetry-close", action="store_true")
    parser.add_argument("--factor-rival-eligibility", action="store_true")
    parser.add_argument("--connected-rivals", action="store_true")
    parser.add_argument("--project-seed", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output,
        args.checkpoint,
        args.smt2_output,
        args.max_iterations,
        args.batch_size,
        args.timeout_seconds,
        args.break_good_symmetry,
        args.radius,
        args.resume_from,
        args.random_seed,
        args.factored_hall,
        args.seed_from,
        args.symmetry_close,
        args.factor_rival_eligibility,
        args.hall_witness,
        args.trap_partition,
        tuple(args.trap_agent),
        args.trap_bundle,
        args.connected_rivals,
        args.project_seed,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
