#!/usr/bin/env python3
"""Solver-free independent verification of the exact response-relation chart witnesses.

For every pinned relation: re-derive the twelve-atom master's displayed premises at the
witness valuation with exact Fractions (value box, base normalization, base EFX tails,
charity safety, the named packet inequalities, the d-wall, the three retained cores),
recompute the exact nonself response relation from scratch, recompute the rank by
brute-force matching, and check that no rank-four matching exists at the support, split
and reassembly states.  Nothing here imports z3 or the CEGAR modules.
"""
from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

OWNERS = ("r", "q", "d", "s")
TARGETS = (*OWNERS, "charity")
GOODS = ("a0", "a1", "h", "j", "k", "q0", "l", "e", "m", "gq", "gr", "p")
BASE = {"r": ("a0", "m"), "q": ("q0", "a1"), "d": ("h", "k", "gq"), "s": ("e", "p"), "charity": ("j", "l", "gr")}
P = {"A": ("a0", "a1"), "H": ("h",), "Q": ("j", "k", "q0"), "K": ("j", "k"), "J": ("j",), "E": ("l", "e"), "L": ("l",),
     "W": ("m", "gq", "gr"), "P": ("p",)}
SUPPORT = {"r": ("a0", "a1", "h"), "q": ("j", "k", "q0"), "d": ("m", "gq", "gr"), "s": ("l", "e"), "charity": ("p",)}
SPLIT = {"r": ("a0", "a1", "gr"), "q": ("j", "q0", "gq"), "d": ("k", "h", "l"), "s": ("e", "m"), "charity": ("p",)}
REASSEMBLY = {"r": SPLIT["r"], "q": SPLIT["q"], "d": ("k", "h", "m"), "s": ("l", "e"), "charity": ("p",)}


def tot(v, o, goods):
    return sum((v[g, o] for g in goods), Fraction())


def tail(v, o, goods):
    goods = tuple(goods)
    return Fraction() if len(goods) <= 1 else tot(v, o, goods) - min(v[g, o] for g in goods)


def edges(v, state, include_current):
    cur = {o: tot(v, o, state[o]) for o in OWNERS}
    E = set()
    for s in OWNERS:
        for t in TARGETS:
            if t == s:
                continue
            for k in range(1, len(state[t]) + 1):
                for sub in itertools.combinations(state[t], k):
                    if tot(v, s, sub) > 1 and all(tail(v, o, sub) <= 1 for o in OWNERS):
                        E.add((s, t)); break
                    if include_current and tot(v, s, sub) > cur[s] and all(tail(v, o, sub) <= cur[o] for o in OWNERS):
                        E.add((s, t)); break
                if (s, t) in E:
                    break
    return E


def max_matching(E):
    for k in range(4, 0, -1):
        for srcs in itertools.combinations(OWNERS, k):
            for tg in itertools.permutations(TARGETS, k):
                if all((s, t) in E for s, t in zip(srcs, tg)):
                    return k
    return 0


def check_master(v):
    ok = []
    ok.append(("value box", all(0 < v[g, o] < 16 for g in GOODS for o in OWNERS)))
    ok.append(("base normalization", all(tot(v, o, BASE[o]) == 1 for o in OWNERS)))
    ok.append(("base charity safe", all(tot(v, o, BASE["charity"]) <= 1 for o in OWNERS)))
    ok.append(("base EFX tails", all(tail(v, o, BASE[t]) <= 1 for o in OWNERS for t in OWNERS if t != o)))
    ok.append(("A(r),Q(q),E(s),Q(d)>1", tot(v, "r", P["A"]) > 1 and tot(v, "q", P["Q"]) > 1 and tot(v, "s", P["E"]) > 1 and tot(v, "d", P["Q"]) > 1))
    ok.append(("inclusion-minimal K", tot(v, "d", ("j", "k", "h")) > 1 and tot(v, "d", ("j", "h")) <= 1 and tot(v, "d", ("k", "h")) <= 1))
    mu_q = tot(v, "q", P["Q"]) - 1
    ok.append(("q budget", tot(v, "q", P["K"]) - tot(v, "q", P["W"]) > mu_q and tot(v, "q", P["J"]) >= tot(v, "q", P["K"]) - mu_q - tot(v, "q", P["W"])))
    nu_d = tot(v, "d", ("j", "k", "h")) - 1
    ok.append(("nu_d + L - J > 0", nu_d + tot(v, "d", P["L"]) - tot(v, "d", P["J"]) > 0))
    B_q = mu_q + tot(v, "q", P["W"]) - v["k", "q"]
    mu_s = tot(v, "s", P["E"]) - 1
    kappa_s = tot(v, "s", P["L"]) - mu_s
    ok.append(("B_q>=0, kappa_s>0", B_q >= 0 and kappa_s > 0))
    ok.append(("residual selector failure", all((tot(v, "s", sub) < kappa_s) or not (tot(v, "q", sub) <= B_q)
                                                for k in range(0, 4) for sub in itertools.combinations(P["W"], k))))
    su = {o: tot(v, o, SPLIT[o]) for o in OWNERS}; ru = {o: tot(v, o, REASSEMBLY[o]) for o in OWNERS}
    ok.append(("split/reassembly utilities", su["r"] > 1 and su["q"] >= 1 and su["d"] > 1 and su["s"] < 1 and ru["r"] > 1 and ru["q"] >= 1 and ru["s"] > 1 and ru["d"] < 1))
    ok.append(("retained cores r:A q:Q s:E", all(tot(v, s_, P[pk]) > 1 and all(tail(v, o, P[pk]) <= 1 for o in OWNERS) for s_, pk in (("r", "A"), ("q", "Q"), ("s", "E")))))
    d_floor = tot(v, "d", P["W"])
    ok.append(("d wall", d_floor < tail(v, "d", P["A"]) and d_floor >= tail(v, "d", P["Q"]) and d_floor >= tail(v, "d", P["E"]) and d_floor >= tot(v, "d", P["P"])))
    ok.append(("no rank-four at support", max_matching(edges(v, SUPPORT, True)) < 4))
    ok.append(("no rank-four at split", max_matching(edges(v, SPLIT, False)) < 4))
    ok.append(("no rank-four at reassembly", max_matching(edges(v, REASSEMBLY, True)) < 4))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chart", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    chart = json.loads(a.chart.read_text())
    rows, keys = [], set()
    for r in chart["relations"]:
        v = {tuple(k.split(":")): Fraction(val) for k, val in r["witness"].items()}
        E = edges(v, SUPPORT, True)
        rel_ok = sorted(E) == sorted(tuple(e) for e in r["edges"])
        checks = check_master(v)
        rows.append({"key": r["key"], "relation_recomputed_matches": rel_ok, "rank_recomputed": max_matching(E),
                     "rank_matches": max_matching(E) == r["rank"], "master_checks": checks, "all_ok": rel_ok and all(f for _, f in checks)})
        keys.add(r["key"])
    assert len(keys) == len(chart["relations"]), "duplicate relations"
    always = set.intersection(*(set(tuple(e) for e in r["edges"]) for r in chart["relations"]))
    summary = {"relations": len(rows), "all_witnesses_verified": all(x["all_ok"] for x in rows),
               "failures": [x for x in rows if not x["all_ok"]], "edges_in_every_relation": sorted(always),
               "charity_target_relations": sum(1 for r in chart["relations"] if any(e[1] == "charity" for e in r["edges"])),
               "rank_histogram": {str(k): sum(1 for x in rows if x["rank_recomputed"] == k) for k in (1, 2, 3, 4)}}
    print(json.dumps(summary, indent=1))
    if a.output:
        a.output.write_text(json.dumps({"summary": summary, "rows": rows}, indent=1) + "\n")


if __name__ == "__main__":
    main()
