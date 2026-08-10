#!/usr/bin/env python3
"""Exact QF_LRA audit of the two length-three reservoir orientations."""

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


def variables(prefix):
    names = ("base", "d", "dtail", "payment", "payment_tail", "a", "atail", "x", "y")
    return {name: tuple(z3.Real(f"{prefix}_{name}_{i}") for i in AGENTS) for name in names}


def tail(v, label, agent):
    if label in {"x", "y"}:
        return z3.RealVal(0)
    return v[{"d": "dtail", "payment": "payment_tail", "a": "atail"}[label]][agent]


def efx_failure(v, assignment):
    return z3.Or(*(
        v[assignment[i]][i] < tail(v, assignment[j], i)
        for i in AGENTS for j in AGENTS
    ))


def conclusion_failure(v, assignment, orientation):
    failures = [efx_failure(v, assignment)]
    if orientation == "q_before_r":
        failures.extend((
            v[assignment[P]][P] < v["base"][P],
            v[assignment[S]][S] < v["base"][S],
            v[assignment[Q]][Q] <= v["base"][Q],
        ))
    else:
        failures.extend((
            v[assignment[P]][P] < v["base"][P],
            v[assignment[S]][S] < v["base"][S],
            v[assignment[R]][R] <= v["base"][R],
        ))
    return z3.Or(*failures)


def base_solver(prefix, orientation, external):
    v = variables(prefix)
    solver = z3.SolverFor("QF_LRA")
    for i in AGENTS:
        solver.add(v["base"][i] > 0)
        for name in ("d", "payment", "a", "x", "y"):
            solver.add(v[name][i] > 0)
        for total_name, tail_name in (("d", "dtail"), ("payment", "payment_tail"), ("a", "atail")):
            solver.add(v[tail_name][i] >= 0, v[tail_name][i] < v[total_name][i])
            solver.add(v[tail_name][i] <= v["base"][i])
    solver.add(v["x"][P] == v["base"][P])
    solver.add(v["y"][S] == v["base"][S])
    solver.add(v["x"][Q] > v["base"][Q])
    solver.add(v["y"][external] > v["base"][external])
    if orientation == "q_before_r":
        solver.add(v["d"][P] > v["base"][P])
    else:
        solver.add(v["d"][R] > v["base"][R])
    return solver, v


def checked_case(name, orientation, external, configure, assignment):
    solver, v = base_solver(name, orientation, external)
    configure(solver, v)
    solver.add(conclusion_failure(v, assignment, orientation))
    checked = solver.check()
    return {"case": name, "status": "FORCED" if checked == z3.unsat else str(checked)}


def run():
    records = []
    for external, external_name in ((P, "p"), (R, "r"), (Q, "q")):
        def q_high(solver, v):
            solver.add(v["payment"][R] >= v["dtail"][R])

        records.append(checked_case(
            f"q_before_r_high_a_{external_name}", "q_before_r", external,
            q_high, ("d", "payment", "x", "y")
        ))

        low_assignments = {
            P: ("a", "d", "x", "y"),
            R: ("d", "a", "x", "y"),
            Q: ("x", "d", "a", "y"),
        }
        for source, source_name in ((P, "p"), (R, "r"), (Q, "q")):
            def q_low(solver, v, source=source):
                solver.add(v["a"][R] < v["dtail"][R])
                solver.add(v["a"][source] > v["base"][source])

            records.append(checked_case(
                f"q_before_r_low_{source_name}_a_{external_name}", "q_before_r", external,
                q_low, low_assignments[source]
            ))

        s_assignment = {
            P: ("y", "d", "x", "a"),
            R: ("d", "y", "x", "a"),
            Q: ("x", "d", "y", "a"),
        }[external]

        def q_low_s(solver, v):
            solver.add(v["a"][R] < v["dtail"][R])
            solver.add(v["a"][S] > v["base"][S])

        records.append(checked_case(
            f"q_before_r_low_s_a_{external_name}", "q_before_r", external,
            q_low_s, s_assignment
        ))

        def r_high(solver, v):
            solver.add(v["payment"][Q] >= v["dtail"][Q])

        records.append(checked_case(
            f"r_before_q_high_a_{external_name}", "r_before_q", external,
            r_high, ("x", "d", "payment", "y")
        ))

        def r_low_r(solver, v):
            solver.add(v["a"][Q] < v["dtail"][Q])
            solver.add(v["a"][R] > v["base"][R])

        records.append(checked_case(
            f"r_before_q_low_r_a_{external_name}", "r_before_q", external,
            r_low_r, ("x", "a", "d", "y")
        ))

        r_s_assignment = {
            P: ("y", "d", "x", "a"),
            R: ("x", "y", "d", "a"),
            Q: ("x", "d", "y", "a"),
        }[external]

        def r_low_s(solver, v):
            solver.add(v["a"][Q] < v["dtail"][Q])
            solver.add(v["a"][S] > v["base"][S])

        records.append(checked_case(
            f"r_before_q_low_s_a_{external_name}", "r_before_q", external,
            r_low_s, r_s_assignment
        ))

    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "length-three-reservoir-order-packet-audit-v1",
        "status": "ALL_FORCED" if all(record["status"] == "FORCED" for record in records) else "FAILED",
        "records": records,
        "claim_boundary": "exact QF_LRA audit of EFX and the required fixed/improving utility signs for every aggregate candidate in both reservoir orientations",
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
