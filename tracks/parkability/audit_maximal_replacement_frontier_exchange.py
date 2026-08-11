#!/usr/bin/env python3
"""Audit scalar implications in the maximal replacement-frontier lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unsat(*constraints):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = str(solver.check())
    assert status == "unsat"
    return status


def run():
    rho, sigma, residual = z3.Reals("rho sigma residual")
    crossing = unsat(
        rho > 0,
        sigma > 0,
        residual > 0,
        residual <= sigma,
        rho + residual > rho,
        rho >= rho + residual,
    )

    removed, inserted = z3.Reals("removed inserted")
    exchange_gap = unsat(
        rho > 0,
        sigma > 0,
        removed >= 0,
        inserted > 0,
        inserted > removed,
        inserted - removed <= sigma,
        rho >= rho - removed + inserted,
    )

    core, complement = z3.Reals("core complement")
    core_complement = unsat(
        rho > 0,
        sigma > 0,
        core > 0,
        complement >= 0,
        core + complement > sigma,
        core < core + complement - sigma,
        complement <= sigma,
    )

    released_crossing = unsat(
        rho > 0,
        sigma > 0,
        complement > sigma,
        rho + complement <= rho + sigma,
    )

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "maximal-replacement-frontier-exchange-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "nonempty_residual_crosses_frontier_slack",
                "status": crossing,
            },
            {
                "claim": "beneficial_exchange_crosses_forbidden_band",
                "status": exchange_gap,
            },
            {
                "claim": "strict_core_capture_leaves_more_than_slack",
                "status": core_complement,
            },
            {
                "claim": "released_complement_crosses_charity",
                "status": released_crossing,
            },
        ],
        "analytic_premises": [
            "finite value-maximal eligible packet",
            "positive charity dominance",
            "subset-sum nondegeneracy",
            "packet-replacement strict core-capture interval",
        ],
        "claim_boundary": (
            "QF_LRA scalar implication audit; existence of the finite "
            "frontier and application of packet maximality are analytic"
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
