#!/usr/bin/env python3
"""Search an exact integer neighborhood of a charity-selector boundary."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .scan_charity_threshold_absorption import scan_profile
except ImportError:
    from anneal import atomic_json
    from scan_charity_threshold_absorption import scan_profile


SCHEMA = "charity-selector-local-search-v1"


def candidate_records(document):
    records = document.get("records", ())
    return [
        record
        for record in records
        if record.get("values") is not None
        and record.get("best_absorption_margin") is not None
    ]


def run(source, output, charity_size, cap):
    if output.exists() or cap < 1:
        raise ValueError("a new output and positive cap are required")
    document = json.loads(source.read_text())
    records = candidate_records(document)
    if not records:
        raise ValueError("source contains no selector records")
    seed = min(records, key=lambda record: Fraction(record["best_absorption_margin"]))
    seed_values = tuple(tuple(int(entry) for entry in row) for row in seed["values"])
    best_result = scan_profile(seed_values, charity_size)
    best_values = seed_values
    tested = 0
    eligible = 0
    counterexample = None
    for agent, row in enumerate(seed_values):
        for good, old_value in enumerate(row):
            for new_value in range(1, cap + 1):
                if new_value == old_value:
                    continue
                candidate = [list(candidate_row) for candidate_row in seed_values]
                candidate[agent][good] = new_value
                candidate = tuple(tuple(candidate_row) for candidate_row in candidate)
                result = scan_profile(candidate, charity_size)
                tested += 1
                if result["status"] == "NO_EFX_WITH_CHARITY_STATE":
                    continue
                eligible += 1
                if Fraction(result["best_absorption_margin"]) < Fraction(
                    best_result["best_absorption_margin"]
                ):
                    best_result = result
                    best_values = candidate
                if result["status"] == "BLOCKED_SELECTOR_COUNTEREXAMPLE":
                    counterexample = {"values": candidate, **result}
                    break
            if counterexample is not None:
                break
        if counterexample is not None:
            break
    result = {
        "schema": SCHEMA,
        "status": (
            "BLOCKED_SELECTOR_COUNTEREXAMPLE_FOUND"
            if counterexample is not None
            else "NO_COUNTEREXAMPLE_IN_ONE_ENTRY_BOX"
        ),
        "meaning": (
            "Exact scan of every one-entry replacement in the stated integer "
            "box around the source's minimum-margin selector profile."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "charity_size": charity_size,
        "cap": cap,
        "tested_profile_count": tested,
        "eligible_profile_count": eligible,
        "seed_margin": seed["best_absorption_margin"],
        "best_margin": best_result["best_absorption_margin"],
        "best_values": [list(row) for row in best_values],
        "best_result": best_result,
        "counterexample": counterexample,
        "claim_boundary": (
            "A negative result is local finite evidence only. A counterexample "
            "would refute the extremal selector, not additive EFX existence."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--charity-size", type=int, required=True)
    parser.add_argument("--cap", type=int, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output, args.charity_size, args.cap)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "tested_profile_count",
                    "eligible_profile_count",
                    "seed_margin",
                    "best_margin",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
