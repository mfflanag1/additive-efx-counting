#!/usr/bin/env python3
"""Independent Boolean piece-placement verifier for one realization cell.

Shares no solver code with fixed_u_universal_split (which uses integer owners).
Each good g and owner t get a Boolean place[g,t]; exactly one owner per good;
edge and split counts are cardinality constraints on Booleans; EFX is written
with explicit per-observer bundle sums.  Also re-derives the cell's good values
from the profile and checks that every observer's minimum is attained.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import z3

OWNERS = ("r", "q", "d", "s")
GOODS = ("a0", "a1", "h", "j", "k", "q0", "l", "e", "m", "gq", "gr", "p")
SUPPLIER = {"a0": "r", "a1": "r", "h": "r", "j": "q", "k": "q", "q0": "q",
            "m": "d", "gq": "d", "gr": "d", "l": "s", "e": "s", "p": "charity"}


def rat(v):
    v = Fraction(v)
    return z3.RealVal(f"{v.numerator}/{v.denominator}")


def realization(totals, minima, cell):
    """cell: {'role:observer': bit}. Returns per-observer good values and good list."""
    goods, values = [], {}
    for role in GOODS:
        single = all(totals[o][role] == minima[o][role] for o in OWNERS)
        names = [f"{role}:0"] if single else [f"{role}:0", f"{role}:1"]
        goods += names
        for o in OWNERS:
            T, M = totals[o][role], minima[o][role]
            if single:
                values[o, names[0]] = T
            else:
                assert 2 * M <= T
                b = cell[f"{role}:{o}"]
                values[o, names[0]] = T - M if b else M
                values[o, names[1]] = M if b else T - M
                assert min(values[o, n] for n in names) == M and sum(values[o, n] for n in names) == T
    return goods, values


def decide(goods, values, split_cap, edge_cap, timeout_seconds):
    place = {(g, t): z3.Bool(f"place_{g.replace(':', '_')}_{t}") for g in goods for t in OWNERS}
    s = z3.Solver()
    s.set(timeout=timeout_seconds * 1000)
    for g in goods:
        s.add(z3.PbEq([(place[g, t], 1) for t in OWNERS], 1))
    edge_used = {}
    for g in goods:
        src = SUPPLIER[g.split(":")[0]]
        for t in OWNERS:
            if t != src:
                edge_used.setdefault((src, t), []).append(place[g, t])
    edge_bools = [z3.Or(*lits) for lits in edge_used.values()]
    s.add(z3.PbLe([(b, 1) for b in edge_bools], edge_cap))
    roles = {}
    for g in goods:
        roles.setdefault(g.split(":")[0], []).append(g)
    split_bools = []
    for members in roles.values():
        if len(members) == 2:
            a, b = members
            split_bools.append(z3.Or(*(z3.And(place[a, t], z3.Not(place[b, t])) for t in OWNERS)))
    if split_bools:
        s.add(z3.PbLe([(b, 1) for b in split_bools], split_cap))
    for o in OWNERS:
        bundle = {t: z3.Sum(*(z3.If(place[g, t], rat(values[o, g]), z3.RealVal(0)) for g in goods)) for t in OWNERS}
        for t in OWNERS:
            if t == o:
                continue
            for g in goods:
                s.add(z3.Implies(place[g, t], bundle[o] >= bundle[t] - rat(values[o, g])))
    st = s.check()
    if st != z3.sat:
        return str(st), None
    m = s.model()
    alloc = {t: [g for g in goods if z3.is_true(m.eval(place[g, t], model_completion=True))] for t in OWNERS}
    return "sat", alloc


def audit(alloc, goods, values, split_cap, edge_cap):
    placed = [g for b in alloc.values() for g in b]
    assert sorted(placed) == sorted(goods)
    edges = {(SUPPLIER[g.split(":")[0]], t) for t, b in alloc.items() for g in b if SUPPLIER[g.split(":")[0]] != t}
    assert len(edges) <= edge_cap
    split = 0
    for role in GOODS:
        owners = {t for t, b in alloc.items() for g in b if g.split(":")[0] == role}
        split += len(owners) > 1
    assert split <= split_cap
    for o in OWNERS:
        own = sum((values[o, g] for g in alloc[o]), Fraction())
        for t in OWNERS:
            if t == o:
                continue
            tot = sum((values[o, g] for g in alloc[t]), Fraction())
            for g in alloc[t]:
                assert own >= tot - values[o, g]
    return sorted(edges), split


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", type=Path, required=True)
    ap.add_argument("--cell-json", type=Path, required=True, help="oracle output containing obstructing_cell")
    ap.add_argument("--timeout-seconds", type=int, default=120)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    raw = json.loads(a.profile.read_text())
    key = "terminal_profile_totals" if "terminal_profile_totals" in raw else "profile_totals"
    totals = {o: {r: Fraction(v) for r, v in row.items()} for o, row in raw[key].items()}
    minima = {o: {r: Fraction(v) for r, v in row.items()} for o, row in raw[key.replace("totals", "minima")].items()}
    cell = json.loads(a.cell_json.read_text())["obstructing_cell"]
    goods, values = realization(totals, minima, cell)
    table = {}
    for edge_cap in (4, 5):
        for split_cap in (0, len(goods)):
            st, alloc = decide(goods, values, split_cap, edge_cap, a.timeout_seconds)
            row = {"status": st}
            if alloc is not None:
                edges, split = audit(alloc, goods, values, split_cap, edge_cap)
                row.update({"allocation": alloc, "edges": [list(e) for e in edges], "split_roles_used": split})
            table[f"edge{edge_cap}_split{split_cap}"] = row
    out = {"schema": "fixed-u-universal-split-cell-independent-audit-v1", "profile": str(a.profile),
           "cell": cell, "good_count": len(goods),
           "values": {o: {g: str(values[o, g]) for g in goods} for o in OWNERS}, "table": table,
           "method": "Boolean piece-placement encoding, PbEq/PbLe cardinalities, explicit bundle sums; no import of the integer-owner oracle"}
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "allocation"} for k, v in table.items()}, indent=1))
    if a.output:
        a.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
