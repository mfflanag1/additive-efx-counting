#!/usr/bin/env python3
"""Exact audit helpers for a fixed-core minimum-slot token orbit."""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_threshold_plateau_exact_paths import (
        exact_best_hall_margin,
        mask_threshold,
        mask_value,
    )
except ImportError:
    from anneal import atomic_json
    from audit_threshold_plateau_exact_paths import (
        exact_best_hall_margin,
        mask_threshold,
        mask_value,
    )


SCHEMA = "minimum-slot-orbit-audit-v1"


def masks_from_bundles(bundles):
    return tuple(
        sum(1 << good for good in bundle)
        for bundle in bundles
    )


def bundles_from_masks(masks, m):
    return tuple(
        tuple(good for good in range(m) if int(mask) & (1 << good))
        for mask in masks
    )


def exact_eligible(values, state):
    n = len(values)
    for observer in range(n):
        own = mask_value(values, observer, state["masks"][observer])
        if own < values[observer][state["floater"]]:
            return False
        for target in range(n):
            if target != observer and own < mask_threshold(
                values,
                observer,
                state["masks"][target],
            ):
                return False
    return True


def exact_theta(values, state):
    return sum(
        Fraction(
            mask_threshold(values, owner, state["masks"][owner]),
            sum(values[owner]),
        )
        for owner in range(len(values))
    )


def minimum_slot_orbit_states(values, base_state, selected_minima):
    n = len(values)
    m = len(values[0])
    if len(selected_minima) != n:
        raise ValueError("one selected minimum is required per owner")
    if len(set(selected_minima)) != n:
        raise ValueError("selected minima must be distinct")
    base_bundles = bundles_from_masks(base_state["masks"], m)
    cores = []
    for owner, selected in enumerate(selected_minima):
        if selected not in base_bundles[owner]:
            raise ValueError(f"good {selected} is not in owner {owner}'s bundle")
        if values[owner][selected] != min(
            values[owner][good] for good in base_bundles[owner]
        ):
            raise ValueError(f"good {selected} is not owner {owner}'s minimum")
        cores.append(tuple(good for good in base_bundles[owner] if good != selected))
    tokens = (*selected_minima, base_state["floater"])
    for assignment in itertools.permutations(tokens):
        bundles = tuple(
            tuple(sorted((*cores[owner], assignment[owner])))
            for owner in range(n)
        )
        yield {
            "assignment": assignment,
            "floater": assignment[n],
            "masks": masks_from_bundles(bundles),
        }


def audit_orbit(values, base_state, selected_minima, *, include_records=True):
    base_theta = exact_theta(values, base_state)
    records = []
    eligible_count = 0
    completing_count = 0
    best_margin = None
    best_record = None
    minimum_theta = None
    for state in minimum_slot_orbit_states(values, base_state, selected_minima):
        if not exact_eligible(values, state):
            continue
        eligible_count += 1
        theta = exact_theta(values, state)
        if theta < base_theta:
            raise AssertionError("eligible minimum-slot permutation lowered theta")
        margin, host, permutation, bottlenecks = exact_best_hall_margin(values, state)
        completing = margin >= 0
        completing_count += int(completing)
        record = {
            "assignment": list(state["assignment"]),
            "floater": state["floater"],
            "masks": list(state["masks"]),
            "theta": str(theta),
            "margin": str(margin),
            "best_host": host,
            "best_permutation": list(permutation),
            "bottleneck_count": len(bottlenecks),
            "completing": completing,
        }
        if best_margin is None or margin > best_margin:
            best_margin = margin
            best_record = record
        if minimum_theta is None or theta < minimum_theta:
            minimum_theta = theta
        if include_records:
            records.append(record)
    if not eligible_count or best_record is None or best_margin is None:
        raise AssertionError("the base token assignment must be eligible")
    return {
        "schema": SCHEMA,
        "status": (
            "ORBIT_COMPLETION_FOUND"
            if completing_count
            else "ORBIT_ALL_ELIGIBLE_STATES_BLOCKED"
        ),
        "meaning": (
            "Exact rational audit of every permutation of four selected owner "
            "minima and one floater over four fixed cores."
        ),
        "n": len(values),
        "m": len(values[0]),
        "selected_minima": list(selected_minima),
        "base_floater": base_state["floater"],
        "base_masks": list(base_state["masks"]),
        "base_theta": str(base_theta),
        "minimum_eligible_orbit_theta": str(minimum_theta),
        "orbit_state_count": len(tuple(itertools.permutations(range(len(values) + 1)))),
        "eligible_orbit_state_count": eligible_count,
        "completing_orbit_state_count": completing_count,
        "best_orbit_margin": str(best_margin),
        "best_orbit_state": best_record,
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--values", type=Path, required=True)
    parser.add_argument("--floater", type=int, required=True)
    parser.add_argument("--masks", required=True)
    parser.add_argument("--minima", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    values_document = json.loads(args.values.read_text())
    values = values_document.get("values", values_document)
    masks = tuple(int(entry) for entry in args.masks.split(","))
    minima = tuple(int(entry) for entry in args.minima.split(","))
    result = audit_orbit(
        values,
        {"floater": args.floater, "masks": masks},
        minima,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
