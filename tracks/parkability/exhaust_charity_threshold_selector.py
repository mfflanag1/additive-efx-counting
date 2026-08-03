#!/usr/bin/env python3
"""Exhaust a finite positive-integer domain for the charity selector."""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path

try:
    from .anneal import atomic_json
    from .scan_charity_threshold_absorption import scan_profile
except ImportError:
    from anneal import atomic_json
    from scan_charity_threshold_absorption import scan_profile


SCHEMA = "charity-threshold-selector-exhaustion-v1"


def primitive_rows(m, cap):
    for row in itertools.product(range(1, cap + 1), repeat=m):
        if math.gcd(*row) == 1:
            yield row


def run(n, m, cap, charity_size, output, max_profiles):
    if output.exists():
        raise ValueError("output must be new")
    rows = tuple(primitive_rows(m, cap))
    profile_bound = len(rows) ** n
    if profile_bound > max_profiles:
        raise ValueError(
            f"primitive profile count {profile_bound} exceeds --max-profiles"
        )
    tested = 0
    eligible = 0
    zero_margin = 0
    minimum_margin = None
    minimum_values = None
    counterexample = None
    for values in itertools.product(rows, repeat=n):
        result = scan_profile(values, charity_size)
        tested += 1
        margin_text = result.get("best_absorption_margin")
        if margin_text is None:
            continue
        eligible += 1
        margin = Fraction(margin_text)
        zero_margin += margin == 0
        if minimum_margin is None or margin < minimum_margin:
            minimum_margin = margin
            minimum_values = values
        if result["status"] == "BLOCKED_SELECTOR_COUNTEREXAMPLE":
            counterexample = {
                "values": [list(row) for row in values],
                **result,
            }
            break
    document = {
        "schema": SCHEMA,
        "status": (
            "BLOCKED_SELECTOR_COUNTEREXAMPLE_FOUND"
            if counterexample is not None
            else "FINITE_DOMAIN_SELECTOR_THEOREM"
        ),
        "meaning": (
            "Exact enumeration of all rowwise-primitive positive integer "
            "valuation profiles in the stated box. Row scaling leaves the "
            "selector invariant, so omitted nonprimitive rows are duplicates."
        ),
        "n": n,
        "m": m,
        "cap": cap,
        "charity_size": charity_size,
        "primitive_row_count": len(rows),
        "profile_count": tested,
        "eligible_profile_count": eligible,
        "zero_margin_profile_count": zero_margin,
        "minimum_margin": None if minimum_margin is None else str(minimum_margin),
        "minimum_values": (
            None if minimum_values is None else [list(row) for row in minimum_values]
        ),
        "counterexample": counterexample,
        "claim_boundary": (
            "A finite-domain theorem does not imply the unrestricted additive "
            "selector. A counterexample refutes the selector, not EFX existence."
        ),
    }
    atomic_json(output, document)
    return document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--m", type=int, required=True)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--charity-size", type=int, required=True)
    parser.add_argument("--max-profiles", type=int, default=1_000_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.n,
        args.m,
        args.cap,
        args.charity_size,
        args.output,
        args.max_profiles,
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "profile_count",
                    "eligible_profile_count",
                    "zero_margin_profile_count",
                    "minimum_margin",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
