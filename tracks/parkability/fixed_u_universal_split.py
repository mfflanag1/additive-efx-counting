#!/usr/bin/env python3
"""Universal k-split oracle over every two-good realization of a form-2 profile.

A realization cell assigns, for every multi-good role and every observer, which
of the role's two goods carries that observer's minimum (side bit).  Observer o's
EFX inequalities depend only on o's own bits, but the allocation must be common.

universal_decide(profile, split_cap, edge_cap) runs the quantifier
    for every cell there exists a complete EFX allocation with <= edge_cap
    support-transfer edges and <= split_cap split roles
as a CEGAR: decide one cell (integer-owner SMT), add the allocation to a menu,
ask exact SMT for a cell that NO menu allocation closes, repeat.  CLOSED means
the final uncovered-cell query is UNSAT (a proof over all 2^(4*multiroles)
cells); OBSTRUCTED returns a cell whose SPLIT_k decision is UNSAT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE

SUPPLIER = {role: source for source, roles in SUPPORT_STATE.items() for role in roles}


def q(value):
    value = Fraction(value)
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def load_profile(path):
    raw = json.loads(Path(path).read_text())
    for tot, mini in (("profile_totals", "profile_minima"),
                      ("terminal_profile_totals", "terminal_profile_minima"),
                      ("totals", "minima")):
        if tot in raw and mini in raw:
            totals = {o: {r: Fraction(v) for r, v in row.items()} for o, row in raw[tot].items()}
            minima = {o: {r: Fraction(v) for r, v in row.items()} for o, row in raw[mini].items()}
            return totals, minima
    if "round" in raw:
        return load_rows(raw["round"])
    raise ValueError(f"no profile in {path}")


def load_rows(round_):
    totals = {o: {r: Fraction(v) for r, v in row.items()} for o, row in round_["totals"].items()}
    minima = {o: {r: Fraction(v) for r, v in row.items()} for o, row in round_["minima"].items()}
    return totals, minima


def check_admissible_shape(totals, minima):
    for role in GOODS:
        single = all(totals[o][role] == minima[o][role] for o in OWNERS)
        multi = all(2 * minima[o][role] <= totals[o][role] for o in OWNERS)
        assert single or multi, ("role neither singleton nor multi", role)
        assert all(minima[o][role] > 0 for o in OWNERS), ("nonpositive minimum", role)


def multi_roles(totals, minima):
    return tuple(r for r in GOODS if not all(totals[o][r] == minima[o][r] for o in OWNERS))


def role_goods(totals, minima):
    return {r: ((f"{r}:0", f"{r}:1") if r in multi_roles(totals, minima) else (f"{r}:0",)) for r in GOODS}


def cell_values(totals, minima, cell):
    """cell: {(role, observer): bit}; bit 0 -> good0 carries the minimum."""
    values = {}
    for role, goods in role_goods(totals, minima).items():
        for o in OWNERS:
            T, M = totals[o][role], minima[o][role]
            if len(goods) == 1:
                values[o, goods[0]] = T
            else:
                low, high = M, T - M
                if cell[role, o]:
                    low, high = high, low
                values[o, goods[0]] = low
                values[o, goods[1]] = high
    return values


NEGATIVE_CONTROL = {"mode": None}  # "drop-charity-edge": deliberately broken edge count (calibration only)


def decide_cell(totals, minima, cell, split_cap, edge_cap, timeout_seconds=60):
    """Integer-owner SMT: complete EFX allocation of the cell's goods."""
    goods_by_role = role_goods(totals, minima)
    values = cell_values(totals, minima, cell)
    goods = tuple(g for r in GOODS for g in goods_by_role[r])
    owner = {g: z3.Int(f"owner_{g.replace(':', '_')}") for g in goods}
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(*(z3.And(owner[g] >= 0, owner[g] < len(OWNERS)) for g in goods))
    edge_flags = []
    for source in SUPPORT_STATE:
        if NEGATIVE_CONTROL["mode"] == "drop-charity-edge" and source == "charity":
            continue
        source_goods = [g for g in goods if SUPPLIER[g.split(":", 1)[0]] == source]
        for index, target in enumerate(OWNERS):
            if source != target:
                edge_flags.append(z3.Or(*(owner[g] == index for g in source_goods)))
    solver.add(z3.PbLe([(f, 1) for f in edge_flags], edge_cap))
    split_flags = [owner[m[0]] != owner[m[1]] for m in goods_by_role.values() if len(m) == 2]
    if split_flags:
        solver.add(z3.PbLe([(f, 1) for f in split_flags], split_cap))
    for oi, o in enumerate(OWNERS):
        util = {i: z3.Sum(*(z3.If(owner[g] == i, q(values[o, g]), z3.RealVal(0)) for g in goods))
                for i in range(len(OWNERS))}
        for ti in range(len(OWNERS)):
            if ti == oi:
                continue
            for g in goods:
                solver.add(z3.Implies(owner[g] == ti, util[oi] >= util[ti] - q(values[o, g])))
    status = solver.check()
    if status != z3.sat:
        return str(status), None, (solver.reason_unknown() if status == z3.unknown else None)
    model = solver.model()
    allocation = {t: [g for g in goods if model.eval(owner[g]).as_long() == i] for i, t in enumerate(OWNERS)}
    return "sat", allocation, None


def allocation_stats(allocation, goods_by_role):
    edges = sorted({(SUPPLIER[g.split(":", 1)[0]], t) for t, bundle in allocation.items()
                    for g in bundle if SUPPLIER[g.split(":", 1)[0]] != t})
    split = sorted(r for r, members in goods_by_role.items()
                   if len({t for t, b in allocation.items() if set(members) & set(b)}) > 1)
    return edges, split


def audit_allocation(totals, minima, cell, allocation, split_cap, edge_cap):
    """Exact Fraction re-check of one allocation on one cell (no solver)."""
    goods_by_role = role_goods(totals, minima)
    values = cell_values(totals, minima, cell)
    all_goods = [g for b in allocation.values() for g in b]
    assert sorted(all_goods) == sorted(g for r in GOODS for g in goods_by_role[r])
    edges, split = allocation_stats(allocation, goods_by_role)
    if NEGATIVE_CONTROL["mode"] is None:
        assert len(edges) <= edge_cap and len(split) <= split_cap
    for o in OWNERS:
        own = sum((values[o, g] for g in allocation[o]), Fraction())
        for t in OWNERS:
            if t == o:
                continue
            tot = sum((values[o, g] for g in allocation[t]), Fraction())
            for g in allocation[t]:
                assert own >= tot - values[o, g], (o, t, g)
    return edges, split


def uncovered_cell(totals, minima, menu, timeout_seconds=60):
    """Exact SMT over side bits: a cell that no allocation of the menu closes."""
    mroles = multi_roles(totals, minima)
    goods_by_role = role_goods(totals, minima)
    bit = {(r, o): z3.Bool(f"bit_{r}_{o}") for r in mroles for o in OWNERS}
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)

    def val(o, g):
        role, idx = g.split(":", 1)
        T, M = totals[o][role], minima[o][role]
        if len(goods_by_role[role]) == 1:
            return q(T)
        low, high = q(M), q(T - M)
        if idx == "0":
            return z3.If(bit[role, o], high, low)
        return z3.If(bit[role, o], low, high)

    for allocation in menu:
        conds = []
        for o in OWNERS:
            own = z3.Sum(*(val(o, g) for g in allocation[o])) if allocation[o] else z3.RealVal(0)
            for t in OWNERS:
                if t == o or not allocation[t]:
                    continue
                tot = z3.Sum(*(val(o, g) for g in allocation[t]))
                for g in allocation[t]:
                    conds.append(own >= tot - val(o, g))
        solver.add(z3.Not(z3.And(*conds)))
    status = solver.check()
    if status == z3.unsat:
        return "unsat", None, None
    if status == z3.unknown:
        return "unknown", None, solver.reason_unknown()
    model = solver.model()
    cell = {(r, o): (1 if z3.is_true(model.eval(bit[r, o], model_completion=True)) else 0)
            for r in mroles for o in OWNERS}
    return "sat", cell, None


def cell_key(cell):
    return {f"{r}:{o}": b for (r, o), b in sorted(cell.items())}


def universal_decide(totals, minima, split_cap, edge_cap, timeout_seconds=60,
                     max_rounds=400, log=None):
    check_admissible_shape(totals, minima)
    mroles = multi_roles(totals, minima)
    goods_by_role = role_goods(totals, minima)
    menu, rounds = [], []
    cell = {(r, o): 0 for r in mroles for o in OWNERS}
    t0 = time.time()
    for it in range(max_rounds):
        status, allocation, reason = decide_cell(totals, minima, cell, split_cap, edge_cap, timeout_seconds)
        row = {"iteration": it, "cell": cell_key(cell), "cell_status": status}
        if status == "unsat":
            rounds.append(row)
            return {"status": "OBSTRUCTED", "split_cap": split_cap, "edge_cap": edge_cap,
                    "obstructing_cell": cell_key(cell), "menu": menu, "rounds": rounds,
                    "multi_roles": list(mroles), "seconds": time.time() - t0}
        if status != "sat":
            row["reason"] = reason
            rounds.append(row)
            return {"status": "UNKNOWN", "split_cap": split_cap, "edge_cap": edge_cap,
                    "cell": cell_key(cell), "menu": menu, "rounds": rounds, "seconds": time.time() - t0}
        edges, split = audit_allocation(totals, minima, cell, allocation, split_cap, edge_cap)
        menu.append(allocation)
        row.update({"edges": [list(e) for e in edges], "split_roles": split})
        ustatus, ncell, ureason = uncovered_cell(totals, minima, menu, timeout_seconds)
        row["uncovered_status"] = ustatus
        rounds.append(row)
        if log:
            log(f"  it={it} split={split} edges={len(edges)} menu={len(menu)} uncovered={ustatus} t={time.time()-t0:.0f}s")
        if ustatus == "unsat":
            return {"status": "CLOSED", "split_cap": split_cap, "edge_cap": edge_cap,
                    "menu": menu, "menu_size": len(menu), "rounds": rounds,
                    "max_split_used": max((len(r.get("split_roles", [])) for r in rounds), default=0),
                    "multi_roles": list(mroles), "seconds": time.time() - t0}
        if ustatus == "unknown":
            return {"status": "UNKNOWN", "split_cap": split_cap, "edge_cap": edge_cap,
                    "reason": ureason, "menu": menu, "rounds": rounds, "seconds": time.time() - t0}
        cell = ncell
    return {"status": "ROUND_LIMIT", "split_cap": split_cap, "edge_cap": edge_cap,
            "menu": menu, "rounds": rounds, "seconds": time.time() - t0}


def minimal_split_on_cell(totals, minima, cell, edge_cap, timeout_seconds=60, max_split=None):
    """Smallest split cap closing one cell at the given edge cap (None if none)."""
    mroles = multi_roles(totals, minima)
    top = len(mroles) if max_split is None else max_split
    out = []
    for k in range(top + 1):
        status, allocation, reason = decide_cell(totals, minima, cell, k, edge_cap, timeout_seconds)
        out.append({"split_cap": k, "status": status})
        if status == "sat":
            return k, out
        if status == "unknown":
            out[-1]["reason"] = reason
            return None, out
    return None, out


def escalate(totals, minima, cell, timeout_seconds=60):
    """Split-count x edge-cap table for one obstructing cell."""
    mroles = multi_roles(totals, minima)
    table = {}
    for edge_cap in (4, 5, 6, 8, 16):
        k, attempts = minimal_split_on_cell(totals, minima, cell, edge_cap, timeout_seconds)
        table[str(edge_cap)] = {"minimal_split": k, "attempts": attempts}
    cap_free_status, allocation, reason = decide_cell(totals, minima, cell, len(mroles), 16, timeout_seconds)
    table["cap_free"] = {"status": cap_free_status, "reason": reason}
    return table


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--split-cap", type=int, default=4)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--max-rounds", type=int, default=400)
    parser.add_argument("--escalate", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--negative-control", choices=["drop-charity-edge"], default=None)
    args = parser.parse_args()
    NEGATIVE_CONTROL["mode"] = args.negative_control
    totals, minima = load_profile(args.profile)
    result = universal_decide(totals, minima, args.split_cap, args.edge_cap,
                              args.timeout_seconds, args.max_rounds, log=lambda s: print(s, flush=True))
    result["profile"] = str(args.profile)
    result["negative_control"] = args.negative_control
    result["profile_sha256"] = hashlib.sha256(args.profile.read_bytes()).hexdigest()
    if args.escalate and result["status"] == "OBSTRUCTED":
        cell = {tuple(k.split(":")): v for k, v in result["obstructing_cell"].items()}
        result["escalation"] = escalate(totals, minima, cell, args.timeout_seconds)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    summary = {k: result.get(k) for k in ("status", "split_cap", "edge_cap", "menu_size", "max_split_used", "seconds", "obstructing_cell", "escalation")}
    print(json.dumps(summary, indent=1, default=str))
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + "\n")


if __name__ == "__main__":
    main()
