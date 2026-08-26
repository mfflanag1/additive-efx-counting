#!/usr/bin/env python3
"""Symbolic whole-role CEGAR over the complete declared form-2 physical-minimum master.

Question: does every admissible profile (totals/minima satisfying the master)
admit a complete EFX allocation that keeps every named role whole and uses at
most `edge_cap` support-transfer edges?  Whole-role EFX conditions are linear
in the profile (bundle totals versus totals minus a deleted role's minimum),
so every closing allocation is an exact cut on the master.  The loop
    master AND (no menu allocation is EFX)  ->  profile
    decide whole-role allocation on the profile  ->  cut or obstruction
terminates UNSAT (theorem: the finite menu closes the whole master) or at a
profile with no whole-role allocation under the cap (obstruction).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from itertools import product
from pathlib import Path

import z3

from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE
from .fixed_u_universal_split import load_rows

SUPPLIER = {role: src for src, roles in SUPPORT_STATE.items() for role in roles}


def q(v):
    v = Fraction(v)
    return z3.RealVal(f"{v.numerator}/{v.denominator}")


def zfrac(v):
    if z3.is_int_value(v):
        return Fraction(v.as_long())
    return Fraction(v.as_fraction())


def concrete(model, value, minimum):
    totals = {o: {r: zfrac(model.eval(value[r, o], model_completion=True)) for r in GOODS} for o in OWNERS}
    minima = {o: {r: zfrac(model.eval(minimum[r, o], model_completion=True)) for r in GOODS} for o in OWNERS}
    return totals, minima


def efx_whole(allocation, T, M, observer):
    """EFX inequalities of a whole-role allocation for one observer; T,M callables (role)->value."""
    conds = []
    own_expr = z3.Sum(*(T(r) for r in allocation[observer])) if allocation[observer] else z3.RealVal(0)
    for t in OWNERS:
        if t == observer or not allocation[t]:
            continue
        tot = z3.Sum(*(T(r) for r in allocation[t]))
        for r in allocation[t]:
            conds.append(own_expr >= tot - M(r))
    return conds


def decide_whole(totals, minima, edge_cap, timeout_seconds):
    owner = {r: z3.Int(f"w_{r}") for r in GOODS}
    s = z3.Solver()
    s.set(timeout=timeout_seconds * 1000)
    s.add(*(z3.And(owner[r] >= 0, owner[r] < len(OWNERS)) for r in GOODS))
    flags = []
    for src in SUPPORT_STATE:
        for i, t in enumerate(OWNERS):
            if src != t:
                flags.append(z3.Or(*(owner[r] == i for r in SUPPORT_STATE[src])))
    s.add(z3.PbLe([(f, 1) for f in flags], edge_cap))
    for oi, o in enumerate(OWNERS):
        util = {i: z3.Sum(*(z3.If(owner[r] == i, q(totals[o][r]), z3.RealVal(0)) for r in GOODS)) for i in range(len(OWNERS))}
        for ti in range(len(OWNERS)):
            if ti == oi:
                continue
            for r in GOODS:
                s.add(z3.Implies(owner[r] == ti, util[oi] >= util[ti] - q(minima[o][r])))
    st = s.check()
    if st != z3.sat:
        return str(st), None
    m = s.model()
    return "sat", {t: [r for r in GOODS if m.eval(owner[r]).as_long() == i] for i, t in enumerate(OWNERS)}


def audit_whole(allocation, totals, minima, edge_cap):
    assert sorted(r for b in allocation.values() for r in b) == sorted(GOODS)
    edges = {(SUPPLIER[r], t) for t, b in allocation.items() for r in b if SUPPLIER[r] != t}
    assert len(edges) <= edge_cap
    for o in OWNERS:
        own = sum((totals[o][r] for r in allocation[o]), Fraction())
        for t in OWNERS:
            if t == o:
                continue
            tot = sum((totals[o][r] for r in allocation[t]), Fraction())
            for r in allocation[t]:
                assert own >= tot - minima[o][r], (o, t, r)
    return sorted(edges)


def cut_formula(allocation, value, minimum):
    conds = []
    for o in OWNERS:
        conds += efx_whole(allocation, lambda r, o=o: value[r, o], lambda r, o=o: minimum[r, o], o)
    return z3.And(*conds)


def seeds_from_ledgers(paths):
    from .census_fixed_u_universal_split import profiles
    return [load_rows(r) for _, r in profiles(paths)]


def run(edge_cap, master_timeout, oracle_timeout, max_rounds, seed_ledgers, seed_profiles, out_path, ledger_path, log, resume_cuts=(), z3_seed=None):
    solver, value, minimum = build_physical_master(2)
    solver.set(timeout=master_timeout * 1000)
    if z3_seed is not None:
        solver.set("random_seed", z3_seed)
    seen_allocations = set()
    menu, records = [], []
    t0 = time.time()

    def install(allocation, origin, totals, minima):
        key = json.dumps(allocation, sort_keys=True)
        if key in seen_allocations:
            return
        seen_allocations.add(key)
        edges = audit_whole(allocation, totals, minima, edge_cap)
        solver.add(z3.Not(cut_formula(allocation, value, minimum)))
        menu.append(allocation)
        rec = {"index": len(menu) - 1, "origin": origin, "allocation": allocation,
               "edges": [list(e) for e in edges],
               "profile_totals": {o: {r: str(v) for r, v in row.items()} for o, row in totals.items()},
               "profile_minima": {o: {r: str(v) for r, v in row.items()} for o, row in minima.items()}}
        records.append(rec)
        with open(ledger_path, "a") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")

    for rp in resume_cuts:
        for line in Path(rp).read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                t_, m_ = load_rows({"totals": rec["profile_totals"], "minima": rec["profile_minima"]})
                install(rec["allocation"], "resume:" + rec["origin"], t_, m_)
    log(f"resumed cuts: {len(menu)}")
    seeds = []
    for p in seed_profiles:
        raw = json.loads(Path(p).read_text())
        key = "terminal_profile_totals" if "terminal_profile_totals" in raw else "profile_totals"
        seeds.append(load_rows({"totals": raw[key], "minima": raw[key.replace("totals", "minima")]}))
    seeds += seeds_from_ledgers(seed_ledgers)
    obstructions = []
    for i, (totals, minima) in enumerate(seeds):
        # skip seeds already closed by the menu
        if any(_closed(a, totals, minima, edge_cap) for a in menu):
            continue
        st, alloc = decide_whole(totals, minima, edge_cap, oracle_timeout)
        if st == "sat":
            install(alloc, f"seed#{i}", totals, minima)
        else:
            obstructions.append({"origin": f"seed#{i}", "status": st,
                                 "profile_totals": {o: {r: str(v) for r, v in row.items()} for o, row in totals.items()},
                                 "profile_minima": {o: {r: str(v) for r, v in row.items()} for o, row in minima.items()}})
    log(f"seeds installed: menu={len(menu)} obstructions={len(obstructions)} t={time.time()-t0:.0f}s")
    status = "ROUND_LIMIT"
    rounds = []
    if not obstructions:
        for it in range(max_rounds):
            ts = time.time()
            verdict = solver.check()
            row = {"iteration": it, "master_verdict": str(verdict), "master_seconds": round(time.time() - ts, 1), "menu": len(menu)}
            if verdict == z3.unsat:
                status = "UNSAT_MENU_CLOSES_MASTER"; rounds.append(row); log(json.dumps(row)); break
            if verdict == z3.unknown:
                row["reason"] = solver.reason_unknown(); status = "MASTER_UNKNOWN"; rounds.append(row); log(json.dumps(row)); break
            totals, minima = concrete(solver.model(), value, minimum)
            st, alloc = decide_whole(totals, minima, edge_cap, oracle_timeout)
            row["oracle"] = st
            if st == "sat":
                install(alloc, f"round#{it}", totals, minima)
            else:
                obstructions.append({"origin": f"round#{it}", "status": st,
                                     "profile_totals": {o: {r: str(v) for r, v in row2.items()} for o, row2 in totals.items()},
                                     "profile_minima": {o: {r: str(v) for r, v in row2.items()} for o, row2 in minima.items()}})
                status = "SAT_WHOLE_ROLE_OBSTRUCTION" if st == "unsat" else "ORACLE_UNKNOWN"
                rounds.append(row); log(json.dumps(row)); break
            rounds.append(row); log(json.dumps(row))
            _dump(out_path, edge_cap, status, menu, rounds, obstructions, t0)
    else:
        status = "SAT_WHOLE_ROLE_OBSTRUCTION_AT_SEED"
    _dump(out_path, edge_cap, status, menu, rounds, obstructions, t0)
    return status


def _closed(allocation, totals, minima, edge_cap):
    try:
        audit_whole(allocation, totals, minima, edge_cap)
        return True
    except AssertionError:
        return False


def _dump(out_path, edge_cap, status, menu, rounds, obstructions, t0):
    Path(out_path).write_text(json.dumps({
        "schema": "fixed-u-whole-role-edge-cegar-v1", "edge_cap": edge_cap, "status": status,
        "menu_size": len(menu), "menu": menu, "rounds": rounds, "obstructions": obstructions,
        "seconds": round(time.time() - t0, 1),
        "claim_boundary": ("UNSAT proves: every profile of the declared form-2 physical-minimum master has a complete "
                           "whole-role EFX allocation with at most edge_cap support-transfer edges (realization-free). "
                           "It does not prove that every saturated fixed-U state is represented by form 2."),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, indent=2, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edge-cap", type=int, default=5)
    ap.add_argument("--master-timeout-seconds", type=int, default=300)
    ap.add_argument("--oracle-timeout-seconds", type=int, default=60)
    ap.add_argument("--max-rounds", type=int, default=500)
    ap.add_argument("--seed-ledger", type=Path, action="append", default=[])
    ap.add_argument("--seed-profile", type=Path, action="append", default=[])
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--cut-ledger", type=Path, required=True)
    ap.add_argument("--resume-cuts", type=Path, action="append", default=[])
    ap.add_argument("--z3-seed", type=int, default=None)
    a = ap.parse_args()
    Path(a.cut_ledger).write_text("")
    status = run(a.edge_cap, a.master_timeout_seconds, a.oracle_timeout_seconds, a.max_rounds,
                 a.seed_ledger, a.seed_profile, a.output, a.cut_ledger, lambda s: print(s, flush=True),
                 resume_cuts=a.resume_cuts, z3_seed=a.z3_seed)
    print("STATUS", status)


if __name__ == "__main__":
    main()
