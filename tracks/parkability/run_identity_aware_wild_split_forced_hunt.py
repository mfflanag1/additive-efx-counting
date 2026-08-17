#!/usr/bin/env python3
"""Hunt a fixed-U profile on which a wild role must be split.

Theorem 1 of `results/IDENTITY_AWARE_SLACK_TWO_20260816.md` closes a profile
for every realization as soon as some menu of complete within-budget
allocations, none of which splits a *wild* role (slack at least three), covers
the side patterns of the tame roles.  It therefore goes silent on exactly one
shape: a profile where no such menu exists, because every complete
within-budget EFX allocation is forced to split a wild role.  That shape is the
only surviving route to a countermodel above slack two.

This driver searches the premises for it.  Fix a designated role `X` and ask
the exact-response physical master for a profile in which

    X is wild                  T[i,X] >= 3 M[i,X]  for every observer,
    every other role is tame   2 M[i,g] <= T[i,g]  for every observer,
                               and T[i,g] < 3 M[i,g] for some observer,

together with a side pattern of the tame roles under which **no** complete
four-support-edge EFX allocation avoids splitting `X`.

The restriction to a single wild role is what makes the question exactly
decidable in the two-good model.  Tame roles have exactly two goods with the
forced column by Lemma B, and `X`, never split by the family under test,
contributes exactly its total and its minimum whatever its true width by
Lemma C'.  So the two-good stand-in is exact for every role, and a concrete
`unsat` genuinely means every four-edge EFX allocation splits `X`.

The allocation family deliberately permits splitting arbitrarily many tame
roles at once: forcedness tested against a one-split-at-a-time family produces
false positives, which is how an earlier chart obstruction on this same chart
arose.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import support_supplier
from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def rational(value):
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def build_hunt_master(form_index, wild_role):
    """Physical master with `wild_role` wild and every other role tame."""
    solver, value, minimum = build_physical_master(form_index)
    for observer in OWNERS:
        solver.add(value[wild_role, observer] >= 3 * minimum[wild_role, observer])
    for role in GOODS:
        if role == wild_role:
            continue
        solver.add(*(
            2 * minimum[role, observer] <= value[role, observer]
            for observer in OWNERS
        ))
        solver.add(z3.Or(*(
            value[role, observer] < 3 * minimum[role, observer]
            for observer in OWNERS
        )))
    return solver, value, minimum


def role_goods_layout():
    return {role: (f"{role}:0", f"{role}:1") for role in GOODS}


def symbolic_values(value, minimum, side, wild_role, role_goods):
    """Good values as linear expressions in the profile and side unknowns."""
    physical = {}
    for role in GOODS:
        low, high = role_goods[role]
        for observer in OWNERS:
            base = minimum[role, observer]
            rest = value[role, observer] - minimum[role, observer]
            if role == wild_role:
                physical[observer, low] = base
                physical[observer, high] = rest
                continue
            gap = value[role, observer] - 2 * minimum[role, observer]
            shift = z3.If(side[role, observer], gap, z3.RealVal(0))
            physical[observer, low] = base + shift
            physical[observer, high] = rest - shift
    return physical


def concrete_values(totals, minima, sides, wild_role, role_goods):
    physical = {}
    for role in GOODS:
        low, high = role_goods[role]
        for observer in OWNERS:
            base = minima[observer][role]
            rest = totals[observer][role] - base
            if role == wild_role:
                physical[observer, low] = base
                physical[observer, high] = rest
            else:
                gap = totals[observer][role] - 2 * base
                shift = gap if sides[role, observer] else Fraction(0)
                physical[observer, low] = base + shift
                physical[observer, high] = rest - shift
            assert physical[observer, low] > 0 and physical[observer, high] > 0
            assert min(physical[observer, low], physical[observer, high]) == base
    return physical


def build_decision(physical, role_goods, wild_role, edge_cap):
    """Complete four-edge EFX decision over allocations that never split X."""
    goods = tuple(g for role in GOODS for g in role_goods[role])
    supplier = support_supplier()
    assign = {
        (good, owner): z3.Bool(f"x_{good.replace(':', '_')}_{owner}")
        for good in goods for owner in OWNERS
    }
    edge = {
        (source, target): z3.Bool(f"e_{source}_{target}")
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
    # The wild role is never split; every tame role may be split freely, and
    # any number of them may be split at once.
    low, high = role_goods[wild_role]
    for owner in OWNERS:
        solver.add(assign[low, owner] == assign[high, owner])

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


def failure_clause(allocation, physical):
    utility = {
        (observer, target): z3.Sum(*(
            physical[observer, good] for good in allocation[target]
        )) if allocation[target] else z3.RealVal(0)
        for observer in OWNERS for target in OWNERS
    }
    return z3.Or(*(
        utility[observer, observer]
        < utility[observer, target] - physical[observer, good]
        for observer in OWNERS
        for target in OWNERS
        if target != observer
        for good in allocation[target]
    ))


def serialize(model, table):
    return {
        observer: {
            role: str(Fraction(str(model.eval(table[role, observer],
                                              model_completion=True))))
            for role in GOODS
        }
        for observer in OWNERS
    }


def audit(allocation, physical, wild_role, role_goods, edge_cap):
    supplier = support_supplier()
    placed = [g for goods in allocation.values() for g in goods]
    assert sorted(placed) == sorted(g for r in GOODS for g in role_goods[r])
    low, high = role_goods[wild_role]
    holder = {g: o for o, goods in allocation.items() for g in goods}
    assert holder[low] == holder[high]
    edges = sorted({
        (supplier[g.split(":", 1)[0]], owner)
        for owner, goods in allocation.items()
        for g in goods
        if supplier[g.split(":", 1)[0]] != owner
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


def hunt(form_index, wild_role, edge_cap, maximum_rounds, timeout_seconds,
         random_seed, canonical_sides=False):
    role_goods = role_goods_layout()
    master, value, minimum = build_hunt_master(form_index, wild_role)
    master.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    side = {
        (role, observer): z3.Bool(f"side_{role}_{observer}")
        for role in GOODS if role != wild_role
        for observer in OWNERS
    }
    if canonical_sides:
        # Stage one pins every tame role to the all-coincide pattern.  This is
        # a restriction of the search, so a profile found here is still a
        # genuine witness, while an unsat verdict covers only that pattern.
        master.add(*(z3.Not(flag) for flag in side.values()))
    else:
        master.add(*(
            z3.Not(side[role, "r"]) for role in GOODS if role != wild_role
        ))
    symbolic = symbolic_values(value, minimum, side, wild_role, role_goods)

    rounds = 0
    for _ in range(maximum_rounds):
        outcome = master.check()
        if outcome == z3.unsat:
            return {
                "status": "UNSAT_NO_ADMISSIBLE_PROFILE_FORCES_THIS_WILD_SPLIT",
                "rounds": rounds,
            }
        if outcome == z3.unknown:
            return {"status": "UNKNOWN", "rounds": rounds,
                    "reason_unknown": master.reason_unknown()}
        model = master.model()
        totals = serialize(model, value)
        minima = serialize(model, minimum)
        totals = {o: {g: Fraction(a) for g, a in row.items()}
                  for o, row in totals.items()}
        minima = {o: {g: Fraction(a) for g, a in row.items()}
                  for o, row in minima.items()}
        sides = {k: z3.is_true(model.eval(f)) for k, f in side.items()}
        physical = concrete_values(totals, minima, sides, wild_role, role_goods)

        solver, assign, goods = build_decision(
            physical, role_goods, wild_role, edge_cap
        )
        solver.set(timeout=timeout_seconds * 1000)
        verdict = solver.check()
        rounds += 1
        if verdict == z3.unsat:
            return {
                "status": "WILD_SPLIT_FORCED_PROFILE_FOUND",
                "rounds": rounds,
                "wild_role": wild_role,
                "role_slacks": {
                    g: str(min(totals[o][g] // minima[o][g] for o in OWNERS))
                    for g in GOODS
                },
                "totals": {o: {g: str(v) for g, v in row.items()}
                           for o, row in totals.items()},
                "minima": {o: {g: str(v) for g, v in row.items()}
                           for o, row in minima.items()},
                "physical_values": {
                    o: {g: str(physical[o, g])
                        for r in GOODS for g in role_goods[r]}
                    for o in OWNERS
                },
            }
        if verdict == z3.unknown:
            return {"status": "UNKNOWN", "rounds": rounds,
                    "reason_unknown": solver.reason_unknown()}
        allocation = {
            owner: [g for g in goods
                    if z3.is_true(solver.model().eval(assign[g, owner]))]
            for owner in OWNERS
        }
        audit(allocation, physical, wild_role, role_goods, edge_cap)
        master.add(failure_clause(allocation, symbolic))
        print(f"    {wild_role} round {rounds}: blocked an allocation",
              flush=True)
    return {"status": "ROUND_LIMIT", "rounds": rounds}


def run(output_path, form_index, roles, edge_cap, maximum_rounds,
        timeout_seconds, random_seed, canonical_sides=False):
    results = {}
    found = None
    for role in roles:
        outcome = hunt(form_index, role, edge_cap, maximum_rounds,
                       timeout_seconds, random_seed, canonical_sides)
        results[role] = outcome
        print(role, outcome["status"], "rounds", outcome["rounds"], flush=True)
        # Checkpoint after every role so a long sweep is never lost wholesale.
        output_path.write_text(json.dumps(
            {"schema": "identity-aware-wild-split-forced-hunt-v1",
             "status": "IN_PROGRESS", "per_role": results},
            indent=2, sort_keys=True) + "\n")
        if outcome["status"] == "WILD_SPLIT_FORCED_PROFILE_FOUND":
            found = outcome
            break

    statuses = {outcome["status"] for outcome in results.values()}
    result = {
        "schema": "identity-aware-wild-split-forced-hunt-v1",
        "status": (
            "WILD_SPLIT_FORCED_PROFILE_FOUND" if found
            else ("UNSAT_NO_ADMISSIBLE_SINGLE_WILD_ROLE_IS_FORCED"
                  if statuses == {"UNSAT_NO_ADMISSIBLE_PROFILE_FORCES_THIS_WILD_SPLIT"}
                  else "INCOMPLETE")
        ),
        "form_index": form_index,
        "canonical_sides_only": canonical_sides,
        "edge_cap": edge_cap,
        "edge_origin": "support",
        "roles_examined": list(roles),
        "per_role": results,
        "terminal": found,
        "search_shape": (
            "one designated wild role, every other role tame multi-good; the "
            "allocation family forbids splitting the wild role and permits "
            "splitting any number of tame roles simultaneously"
        ),
        "claim_boundary": (
            "A found profile is an exact fixed-U-admissible witness that every "
            "complete four-support-edge EFX allocation splits the designated "
            "wild role, which is the one shape the realization-free reduction "
            "cannot close.  An unsat verdict proves no admissible profile with "
            "exactly one wild role and all others tame multi-good forces that "
            "role's split; it says nothing about profiles with several wild "
            "roles or with singleton roles present."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, default=2)
    parser.add_argument("--role", action="append", default=None)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--maximum-rounds", type=int, default=60)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--random-seed", type=int, default=8160)
    parser.add_argument("--canonical-sides", action="store_true")
    args = parser.parse_args()
    roles = tuple(args.role) if args.role else GOODS
    result = run(args.output, args.form_index, roles, args.edge_cap,
                 args.maximum_rounds, args.timeout_seconds, args.random_seed,
                 args.canonical_sides)
    print(json.dumps({
        "status": result["status"],
        "per_role": {r: o["status"] for r, o in result["per_role"].items()},
    }, indent=2))


if __name__ == "__main__":
    main()
