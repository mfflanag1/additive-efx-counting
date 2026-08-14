#!/usr/bin/env python3
"""Batched exact CEGAR for the named-packet fixed-U terminal cell.

Unlike the discovery v1 run, this records each exact rational master profile
and installs a menu of all discovered minimum-radius escapes at each round.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_fixed_u_full_packet_terminal_cegar import (
        BASE, GOODS, OWNERS, RECIPIENTS, allocation_formula, build_master,
        fractions, lex_improves,
    )
except ImportError:  # Permit direct replay from the script path.
    from run_fixed_u_full_packet_terminal_cegar import (
        BASE, GOODS, OWNERS, RECIPIENTS, allocation_formula, build_master,
        fractions, lex_improves,
    )


def exact(value):
    return z3.RealVal(str(value))


def oracle_menu(values, mode, maximum_escapes, radius_slack, metric="goods",
                provenance=None):
    holder = {good: z3.Int(f"{mode}_holder_{good}") for good in GOODS}
    solver = z3.Solver()
    for variable in holder.values():
        solver.add(variable >= 0, variable < len(RECIPIENTS))
    if mode == "efx_lex":
        solver.add(z3.Or(*(holder[good] == 4 for good in GOODS)))
    elif mode == "complete_efx":
        solver.add(*(holder[good] < 4 for good in GOODS))

    utility = {}
    for observer in OWNERS:
        for recipient_index, recipient in enumerate(RECIPIENTS):
            utility[observer, recipient] = z3.Sum(*(
                z3.If(holder[good] == recipient_index, exact(values[observer][good]), 0)
                for good in GOODS
            ))
    own = {owner: utility[owner, owner] for owner in OWNERS}
    if mode == "efx_lex":
        solver.add(lex_improves(own))
        for observer in OWNERS:
            for target_index, target in enumerate(OWNERS):
                if observer == target:
                    continue
                for good in GOODS:
                    solver.add(z3.Implies(
                        holder[good] == target_index,
                        own[observer] >= utility[observer, target]
                        - exact(values[observer][good]),
                    ))
            solver.add(own[observer] >= utility[observer, "charity"])
    elif mode == "complete_efx":
        for observer in OWNERS:
            for target_index, target in enumerate(OWNERS):
                if observer == target:
                    continue
                for good in GOODS:
                    solver.add(z3.Implies(
                        holder[good] == target_index,
                        own[observer] >= utility[observer, target]
                        - exact(values[observer][good]),
                    ))
    elif mode == "pareto":
        solver.add(*(own[owner] >= 1 for owner in OWNERS))
        solver.add(z3.Or(*(own[owner] > 1 for owner in OWNERS)))
    else:
        raise ValueError(mode)

    provenance = BASE if provenance is None else provenance
    base_holder = {
        good: RECIPIENTS.index(recipient)
        for recipient, goods in provenance.items() for good in goods
    }
    if metric == "goods":
        move_count = z3.Sum(*(
            z3.If(holder[good] == base_holder[good], 0, 1) for good in GOODS
        ))
        maximum_radius = len(GOODS)
    elif metric in ("edges", "functional_edges"):
        edge_terms = []
        for supplier_index, supplier in enumerate(RECIPIENTS):
            supplied = tuple(good for good in GOODS if base_holder[good] == supplier_index)
            supplier_edges = []
            for recipient_index, recipient in enumerate(RECIPIENTS):
                if recipient == supplier or not supplied:
                    continue
                active = z3.Or(*(holder[good] == recipient_index for good in supplied))
                edge_terms.append(z3.If(active, 1, 0))
                supplier_edges.append(active)
            if metric == "functional_edges" and supplier_edges:
                solver.add(z3.AtMost(*supplier_edges, 1))
        move_count = z3.Sum(*edge_terms)
        maximum_radius = len(edge_terms)
    else:
        raise ValueError(metric)
    minimum_radius = None
    for radius in range(maximum_radius + 1):
        solver.push()
        solver.add(move_count <= radius)
        status = solver.check()
        solver.pop()
        if status == z3.sat:
            minimum_radius = radius
            break
        if status == z3.unknown:
            return None, [], solver.reason_unknown()
    if minimum_radius is None:
        return None, [], None

    solver.add(move_count <= min(maximum_radius, minimum_radius + radius_slack))
    allocations = []
    while len(allocations) < maximum_escapes and solver.check() == z3.sat:
        model = solver.model()
        allocation = {recipient: [] for recipient in RECIPIENTS}
        assignment = []
        for good in GOODS:
            recipient_index = model.eval(holder[good]).as_long()
            assignment.append(holder[good] == recipient_index)
            allocation[RECIPIENTS[recipient_index]].append(good)
        for goods in allocation.values():
            goods.sort()
        allocations.append(allocation)
        solver.add(z3.Not(z3.And(*assignment)))
    return minimum_radius, allocations, None


def serialize_values(values):
    return {
        owner: {good: str(amount) for good, amount in row.items()}
        for owner, row in values.items()
    }


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(seed_path, output, maximum_iterations, timeout_seconds,
        maximum_escapes, radius_slack):
    master, value = build_master()
    master.set(timeout=timeout_seconds * 1000)
    seed = json.loads(seed_path.read_text())
    seed_allocations = []
    for record in seed["iterations"]:
        allocation = record.get("blocking_allocation")
        if allocation is not None:
            seed_allocations.append((record["mode"], allocation))
            master.add(z3.Not(allocation_formula(allocation, value, record["mode"])))

    result = {
        "schema": "fixed-u-full-packet-batch-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "seed": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "seed_cut_count": len(seed_allocations),
        "maximum_escapes_per_round": maximum_escapes,
        "radius_slack": radius_slack,
        "rounds": [],
        "claim_boundary": (
            "exact batched CEGAR for the twelve-atom named-packet premises and "
            "global EFX-lex/Pareto maximality; it records exact profiles and escape "
            "menus, but does not encode response saturation, recurrence reachability, "
            "or a genuine exact repeat and cannot establish cap-free termination"
        ),
    }
    checkpoint(output, result)
    for iteration in range(maximum_iterations):
        status = master.check()
        round_record = {"iteration": iteration, "master_status": str(status)}
        result["rounds"].append(round_record)
        if status != z3.sat:
            result["status"] = str(status)
            if status == z3.unknown:
                result["reason_unknown"] = master.reason_unknown()
            checkpoint(output, result)
            return result

        values = fractions(master.model(), value)
        round_record["values"] = serialize_values(values)
        found_mode = None
        for mode in ("complete_efx", "efx_lex", "pareto"):
            radius, allocations, reason = oracle_menu(
                values, mode, maximum_escapes, radius_slack
            )
            if reason is not None:
                result["status"] = "oracle_unknown"
                round_record["mode"] = mode
                round_record["reason_unknown"] = reason
                checkpoint(output, result)
                return result
            if allocations:
                found_mode = mode
                round_record["mode"] = mode
                round_record["minimum_radius"] = radius
                round_record["blocking_allocations"] = allocations
                for allocation in allocations:
                    master.add(z3.Not(allocation_formula(allocation, value, mode)))
                break

        if found_mode is None:
            result["status"] = "sat_packet_terminal_obstruction"
            result["countermodel_iteration"] = iteration
            checkpoint(output, result)
            return result
        checkpoint(output, result)
        print(json.dumps({
            "iteration": iteration,
            "mode": found_mode,
            "minimum_radius": round_record["minimum_radius"],
            "cuts": len(round_record["blocking_allocations"]),
        }), flush=True)
    result["status"] = "iteration_limit"
    checkpoint(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=100)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--maximum-escapes", type=int, default=32)
    parser.add_argument("--radius-slack", type=int, default=0)
    args = parser.parse_args()
    result = run(
        args.seed, args.output, args.maximum_iterations, args.timeout_seconds,
        args.maximum_escapes, args.radius_slack,
    )
    print(json.dumps({
        "status": result["status"],
        "rounds": len(result["rounds"]),
    }, indent=2))


if __name__ == "__main__":
    main()
