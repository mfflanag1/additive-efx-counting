#!/usr/bin/env python3
"""Audit the bounded rooted connected-transfer refutation arithmetically."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path

try:
    from .decide_three_nonsingleton_flower_one_unpaid_cover import (
        BASE,
        candidate_covers,
    )
except ImportError:
    from decide_three_nonsingleton_flower_one_unpaid_cover import (
        BASE,
        candidate_covers,
    )


AGENTS = ("r", "q", "c", "s")
RECIPIENTS = (*AGENTS, "_")
OLD_COMPONENTS = {
    "r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "q": ("aq_tq", "ar_bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}
COMPONENT_BUNDLES = {
    "A_q": ("aq_tq", "aq_br"),
    "A_r": ("ar_tr", "ar_bq"),
    "D_r": ("aq_tq", "f"),
    "D_q": ("ar_tr", "tr_rest", "f"),
    "D_c": ("tc", "f"),
    "X_r": OLD_COMPONENTS["r"],
    "X_q": OLD_COMPONENTS["q"],
    "X_c": OLD_COMPONENTS["c"],
    "Z": ("z",),
}


def atom_names(component):
    if component in ("f", "z"):
        return (component,)
    return tuple(f"{component}_{index}" for index in range(2))


def old_bundles():
    return {
        agent: tuple(
            good for component in components for good in atom_names(component)
        )
        for agent, components in OLD_COMPONENTS.items()
    }


def value(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return value(values, observer, goods) - min(values[observer][good] for good in goods)


def validate(values, old, allocation):
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: value(values, agent, allocation[agent]) for agent in AGENTS}
    assert own["r"] >= base["r"] and own["q"] > base["q"]
    for observer in AGENTS:
        for target in AGENTS:
            assert own[observer] >= tail(values, observer, allocation[target])
        assert own[observer] >= value(values, observer, allocation["_"])


def transfer_topology(old, allocation):
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    new_owner = {
        good: recipient for recipient in RECIPIENTS for good in allocation[recipient]
    }
    moved = sorted(good for good in new_owner if new_owner[good] != base_owner[good])
    edge_counts = Counter((base_owner[good], new_owner[good]) for good in moved)
    adjacency = defaultdict(set)
    for source, target in edge_counts:
        adjacency[source].add(target)
        adjacency[target].add(source)
    components = []
    unseen = set(adjacency)
    while unseen:
        root = min(unseen)
        seen = {root}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        unseen -= seen
        components.append(sorted(seen))
    return {
        "moved_goods": moved,
        "edge_counts": [
            {"source": source, "target": target, "count": count}
            for (source, target), count in sorted(edge_counts.items())
        ],
        "nontrivial_components": sorted(components),
        "signature": ";".join(
            f"{source}->{target}:{count}"
            for (source, target), count in sorted(edge_counts.items())
        ),
    }


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path, root):
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def endpoint_succeeds(values, old, allocation):
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: value(values, agent, allocation[agent]) for agent in AGENTS}
    if own["r"] < base["r"] or own["q"] <= base["q"]:
        return False
    for observer in AGENTS:
        for target in AGENTS:
            if own[observer] < tail(values, observer, allocation[target]):
                return False
        if own[observer] < value(values, observer, allocation["_"]):
            return False
    return True


def lex_endpoint_succeeds(values, old, allocation):
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: value(values, agent, allocation[agent]) for agent in AGENTS}
    lex_improves = any(
        all(own[AGENTS[index]] == base[AGENTS[index]] for index in range(position))
        and own[agent] > base[agent]
        for position, agent in enumerate(AGENTS)
    )
    if not lex_improves:
        return False
    for observer in AGENTS:
        for target in AGENTS:
            if own[observer] < tail(values, observer, allocation[target]):
                return False
        if own[observer] < value(values, observer, allocation["_"]):
            return False
    return True


def validate_flower_master(values):
    assert all(amount > 0 for row in values.values() for amount in row.values())
    bundles = {
        name: tuple(good for component in parts for good in atom_names(component))
        for name, parts in COMPONENT_BUNDLES.items()
    }
    old = old_bundles()
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    for agent in AGENTS:
        for goods in bundles.values():
            assert tail(values, agent, goods) <= base[agent]
        assert values[agent]["f"] <= base[agent]
        assert value(values, agent, old["c"]) <= base[agent]
    for name, owner in {
        "D_r": "r",
        "D_q": "q",
        "D_c": "r",
        "Z": "c",
        "A_q": "c",
        "A_r": "c",
    }.items():
        assert value(values, owner, bundles[name]) > base[owner]
    for cover in candidate_covers("r", "c", "c", "c", tuple(AGENTS)):
        if cover["unpaid_agent"] is None:
            continue
        unpaid = cover["unpaid_agent"]
        payment = bundles[cover["assignment"][unpaid]]
        assert any(
            value(values, unpaid, payment)
            < tail(values, unpaid, bundles[cover["assignment"][target]])
            for target in AGENTS if target != unpaid
        )
    assert any(values["q"]["f"] > values["q"][good] for good in old["q"])
    return old


def allocation_key(allocation):
    return tuple(tuple(sorted(allocation[recipient])) for recipient in (*AGENTS, "_"))


def apply_moves(old, moves):
    allocation = {agent: list(old[agent]) for agent in AGENTS}
    allocation["_"] = ["f"]
    for good, source, target in moves:
        allocation[source].remove(good)
        allocation[target].append(good)
    return {recipient: sorted(goods) for recipient, goods in allocation.items()}


def rooted_allocations(old):
    allocations = {}
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    for released in old["q"]:
        root = (("f", "_", "q"), (released, "q", "_"))
        allocation = apply_moves(old, root)
        allocations[allocation_key(allocation)] = allocation
        for good, source in base_owner.items():
            if good == released or source in ("r", "s"):
                continue
            for target in (*AGENTS, "_"):
                if target == source:
                    continue
                if source != "q" and target not in ("q", "_"):
                    continue
                candidate = apply_moves(old, (*root, (good, source, target)))
                allocations[allocation_key(candidate)] = candidate
    return tuple(allocations.values())


def radius_one_allocations(old):
    allocations = []
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    for good, source in base_owner.items():
        for target in (*AGENTS, "_"):
            if target != source:
                allocations.append(apply_moves(old, ((good, source, target),)))
    return tuple(allocations)


def run(source_path):
    source = json.loads(source_path.read_text())
    if source["status"] != "sat" or not source["rooted_at_selected_replacement"]:
        raise ValueError("source is not the rooted SAT refutation")
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = validate_flower_master(values)

    rooted = rooted_allocations(old)
    assert len(rooted) == source["candidate_allocation_count"]
    assert not any(endpoint_succeeds(values, old, allocation) for allocation in rooted)
    nearest = source["nearest_flexible_escape"]
    allocation = nearest["allocation"]
    validate(values, old, allocation)
    assert transfer_topology(old, allocation) == nearest["topology"]
    radius_one = radius_one_allocations(old)
    assert not any(endpoint_succeeds(values, old, candidate) for candidate in radius_one)
    assert nearest["minimum_moved_goods"] == 2
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flexible-later-owner-rooted-connected-transfer-refutation-audit-v1",
        "status": "VERIFIED",
        "rooted_candidate_count": len(rooted),
        "minimum_flexible_escape_radius": 2,
        "escape_topology": nearest["topology"],
        "claim_boundary": (
            "exact arithmetic audit of one bounded representative flower model "
            "blocking every connected radius-three transfer rooted at the selected "
            "f-for-good replacement; it does not refute the unrestricted connected "
            "radius-three lemma or any EFX existence claim"
        ),
        "provenance": {
            "source": display_path(source_path, root),
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
        "rooted_candidate_count": result["rooted_candidate_count"],
        "escape_signature": result["escape_topology"]["signature"],
    }, indent=2))


if __name__ == "__main__":
    main()
