#!/usr/bin/env python3
"""Cap-free lift: whole-role EFX closure of the physical-minimum rank-three master with NO
response-form restriction.  Every twelve-atom 'good' becomes a role with total T and per-observer
minimum M (singleton iff T=M for all observers, else T>=2M), as in
run_exact_response_physical_minimum_cegar.build_physical_master, but with only
exclude_self_responses=True (all 316 exact relations admitted).  Whole-role EFX conditions are
linear in (T,M), so closing allocations are exact cuts.  UNSAT = every physical state of the master
(any response form, any packet sizes) has a whole-role EFX allocation within edge_cap edges."""
from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from . import run_fixed_u_full_packet_terminal_cegar as terminal
from . import run_fixed_u_rank_three_relation_cegar as relation
from .run_exact_response_physical_minimum_cegar import physical_tail
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE

SUPPLIER = {g: s for s, goods in SUPPORT_STATE.items() for g in goods}


def build_physical_master_free():
    minimum = {(g, o): z3.Real(f"physical_min_{g}_{o}") for g in GOODS for o in OWNERS}
    tail = physical_tail(minimum)
    old_t, old_r = terminal.tail, relation.tail
    try:
        terminal.tail = tail; relation.tail = tail
        solver, value = relation.build_rank_three_master(exclude_self_responses=True)
    finally:
        terminal.tail, relation.tail = old_t, old_r
    solver.add(*(z3.And(minimum[g, o] > 0, minimum[g, o] <= value[g, o]) for g in GOODS for o in OWNERS))
    solver.add(*(z3.Or(z3.And(*(minimum[g, o] == value[g, o] for o in OWNERS)),
                       z3.And(*(2 * minimum[g, o] <= value[g, o] for o in OWNERS))) for g in GOODS))
    return solver, value, minimum


def q(v):
    v = Fraction(v); return z3.RealVal(f"{v.numerator}/{v.denominator}")


def zfrac(v):
    return Fraction(v.as_long()) if z3.is_int_value(v) else Fraction(v.as_fraction())


def decide_whole(T, M, edge_cap, timeout):
    owner = {g: z3.Int(f"w_{g}") for g in GOODS}
    s = z3.Solver(); s.set(timeout=timeout * 1000)
    s.add(*(z3.And(owner[g] >= 0, owner[g] < 4) for g in GOODS))
    flags = []
    for src in SUPPORT_STATE:
        for i, t in enumerate(OWNERS):
            if src != t:
                flags.append(z3.Or(*(owner[g] == i for g in SUPPORT_STATE[src])))
    s.add(z3.PbLe([(f, 1) for f in flags], edge_cap))
    for oi, o in enumerate(OWNERS):
        util = {i: z3.Sum(*(z3.If(owner[g] == i, q(T[g, o]), z3.RealVal(0)) for g in GOODS)) for i in range(4)}
        for ti in range(4):
            if ti == oi:
                continue
            for g in GOODS:
                s.add(z3.Implies(owner[g] == ti, util[oi] >= util[ti] - q(M[g, o])))
    st = s.check()
    if st != z3.sat:
        return str(st), None
    m = s.model()
    return "sat", {t: [g for g in GOODS if m.eval(owner[g]).as_long() == i] for i, t in enumerate(OWNERS)}


def audit(alloc, T, M, edge_cap):
    assert sorted(g for b in alloc.values() for g in b) == sorted(GOODS)
    assert len({(SUPPLIER[g], t) for t, b in alloc.items() for g in b if SUPPLIER[g] != t}) <= edge_cap
    for o in OWNERS:
        own = sum((T[g, o] for g in alloc[o]), Fraction())
        for t in OWNERS:
            if t == o:
                continue
            tot = sum((T[g, o] for g in alloc[t]), Fraction())
            for g in alloc[t]:
                assert own >= tot - M[g, o]


def cut(alloc, value, minimum):
    conds = []
    for o in OWNERS:
        own = z3.Sum(*(value[g, o] for g in alloc[o])) if alloc[o] else z3.RealVal(0)
        for t in OWNERS:
            if t == o or not alloc[t]:
                continue
            tot = z3.Sum(*(value[g, o] for g in alloc[t]))
            for g in alloc[t]:
                conds.append(own >= tot - minimum[g, o])
    return z3.And(*conds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edge-cap", type=int, default=5)
    ap.add_argument("--timeout-seconds", type=int, default=900)
    ap.add_argument("--max-rounds", type=int, default=100000)
    ap.add_argument("--resume-cuts", type=Path, action="append", default=[])
    ap.add_argument("--z3-seed", type=int, default=None)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--cut-ledger", type=Path, required=True)
    a = ap.parse_args()
    solver, value, minimum = build_physical_master_free()
    solver.set(timeout=a.timeout_seconds * 1000)
    if a.z3_seed is not None:
        solver.set("random_seed", a.z3_seed)
    seen, menu = set(), []
    ledger = a.cut_ledger.open("w")

    def install(alloc, origin):
        k = json.dumps(alloc, sort_keys=True)
        if k in seen:
            return
        seen.add(k); menu.append(alloc); solver.add(z3.Not(cut(alloc, value, minimum)))
        ledger.write(json.dumps({"origin": origin, "allocation": alloc}, sort_keys=True) + "\n"); ledger.flush()

    for p in a.resume_cuts:
        for line in Path(p).read_text().splitlines():
            if line.strip():
                install(json.loads(line)["allocation"], "resume")
    print(f"installed {len(menu)}", flush=True)
    status, t0, rounds = "ROUND_LIMIT", time.time(), []
    for it in range(a.max_rounds):
        ts = time.time(); v = solver.check(); dt = time.time() - ts
        if v == z3.unsat:
            status = "UNSAT_MENU_CLOSES_PHYSICAL_MASTER"; break
        if v == z3.unknown:
            status = "MASTER_UNKNOWN:" + solver.reason_unknown(); break
        m = solver.model()
        T = {(g, o): zfrac(m.eval(value[g, o], model_completion=True)) for g in GOODS for o in OWNERS}
        M = {(g, o): zfrac(m.eval(minimum[g, o], model_completion=True)) for g in GOODS for o in OWNERS}
        st, alloc = decide_whole(T, M, a.edge_cap, a.timeout_seconds)
        if st != "sat":
            status = "PHYSICAL_WHOLE_ROLE_OBSTRUCTION" if st == "unsat" else "ORACLE_UNKNOWN"
            Path(str(a.output) + ".obstruction.json").write_text(json.dumps(
                {"totals": {f"{g}:{o}": str(T[g, o]) for g in GOODS for o in OWNERS},
                 "minima": {f"{g}:{o}": str(M[g, o]) for g in GOODS for o in OWNERS}}, indent=1))
            break
        audit(alloc, T, M, a.edge_cap); install(alloc, f"round{it}")
        rounds.append({"it": it, "master_seconds": round(dt, 1), "menu": len(menu)})
        if it % 10 == 0:
            print(json.dumps(rounds[-1]), flush=True)
    a.output.write_text(json.dumps({"status": status, "edge_cap": a.edge_cap, "menu_size": len(menu), "rounds": rounds,
                                    "seconds": round(time.time() - t0, 1)}, indent=1) + "\n")
    print("STATUS", status, "menu", len(menu), flush=True)


if __name__ == "__main__":
    main()
