#!/usr/bin/env python3
"""Census of the minimum split count over the banked adversarial population.

Theorem A of the slack-two note says a complete four-support-edge EFX
allocation that splits no role is EFX in *every* physical realization of its
totals/minima profile, at every role cardinality and every witness identity.
So the profiles admitting a zero-split allocation are closed outright, with no
slack hypothesis at all.

This driver measures how far that reaches: for each distinct banked profile it
finds the least number of roles any four-edge complete EFX allocation must
split, in the canonical two-good realization.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import (
    build_decision,
    support_supplier,
)
from .run_identity_aware_witness_side_batch import distinct_profiles, slack
from .run_identity_aware_witness_side_cegar import (
    audit_allocation,
    concrete_values,
    role_layout,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def whole_role_minimum(minima, observer, roles):
    """min over whole roles of the role minimum, the exact bundle minimum."""
    values = [minima[observer][role] for role in roles]
    return min(values) if values else None


def audit_whole_role_efx(allocation, totals, minima, role_goods, edge_cap):
    """Re-audit a zero-split allocation directly in the (T, M) abstraction.

    For a bundle that is a union of whole roles, every realization gives
    v_i(B) = sum of T and min_x v_i(x) = min of M, whatever the cardinalities.
    Checking EFX in those terms is therefore a realization-free audit.
    """
    owner_roles = {}
    for owner, goods in allocation.items():
        roles = sorted({good.split(":", 1)[0] for good in goods})
        for role in roles:
            assert set(role_goods[role]) <= set(goods), (role, owner)
        owner_roles[owner] = roles
    placed = sorted(r for roles in owner_roles.values() for r in roles)
    assert placed == sorted(GOODS), placed

    supplier = support_supplier()
    edges = sorted({
        (supplier[role], owner)
        for owner, roles in owner_roles.items()
        for role in roles
        if supplier[role] != owner
    })
    assert len(edges) <= edge_cap, edges

    for observer in OWNERS:
        own = sum(
            (totals[observer][role] for role in owner_roles[observer]), Fraction()
        )
        for target in OWNERS:
            if target == observer or not owner_roles[target]:
                continue
            gross = sum(
                (totals[observer][role] for role in owner_roles[target]), Fraction()
            )
            least = whole_role_minimum(minima, observer, owner_roles[target])
            assert own >= gross - least, (observer, target)
    return owner_roles, edges


def least_split_count(totals, minima, edge_cap, timeout_seconds):
    role_goods, multi = role_layout(totals, minima)
    canonical = {(role, o): False for role in multi for o in OWNERS}
    physical = concrete_values(totals, minima, role_goods, canonical)
    for split_cap in range(0, len(multi) + 1):
        solver, assign, _, split, goods = build_decision(
            physical, role_goods, split_cap=split_cap, edge_cap=edge_cap
        )
        solver.set(timeout=timeout_seconds * 1000)
        status = solver.check()
        if status == z3.unknown:
            return None, "UNKNOWN", None, None
        if status != z3.sat:
            continue
        model = solver.model()
        allocation = {
            owner: [g for g in goods if z3.is_true(model.eval(assign[g, owner]))]
            for owner in OWNERS
        }
        audit_allocation(allocation, physical, edge_cap)
        split_roles = sorted(
            role for role, flag in split.items() if z3.is_true(model.eval(flag))
        )
        assert len(split_roles) <= split_cap
        owner_roles = None
        if split_cap == 0:
            owner_roles, _ = audit_whole_role_efx(
                allocation, totals, minima, role_goods, edge_cap
            )
        return split_cap, "sat", split_roles, owner_roles
    return None, "UNSAT_AT_EVERY_SPLIT_CAP", None, None


def run(trace_paths, output_path, edge_cap, timeout_seconds, limit):
    profiles = distinct_profiles(trace_paths)
    if limit is not None:
        profiles = profiles[:limit]
    records = []
    for index, profile in enumerate(profiles):
        totals, minima = profile["totals"], profile["minima"]
        count, status, split_roles, owner_roles = least_split_count(
            totals, minima, edge_cap, timeout_seconds
        )
        slacks = {role: slack(totals, minima, role) for role in GOODS}
        record = {
            "index": index,
            "source": profile["source"],
            "source_iteration": profile["iteration"],
            "status": status,
            "least_split_count": count,
            "split_roles": split_roles,
            "maximum_role_slack": str(max(slacks.values())),
            "slack_two_stratum": all(value <= 2 for value in slacks.values()),
            "closed_at_every_cardinality": count == 0,
        }
        if owner_roles is not None:
            record["whole_role_allocation"] = owner_roles
        records.append(record)
        print(index, profile["source"][:34], profile["iteration"], status,
              "splits", count, "maxslack", record["maximum_role_slack"], flush=True)

    result = {
        "schema": "whole-role-universality-census-v1",
        "traces": [
            {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in trace_paths
        ],
        "profiles_examined": len(records),
        "edge_cap": edge_cap,
        "least_split_count_tally": dict(
            Counter(str(r["least_split_count"]) for r in records)
        ),
        "closed_at_every_cardinality_count": sum(
            1 for r in records if r["closed_at_every_cardinality"]
        ),
        "closed_at_every_cardinality_above_slack_two": sum(
            1 for r in records
            if r["closed_at_every_cardinality"] and not r["slack_two_stratum"]
        ),
        "slack_two_stratum_count": sum(1 for r in records if r["slack_two_stratum"]),
        "records": records,
        "claim_boundary": (
            "A least_split_count of zero is a realization-free verdict: by "
            "Theorem A the exhibited whole-role allocation is EFX in every "
            "physical realization of the profile, at every cardinality and "
            "every witness identity, and it is re-audited here directly in the "
            "totals/minima abstraction.  A positive least_split_count is a "
            "statement about the canonical two-good realization only."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    result = run(tuple(args.trace), args.output, args.edge_cap,
                 args.timeout_seconds, args.limit)
    print(json.dumps({
        "profiles_examined": result["profiles_examined"],
        "least_split_count_tally": result["least_split_count_tally"],
        "closed_at_every_cardinality_count":
            result["closed_at_every_cardinality_count"],
        "closed_at_every_cardinality_above_slack_two":
            result["closed_at_every_cardinality_above_slack_two"],
    }, indent=2))


if __name__ == "__main__":
    main()
