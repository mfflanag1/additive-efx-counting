#!/usr/bin/env python3
"""Exact replay of the dual-anchor selector on a strict-separated profile."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


AGENTS = ("r", "q", "c", "s")
BASE = {
    "r": (
        "aq_br_0", "aq_br_1", "ar_tr_0", "ar_tr_1",
        "br_rest_0", "br_rest_1", "tr_rest_0", "tr_rest_1",
    ),
    "q": ("aq_tq_0", "aq_tq_1", "ar_bq_0", "ar_bq_1"),
    "c": ("tc_0", "tc_1", "bc_0", "bc_1"),
    "s": ("z",),
}
D_Q = ("ar_tr_0", "ar_tr_1", "tr_rest_0", "tr_rest_1", "f")
A_Q = ("aq_tq_0", "aq_tq_1", "aq_br_0", "aq_br_1")
H_PACKET = ("aq_br_0", "aq_br_1")
B_Q = ("ar_bq_0", "ar_bq_1")
POOL = (
    "br_rest_0", "br_rest_1", "ar_bq_0", "ar_bq_1",
    "tc_0", "tc_1", "bc_0", "bc_1", "z",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(values, agent, goods):
    return sum((values[agent][good] for good in goods), Fraction(0))


def tail(values, agent, goods):
    if not goods:
        return Fraction(0)
    return value(values, agent, goods) - min(values[agent][good] for good in goods)


def desired_subsets(values, base, source, offered):
    desired = []
    for size in range(1, len(offered) + 1):
        for subset in itertools.combinations(offered, size):
            if value(values, source, subset) <= base[source]:
                continue
            if all(tail(values, observer, subset) <= base[observer] for observer in AGENTS):
                desired.append(frozenset(subset))
    return [
        subset for subset in desired
        if not any(other < subset for other in desired)
    ]


def run(root: Path, profile_path: Path) -> dict:
    profile = json.loads(profile_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in profile["values"].items()
    }
    base = {agent: value(values, agent, BASE[agent]) for agent in AGENTS}

    candidates = []
    for mask in range(1 << len(POOL)):
        low = tuple(POOL[index] for index in range(len(POOL)) if mask & (1 << index))
        high = tuple(good for good in POOL if good not in low)
        if value(values, "r", high) < base["r"]:
            continue
        if value(values, "r", high) < value(values, "r", low):
            continue
        candidates.append((value(values, "s", low), low, high))
    best_value = max(candidate[0] for candidate in candidates)
    low, high = min(
        (candidate[1], candidate[2])
        for candidate in candidates if candidate[0] == best_value
    )
    allocation = {"r": high, "q": D_Q, "c": A_Q, "s": low}

    walls = []
    for observer in AGENTS:
        for target in AGENTS:
            if value(values, observer, allocation[observer]) < tail(
                values, observer, allocation[target]
            ):
                walls.append([observer, target])

    responses = {}
    witnesses = {}
    for target in AGENTS:
        responses[target] = []
        for source in AGENTS:
            subsets = desired_subsets(values, base, source, allocation[target])
            if subsets:
                responses[target].append(source)
                witnesses[(source, target)] = min(
                    subsets, key=lambda subset: (len(subset), sorted(subset))
                )

    matchings = []
    for sources in itertools.permutations(AGENTS):
        if all(sources[index] in responses[target] for index, target in enumerate(AGENTS)):
            matchings.append(dict(zip(AGENTS, sources)))

    old_owner = {good: owner for owner, goods in BASE.items() for good in goods}
    old_owner["f"] = "_"
    new_owner = {good: owner for owner, goods in allocation.items() for good in goods}
    incoming = {
        target: sorted(good for good in allocation[target] if old_owner[good] != target)
        for target in AGENTS
    }
    released = {
        owner: sorted(good for good in BASE[owner] if new_owner.get(good) != owner)
        for owner in AGENTS
    }
    incoming_goods = [good for packet in incoming.values() for good in packet]
    supplied = {"f"}.union(good for packet in released.values() for good in packet)

    strict_separated = all(
        values["q"][bottom] > values["q"][captured]
        for bottom in B_Q for captured in H_PACKET
    )
    selected_utilities = {
        agent: str(value(values, agent, allocation[agent])) for agent in AGENTS
    }
    base_utilities = {agent: str(base[agent]) for agent in AGENTS}

    script = Path(__file__).resolve()
    return {
        "schema": "dual-anchor-strict-separated-profile-audit-v1",
        "status": "PI_RESPONSE_MATCHING" if matchings else "NO_INTERNAL_SDR",
        "strict_separated_q_order": strict_separated,
        "root_pool_value": str(value(values, "r", POOL)),
        "root_base_value": str(base["r"]),
        "root_payable": value(values, "r", POOL) >= base["r"],
        "maximizing_partition": {"r": list(high), "s": list(low)},
        "allocation": {agent: list(goods) for agent, goods in allocation.items()},
        "base_utilities": base_utilities,
        "selected_utilities": selected_utilities,
        "all_intended_owners_strictly_improve": all(
            value(values, agent, allocation[agent]) > base[agent] for agent in AGENTS
        ),
        "efx_walls": walls,
        "response_sources": responses,
        "internal_matchings": matchings,
        "selected_matching_witnesses": {
            f"{source}->{target}": sorted(witnesses[(source, target)])
            for target, source in matchings[0].items()
        } if matchings else {},
        "incoming_packets": incoming,
        "released_packets": released,
        "incoming_disjoint": len(incoming_goods) == len(set(incoming_goods)),
        "all_incoming_supplied": set(incoming_goods) <= supplied,
        "claim_boundary": (
            "exact Fraction replay on one bounded strict-separated full-capture "
            "profile; the dual selector closes this adversary by a release-supported "
            "response matching, not by an EFX endpoint, and this is not a cap-free closure"
        ),
        "provenance": {
            "profile": str(profile_path.relative_to(root)),
            "profile_sha256": sha256(profile_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root, args.profile.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "strict_separated": result["strict_separated_q_order"],
        "walls": result["efx_walls"],
        "matchings": len(result["internal_matchings"]),
    }, indent=2))


if __name__ == "__main__":
    main()
