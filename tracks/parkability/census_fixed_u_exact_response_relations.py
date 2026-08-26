#!/usr/bin/env python3
"""Exhaustive chart of exact nonself response relations under the rank-three fixed-U master.

CEGAR: master (rank-three saturated separator premises, self responses excluded)
  -> model -> read the exact relation E (which of the 16 nonself source->target
  response edges hold at the model's valuation) -> record E with a rational witness
  -> block "relation == E" -> repeat.  UNSAT terminates with the complete chart.
Graph feasibility (rank, forms) is recomputed in plain Python from the witness by an
independent implementation; valuation feasibility is the SMT model.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .run_fixed_u_rank_three_relation_cegar import (
    build_rank_three_master, response_edges, TARGETS,
)
from .run_fixed_u_full_packet_terminal_cegar import (
    GOODS, OWNERS, SUPPORT_STATE, BASE, PACKETS,
)

NONSELF = tuple((s, t) for s in OWNERS for t in TARGETS if t != s)
CORRECTED_FORMS = (
    (("r", "q"), ("q", "r"), ("s", "d"), ("d", "q"), ("d", "r")),
    (("r", "q"), ("q", "d"), ("s", "r"), ("d", "q"), ("d", "r")),
    (("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r")),
    (("r", "q"), ("q", "s"), ("s", "d"), ("d", "q"), ("d", "r")),
)


def zfrac(v):
    if z3.is_int_value(v):
        return Fraction(v.as_long())
    return Fraction(v.as_fraction())


# ---- independent graph-side recomputation (plain Python, Fractions) ----
def tot(vals, o, goods):
    return sum((vals[g, o] for g in goods), Fraction())


def tail(vals, o, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction()
    return tot(vals, o, goods) - min(vals[g, o] for g in goods)


def independent_edges(vals, state=SUPPORT_STATE):
    """source->target edge iff some nonempty subset of target's bundle is a base-common-safe
    response (total>1 for the source, tails<=1 for all observers) or a current-safe response
    (total > source's current utility, tails <= each observer's current utility)."""
    current = {o: tot(vals, o, state[o]) for o in OWNERS}
    edges = set()
    for s in OWNERS:
        for t in TARGETS:
            if t == s:
                continue
            bundle = tuple(state[t])
            hit = False
            for k in range(1, len(bundle) + 1):
                for sub in itertools.combinations(bundle, k):
                    if tot(vals, s, sub) > 1 and all(tail(vals, o, sub) <= 1 for o in OWNERS):
                        hit = True
                    if tot(vals, s, sub) > current[s] and all(tail(vals, o, sub) <= current[o] for o in OWNERS):
                        hit = True
                    if hit:
                        break
                if hit:
                    break
            if hit:
                edges.add((s, t))
    return edges


def rank(edges):
    best = 0
    for targets in itertools.permutations(TARGETS, len(OWNERS)):
        m = sum(1 for s, t in zip(OWNERS, targets) if (s, t) in edges)
        best = max(best, m)
    # rank = size of maximum matching (sources to distinct targets)
    return max_matching(edges)


def max_matching(edges):
    best = 0
    for k in range(len(OWNERS), 0, -1):
        for srcs in itertools.combinations(OWNERS, k):
            for targets in itertools.permutations(TARGETS, k):
                if all((s, t) in edges for s, t in zip(srcs, targets)):
                    return k
    return 0


def relation_key(edges):
    return ",".join(f"{s}>{t}" for s, t in NONSELF if (s, t) in edges)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout-seconds", type=int, default=600)
    ap.add_argument("--max-rounds", type=int, default=5000)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--resume", type=Path, default=None)
    a = ap.parse_args()
    solver, value = build_rank_three_master(exclude_self_responses=True)
    solver.set(timeout=a.timeout_seconds * 1000)
    edge = response_edges(value, SUPPORT_STATE, include_current=True, exclude_self=True)
    chart = {}
    if a.resume and a.resume.exists():
        prev = json.loads(a.resume.read_text())
        for row in prev["relations"]:
            chart[row["key"]] = row
    for row in chart.values():
        E = {tuple(e) for e in row["edges"]}
        solver.add(z3.Not(z3.And(*(edge[e] if e in E else z3.Not(edge[e]) for e in NONSELF))))
    t0 = time.time()
    status = "ROUND_LIMIT"
    for it in range(a.max_rounds):
        ts = time.time()
        verdict = solver.check()
        if verdict == z3.unsat:
            status = "COMPLETE"; print(f"UNSAT after {len(chart)} relations", flush=True); break
        if verdict == z3.unknown:
            status = "UNKNOWN:" + solver.reason_unknown(); print(status, flush=True); break
        model = solver.model()
        vals = {(g, o): zfrac(model.eval(value[g, o], model_completion=True)) for g in GOODS for o in OWNERS}
        E_model = {e for e in NONSELF if z3.is_true(model.eval(edge[e], model_completion=True))}
        E_indep = independent_edges(vals)
        agree = (E_model == E_indep)
        key = relation_key(E_model)
        forms = [i for i, f in enumerate(CORRECTED_FORMS) if set(f) == E_model]
        row = {"key": key, "edges": sorted(E_model), "edge_count": len(E_model), "rank": max_matching(E_model),
               "independent_edges_agree": agree, "independent_edges": sorted(E_indep),
               "corrected_form_index": forms[0] if forms else None,
               "witness": {f"{g}:{o}": str(vals[g, o]) for g in GOODS for o in OWNERS},
               "seconds": round(time.time() - ts, 1)}
        chart[key] = row
        print(f"it={it} relation#{len(chart)} edges={len(E_model)} rank={row['rank']} form={row['corrected_form_index']} agree={agree} t={time.time()-t0:.0f}s", flush=True)
        solver.add(z3.Not(z3.And(*(edge[e] if e in E_model else z3.Not(edge[e]) for e in NONSELF))))
        a.output.write_text(json.dumps({"status": "RUNNING", "relations": list(chart.values())}, indent=1) + "\n")
    out = {"schema": "fixed-u-exact-response-relation-chart-v1", "status": status,
           "master": "build_rank_three_master(exclude_self_responses=True) = saturated root-facing rank-three separator premises, nonself responses",
           "relation_count": len(chart), "relations": list(chart.values()),
           "corrected_forms": [list(map(list, f)) for f in CORRECTED_FORMS],
           "seconds": round(time.time() - t0, 1),
           "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    a.output.write_text(json.dumps(out, indent=1) + "\n")
    print("STATUS", status, "relations", len(chart))


if __name__ == "__main__":
    main()
