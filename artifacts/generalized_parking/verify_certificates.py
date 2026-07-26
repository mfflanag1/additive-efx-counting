#!/usr/bin/env python3
"""Verify the paper's six parking certificates and one extra (4,8) witness.

The default run is exhaustive: in addition to checking every recorded slack, it
enumerates all n^m labeled allocations and verifies that the EFX0 set is exactly
the n parkings of the recorded floater.  Use --skip-exact for the fast
certificate-only check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable


ARTIFACT_DIR = Path(__file__).resolve().parent
REPO_ROOT = ARTIFACT_DIR.parents[1]
CERTIFICATE_PATH = ARTIFACT_DIR / "certificates.json"


def bundle_value(values: list[list[int]], observer: int, bundle: Iterable[int]) -> int:
    return sum(values[observer][good] for good in bundle)


def tau(values: list[list[int]], observer: int, bundle: list[int]) -> int:
    """The EFX0 removal threshold, with tau(empty)=0."""
    if not bundle:
        return 0
    total = bundle_value(values, observer, bundle)
    return total - min(values[observer][good] for good in bundle)


def assignment_to_bundles(assignment: list[int], n: int) -> list[list[int]]:
    bundles = [[] for _ in range(n)]
    for good, owner in enumerate(assignment):
        bundles[owner].append(good)
    return bundles


def is_efx0(values: list[list[int]], bundles: list[list[int]]) -> bool:
    n = len(values)
    for observer in range(n):
        own = bundle_value(values, observer, bundles[observer])
        for target in range(n):
            if observer != target and own < tau(values, observer, bundles[target]):
                return False
    return True


def parking_assignment(
    base_bundles: list[list[int]], floater: int, host: int, m: int
) -> list[int]:
    assignment = [-1] * m
    for owner, bundle in enumerate(base_bundles):
        for good in bundle:
            assert assignment[good] == -1
            assignment[good] = owner
    assert assignment[floater] == -1
    assignment[floater] = host
    assert all(owner >= 0 for owner in assignment)
    return assignment


def base_slack_minima(
    values: list[list[int]], base_bundles: list[list[int]]
) -> tuple[int, int]:
    n = len(values)
    efx_slacks = []
    envy_slacks = []
    for observer in range(n):
        own = bundle_value(values, observer, base_bundles[observer])
        for target in range(n):
            if observer == target:
                continue
            efx_slacks.append(own - tau(values, observer, base_bundles[target]))
            envy_slacks.append(
                own - bundle_value(values, observer, base_bundles[target])
            )
    return min(efx_slacks), min(envy_slacks)


def parking_slack_matrix(
    values: list[list[int]], base_bundles: list[list[int]], floater: int
) -> list[list[int | None]]:
    """Rows are observers and columns are hosts; the diagonal is inapplicable."""
    n = len(values)
    matrix: list[list[int | None]] = []
    for observer in range(n):
        own = bundle_value(values, observer, base_bundles[observer])
        row: list[int | None] = []
        for host in range(n):
            if observer == host:
                row.append(None)
                continue
            host_bundle = base_bundles[host]
            host_value = bundle_value(values, observer, host_bundle)
            if host_bundle:
                host_minimum = min(values[observer][good] for good in host_bundle)
                surplus = max(0, values[observer][floater] - host_minimum)
            else:
                surplus = 0
            row.append(own - host_value - surplus)
        matrix.append(row)
    return matrix


def exhaustive_efx0_assignments(values: list[list[int]]) -> list[list[int]]:
    """Exact stdlib-only enumeration using subset value/threshold tables."""
    n = len(values)
    m = len(values[0])
    subset_count = 1 << m
    subset_values = [[0] * subset_count for _ in range(n)]
    subset_tau = [[0] * subset_count for _ in range(n)]

    for observer in range(n):
        minima = [10**100] * subset_count
        for mask in range(1, subset_count):
            bit = mask & -mask
            good = bit.bit_length() - 1
            rest = mask ^ bit
            subset_values[observer][mask] = (
                subset_values[observer][rest] + values[observer][good]
            )
            minima[mask] = min(minima[rest], values[observer][good])
            subset_tau[observer][mask] = (
                subset_values[observer][mask] - minima[mask]
            )

    bundles = [0] * n
    assignment = [0] * m
    found: list[list[int]] = []

    def allocation_is_efx0() -> bool:
        for observer in range(n):
            own = subset_values[observer][bundles[observer]]
            thresholds = subset_tau[observer]
            for target in range(n):
                if observer != target and own < thresholds[bundles[target]]:
                    return False
        return True

    def visit(good: int) -> None:
        if good == m:
            if allocation_is_efx0():
                found.append(assignment.copy())
            return
        bit = 1 << good
        for owner in range(n):
            assignment[good] = owner
            bundles[owner] |= bit
            visit(good + 1)
            bundles[owner] ^= bit

    visit(0)
    return found


def validate_witness(record: dict, exact: bool) -> dict:
    source_path = REPO_ROOT / record["source"]
    source_bytes = source_path.read_bytes()
    actual_hash = hashlib.sha256(source_bytes).hexdigest()
    assert actual_hash == record["source_sha256"], (
        record["id"],
        "source hash",
        actual_hash,
        record["source_sha256"],
    )
    instance = json.loads(source_bytes)
    n = instance["n"]
    m = instance["m"]
    values = instance["values"]
    assert (n, m) == (record["n"], record["m"])
    assert len(values) == n and all(len(row) == m for row in values)
    assert all(value >= 0 for row in values for value in row)

    floater = record["floater"]
    base_bundles = record["base_bundles"]
    assert len(base_bundles) == n
    base_goods = sorted(good for bundle in base_bundles for good in bundle)
    assert base_goods == [good for good in range(m) if good != floater]
    assert all(len(bundle) == len(set(bundle)) for bundle in base_bundles)

    base_efx_min, base_envy_min = base_slack_minima(values, base_bundles)
    assert base_efx_min == record["base_efx_min_slack"]
    assert base_envy_min == record["base_envy_min_slack"]
    assert base_efx_min >= 0
    assert base_envy_min >= 0

    row_minimum_flags = [
        values[observer][floater] == min(values[observer])
        for observer in range(n)
    ]
    assert row_minimum_flags == record["floater_is_row_minimum"]
    assert all(row_minimum_flags) == record["universal_minimum"]

    slack_matrix = parking_slack_matrix(values, base_bundles, floater)
    assert slack_matrix == record["parking_slack_matrix"]
    finite_slacks = [
        slack for row in slack_matrix for slack in row if slack is not None
    ]
    assert min(finite_slacks) == record["parking_min_slack"]
    assert min(finite_slacks) >= 0

    parkings = [
        parking_assignment(base_bundles, floater, host, m) for host in range(n)
    ]
    assert len({tuple(assignment) for assignment in parkings}) == n
    for assignment in parkings:
        assert is_efx0(values, assignment_to_bundles(assignment, n))

    if exact:
        exact_efx0 = exhaustive_efx0_assignments(values)
        assert len(exact_efx0) == record["expected_efx0_count"]
        assert {tuple(assignment) for assignment in exact_efx0} == {
            tuple(assignment) for assignment in parkings
        }

    return {
        "id": record["id"],
        "cell": record["cell"],
        "count": record["expected_efx0_count"],
        "base_efx_min": base_efx_min,
        "base_envy_min": base_envy_min,
        "parking_min": min(finite_slacks),
        "universal_minimum": all(row_minimum_flags),
        "exact": exact,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-exact",
        action="store_true",
        help="check the theorem certificates but skip exhaustive n^m enumeration",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="ID",
        help="verify only a named witness; may be repeated",
    )
    args = parser.parse_args()

    certificate = json.loads(CERTIFICATE_PATH.read_text())
    selected = set(args.only)
    records = [
        record
        for record in certificate["witnesses"]
        if not selected or record["id"] in selected
    ]
    if selected:
        found = {record["id"] for record in records}
        assert found == selected, f"unknown witness ids: {sorted(selected - found)}"

    exact = not args.skip_exact
    for record in records:
        result = validate_witness(record, exact=exact)
        mode = "exact enumeration" if exact else "certificate only"
        universal = "yes" if result["universal_minimum"] else "no"
        print(
            f"PASS {result['id']} {result['cell']}: "
            f"count={result['count']}, base-EFX-min={result['base_efx_min']}, "
            f"base-envy-min={result['base_envy_min']}, "
            f"parking-min={result['parking_min']}, "
            f"universal-min={universal} ({mode})"
        )
    print(f"PASS all {len(records)} generalized-parking certificates")


if __name__ == "__main__":
    main()
