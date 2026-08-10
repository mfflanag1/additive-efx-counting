#!/usr/bin/env python3
"""Exact QF_LRA audit of the augmented-root payment reduction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


AGENTS = range(4)
P, R, Q, S = AGENTS


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def maximum(*terms):
    result = terms[0]
    for term in terms[1:]:
        result = z3.If(result >= term, result, term)
    return result


def make_variables(prefix):
    names = (
        "base",
        "root",
        "root_tail",
        "root_minus_h",
        "root_minus_h_tail",
        "root_minus_k",
        "root_minus_k_tail",
        "k",
        "boundary",
        "boundary_tail",
        "z",
        "w",
        "a",
        "b",
    )
    return {
        name: tuple(z3.Real(f"{prefix}_{name}_{agent}") for agent in AGENTS)
        for name in names
    }


def total(v, label, agent):
    if label == "zk":
        return v["z"][agent] + v["k"][agent]
    if label == "ak":
        return v["a"][agent] + v["k"][agent]
    return v[label][agent]


def tail(v, label, agent):
    if label in {"z", "w", "a", "b"}:
        return z3.RealVal(0)
    if label == "zk":
        return maximum(v["z"][agent], v["k"][agent])
    if label == "ak":
        return maximum(v["a"][agent], v["k"][agent])
    return v[f"{label}_tail"][agent]


def efx_failure(v, assignment):
    return z3.Or(
        *(
            total(v, assignment[observer], observer)
            < tail(v, assignment[target], observer)
            for observer in AGENTS
            for target in AGENTS
        )
    )


def base_solver(prefix):
    v = make_variables(prefix)
    solver = z3.SolverFor("QF_LRA")
    total_names = (
        "base",
        "root",
        "root_minus_h",
        "root_minus_k",
        "k",
        "boundary",
        "z",
        "w",
        "a",
        "b",
    )
    tail_names = (
        "root_tail",
        "root_minus_h_tail",
        "root_minus_k_tail",
        "boundary_tail",
    )
    for agent in AGENTS:
        solver.add(*(v[name][agent] > 0 for name in total_names))
        solver.add(*(v[name][agent] >= 0 for name in tail_names))
        solver.add(v["root"][agent] == v["root_minus_k"][agent] + v["k"][agent])
        solver.add(v["root_tail"][agent] <= v["root"][agent])
        solver.add(v["root_minus_h"][agent] <= v["root_tail"][agent])
        solver.add(v["root_minus_k"][agent] <= v["root_tail"][agent])
        solver.add(v["k"][agent] <= v["root_tail"][agent])
        solver.add(v["root_minus_h_tail"][agent] <= v["root_minus_h"][agent])
        solver.add(v["root_minus_k_tail"][agent] <= v["root_minus_k"][agent])
        solver.add(v["boundary_tail"][agent] <= v["boundary"][agent])

    solver.add(v["root"][P] > v["base"][P])
    solver.add(v["root_tail"][P] > v["base"][P])
    for agent in (R, Q, S):
        solver.add(v["root_tail"][agent] <= v["base"][agent])

    # Both charity singletons are p-bounded in the live external-q-only branch.
    for singleton in ("z", "w", "a", "b"):
        solver.add(v[singleton][P] <= v["base"][P])

    solver.add(v["z"][Q] > v["base"][Q])
    solver.add(v["w"][S] >= v["base"][S])
    solver.add(v["z"][S] <= v["w"][S])
    solver.add(v["boundary_tail"][P] <= v["root_tail"][P])
    solver.add(v["boundary_tail"][Q] <= v["z"][Q])
    solver.add(v["boundary_tail"][S] <= v["w"][S])
    solver.add(v["boundary"][R] < v["root_tail"][R])
    return solver, v


def checked_case(name, configure, assignment):
    solver, values = base_solver(name)
    configure(solver, values)
    solver.add(efx_failure(values, assignment))
    checked = solver.check()
    return {"case": name, "status": "FORCED" if checked == z3.unsat else str(checked)}


def run():
    def p_source(solver, v):
        solver.add(v["boundary"][P] > v["root_tail"][P])
        solver.add(v["root_minus_h"][R] == v["root_tail"][R])

    def q_high(solver, v):
        solver.add(v["boundary"][Q] > v["z"][Q])
        solver.add(v["z"][R] >= v["root_tail"][R])

    def q_low(solver, v):
        solver.add(v["boundary"][Q] > v["z"][Q])
        solver.add(v["z"][R] < v["root_tail"][R])
        solver.add(v["root_minus_k"][P] == v["root_tail"][P])
        solver.add(v["z"][R] + v["k"][R] >= v["root_minus_k_tail"][R])
        solver.add(v["z"][R] + v["k"][R] >= v["boundary_tail"][R])

    def s_common(solver, v):
        solver.add(v["boundary"][S] > v["w"][S])
        solver.add(v["w"][S] >= v["a"][S], v["w"][S] >= v["b"][S])
        solver.add(v["b"][Q] >= v["a"][Q], v["b"][Q] >= v["z"][Q])

    def s_high(solver, v):
        s_common(solver, v)
        solver.add(v["a"][R] >= v["root_tail"][R])

    def s_low(solver, v):
        s_common(solver, v)
        solver.add(v["a"][R] < v["root_tail"][R])
        solver.add(v["root_minus_k"][P] == v["root_tail"][P])
        solver.add(v["a"][R] + v["k"][R] >= v["root_minus_k_tail"][R])
        solver.add(v["a"][R] + v["k"][R] >= v["boundary_tail"][R])

    records = [
        checked_case("p_source", p_source, ("boundary", "root_minus_h", "z", "w")),
        checked_case("q_source_high", q_high, ("root", "z", "boundary", "w")),
        checked_case("q_source_low_compensated", q_low, ("root_minus_k", "zk", "boundary", "w")),
        checked_case("s_source_high", s_high, ("root", "a", "b", "boundary")),
        checked_case("s_source_low_compensated", s_low, ("root_minus_k", "ak", "b", "boundary")),
    ]
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "length-three-augmented-root-payment-audit-v1",
        "status": "ALL_FORCED" if all(record["status"] == "FORCED" for record in records) else "FAILED",
        "records": records,
        "claim_boundary": "exact QF_LRA audit of the five aggregate candidate-allocation implications in the analytic augmented-root payment reduction",
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "cases": len(result["records"])}, indent=2))


if __name__ == "__main__":
    main()
