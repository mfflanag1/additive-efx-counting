#!/usr/bin/env python3
"""Rebuild the eight archived favorite-cell formulas without solving them."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import tempfile
from dataclasses import dataclass
from pathlib import Path

import z3

try:
    from . import core
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import core
    from lra_master import ParkabilityLRAMaster


N = 4
M = 8


@dataclass(frozen=True)
class Cell:
    archive_stem: str
    favorites: tuple[int, ...]
    seconds: tuple[int, ...] | None
    favorite_stabilizer: bool
    prefix_stabilizer: bool


CELLS = (
    Cell("partition-favorite-211", (0, 0, 1, 2), None, False, False),
    Cell("partition-favorite-31", (0, 0, 0, 1), None, True, False),
    Cell("partition-favorite-22", (0, 0, 1, 1), None, True, False),
    Cell("partition-top4-second1111", (0, 0, 0, 0), (1, 2, 3, 4), False, True),
    Cell("partition-top4-second4", (0, 0, 0, 0), (1, 1, 1, 1), False, True),
    Cell("partition-top4-second31", (0, 0, 0, 0), (1, 1, 1, 2), False, True),
    Cell("partition-top4-second22", (0, 0, 0, 0), (1, 1, 2, 2), False, True),
    Cell("partition-top4-second211", (0, 0, 0, 0), (1, 1, 2, 3), False, True),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes())


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


def build_formula(cell: Cell) -> tuple[bytes, int]:
    master = ParkabilityLRAMaster(
        N,
        M,
        exclude_universal_min=True,
        exclude_peelable=True,
        require_pairwise_distinct_rows=True,
    )
    master.add_strict_favorite_pattern(cell.favorites)
    if cell.favorite_stabilizer:
        master.add_favorite_pattern_stabilizer(cell.favorites)
    if cell.seconds is not None:
        prefixes = tuple(zip(cell.favorites, cell.seconds))
        master.add_strict_ranking_prefixes(prefixes)
        if cell.prefix_stabilizer:
            master.add_ranking_prefix_stabilizer(prefixes)
    partition_count = 0
    for partition in core.iter_unlabeled_nonempty_partitions(N, M):
        if not master.add_partition_obstruction(
            partition,
            encoding="matching_clauses",
        ):
            raise AssertionError("partition generator emitted a duplicate")
        partition_count += 1
    if partition_count != 1701:
        raise AssertionError(f"unexpected partition count: {partition_count}")
    return master.to_smt2().encode(), partition_count


def rebuild_one(*, cell: Cell, archive: Path, output_dir: Path) -> dict:
    archive_formula = archive / f"{cell.archive_stem}.smt2"
    archive_result = archive / f"{cell.archive_stem}-result.json"
    output_formula = output_dir / f"{cell.archive_stem}.rebuilt.smt2"
    output_metadata = output_dir / f"{cell.archive_stem}.rebuild.json"
    if (
        not archive_formula.is_file()
        or not archive_result.is_file()
        or output_formula.exists()
        or output_metadata.exists()
    ):
        raise ValueError(f"missing archive input or existing output for {cell}")
    result = json.loads(archive_result.read_text())
    formula, partition_count = build_formula(cell)
    atomic_write(output_formula, formula)
    rebuilt_hash = sha256(formula)
    archive_bytes = archive_formula.read_bytes()
    archive_hash = sha256(archive_bytes)
    record = {
        "schema": "favorite-cell-single-byte-rebuild-v1",
        "cell": cell.archive_stem,
        "partition_count": partition_count,
        "archive_formula": str(archive_formula.resolve()),
        "archive_sha256": archive_hash,
        "recorded_archive_sha256": result["smt2_sha256"],
        "rebuilt_formula": str(output_formula.resolve()),
        "rebuilt_sha256": rebuilt_hash,
        "byte_identical": (
            rebuilt_hash == archive_hash == result["smt2_sha256"]
            and formula == archive_bytes
        ),
        "environment": {
            "python": platform.python_version(),
            "z3": z3.get_version_string(),
        },
    }
    atomic_write(
        output_metadata,
        (json.dumps(record, indent=2, sort_keys=True) + "\n").encode(),
    )
    print(json.dumps(record, indent=2, sort_keys=True), flush=True)
    if not record["byte_identical"]:
        raise SystemExit(2)
    return record


def aggregate(*, output_dir: Path) -> dict:
    metadata_path = output_dir / "rebuild-audit.json"
    if metadata_path.exists():
        raise ValueError("rebuild metadata already exists")
    records = []
    for cell in CELLS:
        path = output_dir / f"{cell.archive_stem}.rebuild.json"
        if not path.is_file():
            raise ValueError(f"missing isolated rebuild record: {path}")
        record = json.loads(path.read_text())
        if (
            record.get("schema") != "favorite-cell-single-byte-rebuild-v1"
            or record.get("cell") != cell.archive_stem
        ):
            raise ValueError(f"invalid isolated rebuild record: {path}")
        records.append(record)
    source_paths = [
        Path(__file__),
        Path(core.__file__),
        Path(__file__).with_name("lra_master.py"),
    ]
    document = {
        "schema": "favorite-cell-byte-rebuild-v1",
        "meaning": (
            "each formula was rebuilt in a separate fresh Python process "
            "using the original project encoder"
        ),
        "sources": {
            str(path.resolve()): file_sha256(path) for path in source_paths
        },
        "cell_count": len(records),
        "all_byte_identical": all(record["byte_identical"] for record in records),
        "cells": records,
    }
    atomic_write(
        metadata_path,
        (json.dumps(document, indent=2, sort_keys=True) + "\n").encode(),
    )
    print(json.dumps(document, indent=2, sort_keys=True), flush=True)
    if not document["all_byte_identical"]:
        raise SystemExit(2)
    return document


def run(*, archive: Path, output_dir: Path) -> dict:
    if not archive.is_dir():
        raise ValueError("archive directory is required")
    records = []
    for cell in CELLS:
        archive_formula = archive / f"{cell.archive_stem}.smt2"
        archive_result = archive / f"{cell.archive_stem}-result.json"
        output_formula = output_dir / f"{cell.archive_stem}.rebuilt.smt2"
        if (
            not archive_formula.is_file()
            or not archive_result.is_file()
            or output_formula.exists()
        ):
            raise ValueError(f"missing archive input or existing output for {cell}")
        result = json.loads(archive_result.read_text())
        formula, partition_count = build_formula(cell)
        atomic_write(output_formula, formula)
        rebuilt_hash = sha256(formula)
        archive_hash = file_sha256(archive_formula)
        records.append(
            {
                "cell": cell.archive_stem,
                "partition_count": partition_count,
                "archive_formula": str(archive_formula.resolve()),
                "archive_sha256": archive_hash,
                "recorded_archive_sha256": result["smt2_sha256"],
                "rebuilt_formula": str(output_formula.resolve()),
                "rebuilt_sha256": rebuilt_hash,
                "byte_identical": (
                    rebuilt_hash == archive_hash == result["smt2_sha256"]
                    and formula == archive_formula.read_bytes()
                ),
            }
        )
    source_paths = [
        Path(__file__),
        Path(core.__file__),
        Path(__file__).with_name("lra_master.py"),
    ]
    document = {
        "schema": "favorite-cell-byte-rebuild-v1",
        "meaning": (
            "deterministic formula rebuild using the original project encoder; "
            "this is reproducibility evidence, not an independent encoding"
        ),
        "environment": {
            "python": platform.python_version(),
            "z3": z3.get_version_string(),
        },
        "sources": {
            str(path.resolve()): file_sha256(path) for path in source_paths
        },
        "cell_count": len(records),
        "all_byte_identical": all(record["byte_identical"] for record in records),
        "cells": records,
    }
    metadata_path = output_dir / "rebuild-audit.json"
    if metadata_path.exists():
        raise ValueError("rebuild metadata already exists")
    atomic_write(
        metadata_path,
        (json.dumps(document, indent=2, sort_keys=True) + "\n").encode(),
    )
    print(json.dumps(document, indent=2, sort_keys=True), flush=True)
    if not document["all_byte_identical"]:
        raise SystemExit(2)
    return document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--cell",
        choices=[cell.archive_stem for cell in CELLS],
    )
    parser.add_argument("--aggregate", action="store_true")
    args = parser.parse_args()
    if args.cell is not None and args.aggregate:
        parser.error("--cell and --aggregate are mutually exclusive")
    if args.aggregate:
        aggregate(output_dir=args.output_dir)
    elif args.cell is not None:
        cell = next(cell for cell in CELLS if cell.archive_stem == args.cell)
        rebuild_one(cell=cell, archive=args.archive, output_dir=args.output_dir)
    else:
        run(archive=args.archive, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
