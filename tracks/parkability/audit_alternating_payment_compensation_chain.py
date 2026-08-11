#!/usr/bin/env python3
"""Audit terminal implications of the alternating compensation chain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    tr, floater, base, external, core, released, compensation = z3.Reals(
        "tr floater base external core released compensation"
    )
    q_wall = z3.SolverFor("QF_LRA")
    q_wall.add(
        tr > 0,
        floater > 0,
        base > 0,
        external > 0,
        core > external,
        released > 0,
        compensation >= 0,
        compensation <= released,
        core + released == base,
        tr + floater > base,
        tr <= core - external + compensation,
        external >= floater,
    )
    q_wall_status = str(q_wall.check())
    assert q_wall_status == "unsat"

    r_payment, r_released, r_top = z3.Reals(
        "r_payment r_released r_top"
    )
    r_wall = z3.SolverFor("QF_LRA")
    r_wall.add(
        r_payment > 0,
        r_released > 0,
        r_top > 0,
        r_payment <= r_top,
        r_released < r_payment,
        r_released >= r_top,
    )
    r_wall_status = str(r_wall.check())
    assert r_wall_status == "unsat"

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "alternating-payment-compensation-chain-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "q_exhaustion_forces_external_below_floater",
                "status": q_wall_status,
            },
            {
                "claim": "r_exhaustion_is_stronger_than_aggregate_r_wall",
                "status": r_wall_status,
            },
        ],
        "analytic_records": [
            {
                "claim": "monotone_chain_terminates",
                "reason": "each repair strictly enlarges P or H inside finite disjoint reservoirs",
            },
            {
                "claim": "repair_packets_are_deletion_critical",
                "reason": "each repair packet is selected inclusion-minimally",
            },
        ],
        "claim_boundary": (
            "QF_LRA terminal-wall audit plus finite-set analytic termination; "
            "existence of the initial payment packet is inherited from the "
            "packet-replacement complement-return lemma"
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
