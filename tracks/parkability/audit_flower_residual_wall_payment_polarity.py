#!/usr/bin/env python3
"""QF_LRA check for the residual-wall unpayable polarity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    own, bottom, retained, residual = z3.Reals(
        "own bottom retained residual"
    )
    min_old, min_new = z3.Reals("min_old min_new")
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        own > 0,
        bottom > 0,
        retained > 0,
        residual > 0,
        min_old > 0,
        min_new > 0,
        min_old <= residual,
        own >= retained + residual - min_old,
        own + residual < bottom + retained - min_new,
        bottom <= residual,
    )
    checked = str(solver.check())
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flower-residual-wall-payment-polarity-audit-v1",
        "status": "FORCED" if checked == "unsat" else "OPEN",
        "record": {
            "claim": "unpayable evolved-target wall forces Bq over R",
            "status": checked,
        },
        "claim_boundary": (
            "QF_LRA audit of the scalar unpayable implication; root payment "
            "uses the analytic early-root bottom polarity"
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
