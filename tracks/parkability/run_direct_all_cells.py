#!/usr/bin/env python3
"""Run the 40,824-allocation cross-encoding in all eight terminal cells."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

try:
    from .run_lra_cegar import atomic_json, atomic_write
except ImportError:
    from run_lra_cegar import atomic_json, atomic_write


@dataclass(frozen=True)
class Cell:
    name: str
    favorites: tuple[int, ...]
    seconds: tuple[int, ...] | None
    stabilizer: bool


CELLS = (
    Cell("favorite-211", (0, 0, 1, 2), None, False),
    Cell("favorite-31", (0, 0, 0, 1), None, True),
    Cell("favorite-22", (0, 0, 1, 1), None, True),
    Cell(
        "top4-second1111",
        (0, 0, 0, 0),
        (1, 2, 3, 4),
        True,
    ),
    Cell("top4-second4", (0, 0, 0, 0), (1, 1, 1, 1), True),
    Cell("top4-second31", (0, 0, 0, 0), (1, 1, 1, 2), True),
    Cell("top4-second22", (0, 0, 0, 0), (1, 1, 2, 2), True),
    Cell("top4-second211", (0, 0, 0, 0), (1, 1, 2, 3), True),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_pool(path: Path) -> dict[str, int]:
    raw = json.loads(path.read_text())
    allocations = (
        raw["allocations"]
        if isinstance(raw, dict)
        else raw
    )
    actual = {tuple(item) for item in allocations}
    expected = {
        assignment
        for assignment in itertools.product(range(4), repeat=8)
        if len(set(assignment)) == 4
    }
    if (
        len(allocations) != 40_824
        or len(actual) != 40_824
        or actual != expected
    ):
        raise ValueError(
            "direct-allocation pool is not the exact onto universe"
        )
    return dict(
        sorted(
            Counter(
                "".join(
                    map(
                        str,
                        sorted(
                            (
                                assignment.count(agent)
                                for agent in range(4)
                            ),
                            reverse=True,
                        ),
                    )
                )
                for assignment in actual
            ).items()
        )
    )


def validate_record(
    cell: Cell,
    result_path: Path,
    formula_path: Path,
    expected_pool_sha256: str,
) -> dict:
    record = json.loads(result_path.read_text())
    if (
        record.get("schema") != "direct-ranking-cell-lra-result-v1"
        or record.get("favorite_pattern") != list(cell.favorites)
        or record.get("second_favorite_pattern")
        != (list(cell.seconds) if cell.seconds is not None else None)
        or record.get("pattern_stabilizer") is not cell.stabilizer
        or record.get("allocation_count") != 40_824
        or record.get("pool_sha256") != expected_pool_sha256
        or record.get("smt2_sha256") != sha256(formula_path)
    ):
        raise ValueError(f"{cell.name}: invalid existing result record")
    return record


def validate_cvc5_replay(
    *,
    cell: Cell,
    output: Path,
    formula_path: Path,
    record: dict,
) -> dict | None:
    normalized_path = output / f"{cell.name}.direct.cvc5.smt2"
    normalization_path = output / f"{cell.name}.direct.cvc5-normalization.json"
    replay_path = output / f"{cell.name}.direct.cvc5.json"
    if not replay_path.exists():
        return None
    if not normalized_path.is_file() or not normalization_path.is_file():
        raise ValueError(f"{cell.name}: incomplete cvc5 replay artifacts")

    normalization = json.loads(normalization_path.read_text())
    normalized_hash = sha256(normalized_path)
    if (
        normalization.get("schema") != "strict-smt2-normalization-v1"
        or Path(normalization.get("source", "")).resolve()
        != formula_path.resolve()
        or normalization.get("source_sha256") != record["smt2_sha256"]
        or Path(normalization.get("output", "")).resolve()
        != normalized_path.resolve()
        or normalization.get("output_sha256") != normalized_hash
        or normalization.get("transformation", {}).get("inserted_logic")
        != "QF_LRA"
    ):
        raise ValueError(f"{cell.name}: invalid cvc5 normalization record")

    replay = json.loads(replay_path.read_text())
    if (
        replay.get("schema") != "external-smt-replay-v1"
        or replay.get("solver_interface") != "cvc5"
        or replay.get("timed_out") is not False
        or replay.get("returncode") != 0
        or replay.get("verdict") != "unsat"
        or replay.get("expected") != "unsat"
        or replay.get("confirmed_expected") is not True
        or Path(replay.get("formula", "")).resolve()
        != normalized_path.resolve()
        or replay.get("formula_sha256") != normalized_hash
    ):
        raise ValueError(f"{cell.name}: cvc5 replay does not prove UNSAT")
    return {
        "status": "UNSAT_CVC5_REPLAY",
        "solver_status": "unsat",
        "solver_wall_seconds": replay["elapsed_seconds"],
        "auxiliary_artifacts": [
            {
                "role": "cvc5_normalized_formula",
                "path": normalized_path.name,
                "sha256": normalized_hash,
            },
            {
                "role": "cvc5_normalization_record",
                "path": normalization_path.name,
                "sha256": sha256(normalization_path),
            },
            {
                "role": "cvc5_replay_record",
                "path": replay_path.name,
                "sha256": sha256(replay_path),
            },
        ],
    }


def unsat_evidence(
    *,
    cell: Cell,
    output: Path,
    formula_path: Path,
    record: dict,
) -> dict:
    if (
        record.get("status") == "UNSAT_CANDIDATE"
        and record.get("solver_status") == "unsat"
    ):
        return {
            "status": record["status"],
            "solver_status": record["solver_status"],
            "solver_wall_seconds": record["solver_wall_seconds"],
            "auxiliary_artifacts": [],
        }
    replay = validate_cvc5_replay(
        cell=cell,
        output=output,
        formula_path=formula_path,
        record=record,
    )
    if replay is not None:
        return replay
    return {
        "status": record["status"],
        "solver_status": record["solver_status"],
        "solver_wall_seconds": record["solver_wall_seconds"],
        "auxiliary_artifacts": [],
    }


def run_cell(
    *,
    runner: Path,
    pool: Path,
    output: Path,
    cell: Cell,
    time_limit: float,
    pool_sha256: str,
) -> dict:
    result_path = output / f"{cell.name}.direct.json"
    formula_path = output / f"{cell.name}.direct.smt2"
    log_path = output / f"{cell.name}.direct.log"
    existing = (result_path.exists(), formula_path.exists())
    if existing == (True, True):
        return validate_record(
            cell,
            result_path,
            formula_path,
            pool_sha256,
        )
    if existing != (False, False):
        raise ValueError(
            f"{cell.name}: incomplete direct-crosscheck artifacts"
        )

    command = [
        sys.executable,
        str(runner),
        "--pool",
        str(pool),
        "--favorite-pattern",
        ",".join(map(str, cell.favorites)),
        "--time-limit",
        str(time_limit),
        "--result",
        str(result_path),
        "--smt2",
        str(formula_path),
    ]
    if cell.seconds is not None:
        command.extend(
            [
                "--second-favorite-pattern",
                ",".join(map(str, cell.seconds)),
            ]
        )
    if cell.stabilizer:
        command.append("--pattern-stabilizer")
    started = time.time()
    process = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    atomic_write(log_path, process.stdout)
    if process.returncode != 0:
        raise RuntimeError(
            f"{cell.name}: direct crosscheck failed after "
            f"{time.time() - started:.3f}s; see {log_path}"
        )
    return validate_record(
        cell,
        result_path,
        formula_path,
        pool_sha256,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=21_600)
    parser.add_argument(
        "--cells",
        help="comma-separated subset; default is all eight",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    chosen = (
        set(args.cells.split(","))
        if args.cells
        else {cell.name for cell in CELLS}
    )
    known = {cell.name for cell in CELLS}
    if not chosen or not chosen <= known:
        raise ValueError(f"unknown or empty cell set: {chosen - known}")
    pool_shapes = audit_pool(args.pool)
    pool_hash = sha256(args.pool)

    runner = Path(__file__).with_name(
        "run_direct_cell_lra.py"
    ).resolve()
    records = []
    for cell in CELLS:
        if cell.name not in chosen:
            continue
        record = run_cell(
            runner=runner,
            pool=args.pool.resolve(),
            output=output,
            cell=cell,
            time_limit=args.time_limit,
            pool_sha256=pool_hash,
        )
        formula_path = output / f"{cell.name}.direct.smt2"
        evidence = unsat_evidence(
            cell=cell,
            output=output,
            formula_path=formula_path,
            record=record,
        )
        records.append(
            {
                "cell": cell.name,
                "status": evidence["status"],
                "base_result_status": record["status"],
                "solver_status": evidence["solver_status"],
                "solver_wall_seconds": evidence["solver_wall_seconds"],
                "formula": f"{cell.name}.direct.smt2",
                "formula_sha256": record["smt2_sha256"],
                "result": f"{cell.name}.direct.json",
                "result_sha256": sha256(
                    output / f"{cell.name}.direct.json"
                ),
                "auxiliary_artifacts": evidence["auxiliary_artifacts"],
            }
        )
        payload = {
            "schema": "direct-all-eight-cells-crosscheck-v1",
            "requested_cells": sorted(chosen),
            "completed_cell_count": len(records),
            "all_requested_completed": len(records) == len(chosen),
            "all_completed_unsat": all(
                item["status"]
                in {"UNSAT_CANDIDATE", "UNSAT_CVC5_REPLAY"}
                for item in records
            ),
            "allocation_count_per_cell": 40_824,
            "pool_universe_exact": True,
            "pool_count_by_labeled_shape": pool_shapes,
            "pool": str(args.pool.resolve()),
            "pool_sha256": pool_hash,
            "records": records,
        }
        atomic_json(
            output / "DIRECT_ALLOCATION_CROSSCHECK.json",
            payload,
        )
        print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
