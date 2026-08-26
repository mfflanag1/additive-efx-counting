#!/usr/bin/env python3
"""Global CEGAR: does every valuation of the rank-three fixed-U master (nonself responses, no
form restriction) admit a complete EFX allocation of the twelve atoms within `edge_cap`
support-transfer edges?  Cuts are the (linear) EFX conditions of closing allocations; the
oracle prefers minimal-edge allocations.  UNSAT = twelve-atom theorem on the whole master;
an UNSAT oracle = exact residual valuation with no such allocation."""
from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS
from .decide_fixed_u_chart_cells_complete_efx import decide_complete_efx, efx_cut, zfrac, audit


def load_cuts(paths):
    out = []
    for p in paths:
        for line in Path(p).read_text().splitlines():
            if line.strip():
                out.append(json.loads(line)["allocation"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edge-cap", type=int, default=4)
    ap.add_argument("--timeout-seconds", type=int, default=600)
    ap.add_argument("--max-rounds", type=int, default=100000)
    ap.add_argument("--resume-cuts", type=Path, action="append", default=[])
    ap.add_argument("--seed-chart", type=Path, default=None)
    ap.add_argument("--z3-seed", type=int, default=None)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--cut-ledger", type=Path, required=True)
    a = ap.parse_args()
    solver, value = build_rank_three_master(exclude_self_responses=True)
    solver.set(timeout=a.timeout_seconds * 1000)
    if a.z3_seed is not None:
        solver.set("random_seed", a.z3_seed)
    seen, menu = set(), []
    ledger = a.cut_ledger.open("w")

    def install(alloc, origin):
        k = json.dumps(alloc, sort_keys=True)
        if k in seen:
            return False
        seen.add(k); menu.append(alloc)
        solver.add(z3.Not(efx_cut(alloc, value)))
        ledger.write(json.dumps({"origin": origin, "allocation": alloc}, sort_keys=True) + "\n"); ledger.flush()
        return True

    for alloc in load_cuts(a.resume_cuts):
        install(alloc, "resume")
    if a.seed_chart:
        for r in json.loads(a.seed_chart.read_text())["relations"]:
            vals = {tuple(k.split(":")): Fraction(v) for k, v in r["witness"].items()}
            for cap in range(1, a.edge_cap + 1):
                st, alloc = decide_complete_efx(vals, cap, a.timeout_seconds)
                if st == "sat":
                    audit(alloc, vals); install(alloc, "chart:" + r["key"]); break
    print(f"installed {len(menu)} cuts", flush=True)
    status, rounds, t0 = "ROUND_LIMIT", [], time.time()
    for it in range(a.max_rounds):
        ts = time.time(); v = solver.check(); dt = time.time() - ts
        if v == z3.unsat:
            status = "UNSAT_MENU_CLOSES_MASTER"; print("UNSAT", flush=True); break
        if v == z3.unknown:
            status = "MASTER_UNKNOWN:" + solver.reason_unknown(); print(status, flush=True); break
        m = solver.model()
        vals = {(g, o): zfrac(m.eval(value[g, o], model_completion=True)) for g in GOODS for o in OWNERS}
        st = None
        for cap in range(1, a.edge_cap + 1):
            st, alloc = decide_complete_efx(vals, cap, a.timeout_seconds)
            if st == "sat":
                break
        if st != "sat":
            status = "RESIDUAL_NO_COMPLETE_EFX" if st == "unsat" else "ORACLE_UNKNOWN"
            Path(str(a.output) + ".residual.json").write_text(json.dumps({f"{g}:{o}": str(vals[g, o]) for g in GOODS for o in OWNERS}, indent=1))
            print(status, flush=True); break
        e = audit(alloc, vals); install(alloc, f"round{it}")
        rounds.append({"it": it, "master_seconds": round(dt, 1), "edges": e, "menu": len(menu)})
        if it % 10 == 0:
            print(json.dumps(rounds[-1]), flush=True)
    a.output.write_text(json.dumps({"status": status, "edge_cap": a.edge_cap, "menu_size": len(menu), "rounds": rounds,
                                    "seconds": round(time.time() - t0, 1)}, indent=1) + "\n")
    print("STATUS", status, "menu", len(menu))


if __name__ == "__main__":
    main()
