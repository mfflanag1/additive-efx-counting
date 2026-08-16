#!/usr/bin/env python3
"""CEGAR against every four-edge allocation of canonical physical roles.

Each singleton totals/minimum role is one good.  Each multi-good role is
realized by two goods with values M and T-M in every observer row.  The
concrete oracle permits every physical good to move independently, so a model
with no oracle allocation is an exact positive-rational countermodel to the
four-support-edge conclusion inside the declared response chart.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import build_decision
from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def concrete_profile(totals, minima):
    role_goods = {}
    physical = {}
    multi = []
    for role in GOODS:
        is_singleton = all(totals[o][role] == minima[o][role] for o in OWNERS)
        names = (f"{role}:0",) if is_singleton else (f"{role}:0", f"{role}:1")
        role_goods[role] = names
        if not is_singleton:
            multi.append(role)
        for observer in OWNERS:
            physical[observer, names[0]] = minima[observer][role]
            if not is_singleton:
                physical[observer, names[1]] = totals[observer][role] - minima[observer][role]
    return physical, role_goods, tuple(multi)


def oracle(physical, role_goods):
    solver, x, _, _, goods = build_decision(
        physical, role_goods, split_cap=None, edge_cap=4
    )
    if solver.check() != z3.sat:
        return None
    model = solver.model()
    return {
        owner: [g for g in goods if z3.is_true(model.eval(x[g, owner]))]
        for owner in OWNERS
    }


def symbolic_good_value(total, minimum, observer, good, multi):
    role, index = good.split(":")
    if role not in multi:
        return total[role, observer]
    return minimum[role, observer] if index == "0" else total[role, observer] - minimum[role, observer]


def symbolic_cut(allocation, total, minimum, multi):
    multi = set(multi)
    pattern = []
    for role in GOODS:
        if role in multi:
            pattern.append(z3.And(*(
                2 * minimum[role, observer] <= total[role, observer]
                for observer in OWNERS
            )))
        else:
            pattern.append(z3.And(*(
                minimum[role, observer] == total[role, observer]
                for observer in OWNERS
            )))
    utility = {
        (observer, target): z3.Sum(*(
            symbolic_good_value(total, minimum, observer, good, multi)
            for good in allocation[target]
        )) if allocation[target] else z3.RealVal(0)
        for observer in OWNERS for target in OWNERS
    }
    efx = []
    for observer in OWNERS:
        for target in OWNERS:
            if observer == target:
                continue
            for good in allocation[target]:
                efx.append(
                    utility[observer, observer] >= utility[observer, target]
                    - symbolic_good_value(total, minimum, observer, good, multi)
                )
    return z3.And(*(pattern + efx))


def run(output, form_index, maximum_rounds, timeout_seconds, random_seed, resume=None):
    solver, total, minimum = build_physical_master(form_index)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    result = {
        "schema": "exact-response-canonical-physical-cegar-v1",
        "status": "RUNNING",
        "form_index": form_index,
        "physical_realization": "singleton T=M or two goods M and T-M",
        "edge_cap": 4,
        "rounds": [],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "SAT obstruction is an exact concrete countermodel to the four-support-"
            "edge conclusion for this response chart. UNSAT proves only the canonical "
            "one/two-good realization, not every larger physical packet realization."
        ),
    }
    if resume is not None:
        previous = json.loads(resume.read_text())
        if previous["form_index"] != form_index:
            raise ValueError("resume form index mismatch")
        for round_record in previous["rounds"]:
            solver.add(z3.Not(symbolic_cut(
                round_record["allocation"], total, minimum,
                round_record["multi_roles"],
            )))
        result["rounds"] = previous["rounds"]
        result["resumed_from"] = str(resume)
        result["resumed_from_sha256"] = hashlib.sha256(resume.read_bytes()).hexdigest()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for _ in range(maximum_rounds):
        iteration = len(result["rounds"])
        status = solver.check()
        if status != z3.sat:
            result["status"] = "UNSAT_CANONICAL_PHYSICAL_CHART_THEOREM" if status == z3.unsat else "UNKNOWN"
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result
        model = solver.model()
        totals = {o: {g: Fraction(str(model.eval(total[g, o], model_completion=True))) for g in GOODS} for o in OWNERS}
        minima = {o: {g: Fraction(str(model.eval(minimum[g, o], model_completion=True))) for g in GOODS} for o in OWNERS}
        physical, role_goods, multi = concrete_profile(totals, minima)
        allocation = oracle(physical, role_goods)
        if allocation is None:
            result["status"] = "SAT_EXACT_CANONICAL_PHYSICAL_FOUR_EDGE_COUNTERMODEL"
            result["countermodel_iteration"] = iteration
            result["countermodel_totals"] = serialize(model, total)
            result["countermodel_minima"] = serialize(model, minimum)
            result["countermodel_multi_roles"] = list(multi)
            output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result
        solver.add(z3.Not(symbolic_cut(allocation, total, minimum, multi)))
        result["rounds"].append({
            "iteration": iteration,
            "multi_roles": list(multi),
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
    parser.add_argument("--maximum-rounds", type=int, default=50)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()
    result = run(args.output, args.form_index, args.maximum_rounds,
                 args.timeout_seconds, args.random_seed, args.resume)
    print(json.dumps({"status": result["status"], "rounds": len(result["rounds"])}, indent=2))


if __name__ == "__main__":
    main()
