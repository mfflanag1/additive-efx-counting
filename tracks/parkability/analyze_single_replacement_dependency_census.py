#!/usr/bin/env python3
"""Classify one-good packet-for-charity starts in a frozen flower profile."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from .analyze_three_nonsingleton_flower_full_q_capture_witness import (
        AGENTS,
        load_values,
        old_owner,
    )
    from .analyze_two_leaf_hub_split_census import champion_sources, tail, value
except ImportError:
    from analyze_three_nonsingleton_flower_full_q_capture_witness import (
        AGENTS,
        load_values,
        old_owner,
    )
    from analyze_two_leaf_hub_split_census import champion_sources, tail, value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner_walls(values, allocation):
    return {
        target: [
            observer
            for observer in AGENTS
            if value(values, observer, allocation[observer])
            < tail(values, observer, allocation[target])
        ]
        for target in AGENTS
    }


def run(witness_path: Path, hub: str) -> dict:
    witness_path = witness_path.resolve()
    witness, values, scale = load_values(witness_path)
    goods = tuple(values[AGENTS[0]])
    base = {
        agent: tuple(good for good in goods if old_owner(good) == agent)
        for agent in AGENTS
    }
    counts = Counter()
    records = []

    for released in base[hub]:
        if values[hub]["f"] <= values[hub][released]:
            continue
        partial = {agent: list(base[agent]) for agent in AGENTS}
        partial[hub] = [good for good in base[hub] if good != released] + ["f"]
        walls = owner_walls(values, partial)
        target_walls = sorted(set().union(*walls.values()))
        charity_walls = sorted(
            observer
            for observer in AGENTS
            if value(values, observer, partial[observer]) < values[observer][released]
        )
        if not target_walls and not charity_walls:
            partial_class = "partial_efx"
        elif charity_walls:
            partial_class = "charity_dependency"
        else:
            partial_class = "target_dependency"
        counts[partial_class] += 1

        completions = []
        for leaf in (agent for agent in AGENTS if agent != hub):
            complete = {agent: list(partial[agent]) for agent in AGENTS}
            complete[leaf].append(released)
            complete_walls = owner_walls(values, complete)
            if not any(complete_walls.values()):
                classification = "complete_efx"
                responses = {}
            else:
                changed = (hub, leaf)
                responses = {
                    target: champion_sources(values, base, complete[target])
                    for target in changed
                }
                internal = {
                    target: set(responses[target]).intersection(changed)
                    for target in changed
                }
                if hub in internal[hub]:
                    classification = "pi_hub_self_response"
                elif (
                    hub in internal[leaf]
                    and leaf in internal[hub]
                ):
                    classification = "pi_two_cycle_response"
                elif any(not internal[target] for target in changed):
                    classification = "open_response_source"
                else:
                    classification = "two_target_hall_deficient"
            counts[f"one_leaf_{classification}"] += 1
            completions.append({
                "leaf": leaf,
                "classification": classification,
                "wall_observers": complete_walls,
                "champion_sources": responses,
            })

        records.append({
            "released": released,
            "partial_classification": partial_class,
            "target_wall_observers": walls,
            "charity_wall_observers": charity_walls,
            "hub_target_champion_sources": champion_sources(values, base, partial[hub]),
            "one_leaf_completions": completions,
        })

    script = Path(__file__).resolve()
    root = script.parents[2]
    try:
        witness_label = str(witness_path.relative_to(root))
    except ValueError:
        witness_label = str(witness_path)
    return {
        "schema": "single-replacement-dependency-census-v1",
        "status": "CLASSIFIED",
        "hub": hub,
        "source_order_key": witness["source_order_key"],
        "integer_scale": scale,
        "eligible_count": len(records),
        "counts": dict(sorted(counts.items())),
        "records": records,
        "claim_boundary": (
            "exact dependency and one-leaf completion census for improving singleton "
            "packet-for-charity replacements in one frozen bounded flower profile; it "
            "does not prove cap-free dependency termination"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "witness": witness_label,
            "witness_sha256": sha256(witness_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", type=Path, required=True)
    parser.add_argument("--hub", choices=AGENTS, default="q")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.witness, args.hub)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "eligible": result["eligible_count"],
        "counts": result["counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
