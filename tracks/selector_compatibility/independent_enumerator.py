#!/usr/bin/env python3
"""Standalone exact four-agent EFX enumeration; no project helpers are imported.

Input schemas: ``lexmax-partial-counterexample-v1`` (the existing artifact), or
``selector-compatibility-input-v1`` with n, m, agent_order, values, and candidate.
Both use candidate.base_owner: one entry per *physical* good, either 0..3 or null
for charity. Values are positive integers or rational strings; JSON decimals are
parsed as exact Fractions, never binary floats. Priority is always [0, 1, 2, 3].

All 5**m assignments are visited, including complete allocations. Subset tables
reduce the conjunction of all deleted-good EFX inequalities to its exact maximum
right-hand side. Every reported witness is also checked deletion by deletion.
Ties retain the first assignment in lexicographic owner-code order (charity=4),
and report the full number of maximizing assignments. Runtime is deliberately
excluded from the deterministic JSON report.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from math import comb, lcm
from pathlib import Path
import sys
from typing import Any


INPUT_SCHEMA = "selector-compatibility-input-v1"
LEGACY_SCHEMA = "lexmax-partial-counterexample-v1"
OUTPUT_SCHEMA = "selector-compatibility-independent-audit-v1"
PRIORITY = (0, 1, 2, 3)
DOMAIN_DEFINITIONS = {
    "all_partial_efx": "All partial EFX allocations, including complete; no charity safety condition.",
    "all_partial_efx_safe": "All partial EFX allocations with whole-charity nonenvy, including complete.",
    "at_most_one_charity_efx_safe": "EFX and whole-charity nonenvy with zero or one charity good, including complete.",
    "exactly_one_charity_efx_safe": "EFX and whole-charity nonenvy with exactly one charity good.",
    "complete_efx": "Complete EFX allocations (zero charity goods).",
}


def exact_number(value: Any, location: str, *, positive: bool = True) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError(f"{location}: expected an exact integer or rational, not {type(value).__name__}")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError, OverflowError) as error:
        raise ValueError(f"{location}: invalid rational value") from error
    if positive and result <= 0:
        raise ValueError(f"{location}: values must be strictly positive")
    return result


def exact_json(value: Fraction) -> int | str:
    return value.numerator if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def validate_owners(owners: Any, m: int) -> tuple[int | None, ...]:
    if not isinstance(owners, (list, tuple)) or len(owners) != m:
        raise ValueError(f"candidate.base_owner must contain exactly {m} entries")
    if any(owner is not None and (type(owner) is not int or owner not in PRIORITY) for owner in owners):
        raise ValueError("each physical good must have one owner in 0..3 or null for charity")
    return tuple(owners)


@dataclass(frozen=True)
class Instance:
    values: tuple[tuple[Fraction, ...], ...]
    candidate: tuple[int | None, ...]

    @property
    def m(self) -> int:
        return len(self.values[0])


def parse_instance(document: Any, *, max_goods: int = 10) -> Instance:
    if type(max_goods) is not int or max_goods < 1:
        raise ValueError("max_goods must be a positive integer")
    if not isinstance(document, dict) or document.get("schema") not in (INPUT_SCHEMA, LEGACY_SCHEMA):
        raise ValueError(f"schema must be {INPUT_SCHEMA!r} or {LEGACY_SCHEMA!r}")
    if type(document.get("n")) is not int or document["n"] != 4:
        raise ValueError("exactly four agents are required")
    m = document.get("m")
    if type(m) is not int or not 1 <= m <= max_goods:
        raise ValueError(f"m must be an integer between 1 and max_goods={max_goods}")
    order = document.get("agent_order")
    if not isinstance(order, list) or any(type(i) is not int for i in order) or order != list(PRIORITY):
        raise ValueError("agent_order must be exactly [0, 1, 2, 3]")
    if document["schema"] == LEGACY_SCHEMA:
        lift = document.get("positive_nondegenerate_lift")
        if not isinstance(lift, dict):
            raise ValueError("positive_nondegenerate_lift must be an object")
        raw_values = lift.get("values")
    else:
        raw_values = document.get("values")
    if not isinstance(raw_values, list) or len(raw_values) != 4:
        raise ValueError("values must contain exactly four rows")
    rows = []
    for i, row in enumerate(raw_values):
        if not isinstance(row, list) or len(row) != m:
            raise ValueError(f"values[{i}] must contain exactly m={m} entries")
        rows.append(tuple(exact_number(value, f"values[{i}][{g}]") for g, value in enumerate(row)))
    candidate = document.get("candidate")
    if not isinstance(candidate, dict):
        raise ValueError("candidate must be an object with base_owner")
    owners = validate_owners(candidate.get("base_owner"), m)
    bundles = [[g for g, owner in enumerate(owners) if owner == i] for i in PRIORITY]
    if "bundles" in candidate:
        declared = candidate["bundles"]
        if (not isinstance(declared, list) or len(declared) != 4
                or any(not isinstance(bundle, list) or any(type(g) is not int for g in bundle)
                       for bundle in declared)
                or any(sorted(bundle) != expected for bundle, expected in zip(declared, bundles))):
            raise ValueError("candidate.bundles must agree with base_owner without duplicate or missing goods")
    if "floater" in candidate:
        floater = candidate["floater"]
        if type(floater) is not int or [g for g, owner in enumerate(owners) if owner is None] != [floater]:
            raise ValueError("candidate.floater must be the unique charity good")
    if "utilities" in candidate:
        utilities = candidate["utilities"]
        if not isinstance(utilities, list) or len(utilities) != 4:
            raise ValueError("candidate.utilities must have four entries")
        claimed = tuple(exact_number(value, f"candidate.utilities[{i}]", positive=False)
                        for i, value in enumerate(utilities))
        actual = tuple(sum((rows[i][g] for g in bundles[i]), Fraction(0)) for i in PRIORITY)
        if claimed != actual:
            raise ValueError("candidate.utilities disagrees with the physical allocation")
    return Instance(tuple(rows), owners)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON number: {token}")


def load_instance(path: str | Path, *, max_goods: int = 10) -> Instance:
    with Path(path).open(encoding="utf-8") as stream:
        document = json.load(stream, parse_float=Fraction, parse_constant=_reject_constant,
                             object_pairs_hook=_unique_object)
    return parse_instance(document, max_goods=max_goods)


@dataclass(frozen=True)
class Tables:
    denominator: int
    integer_values: tuple[tuple[int, ...], ...]
    sums: tuple[tuple[int, ...], ...]
    deletion_max: tuple[tuple[int, ...], ...]


def make_tables(instance: Instance) -> Tables:
    denominator = lcm(*(value.denominator for row in instance.values for value in row))
    integer_values = tuple(tuple(int(value * denominator) for value in row) for row in instance.values)
    sum_rows, deletion_rows = [], []
    for row in integer_values:
        sums = [0] * (1 << instance.m)
        deletion_max = [0] * len(sums)
        for mask in range(1, len(sums)):
            bit = mask & -mask
            sums[mask] = sums[mask ^ bit] + row[bit.bit_length() - 1]
            # Explicitly visit every physical deleted good; empty targets are vacuous.
            remaining = mask
            while remaining:
                deleted_bit = remaining & -remaining
                deletion_max[mask] = max(deletion_max[mask], sums[mask ^ deleted_bit])
                remaining ^= deleted_bit
        sum_rows.append(tuple(sums))
        deletion_rows.append(tuple(deletion_max))
    return Tables(denominator, integer_values, tuple(sum_rows), tuple(deletion_rows))


def allocation_record(instance: Instance, owners: Any, tables: Tables | None = None) -> dict[str, Any]:
    """Validate conservation, all EFX deletion inequalities, and the *whole* pool."""
    owners = validate_owners(owners, instance.m)
    tables = tables or make_tables(instance)
    bundles = [[g for g, owner in enumerate(owners) if owner == i] for i in PRIORITY]
    charity = [g for g, owner in enumerate(owners) if owner is None]
    utilities = tuple(sum(tables.integer_values[i][g] for g in bundles[i]) for i in PRIORITY)
    efx_comparisons = []
    for observer in PRIORITY:
        row = tables.integer_values[observer]
        for target in PRIORITY:
            target_value = sum(row[g] for g in bundles[target])
            for deleted in bundles[target]:
                rhs = target_value - row[deleted]
                efx_comparisons.append({
                    "observer": observer, "target": target, "deleted_good": deleted,
                    "lhs_scaled": utilities[observer], "rhs_scaled": rhs,
                    "slack_scaled": utilities[observer] - rhs,
                })
    charity_slacks = [utilities[i] - sum(tables.integer_values[i][g] for g in charity) for i in PRIORITY]
    is_efx = all(comparison["slack_scaled"] >= 0 for comparison in efx_comparisons)
    safe = all(slack >= 0 for slack in charity_slacks)
    memberships = domain_memberships(is_efx, safe, len(charity))
    return {
        "base_owner": list(owners), "bundles": bundles, "charity": charity,
        "utilities_scaled": list(utilities),
        "utilities": [exact_json(Fraction(value, tables.denominator)) for value in utilities],
        "is_efx": is_efx, "whole_charity_nonenvy": safe,
        "charity_nonenvy_slacks_scaled": charity_slacks,
        "efx_comparisons": efx_comparisons,
        "min_efx_slack_scaled": min((item["slack_scaled"] for item in efx_comparisons), default=None),
        "domain_membership": memberships,
    }


def domain_memberships(is_efx: bool, safe: bool, charity_size: int) -> dict[str, bool]:
    return dict(zip(DOMAIN_DEFINITIONS, (
        is_efx, is_efx and safe, is_efx and safe and charity_size <= 1,
        is_efx and safe and charity_size == 1, is_efx and charity_size == 0,
    )))


@dataclass
class Accumulator:
    count: int = 0
    key: tuple[int, ...] | None = None
    maximizer_count: int = 0
    owners: tuple[int, ...] | None = None

    def add(self, key: tuple[int, ...], owners: tuple[int, ...]) -> None:
        self.count += 1
        if self.key is None or key > self.key:
            self.key, self.owners, self.maximizer_count = key, owners, 1
        elif key == self.key:
            self.maximizer_count += 1

    def report(self, instance: Instance, tables: Tables) -> dict[str, Any]:
        witness = None if self.owners is None else allocation_record(
            instance, [None if owner == 4 else owner for owner in self.owners], tables)
        if witness is not None and (not witness["is_efx"] or tuple(witness["utilities_scaled"]) != self.key):
            raise RuntimeError("independent witness recheck disagrees with enumeration")
        return {
            "allocation_count": self.count, "maximizer_count": self.maximizer_count,
            "maximum_utility_key_scaled": None if self.key is None else list(self.key),
            "maximum_utility_key": None if self.key is None else [
                exact_json(Fraction(value, tables.denominator)) for value in self.key],
            "maximizer": witness,
        }


def audit(instance: Instance, *, max_goods: int = 10) -> dict[str, Any]:
    # Revalidate public API inputs as well as CLI documents before any enumeration.
    instance = parse_instance({
        "schema": INPUT_SCHEMA, "n": 4, "m": instance.m, "agent_order": list(PRIORITY),
        "values": [list(row) for row in instance.values],
        "candidate": {"base_owner": list(instance.candidate)},
    }, max_goods=max_goods)
    tables = make_tables(instance)
    accumulators = [Accumulator() for _ in DOMAIN_DEFINITIONS]
    outside_restricted = Accumulator()
    counts_by_charity_size = [0] * (instance.m + 1)
    efx_counts_by_charity_size = [0] * (instance.m + 1)
    safe_efx_counts_by_charity_size = [0] * (instance.m + 1)
    visited = 0
    bits = tuple(1 << g for g in range(instance.m))
    for owners in product(range(5), repeat=instance.m):
        masks = [0, 0, 0, 0, 0]
        for bit, owner in zip(bits, owners):
            masks[owner] |= bit
        visited += 1
        charity_size = masks[4].bit_count()
        counts_by_charity_size[charity_size] += 1
        utilities = tuple(tables.sums[i][masks[i]] for i in PRIORITY)
        if any(utilities[i] < tables.deletion_max[i][masks[j]] for i in PRIORITY for j in PRIORITY):
            continue
        efx_counts_by_charity_size[charity_size] += 1
        accumulators[0].add(utilities, owners)
        safe = all(utilities[i] >= tables.sums[i][masks[4]] for i in PRIORITY)
        if safe:
            safe_efx_counts_by_charity_size[charity_size] += 1
            accumulators[1].add(utilities, owners)
            if charity_size <= 1:
                accumulators[2].add(utilities, owners)
            if charity_size == 1:
                accumulators[3].add(utilities, owners)
        if charity_size == 0:
            accumulators[4].add(utilities, owners)
        if not safe or charity_size > 1:
            outside_restricted.add(utilities, owners)
    expected = 5 ** instance.m
    expected_by_size = [comb(instance.m, k) * 4 ** (instance.m - k) for k in range(instance.m + 1)]
    if visited != expected or counts_by_charity_size != expected_by_size:
        raise RuntimeError("incomplete enumeration: refusing to issue an audit report")
    candidate = allocation_record(instance, instance.candidate, tables)
    candidate_key = tuple(candidate["utilities_scaled"])
    candidate["attains_domain_maximum"] = {
        name: candidate["domain_membership"][name] and accumulator.key == candidate_key
        for name, accumulator in zip(DOMAIN_DEFINITIONS, accumulators)
    }
    domains = {}
    for name, accumulator in zip(DOMAIN_DEFINITIONS, accumulators):
        result = accumulator.report(instance, tables)
        if result["maximizer"] is not None and not result["maximizer"]["domain_membership"][name]:
            raise RuntimeError(f"maximizer fails its domain's independent recheck: {name}")
        result["definition"] = DOMAIN_DEFINITIONS[name]
        domains[name] = result
    outside_report = outside_restricted.report(instance, tables)
    improving = None
    if outside_restricted.key is not None and outside_restricted.key > candidate_key:
        improving = outside_report["maximizer"]
    return {
        "schema": OUTPUT_SCHEMA,
        "n": 4, "m": instance.m, "agent_order": list(PRIORITY),
        "arithmetic": {
            "method": "Exact rational input; common-denominator integer comparisons.",
            "common_denominator": tables.denominator,
            "values_scaled": [list(row) for row in tables.integer_values],
        },
        "enumeration": {
            "complete": True, "expected_assignment_count": expected,
            "visited_assignment_count": visited,
            "assignment_count_by_charity_size": counts_by_charity_size,
            "efx_count_by_charity_size": efx_counts_by_charity_size,
            "safe_efx_count_by_charity_size": safe_efx_counts_by_charity_size,
            "tie_break": "First base-5 owner-code vector in lexicographic order; charity code is 4.",
        },
        "candidate": candidate,
        "domains": domains,
        "outside_at_most_one_safe_domain": {
            "definition": "All partial EFX allocations that fail whole-charity nonenvy or have more than one charity good.",
            **outside_report,
        },
        "globally_improving_out_of_class_efx_assignment": improving,
        "improvement_comparison": "Strict lexicographic utility improvement over the supplied candidate, priority [0,1,2,3]; outside the at-most-one-charity safe domain.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="valuation/candidate JSON")
    parser.add_argument("--max-goods", type=int, default=10, help="fail closed above this size (default: 10)")
    parser.add_argument("--output", type=Path, help="write deterministic JSON after a complete audit")
    args = parser.parse_args(argv)
    try:
        report = audit(load_instance(args.input, max_goods=args.max_goods), max_goods=args.max_goods)
        rendered = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (ValueError, TypeError, OSError, RuntimeError) as error:
        print(f"audit failed: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("audit interrupted: no complete report issued", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
