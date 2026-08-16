#!/usr/bin/env python3
"""Decide a stored rival-menu cover of the canonical Hall obstruction cell."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import integerize
    from .decide_partial_hall_designated_pair_trap import (
        SELECTED_PARTITIONS,
        designated_bundle,
    )
    from .partial_hall_factored_master import build_factored_master
    from .run_partial_hall_pareto_cegar import build_master
    from .run_partial_hall_utilitarian_cegar import (
        add_good_symmetry_breaking,
    )
    from .run_partial_hall_utilitarian_local_cegar import add_local_rivals
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import integerize
    from decide_partial_hall_designated_pair_trap import (
        SELECTED_PARTITIONS,
        designated_bundle,
    )
    from partial_hall_factored_master import build_factored_master
    from run_partial_hall_pareto_cegar import build_master
    from run_partial_hall_utilitarian_cegar import add_good_symmetry_breaking
    from run_partial_hall_utilitarian_local_cegar import add_local_rivals


def run(
    menu_path: Path,
    output: Path,
    smt2_output: Path,
    timeout_seconds: int,
    factored_hall: bool,
    hall_witness: bool,
    symmetry_close: bool,
    break_good_symmetry: bool,
    designated_trap: bool,
) -> dict:
    if factored_hall:
        solver, values, base, floater, partitions, hall_edges = build_factored_master(
            timeout_seconds * 1000,
            hall_encoding="witness" if hall_witness else "matching",
        )
    else:
        solver, values, base, floater, partitions = build_master(
            timeout_seconds * 1000
        )
        hall_edges = None
    if designated_trap:
        if hall_edges is None:
            raise ValueError("designated-trap strengthening requires factored Hall")
        traps = []
        for partition_index in SELECTED_PARTITIONS:
            bundle = designated_bundle(partitions[partition_index])
            for pair in itertools.combinations(range(4), 2):
                traps.append(
                    z3.And(
                        *(
                            hall_edges[partition_index][agent][bundle]
                            for agent in pair
                        ),
                        *(
                            z3.Not(hall_edges[partition_index][agent][other])
                            for agent in pair
                            for other in range(4)
                            if other != bundle
                        ),
                    )
                )
        solver.add(z3.Or(*traps))
    if break_good_symmetry:
        add_good_symmetry_breaking(solver, values, base)
    menu = json.loads(menu_path.read_text())
    rivals = [
        {"floater": record["floater"], "masks": tuple(record["masks"])}
        for record in menu["selected_rivals"]
    ]
    learned = set()
    add_local_rivals(
        solver,
        values,
        base,
        learned,
        rivals,
        symmetry_close=symmetry_close,
    )
    verdict = solver.check()
    if verdict == z3.sat:
        status = "SAT_UNCOVERED_HALL_OBSTRUCTION"
        model_values = integerize(solver.model(), values)
    elif verdict == z3.unsat:
        status = "UNSAT"
        model_values = None
    else:
        status = "UNKNOWN"
        model_values = None
    smt2_output.write_text(solver.to_smt2())
    artifact = {
        "schema": "partial-hall-rival-menu-gate-v1",
        "status": status,
        "meaning": (
            "UNSAT proves the selected rival menu covers every canonical Hall "
            "obstruction; SAT gives an exact uncovered valuation; UNKNOWN is "
            "inconclusive."
        ),
        "menu": str(menu_path),
        "menu_selected_rival_count": len(rivals),
        "asserted_rival_count": len(learned),
        "factored_hall": factored_hall,
        "hall_witness": hall_witness,
        "symmetry_close": symmetry_close,
        "break_good_symmetry": break_good_symmetry,
        "designated_trap": designated_trap,
        "timeout_seconds": timeout_seconds,
        "candidate_partition_count": len(partitions),
        "values": model_values,
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "solver_statistics": str(solver.statistics()),
        "smt2_output": str(smt2_output),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--menu", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2-output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--factored-hall", action="store_true")
    parser.add_argument("--hall-witness", action="store_true")
    parser.add_argument("--symmetry-close", action="store_true")
    parser.add_argument("--break-good-symmetry", action="store_true")
    parser.add_argument("--designated-trap", action="store_true")
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.menu,
                args.output,
                args.smt2_output,
                args.timeout_seconds,
                args.factored_hall,
                args.hall_witness,
                args.symmetry_close,
                args.break_good_symmetry,
                args.designated_trap,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
