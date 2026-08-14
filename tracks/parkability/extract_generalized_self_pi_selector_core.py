#!/usr/bin/env python3
"""Extract a deletion-minimal self-PI exclusion core for the named selector."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

from .decide_two_survivor_named_topology_family import (
    R2_TOPOLOGIES, R3_TOPOLOGIES, allocations_supported_by, canonical,
)
from .run_fixed_u_full_packet_terminal_cegar import (
    BASE, OWNERS, allocation_formula,
)
from .run_fixed_u_rank_three_relation_cegar import (
    base_response, build_rank_three_master,
)


def labelled_self_exclusions(value):
    rows = []
    charity = tuple(BASE["charity"])
    charity_set = set(charity)
    for owner in OWNERS:
        universe = (*tuple(BASE[owner]), *charity)
        for size in range(1, len(universe) + 1):
            for goods in itertools.combinations(universe, size):
                if not set(goods) & charity_set:
                    continue
                label = z3.Bool("no_self_pi_" + owner + "_" + "_".join(goods))
                rows.append((label, owner, goods, z3.Not(base_response(value, owner, goods))))
    return rows


def build(form_index):
    solver, value = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    seen = set()
    topologies = R2_TOPOLOGIES if form_index == 0 else R3_TOPOLOGIES
    for topology in topologies:
        for allocation in allocations_supported_by(topology):
            key = canonical(allocation)
            if key in seen:
                continue
            seen.add(key)
            solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    rows = labelled_self_exclusions(value)
    for label, _, _, constraint in rows:
        solver.add(z3.Implies(label, constraint))
    return solver, rows, len(seen)


def run(output, form_index, timeout_seconds, random_seed):
    solver, rows, allocation_count = build(form_index)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    assumptions = [row[0] for row in rows]
    checked = solver.check(*assumptions)
    if checked != z3.unsat:
        raise AssertionError(("full assumption set", checked, solver.reason_unknown()))
    raw_core = set(solver.unsat_core())
    active = [row for row in rows if row[0] in raw_core]

    # Deterministic deletion minimization; UNKNOWN retains the assumption.
    changed = True
    while changed:
        changed = False
        for row in tuple(active):
            trial = [candidate[0] for candidate in active if candidate is not row]
            status = solver.check(*trial)
            if status == z3.unsat:
                active.remove(row)
                changed = True

    final_status = solver.check(*(row[0] for row in active))
    deletion_statuses = []
    for row in active:
        trial = [candidate[0] for candidate in active if candidate is not row]
        deletion_statuses.append({
            "removed": str(row[0]),
            "status": str(solver.check(*trial)),
        })
    result = {
        "schema": "generalized-self-pi-selector-core-v1",
        "status": "DELETION_MINIMAL_SELF_PI_SELECTOR_CORE",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "allocation_count": allocation_count,
        "declared_self_exclusion_count": len(rows),
        "raw_core_count": len(raw_core),
        "minimal_core_count": len(active),
        "minimal_core": [
            {"label": str(label), "owner": owner, "desired_core": list(goods)}
            for label, owner, goods, _ in active
        ],
        "final_status": str(final_status),
        "single_deletion_statuses": deletion_statuses,
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Deletion-minimal generalized self-PI exclusions sufficient for "
            "the bounded named-selector theorem. This core is an analytic-lemma "
            "candidate, not a cap-free proof."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(args.output, args.form_index, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "form_index": result["form_index"],
        "raw_core_count": result["raw_core_count"],
        "minimal_core_count": result["minimal_core_count"],
        "minimal_core": result["minimal_core"],
    }, indent=2))


if __name__ == "__main__":
    main()
