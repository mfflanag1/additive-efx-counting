#!/usr/bin/env python3
"""Exact census of bundle cycles and source-substitution Nash rescues."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
except ImportError:
    import core
    import independent
    from anneal import atomic_json


SCHEMA = "partial-nash-substitution-census-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(values, observer: int, bundle) -> int:
    return sum(values[observer][good] for good in bundle)


def product(items) -> int:
    result = 1
    for item in items:
        result *= item
    return result


def directed_cycles(n: int):
    return tuple(
        cycle
        for length in range(2, n + 1)
        for cycle in itertools.permutations(range(n), length)
        if cycle[0] == min(cycle)
    )


def has_strict_bundle_cycle(values, bundles, utilities, cycles) -> bool:
    edges = {
        (observer, target)
        for observer in range(len(values))
        for target in range(len(values))
        if observer != target
        and value(values, observer, bundles[target]) > utilities[observer]
    }
    return any(
        all(
            (cycle[index], cycle[(index + 1) % len(cycle)]) in edges
            for index in range(len(cycle))
        )
        for cycle in cycles
    )


def permutation_shape(permutation: tuple[int, ...]) -> str:
    seen = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return "".join(map(str, sorted(lengths, reverse=True)))


def owner_from_bundles(bundles, permutation, floater: int, m: int):
    owner: list[int | None] = [None] * m
    for agent, bundle_index in enumerate(permutation):
        for good in bundles[bundle_index]:
            if owner[good] is not None:
                raise AssertionError("rematched bundles overlap")
            owner[good] = agent
    if owner[floater] is not None or any(
        assigned is None for good, assigned in enumerate(owner) if good != floater
    ):
        raise AssertionError("rematching did not leave exactly the floater")
    return tuple(owner)


def best_source_substitution(values, floater: int, base: dict):
    n = len(values)
    m = len(values[0])
    bundles = tuple(tuple(bundle) for bundle in base["bundles"])
    old_utilities = tuple(base["own_values"])
    old_product = product(old_utilities)
    sources = tuple(
        host
        for host in range(n)
        if all(
            old_utilities[observer]
            >= value(values, observer, bundles[host])
            for observer in range(n)
            if observer != host
        )
    )
    best = None
    for host in sources:
        for removed in bundles[host]:
            modified = list(bundles)
            modified[host] = tuple(
                good for good in bundles[host] if good != removed
            ) + (floater,)
            for permutation in itertools.permutations(range(n)):
                owner = owner_from_bundles(
                    modified,
                    permutation,
                    removed,
                    m,
                )
                if not independent.is_removed_good_efx0(
                    values,
                    owner,
                    removed,
                ):
                    continue
                new_utilities = tuple(
                    value(
                        values,
                        agent,
                        tuple(
                            good
                            for good, assigned in enumerate(owner)
                            if assigned == agent
                        ),
                    )
                    for agent in range(n)
                )
                if any(
                    new_utilities[agent] < values[agent][removed]
                    for agent in range(n)
                ):
                    continue
                if product(new_utilities) <= old_product:
                    continue
                receiver = permutation.index(host)
                supporters = tuple(
                    agent
                    for agent in range(n)
                    if values[agent][floater] > values[agent][removed]
                )
                record = {
                    "owner_loss_count": sum(
                        new_utilities[agent] < old_utilities[agent]
                        for agent in range(n)
                    ),
                    "owner_gain_count": sum(
                        new_utilities[agent] > old_utilities[agent]
                        for agent in range(n)
                    ),
                    "permutation_shape": permutation_shape(permutation),
                    "supporter_count": len(supporters),
                    "receiver_is_supporter": receiver in supporters,
                }
                key = (
                    record["owner_loss_count"],
                    -record["owner_gain_count"],
                    record["permutation_shape"],
                    record["supporter_count"],
                    not record["receiver_is_supporter"],
                )
                if best is None or key < best[0]:
                    best = key, record
    return None if best is None else best[1]


def audit_profile(label: str, values) -> tuple[dict, Counter]:
    values = core.validate_values(values, expected_n=4, expected_m=9, lower=1)
    cycles = directed_cycles(4)
    counts = Counter()
    templates = Counter()
    for floater in range(9):
        for base in core.iter_efx_bases(values, floater):
            if not all(
                base["own_values"][agent] >= values[agent][floater]
                for agent in range(4)
            ):
                continue
            counts["eligible_state_count"] += 1
            if base["parkable_hosts"]:
                continue
            counts["all_host_blocked_state_count"] += 1
            bundles = tuple(tuple(bundle) for bundle in base["bundles"])
            utilities = tuple(base["own_values"])
            if has_strict_bundle_cycle(values, bundles, utilities, cycles):
                counts["strict_bundle_cycle_state_count"] += 1
                continue
            rescue = best_source_substitution(values, floater, base)
            if rescue is None:
                counts["residual_state_count"] += 1
                continue
            counts["source_substitution_rescue_state_count"] += 1
            counts["rescues_with_owner_loss_count"] += int(
                rescue["owner_loss_count"] > 0
            )
            templates[
                (
                    rescue["owner_loss_count"],
                    rescue["owner_gain_count"],
                    rescue["permutation_shape"],
                    rescue["supporter_count"],
                    rescue["receiver_is_supporter"],
                )
            ] += 1
    return {"label": label, **counts}, templates


def load_profiles(linear_path: Path, models_path: Path):
    linear = json.loads(linear_path.read_text())
    models = json.loads(models_path.read_text())
    profiles = [("linear_refutation", linear["values"])]
    profiles.extend(
        (f"initial_cegar_iteration_{record['iteration']}", record["values"])
        for record in models["models"]
    )
    return profiles


def run(linear_path: Path, models_path: Path, output: Path) -> dict:
    profile_records = []
    templates = Counter()
    for label, values in load_profiles(linear_path, models_path):
        print(f"auditing {label}", flush=True)
        record, observed_templates = audit_profile(label, values)
        profile_records.append(record)
        templates.update(observed_templates)
    totals = {
        key: sum(record.get(key, 0) for record in profile_records)
        for key in (
            "eligible_state_count",
            "all_host_blocked_state_count",
            "strict_bundle_cycle_state_count",
            "source_substitution_rescue_state_count",
            "rescues_with_owner_loss_count",
            "residual_state_count",
        )
    }
    if (
        totals["all_host_blocked_state_count"]
        != totals["strict_bundle_cycle_state_count"]
        + totals["source_substitution_rescue_state_count"]
        + totals["residual_state_count"]
    ):
        raise AssertionError("blocked-state trichotomy counts do not partition")
    result = {
        "schema": SCHEMA,
        "status": (
            "NO_RESIDUAL_IN_AUDITED_PROFILES"
            if totals["residual_state_count"] == 0
            else "RESIDUAL_STATE_FOUND"
        ),
        "meaning": (
            "Every audited all-host-blocked eligible state either had a "
            "strict bundle cycle or an eligible source substitution/rematching "
            "with strictly larger Nash welfare. This finite census is not a "
            "proof of the general trichotomy."
        ),
        "inputs": [
            {"path": str(linear_path), "sha256": sha256(linear_path)},
            {"path": str(models_path), "sha256": sha256(models_path)},
        ],
        "profiles": profile_records,
        "totals": totals,
        "rescue_templates": [
            {
                "count": count,
                "owner_loss_count": key[0],
                "owner_gain_count": key[1],
                "permutation_shape": key[2],
                "supporter_count": key[3],
                "receiver_is_supporter": key[4],
            }
            for key, count in sorted(
                templates.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ],
        "candidate_trichotomy": (
            "Every eligible all-host-blocked state has either a strict bundle "
            "preference cycle or a source-good substitution followed by an "
            "eligible bundle rematching with larger Nash welfare."
        ),
        "claim_boundary": (
            "The census covers six exact four-agent, nine-good profiles. It "
            "does not establish the candidate trichotomy for arbitrary values, "
            "bundle shapes, or numbers of goods."
        ),
    }
    atomic_json(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--linear",
        type=Path,
        default=Path("results/partial_linear_potential_refutation.json"),
    )
    parser.add_argument(
        "--models",
        type=Path,
        default=Path("results/partial_nash_initial_cegar_models.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.linear, args.models, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
