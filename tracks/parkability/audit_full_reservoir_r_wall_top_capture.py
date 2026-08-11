#!/usr/bin/env python3
"""Audit the full-reservoir R-wall top-capture implication."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    top_core, top_rest, bottom_missing, external = z3.Reals(
        "top_core top_rest bottom_missing external"
    )
    root_top, payment, root_bottom, floater = z3.Reals(
        "root_top payment root_bottom floater"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        top_core >= 0,
        top_rest >= 0,
        bottom_missing >= 0,
        external > 0,
        root_top > 0,
        payment > 0,
        root_bottom > 0,
        floater > 0,
        payment <= root_top,
        top_rest + bottom_missing + external < payment,
        top_core + top_rest + floater > root_top + root_bottom,
        root_bottom >= floater,
        top_core <= bottom_missing + external,
    )
    status = str(solver.check())
    assert status == "unsat"

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "full-reservoir-r-wall-top-capture-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "full_reservoir_r_wall_forces_strict_top_capture",
                "status": status,
            }
        ],
        "claim_boundary": (
            "QF_LRA aggregate packet implication; packet decomposition, "
            "positivity, and the early-root inequality are analytic premises"
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
