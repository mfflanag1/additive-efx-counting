#!/usr/bin/env python3
"""Audit the nondegenerate refutation of the two-branch split-packet target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_anchored_or_promoted_split_cegar import find_restricted_rivals
    from .run_alternating_split_packet_cegar import (
        BASE_BUNDLES,
        BASE_OWNER,
        GOODS,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )
except ImportError:
    from run_alternating_anchored_or_promoted_split_cegar import find_restricted_rivals
    from run_alternating_split_packet_cegar import (
        BASE_BUNDLES,
        BASE_OWNER,
        GOODS,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )


SCHEMA = "alternating-anchored-or-promoted-refutation-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(values, agent: int, goods) -> int:
    return sum(values[agent][good] for good in goods)


def audit(profile_path: Path) -> dict:
    payload = json.loads(profile_path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    order = tuple(payload["agent_order"])
    rival = tuple(payload["unrestricted_rival"])
    own = numeric_utilities(values, BASE_OWNER)

    solver, symbolic, _ = structural_solver()
    solver.add(
        *(symbolic[agent][good] * sum(values[agent]) == values[agent][good]
          for agent in range(4) for good in range(11))
    )
    if solver.check() != z3.sat:
        raise AssertionError("profile is outside the exact structural cell")

    nondegenerate = []
    for row in values:
        sums = {
            sum(row[good] for good in range(11) if mask & (1 << good))
            for mask in range(1 << 11)
        }
        nondegenerate.append(len(sums) == 1 << 11)
    if nondegenerate != [True] * 4:
        raise AssertionError("profile is not subset-nondegenerate")

    status, restricted, _, _, reason = find_restricted_rivals(values, order, 60, 1)
    if status != "unsat" or restricted:
        raise AssertionError(("restricted target not refuted", status, reason))

    if not numeric_efx(values, rival):
        raise AssertionError("stored unrestricted rival is not EFX")
    rival_utility = numeric_utilities(values, rival)
    if tuple(rival_utility[agent] for agent in order) <= tuple(own[agent] for agent in order):
        raise AssertionError("stored unrestricted rival does not lexicographically improve")

    offer = BASE_BUNDLES[1] + (10,)
    desired_sets = []
    for size in range(1, len(offer) + 1):
        for candidate in itertools.combinations(offer, size):
            if value(values, 0, candidate) <= own[0]:
                continue
            if all(
                value(values, observer, tuple(good for good in candidate if good != removed))
                <= own[observer]
                for observer in range(4)
                for removed in candidate
            ):
                desired_sets.append(candidate)
    root_bundle = tuple(good for good, owner in enumerate(rival) if owner == order[0])
    if root_bundle not in desired_sets:
        raise AssertionError(("escape root is not an alternate desired set", root_bundle, desired_sets))

    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "NONDEGENERATE_CANONICAL_TWO_BRANCH_TARGET_REFUTED",
        "claim_boundary": {
            "refuted": "anchor the root or promote it to the one selected desired set in the exact eleven-good (p,q,s,r) cell",
            "surviving_repair": "allow promotion to any desired subset on the same champion offer",
            "not_refuted": "the any-desired repair, unrestricted alternating escape, two-large closure, or complete EFX",
        },
        "agent_order": list(order),
        "subset_nondegenerate_by_agent": nondegenerate,
        "restricted_search_status": status,
        "restricted_search_reason_unknown": reason,
        "base_utilities": list(own),
        "unrestricted_rival": list(rival),
        "unrestricted_rival_by_good": {
            GOODS[good]: None if owner is None else owner for good, owner in enumerate(rival)
        },
        "unrestricted_rival_utilities": list(rival_utility),
        "root_bundle": [GOODS[good] for good in root_bundle],
        "root_bundle_is_alternate_desired_set": True,
        "desired_sets_on_root_offer": [
            [GOODS[good] for good in candidate] for candidate in desired_sets
        ],
        "values": [list(row) for row in values],
        "provenance": {
            "audit_script": str(script.relative_to(script.parents[2])),
            "audit_script_sha256": sha256(script),
            "profile": str(profile_path),
            "profile_sha256": sha256(profile_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.profile)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered)


if __name__ == "__main__":
    main()
