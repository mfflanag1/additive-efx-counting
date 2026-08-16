#!/usr/bin/env python3
"""Differentially audit independent residual and cell constraints."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import tempfile
from collections import Counter
from pathlib import Path

import z3

try:
    from .independent_lra_generator import (
        CELLS,
        M,
        N,
        Cell,
        Formula,
        add_cell,
        add_domain,
        add_residual_reductions,
        value,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from independent_lra_generator import (
        CELLS,
        M,
        N,
        Cell,
        Formula,
        add_cell,
        add_domain,
        add_residual_reductions,
        value,
    )
    from lra_master import ParkabilityLRAMaster


def atomic_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(document, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def configure_original(master: ParkabilityLRAMaster, cell: Cell) -> None:
    master.add_strict_favorite_pattern(cell.favorites)
    if cell.favorite_stabilizer:
        master.add_favorite_pattern_stabilizer(cell.favorites)
    if cell.seconds is not None:
        prefixes = tuple(zip(cell.favorites, cell.seconds))
        master.add_strict_ranking_prefixes(prefixes)
        if cell.prefix_stabilizer:
            master.add_ranking_prefix_stabilizer(prefixes)


def original_status(
    values: tuple[tuple[int, ...], ...],
    cell: Cell,
) -> str:
    master = ParkabilityLRAMaster(
        N,
        M,
        exclude_universal_min=True,
        exclude_peelable=True,
        require_pairwise_distinct_rows=True,
        fixed_values=values,
    )
    configure_original(master, cell)
    return master.solve(time_limit_s=10).status


def independent_status(
    values: tuple[tuple[int, ...], ...],
    cell: Cell,
) -> str:
    formula = Formula()
    add_domain(formula)
    add_residual_reductions(formula)
    add_cell(formula, cell)
    for agent, row in enumerate(values):
        total = sum(row)
        for good, item in enumerate(row):
            formula.assert_(
                f"(= {value(agent, good)} (/ {item} {total}))"
            )
    script = formula.render().decode()
    solver = z3.SolverFor("QF_LRA")
    solver.add(z3.parse_smt2_string(script))
    status = solver.check()
    if status == z3.sat:
        return "SAT"
    if status == z3.unsat:
        return "UNSAT"
    return "UNKNOWN"


def satisfying_witness(cell: Cell) -> tuple[tuple[int, ...], ...]:
    master = ParkabilityLRAMaster(
        N,
        M,
        exclude_universal_min=True,
        exclude_peelable=True,
        require_pairwise_distinct_rows=True,
    )
    configure_original(master, cell)
    result = master.solve(time_limit_s=30)
    if result.status != "SAT" or result.values is None:
        raise AssertionError(f"original preamble unexpectedly {result.status}: {cell}")
    return result.values


def run(*, output_path: Path, random_count: int, seed: int) -> dict:
    if output_path.exists() or random_count < 1:
        raise ValueError("new output and positive random count are required")
    generator = random.Random(seed)
    witness_values = [satisfying_witness(cell) for cell in CELLS]
    random_values = [
        tuple(
            tuple(generator.randint(1, 20) for _ in range(M))
            for _ in range(N)
        )
        for _ in range(random_count)
    ]
    repeated_row = tuple(tuple(range(1, M + 1)) for _ in range(N))
    tied_rows = tuple(
        tuple(1 + ((agent + good) % 3) for good in range(M))
        for agent in range(N)
    )
    matrices = [*witness_values, *random_values, repeated_row, tied_rows]
    comparisons = []
    counts: dict[str, Counter[str]] = {
        cell.name: Counter() for cell in CELLS
    }
    for matrix_index, values in enumerate(matrices):
        for cell in CELLS:
            original = original_status(values, cell)
            independent = independent_status(values, cell)
            counts[cell.name][f"{original}/{independent}"] += 1
            if original != independent:
                comparisons.append(
                    {
                        "matrix_index": matrix_index,
                        "cell": cell.name,
                        "original": original,
                        "independent": independent,
                        "values": values,
                    }
                )
    document = {
        "schema": "independent-cell-preamble-audit-v1",
        "meaning": (
            "project Z3 constraints and independently emitted SMT-LIB "
            "preambles are compared on cell witnesses and random matrices"
        ),
        "seed": seed,
        "random_matrix_count": random_count,
        "matrix_count": len(matrices),
        "cell_count": len(CELLS),
        "comparison_count": len(matrices) * len(CELLS),
        "mismatch_count": len(comparisons),
        "mismatches": comparisons[:20],
        "counts_by_cell": {
            cell: dict(sorted(counter.items()))
            for cell, counter in counts.items()
        },
        "all_equal": not comparisons,
        "witness_sha256": hashlib.sha256(
            json.dumps(witness_values, sort_keys=True).encode()
        ).hexdigest(),
        "z3_version": z3.get_version_string(),
    }
    atomic_json(output_path, document)
    print(json.dumps(document, indent=2, sort_keys=True), flush=True)
    if not document["all_equal"]:
        raise SystemExit(2)
    return document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-count", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20260729)
    args = parser.parse_args()
    run(
        output_path=args.output,
        random_count=args.random_count,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
