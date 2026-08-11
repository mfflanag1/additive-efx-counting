#!/usr/bin/env python3
"""QF_LRA checks for the lex-rooted donation wall implications."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name, constraints):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def threshold(residual, minimum, item):
    return residual + z3.If(item > minimum, item - minimum, 0)


def run():
    residual, minimum, h, g, own, charity = z3.Reals(
        "residual minimum h g own charity"
    )
    positive = [
        residual > 0, minimum > 0, residual >= minimum,
        h > 0, g > 0, own > 0, charity >= 0,
    ]
    records = [
        checked(
            "external_root_wall_forces_h_over_g",
            positive + [
                own >= threshold(residual, minimum, g),
                own < threshold(residual, minimum, h),
                h <= g,
            ],
        ),
        checked(
            "external_charity_wall_forces_release_over_slack",
            positive + [own >= charity, own < charity + g, g <= own - charity],
        ),
    ]
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "lex-rooted-owner-charity-donation-obstruction-audit-v1",
        "status": (
            "ALL_FORCED"
            if all(record["status"] == "unsat" for record in records)
            else "OPEN"
        ),
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of the two scalar wall implications; failure "
            "exhaustiveness and generalized-edge conversion are analytic"
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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
