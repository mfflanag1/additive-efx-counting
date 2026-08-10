#!/usr/bin/env python3
"""Exact QF_LRA audit of the canonical length-three packet calculations."""

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
    names = ("b", "x", "y", "h", "l", "ltail", "f", "ftail")
    return {
        name: tuple(z3.Real(f"{prefix}_{name}_{agent}") for agent in AGENTS)
        for name in names
    }


def tail(v, label, agent):
    if label in {"x", "y"}:
        return z3.RealVal(0)
    if label == "e":
        return maximum(v["l"][agent], v["h"][agent] + v["ltail"][agent])
    if label == "l":
        return v["ltail"][agent]
    if label == "f":
        return v["ftail"][agent]
    if label == "xh":
        return maximum(v["x"][agent], v["h"][agent])
    raise ValueError(label)


def total(v, label, agent):
    if label in {"x", "y", "h", "l", "f"}:
        return v[label][agent]
    if label == "e":
        return v["h"][agent] + v["l"][agent]
    if label == "xh":
        return v["x"][agent] + v["h"][agent]
    raise ValueError(label)


def efx_failure(v, assignment):
    return z3.Or(
        *(
            total(v, assignment[observer], observer)
            < tail(v, assignment[target], observer)
            for observer in AGENTS
            for target in AGENTS
        )
    )


def base_solver(prefix, source_type, boundary_source, r_x_case):
    v = make_variables(prefix)
    solver = z3.SolverFor("QF_LRA")
    for agent in AGENTS:
        solver.add(v["b"][agent] > 0)
        for name in ("x", "y", "h", "l", "f"):
            solver.add(v[name][agent] > 0)
        solver.add(v["ltail"][agent] >= 0, v["ltail"][agent] <= v["l"][agent])
        solver.add(v["ftail"][agent] >= 0, v["ftail"][agent] <= v["f"][agent])
        solver.add(v["l"][agent] <= v["b"][agent])
        solver.add(v["h"][agent] + v["ltail"][agent] <= v["b"][agent])

    solver.add(v["x"][P] == v["b"][P])
    solver.add(v["y"][S] == v["b"][S])
    solver.add(v["h"][P] + v["l"][P] > v["b"][P])
    solver.add(v["x"][Q] > v["b"][Q])
    solver.add(v["h"][R] <= v["l"][R])
    solver.add(v["h"][R] + v["ltail"][R] <= v["l"][R])
    solver.add(v["f"][R] < v["l"][R])
    solver.add(v["ftail"][Q] <= v["x"][Q])
    solver.add(v["ftail"][S] <= v["b"][S])
    solver.add(v["ftail"][P] <= v["h"][P] + v["l"][P])

    if source_type == "p":
        solver.add(v["y"][P] > v["b"][P])
        solver.add(v["x"][S] <= v["b"][S])
        solver.add(v["ftail"][P] <= v["y"][P])
    elif source_type == "r":
        solver.add(v["y"][R] > v["b"][R])
        solver.add(v["x"][S] <= v["b"][S])
    else:
        raise ValueError(source_type)

    threshold = {P: v["h"][P] + v["l"][P], Q: v["x"][Q], S: v["b"][S]}
    solver.add(v["f"][boundary_source] > threshold[boundary_source])
    if r_x_case == "high":
        solver.add(v["x"][R] >= v["l"][R])
    elif r_x_case == "low":
        solver.add(v["x"][R] < v["l"][R])
    return solver, v


def run():
    cases = (
        ("p_p_source", "p", P, None, ("f", "e", "x", "y")),
        ("p_s_source", "p", S, None, ("y", "e", "x", "f")),
        ("p_q_high", "p", Q, "high", ("e", "x", "f", "y")),
        ("p_q_low", "p", Q, "low", ("xh", "l", "f", "y")),
        ("r_p_source", "r", P, None, ("f", "e", "x", "y")),
        ("r_s_source", "r", S, None, ("e", "y", "x", "f")),
        ("r_q_high", "r", Q, "high", ("e", "x", "f", "y")),
        ("r_q_low", "r", Q, "low", ("xh", "l", "f", "y")),
    )
    records = []
    for name, source_type, boundary_source, r_x_case, assignment in cases:
        solver, values = base_solver(name, source_type, boundary_source, r_x_case)
        solver.add(efx_failure(values, assignment))
        checked = solver.check()
        records.append({"case": name, "status": "FORCED" if checked == z3.unsat else str(checked)})
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "length-three-canonical-packet-audit-v1",
        "status": "ALL_FORCED" if all(record["status"] == "FORCED" for record in records) else "FAILED",
        "records": records,
        "claim_boundary": "exact audit of the aggregate inequalities in the two analytic packet lemmas; BCFF derivation of those inequalities remains analytic",
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
