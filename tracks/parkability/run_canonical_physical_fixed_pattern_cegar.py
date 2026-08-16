#!/usr/bin/env python3
"""Canonical-physical CEGAR with the singleton/multi role pattern fixed.

Fixing the common packet-cardinality pattern removes the 12 symbolic
singleton/multi disjunctions and makes every allocation cut unconditional.
This is the exact partition used to resolve hard cores from the global
canonical-physical run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_exact_response_canonical_physical_cegar import (
    concrete_profile,
    oracle,
    symbolic_cut,
)
from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def pattern_formula(total, minimum, multi_roles):
    multi = set(multi_roles)
    return z3.And(*(
        z3.And(*(2 * minimum[role, observer] <= total[role, observer]
                 for observer in OWNERS))
        if role in multi else
        z3.And(*(minimum[role, observer] == total[role, observer]
                 for observer in OWNERS))
        for role in GOODS
    ))


def run(output, form_index, multi_roles, seeds, maximum_rounds,
        timeout_seconds, random_seed):
    multi_roles = tuple(role for role in GOODS if role in set(multi_roles))
    solver, total, minimum = build_physical_master(form_index)
    solver.add(pattern_formula(total, minimum, multi_roles))
    seeded = []
    for seed in seeds:
        previous = json.loads(seed.read_text())
        records = previous.get("rounds", previous.get("new_rounds", ()))
        for record in records:
            record_multi = tuple(record.get("multi_roles", multi_roles))
            if record_multi == multi_roles:
                solver.add(z3.Not(symbolic_cut(
                    record["allocation"], total, minimum, multi_roles,
                )))
                seeded.append(record)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    result = {
        "schema": "exact-response-canonical-physical-fixed-pattern-cegar-v1",
        "status": "RUNNING",
        "form_index": form_index,
        "multi_roles": list(multi_roles),
        "singleton_roles": [role for role in GOODS if role not in multi_roles],
        "seeds": [str(seed) for seed in seeds],
        "seed_sha256": {
            str(seed): hashlib.sha256(seed.read_bytes()).hexdigest() for seed in seeds
        },
        "seeded_cut_count": len(seeded),
        "new_rounds": [],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "UNSAT proves the canonical one/two-good four-edge conclusion only "
            "for this exact response chart and fixed common role-cardinality pattern."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for offset in range(maximum_rounds):
        status = solver.check()
        if status != z3.sat:
            result["status"] = "UNSAT_FIXED_PATTERN_THEOREM" if status == z3.unsat else "UNKNOWN"
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result
        model = solver.model()
        totals = {o: {g: Fraction(str(model.eval(total[g, o], model_completion=True))) for g in GOODS} for o in OWNERS}
        minima = {o: {g: Fraction(str(model.eval(minimum[g, o], model_completion=True))) for g in GOODS} for o in OWNERS}
        physical, role_goods, actual_multi = concrete_profile(totals, minima)
        assert actual_multi == multi_roles
        allocation = oracle(physical, role_goods)
        if allocation is None:
            result["status"] = "SAT_EXACT_CANONICAL_PHYSICAL_FOUR_EDGE_COUNTERMODEL"
            result["countermodel_iteration"] = offset
            result["countermodel_totals"] = serialize(model, total)
            result["countermodel_minima"] = serialize(model, minimum)
            output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result
        solver.add(z3.Not(symbolic_cut(allocation, total, minimum, multi_roles)))
        result["new_rounds"].append({
            "iteration": offset,
            "allocation": allocation,
            "totals": serialize(model, total),
            "minima": serialize(model, minimum),
        })
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    result["status"] = "ITERATION_LIMIT"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--multi-roles", nargs="*", required=True)
    parser.add_argument("--seed", type=Path, nargs="*", default=())
    parser.add_argument("--maximum-rounds", type=int, default=100)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    unknown = set(args.multi_roles) - set(GOODS)
    if unknown:
        parser.error(f"unknown roles: {sorted(unknown)}")
    result = run(args.output, args.form_index, args.multi_roles, args.seed,
                 args.maximum_rounds, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"], "seeded": result["seeded_cut_count"],
        "new_rounds": len(result["new_rounds"]),
    }, indent=2))


if __name__ == "__main__":
    main()
