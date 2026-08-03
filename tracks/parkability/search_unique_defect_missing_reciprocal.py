#!/usr/bin/env python3
"""Search for a full unique defect without a reciprocal champion edge."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import random
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_unique_defect_champion_cycles import champion_desired_sets
    from .audit_unique_defect_handoff import acceptance_edges, candidate_slacks
    from .scan_charity_threshold_absorption import (
        eligible,
        scan_profile,
        tables,
        theta,
    )
    from .search_unique_defect_champion_threshold import random_state
except ImportError:
    from anneal import atomic_json
    from audit_unique_defect_champion_cycles import champion_desired_sets
    from audit_unique_defect_handoff import acceptance_edges, candidate_slacks
    from scan_charity_threshold_absorption import eligible, scan_profile, tables, theta
    from search_unique_defect_champion_threshold import random_state


SCHEMA = "unique-defect-missing-reciprocal-search-v1"


def classify(values, masks, floater, counts):
    n = len(values)
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    if not eligible(masks, 1 << floater, totals, thresholds):
        return None
    counts["eligible_states"] += 1
    for host in range(n):
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
        forced = champion_desired_sets(
            bad,
            host,
            masks,
            floater,
            totals,
            thresholds,
        )
        if not forced:
            counts["bad_champion_missing"] += 1
            continue
        reciprocal = champion_desired_sets(
            host,
            bad,
            masks,
            floater,
            totals,
            thresholds,
        )
        if reciprocal:
            counts["reciprocal_candidates"] += 1
            continue
        counts["missing_reciprocal_candidates"] += 1
        return {
            "host": host,
            "bad": bad,
            "identity_slacks": [str(slack) for slack in slacks],
            "bad_envies_host": totals[bad][masks[host]]
            > totals[bad][masks[bad]],
            "forced_desired_masks": list(forced),
            "base_theta": str(theta(masks, totals, thresholds, row_totals)),
        }
    return None


def run(n, m, cap, iterations, seed, output):
    if output.exists():
        raise ValueError("output must be new")
    rng = random.Random(seed)
    counts = Counter()
    for iteration in range(1, iterations + 1):
        values = tuple(
            tuple(rng.randint(1, cap) for _ in range(m)) for _ in range(n)
        )
        masks, floater = random_state(n, m, rng)
        result = classify(values, masks, floater, counts)
        if result is None:
            continue
        selector = scan_profile(values, 1)
        document = {
            "schema": SCHEMA,
            "status": "LOCAL_RECIPROCITY_REFUTED",
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
                "This refutes only local reciprocity. The state is not asserted "
                "to be globally threshold-maximal and complete EFX remains open."
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
    parser.add_argument("--m", type=int, default=6)
    parser.add_argument("--cap", type=int, default=30)
    parser.add_argument("--iterations", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.n,
                args.m,
                args.cap,
                args.iterations,
                args.seed,
                args.output,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
