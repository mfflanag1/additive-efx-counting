#!/usr/bin/env python3
"""Perturb the bounded radius-three countermodel to subset-sum injectivity."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from fractions import Fraction
from pathlib import Path

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        validate_flower_master,
        value,
    )
    from .decide_flexible_later_owner_connected_transfer import enumerate_connected
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        validate_flower_master,
        value,
    )
    from decide_flexible_later_owner_connected_transfer import enumerate_connected


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def live_polarity(values):
    bottom_r = ("aq_br_0", "aq_br_1", "br_rest_0", "br_rest_1")
    bottom_q = ("ar_bq_0", "ar_bq_1")
    return (
        value(values, "r", bottom_r) >= values["r"]["f"]
        and values["r"]["f"] > value(values, "r", bottom_q)
        and value(values, "q", bottom_q) > value(values, "q", bottom_r)
    )


def perturb(source_values, seed, delta):
    result = {}
    goods = sorted(source_values[AGENTS[0]])
    for offset, agent in enumerate(AGENTS):
        order = goods[:]
        random.Random(seed * len(AGENTS) + offset).shuffle(order)
        rank = {good: index for index, good in enumerate(order)}
        result[agent] = {
            good: source_values[agent][good] + delta * (1 << rank[good])
            for good in goods
        }
    return result


def run(source_path, maximum_seed, delta_power):
    source = json.loads(source_path.read_text())
    if source.get("status") != "sat":
        raise ValueError("source is not a SAT CEGAR result")
    source_values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = validate_flower_master(source_values)
    candidates = enumerate_connected(
        old, radius=3, rooted=False, structural_reductions=False
    )
    assert len(candidates) == 41394
    delta = Fraction(1, 1 << delta_power)
    goods = len(source_values[AGENTS[0]])
    assert delta * ((1 << goods) - 1) < Fraction(1, 32)
    for seed in range(maximum_seed):
        values = perturb(source_values, seed, delta)
        try:
            validate_flower_master(values)
        except AssertionError:
            continue
        if not live_polarity(values):
            continue
        successful = sum(
            lex_endpoint_succeeds(values, old, allocation)
            for allocation in candidates
        )
        if successful:
            continue
        script = Path(__file__).resolve()
        root = script.parents[2]
        return {
            "schema": "flexible-lex-radius3-hardened-countermodel-v1",
            "status": "HARDENED_COUNTERMODEL",
            "seed": seed,
            "delta": str(delta),
            "atom_count": goods,
            "connected_radius3_candidate_count": len(candidates),
            "successful_lex_endpoint_count": 0,
            "subset_sum_injective": True,
            "subset_sum_injectivity_argument": (
                "all source values are multiples of 1/16; the total binary "
                "perturbation is below 1/32, so unequal source subset sums "
                "cannot collide, while equal source subset sums receive "
                "distinct binary perturbation sums"
            ),
            "values": {
                agent: {good: str(amount) for good, amount in row.items()}
                for agent, row in values.items()
            },
            "claim_boundary": (
                "positive subset-sum-injective bounded two-atom live-polarity "
                "flower valuation with no connected radius-three lex EFX "
                "endpoint; this refutes the bounded local transfer claim but "
                "does not refute EFX existence or a larger component lemma"
            ),
            "provenance": {
                "source": str(source_path.relative_to(root)),
                "source_sha256": sha256(source_path),
                "script": str(script.relative_to(root)),
                "script_sha256": sha256(script),
            },
        }
    return {
        "schema": "flexible-lex-radius3-hardened-countermodel-v1",
        "status": "NO_HARDENING_FOUND",
        "maximum_seed": maximum_seed,
        "delta": str(delta),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-seed", type=int, default=1000)
    parser.add_argument("--delta-power", type=int, default=30)
    args = parser.parse_args()
    result = run(args.source.resolve(), args.maximum_seed, args.delta_power)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "seed": result.get("seed"),
    }, indent=2))


if __name__ == "__main__":
    main()
