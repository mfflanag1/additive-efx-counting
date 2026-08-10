#!/usr/bin/env python3
"""Enumerate selected simple-cycle types with three nonsingleton owners."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


AGENTS = ("a", "b", "c", "s")
LARGE = frozenset(("a", "b", "c"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rotations(word: tuple[str, ...]):
    return tuple(word[index:] + word[:index] for index in range(len(word)))


def canonical_cycle(cycle: tuple[str, ...]) -> tuple[str, ...]:
    return min(rotations(cycle))


def canonical_pattern(pattern: tuple[str, ...]) -> str:
    return "".join(min(rotations(pattern)))


def run() -> dict:
    labeled_cycles = set()
    for length in range(2, 5):
        for cycle in itertools.permutations(AGENTS, length):
            labeled_cycles.add(canonical_cycle(cycle))

    classes: dict[tuple[str, tuple[str, ...]], dict] = {}
    labeled_configurations = 0
    for cycle in sorted(labeled_cycles):
        large_targets = tuple(agent for agent in cycle if agent in LARGE)
        for genuine_count in range(2, len(large_targets) + 1):
            for genuine_targets in itertools.combinations(large_targets, genuine_count):
                genuine_targets = frozenset(genuine_targets)
                pattern = tuple(
                    "S" if target == "s" else "G" if target in genuine_targets else "L"
                    for target in cycle
                )
                abstract = canonical_pattern(pattern)
                external = tuple(sorted(
                    "S" if agent == "s" else "L"
                    for agent in set(AGENTS) - set(cycle)
                ))
                key = (abstract, external)
                labeled_configurations += 1
                if key not in classes:
                    classes[key] = {
                        "cycle_length": len(cycle),
                        "cycle_pattern": abstract,
                        "external_types": list(external),
                        "genuine_count": genuine_count,
                        "representative_cycle": list(cycle),
                        "representative_genuine_targets": sorted(genuine_targets),
                        "labeled_configuration_count": 0,
                    }
                classes[key]["labeled_configuration_count"] += 1

    records = sorted(
        classes.values(),
        key=lambda record: (
            record["cycle_length"],
            record["genuine_count"],
            record["cycle_pattern"],
            record["external_types"],
        ),
    )
    expected = {
        (2, "GG", ("L", "S")),
        (3, "GGL", ("S",)),
        (3, "GGS", ("L",)),
        (3, "GGG", ("S",)),
        (4, "GGLS", ()),
        (4, "GGSL", ()),
        (4, "GLGS", ()),
        (4, "GGGS", ()),
    }
    observed = {
        (record["cycle_length"], record["cycle_pattern"], tuple(record["external_types"]))
        for record in records
    }
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-selected-cycle-census-v1",
        "status": "EXHAUSTIVE" if observed == expected else "FAILED",
        "class_count": len(records),
        "labeled_configuration_count": labeled_configurations,
        "classes": records,
        "notation": {
            "G": "nonsingleton target of a genuine selected champion edge",
            "L": "nonsingleton target of an ordinary selected envy edge",
            "S": "the singleton target of an ordinary selected envy edge",
        },
        "claim_boundary": "directed-cycle census up to rotation; it classifies selected simple cycles but proves no EFX escape",
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "classes": result["class_count"]}, indent=2))


if __name__ == "__main__":
    main()
