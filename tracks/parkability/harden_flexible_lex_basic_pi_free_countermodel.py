#!/usr/bin/env python3
"""Harden the radius-three model while preserving basic PI-freeness."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path

try:
    from .analyze_flexible_lex_radius3_hardness_gap import (
        desired_subsets,
        directed_cycles,
    )
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        validate_flower_master,
        value,
    )
    from .decide_flexible_later_owner_connected_transfer import enumerate_connected
    from .harden_flexible_lex_radius3_countermodel import live_polarity, sha256
except ImportError:
    from analyze_flexible_lex_radius3_hardness_gap import (
        desired_subsets,
        directed_cycles,
    )
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        validate_flower_master,
        value,
    )
    from decide_flexible_later_owner_connected_transfer import enumerate_connected
    from harden_flexible_lex_radius3_countermodel import live_polarity, sha256


def basic_pi_free(values, old):
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    envy_edges = {
        (source, target)
        for source in AGENTS for target in AGENTS
        if source != target and value(values, source, old[target]) > base[source]
    }
    if directed_cycles(AGENTS, envy_edges):
        return False
    genuine = {}
    for source in AGENTS:
        for target in AGENTS:
            subsets = desired_subsets(
                values, base, source, tuple(old[target]) + ("f",)
            )
            genuine[source, target] = any("f" in subset for subset in subsets)
    if any(genuine[agent, agent] for agent in AGENTS):
        return False
    for size in range(2, len(AGENTS) + 1):
        for cycle in itertools.permutations(AGENTS, size):
            if cycle[0] != min(cycle):
                continue
            edges = tuple(
                (cycle[index], cycle[(index + 1) % size])
                for index in range(size)
            )
            for genuine_index, edge in enumerate(edges):
                if not genuine[edge]:
                    continue
                if all(
                    other in envy_edges
                    for index, other in enumerate(edges)
                    if index != genuine_index
                ):
                    return False
    return True


def perturb(source_values, seed, delta):
    goods = sorted(source_values[AGENTS[0]])
    result = {}
    for offset, agent in enumerate(AGENTS):
        order = goods[:]
        random.Random(seed * len(AGENTS) + offset).shuffle(order)
        rank = {good: index for index, good in enumerate(order)}
        result[agent] = {
            good: source_values[agent][good] + delta * (1 << rank[good])
            for good in goods
        }
    return result


def run(source_path, maximum_seed):
    source = json.loads(source_path.read_text())
    if source.get("status") != "sat":
        raise ValueError("source is not a SAT basic-PI-free result")
    source_values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = validate_flower_master(source_values)
    candidates = enumerate_connected(
        old, radius=3, rooted=False, structural_reductions=False
    )
    common_denominator = math.lcm(*(
        amount.denominator
        for row in source_values.values() for amount in row.values()
    ))
    atom_count = len(source_values[AGENTS[0]])
    delta_power = common_denominator.bit_length() + atom_count + 2
    delta = Fraction(1, 1 << delta_power)
    assert delta * ((1 << atom_count) - 1) < Fraction(1, 2 * common_denominator)
    for seed in range(maximum_seed):
        values = perturb(source_values, seed, delta)
        try:
            validate_flower_master(values)
        except AssertionError:
            continue
        if not live_polarity(values) or not basic_pi_free(values, old):
            continue
        if any(
            lex_endpoint_succeeds(values, old, allocation)
            for allocation in candidates
        ):
            continue
        script = Path(__file__).resolve()
        root = script.parents[2]
        return {
            "schema": "flexible-lex-basic-pi-free-hardened-countermodel-v1",
            "status": "HARDENED_COUNTERMODEL",
            "seed": seed,
            "delta": str(delta),
            "source_common_denominator": common_denominator,
            "atom_count": atom_count,
            "positive": True,
            "subset_sum_injective": True,
            "flower_master_valid": True,
            "live_polarity_valid": True,
            "basic_pi_free": True,
            "connected_radius3_candidate_count": len(candidates),
            "successful_lex_endpoint_count": 0,
            "values": {
                agent: {good: str(amount) for good, amount in row.items()}
                for agent, row in values.items()
            },
            "claim_boundary": (
                "positive subset-sum-injective bounded representative flower "
                "valuation with no self champion, ordinary envy cycle, or "
                "one-genuine PI cycle and no connected radius-three lex EFX "
                "endpoint; generalized multi-genuine PI-freeness and global "
                "lex maximality are not claimed"
            ),
            "provenance": {
                "source": str(source_path.relative_to(root)),
                "source_sha256": sha256(source_path),
                "script": str(script.relative_to(root)),
                "script_sha256": sha256(script),
            },
        }
    return {
        "schema": "flexible-lex-basic-pi-free-hardened-countermodel-v1",
        "status": "NO_HARDENING_FOUND",
        "maximum_seed": maximum_seed,
        "delta": str(delta),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-seed", type=int, default=10000)
    args = parser.parse_args()
    result = run(args.source.resolve(), args.maximum_seed)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "seed": result.get("seed"),
    }, indent=2))


if __name__ == "__main__":
    main()
