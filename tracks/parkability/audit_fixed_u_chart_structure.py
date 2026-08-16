#!/usr/bin/env python3
"""Audit the chart-level structure behind the tame-covering-menu question.

Records, in exact rational arithmetic and without a solver:

* that the rank-three wall premise `v_d(W) < tail_d(A)` holds on every banked
  profile, which is what Lemma D rests on;
* that Lemma D's disjunction -- every EFX allocation gives `d` a role outside
  `W` or separates `a0` from `a1` -- holds across the banked whole-role menu;
* the two refuted constructive routes, base blocks and supplier homes, with
  their EFX counts, edge counts and the failing observer/target pairs;
* which roles are ever wild, and which roles are ever forced to be split.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .decide_physical_minimum_countermodel_four_edge import support_supplier
from .run_identity_aware_witness_side_batch import distinct_profiles, slack
from .run_fixed_u_full_packet_terminal_cegar import (
    BASE,
    GOODS,
    OWNERS,
    PACKETS,
    SUPPORT_STATE,
)


def bundles_of(role_owner):
    return {
        owner: [role for role in GOODS if role_owner[role] == owner]
        for owner in OWNERS
    }


def edges_of(role_owner):
    supplier = support_supplier()
    return sorted({
        (supplier[role], owner)
        for role, owner in role_owner.items()
        if supplier[role] != owner
    })


def efx_failures(role_owner, totals, minima):
    """Every (observer, target) pair whose EFX comparison breaks."""
    bundles = bundles_of(role_owner)
    failures = []
    for observer in OWNERS:
        own = sum((totals[observer][r] for r in bundles[observer]), Fraction())
        for target in OWNERS:
            if target == observer or not bundles[target]:
                continue
            gross = sum((totals[observer][r] for r in bundles[target]), Fraction())
            least = min(minima[observer][r] for r in bundles[target])
            if own < gross - least:
                failures.append((observer, target))
    return failures


def tail(totals, minima, observer, roles):
    roles = tuple(roles)
    return (
        sum((totals[observer][r] for r in roles), Fraction())
        - min(minima[observer][r] for r in roles)
    )


def wall_premise_holds(totals, minima):
    """The rank-three wall: v_d(W) < tail_d(A)."""
    d_floor = sum((totals["d"][r] for r in PACKETS["W"]), Fraction())
    return d_floor < tail(totals, minima, "d", PACKETS["A"])


def lemma_d_disjunction(role_owner):
    """d receives a role outside W, or a0 and a1 sit in different bundles."""
    wide = set(PACKETS["W"])
    d_bundle = {role for role in GOODS if role_owner[role] == "d"}
    return (not d_bundle <= wide) or (role_owner["a0"] != role_owner["a1"])


def base_block_allocation(host):
    role_owner = {}
    for owner in OWNERS:
        for role in BASE[owner]:
            role_owner[role] = owner
    for role in BASE["charity"]:
        role_owner[role] = host
    return role_owner


def supplier_home_allocation(host):
    role_owner = {}
    for owner, roles in SUPPORT_STATE.items():
        for role in roles:
            role_owner[role] = host if owner == "charity" else owner
    return role_owner


def survey_construction(builder, profiles, edge_cap):
    records = []
    for host in OWNERS:
        role_owner = builder(host)
        edges = edges_of(role_owner)
        failures = [efx_failures(role_owner, p["totals"], p["minima"])
                    for p in profiles]
        pairs = Counter()
        for failure in failures:
            pairs.update(failure)
        records.append({
            "charity_host": host,
            "edge_count": len(edges),
            "within_edge_cap": len(edges) <= edge_cap,
            "edges": [list(e) for e in edges],
            "efx_profile_count": sum(1 for f in failures if not f),
            "profiles": len(profiles),
            "failing_pairs": {
                f"{o}->{t}": count
                for (o, t), count in sorted(pairs.items(), key=lambda x: -x[1])
            },
        })
    return records


def run(trace_paths, menu_path, output_path, edge_cap):
    profiles = distinct_profiles(trace_paths)
    menu = json.loads(menu_path.read_text())

    wall = [wall_premise_holds(p["totals"], p["minima"]) for p in profiles]
    lemma_d = [lemma_d_disjunction(entry) for entry in menu]

    separates = sum(1 for e in menu if e["a0"] != e["a1"])
    outside_w = sum(
        1 for e in menu
        if not {r for r in GOODS if e[r] == "d"} <= set(PACKETS["W"])
    )
    a_to_d = sum(1 for e in menu if "d" in (e["a0"], e["a1"]))

    wildness = Counter()
    for profile in profiles:
        for role in GOODS:
            if slack(profile["totals"], profile["minima"], role) >= 3:
                wildness[role] += 1

    result = {
        "schema": "fixed-u-chart-structure-audit-v1",
        "traces": [
            {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in trace_paths
        ],
        "menu_source": str(menu_path),
        "menu_source_sha256": hashlib.sha256(menu_path.read_bytes()).hexdigest(),
        "profiles_examined": len(profiles),
        "menu_size": len(menu),
        "wall_premise_holds_on": sum(wall),
        "wall_premise_violated_on": sum(1 for w in wall if not w),
        "lemma_d_satisfied_by": sum(lemma_d),
        "lemma_d_violated_by": sum(1 for x in lemma_d if not x),
        "lemma_d_breakdown": {
            "separates_a0_from_a1": separates,
            "gives_d_a_role_outside_W": outside_w,
            "of_which_gives_d_a_role_of_A": a_to_d,
        },
        "refutation_base_blocks": survey_construction(
            base_block_allocation, profiles, edge_cap
        ),
        "refutation_supplier_homes": survey_construction(
            supplier_home_allocation, profiles, edge_cap
        ),
        "role_wildness_counts": {role: wildness[role] for role in GOODS},
        "distinct_edge_sets_in_menu": len({
            tuple(edges_of(entry)) for entry in menu
        }),
        "menu_edge_count_distribution": dict(sorted(
            Counter(len(edges_of(entry)) for entry in menu).items()
        )),
        "claim_boundary": (
            "Closed-form exact arithmetic over the banked profiles and the "
            "banked whole-role menu.  The wall premise and Lemma D are "
            "verified, not assumed.  The two refutations are statements about "
            "these two specific constructions on this population; they do not "
            "show that no constructive rule exists, only that the two natural "
            "ones fail."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, action="append", required=True)
    parser.add_argument("--menu", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    args = parser.parse_args()
    result = run(tuple(args.trace), args.menu, args.output, args.edge_cap)
    print(json.dumps({
        "profiles_examined": result["profiles_examined"],
        "wall_premise_violated_on": result["wall_premise_violated_on"],
        "lemma_d_violated_by": result["lemma_d_violated_by"],
        "lemma_d_breakdown": result["lemma_d_breakdown"],
        "base_block_efx_counts": [
            r["efx_profile_count"] for r in result["refutation_base_blocks"]
        ],
        "supplier_home_efx_counts": [
            r["efx_profile_count"] for r in result["refutation_supplier_homes"]
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
