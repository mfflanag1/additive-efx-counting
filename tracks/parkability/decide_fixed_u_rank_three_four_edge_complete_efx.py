#!/usr/bin/env python3
"""Decide the four-provenance-edge complete-EFX gate in the 12-atom cell.

This is deliberately a direct decision encoding rather than another CEGAR
sample.  It conjoins the negation of complete EFX for every allocation whose
active base-provenance transfer graph has at most four directed edges.
Consequently SAT gives an exact bounded-atom no-go profile and UNSAT proves
the four-edge statement for the declared atomization.  Neither verdict alone
is a cap-free theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .run_fixed_u_full_packet_terminal_cegar import (
        BASE,
        GOODS,
        OWNERS,
        RECIPIENTS,
        SUPPORT_STATE,
        allocation_formula,
        fractions,
    )
except ImportError:  # Permit direct replay from the script path.
    from run_fixed_u_full_packet_terminal_cegar import (
        BASE,
        GOODS,
        OWNERS,
        RECIPIENTS,
        SUPPORT_STATE,
        allocation_formula,
        fractions,
    )


def serialize_values(values):
    return {
        owner: {good: str(amount) for good, amount in row.items()}
        for owner, row in values.items()
    }


def provenance_holder(provenance):
    return {
        good: supplier
        for supplier, goods in provenance.items()
        for good in goods
    }


def allocations_with_at_most_edges(edge_bound=4, provenance=SUPPORT_STATE):
    supplier = provenance_holder(provenance)
    possible_edges = tuple(
        (source, target)
        for source in provenance
        for target in OWNERS
        if source != target
    )
    for size in range(edge_bound + 1):
        for selected_tuple in itertools.combinations(possible_edges, size):
            selected = set(selected_tuple)
            choices = []
            feasible = True
            for good in GOODS:
                source = supplier[good]
                outgoing = tuple(
                    target for edge_source, target in selected_tuple
                    if edge_source == source
                )
                targets = outgoing if source == "charity" else (source, *outgoing)
                if not targets:
                    feasible = False
                    break
                choices.append(targets)
            if not feasible:
                continue
            for targets in itertools.product(*choices):
                actual = {
                    (supplier[good], target)
                    for good, target in zip(GOODS, targets)
                    if supplier[good] != target
                }
                if actual != selected:
                    continue
                allocation = {recipient: [] for recipient in RECIPIENTS}
                for good, target in zip(GOODS, targets):
                    allocation[target].append(good)
                yield allocation


def run(output: Path, timeout_seconds: int, edge_origin: str, edge_bound: int,
        threads: int, random_seed: int, corrected_exact_relation=False,
        owner_cycle_form_index=None, functional_only=False,
        ordinary_pi_free=False, generalized_self_pi_free=False):
    loaded_source_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    try:
        from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    except ImportError:
        from run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    solver, value = build_rank_three_master(
        exclude_self_responses=corrected_exact_relation,
        required_owner_cycle_form=corrected_exact_relation,
        exact_owner_cycle_response_relation=corrected_exact_relation,
        owner_cycle_form_index=owner_cycle_form_index,
    )
    if ordinary_pi_free:
        try:
            from .run_full_capture_rank_three_cegar import ordinary_pi_free_constraints
        except ImportError:
            from run_full_capture_rank_three_cegar import ordinary_pi_free_constraints
        solver.add(*ordinary_pi_free_constraints(value, BASE))
    if generalized_self_pi_free:
        try:
            from .run_full_capture_rank_three_cegar import generalized_self_pi_free_constraints
        except ImportError:
            from run_full_capture_rank_three_cegar import generalized_self_pi_free_constraints
        solver.add(*generalized_self_pi_free_constraints(value, BASE))
    solver.set(timeout=timeout_seconds * 1000)
    solver.set(threads=threads, random_seed=random_seed)
    started = time.monotonic()
    allocation_count = 0
    empty_owner_omissions = 0
    provenance = SUPPORT_STATE if edge_origin == "support" else BASE
    for allocation in allocations_with_at_most_edges(edge_bound, provenance):
        if any(not allocation[owner] for owner in OWNERS):
            empty_owner_omissions += 1
            continue
        if functional_only:
            supplier = provenance_holder(provenance)
            edges = {
                (supplier[good], recipient)
                for recipient, goods in allocation.items()
                if recipient != "charity"
                for good in goods if supplier[good] != recipient
            }
            if len({source for source, _ in edges}) != len(edges):
                continue
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
        allocation_count += 1

    build_seconds = time.monotonic() - started
    status = solver.check()
    result = {
        "schema": "fixed-u-rank-three-bounded-edge-complete-efx-decision-v1",
        "status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "timeout_seconds": timeout_seconds,
        "threads": threads,
        "random_seed": random_seed,
        "corrected_exact_relation": corrected_exact_relation,
        "owner_cycle_form_index": owner_cycle_form_index,
        "functional_only": functional_only,
        "ordinary_pi_free": ordinary_pi_free,
        "generalized_self_pi_free": generalized_self_pi_free,
        "allocation_count": allocation_count,
        "empty_owner_allocations_omitted": empty_owner_omissions,
        "empty_owner_omission_justification": (
            "with strictly positive values, an empty owner can be EFX only if every "
            "other owner bundle is a singleton; three nonempty owner bundles cannot "
            "hold all twelve goods"
        ),
        "edge_bound": edge_bound,
        "edge_origin": edge_origin,
        "edge_definition": (
            "number of distinct directed selected-provenance-supplier to final-owner "
            "pairs carrying at least one good; retained goods create no edge"
        ),
        "build_seconds": build_seconds,
        "source_sha256": loaded_source_sha256,
        "dependency_sha256": {
            "run_fixed_u_rank_three_relation_cegar.py": hashlib.sha256(
                (Path(__file__).parent / "run_fixed_u_rank_three_relation_cegar.py").read_bytes()
            ).hexdigest(),
            "run_fixed_u_full_packet_terminal_cegar.py": hashlib.sha256(
                (Path(__file__).parent / "run_fixed_u_full_packet_terminal_cegar.py").read_bytes()
            ).hexdigest(),
        },
        "claim_boundary": (
            "direct exhaustive decision for the declared positive rational "
            "twelve-atom root-facing rank-three packet cell"
            + (" restricted to functional transfer graphs" if functional_only else "")
            + (" with complete ordinary PI-freeness" if ordinary_pi_free else "")
            + (" excluding every generalized self-PI edge"
               if generalized_self_pi_free else "")
            + ". UNSAT is a bounded-"
            "atom theorem, not a cap-free theorem. SAT is a bounded four-edge "
            "no-go profile, but is not a full recurrence countermodel because "
            "signed-record reachability and all Hall resets remain unencoded."
        ),
    }
    if status == z3.sat:
        result["values"] = serialize_values(fractions(solver.model(), value))
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    result["solve_seconds"] = time.monotonic() - started - build_seconds
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--edge-origin", choices=("base", "support"), default="support")
    parser.add_argument("--edge-bound", type=int, default=4)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--corrected-exact-relation", action="store_true")
    parser.add_argument("--owner-cycle-form-index", type=int, choices=range(4))
    parser.add_argument("--functional-only", action="store_true")
    parser.add_argument("--ordinary-pi-free", action="store_true")
    parser.add_argument("--generalized-self-pi-free", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output, args.timeout_seconds, args.edge_origin, args.edge_bound,
        args.threads, args.random_seed, args.corrected_exact_relation,
        args.owner_cycle_form_index, args.functional_only,
        args.ordinary_pi_free,
        args.generalized_self_pi_free,
    )
    print(json.dumps({
        "status": result["status"],
        "allocation_count": result["allocation_count"],
        "build_seconds": result["build_seconds"],
        "solve_seconds": result["solve_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
