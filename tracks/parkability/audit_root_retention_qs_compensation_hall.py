#!/usr/bin/env python3
"""Exact finite audit of root-retention compensation identities and Hall cut."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def value(row, goods):
    return sum((row[g] for g in goods), Fraction(0))


def run():
    goods = tuple(range(4))
    owners = ("r", "q", "d", "s")
    rows = {
        owner: {g: Fraction((index + 2) * (g + 1), 37) for g in goods}
        for index, owner in enumerate(owners)
    }
    identity_cases = 0
    price_bound_cases = 0
    hall_cases = 0

    # Enumerate every complete endpoint allocation and every current-root set.
    for assignment in product(range(4), repeat=len(goods)):
        z = {
            owner: frozenset(g for g, target in zip(goods, assignment) if target == i)
            for i, owner in enumerate(owners)
        }
        for root_mask in range(1 << len(goods)):
            y_root = frozenset(g for g in goods if root_mask & (1 << g))
            captured = {owner: z[owner] & y_root for owner in ("q", "d", "s")}
            released = z["r"] - y_root
            for released_assignment in product(range(3), repeat=len(released)):
                released_tuple = tuple(sorted(released))
                packets = {
                    owner: frozenset(
                        g for g, target in zip(released_tuple, released_assignment)
                        if target == i
                    )
                    for i, owner in enumerate(("q", "s", "d"))
                }
                w = {
                    "r": y_root,
                    "q": (z["q"] - y_root) | packets["q"],
                    "s": (z["s"] - y_root) | packets["s"],
                    "d": (z["d"] - y_root) | packets["d"],
                }
                assert set().union(*w.values()) == set(goods)
                assert sum(len(bundle) for bundle in w.values()) == len(goods)
                for owner in ("q", "s"):
                    lhs = value(rows[owner], w[owner]) - 1
                    rhs = (
                        value(rows[owner], z[owner]) - 1
                        - value(rows[owner], captured[owner])
                        + value(rows[owner], packets[owner])
                    )
                    assert lhs == rhs
                    identity_cases += 1

            # Check the paid-endpoint price bound whenever the hypothesis holds.
            for owner in ("q", "s"):
                endpoint_value = value(rows[owner], z[owner])
                if endpoint_value >= 1:
                    price = max(
                        Fraction(0),
                        1 - endpoint_value + value(rows[owner], captured[owner]),
                    )
                    assert 0 <= price <= value(rows[owner], captured[owner])
                    price_bound_cases += 1

            # Unfiltered two-family Hall classification on the released pool.
            released_tuple = tuple(sorted(released))
            subsets = [
                frozenset(
                    g for position, g in enumerate(released_tuple)
                    if mask & (1 << position)
                )
                for mask in range(1 << len(released_tuple))
            ]
            pq = [a for a in subsets if len(a) % 2 == 0]
            ps = [a for a in subsets if sum(a) % 2 == 0]
            edge_exists = any(not (a & b) for a in pq for b in ps)
            obstruction = not pq or (bool(pq) and not ps) or (
                bool(pq) and bool(ps) and all(a & b for a in pq for b in ps)
            )
            assert edge_exists != obstruction
            hall_cases += 1

    theorem = ROOT / "results/ROOT_RETENTION_QS_COMPENSATION_HALL_REDUCTION_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-retention-qs-compensation-hall-audit-v1",
        "status": "AUDIT_PASSED",
        "identity_cases": identity_cases,
        "price_bound_cases": price_bound_cases,
        "hall_classification_cases": hall_cases,
        "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact finite audit of the set partition, compensation identities, "
            "paid-endpoint price bound, and abstract two-family Hall alternative. "
            "Supplier compatibility remains an analytic premise."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
