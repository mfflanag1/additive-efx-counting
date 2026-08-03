#!/usr/bin/env python3
"""Search for a local counterexample to threshold-compatible champion repair."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import random
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_unique_defect_champion_cycles import (
        basic_cycle_endpoint,
        champion_desired_sets,
    )
    from .audit_unique_defect_handoff import (
        acceptance_edges,
        candidate_slacks,
    )
    from .scan_charity_threshold_absorption import (
        eligible,
        scan_profile,
        tables,
        theta,
    )
except ImportError:
    from anneal import atomic_json
    from audit_unique_defect_champion_cycles import (
        basic_cycle_endpoint,
        champion_desired_sets,
    )
    from audit_unique_defect_handoff import acceptance_edges, candidate_slacks
    from scan_charity_threshold_absorption import eligible, scan_profile, tables, theta


SCHEMA = "unique-defect-champion-threshold-search-v1"


def random_state(n, m, rng):
    floater = rng.randrange(m)
    while True:
        masks = [0] * n
        for good in range(m):
            if good != floater:
                masks[rng.randrange(n)] |= 1 << good
        if all(masks):
            return tuple(masks), floater


def owner_minimum_escapes(values, masks, floater, totals, thresholds, row_totals, bad):
    owner_goods = [good for good in range(len(values[0])) if masks[bad] & (1 << good)]
    minimum = min(values[bad][good] for good in owner_goods)
    base_theta = theta(masks, totals, thresholds, row_totals)
    escapes = []
    for good in owner_goods:
        if values[bad][good] != minimum or values[bad][floater] <= minimum:
            continue
        candidate = list(masks)
        candidate[bad] = (candidate[bad] & ~(1 << good)) | (1 << floater)
        candidate = tuple(candidate)
        if eligible(candidate, 1 << good, totals, thresholds):
            escapes.append(
                {
                    "outgoing_good": good,
                    "masks": list(candidate),
                    "charity_mask": 1 << good,
                    "utility_gain": values[bad][floater] - values[bad][good],
                    "theta_change": str(
                        theta(candidate, totals, thresholds, row_totals)
                        - base_theta
                    ),
                }
            )
    return escapes


def classify(values, masks, floater, counts, require_no_owner_minimum_escape=False):
    n = len(values)
    m = len(values[0])
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    if not eligible(masks, 1 << floater, totals, thresholds):
        return None
    counts["eligible_states"] += 1
    base_theta = theta(masks, totals, thresholds, row_totals)
    all_mask = (1 << m) - 1
    for host in range(n):
        counts["host_candidates"] += 1
        witness = {"host": host, "permutation": list(range(n))}
        slacks = candidate_slacks(
            masks,
            floater,
            witness,
            totals,
            thresholds,
            row_totals,
        )
        bad_agents = [agent for agent, slack in enumerate(slacks) if slack < 0]
        if len(bad_agents) != 1:
            continue
        counts["identity_unique_defect_candidates"] += 1
        bad = bad_agents[0]
        if bad == host:
            continue
        edges = acceptance_edges(masks, floater, witness, totals, thresholds)
        if any((agent, bad) in edges for agent in range(n)):
            continue
        counts["full_witness_candidates"] += 1
        if totals[bad][masks[host]] <= totals[bad][masks[bad]]:
            continue
        counts["full_witness_bad_envies_host"] += 1
        reciprocal = champion_desired_sets(
            host,
            bad,
            masks,
            floater,
            totals,
            thresholds,
        )
        endpoints = []
        for desired in reciprocal:
            endpoint, charity = basic_cycle_endpoint(
                masks,
                host,
                bad,
                desired,
                (bad, host),
                all_mask,
            )
            if charity.bit_count() != 1:
                continue
            if not eligible(endpoint, charity, totals, thresholds):
                counts["one_charity_champion_cycles_failing_eligibility"] += 1
                continue
            old_utilities = tuple(
                totals[owner][masks[owner]] for owner in range(n)
            )
            new_utilities = tuple(
                totals[owner][endpoint[owner]] for owner in range(n)
            )
            if not (
                all(new >= old for old, new in zip(old_utilities, new_utilities))
                and any(new > old for old, new in zip(old_utilities, new_utilities))
            ):
                raise AssertionError("basic champion cycle failed Pareto replay")
            endpoints.append(
                {
                    "desired_mask": desired,
                    "masks": list(endpoint),
                    "charity_mask": charity,
                    "theta_change": theta(
                        endpoint,
                        totals,
                        thresholds,
                        row_totals,
                    )
                    - base_theta,
                }
            )
        if endpoints and max(item["theta_change"] for item in endpoints) < 0:
            counts["negative_best_reciprocal_cycles"] += 1
            minimum_escapes = owner_minimum_escapes(
                values,
                masks,
                floater,
                totals,
                thresholds,
                row_totals,
                bad,
            )
            if minimum_escapes:
                counts["negative_cycle_states_with_owner_minimum_escape"] += 1
                if require_no_owner_minimum_escape:
                    continue
            return {
                "host": host,
                "bad": bad,
                "identity_slacks": [str(slack) for slack in slacks],
                "base_theta": str(base_theta),
                "reciprocal_one_charity_endpoints": [
                    {**item, "theta_change": str(item["theta_change"])}
                    for item in endpoints
                ],
                "owner_minimum_escapes": minimum_escapes,
            }
        if endpoints:
            counts["one_charity_reciprocal_cycles"] += 1
            if max(item["theta_change"] for item in endpoints) == 0:
                counts["zero_best_reciprocal_cycles"] += 1
            else:
                counts["positive_best_reciprocal_cycles"] += 1
    return None


def run(n, m, cap, iterations, seed, output, require_no_owner_minimum_escape=False):
    if output.exists():
        raise ValueError("output must be new")
    rng = random.Random(seed)
    counts = Counter()
    for iteration in range(1, iterations + 1):
        values = tuple(
            tuple(rng.randint(1, cap) for _ in range(m)) for _ in range(n)
        )
        masks, floater = random_state(n, m, rng)
        result = classify(
            values,
            masks,
            floater,
            counts,
            require_no_owner_minimum_escape,
        )
        if result is not None:
            selector = scan_profile(values, 1)
            document = {
                "schema": SCHEMA,
                "status": (
                    "COMBINED_LOCAL_ESCAPE_REFUTED"
                    if require_no_owner_minimum_escape
                    else "LOCAL_THRESHOLD_COMPATIBILITY_REFUTED"
                ),
                "n": n,
                "m": m,
                "cap": cap,
                "seed": seed,
                "iteration": iteration,
                "counts": dict(sorted(counts.items())),
                "values": [list(row) for row in values],
                "values_sha256": hashlib.sha256(
                    json.dumps(values, separators=(",", ":")).encode()
                ).hexdigest(),
                "masks": list(masks),
                "floater": floater,
                **result,
                "global_theta_audit": {
                    "state_is_global_maximizer": result["base_theta"]
                    == selector["best_theta"],
                    "best_theta": selector["best_theta"],
                    "theta_maximizer_count": selector["theta_maximizer_count"],
                    "insertable_theta_maximizer_count": selector[
                        "insertable_theta_maximizer_count"
                    ],
                    "selector_status": selector["status"],
                },
                "claim_boundary": (
                    "This refutes only the combined local escape claim; it "
                    "does not satisfy global Theta maximality and does not "
                    "refute the Hall selector or EFX existence."
                    if require_no_owner_minimum_escape
                    else "This refutes only the local claim that a reciprocal "
                    "one-charity basic champion cycle cannot lower Theta. It "
                    "does not satisfy global Theta maximality and does not "
                    "refute the Hall selector or EFX existence."
                ),
            }
            atomic_json(output, document)
            return document
    document = {
        "schema": SCHEMA,
        "status": "NO_COUNTEREXAMPLE_FOUND",
        "n": n,
        "m": m,
        "cap": cap,
        "seed": seed,
        "iterations": iterations,
        "counts": dict(sorted(counts.items())),
        "claim_boundary": "Bounded random search only; no theorem is claimed.",
    }
    atomic_json(output, document)
    return document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=7)
    parser.add_argument("--cap", type=int, default=30)
    parser.add_argument("--iterations", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=20260803)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-no-owner-minimum-escape", action="store_true")
    args = parser.parse_args()
    result = run(
        args.n,
        args.m,
        args.cap,
        args.iterations,
        args.seed,
        args.output,
        args.require_no_owner_minimum_escape,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
