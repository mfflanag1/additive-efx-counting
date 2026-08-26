#!/usr/bin/env python3
"""For every exact response relation of the chart: is every valuation in the cell closed by a
complete EFX allocation (12 atomic goods to the four owners, no charity, unrestricted edges)?

Per cell CEGAR on the rank-three master restricted to the cell:
   master AND relation==E AND (no menu allocation is EFX)  -> valuation
   decide complete EFX at that valuation (integer-owner SMT)  -> allocation, added as a linear cut
UNSAT closes the cell for all its valuations; an UNSAT allocation decision is an exact residual
valuation with no complete EFX allocation (a 4-agent/12-good EFX obstruction candidate).
Also reports the minimal support-transfer edge count (from SUPPORT_STATE) of the closing menu.
"""
from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master, response_edges, TARGETS
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE

NONSELF = tuple((s, t) for s in OWNERS for t in TARGETS if t != s)
SUPPLIER = {g: src for src, goods in SUPPORT_STATE.items() for g in goods}


def q(v):
    v = Fraction(v)
    return z3.RealVal(f"{v.numerator}/{v.denominator}")


def zfrac(v):
    return Fraction(v.as_long()) if z3.is_int_value(v) else Fraction(v.as_fraction())


def decide_complete_efx(vals, edge_cap, timeout):
    owner = {g: z3.Int(f"o_{g}") for g in GOODS}
    s = z3.Solver(); s.set(timeout=timeout * 1000)
    s.add(*(z3.And(owner[g] >= 0, owner[g] < 4) for g in GOODS))
    if edge_cap is not None:
        flags = []
        for src in SUPPORT_STATE:
            for i, t in enumerate(OWNERS):
                if src != t:
                    flags.append(z3.Or(*(owner[g] == i for g in SUPPORT_STATE[src])))
        s.add(z3.PbLe([(f, 1) for f in flags], edge_cap))
    for oi, o in enumerate(OWNERS):
        util = {i: z3.Sum(*(z3.If(owner[g] == i, q(vals[g, o]), z3.RealVal(0)) for g in GOODS)) for i in range(4)}
        for ti in range(4):
            if ti == oi:
                continue
            for g in GOODS:
                s.add(z3.Implies(owner[g] == ti, util[oi] >= util[ti] - q(vals[g, o])))
    st = s.check()
    if st != z3.sat:
        return str(st), None
    m = s.model()
    return "sat", {t: [g for g in GOODS if m.eval(owner[g]).as_long() == i] for i, t in enumerate(OWNERS)}


def audit(alloc, vals):
    assert sorted(g for b in alloc.values() for g in b) == sorted(GOODS)
    for o in OWNERS:
        own = sum((vals[g, o] for g in alloc[o]), Fraction())
        for t in OWNERS:
            if t == o:
                continue
            tot = sum((vals[g, o] for g in alloc[t]), Fraction())
            for g in alloc[t]:
                assert own >= tot - vals[g, o]
    return len({(SUPPLIER[g], t) for t, b in alloc.items() for g in b if SUPPLIER[g] != t})


def efx_cut(alloc, value):
    conds = []
    for o in OWNERS:
        own = z3.Sum(*(value[g, o] for g in alloc[o])) if alloc[o] else z3.RealVal(0)
        for t in OWNERS:
            if t == o or not alloc[t]:
                continue
            tot = z3.Sum(*(value[g, o] for g in alloc[t]))
            for g in alloc[t]:
                conds.append(own >= tot - value[g, o])
    return z3.And(*conds)


def close_cell(E, timeout, max_rounds, edge_cap=None):
    solver, value = build_rank_three_master(exclude_self_responses=True)
    solver.set(timeout=timeout * 1000)
    edge = response_edges(value, SUPPORT_STATE, include_current=True, exclude_self=True)
    solver.add(z3.And(*(edge[e] if e in E else z3.Not(edge[e]) for e in NONSELF)))
    menu, edges_used = [], []
    t0 = time.time()
    for it in range(max_rounds):
        v = solver.check()
        if v == z3.unsat:
            return {"status": "CLOSED", "menu": menu, "menu_size": len(menu), "max_edges_used": max(edges_used) if edges_used else 0,
                    "rounds": it, "seconds": round(time.time() - t0, 1)}
        if v == z3.unknown:
            return {"status": "MASTER_UNKNOWN", "reason": solver.reason_unknown(), "menu": menu, "rounds": it, "seconds": round(time.time() - t0, 1)}
        m = solver.model()
        vals = {(g, o): zfrac(m.eval(value[g, o], model_completion=True)) for g in GOODS for o in OWNERS}
        st, alloc = None, None
        for cap in ([1, 2, 3, 4] if edge_cap is None else list(range(1, edge_cap + 1))) + [edge_cap]:
            st, alloc = decide_complete_efx(vals, cap, timeout)
            if st == "sat":
                break
        if st != "sat":
            return {"status": "RESIDUAL_NO_COMPLETE_EFX" if st == "unsat" else "ORACLE_UNKNOWN",
                    "witness": {f"{g}:{o}": str(vals[g, o]) for g in GOODS for o in OWNERS}, "menu": menu,
                    "rounds": it, "seconds": round(time.time() - t0, 1)}
        edges_used.append(audit(alloc, vals))
        menu.append(alloc)
        solver.add(z3.Not(efx_cut(alloc, value)))
    return {"status": "ROUND_LIMIT", "menu": menu, "rounds": max_rounds, "seconds": round(time.time() - t0, 1)}


def work(args):
    r, timeout, max_rounds, edge_cap = args
    E = {tuple(e) for e in r["edges"]}
    res = close_cell(E, timeout, max_rounds, edge_cap)
    res.update({"key": r["key"], "rank": r["rank"], "edge_count": r["edge_count"], "corrected_form_index": r["corrected_form_index"]})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chart", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--timeout-seconds", type=int, default=300)
    ap.add_argument("--max-rounds", type=int, default=400)
    ap.add_argument("--edge-cap", type=int, default=None)
    ap.add_argument("--only", type=str, default=None, help="comma-separated relation keys")
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    chart = json.loads(a.chart.read_text())
    rows = chart["relations"]
    if a.only:
        keep = set(a.only.split(","))
        rows = [r for r in rows if r["key"] in keep]
    out = []
    from multiprocessing import Pool
    jobs = [(r, a.timeout_seconds, a.max_rounds, a.edge_cap) for r in rows]
    with Pool(a.workers) as pool:
        for res in pool.imap_unordered(work, jobs):
            out.append(res)
            print(res["key"], res["status"], res.get("menu_size"), res.get("max_edges_used"), res.get("rounds"), res["seconds"], flush=True)
            a.output.write_text(json.dumps({"edge_cap": a.edge_cap, "cells": out}, indent=1) + "\n")


if __name__ == "__main__":
    main()
