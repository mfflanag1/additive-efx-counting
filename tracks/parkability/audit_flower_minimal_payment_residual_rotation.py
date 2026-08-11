#!/usr/bin/env python3
"""QF_LRA check for the minimal-payment residual target wall."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def charge(total, least, core_least):
    return total + core_least - z3.If(
        core_least <= least, core_least, least
    )


def run():
    own, old_charge, core_least = z3.Reals(
        "own old_charge core_least"
    )
    old_total, old_least, new_total, new_least = z3.Reals(
        "old_total old_least new_total new_least"
    )
    old = charge(old_total, old_least, core_least)
    new = charge(new_total, new_least, core_least)
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        own > 0,
        core_least > 0,
        old_total >= old_least,
        old_least > 0,
        new_total >= new_least,
        new_least > 0,
        old_charge >= 0,
        own >= old_charge + old,
        own < old_charge + new,
        new <= old,
    )
    checked = str(solver.check())
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flower-minimal-payment-residual-rotation-audit-v1",
        "status": "FORCED" if checked == "unsat" else "OPEN",
        "record": {
            "claim": "new target wall forces larger insertion charge",
            "status": checked,
        },
        "claim_boundary": (
            "QF_LRA audit of the threshold-charge implication; selection, "
            "charity dominance, and failure exhaustiveness are analytic"
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
