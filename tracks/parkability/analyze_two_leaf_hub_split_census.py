#!/usr/bin/env python3
"""Enumerate all improving two-leaf hub splits in a frozen flower profile."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .analyze_three_nonsingleton_flower_full_q_capture_witness import (
        AGENTS,
        load_values,
        old_owner,
    )
    from .audit_three_target_hub_hall_patterns import has_hub_cycle
except ImportError:
    from analyze_three_nonsingleton_flower_full_q_capture_witness import (
        AGENTS,
        load_values,
        old_owner,
    )
    from audit_three_target_hub_hall_patterns import has_hub_cycle


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(values, observer, bundle) -> int:
    return sum(values[observer][good] for good in bundle)


def tail(values, observer, bundle) -> int:
    if len(bundle) <= 1:
        return 0
    entries = [values[observer][good] for good in bundle]
    return sum(entries) - min(entries)


def wall_sources(values, allocation, target):
    target_tail = {observer: tail(values, observer, allocation[target]) for observer in AGENTS}
    return sorted(
        observer
        for observer in AGENTS
        if observer != target
        and value(values, observer, allocation[observer]) < target_tail[observer]
    )


def summarize_example(hub, leaves, packet, allocation, walls):
    return {
        "hub": hub,
        "leaves": list(leaves),
        "packet": sorted(packet),
        "allocation": {agent: sorted(allocation[agent]) for agent in AGENTS},
        "wall_sources": walls,
    }


def run(witness_path: Path) -> dict:
    witness_path = witness_path.resolve()
    witness, values, scale = load_values(witness_path)
    goods = tuple(values[AGENTS[0]])
    base = {
        agent: tuple(good for good in goods if old_owner(good) == agent)
        for agent in AGENTS
    }
    counts = Counter()
    by_hub = {agent: Counter() for agent in AGENTS}
    examples = {}

    for hub in AGENTS:
        hub_goods = base[hub]
        for leaves in itertools.combinations((agent for agent in AGENTS if agent != hub), 2):
            for assignment in itertools.product((0, 1, 2), repeat=len(hub_goods)):
                if 1 not in assignment or 2 not in assignment:
                    continue
                packet_parts = {
                    leaves[index]: tuple(
                        good for good, destination in zip(hub_goods, assignment)
                        if destination == index + 1
                    )
                    for index in range(2)
                }
                packet = tuple(good for good, destination in zip(hub_goods, assignment) if destination)
                if values[hub]["f"] <= value(values, hub, packet):
                    continue

                allocation = {agent: list(base[agent]) for agent in AGENTS}
                allocation[hub] = [good for good in hub_goods if good not in packet] + ["f"]
                for leaf in leaves:
                    allocation[leaf].extend(packet_parts[leaf])

                counts["eligible"] += 1
                by_hub[hub]["eligible"] += 1
                changed = (hub,) + leaves
                walls = {target: wall_sources(values, allocation, target) for target in changed}
                if not any(walls.values()):
                    classification = "efx"
                else:
                    internal = {
                        target: frozenset(source for source in walls[target] if source in changed)
                        for target in changed
                    }
                    relabel = {
                        "h": frozenset(
                            "h" if source == hub else "r" if source == leaves[0] else "s"
                            for source in internal[hub]
                        ),
                        "r": frozenset(
                            "h" if source == hub else "r" if source == leaves[0] else "s"
                            for source in internal[leaves[0]]
                        ),
                        "s": frozenset(
                            "h" if source == hub else "r" if source == leaves[0] else "s"
                            for source in internal[leaves[1]]
                        ),
                    }
                    if has_hub_cycle(relabel):
                        classification = "pi_hub_cycle"
                    elif any(not relabel[target] for target in ("h", "r", "s")):
                        empty_targets = [
                            target for target, actual in zip(("h", "r", "s"), changed)
                            if not relabel[target]
                        ]
                        has_external_wall = any(
                            walls[actual] for target, actual in zip(("h", "r", "s"), changed)
                            if target in empty_targets
                        )
                        classification = (
                            "open_external_wall" if has_external_wall else "terminal_internal_target"
                        )
                    else:
                        assert relabel["r"] == frozenset({"s"})
                        assert relabel["s"] == frozenset({"r"})
                        assert relabel["h"] and relabel["h"] <= frozenset({"r", "s"})
                        classification = "leaf_mutual_trap"

                counts[classification] += 1
                by_hub[hub][classification] += 1
                key = (classification, len(packet), hub, leaves)
                old_key = examples.get(classification, {}).get("_key")
                if old_key is None or key[1:] < old_key[1:]:
                    examples[classification] = {
                        "_key": key,
                        **summarize_example(hub, leaves, packet, allocation, walls),
                    }

    for example in examples.values():
        example.pop("_key")
    script = Path(__file__).resolve()
    root = script.parents[2]
    try:
        witness_label = str(witness_path.relative_to(root))
    except ValueError:
        witness_label = str(witness_path)
    return {
        "schema": "two-leaf-hub-split-census-v1",
        "status": "CLASSIFIED",
        "source_order_key": witness["source_order_key"],
        "integer_scale": scale,
        "counts": dict(sorted(counts.items())),
        "by_hub": {hub: dict(sorted(row.items())) for hub, row in by_hub.items()},
        "minimal_examples": examples,
        "claim_boundary": (
            "exact census of improving complete two-leaf hub splits in one frozen bounded flower "
            "profile; classifications use the analytic hub-wall lemma but do not prove a cap-free selector"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "witness": witness_label,
            "witness_sha256": sha256(witness_path),
        },
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--witness",
        type=Path,
        default=root / "results" / "three_nonsingleton_flower_full_capture_packet_gate.json",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.witness)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
