#!/usr/bin/env python3
"""Replay the dual-reservoir extension-or-handoff trichotomy."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .decide_alternating_two_safe_bundle_gate import numeric_desired, numeric_safe
    from .run_alternating_variable_packet_rooted_cegar import (
        make_cell,
        numeric_efx,
        numeric_utilities,
    )
except ImportError:
    from decide_alternating_two_safe_bundle_gate import numeric_desired, numeric_safe
    from run_alternating_variable_packet_rooted_cegar import (
        make_cell,
        numeric_efx,
        numeric_utilities,
    )


SCHEMA = "alternating-dual-reservoir-trichotomy-audit-v1"
AGENTS = ("p", "r", "s", "q")
ORDER = (0, 2, 3, 1)


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


def same_offer_pair(values, cell):
    own = numeric_utilities(values, cell["base_owner"])
    offer = cell["base_bundles"][1] + (cell["floater"],)
    unavailable = {cell["x"], cell["y"]}
    for active in powerset(offer):
        if not numeric_desired(values, own, 0, active):
            continue
        available = tuple(
            good
            for good in range(cell["m"])
            if good not in unavailable and good not in active
        )
        for payment in powerset(available):
            if not numeric_safe(values, own, payment):
                continue
            if sum(values[1][good] for good in payment) >= threshold(values, 1, active):
                return active, payment
    return None


def select_pair(values, cell):
    tr, br, _tq, _bq = cell["packets"]
    selected = tr + (cell["floater"],)
    reservoir = cell["base_bundles"][3] + br
    own = numeric_utilities(values, cell["base_owner"])
    if not numeric_desired(values, own, 0, selected):
        raise AssertionError("selected T_r+f block is not desired by p")
    forbidden_sources = tuple(
        source
        for source in (1, 2)
        if any(
            numeric_desired(values, own, source, candidate)
            for candidate in powerset(reservoir)
        )
    )
    if forbidden_sources:
        raise AssertionError(f"compatible-family absence failed: {forbidden_sources}")

    target = threshold(values, 1, selected)
    reservoir_value = sum(values[1][good] for good in reservoir)
    if reservoir_value < target:
        source, active = next(
            (source, active)
            for source, active in desired_subsets(values, own, reservoir)
            if source in (0, 3)
        )
        return "low_reservoir_reversal", source, active, selected

    payment = list(reservoir)
    changed = True
    while changed:
        changed = False
        for good in tuple(payment):
            remainder = tuple(item for item in payment if item != good)
            if sum(values[1][item] for item in remainder) >= target:
                payment.remove(good)
                changed = True
                break
    payment = tuple(payment)
    if numeric_safe(values, own, payment):
        return "same_offer_extension", 0, selected, payment

    unsafe_remainder = next(
        tuple(good for good in payment if good != removed)
        for removed in payment
        if any(
            sum(values[observer][good] for good in payment if good != removed)
            > own[observer]
            for observer in range(4)
        )
    )
    source, active = next(
        (source, active)
        for source, active in desired_subsets(values, own, unsafe_remainder)
        if source in (0, 3)
    )
    return "unsafe_threshold_reversal", source, active, selected


def audit_profile(values, label, sizes):
    cell = make_cell(sizes)
    if any(entry <= 0 for row in values for entry in row):
        raise AssertionError("profile is not strictly positive")
    own = numeric_utilities(values, cell["base_owner"])
    branch, source, active, payment = select_pair(values, cell)
    if set(active).intersection(payment):
        raise AssertionError("active and payment bundles overlap")
    if not numeric_desired(values, own, source, active):
        raise AssertionError("active bundle is not desired by its source")
    if not numeric_safe(values, own, payment):
        raise AssertionError("payment bundle is not common-safe")
    slack = sum(values[1][good] for good in payment) - threshold(values, 1, active)
    if slack < 0:
        raise AssertionError("payment misses r's EFX threshold")

    owner = [None] * cell["m"]
    owner[cell["y"]] = 2
    if source == 3:
        mode = "anchored_q_handoff"
        owner[cell["x"]] = 0
        for good in active:
            owner[good] = 3
    elif set(active).issubset(set(cell["base_bundles"][1] + (cell["floater"],))):
        mode = "same_offer_promotion"
        owner[cell["x"]] = 3
        for good in active:
            owner[good] = 0
    else:
        mode = "opposite_reservoir_promotion"
        owner[cell["x"]] = 3
        for good in active:
            owner[good] = 0
    for good in payment:
        owner[good] = 1
    owner = tuple(owner)
    if not numeric_efx(values, owner):
        raise AssertionError("constructed allocation is not EFX")
    rival = numeric_utilities(values, owner)
    if tuple(rival[agent] for agent in ORDER) <= tuple(own[agent] for agent in ORDER):
        raise AssertionError("constructed allocation is not lex-improving")
    alternate = same_offer_pair(values, cell)
    return {
        "label": label,
        "branch": branch,
        "mode": mode,
        "source": AGENTS[source],
        "active_bundle": [cell["goods"][good] for good in active],
        "payment_bundle": [cell["goods"][good] for good in payment],
        "r_slack": slack,
        "rival_utilities": list(rival),
        "same_offer_pair": None
        if alternate is None
        else {
            "active_bundle": [cell["goods"][good] for good in alternate[0]],
            "payment_bundle": [cell["goods"][good] for good in alternate[1]],
        },
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
        "status": "ALL_PROFILES_PASS_DUAL_RESERVOIR_TRICHOTOMY",
        "packet_sizes": list(sizes),
        "profile_count": len(records),
        "branch_counts": {
            branch: sum(record["branch"] == branch for record in records)
            for branch in sorted({record["branch"] for record in records})
        },
        "mode_counts": {
            mode: sum(record["mode"] == mode for record in records)
            for mode in sorted({record["mode"] for record in records})
        },
        "profiles_with_same_offer_pair": sum(
            record["same_offer_pair"] is not None for record in records
        ),
        "profiles": records,
        "claim_boundary": (
            "constructive replay only; the cap-free trichotomy is analytic, "
            "while elimination of opposite-reservoir p-promotion remains open"
        ),
        "provenance": {
            "script": "tracks/parkability/audit_alternating_dual_reservoir_trichotomy.py",
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
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "profile_count",
                    "branch_counts",
                    "mode_counts",
                    "profiles_with_same_offer_pair",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
