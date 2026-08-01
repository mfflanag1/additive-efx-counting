#!/usr/bin/env python3
"""Differentially audit the independent SMT-LIB partition encoding."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .independent_lra_generator import (
        M,
        N,
        Formula,
        add_partition_obstruction,
        iter_partitions,
        value,
    )
except ImportError:
    import core
    import independent
    from independent_lra_generator import (
        M,
        N,
        Formula,
        add_partition_obstruction,
        iter_partitions,
        value,
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def supports_efx(
    values: tuple[tuple[int, ...], ...],
    partition: tuple[tuple[int, ...], ...],
) -> bool:
    for matching in itertools.permutations(range(N)):
        assignment = [0] * M
        for agent, bundle_index in enumerate(matching):
            for good in partition[bundle_index]:
                assignment[good] = agent
        if independent.is_complete_efx0(values, assignment):
            return True
    return False


def make_batch(
    values: tuple[tuple[int, ...], ...],
    partitions: tuple[tuple[tuple[int, ...], ...], ...],
) -> bytes:
    formula = Formula()
    formula.lines = [
        "; fixed-matrix differential audit of independent partition encoding",
        "(set-logic QF_LRA)",
    ]
    for agent in range(N):
        for good in range(M):
            formula.declare_real(value(agent, good))
    for agent, row in enumerate(values):
        total = sum(row)
        for good, item in enumerate(row):
            formula.assert_(
                f"(= {value(agent, good)} (/ {item} {total}))"
            )
    for index, partition in enumerate(partitions):
        formula.lines.append("(push 1)")
        add_partition_obstruction(formula, index, partition)
        formula.lines.append("(check-sat)")
        formula.lines.append("(pop 1)")
    return ("\n".join([*formula.lines, ""]) + "\n").encode()


def run(
    *,
    matrix_paths: tuple[Path, ...],
    solver_path: Path,
    output_dir: Path,
    time_limit_s: float,
) -> dict:
    if (
        not matrix_paths
        or not solver_path.is_file()
        or time_limit_s <= 0
        or (output_dir / "audit.json").exists()
    ):
        raise ValueError("matrices, solver, timeout, and new output are required")
    project_partitions = tuple(core.iter_unlabeled_nonempty_partitions(N, M))
    independent_partitions = tuple(iter_partitions(N, M))
    partition_sets_equal = set(project_partitions) == set(independent_partitions)
    if len(independent_partitions) != 1701 or not partition_sets_equal:
        raise AssertionError("independent partition universe mismatch")
    records = []
    for matrix_path in matrix_paths:
        raw = json.loads(matrix_path.read_text())
        values = core.validate_values(
            raw["values"],
            expected_n=N,
            expected_m=M,
            lower=1,
        )
        expected = [
            "unsat" if supports_efx(values, partition) else "sat"
            for partition in independent_partitions
        ]
        batch_path = output_dir / f"{matrix_path.stem}.partition-audit.smt2"
        batch_bytes = make_batch(values, independent_partitions)
        atomic_write(batch_path, batch_bytes)
        started = time.monotonic()
        completed = subprocess.run(
            [
                str(solver_path),
                f"-T:{round(time_limit_s)}",
                str(batch_path),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=time_limit_s + 60,
        )
        elapsed = time.monotonic() - started
        actual = [
            line.strip()
            for line in completed.stdout.splitlines()
            if line.strip() in {"sat", "unsat", "unknown"}
        ]
        mismatches = [
            {
                "partition_index": index,
                "partition": independent_partitions[index],
                "expected": wanted,
                "actual": actual[index] if index < len(actual) else None,
            }
            for index, wanted in enumerate(expected)
            if index >= len(actual) or actual[index] != wanted
        ]
        records.append(
            {
                "matrix": str(matrix_path.resolve()),
                "matrix_sha256": file_sha256(matrix_path),
                "batch": str(batch_path.resolve()),
                "batch_sha256": hashlib.sha256(batch_bytes).hexdigest(),
                "returncode": completed.returncode,
                "stderr": completed.stderr.strip(),
                "elapsed_seconds": round(elapsed, 6),
                "expected_counts": dict(sorted(Counter(expected).items())),
                "actual_counts": dict(sorted(Counter(actual).items())),
                "verdict_count": len(actual),
                "mismatch_count": len(mismatches),
                "mismatches": mismatches[:20],
                "passed": (
                    completed.returncode == 0
                    and not completed.stderr.strip()
                    and len(actual) == len(expected)
                    and not mismatches
                ),
            }
        )
    document = {
        "schema": "independent-lra-generator-audit-v1",
        "meaning": (
            "every partition obstruction is checked at fixed matrices against "
            "the definition-literal EFX evaluator"
        ),
        "solver": str(solver_path.resolve()),
        "solver_sha256": file_sha256(solver_path),
        "partition_count": len(independent_partitions),
        "partition_sets_equal": partition_sets_equal,
        "matrix_count": len(records),
        "all_passed": all(record["passed"] for record in records),
        "records": records,
    }
    atomic_write(
        output_dir / "audit.json",
        (json.dumps(document, indent=2, sort_keys=True) + "\n").encode(),
    )
    print(json.dumps(document, indent=2, sort_keys=True), flush=True)
    if not document["all_passed"]:
        raise SystemExit(2)
    return document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, action="append", required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, required=True)
    args = parser.parse_args()
    run(
        matrix_paths=tuple(args.matrix),
        solver_path=args.solver,
        output_dir=args.output_dir,
        time_limit_s=args.time_limit,
    )


if __name__ == "__main__":
    main()
