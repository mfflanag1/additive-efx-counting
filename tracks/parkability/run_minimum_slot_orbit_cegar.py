#!/usr/bin/env python3
"""CEGAR for a globally threshold-maximal blocked five-token orbit."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import time

import z3

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import audit_orbit, bundles_from_masks
    from .decide_threshold_hall_local_gradient import (
        eligible,
        integer_values,
        maximum,
        threshold,
        total,
    )
    from .fast_count import FastParkability
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import audit_orbit, bundles_from_masks
    from decide_threshold_hall_local_gradient import (
        eligible,
        integer_values,
        maximum,
        threshold,
        total,
    )
    from fast_count import FastParkability


SCHEMA = "minimum-slot-orbit-global-threshold-cegar-v1"
BASE = ((0, 1), (2, 3), (4, 5), (6, 7))
CORES = (0, 2, 4, 6)
TOKENS = (1, 3, 5, 7, 8)
FLOATER = 8


def masks_from_bundles(bundles):
    return tuple(
        sum(1 << good for good in bundle)
        for bundle in bundles
    )


def theta(values, bundles):
    return z3.Sum(
        *(threshold(values[owner], bundles[owner]) for owner in range(4))
    )


def complete_failure(values, bundles, floater, host, permutation):
    complete = list(bundles)
    complete[host] = tuple(sorted((*complete[host], floater)))
    failures = []
    for observer in range(4):
        assigned = permutation[observer]
        required = maximum(
            threshold(values[observer], complete[target])
            for target in range(4)
            if target != assigned
        )
        failures.append(
            total(values[observer], complete[assigned]) < required
        )
    return z3.Or(*failures)


def orbit_bundles(assignment):
    return tuple(
        tuple(sorted((CORES[owner], assignment[owner])))
        for owner in range(4)
    )


def global_landscape(raw_values):
    evaluator = FastParkability(4, 9)
    landscape = evaluator.partial_linear_potential_landscape(
        raw_values,
        potential="normalized_threshold",
    )
    base_masks = masks_from_bundles(BASE)
    fixed = next(
        (
            winner
            for winner in landscape["maximizers"]
            if winner["floater"] == FLOATER
            and tuple(
                int(mask)
                for mask in evaluator.base_masks[FLOATER][winner["base_index"]]
            )
            == base_masks
        ),
        None,
    )
    first = landscape["maximizers"][0]
    first_masks = tuple(
        int(mask)
        for mask in evaluator.base_masks[first["floater"]][first["base_index"]]
    )
    return landscape, fixed, {
        "floater": first["floater"],
        "masks": first_masks,
        "hall_insertable": first["hall_insertable"],
    }


def state_key(state):
    return (state["floater"], tuple(int(mask) for mask in state["masks"]))


def owner_relabelings(mode):
    if mode == "none":
        return ((0, 1, 2, 3),)
    if mode == "cyclic":
        return tuple(
            tuple((owner + shift) % 4 for owner in range(4))
            for shift in range(4)
        )
    if mode == "full":
        return tuple(itertools.permutations(range(4)))
    raise ValueError(f"unknown relabeling mode: {mode}")


def relabeled_state_orbit(state, mode):
    results = {}
    for permutation in owner_relabelings(mode):
        good_map = {8: 8}
        for owner in range(4):
            good_map[2 * owner] = 2 * permutation[owner]
            good_map[2 * owner + 1] = 2 * permutation[owner] + 1
        masks = [0] * 4
        for owner, mask in enumerate(state["masks"]):
            mapped_owner = permutation[owner]
            for good in range(9):
                if int(mask) & (1 << good):
                    masks[mapped_owner] |= 1 << good_map[good]
        mapped = {
            "floater": good_map[state["floater"]],
            "masks": tuple(masks),
        }
        results[state_key(mapped)] = mapped
    return tuple(results.values())


def add_global_cut(solver, values, base_theta, state):
    bundles = bundles_from_masks(state["masks"], 9)
    solver.add(
        z3.Implies(
            eligible(values, bundles, state["floater"]),
            theta(values, bundles) <= base_theta,
        )
    )


def run(
    output: Path,
    timeout_seconds: int,
    max_iterations: int,
    seed: Path | None,
    relabeling_mode: str,
    completion_batch_size: int,
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
    for owner, (core, token) in enumerate(zip(CORES, TOKENS[:4])):
        solver.add(values[owner][token] < values[owner][core])

    base_theta = theta(values, BASE)
    for assignment in itertools.permutations(TOKENS):
        bundles = orbit_bundles(assignment)
        solver.add(
            z3.Implies(
                eligible(values, bundles, assignment[4]),
                z3.And(
                    *(
                        values[owner][assignment[owner]]
                        <= values[owner][CORES[owner]]
                        for owner in range(4)
                    )
                ),
            )
        )

    global_cuts = set()
    completion_cuts = set()
    global_cut_records = []
    completion_cut_records = []
    prior_iterations = 0
    if seed is not None:
        seed_document = json.loads(seed.read_text())
        if seed_document.get("schema") != SCHEMA:
            raise ValueError("seed has incompatible schema")
        prior_iterations = int(seed_document.get("total_iterations", 0))
        for record in seed_document.get("global_cuts", []):
            seed_state = {
                "floater": int(record["floater"]),
                "masks": tuple(int(mask) for mask in record["masks"]),
            }
            for state in relabeled_state_orbit(seed_state, relabeling_mode):
                key = state_key(state)
                if key in global_cuts:
                    continue
                global_cuts.add(key)
                global_cut_records.append(
                    {
                        "floater": state["floater"],
                        "masks": list(state["masks"]),
                    }
                )
                add_global_cut(solver, values, base_theta, state)
        for record in seed_document.get("completion_cuts", []):
            assignment = tuple(int(good) for good in record["assignment"])
            host = int(record["host"])
            permutation = tuple(int(bundle) for bundle in record["permutation"])
            key = (assignment, host, permutation)
            if key in completion_cuts:
                continue
            completion_cuts.add(key)
            completion_cut_records.append(
                {
                    "assignment": list(assignment),
                    "host": host,
                    "permutation": list(permutation),
                }
            )
            bundles = orbit_bundles(assignment)
            solver.add(
                z3.Implies(
                    eligible(values, bundles, assignment[4]),
                    complete_failure(
                        values,
                        bundles,
                        assignment[4],
                        host,
                        permutation,
                    ),
                )
            )
    started = time.monotonic()
    last_values = None
    last_orbit = None
    last_global = None
    last_orbit_blocked_values = None
    last_orbit_blocked_orbit = None
    last_orbit_blocked_global = None
    orbit_blocked_seed_path = output.with_name(
        f"{output.stem}_orbit_blocked_seed.json"
    )
    status = "ITERATION_LIMIT"
    reason_unknown = None

    for iteration in range(1, max_iterations + 1):
        verdict = solver.check()
        if verdict == z3.unsat:
            status = "FIXED_PAIR_TOKEN_ORBIT_FORCED"
            break
        if verdict == z3.unknown:
            status = "UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break

        model = solver.model()
        raw_values = integer_values(model, values)
        last_values = raw_values
        last_global = None
        base_state = {
            "floater": FLOATER,
            "masks": masks_from_bundles(BASE),
        }
        last_orbit = audit_orbit(
            raw_values,
            base_state,
            TOKENS[:4],
            include_records=True,
        )
        completing_records = [
            record for record in last_orbit["records"] if record["completing"]
        ][:completion_batch_size]
        if completing_records:
            for completing in completing_records:
                assignment = tuple(completing["assignment"])
                key = (
                    assignment,
                    completing["best_host"],
                    tuple(completing["best_permutation"]),
                )
                if key in completion_cuts:
                    raise AssertionError("repeated token-orbit completion witness")
                completion_cuts.add(key)
                completion_cut_records.append(
                    {
                        "assignment": list(assignment),
                        "host": completing["best_host"],
                        "permutation": list(completing["best_permutation"]),
                    }
                )
                bundles = orbit_bundles(assignment)
                solver.add(
                    z3.Implies(
                        eligible(values, bundles, assignment[4]),
                        complete_failure(
                            values,
                            bundles,
                            assignment[4],
                            completing["best_host"],
                            tuple(completing["best_permutation"]),
                        ),
                    )
                )
            continue

        landscape, fixed, higher_state = global_landscape(raw_values)
        last_global = {
            "eligible_state_count": landscape["eligible_base_count"],
            "maximum_threshold_state_count": landscape["maximizer_count"],
            "hall_insertable_maximum_threshold_state_count": landscape[
                "hall_insertable_maximizer_count"
            ],
            "fixed_base_is_global_threshold_maximum": fixed is not None,
        }
        last_orbit_blocked_values = raw_values
        last_orbit_blocked_orbit = last_orbit
        last_orbit_blocked_global = last_global
        atomic_json(
            orbit_blocked_seed_path,
            {
                "schema": "minimum-slot-orbit-blocked-seed-v1",
                "status": "EXACT_ORBIT_BLOCKED",
                "meaning": (
                    "Exact positive valuation whose canonical five-token "
                    "orbit has no eligible EFX completion. Global audit is "
                    "aligned to the same valuation."
                ),
                "source_session": str(output),
                "iteration": iteration,
                "values": raw_values,
                "orbit_audit": last_orbit,
                "global_audit": last_global,
                "global_cut_count": len(global_cuts),
                "completion_cut_count": len(completion_cuts),
            },
        )

        if fixed is None:
            witness_key = state_key(higher_state)
            if witness_key in global_cuts:
                raise AssertionError("repeated global maximality witness")
            for state in relabeled_state_orbit(higher_state, relabeling_mode):
                key = state_key(state)
                if key in global_cuts:
                    continue
                global_cuts.add(key)
                global_cut_records.append(
                    {
                        "floater": state["floater"],
                        "masks": list(state["masks"]),
                    }
                )
                add_global_cut(solver, values, base_theta, state)
            continue

        status = "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND"
        break

    artifact = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "Exact CEGAR for a positive canonical four-pair base with unique "
            "owner minima. Global cuts enforce normalized-threshold maximality; "
            "completion cuts adversarially block exact EFX matchings inside "
            "the fixed five-token orbit."
        ),
        "claim_boundary": (
            "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND refutes the fixed-core "
            "orbit theorem for this base cell after exact replay. UNSAT proves "
            "only the canonical four-pair cell. Other statuses are not verdicts."
        ),
        "iterations": iteration,
        "prior_iterations": prior_iterations,
        "total_iterations": prior_iterations + iteration,
        "max_iterations": max_iterations,
        "timeout_seconds_per_check": timeout_seconds,
        "relabeling_mode": relabeling_mode,
        "completion_batch_size": completion_batch_size,
        "elapsed_seconds": time.monotonic() - started,
        "global_cut_count": len(global_cuts),
        "completion_cut_count": len(completion_cuts),
        "global_cuts": global_cut_records,
        "completion_cuts": completion_cut_records,
        "solver_reason_unknown": reason_unknown,
        "values": last_values,
        "global_audit": last_global,
        "orbit_audit": last_orbit,
        "last_orbit_blocked_values": last_orbit_blocked_values,
        "last_orbit_blocked_orbit_audit": last_orbit_blocked_orbit,
        "last_orbit_blocked_global_audit": last_orbit_blocked_global,
        "orbit_blocked_seed": (
            str(orbit_blocked_seed_path)
            if last_orbit_blocked_values is not None
            else None
        ),
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--seed", type=Path)
    parser.add_argument(
        "--relabeling-mode",
        choices=("none", "cyclic", "full"),
        default="cyclic",
    )
    parser.add_argument("--completion-batch-size", type=int, default=8)
    args = parser.parse_args()
    result = run(
        args.output,
        args.timeout_seconds,
        args.max_iterations,
        args.seed,
        args.relabeling_mode,
        args.completion_batch_size,
    )
    summary = {
        key: result[key]
        for key in (
            "schema",
            "status",
            "iterations",
            "total_iterations",
            "elapsed_seconds",
            "global_cut_count",
            "completion_cut_count",
            "solver_reason_unknown",
            "global_audit",
        )
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
