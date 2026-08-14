#!/usr/bin/env python3
"""Exact generalized-PI CEGAR for the flexible named four-edge selector.

The master negates every complete EFX allocation in the selected unrestricted
packet topology menu.  Each SAT valuation is searched exhaustively for a
canonical generalized BCFF PI cycle.  A found cycle yields an exact symbolic
cut forbidding the conjunction of its champion relations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .decide_two_survivor_named_topology_family import (
        ALL_D_BILATERAL_TOPOLOGIES, R2_TOPOLOGIES, R3_TOPOLOGIES,
        ROOT_REASSEMBLY_TOPOLOGIES, allocations_supported_by, canonical,
    )
    from .find_generalized_pi_cycle import find_cycle
    from .run_fixed_u_full_packet_terminal_cegar import (
        BASE, OWNERS, allocation_formula, fractions,
    )
    from .run_fixed_u_rank_three_relation_cegar import (
        base_response, build_rank_three_master,
    )
    from .run_full_capture_rank_three_cegar import (
        generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
    )
except ImportError:
    from decide_two_survivor_named_topology_family import (
        ALL_D_BILATERAL_TOPOLOGIES, R2_TOPOLOGIES, R3_TOPOLOGIES,
        ROOT_REASSEMBLY_TOPOLOGIES, allocations_supported_by, canonical,
    )
    from find_generalized_pi_cycle import find_cycle
    from run_fixed_u_full_packet_terminal_cegar import (
        BASE, OWNERS, allocation_formula, fractions,
    )
    from run_fixed_u_rank_three_relation_cegar import (
        base_response, build_rank_three_master,
    )
    from run_full_capture_rank_three_cegar import (
        generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
    )


def cycle_signature(witness):
    # The symbolic cut depends only on the source/core family. Different
    # cyclic target labelings of the same closed disjoint cores induce the
    # identical conjunction of champion relations.
    return tuple(sorted(
        (edge["source"], tuple(sorted(edge["desired_core"])))
        for edge in witness["edges"]
    ))


def generalized_pi_cut(value, witness):
    """Block the exact champion conjunction supporting ``witness``.

    Incoming disjointness and release coverage depend only on the displayed
    goods and base allocation, so they need not be repeated symbolically.
    """
    relations = tuple(
        base_response(value, edge["source"], tuple(edge["desired_core"]))
        for edge in witness["edges"]
    )
    return z3.Not(z3.And(*relations))


def topology_menu(form_index, include_root_reassembly, include_all_d_bilateral):
    topologies = R2_TOPOLOGIES if form_index == 0 else R3_TOPOLOGIES
    if include_root_reassembly:
        topologies = (*topologies, *ROOT_REASSEMBLY_TOPOLOGIES)
    if include_all_d_bilateral:
        topologies = (*topologies, *ALL_D_BILATERAL_TOPOLOGIES)
    return topologies


def run(output, form_index, timeout_seconds, random_seed, maximum_iterations,
        include_root_reassembly=True, include_all_d_bilateral=True):
    solver, value = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    solver.add(*ordinary_pi_free_constraints(value, BASE))
    solver.add(*generalized_self_pi_free_constraints(value, BASE))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    seen_allocations = set()
    topologies = topology_menu(
        form_index, include_root_reassembly, include_all_d_bilateral,
    )
    for topology in topologies:
        for allocation in allocations_supported_by(topology):
            key = canonical(allocation)
            if key in seen_allocations:
                continue
            seen_allocations.add(key)
            solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))

    result = {
        "schema": "generalized-pi-named-selector-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "form_name": "R2_TWO_CYCLE" if form_index == 0 else "R3_THREE_CYCLE",
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "maximum_iterations": maximum_iterations,
        "ordinary_pi_free": True,
        "generalized_self_pi_free": True,
        "include_root_reassembly": include_root_reassembly,
        "include_all_d_bilateral": include_all_d_bilateral,
        "distinct_allocation_count": len(seen_allocations),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "iterations": [],
        "claim_boundary": (
            "Exact generalized-PI CEGAR for the enlarged named unrestricted-"
            "packet four-edge selector in the declared twelve-good necessary-"
            "premise cell. UNSAT is a bounded-cell selector theorem, not a "
            "cap-free theorem. SAT_NO_GENERALIZED_PI is a genuine selector "
            "counterprofile under complete canonical generalized PI-freeness, "
            "but not a saturated-state countermodel."
        ),
    }
    signatures = set()
    started = time.monotonic()
    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {"iteration": iteration, "solver_status": str(checked)}
        if checked == z3.unsat:
            result["status"] = "UNSAT_GENERALIZED_PI_REFINED_SELECTOR"
            result["iterations"].append(record)
            break
        if checked == z3.unknown:
            record["reason_unknown"] = solver.reason_unknown()
            result["status"] = "UNKNOWN"
            result["iterations"].append(record)
            break

        values = fractions(solver.model(), value)
        witness, minimal = find_cycle(values)
        record["minimal_common_safe_desired_counts"] = {
            owner: len(rows) for owner, rows in minimal.items()
        }
        if witness is None:
            result["status"] = "SAT_NO_GENERALIZED_PI"
            result["values"] = {
                owner: {good: str(amount) for good, amount in row.items()}
                for owner, row in values.items()
            }
            result["iterations"].append(record)
            break

        signature = cycle_signature(witness)
        if signature in signatures:
            raise AssertionError("generalized PI cut failed to remove its witness")
        signatures.add(signature)
        record["pi_witness"] = witness
        record["cut_signature"] = [list(row) for row in signature]
        result["iterations"].append(record)
        solver.add(generalized_pi_cut(value, witness))
    else:
        result["status"] = "ITERATION_LIMIT"
    result["elapsed_seconds"] = time.monotonic() - started
    result["generalized_pi_cut_count"] = len(signatures)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-iterations", type=int, default=100)
    parser.add_argument("--no-root-reassembly", action="store_true")
    parser.add_argument("--no-all-d-bilateral", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.timeout_seconds, args.random_seed,
        args.maximum_iterations,
        include_root_reassembly=not args.no_root_reassembly,
        include_all_d_bilateral=not args.no_all_d_bilateral,
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "iterations": len(result["iterations"]),
        "allocations": result["distinct_allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
