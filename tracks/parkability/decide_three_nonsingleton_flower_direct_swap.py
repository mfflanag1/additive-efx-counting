#!/usr/bin/env python3
"""Exact aggregate audit of the direct c/s flower swap."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


AGENTS = range(4)
R, Q, C, S = AGENTS


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict:
    base = tuple(z3.Real(f"base_{i}") for i in AGENTS)
    bundles = {
        "xr": tuple(z3.Real(f"xr_{i}") for i in AGENTS),
        "xq": tuple(z3.Real(f"xq_{i}") for i in AGENTS),
        "z": tuple(z3.Real(f"z_{i}") for i in AGENTS),
        "dc": tuple(z3.Real(f"dc_{i}") for i in AGENTS),
    }
    tails = {
        name: tuple(z3.Real(f"{name}_tail_{i}") for i in AGENTS)
        for name in bundles
    }
    solver = z3.SolverFor("QF_LRA")
    for i in AGENTS:
        solver.add(base[i] > 0)
        for name in bundles:
            solver.add(bundles[name][i] > 0)
            solver.add(tails[name][i] >= 0, tails[name][i] <= base[i])
    solver.add(bundles["xr"][R] == base[R])
    solver.add(bundles["xq"][Q] == base[Q])
    solver.add(bundles["z"][C] > base[C])
    solver.add(bundles["dc"][S] > base[S])

    assignment = ("xr", "xq", "z", "dc")
    failure = z3.Or(
        *(
            bundles[assignment[i]][i] < tails[assignment[j]][i]
            for i in AGENTS
            for j in AGENTS
        ),
        bundles["xr"][R] < base[R],
        bundles["xq"][Q] < base[Q],
        bundles["z"][C] <= base[C],
        bundles["dc"][S] <= base[S],
    )
    solver.add(failure)
    checked = solver.check()
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-direct-swap-v1",
        "status": "FORCED" if checked == z3.unsat else str(checked),
        "source_cell": {"third_arm_source": "s", "singleton_envier": "c"},
        "allocation": {"r": "X_r", "q": "X_q", "c": "{z}", "s": "T_c+f"},
        "claim_boundary": "aggregate QF_LRA audit of EFX and strict c/s improvement in the direct flower source cell",
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
    print(json.dumps({"status": result["status"], "source_cell": result["source_cell"]}, indent=2))


if __name__ == "__main__":
    main()
