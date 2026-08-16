#!/usr/bin/env python3
"""Decide whether one-rival frozen cores force agentwise Pareto gains."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .strengthen_partial_hall_master_with_frozen_cores import expression, mask_sum
except ImportError:
    from anneal import atomic_json
    from strengthen_partial_hall_master_with_frozen_cores import expression, mask_sum


SCHEMA = "partial-hall-core-rival-dominance-audit-v1"


def verdict(assumptions, query):
    solver = z3.Solver()
    solver.add(*assumptions, query)
    return str(solver.check())


def audit(source):
    document = json.loads(source.read_text())
    core = document.get("deletion_irreducible_unsat_core") or document["unsat_core"]
    rivals = [item for item in core if item["kind"] == "maximality"]
    if len(rivals) != 1:
        raise ValueError(f"expected exactly one core rival: {source}")
    fixed_masks = tuple(map(int, document["fixed_state"]["masks"]))
    values = [[z3.Real(f"v_{a}_{g}") for g in range(9)] for a in range(4)]
    assumptions = [
        expression(item, values, fixed_masks, 9)[0]
        for item in core
        if item["kind"] != "maximality"
    ]
    rival = rivals[0]
    agents = []
    for agent in range(4):
        gain = (
            mask_sum(values, agent, rival["masks"][agent], 9)
            - mask_sum(values, agent, fixed_masks[agent], 9)
        )
        negative = verdict(assumptions, gain < 0)
        nonpositive = verdict(assumptions, gain <= 0)
        agents.append(
            {
                "agent": agent,
                "negative_gain_verdict": negative,
                "nonpositive_gain_verdict": nonpositive,
                "weak_gain_forced": negative == "unsat",
                "strict_gain_forced": nonpositive == "unsat",
            }
        )
    return {
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "rival": rival,
        "agents": agents,
        "pareto_dominance_forced": all(item["weak_gain_forced"] for item in agents)
        and any(item["strict_gain_forced"] for item in agents),
    }


def run(sources, output):
    records = [audit(source) for source in sources]
    artifact = {
        "schema": SCHEMA,
        "status": "AUDITED",
        "meaning": (
            "UNSAT for negative gain proves the core assumptions force a "
            "weak agentwise gain; UNSAT for nonpositive gain proves a strict "
            "gain."
        ),
        "source_count": len(records),
        "pareto_forced_count": sum(
            record["pareto_dominance_forced"] for record in records
        ),
        "records": records,
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
