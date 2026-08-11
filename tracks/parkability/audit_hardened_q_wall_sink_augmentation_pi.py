#!/usr/bin/env python3
"""Replay two sink augmentations and the final PI matching on the hardened Q-wall."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


AGENTS = ("r", "q", "c", "s")
COMPONENTS = {
    "r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "q": ("aq_tq", "ar_bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atoms(component):
    if component == "z":
        return (component,)
    return tuple(f"{component}_{index}" for index in range(2))


def base_bundles():
    return {
        agent: frozenset(
            good for component in components for good in atoms(component)
        )
        for agent, components in COMPONENTS.items()
    }


def value(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return value(values, observer, goods) - min(
        values[observer][good] for good in goods
    )


def common_safe(values, base, goods):
    return all(tail(values, observer, goods) <= base[observer] for observer in AGENTS)


def desired_subsets(values, base, source, offered):
    desired = []
    offered = tuple(offered)
    for size in range(1, len(offered) + 1):
        for group in map(frozenset, itertools.combinations(offered, size)):
            if value(values, source, group) > base[source] and common_safe(
                values, base, group
            ):
                desired.append(group)
    return [group for group in desired if not any(other < group for other in desired)]


def run(profile_path):
    profile = json.loads(profile_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in profile["values"].items()
    }
    old = base_bundles()
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    all_goods = set().union(*old.values(), {"f"})

    e_packet = frozenset(("aq_tq_0", "ar_bq_1"))
    q_target = frozenset(("ar_bq_0", "aq_tq_1", "f"))
    first_desired = frozenset(("z",))
    first_sink = old["c"] | e_packet
    second_desired = frozenset(("aq_tq_0", "bc_0", "bc_1", "tc_1"))
    second_sink = old["r"] | (first_sink - second_desired)

    assert common_safe(values, base, first_desired)
    assert value(values, "c", first_desired) > base["c"]
    assert value(values, "s", first_sink) > base["s"]
    assert common_safe(values, base, second_desired)
    assert value(values, "r", second_desired) > base["r"]
    assert value(values, "s", second_sink) > base["s"]

    allocation = {
        "q": q_target,
        "c": first_desired,
        "r": second_desired,
        "s": second_sink,
        "_": frozenset(),
    }
    assigned = set().union(*allocation.values())
    assert assigned == all_goods
    assert sum(map(len, allocation.values())) == len(all_goods)
    utilities = {
        agent: value(values, agent, allocation[agent]) for agent in AGENTS
    }
    assert all(utilities[agent] > base[agent] for agent in AGENTS)

    responses = {
        target: {
            source: desired_subsets(values, base, source, allocation[target])
            for source in AGENTS
        }
        for target in AGENTS
    }
    responses = {
        target: {
            source: groups for source, groups in by_source.items() if groups
        }
        for target, by_source in responses.items()
    }
    matching = {"q": "s", "c": "c", "r": "r", "s": "q"}
    assert all(matching[target] in responses[target] for target in AGENTS)
    assert len(set(matching.values())) == len(AGENTS)

    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    new_owner = {
        good: recipient for recipient, goods in allocation.items() for good in goods
    }
    incoming = {
        target: sorted(
            good for good in allocation[target] if base_owner[good] != target
        )
        for target in AGENTS
    }
    released = {
        source: sorted(
            good for good in old[source] if new_owner[good] != source
        )
        for source in AGENTS
    }
    incoming_goods = [good for packet in incoming.values() for good in packet]
    assert len(incoming_goods) == len(set(incoming_goods))
    assert set(incoming_goods) <= {"f"}.union(
        good for packet in released.values() for good in packet
    )

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "hardened-q-wall-sink-augmentation-pi-audit-v1",
        "status": "PI_RESPONSE_MATCHING",
        "augmentation_sequence": [
            {
                "new_source": "c",
                "desired_subset": sorted(first_desired),
                "sink": "s",
                "new_sink_target": sorted(first_sink),
            },
            {
                "new_source": "r",
                "desired_subset": sorted(second_desired),
                "sink": "s",
                "new_sink_target": sorted(second_sink),
            },
        ],
        "allocation": {
            owner: sorted(goods) for owner, goods in allocation.items()
        },
        "base_utilities": {agent: str(base[agent]) for agent in AGENTS},
        "final_utilities": {agent: str(utilities[agent]) for agent in AGENTS},
        "response_sources": {
            target: {
                source: [sorted(group) for group in groups]
                for source, groups in by_source.items()
            }
            for target, by_source in responses.items()
        },
        "internal_matching": matching,
        "incoming_packets": incoming,
        "released_packets": released,
        "incoming_disjoint": True,
        "all_incoming_supplied": True,
        "claim_boundary": (
            "exact solver-free closure of one hardened bounded profile by two "
            "sink augmentations and a generalized PI matching; not a cap-free "
            "proof that every flower profile follows this branch"
        ),
        "provenance": {
            "source": str(profile_path.relative_to(root)),
            "source_sha256": sha256(profile_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.profile.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "matching": result["internal_matching"],
    }, indent=2))


if __name__ == "__main__":
    main()
