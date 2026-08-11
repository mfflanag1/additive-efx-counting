#!/usr/bin/env python3
"""Audit the released-owner compensation chain terminal claims and support."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    tr, floater, core, held, escape_q, external, given = z3.Reals(
        "tr floater core held escape_q external given"
    )
    q_wall = z3.SolverFor("QF_LRA")
    q_wall.add(
        tr > 0,
        floater > 0,
        core > 0,
        held >= 0,
        escape_q >= 0,
        external > 0,
        given >= 0,
        given <= external,
        tr + floater > core + held + escape_q,
        tr <= core - external + held + given,
        floater <= escape_q + external - given,
    )
    q_wall_status = str(q_wall.check())
    assert q_wall_status == "unsat"

    r_payment, r_old_release, r_external, r_top = z3.Reals(
        "r_payment r_old_release r_external r_top"
    )
    r_wall = z3.SolverFor("QF_LRA")
    r_wall.add(
        r_payment > 0,
        r_old_release > 0,
        r_external > 0,
        r_top > 0,
        r_payment <= r_top,
        r_old_release + r_external < r_payment,
        r_old_release + r_external >= r_top,
    )
    r_wall_status = str(r_wall.check())
    assert r_wall_status == "unsat"

    incoming = {
        "a": {"K", "f"},
        "q": {"Xa_minus_G", "P"},
        "r": {"H", "G"},
    }
    released = {
        "a": {"Xa_minus_G", "G"},
        "q": {"K", "H"},
        "r": {"P"},
    }
    assert sum(map(len, incoming.values())) == len(set().union(*incoming.values()))
    assert set().union(*incoming.values()) <= {"f"}.union(*released.values())

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "released-owner-compensation-chain-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "expanded_q_exhaustion_forces_root_switch_margin",
                "status": q_wall_status,
            },
            {
                "claim": "expanded_r_exhaustion_is_full_reservoir_wall",
                "status": r_wall_status,
            },
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
            "QF_LRA terminal implications and exact packet support; finite "
            "alternating termination is analytic"
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
