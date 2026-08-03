#!/usr/bin/env python3
"""Exactly scan the threshold/absorption selector at fixed charity size."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import random
from pathlib import Path

try:
    from .anneal import atomic_json
    from .scan_partial_nash_potential import matrices
except ImportError:
    from anneal import atomic_json
    from scan_partial_nash_potential import matrices


SCHEMA = "charity-threshold-absorption-scan-v1"


def parse_values(document, source: Path) -> tuple[tuple[int, ...], ...]:
    raw = document.get("values", document.get("candidate_values"))
    if raw is None:
        raise ValueError(f"{source} contains no values")
    values = tuple(tuple(int(entry) for entry in row) for row in raw)
    if (
        not values
        or any(len(row) != len(values[0]) for row in values)
        or any(entry <= 0 for row in values for entry in row)
    ):
        raise ValueError("values must be a positive rectangular matrix")
    return values


def load_profiles(path: Path) -> list[tuple[str, tuple[tuple[int, ...], ...]]]:
    document = json.loads(path.read_text())
    failures = document.get("direct_hall_failures")
    if failures is None:
        return [(str(path), parse_values(document, path))]
    profiles = []
    seen = set()
    for failure in failures:
        source = Path(failure["source"])
        candidates = matrices(source)
        for value_key, values in candidates:
            key = tuple(values)
            if key in seen:
                continue
            seen.add(key)
            profiles.append((f"{path}:{source}:{value_key}", values))
    return profiles


def tables(values):
    m = len(values[0])
    totals = []
    thresholds = []
    for row in values:
        row_totals = [0] * (1 << m)
        row_thresholds = [0] * (1 << m)
        for mask in range(1, 1 << m):
            goods = [row[good] for good in range(m) if mask & (1 << good)]
            row_totals[mask] = sum(goods)
            row_thresholds[mask] = row_totals[mask] - min(goods)
        totals.append(row_totals)
        thresholds.append(row_thresholds)
    return tuple(totals), tuple(thresholds)


def eligible(masks, charity, totals, thresholds):
    n = len(masks)
    return all(
        totals[agent][masks[agent]] >= totals[agent][charity]
        and all(
            totals[agent][masks[agent]] >= thresholds[agent][masks[target]]
            for target in range(n)
            if target != agent
        )
        for agent in range(n)
    )


def theta(masks, totals, thresholds, row_totals):
    return sum(
        Fraction(thresholds[owner][masks[owner]], row_totals[owner])
        for owner in range(len(masks))
    )


def absorption_margin(masks, charity, totals, thresholds, row_totals):
    n = len(masks)
    best = None
    witness = None
    for good in range(charity.bit_length()):
        if not charity & (1 << good):
            continue
        remainder = charity & ~(1 << good)
        for host in range(n):
            complete = list(masks)
            complete[host] |= 1 << good
            for permutation in itertools.permutations(range(n)):
                margin = min(
                    Fraction(
                        totals[agent][complete[permutation[agent]]]
                        - max(
                            totals[agent][remainder],
                            max(
                                thresholds[agent][complete[target]]
                                for target in range(n)
                                if target != permutation[agent]
                            ),
                        ),
                        row_totals[agent],
                    )
                    for agent in range(n)
                )
                if best is None or margin > best:
                    best = margin
                    witness = {
                        "good": good,
                        "host": host,
                        "permutation": list(permutation),
                    }
    if best is None or witness is None:
        raise AssertionError("nonempty charity has no absorption candidate")
    return best, witness


def theta_maximizers(values, charity_size):
    n = len(values)
    m = len(values[0])
    if not 0 < charity_size <= m - n:
        raise ValueError("charity size must leave at least one good per agent")
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    best_theta = None
    maximizers = []
    eligible_count = 0
    goods = range(m)
    for charity_goods in itertools.combinations(goods, charity_size):
        charity = sum(1 << good for good in charity_goods)
        allocated = [good for good in goods if not charity & (1 << good)]
        for owners in itertools.product(range(n), repeat=len(allocated)):
            masks = [0] * n
            for good, owner in zip(allocated, owners):
                masks[owner] |= 1 << good
            if any(mask == 0 for mask in masks):
                continue
            masks = tuple(masks)
            if not eligible(masks, charity, totals, thresholds):
                continue
            eligible_count += 1
            score = theta(masks, totals, thresholds, row_totals)
            if best_theta is None or score > best_theta:
                best_theta = score
                maximizers = [(masks, charity)]
            elif score == best_theta:
                maximizers.append((masks, charity))

    return {
        "totals": totals,
        "thresholds": thresholds,
        "row_totals": row_totals,
        "eligible_state_count": eligible_count,
        "best_theta": best_theta,
        "maximizers": maximizers,
    }


def scan_profile(values, charity_size):
    landscape = theta_maximizers(values, charity_size)
    best_theta = landscape["best_theta"]
    if best_theta is None:
        return {"status": "NO_EFX_WITH_CHARITY_STATE", "eligible_state_count": 0}
    totals = landscape["totals"]
    thresholds = landscape["thresholds"]
    row_totals = landscape["row_totals"]
    maximizers = landscape["maximizers"]

    best_margin = None
    best_record = None
    insertable_maximizers = 0
    for masks, charity in maximizers:
        margin, witness = absorption_margin(
            masks, charity, totals, thresholds, row_totals
        )
        insertable_maximizers += margin >= 0
        if best_margin is None or margin > best_margin:
            best_margin = margin
            best_record = {
                "masks": list(masks),
                "charity_mask": charity,
                "absorption_witness": witness,
            }
    assert best_margin is not None and best_record is not None
    return {
        "status": (
            "SELECTOR_ABSORBS"
            if best_margin >= 0
            else "BLOCKED_SELECTOR_COUNTEREXAMPLE"
        ),
        "eligible_state_count": landscape["eligible_state_count"],
        "theta_maximizer_count": len(maximizers),
        "insertable_theta_maximizer_count": insertable_maximizers,
        "best_theta": str(best_theta),
        "best_absorption_margin": str(best_margin),
        **best_record,
    }


def random_values(n, m, cap, rng):
    return tuple(tuple(rng.randint(1, cap) for _ in range(m)) for _ in range(n))


def run(paths, random_profiles, n, m, cap, charity_size, seed, output):
    if output.exists() or random_profiles < 0 or cap < 1:
        raise ValueError("a new output and valid random parameters are required")
    rng = random.Random(seed)
    profiles = [profile for path in paths for profile in load_profiles(path)] + [
        (f"random:{seed}:{index}", random_values(n, m, cap, rng))
        for index in range(random_profiles)
    ]
    if not profiles:
        raise ValueError("at least one source or random profile is required")
    records = []
    for source, values in profiles:
        result = scan_profile(values, charity_size)
        records.append(
            {
                "source": source,
                "values_sha256": hashlib.sha256(
                    json.dumps(values, separators=(",", ":")).encode()
                ).hexdigest(),
                "values": [list(row) for row in values],
                **result,
            }
        )
        print(f"{source}: {result['status']}", flush=True)
        if result["status"] == "BLOCKED_SELECTOR_COUNTEREXAMPLE":
            break
    status = (
        "BLOCKED_SELECTOR_COUNTEREXAMPLE_FOUND"
        if any(
            record["status"] == "BLOCKED_SELECTOR_COUNTEREXAMPLE"
            for record in records
        )
        else "SELECTOR_SURVIVES_SCANNED_PROFILES"
    )
    document = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "Exact enumeration of EFX-with-charity states, global normalized-"
            "threshold maximizers, and their best one-good Hall absorption margin."
        ),
        "charity_size": charity_size,
        "profile_count": len(records),
        "records": records,
        "claim_boundary": (
            "A counterexample refutes the extremal selector. Survival is finite "
            "evidence only and does not prove the absorption-gradient lemma."
        ),
    }
    atomic_json(output, document)
    return document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--values", type=Path, action="append", default=[])
    parser.add_argument("--random-profiles", type=int, default=0)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--m", type=int, default=6)
    parser.add_argument("--cap", type=int, default=5)
    parser.add_argument("--charity-size", type=int, required=True)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.values,
        args.random_profiles,
        args.n,
        args.m,
        args.cap,
        args.charity_size,
        args.seed,
        args.output,
    )
    print(json.dumps({key: result[key] for key in ("status", "profile_count")}, indent=2))


if __name__ == "__main__":
    main()
