#!/usr/bin/env python3
"""Constructive audit of witness-partition realizability for named roles.

For a named role `g` the totals/minima abstraction records, per observer `i`,
the role total `T[i,g]` and the least physical-good value `M[i,g]`.  The
identity-aware enrichment additionally records which physical good realizes
each observer's minimum.  Formally a *witness selection* is a map
`w : observers -> g` with `w(i)` a minimizer of `v_i` on `g`; its *coincidence
partition* is `ker(w)`, an element of the fifteen set partitions of the four
observers.  A role *admits* a partition when some witness selection induces it.

This audit builds, for every role of a banked totals/minima profile and every
one of the fifteen partitions, an explicit positive-rational physical role and
checks by direct computation that its totals and minima reproduce the profile
and that its witness selection induces the requested partition.  When the
construction is refused it records the observer and the exact inequality that
blocks it.  Nothing here imports a solver: the realizations are closed-form.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

OBSERVERS = ("r", "q", "d", "s")


def set_partitions(elements):
    """Every set partition of `elements`, each as a sorted tuple of blocks."""
    elements = tuple(elements)
    if not elements:
        yield ()
        return
    head, rest = elements[0], elements[1:]
    for smaller in set_partitions(rest):
        for index in range(len(smaller)):
            yield tuple(
                sorted(
                    smaller[:index]
                    + (tuple(sorted(smaller[index] + (head,))),)
                    + smaller[index + 1:]
                )
            )
        yield tuple(sorted(smaller + ((head,),)))


def partition_name(partition):
    return "|".join("".join(block) for block in partition)


def load_profile(path):
    raw = json.loads(path.read_text())
    totals = {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in raw["countermodel_totals"].items()
    }
    minima = {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in raw["countermodel_minima"].items()
    }
    return raw, totals, minima


def slack_ratio(totals, minima, role):
    """min_i floor(T[i,role] / M[i,role]); the role-local block-count budget."""
    return min(totals[o][role] // minima[o][role] for o in OBSERVERS)


def realize(totals, minima, role, partition):
    """Explicit physical role admitting `partition`, or the blocking observer.

    Block `j` receives a distinct physical good `x_j`.  Observer `i` in block
    `j` values `x_j` at `M[i]` and spreads `T[i] - M[i]` evenly over the other
    blocks' goods, so every non-witness good is worth at least `M[i]` exactly
    when `T[i] >= b * M[i]`.  A one-block multi-good role instead uses the two
    goods `M[i]` and `T[i] - M[i]`.
    """
    blocks = tuple(partition)
    width = len(blocks)
    singleton_role = all(totals[o][role] == minima[o][role] for o in OBSERVERS)
    if singleton_role:
        if width > 1:
            blocked = OBSERVERS[0]
            return None, {
                "observer": blocked,
                "blocks": width,
                "total": str(totals[blocked][role]),
                "minimum": str(minima[blocked][role]),
                "reason": "singleton role carries one physical good",
            }
        return {"x0": {o: totals[o][role] for o in OBSERVERS}}, None

    for observer in OBSERVERS:
        if totals[observer][role] < width * minima[observer][role]:
            return None, {
                "observer": observer,
                "blocks": width,
                "total": str(totals[observer][role]),
                "minimum": str(minima[observer][role]),
                "reason": "total below block count times minimum",
            }

    if width == 1:
        values = {"x0": {}, "x1": {}}
        for observer in OBSERVERS:
            values["x0"][observer] = minima[observer][role]
            values["x1"][observer] = totals[observer][role] - minima[observer][role]
        return values, None

    goods = tuple(f"x{index}" for index in range(width))
    values = {good: {} for good in goods}
    for index, block in enumerate(blocks):
        for observer in block:
            spare = totals[observer][role] - width * minima[observer][role]
            share = spare / (width - 1)
            for other, good in enumerate(goods):
                values[good][observer] = (
                    minima[observer][role] if other == index
                    else minima[observer][role] + share
                )
    return values, None


def check_realization(values, totals, minima, role, partition):
    """Recompute totals, minima and the induced partition from the goods."""
    goods = tuple(values)
    induced = {}
    for observer in OBSERVERS:
        column = {good: values[good][observer] for good in goods}
        assert all(amount > 0 for amount in column.values()), (role, observer)
        assert sum(column.values()) == totals[observer][role], (role, observer)
        least = min(column.values())
        assert least == minima[observer][role], (role, observer)
        induced[observer] = tuple(
            sorted(good for good, amount in column.items() if amount == least)
        )
    target = tuple(sorted(tuple(sorted(block)) for block in partition))
    for choice in itertools.product(*(induced[o] for o in OBSERVERS)):
        kernel = {}
        for observer, good in zip(OBSERVERS, choice):
            kernel.setdefault(good, []).append(observer)
        shape = tuple(sorted(tuple(sorted(block)) for block in kernel.values()))
        if shape == target:
            return True
    return False


def audit_profile(path, partitions):
    raw, totals, minima = load_profile(path)
    roles = tuple(sorted(totals[OBSERVERS[0]]))
    rows = {}
    for role in roles:
        budget = slack_ratio(totals, minima, role)
        singleton_role = all(totals[o][role] == minima[o][role] for o in OBSERVERS)
        entries = {}
        for partition in partitions:
            values, blocked = realize(totals, minima, role, partition)
            if values is None:
                entries[partition_name(partition)] = {
                    "admitted": False,
                    "obstruction": blocked,
                }
                continue
            entries[partition_name(partition)] = {
                "admitted": True,
                "verified_by_recomputation": check_realization(
                    values, totals, minima, role, partition
                ),
                "physical_good_count": len(values),
                "values": {
                    good: {o: str(amount) for o, amount in column.items()}
                    for good, column in values.items()
                },
            }
        rows[role] = {
            "singleton_role": singleton_role,
            "slack_ratio": str(budget),
            "block_counts_admitted": sorted({
                len(p) for p in partitions if entries[partition_name(p)]["admitted"]
            }),
            "partitions": entries,
        }

    # Two derived checks.  The first asks whether admission is blind to the
    # shape of a partition and sees only its number of blocks; the second asks
    # whether the admitted block counts are exactly those at most the slack.
    shape_independent = all(
        len({
            rows[role]["partitions"][partition_name(p)]["admitted"]
            for p in partitions if len(p) == width
        }) == 1
        for role in roles
        for width in (1, 2, 3, 4)
    )
    threshold_matches_slack = all(
        rows[role]["partitions"][partition_name(p)]["admitted"]
        == (len(p) <= (1 if rows[role]["singleton_role"]
                       else int(rows[role]["slack_ratio"])))
        for role in roles
        for p in partitions
    )
    every_realization_verified = all(
        entry["verified_by_recomputation"]
        for role in roles
        for entry in rows[role]["partitions"].values()
        if entry["admitted"]
    )
    return {
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "source_status": raw.get("status"),
        "roles": rows,
        "admission_depends_only_on_block_count": shape_independent,
        "admission_threshold_equals_slack_ratio": threshold_matches_slack,
        "every_admitted_realization_verified": every_realization_verified,
    }


def audit(profile_paths, output_path):
    partitions = tuple(sorted(set(set_partitions(OBSERVERS)),
                              key=lambda p: (len(p), p)))
    assert len(partitions) == 15
    profiles = [audit_profile(path, partitions) for path in profile_paths]
    result = {
        "schema": "identity-aware-witness-realizability-audit-v1",
        "observers": list(OBSERVERS),
        "partition_count": len(partitions),
        "partitions": [partition_name(p) for p in partitions],
        "construction": (
            "block j owns a distinct physical good; an observer in block j "
            "values it at M and spreads T-M evenly over the remaining b-1 "
            "goods, so every non-witness good is worth at least M exactly when "
            "T >= b*M"
        ),
        "profiles": profiles,
        "claim_boundary": (
            "Exact and closed-form for the banked totals/minima profiles listed "
            "here.  It characterises which coincidence partitions a role can "
            "carry; it decides no EFX allocation and does not bear on the "
            "universal fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(tuple(args.profile), args.output)
    for profile in result["profiles"]:
        print(Path(profile["source"]).name)
        print("   shape independent:",
              profile["admission_depends_only_on_block_count"],
              "| threshold == slack:",
              profile["admission_threshold_equals_slack_ratio"],
              "| realizations verified:",
              profile["every_admitted_realization_verified"])
        for role, row in sorted(profile["roles"].items()):
            print(f"   {role:4} slack={row['slack_ratio']:>5} "
                  f"blocks={row['block_counts_admitted']}"
                  f"{' singleton' if row['singleton_role'] else ''}")


if __name__ == "__main__":
    main()
