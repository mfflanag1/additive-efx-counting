#!/usr/bin/env python3
"""Exact audit of the surplus-budgeted component lemma and a branching witness."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path


AGENTS = ("r", "q", "c", "s")
RECIPIENTS = AGENTS + ("_",)
OLD_COMPONENTS = {
    "r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "q": ("aq_tq", "ar_bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}
BRANCHING_ALLOCATION = {
    "_": (),
    "c": ("aq_br_0", "bc_0", "bc_1", "tc_0"),
    "q": ("aq_tq_0", "aq_tq_1", "ar_bq_0", "ar_bq_1", "br_rest_1"),
    "r": (
        "aq_br_1",
        "ar_tr_0",
        "ar_tr_1",
        "br_rest_0",
        "f",
        "tr_rest_0",
        "tr_rest_1",
    ),
    "s": ("tc_1", "z"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atom_names(component: str) -> tuple[str, ...]:
    if component in ("f", "z"):
        return (component,)
    return tuple(f"{component}_{index}" for index in range(2))


def old_bundles() -> dict[str, tuple[str, ...]]:
    return {
        agent: tuple(
            good
            for component in components
            for good in atom_names(component)
        )
        for agent, components in OLD_COMPONENTS.items()
    }


def value(values, observer: str, goods) -> Fraction:
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer: str, goods) -> Fraction:
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return value(values, observer, goods) - min(values[observer][good] for good in goods)


def transfer_topology(old, allocation) -> dict:
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    new_owner = {
        good: recipient
        for recipient in RECIPIENTS
        for good in allocation[recipient]
    }
    moved = sorted(good for good in new_owner if new_owner[good] != base_owner[good])
    edges = Counter((base_owner[good], new_owner[good]) for good in moved)
    adjacency = defaultdict(set)
    for source, target in edges:
        adjacency[source].add(target)
        adjacency[target].add(source)
    unseen = set(adjacency)
    components = []
    while unseen:
        root = min(unseen)
        queue = deque([root])
        seen = {root}
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
            for (source, target), count in sorted(edges.items())
        ],
        "nontrivial_components": sorted(components),
        "signature": ";".join(
            f"{source}->{target}:{count}"
            for (source, target), count in sorted(edges.items())
        ),
    }


def run(root: Path) -> dict:
    source_path = root / "results" / "flexible_lex_basic_pi_free_cegar.json"
    source = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = old_bundles()
    allocation = BRANCHING_ALLOCATION
    all_goods = set(values[AGENTS[0]])
    assigned = [good for recipient in RECIPIENTS for good in allocation[recipient]]
    assert len(assigned) == len(all_goods) and set(assigned) == all_goods

    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: value(values, agent, allocation[agent]) for agent in AGENTS}
    base_efx = all(
        base[observer] >= tail(values, observer, old[target])
        for observer in AGENTS
        for target in AGENTS
    ) and all(base[observer] >= values[observer]["f"] for observer in AGENTS)
    assert base_efx

    changed = [
        agent for agent in AGENTS if set(allocation[agent]) != set(old[agent])
    ]
    surplus = {agent: own[agent] - base[agent] for agent in AGENTS}
    weakly_paid = {agent: surplus[agent] >= 0 for agent in changed}
    strictly_paid = {agent: surplus[agent] > 0 for agent in changed}
    overshoots = {
        f"{observer}->{target}": max(
            Fraction(0), tail(values, observer, allocation[target]) - base[observer]
        )
        for observer in AGENTS
        for target in changed
        if observer != target
    }
    surplus_budget_failures = [
        key
        for key, amount in overshoots.items()
        if amount > surplus[key.split("->", 1)[0]]
    ]
    positive_overshoots = {
        key: str(amount) for key, amount in overshoots.items() if amount > 0
    }
    final_efx = all(
        own[observer] >= tail(values, observer, allocation[target])
        for observer in AGENTS
        for target in AGENTS
    ) and all(
        own[observer] >= value(values, observer, allocation["_"])
        for observer in AGENTS
    )
    topology = transfer_topology(old, allocation)
    assert all(weakly_paid.values())
    assert all(strictly_paid.values())
    assert len(positive_overshoots) == 5
    assert not surplus_budget_failures
    assert final_efx
    assert allocation["_"] == ()
    assert len(topology["nontrivial_components"]) == 1
    assert topology["signature"] == "_->r:1;c->s:1;r->c:1;r->q:1"

    theorem = root / "results" / "SURPLUS_BUDGETED_CONNECTED_COMPONENT_TRANSFER_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "surplus-budgeted-connected-component-transfer-audit-v1",
        "status": "VERIFIED",
        "base_efx": base_efx,
        "changed_owners": changed,
        "surpluses": {agent: str(amount) for agent, amount in surplus.items()},
        "weakly_paid": weakly_paid,
        "strictly_paid": strictly_paid,
        "positive_threshold_overshoots": positive_overshoots,
        "surplus_budget_failures": surplus_budget_failures,
        "final_efx": final_efx,
        "charity_only_donates": True,
        "topology": topology,
        "claim_boundary": (
            "exact branching exemplar plus cap-free endpoint implication; "
            "terminal-polarity packet selection and GG closure remain open"
        ),
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results" / "surplus_budgeted_connected_component_transfer_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
