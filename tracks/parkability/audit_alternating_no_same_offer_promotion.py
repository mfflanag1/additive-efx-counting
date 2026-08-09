#!/usr/bin/env python3
"""Audit a profile with no same-offer promotion but an anchored repair."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_alternating_anchored_or_promoted_split_cegar import (
        find_restricted_rivals,
    )
    from .run_alternating_split_packet_cegar import (
        BASE_BUNDLES,
        BASE_OWNER,
        FLOATER,
        GOODS,
        M,
        N,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )
    from .decide_alternating_strict_bridge_dominance import OUTSIDE_OWNER
except ImportError:
    from run_alternating_anchored_or_promoted_split_cegar import (
        find_restricted_rivals,
    )
    from run_alternating_split_packet_cegar import (
        BASE_BUNDLES,
        BASE_OWNER,
        FLOATER,
        GOODS,
        M,
        N,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )
    from decide_alternating_strict_bridge_dominance import OUTSIDE_OWNER


SCHEMA = "alternating-no-same-offer-promotion-audit-v1"
ORDER = (0, 2, 3, 1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def named_bundles(owner):
    return [
        [GOODS[good] for good, assigned in enumerate(owner) if assigned == agent]
        for agent in range(4)
    ]


def promotion_search(values, timeout_seconds=120):
    owner = tuple(z3.Int(f"promotion_owner_{good}") for good in range(M))
    solver = z3.SolverFor("QF_LIA")
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(*(z3.And(variable >= 0, variable <= N) for variable in owner))
    base = numeric_utilities(values, BASE_OWNER)
    utilities = tuple(
        z3.Sum(
            *(z3.If(owner[good] == agent, values[agent][good], 0) for good in range(M))
        )
        for agent in range(N)
    )
    targets = tuple(
        tuple(
            z3.Sum(
                *(z3.If(owner[good] == target, values[observer][good], 0) for good in range(M))
            )
            for target in range(N)
        )
        for observer in range(N)
    )
    offer = BASE_BUNDLES[1] + (FLOATER,)
    solver.add(*(owner[good] != 0 for good in range(M) if good not in offer))
    solver.add(utilities[0] > base[0])
    solver.add(
        *(
            z3.Implies(
                owner[removed] == 0,
                targets[observer][0] - values[observer][removed] <= base[observer],
            )
            for observer in range(N)
            for removed in offer
        )
    )
    solver.add(
        *(
            z3.Implies(
                owner[removed] == target,
                utilities[observer]
                >= targets[observer][target] - values[observer][removed],
            )
            for observer in range(N)
            for target in range(N)
            for removed in range(M)
        )
    )
    checked = solver.check()
    if checked == z3.sat:
        model = solver.model()
        concrete = tuple(
            None if model.eval(variable).as_long() == N else model.eval(variable).as_long()
            for variable in owner
        )
        return "sat", concrete, None
    if checked == z3.unsat:
        return "unsat", None, None
    return "unknown", None, solver.reason_unknown()


def audit(profile_path: Path) -> dict:
    payload = json.loads(profile_path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    solver, symbolic, _ = structural_solver()
    solver.add(
        *(
            symbolic[agent][good] * sum(values[agent]) == values[agent][good]
            for agent in range(4)
            for good in range(11)
        )
    )
    if solver.check() != z3.sat:
        raise AssertionError("profile is outside the structural cell")

    promotion_status, promotion, promotion_reason = promotion_search(values)
    if promotion_status != "unsat" or promotion is not None:
        raise AssertionError(("same-offer promotion survived", promotion_status))
    anchor_status, anchors, anchor_utilities, _, anchor_reason = find_restricted_rivals(
        values, ORDER, 120, 1, "none", "root-only"
    )
    if anchor_status != "sat" or not anchors:
        raise AssertionError(("anchored repair missing", anchor_status))
    outside = tuple(OUTSIDE_OWNER)
    if not numeric_efx(values, outside):
        raise AssertionError("outside-reservoir allocation is not EFX")
    base = numeric_utilities(values, BASE_OWNER)
    outside_utility = numeric_utilities(values, outside)
    if tuple(outside_utility[a] for a in ORDER) <= tuple(base[a] for a in ORDER):
        raise AssertionError("outside-reservoir allocation does not improve")

    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "NO_SAME_OFFER_PROMOTION_WITH_ANCHORED_REPAIR",
        "claim_boundary": {
            "proved_exactly": (
                "this eleven-good profile has no EFX lexicographic escape that "
                "promotes p to any desired subset of X_r+f"
            ),
            "also_verified": (
                "an anchored EFX improvement and an opposite-reservoir p-promotion exist"
            ),
            "not_refuted": (
                "the anchored-or-any-same-offer dichotomy, because its anchored branch holds"
            ),
        },
        "base_utilities": list(base),
        "promotion_search_status": promotion_status,
        "promotion_search_reason_unknown": promotion_reason,
        "anchor_search_status": anchor_status,
        "anchor_search_reason_unknown": anchor_reason,
        "anchor_owner": list(anchors[0]),
        "anchor_bundles": named_bundles(anchors[0]),
        "anchor_utilities": list(anchor_utilities[0]),
        "outside_owner": list(outside),
        "outside_bundles": named_bundles(outside),
        "outside_utilities": list(outside_utility),
        "values": [list(row) for row in values],
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
            "profile": str(profile_path),
            "profile_sha256": sha256(profile_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.profile)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps({key: result[key] for key in ("status", "promotion_search_status", "anchor_search_status")}, indent=2))


if __name__ == "__main__":
    main()
