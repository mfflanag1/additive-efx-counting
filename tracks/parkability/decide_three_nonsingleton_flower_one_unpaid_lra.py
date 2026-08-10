#!/usr/bin/env python3
"""QF_LRA audit of every selected one-unpaid flower cover."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS, run as run_cover
except ImportError:
    from decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS, run as run_cover


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_record(index: int, record: dict) -> dict:
    order = tuple(record["priority_order"])
    assignment = record["assignment"]
    signs = record["signs"]
    bundle_names = tuple(dict.fromkeys(assignment.values()))
    base = {agent: z3.Real(f"c{index}_base_{agent}") for agent in AGENTS}
    total = {
        (name, agent): z3.Real(f"c{index}_{name}_{agent}")
        for name in bundle_names
        for agent in AGENTS
    }
    tail = {
        (name, agent): z3.Real(f"c{index}_{name}_tail_{agent}")
        for name in bundle_names
        for agent in AGENTS
    }
    solver = z3.SolverFor("QF_LRA")
    for agent in AGENTS:
        solver.add(base[agent] > 0)
        for name in bundle_names:
            solver.add(total[name, agent] > 0)
            solver.add(tail[name, agent] >= 0, tail[name, agent] <= base[agent])
        assigned = assignment[agent]
        if signs[agent] == "fixed":
            solver.add(total[assigned, agent] == base[agent])
        elif signs[agent] == "improves":
            solver.add(total[assigned, agent] > base[agent])

    unpaid = record["unpaid_agent"]
    if unpaid is not None:
        assigned = assignment[unpaid]
        for name in bundle_names:
            solver.add(total[assigned, unpaid] >= tail[name, unpaid])

    efx_failure = z3.Or(*(
        total[assignment[observer], observer] < tail[assignment[target], observer]
        for observer in AGENTS
        for target in AGENTS
    ))
    lex_terms = []
    for position, agent in enumerate(order):
        lex_terms.append(z3.And(
            *(total[assignment[earlier], earlier] == base[earlier] for earlier in order[:position]),
            total[assignment[agent], agent] > base[agent],
        ))
    lex_improves = z3.Or(*lex_terms)
    solver.add(z3.Or(efx_failure, z3.Not(lex_improves)))
    checked = solver.check()
    return {
        "index": index,
        "status": "FORCED" if checked == z3.unsat else str(checked),
        "cover_status": record["status"],
        "unpaid_agent": unpaid,
    }


def run() -> dict:
    cover = run_cover()
    records = [
        checked_record(index, record)
        for index, record in enumerate(cover["records"])
    ]
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-one-unpaid-lra-v1",
        "status": "ALL_FORCED" if all(record["status"] == "FORCED" for record in records) else "FAILED",
        "case_count": len(records),
        "records": records,
        "claim_boundary": (
            "aggregate QF_LRA audit: selected covers are EFX and lex-improving when the named "
            "unpaid recipient meets every assigned-bundle tail; it does not prove that payment inequality"
        ),
        "provenance": {
            "cover_script_sha256": cover["provenance"]["script_sha256"],
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "cases": result["case_count"]}, indent=2))


if __name__ == "__main__":
    main()
