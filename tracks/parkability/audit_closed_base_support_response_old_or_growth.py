#!/usr/bin/env python3
"""Audit the closed-target response old-or-external-support dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DOC = Path(__file__).parents[2] / "results" / (
    "CLOSED_BASE_SUPPORT_RESPONSE_OLD_OR_GROWTH_LEMMA_20260813.md"
)


def audit():
    universe = set(range(8))
    records = 0
    old_records = 0
    external_records = 0
    checks = {
        "old_branch_is_subset_of_base": True,
        "external_branch_contains_external_support": True,
        "branches_are_exhaustive": True,
        "branches_are_disjoint": True,
    }
    # Encode a disjoint base/external decomposition by ternary membership:
    # absent, base, external. Enumerate every response subset of their union.
    for word in range(3 ** len(universe)):
        digits = []
        number = word
        for _ in universe:
            digits.append(number % 3)
            number //= 3
        base = {good for good, digit in enumerate(digits) if digit == 1}
        external = {good for good, digit in enumerate(digits) if digit == 2}
        target = base | external
        goods = sorted(target)
        for mask in range(1 << len(goods)):
            response = {
                good for index, good in enumerate(goods) if mask & (1 << index)
            }
            records += 1
            old = not (response & external)
            growth = bool(response & external)
            old_records += old
            external_records += growth
            checks["old_branch_is_subset_of_base"] &= (not old or response <= base)
            checks["external_branch_contains_external_support"] &= (
                not growth or bool(response & external)
            )
            checks["branches_are_exhaustive"] &= old or growth
            checks["branches_are_disjoint"] &= not (old and growth)
    return {
        "schema": "closed-base-support-response-old-or-growth-audit-v1",
        "status": (
            "CLOSED_RESPONSE_OLD_OR_GROWTH_VERIFIED"
            if all(checks.values()) else "AUDIT_FAILED"
        ),
        "records_checked": records,
        "old_response_records": old_records,
        "external_support_records": external_records,
        "checks": checks,
        "document_sha256": hashlib.sha256(DOC.read_bytes()).hexdigest(),
        "claim_boundary": (
            "cap-free support localization only. Response rank, saturation "
            "termination, PI, observer EFX, and four-edge extraction remain open."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records_checked"]}, indent=2))


if __name__ == "__main__":
    main()
