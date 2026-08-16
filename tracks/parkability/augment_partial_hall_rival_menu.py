#!/usr/bin/env python3
"""Append best rivals from designated-trap screens to a stored rival menu."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_partial_hall_augmenting_exchange_topologies import (
        component_count,
        owner_vector,
        transfers,
    )
except ImportError:
    from anneal import atomic_json
    from audit_partial_hall_augmenting_exchange_topologies import (
        component_count,
        owner_vector,
        transfers,
    )


BASE_MASKS = (192, 14, 17, 32)
BASE_FLOATER = 8


def run(menu_path: Path, screen_paths: list[Path], output: Path) -> dict:
    menu = json.loads(menu_path.read_text())
    selected = [
        {"floater": record["floater"], "masks": list(record["masks"])}
        for record in menu["selected_rivals"]
    ]
    seen = {(record["floater"], tuple(record["masks"])) for record in selected}
    additions = []
    for screen_path in screen_paths:
        screen = json.loads(screen_path.read_text())
        for record in screen["records"]:
            rival = record.get("best_improving_rival")
            if rival is None:
                continue
            key = rival["floater"], tuple(rival["masks"])
            if key in seen:
                continue
            seen.add(key)
            target_owner = owner_vector(key[1], key[0])
            edges = transfers(owner_vector(BASE_MASKS, BASE_FLOATER), target_owner)
            addition = {
                "floater": key[0],
                "masks": list(key[1]),
                "owner_distance": len(edges),
                "transfer_component_count": component_count(edges),
                "source": str(screen_path),
            }
            additions.append(addition)
            selected.append({"floater": key[0], "masks": list(key[1])})
    artifact = {
        "schema": "partial-hall-cumulative-rival-menu-v1",
        "status": "CUMULATIVE_MENU",
        "meaning": (
            "Cumulative exact rival menu formed by retaining every input rival "
            "and appending distinct best improving rivals from the supplied SAT "
            "screen records. This is not a symbolic cover theorem."
        ),
        "base_menu": str(menu_path),
        "screen_sources": [str(path) for path in screen_paths],
        "base_selected_rival_count": len(menu["selected_rivals"]),
        "addition_count": len(additions),
        "additions": additions,
        "selected_rival_count": len(selected),
        "selected_rivals": selected,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--menu", type=Path, required=True)
    parser.add_argument("--screen", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.menu, args.screen, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
