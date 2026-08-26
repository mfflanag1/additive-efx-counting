#!/usr/bin/env python3
"""Independent CP-SAT verification of the four-edge obstruction.

Shares with the primary audit only the declared form-2 premise builder (for
the admissibility replay) and the public role/owner/supplier labels.  It
rebuilds the two-good realization from the pinned side pattern with Fraction
arithmetic, decides every row of the verdict matrix with OR-tools CP-SAT over
integer-scaled values (a different solver technology from the primary z3
Boolean encoding), and rechecks the five-edge certificate exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import z3
from ortools.sat.python import cp_model

from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE

SUPPLIER = {role: source for source, roles in SUPPORT_STATE.items() for role in roles}


def load_rows(raw, stem):
    return {o: {r: Fraction(v) for r, v in row.items()} for o, row in raw[f"terminal_profile_{stem}"].items()}


def rebuild(totals, minima, pattern):
    values, role_goods = {}, {}
    for role in GOODS:
        if all(totals[o][role] == minima[o][role] for o in OWNERS):
            role_goods[role] = (f"{role}:0",)
            for o in OWNERS:
                values[o, f"{role}:0"] = totals[o][role]
            continue
        role_goods[role] = (f"{role}:0", f"{role}:1")
        for o in OWNERS:
            side = pattern.get(f"{role}:{o}", 0)
            low = minima[o][role] + (totals[o][role] - 2 * minima[o][role]) * side
            values[o, f"{role}:0"] = low
            values[o, f"{role}:1"] = totals[o][role] - low
            assert min(values[o, g] for g in role_goods[role]) == minima[o][role]
            assert sum(values[o, g] for g in role_goods[role]) == totals[o][role]
    return values, role_goods


def exact_check(values, role_goods, allocation, edge_cap, split_cap):
    goods = [g for gs in role_goods.values() for g in gs]
    assert sorted(g for b in allocation.values() for g in b) == sorted(goods)
    owner = {g: o for o, b in allocation.items() for g in b}
    edges = {(SUPPLIER[g.split(":")[0]], owner[g]) for g in goods if SUPPLIER[g.split(":")[0]] != owner[g]}
    splits = [role for role, gs in role_goods.items() if len({owner[g] for g in gs}) > 1]
    assert edge_cap is None or len(edges) <= edge_cap
    assert split_cap is None or len(splits) <= split_cap
    for i in OWNERS:
        own = sum((values[i, g] for g in allocation[i]), Fraction())
        for j in OWNERS:
            if j == i:
                continue
            total = sum((values[i, g] for g in allocation[j]), Fraction())
            for g in allocation[j]:
                assert own >= total - values[i, g], (i, j, g)
    return sorted(edges), sorted(splits)


def cpsat_decide(values, role_goods, split_cap, edge_cap, time_limit):
    goods = [g for gs in role_goods.values() for g in gs]
    den = 1
    for v in values.values():
        den = den * v.denominator // math.gcd(den, v.denominator)
    iv = {k: int(v * den) for k, v in values.items()}
    model = cp_model.CpModel()
    x = {(g, o): model.NewBoolVar(f"x_{g}_{o}") for g in goods for o in OWNERS}
    for g in goods:
        model.AddExactlyOne(x[g, o] for o in OWNERS)
    for o in OWNERS:
        model.AddBoolOr([x[g, o] for g in goods])
    if edge_cap is not None:
        flags = []
        for source in SUPPORT_STATE:
            sg = [g for g in goods if SUPPLIER[g.split(":")[0]] == source]
            for o in OWNERS:
                if o != source:
                    flag = model.NewBoolVar(f"e_{source}_{o}")
                    flags.append(flag)
                    for g in sg:
                        model.AddImplication(x[g, o], flag)
        model.Add(sum(flags) <= edge_cap)
    if split_cap is not None:
        sflags = []
        for role, gs in role_goods.items():
            if len(gs) >= 2:
                flag = model.NewBoolVar(f"s_{role}")
                sflags.append(flag)
                for o in OWNERS:
                    for g in gs[1:]:
                        model.AddBoolOr([x[g, o].Not(), x[gs[0], o], flag])
                        model.AddBoolOr([x[g, o], x[gs[0], o].Not(), flag])
        model.Add(sum(sflags) <= split_cap)
    for i in OWNERS:
        utility = {o: sum(iv[i, g] * x[g, o] for g in goods) for o in OWNERS}
        for j in OWNERS:
            if j == i:
                continue
            for g in goods:
                model.Add(utility[i] >= utility[j] - iv[i, g]).OnlyEnforceIf(x[g, j])
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_workers = 4
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return "sat", {o: [g for g in goods if solver.Value(x[g, o])] for o in OWNERS}
    return {cp_model.INFEASIBLE: "unsat", cp_model.UNKNOWN: "unknown"}.get(status, str(status)), None


def q(value):
    value = Fraction(value)
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def replay_master(totals, minima):
    solver, total, minimum = build_physical_master(2)
    for o in OWNERS:
        for role in GOODS:
            solver.add(total[role, o] == q(totals[o][role]), minimum[role, o] == q(minima[o][role]))
    return str(solver.check())


def run(profile_path, primary_path, output_path, time_limit):
    raw = json.loads(profile_path.read_text())
    totals, minima = load_rows(raw, "totals"), load_rows(raw, "minima")
    primary = json.loads(primary_path.read_text())
    assert primary["status"] == "SAT_FOUR_EDGE_DECLARATION_OBSTRUCTION"
    master = replay_master(totals, minima)
    assert master == "sat"
    values, role_goods = rebuild(totals, minima, primary["minimal_obstruction_pattern"])
    for o in OWNERS:
        for g, v in primary["physical_values"][o].items():
            assert Fraction(v) == values[o, g], (o, g)
    matrix = []
    for edge_cap, split_cap, expected in ((3, None, "unsat"), (4, None, "unsat"), (4, 4, "unsat"),
                                          (4, 0, "unsat"), (5, 0, "sat"), (5, None, "sat")):
        status, allocation = cpsat_decide(values, role_goods, split_cap, edge_cap, time_limit)
        assert status == expected, (edge_cap, split_cap, status)
        row = {"edge_cap": edge_cap, "split_cap": split_cap, "status": status}
        if allocation:
            edges, splits = exact_check(values, role_goods, allocation, edge_cap, split_cap)
            row.update({"allocation": allocation, "edges": [list(e) for e in edges], "split_roles": splits})
        matrix.append(row)
    primary_cert = next(r for r in primary["verdict_matrix"] if r["edge_cap"] == 5 and r["split_cap"] == 0)
    edges, splits = exact_check(values, role_goods, primary_cert["allocation"], 5, 0)
    result = {
        "schema": "fixed-u-four-edge-obstruction-independent-audit-v1",
        "status": "AUDIT_PASS_FOUR_EDGE_DECLARATION_REFUTED_FIVE_EDGES_ZERO_SPLITS_SUFFICE",
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "primary_audit": str(primary_path),
        "primary_audit_sha256": hashlib.sha256(primary_path.read_bytes()).hexdigest(),
        "master_replay_status": master,
        "pattern": primary["minimal_obstruction_pattern"],
        "cpsat_verdict_matrix": matrix,
        "primary_five_edge_certificate_recheck": {"edges": [list(e) for e in edges], "split_roles": splits},
        "method": "CP-SAT integer-scaled Boolean owner encoding plus exact Fraction certificate recheck",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--primary-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--time-limit", type=int, default=120)
    args = parser.parse_args()
    result = run(args.profile, args.primary_audit, args.output, args.time_limit)
    print(json.dumps({"status": result["status"], "matrix": [(r["edge_cap"], r["split_cap"], r["status"]) for r in result["cpsat_verdict_matrix"]]}, indent=2))


if __name__ == "__main__":
    main()
