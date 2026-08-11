#!/usr/bin/env python3
"""QF_LRA check for the early-root charity rotation implication."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    rf, rbr, rbq = z3.Reals("rf rbr rbq")
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        rf > 0,
        rbr > 0,
        rbq > 0,
        rf <= rbr,
        rf > rbq,
        rbr <= rbq,
    )
    script = Path(__file__).resolve()
    root = script.parents[2]
    checked = str(solver.check())
    return {
        "schema": "flower-early-root-charity-rotation-audit-v1",
        "status": "FORCED" if checked == "unsat" else "OPEN",
        "record": {
            "claim": "r(Br)>=r(f)>r(Bq) forces r(Br)>r(Bq)",
            "status": checked,
        },
        "claim_boundary": (
            "aggregate QF_LRA audit of the bottom-order consequence; common "
            "safety and charity dominance of the rotation are analytic"
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
