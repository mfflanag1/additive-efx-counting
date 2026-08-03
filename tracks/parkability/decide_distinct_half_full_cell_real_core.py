#!/usr/bin/env python3
"""Test a finite favorite-pair obstruction core over positive reals."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_hall_layers import add_branch
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .lra_master import ParkabilityLRAMaster
    from .run_universal_threshold_balanced_cegar import sorted_descending
    from .run_distinct_half_full_cell_cegar import (
        add_all_cells_singleton_failure,
        add_no_singleton_failure_cell,
        add_no_full_hall_cell,
        add_singleton_failure_cells,
        full_hall_cells,
        singleton_failure_cells,
    )
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_hall_layers import add_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from lra_master import ParkabilityLRAMaster
    from run_universal_threshold_balanced_cegar import sorted_descending
    from run_distinct_half_full_cell_cegar import (
        add_all_cells_singleton_failure,
        add_no_singleton_failure_cell,
        add_no_full_hall_cell,
        add_singleton_failure_cells,
        full_hall_cells,
        singleton_failure_cells,
    )
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-full-cell-real-core-result-v1"
N = 4
M = 9
FAVORITE = 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_partitions(payload):
    return tuple(
        tuple(tuple(bundle) for bundle in partition)
        for partition in payload["core_partitions"]
    )


def add_rank_cell(master, rank_branch):
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    for agent in range(N):
        master.solver.add(
            2 * master.values[agent][agent + 1]
            > master.values[agent][FAVORITE]
        )
        ordered = sorted_descending(master.values[agent][1:])
        favorite = master.values[agent][FAVORITE]
        master.solver.add(
            ordered[4] + ordered[5] + ordered[6] > favorite,
            (
                ordered[2] + ordered[6] > favorite
                if rank_branch[agent] == "B"
                else ordered[3] + ordered[4] > favorite
            ),
        )


def run(
    result_path: Path,
    smt2_path: Path,
    source_path: Path,
    time_limit: float,
    fixed_values_path: Path | None,
    rank_branch: str | None,
    threshold_encoding: str,
    cell_obstruction: str,
):
    source = json.loads(source_path.read_text())
    partitions = decode_partitions(source)
    universe = tuple(favorite_pair_balanced_universe())
    if (
        len(partitions) != len(set(partitions))
        or not set(partitions) <= set(universe)
    ):
        raise ValueError("source does not contain a valid favorite-pair core")

    fixed_values = None
    if fixed_values_path is not None:
        fixed_payload = json.loads(fixed_values_path.read_text())
        fixed_values = fixed_payload.get(
            "real_canonical_values",
            fixed_payload.get("values", fixed_payload),
        )
        audit_branch(fixed_values)

    master = ParkabilityLRAMaster(N, M, fixed_values=fixed_values)
    if rank_branch is None:
        add_branch(master, None, threshold_encoding=threshold_encoding)
    else:
        add_rank_cell(master, rank_branch)
    if cell_obstruction != "rr_nonsingleton_12":
        for agent in range(N - 1):
            master.solver.add(
                master.values[agent][FAVORITE]
                >= master.values[agent + 1][FAVORITE]
            )
    for good in range(5, M - 1):
        master.solver.add(master.values[0][good] >= master.values[0][good + 1])
    if cell_obstruction == "full_hall":
        full_cell_encoding = add_no_full_hall_cell(master)
    elif cell_obstruction == "singleton":
        full_cell_encoding = add_all_cells_singleton_failure(master)
    elif cell_obstruction == "rr_singleton":
        full_cell_encoding = {
            "full_hall": add_no_full_hall_cell(master),
            "rr_singleton": add_singleton_failure_cells(
                master, itertools.combinations(range(1, 5), 2)
            ),
        }
    else:
        full_cell_encoding = {
            "full_hall": add_no_full_hall_cell(master),
            "rr_nonsingleton_12": add_no_singleton_failure_cell(
                master, (1, 2)
            ),
        }
    for partition in partitions:
        master.add_partition_obstruction(partition)

    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)

    values = solved.values
    favorite_pair_repairs = ()
    if values is not None:
        audit_branch(values)
        if full_hall_cells(values):
            raise AssertionError("decoded model violates no-full-cell formula")
        if (
            cell_obstruction == "singleton"
            and len(singleton_failure_cells(values)) != 28
        ):
            raise AssertionError("decoded model lost a singleton cell witness")
        singleton_cells = {tuple(cell) for cell in singleton_failure_cells(values)}
        rr_cells = set(itertools.combinations(range(1, 5), 2))
        if cell_obstruction == "rr_singleton" and not rr_cells <= singleton_cells:
            raise AssertionError("decoded model lost an RR singleton witness")
        if (
            cell_obstruction == "rr_nonsingleton_12"
            and (1, 2) in singleton_cells
        ):
            raise AssertionError("decoded model gained the forbidden witness")
        if supported_partitions(values, list(partitions)):
            raise AssertionError("decoded model repairs a core partition")
        favorite_pair_repairs = supported_partitions(values, list(universe))

    result = {
        "schema": SCHEMA,
        "status": (
            "UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "SAT_REAL_CORE_ESCAPE"
            if solved.status == "SAT"
            else "MASTER_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "solver": "Z3",
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "fixed_values": (
            {
                "path": str(fixed_values_path),
                "sha256": sha256(fixed_values_path),
            }
            if fixed_values_path is not None
            else None
        ),
        "core_size": len(partitions),
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "universal_threshold_encoding": (
            threshold_encoding
            if rank_branch is None
            else "direct rank-cell sorting"
        ),
        "rank_disjunct_branch": rank_branch,
        "full_hall_cell_forbidden": True,
        "cell_obstruction": cell_obstruction,
        "full_cell_encoding": full_cell_encoding,
        "symmetry_breaking": [
            (
                "none on agents after fixing the nonsingleton RR cell"
                if cell_obstruction == "rr_nonsingleton_12"
                else "nonincreasing favorite values by agent"
            ),
            "nonincreasing agent-0 values on goods 5..8",
        ],
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "values": [list(row) for row in values] if values is not None else None,
        "favorite_pair_repair_count": len(favorite_pair_repairs),
        "favorite_pair_repair_sample": [
            [list(bundle) for bundle in partition]
            for partition in favorite_pair_repairs[:20]
        ],
        "literal_complete_efx_count": (
            independent.count_complete_efx0(values)
            if values is not None
            else None
        ),
        "smt2_path": str(smt2_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "SAT shows that the selected partition pool and cell obstruction "
            "do not close the positive-real branch. UNSAT would establish "
            "only the pool-relative implication and would still require "
            "independent replay."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--fixed-values", type=Path)
    parser.add_argument("--rank-branch")
    parser.add_argument(
        "--threshold-encoding",
        choices=("sorting", "cardinal"),
        default="sorting",
    )
    parser.add_argument(
        "--cell-obstruction",
        choices=(
            "full_hall",
            "singleton",
            "rr_singleton",
            "rr_nonsingleton_12",
        ),
        default="full_hall",
    )
    parser.add_argument("--time-limit", type=float, default=600)
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    if args.rank_branch is not None and (
        len(args.rank_branch) != N or set(args.rank_branch) - {"B", "C"}
    ):
        parser.error("rank branch must be a four-character B/C string")
    result = run(
        args.result,
        args.smt2,
        args.source,
        args.time_limit,
        args.fixed_values,
        args.rank_branch,
        args.threshold_encoding,
        args.cell_obstruction,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
