#!/usr/bin/env python3
"""Ablation: sample profiles from the physical-minimum master WITHOUT the exact owner-cycle
response relation (form-2 exact-response normalization dropped) and decide (F4)."""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
import z3
from . import run_fixed_u_full_packet_terminal_cegar as terminal
from . import run_fixed_u_rank_three_relation_cegar as relation
from .run_exact_response_physical_minimum_cegar import physical_tail
from .decide_fixed_u_f4 import decide, OWNERS, GOODS
from .run_fixed_u_tame_or_anchor_cegar import concrete_profile

def build_master(exact_relation, form_index):
    minimum = {(g, o): z3.Real(f"physical_min_{g}_{o}") for g in terminal.GOODS for o in terminal.OWNERS}
    tail = physical_tail(minimum)
    ot, orl = terminal.tail, relation.tail
    try:
        terminal.tail = tail; relation.tail = tail
        solver, value = relation.build_rank_three_master(
            exclude_self_responses=True, required_owner_cycle_form=False,
            exact_owner_cycle_response_relation=False, owner_cycle_form_index=None)
    finally:
        terminal.tail = ot; relation.tail = orl
    solver.add(*(z3.And(minimum[g, o] > 0, minimum[g, o] <= value[g, o]) for g in terminal.GOODS for o in terminal.OWNERS))
    solver.add(*(z3.Or(z3.And(*(minimum[g, o] == value[g, o] for o in terminal.OWNERS)),
                       z3.And(*(2 * minimum[g, o] <= value[g, o] for o in terminal.OWNERS))) for g in terminal.GOODS))
    return solver, value, minimum

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=8)
    ap.add_argument("--seed", type=int, default=826)
    ap.add_argument("--master-timeout", type=int, default=300)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    source, total, minimum = build_master(False, 2)
    solver = z3.Solver(); solver.add(*source.assertions()); solver.set(timeout=args.master_timeout * 1000, random_seed=args.seed)
    out = {"mode": "plain_rank_three_master_no_form2_exact_response", "results": []}
    for i in range(args.samples):
        st = solver.check()
        if st != z3.sat:
            out["master_status"] = str(st); break
        totals, minima = concrete_profile(solver.model(), total, minimum)
        r = decide(totals, minima, 4, 4, oracle_timeout=60, adversary_timeout=200)
        rec = {"sample": i, "status": r["status"], "rounds": r["rounds"], "seconds": r["seconds"],
               "totals": {o: {g: str(v) for g, v in totals[o].items()} for o in OWNERS},
               "minima": {o: {g: str(v) for g, v in minima[o].items()} for o in OWNERS}}
        if "realization" in r: rec["realization"] = r["realization"]
        out["results"].append(rec); print({k: rec[k] for k in ("sample", "status", "rounds", "seconds")}, flush=True)
        # exclude a small box around the sampled point to move on
        from fractions import Fraction
        eps = Fraction(1, 10**4)
        solver.add(z3.Or(*[z3.Or(total[g, o] < z3.RealVal(f"{(totals[o][g]-eps).numerator}/{(totals[o][g]-eps).denominator}"),
                                 total[g, o] > z3.RealVal(f"{(totals[o][g]+eps).numerator}/{(totals[o][g]+eps).denominator}")) for g in GOODS for o in OWNERS]))
        args.output.write_text(json.dumps(out, indent=1) + "\n")
    args.output.write_text(json.dumps(out, indent=1) + "\n")

if __name__ == "__main__":
    main()
