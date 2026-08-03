#!/usr/bin/env python3
"""Search the bad-source champion branch for no-singleton-discard states."""

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
    from .scan_charity_threshold_absorption import eligible, scan_profile, tables, theta
    from .search_unique_defect_champion_threshold import random_state
except ImportError:
    from anneal import atomic_json
    from audit_unique_defect_champion_cycles import champion_desired_sets
    from audit_unique_defect_handoff import acceptance_edges, candidate_slacks
    from scan_charity_threshold_absorption import eligible, scan_profile, tables, theta
    from search_unique_defect_champion_threshold import random_state


SCHEMA = "unique-defect-multi-bottom-search-v1"


def classify(values, masks, floater, counts, capture_bad_not_champion=False):
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
        bad_envies_host = totals[bad][masks[host]] > totals[bad][masks[bad]]
        if bad_envies_host:
            counts["full_witness_bad_envies_host"] += 1
            continue
        counts["full_witness_forced_decomposition"] += 1
        desired_sets = champion_desired_sets(
            bad,
            host,
            masks,
            floater,
            totals,
            thresholds,
        )
        if not desired_sets:
            counts["bad_not_champion_candidates"] += 1
            if not capture_bad_not_champion:
                continue
            host_desired = champion_desired_sets(
                host,
                host,
                masks,
                floater,
                totals,
                thresholds,
            )
            return {
                "failure_kind": "bad_not_champion",
                "host": host,
                "bad": bad,
                "identity_slacks": [str(slack) for slack in slacks],
                "base_theta": str(theta(masks, totals, thresholds, row_totals)),
                "bad_envies_host": bad_envies_host,
                "host_strongly_envies_augmented_host": thresholds[host][
                    masks[host] | (1 << floater)
                ]
                > totals[host][masks[host]],
                "host_self_champion_desired_masks": list(host_desired),
            }
        augmented = masks[host] | (1 << floater)
        options = [
            {
                "desired_mask": desired,
                "discard_mask": augmented ^ desired,
                "discard_size": (augmented ^ desired).bit_count(),
            }
            for desired in desired_sets
        ]
        retaining = [option for option in options if option["desired_mask"] & (1 << floater)]
        if not retaining:
            continue
        counts["forced_retain_floater_candidates"] += 1
        minimum_discard = min(option["discard_size"] for option in retaining)
        if minimum_discard <= 1:
            counts["forced_retain_with_singleton_discard"] += 1
            continue
        counts["forced_multi_bottom_candidates"] += 1
        return {
            "failure_kind": "forced_multi_bottom",
            "host": host,
            "bad": bad,
            "identity_slacks": [str(slack) for slack in slacks],
            "base_theta": str(theta(masks, totals, thresholds, row_totals)),
            "bad_envies_host": bad_envies_host,
            "minimum_forced_discard_size": minimum_discard,
            "forced_retain_options": retaining,
        }
    return None


def run(n, m, cap, iterations, seed, output, capture_bad_not_champion=False):
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
            capture_bad_not_champion,
        )
        if result is None:
            continue
        selector = scan_profile(values, 1)
        document = {
            "schema": SCHEMA,
            "status": (
                "BAD_CHAMPION_BRIDGE_REFUTED"
                if result["failure_kind"] == "bad_not_champion"
                else "LOCAL_SINGLETON_DISCARD_REFUTED"
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
                "This refutes the claim that the unique bad identity agent "
                "must champion the augmented host; the host can also strongly "
                "envy that set. It does not refute the corrected two-source "
                "bridge, the Hall selector, or EFX existence."
                if result["failure_kind"] == "bad_not_champion"
                else "This refutes only a local singleton-discard strengthening "
                "of the conditional bad-source champion branch. It is not globally maximal and "
                "does not refute the Hall selector or EFX existence."
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
    parser.add_argument("--m", type=int, default=8)
    parser.add_argument("--cap", type=int, default=40)
    parser.add_argument("--iterations", type=int, default=300000)
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--capture-bad-not-champion", action="store_true")
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
                args.capture_bad_not_champion,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
