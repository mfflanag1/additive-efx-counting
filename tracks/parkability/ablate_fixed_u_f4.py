#!/usr/bin/env python3
"""Hypothesis ablations for (F4): drop the edge cap, drop positivity (zero-value goods), drop admissibility (random physical profiles)."""
from __future__ import annotations
import argparse, json, random, time
from fractions import Fraction
from pathlib import Path
from . import decide_fixed_u_f4 as D

def zerofloor_patch(enable):
    """Zero-value goods: every deletion floor of a whole role or complement drops to 0."""
    if not enable:
        return
    orig = D.Realization.piece_values
    def pv(self, role, anchor, observer):
        x, xf, comp, cf = orig(self, role, anchor, observer)
        return x, xf, comp, Fraction(0)
    D.Realization.piece_values = pv
    # whole-role floors are minima[o][g] in oracle/evaluate: patch minima to 0 via wrapper in main

def random_profile(rng, singleton_prob=0.25):
    totals = {o: {} for o in D.OWNERS}; minima = {o: {} for o in D.OWNERS}
    for g in D.GOODS:
        single = rng.random() < singleton_prob
        for o in D.OWNERS:
            T = Fraction(rng.randint(1, 400), 400)
            if single:
                M = T
            else:
                k = rng.choice((2, 2, 3, 4))
                M = T / k * Fraction(rng.randint(50, 100), 100)
            totals[o][g] = T; minima[o][g] = M
    return totals, minima

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("edgefree", "zerofloor", "random"), required=True)
    ap.add_argument("--profile", type=Path)
    ap.add_argument("--samples", type=int, default=20)
    ap.add_argument("--seed", type=int, default=826)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    out = {"mode": args.mode, "results": []}
    if args.mode == "edgefree":
        totals, minima = D.load_profile(args.profile)
        for c in range(0, 5):
            r = D.decide(totals, minima, c, 16, oracle_timeout=120, adversary_timeout=300)
            out["results"].append({"split_cap": c, "edge_cap": 16, "status": r["status"], "rounds": r["rounds"], "seconds": r["seconds"]})
            print(out["results"][-1], flush=True)
            if r["status"] == "F4_HOLDS":
                break
    elif args.mode == "zerofloor":
        totals, minima = D.load_profile(args.profile)
        D.ZERO_FLOORS = True
        for c in range(0, 5):
            r = D.decide(totals, minima, c, 4, oracle_timeout=120, adversary_timeout=300)
            out["results"].append({"split_cap": c, "edge_cap": 4, "status": r["status"], "rounds": r["rounds"], "seconds": r["seconds"], "realization": r.get("realization")})
            print({k: v for k, v in out["results"][-1].items() if k != "realization"}, flush=True)
            if r["status"] == "F4_HOLDS":
                break
    else:
        rng = random.Random(args.seed)
        for i in range(args.samples):
            totals, minima = random_profile(rng)
            r = D.decide(totals, minima, 4, 4, oracle_timeout=60, adversary_timeout=200)
            rec = {"sample": i, "status": r["status"], "rounds": r["rounds"], "seconds": r["seconds"],
                   "totals": {o: {g: str(v) for g, v in totals[o].items()} for o in D.OWNERS},
                   "minima": {o: {g: str(v) for g, v in minima[o].items()} for o in D.OWNERS}}
            if "realization" in r: rec["realization"] = r["realization"]
            out["results"].append(rec); print({k: rec[k] for k in ("sample", "status", "rounds", "seconds")}, flush=True)
    args.output.write_text(json.dumps(out, indent=1) + "\n")

if __name__ == "__main__":
    main()
