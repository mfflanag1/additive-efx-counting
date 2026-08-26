#!/usr/bin/env python3
"""Independently re-verify every corpus decision: the closing cover at the minimum split cap and
the relaxed obstruction one cap below (resumable, parallel)."""
from __future__ import annotations
import argparse, json, multiprocessing as mp
from fractions import Fraction
from pathlib import Path
from .independently_verify_fixed_u_f4 import verify_cover, verify_obstruction, OWNERS

def work(args):
    r, prof, timeout = args
    totals = {o: {g: Fraction(v) for g, v in prof["totals"][o].items()} for o in OWNERS}
    minima = {o: {g: Fraction(v) for g, v in prof["minima"][o].items()} for o in OWNERS}
    out = {"id": r["id"], "sha256": r["sha256"], "min_split_cap": r["min_split_cap"], "checks": []}
    ms = r["min_split_cap"]
    if ms is not None:
        temps = [t["template"] for t in r.get("closing_templates_at_min_split", [])]
        st = verify_cover(totals, minima, temps, timeout * 1000)
        out["checks"].append({"kind": "cover", "split_cap": ms, "templates": len(temps), "status": st})
        if ms > 0:
            below = r["by_split_cap"].get(str(ms - 1)) or r["by_split_cap"].get(ms - 1)
            if below and below.get("status") == "RELAXED_OBSTRUCTION":
                st2 = verify_obstruction(totals, minima, below["realization"], ms - 1, 4, timeout * 1000)
                out["checks"].append({"kind": "obstruction", "split_cap": ms - 1, "status": st2})
    out["verdict"] = "pass" if all((c["kind"] == "cover" and c["status"] == "unsat") or (c["kind"] == "obstruction" and c["status"] == "unsat") for c in out["checks"]) and out["checks"] else "FAIL"
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, required=True)
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()
    corpus = {p["sha256"]: p for p in json.loads(args.corpus.read_text())["profiles"]}
    done = set()
    if args.output.exists():
        done = {json.loads(l)["sha256"] for l in open(args.output) if l.strip()}
    rows = [json.loads(l) for l in open(args.results) if l.strip()]
    todo = [(r, corpus[r["sha256"]], args.timeout) for r in rows if r["sha256"] not in done]
    print(f"{len(todo)} to verify", flush=True)
    with mp.Pool(args.workers) as pool, open(args.output, "a") as out:
        for res in pool.imap_unordered(work, todo):
            out.write(json.dumps(res, sort_keys=True) + "\n"); out.flush()
            print(res["id"], res["verdict"], res["checks"], flush=True)

if __name__ == "__main__":
    main()
