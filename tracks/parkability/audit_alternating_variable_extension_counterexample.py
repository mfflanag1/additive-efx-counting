#!/usr/bin/env python3
"""Independently audit a variable-packet strict-extension counterexample."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


N = 4
CHARITY = 4
ORDER = (0, 2, 3, 1)


def packets(sizes: tuple[int, int, int, int]):
    result = []
    start = 0
    for size in sizes:
        result.append(tuple(range(start, start + size)))
        start += size
    x, y, floater = start, start + 1, start + 2
    tr, br, tq, bq = result
    base = ((x,), tr + br, (y,), tq + bq)
    return tuple(result), x, y, floater, base


def good_names(sizes: tuple[int, int, int, int]):
    names = []
    for label, size in zip(("tr", "br", "tq", "bq"), sizes):
        names.extend([label] if size == 1 else [f"{label}{index}" for index in range(size)])
    return tuple(names + ["x", "y", "f"])


def bundles(owner):
    return tuple(
        tuple(good for good, target in enumerate(owner) if target == agent)
        for agent in range(N)
    )


def utility(values, observer, bundle):
    return sum(values[observer][good] for good in bundle)


def desired(values, base_utility, source, candidate):
    return utility(values, source, candidate) > base_utility[source] and all(
        utility(values, observer, tuple(g for g in candidate if g != removed))
        <= base_utility[observer]
        for observer in range(N)
        for removed in candidate
    )


def efx(values, owner):
    assigned = bundles(owner)
    own = tuple(utility(values, agent, assigned[agent]) for agent in range(N))
    return all(
        own[observer]
        >= utility(values, observer, tuple(g for g in assigned[target] if g != removed))
        for observer in range(N)
        for target in range(N)
        for removed in assigned[target]
    )


def lex_improves(values, owner, base_utility):
    assigned = bundles(owner)
    candidate = tuple(utility(values, agent, assigned[agent]) for agent in range(N))
    return tuple(candidate[agent] for agent in ORDER) > tuple(
        base_utility[agent] for agent in ORDER
    )


def structural_checks(values, sizes):
    packet, x, y, floater, base = packets(sizes)
    tr, br, tq, bq = packet
    base_utility = tuple(utility(values, agent, base[agent]) for agent in range(N))
    checks = {}
    checks["positive_values"] = all(entry > 0 for row in values for entry in row)
    checks["normalized_rows_not_required_after_integerization"] = True
    checks["p_packet_sort"] = all(
        values[0][left] < values[0][right]
        for group in packet
        for left, right in zip(group, group[1:])
    )
    checks["charity_below_own"] = all(
        base_utility[agent] > values[agent][floater] for agent in range(N)
    )
    expected_envy = {(1, 2), (3, 0)}
    checks["exact_alternating_envy_edges"] = all(
        (
            utility(values, observer, base[target]) > base_utility[observer]
            if (observer, target) in expected_envy
            else base_utility[observer] > utility(values, observer, base[target])
        )
        for observer in range(N)
        for target in range(N)
        if observer != target
    )
    checks["strict_base_efx"] = all(
        base_utility[observer]
        > utility(values, observer, tuple(g for g in base[target] if g != removed))
        for observer in range(N)
        for target in range(N)
        for removed in base[target]
    )
    expected_desired = {
        (0, 1): tr + (floater,),
        (1, 2): (y,),
        (2, 3): tq + (floater,),
        (3, 0): (x,),
    }
    champion_ok = True
    for source in range(N):
        for target in range(N):
            offer = base[target] + (floater,)
            expected = expected_desired.get((source, target))
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    if candidate == expected:
                        champion_ok &= desired(values, base_utility, source, candidate)
                    elif expected is None or candidate == offer:
                        champion_ok &= not desired(values, base_utility, source, candidate)
    checks["champion_cycle_relations"] = champion_ok
    compatible = ((1, 3, br), (2, 3, br), (3, 1, bq), (0, 1, bq))
    compatible_absent = True
    for source, target, incoming in compatible:
        for incoming_size in range(len(incoming) + 1):
            for incoming_subset in itertools.combinations(incoming, incoming_size):
                for release_size in range(len(base[target]) + 1):
                    for release in itertools.combinations(base[target], release_size):
                        offer = tuple(g for g in base[target] if g not in release) + incoming_subset
                        for size in range(1, len(offer) + 1):
                            for candidate in itertools.combinations(offer, size):
                                compatible_absent &= not desired(
                                    values, base_utility, source, candidate
                                )
    checks["four_compatible_families_absent"] = compatible_absent
    return checks, base_utility, (packet, x, y, floater, base)


def audit(payload):
    sizes = tuple(payload["packet_sizes"])
    values = tuple(tuple(row) for row in payload["values"])
    checks, base_utility, geometry = structural_checks(values, sizes)
    packet, x, _y, floater, base = geometry
    tr, br, _tq, _bq = packet
    offer = tr + br + (floater,)
    counts = {"efx_lex": 0, "anchored": 0, "promoted_original_offer": 0, "outside": 0}
    outside = []
    anchored_examples = []
    promoted_examples = []
    for owner in itertools.product(range(N + 1), repeat=len(values[0])):
        normalized = tuple(None if target == CHARITY else target for target in owner)
        if not efx(values, normalized) or not lex_improves(values, normalized, base_utility):
            continue
        counts["efx_lex"] += 1
        assigned = bundles(normalized)
        if assigned[0] == (x,):
            counts["anchored"] += 1
            anchored_examples.append(normalized)
        elif set(assigned[0]).issubset(offer) and desired(
            values, base_utility, 0, assigned[0]
        ):
            counts["promoted_original_offer"] += 1
            promoted_examples.append(normalized)
        else:
            counts["outside"] += 1
            changes = sum(
                normalized[good]
                != next((agent for agent, bundle in enumerate(base) if good in bundle), None)
                for good in range(len(normalized))
            )
            outside.append((changes, normalized))
    outside.sort(key=lambda record: (record[0], str(record[1])))
    smallest = None
    if outside:
        owner = outside[0][1]
        assigned = bundles(owner)
        names = good_names(sizes)
        minimum_changes = outside[0][0]
        smallest = {
            "operation": "cross-face desired-root promotion",
            "changed_good_count": minimum_changes,
            "minimum_change_allocation_count": sum(
                changes == minimum_changes for changes, _owner in outside
            ),
            "owner": list(owner),
            "bundles": [list(bundle) for bundle in assigned],
            "named_bundles": [
                [names[good] for good in bundle] for bundle in assigned
            ],
            "root_bundle_desired_at_base": desired(values, base_utility, 0, assigned[0]),
            "root_bundle_within_original_offer": set(assigned[0]).issubset(offer),
            "root_keeps_x": x in assigned[0],
            "utilities": [utility(values, agent, assigned[agent]) for agent in range(N)],
        }
    return {
        "schema": "alternating-variable-extension-counterexample-audit-v1",
        "status": (
            "EXACT_STRICT_BRIDGE_COUNTEREXAMPLE"
            if all(checks.values())
            and counts["anchored"] == 0
            and counts["promoted_original_offer"] == 0
            and counts["outside"] > 0
            else "AUDIT_FAILED"
        ),
        "packet_sizes": list(sizes),
        "agent_order": list(ORDER),
        "structural_checks": checks,
        "base_utilities": list(base_utility),
        "allocation_counts": counts,
        "allocations_exhausted": (N + 1) ** len(values[0]),
        "smallest_missing_operation": smallest,
        "claim_boundary": (
            "Refutes only the anchored-or-desired-subset-of-original-r-offer bridge. "
            "An outside EFX lexicographic improvement may still exist and does not refute EFX."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raw = args.profile.read_bytes()
    payload = json.loads(raw)
    result = audit(payload)
    result["profile_sha256"] = hashlib.sha256(raw).hexdigest()
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
