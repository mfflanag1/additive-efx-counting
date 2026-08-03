#!/usr/bin/env python3
"""Replay archived favorite-cell SMT2 formulas in fresh Z3 processes."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

try:
    from .run_lra_cegar import atomic_json
except ImportError:
    from run_lra_cegar import atomic_json


def run(
    *,
    root: Path,
    z3_path: Path,
    time_limit_s: float,
    audit_only: bool,
    output_path: Path,
) -> dict:
    if (
        not root.is_dir()
        or not z3_path.is_file()
        or time_limit_s <= 0
        or output_path.exists()
    ):
        raise ValueError("archive, Z3 binary, timeout, and new output are required")
    expected_cells = {
        ((0, 0, 1, 2), ()),
        ((0, 0, 0, 1), ()),
        ((0, 0, 1, 1), ()),
        ((0, 0, 0, 0), (1, 2, 3, 4)),
        ((0, 0, 0, 0), (1, 1, 1, 1)),
        ((0, 0, 0, 0), (1, 1, 1, 2)),
        ((0, 0, 0, 0), (1, 1, 2, 2)),
        ((0, 0, 0, 0), (1, 1, 2, 3)),
    }
    observed_cells = set()
    cells = []
    for result_path in sorted(root.glob("*-result.json")):
        result = json.loads(result_path.read_text())
        if (
            result.get("schema") != "partition-matching-lra-result-v1"
            or result.get("status") != "UNSAT_CANDIDATE"
            or result.get("selected_shapes")
            != ["2222", "3221", "3311", "4211", "5111"]
            or result.get("strict_favorite_pattern") is None
        ):
            continue
        cell_key = (
            tuple(result["strict_favorite_pattern"]),
            tuple(result.get("strict_second_favorite_pattern") or ()),
        )
        if (
            cell_key not in expected_cells
            or cell_key in observed_cells
            or result.get("partition_count") != 1701
            or result.get("obstruction_encoding") != "matching_clauses"
            or result.get("symmetry") != "none"
            or not result.get("exclude_peelable")
            or not result.get("require_pairwise_distinct_rows")
            or result.get("case_cut") != "no_universal_minimum_good"
        ):
            raise AssertionError(f"unexpected terminal metadata in {result_path.name}")
        observed_cells.add(cell_key)
        formula_path = root / Path(result["smt2_path"]).name
        formula_sha256 = hashlib.sha256(formula_path.read_bytes()).hexdigest()
        if formula_sha256 != result["smt2_sha256"]:
            raise AssertionError(f"formula hash mismatch for {formula_path.name}")
        started = time.time()
        if audit_only:
            returncode = None
            stdout = None
            stderr = None
        else:
            completed = subprocess.run(
                [
                    str(z3_path),
                    f"-T:{round(time_limit_s)}",
                    str(formula_path),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=time_limit_s + 60,
            )
            returncode = completed.returncode
            stdout = completed.stdout.strip()
            stderr = completed.stderr.strip()
        cells.append(
            {
                "result": result_path.name,
                "formula": formula_path.name,
                "formula_sha256": formula_sha256,
                "returncode": returncode,
                "stdout": stdout,
                "stderr": stderr,
                "wall_seconds": round(time.time() - started, 6),
                "confirmed_unsat": (
                    returncode == 0
                    and stdout == "unsat"
                    and not stderr
                )
                if not audit_only
                else None,
            }
        )
    if observed_cells != expected_cells:
        raise AssertionError(
            f"terminal cell coverage mismatch: {observed_cells ^ expected_cells}"
        )
    document = {
        "schema": "favorite-cell-standalone-replay-v1",
        "archive": str(root.resolve()),
        "z3": str(z3_path.resolve()),
        "time_limit_seconds_per_cell": time_limit_s,
        "audit_only": audit_only,
        "cell_count": len(cells),
        "all_confirmed_unsat": (
            all(cell["confirmed_unsat"] for cell in cells)
            if not audit_only
            else None
        ),
        "cells": cells,
    }
    atomic_json(output_path, document)
    print(json.dumps(document, indent=2), flush=True)
    return document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--z3", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=7200)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(
        root=args.root,
        z3_path=args.z3,
        time_limit_s=args.time_limit,
        audit_only=args.audit_only,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
