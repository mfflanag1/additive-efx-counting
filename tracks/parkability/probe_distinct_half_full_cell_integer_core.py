#!/usr/bin/env python3
"""Probe a fixed obstruction core at a chosen positive-integer cap."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .run_distinct_half_full_cell_cegar import full_hall_cells
    from .run_generic_partition_cegar import supported_partitions
    from .terminal_cnf import decode_values, solve_formula
    from .terminal_distinct_half_full_cell_cnf import build
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from run_distinct_half_full_cell_cegar import full_hall_cells
    from run_generic_partition_cegar import supported_partitions
    from terminal_cnf import decode_values, solve_formula
    from terminal_distinct_half_full_cell_cnf import build


SCHEMA = "distinct-half-full-cell-integer-core-probe-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def real_canonical_agent_order(values):
    """Find an agent permutation satisfying the normalized-real symmetries."""
    for order in itertools.permutations(range(4)):
        rows = tuple(values[agent] for agent in order)
        normalized_favorites = tuple(
            Fraction(row[0], sum(row)) for row in rows
        )
        if (
            all(
                normalized_favorites[agent]
                >= normalized_favorites[agent + 1]
                for agent in range(3)
            )
            and all(2 * rows[agent][agent + 1] > rows[agent][0]
                    for agent in range(4))
            and all(rows[0][good] >= rows[0][good + 1]
                    for good in range(5, 8))
        ):
            return order, rows
    return None, None


def run(source_path: Path, cap: int):
    source = json.loads(source_path.read_text())
    started = time.perf_counter()
    encoder, partitions, full_cell_encoding = build(source, cap)
    build_seconds = time.perf_counter() - started
    solve_started = time.perf_counter()
    solved = solve_formula(encoder.cnf.clauses, "cadical195")
    solve_seconds = time.perf_counter() - solve_started

    values = (
        tuple(tuple(row) for row in decode_values(
            solved["model"], encoder.value_bits
        ))
        if solved["status"]
        else None
    )
    universe = tuple(favorite_pair_balanced_universe())
    repairs = ()
    cells = ()
    if values is not None:
        audit_branch(values)
        cells = tuple(tuple(cell) for cell in full_hall_cells(values))
        if cells:
            raise AssertionError("decoded model has a forbidden full Hall cell")
        if supported_partitions(values, list(partitions)):
            raise AssertionError("decoded model repairs a core partition")
        repairs = supported_partitions(values, list(universe))
    canonical_order, canonical_values = (
        real_canonical_agent_order(values)
        if values is not None
        else (None, None)
    )

    return {
        "schema": SCHEMA,
        "status": "SAT_CORE_ESCAPE" if values is not None else "UNSAT",
        "solver": "CaDiCaL 1.9.5 through PySAT",
        "cap": cap,
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "core_size": len(partitions),
        "variables": encoder.cnf.nv,
        "clauses": len(encoder.cnf.clauses),
        "full_cell_encoding": full_cell_encoding,
        "seconds": {
            "build": round(build_seconds, 6),
            "solve": round(solve_seconds, 6),
            "total": round(time.perf_counter() - started, 6),
        },
        "values": [list(row) for row in values] if values is not None else None,
        "real_canonical_agent_order": (
            list(canonical_order) if canonical_order is not None else None
        ),
        "real_canonical_values": (
            [list(row) for row in canonical_values]
            if canonical_values is not None
            else None
        ),
        "full_hall_cells": [list(cell) for cell in cells],
        "favorite_pair_repair_count": len(repairs),
        "favorite_pair_repair_sample": [
            [list(bundle) for bundle in partition]
            for partition in repairs[:20]
        ],
        "literal_complete_efx_count": (
            independent.count_complete_efx0(values)
            if values is not None
            else None
        ),
        "interpretation": (
            "SAT means this fixed partition core is cap-specific; it does "
            "not refute the full 840-partition dichotomy. UNSAT closes only "
            "the selected finite core at the stated integer cap."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.cap < 2:
        parser.error("cap must be at least two")
    result = run(args.source, args.cap)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
