#!/usr/bin/env python3
"""Audit the Q-exhaustion root-switch inequality and support."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    tr, floater, core, held, escape, external = z3.Reals(
        "tr floater core held escape external"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        tr > 0,
        floater > 0,
        core > 0,
        held >= 0,
        escape >= 0,
        external > 0,
        tr + floater > core + held + escape,
        tr <= core - external + held,
        floater <= escape + external,
    )
    scalar_status = str(solver.check())
    assert scalar_status == "unsat"

    incoming = {"q": {"f"}, "a": {"E"}}
    released = {"q": {"E"}, "a": set()}
    assert not (incoming["q"] & incoming["a"])
    assert set().union(*incoming.values()) <= {"f"}.union(*released.values())

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "q-exhaustion-root-switch-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "q_exhaustion_forces_f_above_escape_plus_external",
                "status": scalar_status,
            }
        ],
        "support_record": {
            "incoming": {
                key: sorted(value) for key, value in incoming.items()
            },
            "released": {
                key: sorted(value) for key, value in released.items()
            },
            "initially_unallocated": ["f"],
        },
        "claim_boundary": (
            "QF_LRA root-switch implication and one-edge support; EFX and "
            "response-Hall alternatives use the transfer-tree theorem"
        ),
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
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
