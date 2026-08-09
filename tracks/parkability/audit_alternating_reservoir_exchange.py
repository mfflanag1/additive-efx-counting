#!/usr/bin/env python3
"""Replay the cap-free reservoir-exchange construction on exact profiles."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .decide_alternating_two_safe_bundle_gate import (
        numeric_desired,
        numeric_safe,
    )
    from .run_alternating_variable_packet_rooted_cegar import (
        make_cell,
        numeric_efx,
        numeric_utilities,
    )
except ImportError:
    from decide_alternating_two_safe_bundle_gate import (
        numeric_desired,
        numeric_safe,
    )
    from run_alternating_variable_packet_rooted_cegar import (
        make_cell,
        numeric_efx,
        numeric_utilities,
    )


SCHEMA = "alternating-reservoir-exchange-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def powerset(goods):
    for size in range(1, len(goods) + 1):
        yield from itertools.combinations(goods, size)


def threshold(values, observer, bundle):
    return max(
        sum(values[observer][good] for good in bundle if good != removed)
        for removed in bundle
    )


def desired_subsets(values, own, pool):
    for candidate in powerset(pool):
        for source in range(4):
            if numeric_desired(values, own, source, candidate):
                yield source, candidate


def select_pair(values, cell):
    _tr, _br, tq, bq = cell["packets"]
    desired = tq + (cell["floater"],)
    reservoir = cell["base_bundles"][1] + bq
    own = numeric_utilities(values, cell["base_owner"])
    if not numeric_desired(values, own, 2, desired):
        raise AssertionError("selected T_q+f block is not desired by s")
    forbidden_sources = tuple(
        source
        for source in (0, 3)
        if any(
            numeric_desired(values, own, source, candidate)
            for candidate in powerset(reservoir)
        )
    )
    if forbidden_sources:
        raise AssertionError(f"compatible-family absence failed: {forbidden_sources}")

    target = threshold(values, 3, desired)
    reservoir_value = sum(values[3][good] for good in reservoir)
    branch = "low_reservoir"
    if reservoir_value >= target:
        branch = "threshold_minimal_safe"
        payment = list(reservoir)
        changed = True
        while changed:
            changed = False
            for good in tuple(payment):
                remainder = tuple(item for item in payment if item != good)
                if sum(values[3][item] for item in remainder) >= target:
                    payment.remove(good)
                    changed = True
                    break
        payment = tuple(payment)
        if numeric_safe(values, own, payment):
            source, active = 2, desired
            return branch, source, active, payment
        branch = "unsafe_threshold_subset_reversal"
        unsafe_remainder = next(
            tuple(good for good in payment if good != removed)
            for removed in payment
            if any(
                sum(values[observer][good] for good in payment if good != removed)
                > own[observer]
                for observer in range(4)
            )
        )
        candidates = desired_subsets(values, own, unsafe_remainder)
    else:
        candidates = desired_subsets(values, own, reservoir)

    source, active = next(
        (source, active) for source, active in candidates if source in (1, 2)
    )
    return branch, source, active, desired


def audit_profile(values, label, sizes):
    cell = make_cell(sizes)
    if any(entry <= 0 for row in values for entry in row):
        raise AssertionError("profile is not strictly positive")
    own = numeric_utilities(values, cell["base_owner"])
    branch, source, active, payment = select_pair(values, cell)
    if set(active).intersection(payment):
        raise AssertionError("selected bundles overlap")
    if not numeric_desired(values, own, source, active):
        raise AssertionError("selected active bundle is not desired")
    if not numeric_safe(values, own, payment):
        raise AssertionError("selected payment is not common-safe")
    slack = sum(values[3][good] for good in payment) - threshold(values, 3, active)
    if slack < 0:
        raise AssertionError("selected payment misses q threshold")
    owner = [None] * cell["m"]
    owner[cell["x"]] = 0
    owner[cell["y"]] = 1 if source == 2 else 2
    for good in active:
        owner[good] = source
    for good in payment:
        owner[good] = 3
    owner = tuple(owner)
    if not numeric_efx(values, owner):
        raise AssertionError("two-safe-bundle allocation is not EFX")
    rival = numeric_utilities(values, owner)
    order = (0, 2, 1, 3)
    if tuple(rival[agent] for agent in order) <= tuple(own[agent] for agent in order):
        raise AssertionError("two-safe-bundle allocation is not lex-improving")
    return {
        "label": label,
        "branch": branch,
        "source": ("p", "r", "s", "q")[source],
        "active_bundle": [cell["goods"][good] for good in active],
        "payment_bundle": [cell["goods"][good] for good in payment],
        "q_slack": slack,
        "rival_utilities": list(rival),
    }


def load_profiles(session_path, profile_paths):
    session = json.loads(session_path.read_text())
    profiles = [
        (
            f"cegar_iteration_{record['iteration']}",
            tuple(tuple(row) for row in record["values"]),
        )
        for record in session["trace"]
    ]
    for path in profile_paths:
        payload = json.loads(path.read_text())
        profiles.append((path.stem, tuple(tuple(row) for row in payload["values"])))
    return profiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--profile", type=Path, action="append", default=[])
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    records = [
        audit_profile(values, label, sizes)
        for label, values in load_profiles(args.session, args.profile)
    ]
    result = {
        "schema": SCHEMA,
        "status": "ALL_PROFILES_PASS_RESERVOIR_EXCHANGE",
        "packet_sizes": list(sizes),
        "profile_count": len(records),
        "branch_counts": {
            branch: sum(record["branch"] == branch for record in records)
            for branch in sorted({record["branch"] for record in records})
        },
        "profiles": records,
        "claim_boundary": "constructive replay only; the cap-free result is proved analytically",
        "provenance": {
            "script": "tracks/parkability/audit_alternating_reservoir_exchange.py",
            "script_sha256": sha256(Path(__file__).resolve()),
            "session": {"path": str(args.session), "sha256": sha256(args.session)},
            "profiles": [
                {"path": str(path), "sha256": sha256(path)} for path in args.profile
            ],
        },
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps({key: result[key] for key in ("status", "profile_count", "branch_counts")}, indent=2))


if __name__ == "__main__":
    main()
