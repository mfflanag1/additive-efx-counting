#!/usr/bin/env python3
"""Exhaustive chart of exact nonself response relations under the PHYSICAL-MINIMUM rank-three
master (roles with totals/minima, no form restriction).  Same CEGAR as the twelve-atom census;
edge Booleans are built with the physical tail (total minus least minimum)."""
from __future__ import annotations

import argparse
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from . import run_fixed_u_full_packet_terminal_cegar as terminal
from . import run_fixed_u_rank_three_relation_cegar as relation
from .run_exact_response_physical_minimum_cegar import physical_tail
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE
from .run_fixed_u_rank_three_relation_cegar import TARGETS

NONSELF = tuple((s, t) for s in OWNERS for t in TARGETS if t != s)


def zfrac(v):
    return Fraction(v.as_long()) if z3.is_int_value(v) else Fraction(v.as_fraction())


def max_matching(E):
    for k in range(4, 0, -1):
        for srcs in itertools.combinations(OWNERS, k):
            for tg in itertools.permutations(TARGETS, k):
                if all((s, t) in E for s, t in zip(srcs, tg)):
                    return k
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout-seconds", type=int, default=900)
    ap.add_argument("--max-rounds", type=int, default=20000)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    minimum = {(g, o): z3.Real(f"physical_min_{g}_{o}") for g in GOODS for o in OWNERS}
    tail = physical_tail(minimum)
    old_t, old_r = terminal.tail, relation.tail
    try:
        terminal.tail = tail; relation.tail = tail
        solver, value = relation.build_rank_three_master(exclude_self_responses=True)
        edge = relation.response_edges(value, SUPPORT_STATE, include_current=True, exclude_self=True)
    finally:
        terminal.tail, relation.tail = old_t, old_r
    solver.add(*(z3.And(minimum[g, o] > 0, minimum[g, o] <= value[g, o]) for g in GOODS for o in OWNERS))
    solver.add(*(z3.Or(z3.And(*(minimum[g, o] == value[g, o] for o in OWNERS)),
                       z3.And(*(2 * minimum[g, o] <= value[g, o] for o in OWNERS))) for g in GOODS))
    solver.set(timeout=a.timeout_seconds * 1000)
    chart, t0, status = {}, time.time(), "ROUND_LIMIT"
    for it in range(a.max_rounds):
        v = solver.check()
        if v == z3.unsat:
            status = "COMPLETE"; break
        if v == z3.unknown:
            status = "UNKNOWN:" + solver.reason_unknown(); break
        m = solver.model()
        E = {e for e in NONSELF if z3.is_true(m.eval(edge[e], model_completion=True))}
        key = ",".join(f"{s}>{t}" for s, t in NONSELF if (s, t) in E)
        chart[key] = {"key": key, "edges": sorted(E), "edge_count": len(E), "rank": max_matching(E),
                      "witness_totals": {f"{g}:{o}": str(zfrac(m.eval(value[g, o], model_completion=True))) for g in GOODS for o in OWNERS},
                      "witness_minima": {f"{g}:{o}": str(zfrac(m.eval(minimum[g, o], model_completion=True))) for g in GOODS for o in OWNERS}}
        solver.add(z3.Not(z3.And(*(edge[e] if e in E else z3.Not(edge[e]) for e in NONSELF))))
        if it % 50 == 0:
            print(f"it={it} relations={len(chart)} t={time.time()-t0:.0f}s", flush=True)
            a.output.write_text(json.dumps({"status": "RUNNING", "relations": list(chart.values())}, indent=1) + "\n")
    a.output.write_text(json.dumps({"schema": "fixed-u-physical-exact-response-relation-chart-v1", "status": status,
                                    "relation_count": len(chart), "relations": list(chart.values()),
                                    "seconds": round(time.time() - t0, 1)}, indent=1) + "\n")
    print("STATUS", status, "relations", len(chart), flush=True)


if __name__ == "__main__":
    main()
