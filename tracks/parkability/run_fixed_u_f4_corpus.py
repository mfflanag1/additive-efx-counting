#!/usr/bin/env python3
"""Decide (F4) and the split/edge minima for every profile of a corpus (resumable, parallel)."""
from __future__ import annotations
import argparse, json, multiprocessing as mp, sys, time
from fractions import Fraction
from pathlib import Path
from .decide_fixed_u_f4 import minima_table, OWNERS

def work(args):
    prof, edge_cap, split_cap, oto, ato, edge_loop = args
    totals = {o: {g: Fraction(v) for g, v in prof["totals"][o].items()} for o in OWNERS}
    minima = {o: {g: Fraction(v) for g, v in prof["minima"][o].items()} for o in OWNERS}
    t0 = time.time()
    try:
        r = minima_table(totals, minima, edge_cap, split_cap, oracle_timeout=oto, adversary_timeout=ato, edge_loop=edge_loop)
        r["error"] = None
    except Exception as e:  # keep the sweep alive; record
        r = {"error": repr(e), "min_split_cap": None, "min_edge_cap": None}
    r["id"] = prof["id"]; r["sha256"] = prof["sha256"]; r["tag"] = prof["tag"]; r["seconds"] = round(time.time() - t0, 1)
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--edge-cap", type=int, default=4)
    ap.add_argument("--split-cap", type=int, default=4)
    ap.add_argument("--oracle-timeout", type=int, default=60)
    ap.add_argument("--adversary-timeout", type=int, default=300)
    ap.add_argument("--tags", nargs="*")
    ap.add_argument("--no-edge-loop", action="store_true")
    args = ap.parse_args()
    corpus = json.loads(args.corpus.read_text())["profiles"]
    done = set()
    if args.output.exists():
        for line in open(args.output):
            done.add(json.loads(line)["sha256"])
    todo = [p for p in corpus if p["sha256"] not in done and (not args.tags or p["tag"] in args.tags)]
    print(f"{len(todo)} profiles to decide ({len(done)} already done)", flush=True)
    with mp.Pool(args.workers) as pool, open(args.output, "a") as out:
        for r in pool.imap_unordered(work, [(p, args.edge_cap, args.split_cap, args.oracle_timeout, args.adversary_timeout, not args.no_edge_loop) for p in todo]):
            out.write(json.dumps(r, sort_keys=True) + "\n"); out.flush()
            print(f"{r['id']} {r['tag']} min_split={r['min_split_cap']} min_edge={r['min_edge_cap']} s={r['seconds']} err={r['error']}", flush=True)

if __name__ == "__main__":
    main()
