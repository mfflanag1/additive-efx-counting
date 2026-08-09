#!/usr/bin/env python3
"""Replay the boosted anchored handoff on frozen adversarial profiles."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .audit_alternating_dual_reservoir_trichotomy import (
        load_profiles,
        threshold,
    )
    from .decide_alternating_two_safe_bundle_gate import numeric_desired
    from .run_alternating_variable_packet_rooted_cegar import (
        make_cell,
        numeric_efx,
        numeric_utilities,
    )
except ImportError:
    from audit_alternating_dual_reservoir_trichotomy import (
        load_profiles,
        threshold,
    )
    from decide_alternating_two_safe_bundle_gate import numeric_desired
    from run_alternating_variable_packet_rooted_cegar import (
        make_cell,
        numeric_efx,
        numeric_utilities,
    )


SCHEMA = "alternating-boosted-handoff-profile-audit-v1"
ORDER = (0, 2, 3, 1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def powerset(pool):
    for size in range(1, len(pool) + 1):
        yield from itertools.combinations(pool, size)


def find_handoff(values, cell):
    own = numeric_utilities(values, cell["base_owner"])
    residual = tuple(
        good for good in range(cell["m"])
        if good not in (cell["x"], cell["y"])
    )
    subsets = tuple(powerset(residual))
    for active in subsets:
        if not numeric_desired(values, own, 2, active):
            continue
        active_s = sum(values[2][good] for good in active)
        for payment in subsets:
            if set(active).intersection(payment):
                continue
            if sum(values[3][good] for good in payment) < threshold(values, 3, active):
                continue
            if threshold(values, 0, payment) > own[0]:
                continue
            if threshold(values, 1, payment) > values[1][cell["y"]]:
                continue
            if threshold(values, 2, payment) > active_s:
                continue
            owner = [None] * cell["m"]
            owner[cell["x"]] = 0
            owner[cell["y"]] = 1
            for good in active:
                owner[good] = 2
            for good in payment:
                owner[good] = 3
            owner = tuple(owner)
            if not numeric_efx(values, owner):
                raise AssertionError("boosted inequalities did not construct EFX")
            utilities = numeric_utilities(values, owner)
            if tuple(utilities[a] for a in ORDER) <= tuple(own[a] for a in ORDER):
                raise AssertionError("boosted handoff did not improve lexicographically")
            return active, payment, utilities
    raise AssertionError("profile has no boosted handoff")


def audit(session_path: Path, profile_paths, sizes):
    cell = make_cell(sizes)
    profiles = load_profiles(session_path, profile_paths[:6])
    for path in profile_paths[6:]:
        payload = json.loads(path.read_text())
        profiles.append((path.stem, tuple(tuple(row) for row in payload["values"])))
    records = []
    for label, values in profiles:
        active, payment, utilities = find_handoff(values, cell)
        records.append(
            {
                "label": label,
                "s_bundle": [cell["goods"][good] for good in active],
                "q_bundle": [cell["goods"][good] for good in payment],
                "utilities": list(utilities),
            }
        )
    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "ALL_PROFILES_HAVE_BOOSTED_HANDOFF",
        "packet_sizes": list(sizes),
        "profile_count": len(records),
        "profiles": records,
        "claim_boundary": (
            "constructive replay only; cap-free existence remains the intersecting "
            "r-source wall in ALTERNATING_EXTENSION_OR_HANDOFF_REDUCTION.md"
        ),
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
            "session": {"path": str(session_path), "sha256": sha256(session_path)},
            "profiles": [
                {"path": str(path), "sha256": sha256(path)} for path in profile_paths
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--profile", type=Path, action="append", default=[])
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(
        args.session,
        args.profile,
        tuple(int(part) for part in args.sizes.split(",")),
    )
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps({key: result[key] for key in ("status", "profile_count")}, indent=2))


if __name__ == "__main__":
    main()
