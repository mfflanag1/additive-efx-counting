#!/usr/bin/env python3
"""Audit the bounded connected-radius-three flower counterexample exactly."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        RECIPIENTS,
        allocation_key,
        apply_moves,
        endpoint_succeeds,
        lex_endpoint_succeeds,
        old_bundles,
        transfer_topology,
        validate_flower_master,
        value,
    )
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        RECIPIENTS,
        allocation_key,
        apply_moves,
        endpoint_succeeds,
        lex_endpoint_succeeds,
        old_bundles,
        transfer_topology,
        validate_flower_master,
        value,
    )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def connected(edges):
    adjacency = defaultdict(set)
    for source, target in edges:
        adjacency[source].add(target)
        adjacency[target].add(source)
    root = next(iter(adjacency))
    seen = {root}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(adjacency)


def all_connected_allocations(old, maximum_radius=3):
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    goods = tuple(sorted(base_owner))
    allocations = {}
    radius_counts = Counter()
    for radius in range(1, maximum_radius + 1):
        for selected in itertools.combinations(goods, radius):
            sources = tuple(base_owner[good] for good in selected)
            targets_by_good = tuple(
                tuple(recipient for recipient in RECIPIENTS if recipient != source)
                for source in sources
            )
            for targets in itertools.product(*targets_by_good):
                edges = tuple(zip(sources, targets))
                if not connected(edges):
                    continue
                moves = tuple(
                    (good, source, target)
                    for good, source, target in zip(selected, sources, targets)
                )
                allocation = apply_moves(old, moves)
                key = allocation_key(allocation)
                if key not in allocations:
                    allocations[key] = (radius, allocation)
                    radius_counts[radius] += 1
    return tuple(allocations.values()), radius_counts


RADIUS_FOUR_WITNESS = {
    "r": [
        "aq_br_1", "ar_bq_0", "ar_tr_0", "br_rest_0", "br_rest_1",
        "tr_rest_0", "tr_rest_1",
    ],
    "q": ["aq_br_0", "aq_tq_1", "ar_bq_1", "ar_tr_1"],
    "c": ["bc_0", "bc_1", "tc_0", "tc_1"],
    "s": ["z"],
    "_": ["aq_tq_0", "f"],
}


def run(source_path):
    source = json.loads(source_path.read_text())
    if (
        source.get("status") != "sat"
        or source.get("objective") != "later"
        or source.get("schema")
        != "flexible-later-owner-connected-radius3-relaxed-countermodel-v1"
    ):
        raise ValueError("source is not the bounded connected-radius-three SAT gate")
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = validate_flower_master(values)
    candidates, radius_counts = all_connected_allocations(old, 3)
    successes = [
        (radius, allocation)
        for radius, allocation in candidates
        if endpoint_succeeds(values, old, allocation)
    ]
    lex_successes = [
        (radius, allocation)
        for radius, allocation in candidates
        if lex_endpoint_succeeds(values, old, allocation)
    ]
    assert not successes
    assert lex_successes and min(radius for radius, _ in lex_successes) == 2
    assert len(candidates) == 41394
    assert sum(radius_counts.values()) == len(candidates)
    assigned = [good for recipient in RECIPIENTS for good in RADIUS_FOUR_WITNESS[recipient]]
    atoms = [good for agent in AGENTS for good in old[agent]] + ["f"]
    assert len(assigned) == len(atoms) and set(assigned) == set(atoms)
    assert endpoint_succeeds(values, old, RADIUS_FOUR_WITNESS)
    witness_topology = transfer_topology(old, RADIUS_FOUR_WITNESS)
    assert len(witness_topology["moved_goods"]) == 4
    assert len(witness_topology["nontrivial_components"]) == 1
    base_utilities = {
        agent: str(value(values, agent, old[agent])) for agent in AGENTS
    }
    witness_utilities = {
        agent: str(value(values, agent, RADIUS_FOUR_WITNESS[agent]))
        for agent in AGENTS
    }
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flexible-later-owner-connected-radius3-refutation-audit-v1",
        "status": "VERIFIED_RELAXED_REFUTATION",
        "full_connected_candidate_count": len(candidates),
        "radius_counts": {
            str(radius): count for radius, count in sorted(radius_counts.items())
        },
        "successful_candidate_count": 0,
        "lexicographic_escape_count_through_radius_three": len(lex_successes),
        "minimum_lexicographic_escape_radius": 2,
        "minimum_connected_escape_radius": 4,
        "radius_four_witness": {
            "allocation": RADIUS_FOUR_WITNESS,
            "topology": witness_topology,
            "base_utilities": base_utilities,
            "owner_utilities": witness_utilities,
        },
        "flower_master_verified": True,
        "claim_boundary": (
            "exact-Fraction audit of a bounded two-atom relaxed flower-master "
            "valuation with no connected redistribution of at most three "
            "goods that preserves r, strictly improves q, and maintains EFX; "
            "the same valuation has a radius-two earlier-owner lexicographic "
            "escape, so it does not refute the intended lex-hard residual lemma, "
            "EFX existence, or an arbitrary-size connected-component lemma"
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
        "full_connected_candidate_count": result["full_connected_candidate_count"],
        "radius_counts": result["radius_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
