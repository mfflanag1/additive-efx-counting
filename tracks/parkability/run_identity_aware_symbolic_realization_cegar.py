#!/usr/bin/env python3
"""CEGAR over symbolic physical realizations at fixed totals and minima.

The witness-side driver fixes two goods per multi-good role, which is every
realization only when each role's slack `rho(g) = min_i floor(T/M)` is two.
Above slack two a role may carry three or more goods, and then the value
column itself is free: `(M, M+t, T-2M-t)` realizes one totals/minima profile
for a range of `t`, with the off-witness side minimum varying.

This driver removes that restriction.  For a fixed vector of role cardinalities
it makes every physical good value a real unknown constrained by

    u[g,x,i] >= M[i,g],   sum_x u[g,x,i] = T[i,g],   some x attains M[i,g],

so the master ranges over *all* realizations of the profile at those
cardinalities, and the coincidence partition of role `g` is whatever the
attaining indices induce.  Rounds alternate the master, seeking a realization
that defeats every allocation found so far, with the exact concrete
four-support-edge EFX decision.  Each round contributes a new allocation, so
the loop terminates on the finite allocation space.

Cardinalities are swept: every vector with `2 <= k_g <= min(rho(g), cap)` on
multi-good roles.  A verdict is exhaustive for the profile exactly when the
cap did not bind, that is when `cap >= rho(g)` for every role.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import support_supplier
from .run_identity_aware_witness_side_cegar import load_profile
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def rational(value):
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def slack(totals, minima, role):
    return min(totals[o][role] // minima[o][role] for o in OWNERS)


def cardinality_vectors(totals, minima, cap):
    """Every role-cardinality vector allowed by the slack bound and the cap."""
    choices = []
    for role in GOODS:
        singleton = all(totals[o][role] == minima[o][role] for o in OWNERS)
        if singleton:
            choices.append((1,))
            continue
        top = min(int(slack(totals, minima, role)), cap)
        choices.append(tuple(range(2, top + 1)))
    for combination in itertools.product(*choices):
        yield dict(zip(GOODS, combination))


def layout(counts):
    return {role: tuple(f"{role}:{i}" for i in range(counts[role])) for role in GOODS}


def build_decision(physical, role_goods, edge_cap):
    """Exact four-support-edge complete-EFX decision for arbitrary role sizes."""
    goods = tuple(g for role in GOODS for g in role_goods[role])
    supplier = support_supplier()
    assign = {
        (good, owner): z3.Bool(f"x_{good.replace(':', '_')}_{owner}")
        for good in goods for owner in OWNERS
    }
    edge = {
        (source, target): z3.Bool(f"edge_{source}_{target}")
        for source in set(supplier.values())
        for target in OWNERS
        if source != target
    }
    solver = z3.Solver()
    for good in goods:
        solver.add(z3.PbEq([(assign[good, owner], 1) for owner in OWNERS], 1))
        source = supplier[good.split(":", 1)[0]]
        for target in OWNERS:
            if target != source:
                solver.add(z3.Implies(assign[good, target], edge[source, target]))
    solver.add(z3.PbLe([(flag, 1) for flag in edge.values()], edge_cap))
    utility = {
        (observer, target): z3.Sum(*(
            z3.If(assign[good, target], rational(physical[observer, good]),
                  z3.RealVal(0))
            for good in goods
        ))
        for observer in OWNERS for target in OWNERS
    }
    for observer in OWNERS:
        own = utility[observer, observer]
        for target in OWNERS:
            if target == observer:
                continue
            for good in goods:
                solver.add(z3.Implies(
                    assign[good, target],
                    own >= utility[observer, target]
                    - rational(physical[observer, good]),
                ))
    return solver, assign, goods


def decide(physical, role_goods, edge_cap, timeout_seconds):
    solver, assign, goods = build_decision(physical, role_goods, edge_cap)
    solver.set(timeout=timeout_seconds * 1000)
    status = solver.check()
    if status != z3.sat:
        return str(status), None
    model = solver.model()
    return "sat", {
        owner: [g for g in goods if z3.is_true(model.eval(assign[g, owner]))]
        for owner in OWNERS
    }


def audit_allocation(allocation, physical, edge_cap, role_goods):
    supplier = support_supplier()
    placed = [good for goods in allocation.values() for good in goods]
    expected = {g for role in GOODS for g in role_goods[role]}
    assert sorted(placed) == sorted(expected)
    edges = sorted({
        (supplier[good.split(":", 1)[0]], owner)
        for owner, goods in allocation.items()
        for good in goods
        if supplier[good.split(":", 1)[0]] != owner
    })
    assert len(edges) <= edge_cap
    for observer in OWNERS:
        own = sum((physical[observer, g] for g in allocation[observer]), Fraction())
        for target in OWNERS:
            if target == observer:
                continue
            total = sum(
                (physical[observer, g] for g in allocation[target]), Fraction()
            )
            for good in allocation[target]:
                assert own >= total - physical[observer, good]
    return edges


def symbolic_master(totals, minima, role_goods):
    value = {
        (observer, good): z3.Real(f"u_{good.replace(':', '_')}_{observer}")
        for role in GOODS for good in role_goods[role] for observer in OWNERS
    }
    master = z3.Solver()
    for role in GOODS:
        names = role_goods[role]
        for observer in OWNERS:
            floor = minima[observer][role]
            master.add(*(value[observer, g] >= rational(floor) for g in names))
            master.add(
                z3.Sum(*(value[observer, g] for g in names))
                == rational(totals[observer][role])
            )
            master.add(z3.Or(*(
                value[observer, g] == rational(floor) for g in names
            )))
    return master, value


def failure_clause(allocation, value):
    utility = {
        (observer, target): z3.Sum(*(
            value[observer, good] for good in allocation[target]
        )) if allocation[target] else z3.RealVal(0)
        for observer in OWNERS for target in OWNERS
    }
    return z3.Or(*(
        utility[observer, observer]
        < utility[observer, target] - value[observer, good]
        for observer in OWNERS
        for target in OWNERS
        if target != observer
        for good in allocation[target]
    ))


def concrete(model, value, role_goods):
    physical = {}
    for role in GOODS:
        for good in role_goods[role]:
            for observer in OWNERS:
                physical[observer, good] = Fraction(str(
                    model.eval(value[observer, good], model_completion=True)
                ))
    return physical


def coincidence_partitions(physical, minima, role_goods):
    """The partitions the realization actually induces, per role."""
    induced = {}
    for role in GOODS:
        names = role_goods[role]
        blocks = {}
        for observer in OWNERS:
            attaining = tuple(
                g for g in names
                if physical[observer, g] == minima[observer][role]
            )
            blocks.setdefault(attaining[0], []).append(observer)
        induced[role] = "|".join(
            "".join(block) for block in sorted(blocks.values(), key=lambda b: b[0])
        )
    return induced


def solve_configuration(totals, minima, counts, edge_cap, maximum_rounds,
                        timeout_seconds):
    role_goods = layout(counts)
    master, value = symbolic_master(totals, minima, role_goods)
    used = 0
    for _ in range(maximum_rounds):
        outcome = master.check()
        if outcome == z3.unsat:
            return {"status": "UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION",
                    "rounds": used}
        if outcome == z3.unknown:
            return {"status": "UNKNOWN", "rounds": used,
                    "reason_unknown": master.reason_unknown()}
        physical = concrete(master.model(), value, role_goods)
        for role in GOODS:
            for observer in OWNERS:
                column = [physical[observer, g] for g in role_goods[role]]
                assert sum(column) == totals[observer][role]
                assert min(column) == minima[observer][role]
        concrete_status, allocation = decide(
            physical, role_goods, edge_cap, timeout_seconds
        )
        used += 1
        if concrete_status == "unsat":
            return {
                "status": "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL",
                "rounds": used,
                "coincidence_partitions": coincidence_partitions(
                    physical, minima, role_goods
                ),
                "physical_values": {
                    observer: {
                        good: str(physical[observer, good])
                        for role in GOODS for good in role_goods[role]
                    }
                    for observer in OWNERS
                },
            }
        if concrete_status != "sat":
            return {"status": "UNKNOWN", "rounds": used}
        audit_allocation(allocation, physical, edge_cap, role_goods)
        master.add(failure_clause(allocation, value))
    return {"status": "ROUND_LIMIT", "rounds": used}


def run(profile_path, output_path, cap, edge_cap, maximum_rounds, timeout_seconds):
    raw, totals, minima = load_profile(profile_path)
    slacks = {role: int(slack(totals, minima, role)) for role in GOODS}
    vectors = list(cardinality_vectors(totals, minima, cap))
    configurations = []
    countermodel = None
    for counts in vectors:
        outcome = solve_configuration(
            totals, minima, counts, edge_cap, maximum_rounds, timeout_seconds
        )
        outcome["role_cardinalities"] = counts
        outcome["physical_good_count"] = sum(counts.values())
        configurations.append(outcome)
        print(counts, outcome["status"], "rounds", outcome["rounds"], flush=True)
        if outcome["status"] == "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL":
            countermodel = outcome
            break

    exhaustive = all(value <= cap for value in slacks.values())
    statuses = {outcome["status"] for outcome in configurations}
    result = {
        "schema": "identity-aware-symbolic-realization-cegar-v1",
        "status": (
            "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL" if countermodel
            else ("UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION"
                  if statuses == {"UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION"}
                  else "INCOMPLETE")
        ),
        "source_profile": str(profile_path),
        "source_profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "source_profile_status": raw.get("status"),
        "edge_cap": edge_cap,
        "edge_origin": "support",
        "cardinality_cap": cap,
        "role_slacks": slacks,
        "cap_covers_every_role": exhaustive,
        "cardinality_vectors_examined": len(configurations),
        "cardinality_vectors_available": len(vectors),
        "configurations": configurations,
        "terminal": countermodel,
        "realization_family": (
            "every positive-rational realization of the profile at the stated "
            "role cardinalities; values are solver unknowns, not a fixed "
            "two-good template"
        ),
        "claim_boundary": (
            "When cap_covers_every_role is true the sweep is every physical "
            "realization of the profile and the verdict is exact for it.  "
            "Otherwise it covers only realizations with at most `cap` goods "
            "per role.  Nothing here establishes chart coverage or the "
            "universal fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cap", type=int, default=3)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--maximum-rounds", type=int, default=120)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    result = run(args.profile, args.output, args.cap, args.edge_cap,
                 args.maximum_rounds, args.timeout_seconds)
    print(json.dumps({
        "status": result["status"],
        "cardinality_vectors_examined": result["cardinality_vectors_examined"],
        "cap_covers_every_role": result["cap_covers_every_role"],
    }, indent=2))


if __name__ == "__main__":
    main()
