#!/usr/bin/env python3
"""Audit that every additive EFX bundle graph has nonempty agent rows."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


def run(output: Path, smt2: Path) -> dict:
    bundle_values = [z3.Real(f"bundle_{bundle}") for bundle in range(4)]
    solver = z3.Solver()
    solver.add(*(value >= 0 for value in bundle_values))
    solver.add(
        *(
            z3.Or(
                *(
                    bundle_values[target] > bundle_values[bundle]
                    for target in range(4)
                    if target != bundle
                )
            )
            for bundle in range(4)
        )
    )
    verdict = solver.check()
    smt2.write_text(solver.to_smt2())
    artifact = {
        "schema": "partial-hall-nonempty-neighbor-audit-v1",
        "status": "PROVED" if verdict == z3.unsat else str(verdict).upper(),
        "meaning": (
            "UNSAT proves that four bundle values cannot each be strictly "
            "below another. If a bundle is not EFX-safe, some residual and "
            "therefore its full target bundle is strictly larger. Hence an "
            "additive observer always has an EFX-safe bundle and a singleton "
            "Hall-deficient set is impossible."
        ),
        "bundle_count": 4,
        "solver_verdict": str(verdict),
        "smt2": str(smt2),
        "smt2_sha256": hashlib.sha256(smt2.read_bytes()).hexdigest(),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.smt2), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
