#!/usr/bin/env python3
"""QF_LRA audit of the residual-subset payment polarity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict:
    own_after, bottom, retained, residual, selected = z3.Reals(
        "own_after bottom retained residual selected"
    )
    min_old, min_new = z3.Reals("min_old min_new")
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        own_after > 0,
        bottom > 0,
        retained > 0,
        residual > 0,
        selected >= 0,
        selected <= residual,
        min_old > 0,
        min_new > 0,
        min_old <= residual,
        own_after >= retained + residual - min_old,
        own_after + selected < bottom + retained - min_new,
        bottom <= selected,
    )
    checked = str(solver.check())
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flower-weighted-residual-complement-polarity-audit-v1",
        "status": "FORCED" if checked == "unsat" else "OPEN",
        "record": {
            "claim": "every residual subset that fails a wall is below Bq",
            "status": checked,
        },
        "claim_boundary": (
            "QF_LRA audit of the cap-free scalar implication for an arbitrary "
            "selected residual subset; it proves a strict polarity certificate, "
            "not a contradiction between different valuation rows"
        ),
        "provenance": {
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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
