#!/usr/bin/env python3
"""Independent audit of the first genuine wild-and-forced chart profile."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")
SUPPORT = {
    "r": ("a0", "a1", "h"),
    "q": ("j", "k", "q0"),
    "d": ("m", "gq", "gr"),
    "s": ("l", "e"),
    "charity": ("p",),
}
ROLES = tuple(role for roles in SUPPORT.values() for role in roles)


def load_rows(raw, key):
    return {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in raw[key].items()
    }


def physicalize(totals, minima):
    values, role_goods = {}, {}
    for role in ROLES:
        singleton = all(totals[o][role] == minima[o][role] for o in OWNERS)
        goods = (f"{role}:0",) if singleton else (f"{role}:0", f"{role}:1")
        role_goods[role] = goods
        for observer in OWNERS:
            values[observer, goods[0]] = minima[observer][role]
            if not singleton:
                values[observer, goods[1]] = totals[observer][role] - minima[observer][role]
                assert values[observer, goods[1]] >= values[observer, goods[0]] > 0
    return values, role_goods


def independent_decision(values, role_goods, wild_roles, forbid_wild_split):
    goods = tuple(g for role in ROLES for g in role_goods[role])
    supplier = {role: source for source, roles in SUPPORT.items() for role in roles}
    x = {(good, owner): z3.Bool(f"ia_{good.replace(':', '_')}_{owner}")
         for good in goods for owner in OWNERS}
    edge = {(source, target): z3.Bool(f"ia_edge_{source}_{target}")
            for source in SUPPORT for target in OWNERS if source != target}
    solver = z3.Solver()
    for good in goods:
        solver.add(z3.PbEq([(x[good, owner], 1) for owner in OWNERS], 1))
        source = supplier[good.split(":")[0]]
        for target in OWNERS:
            if target != source:
                solver.add(z3.Implies(x[good, target], edge[source, target]))
    solver.add(z3.PbLe([(flag, 1) for flag in edge.values()], 4))
    if forbid_wild_split:
        for role in wild_roles:
            if len(role_goods[role]) == 2:
                low, high = role_goods[role]
                for owner in OWNERS:
                    solver.add(x[low, owner] == x[high, owner])

    def rv(amount):
        return z3.RealVal(f"{amount.numerator}/{amount.denominator}")

    utility = {
        (observer, target): z3.Sum(*(
            z3.If(x[good, target], rv(values[observer, good]), z3.RealVal(0))
            for good in goods
        ))
        for observer in OWNERS for target in OWNERS
    }
    for observer in OWNERS:
        for target in OWNERS:
            if target == observer:
                continue
            for good in goods:
                solver.add(z3.Implies(
                    x[good, target],
                    utility[observer, observer] >= utility[observer, target]
                    - rv(values[observer, good]),
                ))
    status = solver.check()
    return str(status)


def audit_frozen_repair(repair, values, role_goods, wild_roles):
    allocation = repair["terminal"]["allocation"]
    all_goods = {g for goods in role_goods.values() for g in goods}
    placed = [g for goods in allocation.values() for g in goods]
    assert len(placed) == len(set(placed)) and set(placed) == all_goods
    supplier = {role: source for source, roles in SUPPORT.items() for role in roles}
    edges = sorted({
        (supplier[good.split(":")[0]], owner)
        for owner, goods in allocation.items() for good in goods
        if supplier[good.split(":")[0]] != owner
    })
    assert len(edges) <= 4
    split_roles = []
    for role, goods in role_goods.items():
        holders = {
            owner for owner, bundle in allocation.items() if set(goods) & set(bundle)
        }
        if len(holders) > 1:
            split_roles.append(role)
    assert split_roles == repair["terminal"]["split_roles"] == ["a1"]
    assert split_roles[0] in wild_roles
    minimum_slack = None
    for observer in OWNERS:
        own = sum((values[observer, g] for g in allocation[observer]), Fraction())
        for target in OWNERS:
            if target == observer:
                continue
            gross = sum((values[observer, g] for g in allocation[target]), Fraction())
            for good in allocation[target]:
                slack = own - (gross - values[observer, good])
                assert slack >= 0, (observer, target, good, slack)
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
    return edges, split_roles, minimum_slack


def run(profile_path, repair_path, output_path):
    profile = json.loads(profile_path.read_text())
    repair = json.loads(repair_path.read_text())
    assert profile["status"] == "SAT_NO_TAME_COVERING_MENU_FOR_THIS_PROFILE"
    assert profile["halt_reason"] == "wide_family_failed"
    totals = load_rows(profile, "profile_totals")
    minima = load_rows(profile, "profile_minima")
    slacks = {
        role: min(totals[o][role] // minima[o][role] for o in OWNERS)
        for role in ROLES
    }
    wild = tuple(role for role in ROLES if slacks[role] >= 3)
    tame = tuple(role for role in ROLES if slacks[role] == 2)
    values, role_goods = physicalize(totals, minima)
    no_wild_status = independent_decision(
        values, role_goods, wild, forbid_wild_split=True
    )
    unrestricted_status = independent_decision(
        values, role_goods, wild, forbid_wild_split=False
    )
    assert no_wild_status == "unsat"
    assert unrestricted_status == "sat"
    edges, split_roles, minimum_slack = audit_frozen_repair(
        repair, values, role_goods, wild
    )
    result = {
        "schema": "fixed-u-wild-forced-terminal-independent-audit-v1",
        "status": "AUDIT_PASS",
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "repair_sha256": hashlib.sha256(repair_path.read_bytes()).hexdigest(),
        "wild_roles": list(wild),
        "tame_roles": list(tame),
        "role_slacks": {role: str(slack) for role, slack in slacks.items()},
        "canonical_physical_good_count": sum(map(len, role_goods.values())),
        "independent_no_wild_split_status": no_wild_status,
        "independent_unrestricted_status": unrestricted_status,
        "repair_split_roles": split_roles,
        "repair_edges": [list(edge) for edge in edges],
        "repair_minimum_efx_slack": str(minimum_slack),
        "claim_boundary": (
            "This independently refutes the tame-covering-menu conclusion for "
            "the frozen canonical realization and verifies its wild-role four-edge "
            "repair. It does not quantify over every realization of the wild roles "
            "and therefore neither proves nor refutes the universal fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--repair", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.profile, args.repair, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

