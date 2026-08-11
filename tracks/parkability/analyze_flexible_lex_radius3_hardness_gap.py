#!/usr/bin/env python3
"""Locate which genuine hard-state premises the radius-three model violates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        tail,
        value,
    )
    from .analyze_flexible_later_owner_escape_topologies import old_bundles
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        tail,
        value,
    )
    from analyze_flexible_later_owner_escape_topologies import old_bundles


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def common_safe(values, base, goods):
    return all(tail(values, observer, goods) <= base[observer] for observer in AGENTS)


def desired_subsets(values, base, source, offered):
    desired = []
    for size in range(1, len(offered) + 1):
        for subset in itertools.combinations(offered, size):
            if (
                value(values, source, subset) > base[source]
                and common_safe(values, base, subset)
            ):
                desired.append(frozenset(subset))
    minimal = [
        subset for subset in desired
        if not any(other < subset for other in desired)
    ]
    return sorted((sorted(subset) for subset in minimal), key=lambda item: (len(item), item))


def directed_cycles(vertices, edges):
    cycles = set()
    for size in range(1, len(vertices) + 1):
        for cycle in itertools.permutations(vertices, size):
            if cycle[0] != min(cycle):
                continue
            if all((cycle[index], cycle[(index + 1) % size]) in edges for index in range(size)):
                reverse = tuple(reversed(cycle))
                cycles.add(min(cycle, reverse))
    return sorted(cycles, key=lambda item: (len(item), item))


def run(source_path):
    source = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = old_bundles()
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    envy_edges = sorted(
        (source, target)
        for source in AGENTS for target in AGENTS
        if source != target and value(values, source, old[target]) > base[source]
    )
    envy_cycles = directed_cycles(AGENTS, set(envy_edges))
    champion_offers = {}
    genuine_self_champions = []
    for target in AGENTS:
        offered = tuple(old[target]) + ("f",)
        by_source = {}
        for source_agent in AGENTS:
            minimal = desired_subsets(values, base, source_agent, offered)
            if not minimal:
                continue
            modes = sorted({"genuine" if "f" in subset else "ordinary" for subset in minimal})
            by_source[source_agent] = {
                "modes": modes,
                "minimal_desired_subsets": minimal,
            }
            if source_agent == target and "genuine" in modes:
                genuine_self_champions.append(target)
        champion_offers[target] = by_source

    displayed = {
        "D_r": ("r", ("aq_tq_0", "aq_tq_1", "f")),
        "D_q": (
            "q",
            ("ar_tr_0", "ar_tr_1", "tr_rest_0", "tr_rest_1", "f"),
        ),
        "D_c": ("r", ("tc_0", "tc_1", "f")),
        "A_q": ("c", ("aq_tq_0", "aq_tq_1", "aq_br_0", "aq_br_1")),
        "A_r": ("c", ("ar_tr_0", "ar_tr_1", "ar_bq_0", "ar_bq_1")),
        "Z": ("c", ("z",)),
    }
    displayed_minimal = {
        name: {
            "source": source_agent,
            "offer": list(offered),
            "minimal_desired_subsets": desired_subsets(
                values, base, source_agent, offered
            ),
        }
        for name, (source_agent, offered) in displayed.items()
    }
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flexible-lex-radius3-hardness-gap-v1",
        "status": "CLASSIFIED",
        "ordinary_envy_edges": [list(edge) for edge in envy_edges],
        "ordinary_envy_cycles": [list(cycle) for cycle in envy_cycles],
        "genuine_self_champions": sorted(genuine_self_champions),
        "champion_offers": champion_offers,
        "displayed_minimal_desired_sets": displayed_minimal,
        "globally_lex_maximal": False,
        "global_maximality_witness": (
            "results/flexible_lex_radius3_hardened_countermodel_escape.json"
        ),
        "claim_boundary": (
            "exact structural diagnostic of one bounded profile; it identifies "
            "which explicitly checkable PI-free flower premises fail but does "
            "not decide all generalized PI edge sets"
        ),
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "ordinary_envy_cycles": result["ordinary_envy_cycles"],
        "genuine_self_champions": result["genuine_self_champions"],
    }, indent=2))


if __name__ == "__main__":
    main()
