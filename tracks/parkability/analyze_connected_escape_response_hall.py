#!/usr/bin/env python3
"""Check whether a frozen connected escape also closes a response-Hall PI set."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from .analyze_flexible_lex_radius3_hardness_gap import desired_subsets
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        RECIPIENTS,
        transfer_topology,
        value,
    )
    from .analyze_flexible_later_owner_escape_topologies import old_bundles
except ImportError:
    from analyze_flexible_lex_radius3_hardness_gap import desired_subsets
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        RECIPIENTS,
        transfer_topology,
        value,
    )
    from analyze_flexible_later_owner_escape_topologies import old_bundles


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(profile_path, escape_path):
    profile = json.loads(profile_path.read_text())
    escape = json.loads(escape_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in profile["values"].items()
    }
    old = old_bundles()
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    allocation = escape["allocation"]
    topology = transfer_topology(old, allocation)
    changed = tuple(
        agent for agent in AGENTS if set(allocation[agent]) != set(old[agent])
    )
    responses = {}
    for target in changed:
        responses[target] = {
            source: desired_subsets(
                values, base, source, tuple(allocation[target])
            )
            for source in AGENTS
        }
        responses[target] = {
            source: subsets for source, subsets in responses[target].items() if subsets
        }
    internal = {
        target: sorted(set(responses[target]).intersection(changed))
        for target in changed
    }
    matchings = []
    for sources in itertools.permutations(changed):
        if all(sources[index] in internal[target] for index, target in enumerate(changed)):
            matchings.append(dict(zip(changed, sources)))

    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    new_owner = {
        good: recipient
        for recipient in RECIPIENTS for good in allocation[recipient]
    }
    incoming = {
        target: sorted(
            good for good in allocation[target] if base_owner[good] != target
        )
        for target in changed
    }
    released = {
        source: sorted(
            good for good in old[source] if new_owner[good] != source
        )
        for source in changed
    }
    incoming_goods = [good for packet in incoming.values() for good in packet]
    supplied_goods = {"f"}.union(
        good for packet in released.values() for good in packet
    )
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "connected-escape-response-hall-v1",
        "status": "PI_RESPONSE_MATCHING" if matchings else "NO_INTERNAL_SDR",
        "changed_owners": list(changed),
        "topology": topology,
        "response_sources": responses,
        "internal_response_sources": internal,
        "internal_matchings": matchings,
        "incoming_packets": incoming,
        "released_packets": released,
        "incoming_disjoint": len(incoming_goods) == len(set(incoming_goods)),
        "all_incoming_supplied": set(incoming_goods) <= supplied_goods,
        "claim_boundary": (
            "exact response-source and release-support audit for one frozen "
            "connected escape; a matching proves this profile is not PI-free, "
            "while no matching would not exclude other generalized PI edge sets"
        ),
        "provenance": {
            "profile": str(profile_path.relative_to(root)),
            "profile_sha256": sha256(profile_path),
            "escape": str(escape_path.relative_to(root)),
            "escape_sha256": sha256(escape_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--escape", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.profile.resolve(), args.escape.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "internal_matchings": len(result["internal_matchings"]),
        "incoming_disjoint": result["incoming_disjoint"],
        "all_incoming_supplied": result["all_incoming_supplied"],
    }, indent=2))


if __name__ == "__main__":
    main()
