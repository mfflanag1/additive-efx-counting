#!/usr/bin/env python3
"""Enumerate instances of the cap-free two-wall Hall conversion lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "partial-hall-two-wall-gate-audit-v1"


def goods(mask, m):
    return tuple(good for good in range(m) if mask & (1 << good))


def value(values, agent, mask):
    return sum(values[agent][good] for good in goods(mask, len(values[0])))


def efx_comparisons(masks, matching, m):
    comparisons = []
    for agent, assigned in enumerate(matching):
        own = masks[assigned]
        for target, target_mask in enumerate(masks):
            if target == assigned:
                continue
            for removed in goods(target_mask, m):
                comparisons.append(
                    (agent, own, target_mask & ~(1 << removed))
                )
    return comparisons


def partial_comparisons(masks, floater, m):
    comparisons = efx_comparisons(masks, tuple(range(len(masks))), m)
    comparisons.extend(
        (agent, masks[agent], 1 << floater)
        for agent in range(len(masks))
    )
    return comparisons


def holds(values, comparison):
    agent, left, right = comparison
    return value(values, agent, left) >= value(values, agent, right)


def public_comparison(comparison):
    agent, left, right = comparison
    return {"agent": agent, "left_mask": left, "right_mask": right}


def profile(document):
    values = document.get("values")
    state = document.get("fixed_state")
    if state is None and document.get("base_bundles") is not None:
        state = {
            "floater": document["floater"],
            "masks": [
                sum(1 << good for good in part)
                for part in document["base_bundles"]
            ],
        }
    if values is None or state is None:
        raise ValueError(
            "source must contain values and either fixed_state or base_bundles"
        )
    return [list(map(int, row)) for row in values], state


def audit_source(source):
    document = json.loads(source.read_text())
    values, state = profile(document)
    n = len(values)
    m = len(values[0])
    base = tuple(map(int, state["masks"]))
    floater = int(state["floater"])
    base_eligible = all(
        holds(values, item) for item in partial_comparisons(base, floater, m)
    )
    if not base_eligible:
        raise ValueError(f"source base is not an eligible partial EFX state: {source}")
    gates = []
    for agent_a in range(n):
        bundle_a = base[agent_a]
        for agent_c in range(n):
            if agent_c == agent_a:
                continue
            bundle_c = base[agent_c]
            for x in goods(bundle_a, m):
                for y in goods(bundle_a, m):
                    if y == x:
                        continue
                    remainder = bundle_a & ~(1 << x) & ~(1 << y)
                    direct = list(base)
                    direct[agent_c] |= 1 << floater
                    direct_matching = tuple(range(n))
                    critical_direct = (agent_a, bundle_a, bundle_c)
                    direct_comparisons = efx_comparisons(
                        direct, direct_matching, m
                    )
                    direct_support = [
                        item
                        for item in direct_comparisons
                        if item != critical_direct
                    ]
                    if not all(holds(values, item) for item in direct_support):
                        continue

                    transfer = list(base)
                    transfer[agent_a] = (
                        bundle_a & ~(1 << x)
                    ) | (1 << floater)
                    transfer[agent_c] = bundle_c | (1 << x)
                    transfer_matching = list(range(n))
                    transfer_matching[agent_a] = agent_c
                    transfer_matching[agent_c] = agent_a
                    critical_transfer = (
                        agent_a,
                        transfer[agent_c],
                        remainder | (1 << floater),
                    )
                    transfer_comparisons = efx_comparisons(
                        transfer, tuple(transfer_matching), m
                    )
                    transfer_support = [
                        item
                        for item in transfer_comparisons
                        if item != critical_transfer
                    ]
                    if not all(
                        holds(values, item) for item in transfer_support
                    ):
                        continue

                    conversion = list(base)
                    conversion[agent_a] = remainder | (1 << floater)
                    conversion[agent_c] = bundle_c | (1 << y)
                    conversion_comparisons = partial_comparisons(
                        conversion, x, m
                    )
                    if not all(
                        holds(values, item) for item in conversion_comparisons
                    ):
                        continue

                    direct_holds = holds(values, critical_direct)
                    transfer_holds = holds(values, critical_transfer)
                    base_utilities = [
                        value(values, agent, base[agent])
                        for agent in range(n)
                    ]
                    conversion_utilities = [
                        value(values, agent, conversion[agent])
                        for agent in range(n)
                    ]
                    gates.append(
                        {
                            "agent_a": agent_a,
                            "agent_c": agent_c,
                            "x": x,
                            "y": y,
                            "critical_direct": public_comparison(
                                critical_direct
                            ),
                            "critical_direct_holds": direct_holds,
                            "critical_transfer": public_comparison(
                                critical_transfer
                            ),
                            "critical_transfer_holds": transfer_holds,
                            "direct_masks": direct,
                            "transfer_masks": transfer,
                            "transfer_matching": transfer_matching,
                            "conversion_masks": conversion,
                            "conversion_floater": x,
                            "conversion_utilities": conversion_utilities,
                            "base_utilities": base_utilities,
                            "conversion_pareto_dominates": all(
                                after >= before
                                for before, after in zip(
                                    base_utilities, conversion_utilities
                                )
                            )
                            and any(
                                after > before
                                for before, after in zip(
                                    base_utilities, conversion_utilities
                                )
                            ),
                        }
                    )
    return {
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "n": n,
        "m": m,
        "fixed_state": state,
        "base_eligible": base_eligible,
        "gate_count": len(gates),
        "gates": gates,
    }


def run(sources, output):
    records = [audit_source(source) for source in sources]
    artifact = {
        "schema": SCHEMA,
        "status": "AUDITED",
        "meaning": (
            "Each listed gate exactly satisfies the three support conditions "
            "of the cap-free two-wall Hall conversion lemma. Zero gates is a "
            "coverage boundary, not a counterexample to the lemma."
        ),
        "records": records,
        "source_count": len(records),
        "covered_source_count": sum(record["gate_count"] > 0 for record in records),
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = run(args.source, args.output)
    print(json.dumps(artifact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
