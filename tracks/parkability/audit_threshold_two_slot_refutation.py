#!/usr/bin/env python3
"""Audit a nondegenerate refutation of the one-block threshold-Hall target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


SCHEMA = "threshold-two-slot-refutation-audit-v1"
AGENTS = ("p", "r", "s", "q")
GOODS = (
    "tr0", "tr1", "br0", "br1",
    "tq0", "tq1", "bq0", "bq1",
    "x", "y", "f",
)
VALUES = (
    (16896, 376840, 16416, 3059840, 180240, 196610, 81984, 98308, 3486720, 3469313, 3109120),
    (4224, 140288, 4098, 49168, 25088, 28680, 61472, 65540, 192576, 2912257, 41216),
    (20544, 1425409, 672000, 2076674, 794656, 1343492, 41088, 713216, 4194320, 4215808, 2117640),
    (8704, 81984, 40962, 1601552, 155776, 1496064, 24577, 65568, 1749248, 1732616, 90116),
)
BASE_BUNDLES = ((8,), (0, 1, 2, 3), (9,), (4, 5, 6, 7))
FLOATER = 10
TOP_R = (0, 1)
BOTTOM_R = (2, 3)
TOP_Q = (4, 5)
BOTTOM_Q = (6, 7)
EXPECTED_ENVY = {(1, 2), (3, 0)}
EXPECTED_DESIRED = {
    (0, 1): TOP_R + (FLOATER,),
    (1, 2): (9,),
    (2, 3): TOP_Q + (FLOATER,),
    (3, 0): (8,),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(agent: int, goods: tuple[int, ...]) -> int:
    return sum(VALUES[agent][good] for good in goods)


def own_utilities() -> tuple[int, ...]:
    return tuple(value(agent, BASE_BUNDLES[agent]) for agent in range(4))


def safe(candidate: tuple[int, ...], thresholds: tuple[int, ...]) -> bool:
    return all(
        value(observer, tuple(good for good in candidate if good != removed))
        <= thresholds[observer]
        for observer in range(4)
        for removed in candidate
    )


def desired(
    source: int,
    offer: tuple[int, ...],
    own: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        candidate
        for size in range(1, len(offer) + 1)
        for candidate in itertools.combinations(offer, size)
        if value(source, candidate) > own[source] and safe(candidate, own)
    )


def audit() -> dict:
    own = own_utilities()
    if not all(entry > 0 for row in VALUES for entry in row):
        raise AssertionError("profile is not strictly positive")

    nondegenerate = []
    for agent in range(4):
        sums = {
            value(
                agent,
                tuple(good for good in range(11) if mask & (1 << good)),
            )
            for mask in range(1 << 11)
        }
        nondegenerate.append(len(sums) == 1 << 11)
    if nondegenerate != [True] * 4:
        raise AssertionError("profile is not subset-nondegenerate")

    if not all(own[agent] > VALUES[agent][FLOATER] for agent in range(4)):
        raise AssertionError("charity dominance failed")
    if not all(
        own[observer]
        > value(
            observer,
            tuple(good for good in BASE_BUNDLES[target] if good != removed),
        )
        for observer in range(4)
        for target in range(4)
        for removed in BASE_BUNDLES[target]
    ):
        raise AssertionError("strict base EFX failed")

    envy = {
        (observer, target)
        for observer in range(4)
        for target in range(4)
        if observer != target
        and value(observer, BASE_BUNDLES[target]) > own[observer]
    }
    if envy != EXPECTED_ENVY:
        raise AssertionError(("envy graph", envy))

    champion_records = []
    for source in range(4):
        for target in range(4):
            offer = BASE_BUNDLES[target] + (FLOATER,)
            found = desired(source, offer, own)
            expected = EXPECTED_DESIRED.get((source, target))
            if expected is None and found:
                raise AssertionError(("champion chord", source, target, found))
            if expected is not None:
                if expected not in found or offer in found:
                    raise AssertionError(("selected/full desired", source, target, found))
                champion_records.append(
                    {
                        "source": AGENTS[source],
                        "target": AGENTS[target],
                        "selected_desired": [GOODS[good] for good in expected],
                        "desired_set_count_on_edge": len(found),
                    }
                )

    compatible_families = (
        (1, 3, BOTTOM_R),
        (2, 3, BOTTOM_R),
        (3, 1, BOTTOM_Q),
        (0, 1, BOTTOM_Q),
    )
    compatible_offer_count = 0
    for source, target, incoming in compatible_families:
        target_bundle = BASE_BUNDLES[target]
        for incoming_size in range(len(incoming) + 1):
            for incoming_subset in itertools.combinations(incoming, incoming_size):
                for release_size in range(len(target_bundle) + 1):
                    for release in itertools.combinations(target_bundle, release_size):
                        offer = tuple(
                            good for good in target_bundle if good not in release
                        ) + incoming_subset
                        compatible_offer_count += 1
                        if desired(source, offer, own):
                            raise AssertionError(
                                ("compatible family", source, target, incoming_subset, release)
                            )

    fixed_p = TOP_R + (FLOATER,)
    fixed_q = (8,)
    residual = BOTTOM_R + BASE_BUNDLES[3]
    thresholds = (
        value(0, fixed_p),
        max(
            value(1, tuple(good for good in fixed_p if good != removed))
            for removed in fixed_p
        ),
        max(
            value(2, tuple(good for good in fixed_p if good != removed))
            for removed in fixed_p
        ),
        value(3, fixed_q),
    )
    threshold_safe_crossers = []
    residual_subset_count = 0
    for size in range(1, len(residual) + 1):
        for candidate in itertools.combinations(residual, size):
            residual_subset_count += 1
            crosses = (
                value(1, candidate) > thresholds[1]
                or value(2, candidate) > thresholds[2]
            )
            if crosses and safe(candidate, thresholds):
                threshold_safe_crossers.append(candidate)
    if threshold_safe_crossers:
        raise AssertionError(("threshold-safe residual crosser", threshold_safe_crossers))

    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "NONDEGENERATE_TWO_SLOT_THRESHOLD_TARGET_REFUTED",
        "claim_boundary": {
            "refuted": "after fixing p's selected top-plus-f block and q's singleton x, the residual pool must contain one whole threshold-safe block crossing r's or s's terminal threshold",
            "not_refuted": "sequential threshold extraction, subpacket splitting, the full priority-sensitive alternating escape, or complete EFX",
        },
        "agents": list(AGENTS),
        "goods": list(GOODS),
        "values": [list(row) for row in VALUES],
        "base_bundles": [[GOODS[good] for good in bundle] for bundle in BASE_BUNDLES],
        "own_utilities": list(own),
        "subset_nondegenerate_by_agent": nondegenerate,
        "envy_edges": [[AGENTS[source], AGENTS[target]] for source, target in sorted(envy)],
        "champion_edges": champion_records,
        "compatible_family_offer_count": compatible_offer_count,
        "compatible_family_edge_count": 0,
        "threshold_test": {
            "priority_order": ["p", "q", "r", "s"],
            "fixed_p_bundle": [GOODS[good] for good in fixed_p],
            "fixed_q_bundle": [GOODS[good] for good in fixed_q],
            "residual_pool": [GOODS[good] for good in residual],
            "thresholds": list(thresholds),
            "residual_subset_count": residual_subset_count,
            "threshold_safe_crossing_subset_count": 0,
        },
        "construction": {
            "method": "binary perturbation of a rational QF_LRA model",
            "multiplier": 4096,
            "random_seed": 20260809,
            "accepted_iteration": 410,
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
