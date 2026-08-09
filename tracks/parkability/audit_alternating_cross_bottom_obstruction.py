#!/usr/bin/env python3
"""Replay the exact alternating cross-bottom obstruction census."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


SCHEMA = "alternating-cross-bottom-obstruction-audit-v1"
AGENTS = ("p", "r", "s", "q")
GOODS = ("tr", "br", "tq", "bq", "x", "y", "f")
VALUES = (
    (5002, 1008, 4004, 1016, 10064, 1032, 6001),
    (9001, 1064, 1004, 1008, 1016, 11032, 1002),
    (4004, 1008, 5002, 1016, 1032, 10064, 6001),
    (1004, 1008, 9001, 1064, 11032, 1016, 1002),
)
BASE_OWNER = (1, 1, 3, 3, 0, 2, None)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundles(owner: tuple[int | None, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(4)
    )


def value(agent: int, goods: tuple[int, ...]) -> int:
    return sum(VALUES[agent][good] for good in goods)


def utilities(owner: tuple[int | None, ...]) -> tuple[int, ...]:
    return tuple(value(agent, bundle) for agent, bundle in enumerate(bundles(owner)))


def is_efx(owner: tuple[int | None, ...]) -> bool:
    assigned = bundles(owner)
    own = tuple(value(agent, assigned[agent]) for agent in range(4))
    return all(
        own[observer]
        >= value(observer, tuple(g for g in assigned[target] if g != removed))
        for observer in range(4)
        for target in range(4)
        for removed in assigned[target]
    )


def is_safe(candidate: tuple[int, ...], base_utility: tuple[int, ...]) -> bool:
    return all(
        value(observer, tuple(g for g in candidate if g != removed))
        <= base_utility[observer]
        for observer in range(4)
        for removed in candidate
    )


def desired_sets(
    observer: int,
    target: int,
    base_bundles: tuple[tuple[int, ...], ...],
    base_utility: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    offer = base_bundles[target] + (6,)
    return tuple(
        candidate
        for size in range(1, len(offer) + 1)
        for candidate in itertools.combinations(offer, size)
        if value(observer, candidate) > base_utility[observer]
        and is_safe(candidate, base_utility)
    )


def named_owner(owner: tuple[int | None, ...]) -> list[str | None]:
    return [None if assigned is None else AGENTS[assigned] for assigned in owner]


def named_goods(indices: tuple[int, ...]) -> list[str]:
    return [GOODS[index] for index in indices]


def audit() -> dict:
    base_bundles = bundles(BASE_OWNER)
    base_utility = utilities(BASE_OWNER)
    if not is_efx(BASE_OWNER):
        raise AssertionError("documented base allocation is not EFX")
    if not all(base_utility[agent] > VALUES[agent][6] for agent in range(4)):
        raise AssertionError("an owner does not strictly prefer its bundle to charity")

    envy_edges = tuple(
        (observer, target)
        for observer in range(4)
        for target in range(4)
        if observer != target
        and value(observer, base_bundles[target]) > base_utility[observer]
    )
    champions = {
        (observer, target): desired_sets(
            observer, target, base_bundles, base_utility
        )
        for observer in range(4)
        for target in range(4)
    }
    champions = {edge: sets for edge, sets in champions.items() if sets}

    subset_nondegenerate = []
    for agent in range(4):
        sums = {
            sum(VALUES[agent][good] for good in range(7) if mask & (1 << good))
            for mask in range(1 << 7)
        }
        subset_nondegenerate.append(len(sums) == 1 << 7)

    efx_count = 0
    pareto_dominator_count = 0
    first_priority_escape: dict[int, dict] = {}
    for raw_owner in itertools.product(range(5), repeat=7):
        owner = tuple(None if assigned == 4 else assigned for assigned in raw_owner)
        if not is_efx(owner):
            continue
        efx_count += 1
        candidate_utility = utilities(owner)
        if all(
            candidate_utility[agent] >= base_utility[agent] for agent in range(4)
        ) and any(
            candidate_utility[agent] > base_utility[agent] for agent in range(4)
        ):
            pareto_dominator_count += 1
        for agent in range(4):
            if (
                agent not in first_priority_escape
                and candidate_utility[agent] > base_utility[agent]
            ):
                first_priority_escape[agent] = {
                    "owner_by_good": named_owner(owner),
                    "utilities": list(candidate_utility),
                    "gain": candidate_utility[agent] - base_utility[agent],
                }

    expected_envy = ((1, 2), (3, 0))
    expected_champions = {
        (0, 1): ((0, 6),),
        (1, 2): ((5,),),
        (2, 3): ((2, 6),),
        (3, 0): ((4,),),
    }
    if envy_edges != expected_envy:
        raise AssertionError(("envy graph", envy_edges))
    if champions != expected_champions:
        raise AssertionError(("champion graph", champions))
    if subset_nondegenerate != [True] * 4:
        raise AssertionError("subset nondegeneracy failed")
    if efx_count != 2263:
        raise AssertionError(("EFX census", efx_count))
    if pareto_dominator_count != 0:
        raise AssertionError(("Pareto dominators", pareto_dominator_count))
    if len(first_priority_escape) != 4:
        raise AssertionError("not every first-priority agent has an escape")

    largest_offers = (
        (1, 3, (2, 3, 1)),
        (2, 3, (2, 3, 1)),
        (3, 1, (0, 1, 3)),
        (0, 1, (0, 1, 3)),
    )
    offer_audit = []
    for source, target, offer in largest_offers:
        offered_value = value(source, offer)
        if offered_value >= base_utility[source]:
            raise AssertionError(("compatible family not blocked", source, target))
        offer_audit.append(
            {
                "source": AGENTS[source],
                "target": AGENTS[target],
                "largest_offer": named_goods(offer),
                "source_value": offered_value,
                "own_value": base_utility[source],
                "margin": base_utility[source] - offered_value,
            }
        )

    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "PASSED",
        "claim_boundary": {
            "proved": "the displayed base is EFX-Pareto-maximal and blocks all four compatible local cross-bottom families",
            "not_proved": "global lexicographic maximality or failure of the priority-sensitive escape lemma",
        },
        "profile": {
            "agents": list(AGENTS),
            "goods": list(GOODS),
            "values": [list(row) for row in VALUES],
            "base_owner_by_good": named_owner(BASE_OWNER),
            "base_utilities": list(base_utility),
        },
        "structural_checks": {
            "base_efx": True,
            "strict_charity_dominance": True,
            "subset_nondegenerate_by_agent": subset_nondegenerate,
            "envy_edges": [[AGENTS[a], AGENTS[b]] for a, b in envy_edges],
            "basic_f_champions": [
                {
                    "source": AGENTS[source],
                    "target": AGENTS[target],
                    "desired_sets": [named_goods(goods) for goods in sets],
                }
                for (source, target), sets in champions.items()
            ],
            "compatible_family_largest_offer_checks": offer_audit,
        },
        "exhaustive_census": {
            "assignment_count": 5**7,
            "efx_assignment_count": efx_count,
            "pareto_dominating_efx_count": pareto_dominator_count,
            "first_priority_escapes": {
                AGENTS[agent]: first_priority_escape[agent] for agent in range(4)
            },
        },
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload)


if __name__ == "__main__":
    main()
