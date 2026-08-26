#!/usr/bin/env python3
"""Kernel analysis of the pinned four-edge obstruction realization.

(i) every four-edge support topology (charity target x at most three owner
edges) is decided separately; (ii) single-observer and single-envy-pair
deletions locate the load-bearing inequalities; (iii) the five-edge zero-split
topologies that work are enumerated.  Exact rational arithmetic.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import z3

from .audit_fixed_u_four_edge_obstruction import SUPPLIER, load_rows, q, realization
from .run_fixed_u_full_packet_terminal_cegar import OWNERS, SUPPORT_STATE


def decide(values, role_goods, edge_set=None, edge_cap=4, drop_observers=(), drop_pairs=(),
           split_cap=None, timeout_seconds=120):
    goods = [g for gs in role_goods.values() for g in gs]
    x = {(g, o): z3.Bool(f"x_{g}_{o}") for g in goods for o in OWNERS}
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for g in goods:
        solver.add(z3.PbEq([(x[g, o], 1) for o in OWNERS], 1))
    for o in OWNERS:
        solver.add(z3.Or(*(x[g, o] for g in goods)))
    if edge_set is not None:
        for g in goods:
            source = SUPPLIER[g.split(":")[0]]
            for o in OWNERS:
                if o != source and (source, o) not in edge_set:
                    solver.add(z3.Not(x[g, o]))
    elif edge_cap is not None:
        flags = []
        for source in SUPPORT_STATE:
            sg = [g for g in goods if SUPPLIER[g.split(":")[0]] == source]
            for o in OWNERS:
                if o != source:
                    flags.append(z3.Or(*(x[g, o] for g in sg)))
        solver.add(z3.PbLe([(f, 1) for f in flags], edge_cap))
    if split_cap is not None:
        sflags = []
        for role, gs in role_goods.items():
            if len(gs) >= 2:
                sflags.append(z3.Or(*(z3.Not(z3.And(*(x[g, o] == x[gs[0], o] for g in gs[1:])))
                                      for o in OWNERS)))
        solver.add(z3.PbLe([(f, 1) for f in sflags], split_cap))
    for i in OWNERS:
        if i in drop_observers:
            continue
        utility = {o: z3.Sum(*(z3.If(x[g, o], q(values[i, g]), z3.RealVal(0)) for g in goods)) for o in OWNERS}
        for j in OWNERS:
            if j == i or (i, j) in drop_pairs:
                continue
            for g in goods:
                solver.add(z3.Implies(x[g, j], utility[i] >= utility[j] - q(values[i, g])))
    return str(solver.check())


def run(profile_path, primary_path, output_path, timeout_seconds):
    raw = json.loads(profile_path.read_text())
    totals, minima = load_rows(raw, "totals"), load_rows(raw, "minima")
    primary = json.loads(primary_path.read_text())
    bits = {tuple(k.split(":")): v for k, v in primary["minimal_obstruction_pattern"].items()}
    values, role_goods = realization(totals, minima, bits)
    pairs = [(i, j) for i in OWNERS for j in OWNERS if i != j]
    result = {
        "schema": "fixed-u-four-edge-obstruction-kernel-v1",
        "pattern": primary["minimal_obstruction_pattern"],
        "four_edge_cap_status": decide(values, role_goods, timeout_seconds=timeout_seconds),
        "drop_observer": {i: decide(values, role_goods, drop_observers=(i,), timeout_seconds=timeout_seconds) for i in OWNERS},
        "drop_pair": {f"{i}->{j}": decide(values, role_goods, drop_pairs=((i, j),), timeout_seconds=timeout_seconds) for i, j in pairs},
    }
    owner_pairs = pairs
    census = Counter()
    for target in OWNERS:
        for k in range(4):
            for edges in itertools.combinations(owner_pairs, k):
                census[decide(values, role_goods, edge_set={("charity", target), *edges}, timeout_seconds=timeout_seconds)] += 1
    result["four_edge_topology_census"] = {"topologies": sum(census.values()), "status_counts": dict(census)}
    working = []
    for target in OWNERS:
        for edges in itertools.combinations(owner_pairs, 4):
            edge_set = {("charity", target), *edges}
            if decide(values, role_goods, edge_set=edge_set, split_cap=0, timeout_seconds=timeout_seconds) == "sat":
                working.append(sorted(list(e) for e in edge_set))
    result["five_edge_zero_split_topologies"] = working
    assert result["four_edge_cap_status"] == "unsat"
    assert census == Counter({"unsat": 1196})
    assert result["drop_observer"] == {o: "sat" for o in OWNERS}
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--primary-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    result = run(args.profile, args.primary_audit, args.output, args.timeout_seconds)
    print(json.dumps({k: result[k] for k in ("drop_observer", "drop_pair", "four_edge_topology_census")}, indent=2))
    print("five-edge zero-split topologies:", len(result["five_edge_zero_split_topologies"]))


if __name__ == "__main__":
    main()
