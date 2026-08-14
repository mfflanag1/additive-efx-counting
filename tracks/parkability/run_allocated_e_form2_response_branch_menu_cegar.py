#!/usr/bin/env python3
"""Exact CEGAR for the form-2 menu enlarged by all six response branches."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .find_generalized_pi_cycle import find_closed_core_families
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_allocated_e_form2_three_topology_menu_cegar import (
    MENU as THREE_TOPOLOGY_MENU,
    allocations_for_topology,
)
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula, fractions
from .run_generalized_pi_named_selector_cegar import (
    cycle_signature, generalized_pi_cut,
)


# Choose d's response target in {r,q}, omit one source from the represented
# r->q->s->r response cycle, reverse the other two cycle responses, and send
# charity to the omitted source.  Edges below are physical supplier pairs.
SIX_RESPONSE_BRANCHES = (
    (("charity", "r"), ("s", "q"), ("r", "s"), ("r", "d")),
    (("charity", "q"), ("q", "r"), ("r", "s"), ("r", "d")),
    (("charity", "s"), ("q", "r"), ("s", "q"), ("r", "d")),
    (("charity", "r"), ("s", "q"), ("r", "s"), ("q", "d")),
    (("charity", "q"), ("q", "r"), ("r", "s"), ("q", "d")),
    (("charity", "s"), ("q", "r"), ("s", "q"), ("q", "d")),
)
MENU = tuple(dict.fromkeys((*THREE_TOPOLOGY_MENU, *SIX_RESPONSE_BRANCHES)))


def canonical(allocation):
    return tuple(
        (owner, tuple(sorted(goods)))
        for owner, goods in sorted(allocation.items())
    )


def menu_allocations():
    rows = {}
    for topology in MENU:
        for allocation in allocations_for_topology(topology):
            rows.setdefault(canonical(allocation), allocation)
    return list(rows.values())


def load_cut_sources(solver, value, sources):
    signatures = set()
    records = []
    for source in sources:
        raw = source.read_bytes()
        payload = json.loads(raw)
        assert payload["form_index"] == 2
        before = len(signatures)
        for iteration in payload.get("iterations", ()):
            for witness in iteration.get("pi_witnesses") or ():
                signature = cycle_signature(witness)
                if signature in signatures:
                    continue
                signatures.add(signature)
                solver.add(generalized_pi_cut(value, witness))
        records.append({
            "source": str(source),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "new_cut_count": len(signatures) - before,
            "cumulative_cut_count": len(signatures),
        })
    return signatures, records


def run(output: Path, cut_sources: list[Path], timeout_seconds: int,
        random_seed: int, maximum_iterations: int,
        maximum_families_per_round: int):
    solver, value = build_master(2)
    allocations = menu_allocations()
    for allocation in allocations:
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    signatures, source_records = load_cut_sources(
        solver, value, cut_sources,
    )
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    result = {
        "schema": "allocated-e-form2-response-branch-menu-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": 2,
        "menu": [[list(edge) for edge in topology] for topology in MENU],
        "three_topology_count": len(THREE_TOPOLOGY_MENU),
        "response_branch_count": len(SIX_RESPONSE_BRANCHES),
        "topology_count": len(MENU),
        "topology_allocation_counts": [
            len(allocations_for_topology(topology)) for topology in MENU
        ],
        "allocation_count": len(allocations),
        "cut_sources": source_records,
        "loaded_cut_count": len(signatures),
        "timeout_seconds_per_check": timeout_seconds,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "random_seed": random_seed,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "iterations": [],
        "claim_boundary": (
            "Exact twelve-atom allocated-E form-2 decision for the union of "
            "the empirical three-topology menu and all six cap-free response "
            "branches. Any verdict is bounded-atom only."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["generalized_pi_cut_count"] = len(signatures)
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {"iteration": iteration, "solver_status": str(checked)}
        if checked == z3.unsat:
            result["status"] = "UNSAT"
            result["iterations"].append(record)
            checkpoint()
            break
        if checked == z3.unknown:
            result["status"] = "UNKNOWN"
            record["reason_unknown"] = solver.reason_unknown()
            result["iterations"].append(record)
            checkpoint()
            break
        values = fractions(solver.model(), value)
        witnesses, minimal = find_closed_core_families(
            values, ALLOCATED_E_BASE, maximum=maximum_families_per_round,
        )
        record["minimal_common_safe_desired_counts"] = {
            owner: len(rows) for owner, rows in minimal.items()
        }
        if not witnesses:
            result["status"] = "SAT_NO_GENERALIZED_PI"
            result["values"] = {
                owner: {good: str(amount) for good, amount in row.items()}
                for owner, row in values.items()
            }
            result["iterations"].append(record)
            checkpoint()
            break
        fresh = []
        for witness in witnesses:
            signature = cycle_signature(witness)
            if signature in signatures:
                continue
            signatures.add(signature)
            fresh.append(witness)
            solver.add(generalized_pi_cut(value, witness))
        assert fresh
        record["pi_cycle_count"] = len(witnesses)
        record["fresh_cut_count"] = len(fresh)
        record["pi_witnesses"] = fresh
        result["iterations"].append(record)
        checkpoint()
    else:
        result["status"] = "ITERATION_LIMIT"
    checkpoint()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cut-source", type=Path, action="append", default=[])
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-iterations", type=int, default=20)
    parser.add_argument("--maximum-families-per-round", type=int, default=10000)
    args = parser.parse_args()
    result = run(
        args.output, args.cut_source, args.timeout_seconds, args.random_seed,
        args.maximum_iterations, args.maximum_families_per_round,
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "iterations": len(result["iterations"]),
        "allocations": result["allocation_count"],
        "topologies": result["topology_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
