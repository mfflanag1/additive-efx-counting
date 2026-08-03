#!/usr/bin/env python3
"""Extract tracked cube-literal UNSAT cores from an exact SMT2 cover."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "minimum-slot-cube-assumption-core-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assertions(path: Path):
    solver = z3.Solver()
    solver.from_file(str(path))
    return tuple(solver.assertions())


def run(
    source: Path,
    manifest: Path,
    branch_index: int,
    output: Path,
    timeout_seconds: int,
    solver_profile: str,
):
    if timeout_seconds <= 0 or solver_profile not in {"default", "qf_lra", "arith2"}:
        raise ValueError("positive timeout and supported solver profile required")
    cover = json.loads(manifest.read_text())
    if (
        cover.get("schema") != "minimum-slot-literal-cube-cover-v1"
        or cover.get("source_sha256") != sha256(source)
        or not 0 <= branch_index < len(cover.get("branches", ()))
    ):
        raise ValueError("manifest/source/branch mismatch")
    branch = cover["branches"][branch_index]
    branch_path = Path(branch["path"])
    if sha256(branch_path) != branch["sha256"]:
        raise ValueError("branch hash mismatch")

    base_assertions = assertions(source)
    branch_assertions = assertions(branch_path)
    if (
        len(branch_assertions) - len(base_assertions) != len(branch["cube"])
        or any(
            not left.eq(right)
            for left, right in zip(base_assertions, branch_assertions)
        )
    ):
        raise ValueError("branch is not the source plus its recorded cube")

    solver = z3.SolverFor("QF_LRA") if solver_profile == "qf_lra" else z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    if solver_profile == "arith2":
        solver.set("smt.arith.solver", 2)
    solver.add(*base_assertions)
    labels = []
    for position, literal in enumerate(branch_assertions[len(base_assertions) :]):
        label = z3.Bool(f"cube_{branch_index}_{position}")
        labels.append(label)
        solver.assert_and_track(literal, label)

    started = time.monotonic()
    verdict = solver.check()
    elapsed = time.monotonic() - started
    core_names = (
        {str(label) for label in solver.unsat_core()}
        if verdict == z3.unsat
        else set()
    )
    core_positions = [
        position
        for position, label in enumerate(labels)
        if str(label) in core_names
    ]
    artifact = {
        "schema": SCHEMA,
        "status": (
            "CUBE_ASSUMPTION_CORE_EXTRACTED"
            if verdict == z3.unsat
            else "INCOMPLETE"
        ),
        "meaning": (
            "Tracked UNSAT core over only the exact cube literals; all source "
            "assertions remain untracked premises. This is a core, not "
            "necessarily a minimum core."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "manifest": str(manifest),
        "manifest_sha256": sha256(manifest),
        "branch": branch_index,
        "branch_path": str(branch_path),
        "branch_sha256": branch["sha256"],
        "solver": "z3",
        "solver_version": z3.get_version_string(),
        "solver_profile": solver_profile,
        "timeout_seconds": timeout_seconds,
        "elapsed_seconds": elapsed,
        "verdict": str(verdict),
        "reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "cube_literal_count": len(branch["cube"]),
        "core_literal_count": len(core_positions),
        "core_positions": core_positions,
        "core_literals": [branch["cube"][position] for position in core_positions],
        "cube": branch["cube"],
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--branch", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument(
        "--solver-profile",
        choices=("default", "qf_lra", "arith2"),
        default="qf_lra",
    )
    args = parser.parse_args()
    artifact = run(
        args.source,
        args.manifest,
        args.branch,
        args.output,
        args.timeout_seconds,
        args.solver_profile,
    )
    print(
        json.dumps(
            {
                key: artifact[key]
                for key in (
                    "status",
                    "branch",
                    "solver_profile",
                    "elapsed_seconds",
                    "verdict",
                    "reason_unknown",
                    "cube_literal_count",
                    "core_literal_count",
                    "core_positions",
                    "core_literals",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
