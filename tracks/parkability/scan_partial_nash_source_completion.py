#!/usr/bin/env python3
"""Scan maximum-Nash states for direct source-substitution completion."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .fast_count import FastParkability
    from .scan_partial_nash_potential import matrices
except ImportError:
    import core
    from anneal import atomic_json
    from fast_count import FastParkability
    from scan_partial_nash_potential import matrices


SCHEMA = "partial-nash-source-completion-corpus-scan-v1"


def decode_owner(n: int, m: int, floater: int, base_index: int):
    allocated = tuple(good for good in range(m) if good != floater)
    owner: list[int | None] = [None] * m
    for position, good in enumerate(allocated):
        owner[good] = (base_index // (n**position)) % n
    return tuple(owner)


def bundles_from_owner(owner, n: int):
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(n)
    )


def value(values, observer: int, bundle) -> int:
    return sum(values[observer][good] for good in bundle)


def source_hosts(values, owner) -> tuple[int, ...]:
    bundles = bundles_from_owner(owner, len(values))
    utilities = tuple(
        value(values, agent, bundles[agent]) for agent in range(len(values))
    )
    return tuple(
        host
        for host in range(len(values))
        if all(
            utilities[observer] >= value(values, observer, bundles[host])
            for observer in range(len(values))
            if observer != host
        )
    )


def owner_from_rematching(bundles, permutation, floater: int, m: int):
    owner: list[int | None] = [None] * m
    for agent, bundle_index in enumerate(permutation):
        for good in bundles[bundle_index]:
            if owner[good] is not None:
                raise AssertionError("rematched bundles overlap")
            owner[good] = agent
    if owner[floater] is not None or any(
        assigned is None for good, assigned in enumerate(owner) if good != floater
    ):
        raise AssertionError("rematching does not define a one-floater state")
    return tuple(owner)


def source_completion_landscape(values, floater: int, owner) -> dict:
    n = len(values)
    m = len(values[0])
    bundles = bundles_from_owner(owner, n)
    sources = source_hosts(values, owner)
    row_totals = tuple(map(sum, values))
    generated = 0
    states = {}
    for source in sources:
        for removed in bundles[source]:
            modified = list(bundles)
            modified[source] = tuple(
                good for good in bundles[source] if good != removed
            ) + (floater,)
            for permutation in itertools.permutations(range(n)):
                generated += 1
                successor_owner = owner_from_rematching(
                    modified,
                    permutation,
                    removed,
                    m,
                )
                identity = (removed, successor_owner)
                if identity in states:
                    states[identity]["origins"].append(
                        {
                            "source_host": source,
                            "removed_good": removed,
                            "permutation": list(permutation),
                        }
                    )
                    continue
                base = core.classify_base(values, removed, successor_owner)
                floater_slacks = [
                    base["own_values"][agent] - values[agent][removed]
                    for agent in range(n)
                ]
                eligible = (
                    base["base_min_efx_slack"] >= 0
                    and min(floater_slacks) >= 0
                )
                host_margins = [
                    min(
                        base["parking_slack_matrix"][observer][host]
                        / row_totals[observer]
                        for observer in range(n)
                        if observer != host
                    )
                    for host in range(n)
                ]
                states[identity] = {
                    "floater": removed,
                    "base_owner": list(successor_owner),
                    "utilities": base["own_values"],
                    "utility_product": math.prod(base["own_values"]),
                    "base_min_efx_slack": base["base_min_efx_slack"],
                    "floater_nonenvy_slacks": floater_slacks,
                    "eligible": eligible,
                    "best_host_normalized_margin": (
                        max(host_margins) if eligible else None
                    ),
                    "insertable_hosts": (
                        base["parkable_hosts"] if eligible else []
                    ),
                    "origins": [
                        {
                            "source_host": source,
                            "removed_good": removed,
                            "permutation": list(permutation),
                        }
                    ],
                }
    eligible = [state for state in states.values() if state["eligible"]]
    insertable = [state for state in eligible if state["insertable_hosts"]]
    ordered_insertable = sorted(
        insertable,
        key=lambda state: (
            -state["utility_product"],
            state["floater"],
            repr(state["base_owner"]),
        ),
    )
    ordered_eligible = sorted(
        eligible,
        key=lambda state: (
            -state["best_host_normalized_margin"],
            -state["utility_product"],
            state["floater"],
            repr(state["base_owner"]),
        ),
    )
    return {
        "source_hosts": list(sources),
        "generated_rematching_count": generated,
        "distinct_rematched_state_count": len(states),
        "eligible_rematched_state_count": len(eligible),
        "insertable_eligible_rematched_state_count": len(insertable),
        "best_eligible_host_normalized_margin": (
            ordered_eligible[0]["best_host_normalized_margin"]
            if ordered_eligible
            else None
        ),
        "closest_eligible_target": (
            ordered_eligible[0] if ordered_eligible else None
        ),
        "best_insertable_target": (
            ordered_insertable[0] if ordered_insertable else None
        ),
    }


def audit_profile(values, evaluator: FastParkability) -> dict:
    n = len(values)
    m = len(values[0])
    landscape = evaluator.partial_linear_potential_landscape(
        values,
        potential="normalized_nash",
    )
    candidate_records = []
    for candidate in landscape["maximizers"]:
        owner = decode_owner(
            n,
            m,
            candidate["floater"],
            candidate["base_index"],
        )
        exact = core.classify_base(values, candidate["floater"], owner)
        if tuple(exact["own_values"]) != tuple(candidate["utilities"]):
            raise AssertionError("base-index decoding disagrees with core")
        if bool(exact["parkable_hosts"]) != candidate["insertable"]:
            raise AssertionError("vectorized and core insertability disagree")
        source_landscape = (
            None
            if candidate["insertable"]
            else source_completion_landscape(
                values,
                candidate["floater"],
                owner,
            )
        )
        candidate_records.append(
            {
                "floater": candidate["floater"],
                "base_owner": list(owner),
                "utilities": candidate["utilities"],
                "utility_product": math.prod(candidate["utilities"]),
                "directly_insertable": candidate["insertable"],
                "direct_insertable_hosts": exact["parkable_hosts"],
                "source_completion": source_landscape,
            }
        )
    completable = [
        record
        for record in candidate_records
        if record["directly_insertable"]
        or record["source_completion"][
            "insertable_eligible_rematched_state_count"
        ]
        > 0
    ]
    source_margins = [
        record["source_completion"]["best_eligible_host_normalized_margin"]
        for record in candidate_records
        if not record["directly_insertable"]
        and record["source_completion"][
            "best_eligible_host_normalized_margin"
        ]
        is not None
    ]
    return {
        "eligible_base_count": landscape["eligible_base_count"],
        "maximum_product": math.prod(landscape["maximizers"][0]["utilities"]),
        "maximum_product_state_count": len(candidate_records),
        "directly_insertable_maximum_count": sum(
            record["directly_insertable"] for record in candidate_records
        ),
        "direct_or_source_completable_maximum_count": len(completable),
        "best_source_completion_normalized_margin": (
            max(source_margins) if source_margins else None
        ),
        "selector_survives": bool(completable),
        "maximizers": candidate_records,
    }


def run(directory: Path, output: Path, max_goods: int) -> dict:
    evaluators = {}
    seen = set()
    records = []
    paths = sorted(directory.glob("*.json"))
    for position, path in enumerate(paths, 1):
        for value_key, values in matrices(path):
            n = len(values)
            m = len(values[0])
            if n != 4 or m > max_goods or m <= n or values in seen:
                continue
            seen.add(values)
            evaluator = evaluators.setdefault((n, m), FastParkability(n, m))
            audit = audit_profile(values, evaluator)
            records.append(
                {
                    "source": str(path),
                    "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "value_key": value_key,
                    "n": n,
                    "m": m,
                    "values_sha256": hashlib.sha256(
                        json.dumps(values, separators=(",", ":")).encode()
                    ).hexdigest(),
                    **audit,
                }
            )
        if position % 250 == 0:
            print(
                f"files={position}/{len(paths)} profiles={len(records)}",
                flush=True,
            )
    failures = [record for record in records if not record["selector_survives"]]
    blocked = [
        record
        for record in records
        if record["directly_insertable_maximum_count"] == 0
    ]
    result = {
        "schema": SCHEMA,
        "status": (
            "SOURCE_COMPLETION_COUNTEREXAMPLE_FOUND"
            if failures
            else "NO_COUNTEREXAMPLE_IN_CORPUS"
        ),
        "meaning": (
            "For every exact maximum-product eligible state, test direct "
            "insertion and, when blocked, every source-good substitution "
            "followed by every bundle permutation. Survival on this finite "
            "corpus is not a theorem."
        ),
        "directory": str(directory),
        "json_file_count": len(paths),
        "distinct_profile_count": len(records),
        "max_goods": max_goods,
        "blocked_maximum_profile_count": len(blocked),
        "selector_failure_profile_count": len(failures),
        "failures": failures,
        "blocked_maximum_profiles": blocked,
        "records": records,
        "candidate_statement": (
            "Some maximum-product eligible state is either directly "
            "insertable or has an eligible insertable state obtained by "
            "replacing one good in a source bundle with the floater and "
            "permuting the resulting bundles."
        ),
        "claim_boundary": (
            "This is a finite corpus scan of a proof selector. It neither "
            "proves complete additive EFX nor searches for an additive EFX "
            "counterexample."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path("results"))
    parser.add_argument("--max-goods", type=int, default=9)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.directory.is_dir() or args.max_goods < 1:
        parser.error("a valid directory and positive goods bound are required")
    run(args.directory, args.output, args.max_goods)


if __name__ == "__main__":
    main()
