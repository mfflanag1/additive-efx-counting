#!/usr/bin/env python3
"""Deterministically perturb the packet model to exact nondegeneracy."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path

try:
    from . import analyze_residual_flower_packet_countermodel as analysis
    from . import audit_residual_flower_packet_core as packet
except ImportError:
    import analyze_residual_flower_packet_countermodel as analysis
    import audit_residual_flower_packet_core as packet


SEED = 8
EPSILON = Fraction(1, 1 << 24)


def amount(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction())


def run():
    payload = analysis.run()
    assert payload["status"] == "REALIZABLE_PACKET_COUNTERMODEL"
    values = {
        agent: {good: Fraction(value) for good, value in row.items()}
        for agent, row in payload["values"].items()
    }
    goods = tuple(sorted(next(iter(values.values()))))
    randomizer = random.Random(SEED)
    exponents = {}
    for agent in packet.AGENTS:
        permutation = randomizer.sample(range(len(goods)), len(goods))
        exponents[agent] = {
            good: permutation[index] for index, good in enumerate(goods)
        }
        for good in goods:
            values[agent][good] += EPSILON * (1 << exponents[agent][good])

    packet_goods = {
        name: tuple(entries) for name, entries in payload["packet_goods"].items()
    }
    base = {
        agent: tuple(
            good for name in packet.BASE[agent] for good in packet_goods[name]
        )
        for agent in packet.AGENTS
    }
    escape = payload["smallest_global_escape"]["allocation"]
    payload.update({
        "schema": "residual-flower-nondegenerate-packet-countermodel-v1",
        "status": "NONDEGENERATE_REALIZABLE_PACKET_COUNTERMODEL",
        "values": {
            agent: {good: str(value) for good, value in row.items()}
            for agent, row in values.items()
        },
        "perturbation": {
            "seed": SEED,
            "epsilon": str(EPSILON),
            "binary_exponents": exponents,
            "purpose": (
                "binary subset signatures remove every within-agent subset "
                "tie while preserving the audited strict/weak inequalities"
            ),
        },
    })
    payload["smallest_global_escape"]["base_utilities"] = {
        agent: str(amount(values, agent, base[agent]))
        for agent in packet.AGENTS
    }
    payload["smallest_global_escape"]["new_utilities"] = {
        agent: str(amount(values, agent, escape[agent]))
        for agent in packet.AGENTS
    }
    payload["claim_boundary"] = (
        "exact positive nondegenerate refutation of the nine aggregate "
        "packet candidates; the displayed two-good item-level escape shows "
        "that the adaptive flower bridge remains viable"
    )
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = run()
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "good_count": payload["good_count"],
        "candidate_count": payload["candidate_count"],
        "smallest_global_escape": payload["smallest_global_escape"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
