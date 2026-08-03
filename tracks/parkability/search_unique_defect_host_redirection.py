#!/usr/bin/env python3
"""Falsify host-redirection patterns outside the selected plateau corpus."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

try:
    from .anneal import atomic_json
    from .scan_charity_threshold_absorption import eligible, tables
except ImportError:
    from anneal import atomic_json
    from scan_charity_threshold_absorption import eligible, tables


SCHEMA = "unique-defect-host-redirection-search-v1"


def identity_bad_agents(masks, floater, host, totals, thresholds):
    complete = list(masks)
    complete[host] |= 1 << floater
    return tuple(
        agent
        for agent in range(len(masks))
        if totals[agent][complete[agent]]
        < max(
            thresholds[agent][complete[target]]
            for target in range(len(masks))
            if target != agent
        )
    )


def acceptance_edges(masks, floater, host, totals, thresholds):
    complete = list(masks)
    complete[host] |= 1 << floater
    return {
        (agent, assigned)
        for agent in range(len(masks))
        for assigned in range(len(masks))
        if totals[agent][complete[assigned]]
        >= max(
            thresholds[agent][complete[target]]
            for target in range(len(masks))
            if target != assigned
        )
    }


def states(n, m):
    for floater in range(m):
        allocated = [good for good in range(m) if good != floater]
        for owners in itertools.product(range(n), repeat=len(allocated)):
            masks = [0] * n
            for good, owner in zip(allocated, owners):
                masks[owner] |= 1 << good
            if all(masks):
                yield tuple(masks), floater


def random_values(n, m, cap, rng):
    return tuple(tuple(rng.randint(1, cap) for _ in range(m)) for _ in range(n))


def run(n, m, cap, profiles, seed, output):
    if output.exists():
        raise ValueError("output must be new")
    rng = random.Random(seed)
    eligible_states = 0
    full_unique_defects = 0
    redirected_absorptions = 0
    redirected_two_cycles = 0
    other_redirected_defects = 0
    counterexample = None
    for profile in range(profiles):
        values = random_values(n, m, cap, rng)
        totals, thresholds = tables(values)
        for masks, floater in states(n, m):
            if not eligible(masks, 1 << floater, totals, thresholds):
                continue
            eligible_states += 1
            for host in range(n):
                bad_agents = identity_bad_agents(
                    masks, floater, host, totals, thresholds
                )
                if len(bad_agents) != 1:
                    continue
                bad = bad_agents[0]
                if bad == host:
                    continue
                edges = acceptance_edges(
                    masks, floater, host, totals, thresholds
                )
                if any((agent, bad) in edges for agent in range(n)):
                    continue
                full_unique_defects += 1
                redirected = identity_bad_agents(
                    masks, floater, bad, totals, thresholds
                )
                if not redirected:
                    redirected_absorptions += 1
                    continue
                if redirected == (host,):
                    redirected_two_cycles += 1
                    continue
                other_redirected_defects += 1
                counterexample = {
                    "profile_index": profile,
                    "values": [list(row) for row in values],
                    "masks": list(masks),
                    "floater": floater,
                    "host": host,
                    "bad": bad,
                    "redirected_bad_agents": list(redirected),
                }
                break
            if counterexample is not None:
                break
        if counterexample is not None:
            break
    result = {
        "schema": SCHEMA,
        "status": (
            "HOST_TO_BAD_REDUCTION_COUNTEREXAMPLE_FOUND"
            if counterexample is not None
            else "HOST_TO_BAD_REDUCTION_SURVIVES_SEARCH"
        ),
        "n": n,
        "m": m,
        "cap": cap,
        "seed": seed,
        "profiles_requested": profiles,
        "profiles_tested": profile + 1 if profiles else 0,
        "eligible_state_count": eligible_states,
        "full_unique_defect_count": full_unique_defects,
        "redirected_absorption_count": redirected_absorptions,
        "redirected_two_cycle_count": redirected_two_cycles,
        "other_redirected_defect_count": other_redirected_defects,
        "counterexample": counterexample,
        "claim_boundary": (
            "This tests whether redirecting the charity good from the host to "
            "the unique bad bundle either absorbs immediately or leaves only "
            "the old host bad. It scans all one-charity EFX states in sampled "
            "valuation profiles, without imposing global extremality."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=7)
    parser.add_argument("--cap", type=int, default=6)
    parser.add_argument("--profiles", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260803)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(**vars(args)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
