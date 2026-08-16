#!/usr/bin/env python3
"""Extract a bounded CP-SAT core for a terminal radius-two exchange gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from .anneal import atomic_json
    from .decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .decide_distinct_half_terminal_exchange import (
        M,
        N,
        TERMINAL_MATCHING_REPRESENTATIVES,
        TERMINAL_PARTITIONS,
        target_partition_orbits,
        target_partitions,
    )
    from .decide_distinct_half_terminal_exchange_cpsat import add_matching_efx
    from .run_distinct_half_full_cell_cpsat_cegar import add_no_full_hall_cells
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from decide_distinct_half_terminal_exchange import (
        M,
        N,
        TERMINAL_MATCHING_REPRESENTATIVES,
        TERMINAL_PARTITIONS,
        target_partition_orbits,
        target_partitions,
    )
    from decide_distinct_half_terminal_exchange_cpsat import add_matching_efx
    from run_distinct_half_full_cell_cpsat_cegar import add_no_full_hall_cells


SCHEMA = "distinct-half-terminal-exchange-cpsat-core-v1"


def run(
    case,
    matching_orbit,
    cap,
    time_limit,
    workers,
    random_seed,
    output,
    proto_output,
    source_path=None,
    core_dimension="partitions",
    require_no_full_cell=True,
    target_name="radius2",
):
    terminal = TERMINAL_PARTITIONS[case]
    matching = TERMINAL_MATCHING_REPRESENTATIVES[case][matching_orbit]
    radius_targets = target_partitions(target_name, terminal)
    target_orbits = (
        target_partition_orbits(case, matching, target_name)
        if core_dimension == "target_orbits"
        else ()
    )
    if source_path is None:
        targets = radius_targets
    else:
        payload = json.loads(source_path.read_text())
        if payload.get("case", case) != case or payload.get("target", target_name) != target_name:
            raise ValueError("source core metadata does not match the requested case")
        if payload.get("terminal_matching_orbit", matching_orbit) != matching_orbit:
            raise ValueError("source core metadata has a different matching orbit")
        if core_dimension == "partitions":
            targets = tuple(
                tuple(tuple(bundle) for bundle in partition)
                for partition in payload["core_partitions"]
            )
        else:
            orbit_positions = tuple(
                record["orbit_position"]
                for record in payload["core_target_orbits"]
            )
            targets = tuple(
                partition
                for orbit_position in orbit_positions
                for partition in target_orbits[orbit_position]
            )
        if not targets or not set(targets).issubset(radius_targets):
            raise ValueError("source core is not a nonempty radius-two subset")
    universe = tuple(favorite_pair_balanced_universe())
    positions = {partition: position for position, partition in enumerate(universe)}

    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{agent}_{good}")
            for good in range(M)
        )
        for agent in range(N)
    )
    add_branch(model, values)
    cell_guards = (
        {} if core_dimension == "cells" and require_no_full_cell else None
    )
    full_cell_encoding = (
        add_no_full_hall_cells(
            model, values, cap, assumption_guards=cell_guards
        )
        if require_no_full_cell
        else None
    )
    add_matching_efx(model, values, terminal, matching)

    orbit_by_partition = {
        partition: orbit_position
        for orbit_position, orbit in enumerate(target_orbits)
        for partition in orbit
    }
    orbit_guards = {}
    guards = {}
    for target in targets:
        position = positions[target]
        if core_dimension == "partitions":
            guard = model.NewBoolVar(f"target_partition_{position}")
            model.AddAssumption(guard)
            guards[guard.Index()] = target
        elif core_dimension == "target_orbits":
            orbit_position = orbit_by_partition[target]
            guard = orbit_guards.get(orbit_position)
            if guard is None:
                guard = model.NewBoolVar(f"target_orbit_{orbit_position}")
                model.AddAssumption(guard)
                guards[guard.Index()] = orbit_position
                orbit_guards[orbit_position] = guard
        else:
            guard = None
        add_favorite_pair_obstruction(
            model, values, target, position, guard=guard
        )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    started = time.time()
    status_code = solver.Solve(model)
    elapsed = time.time() - started
    core = []
    if status_code == cp_model.INFEASIBLE:
        for literal in solver.SufficientAssumptionsForInfeasibility():
            source_guards = guards if core_dimension != "cells" else cell_guards
            if literal not in source_guards:
                raise AssertionError("unexpected assumption literal")
            core.append(source_guards[literal])

    proto_output.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_output)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_output.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": (
            "ASSUMPTION_CORE_EXTRACTED"
            if core
            else "CP_SAT_UNKNOWN"
            if status_code == cp_model.UNKNOWN
            else solver.StatusName(status_code)
        ),
        "solver_status": solver.StatusName(status_code),
        "case": case,
        "terminal_matching_orbit": matching_orbit,
        "terminal_matching_representative": list(matching),
        "cap": cap,
        "target": target_name,
        "target_partition_count": len(targets),
        "core_dimension": core_dimension,
        "source": str(source_path) if source_path is not None else None,
        "source_sha256": (
            hashlib.sha256(source_path.read_bytes()).hexdigest()
            if source_path is not None
            else None
        ),
        "core_size": len(core),
        "base_formula_infeasible_without_cell_obstructions": (
            core_dimension == "cells"
            and status_code == cp_model.INFEASIBLE
            and not core
        ),
        "core_partitions": (
            [[list(bundle) for bundle in partition] for partition in core]
            if core_dimension == "partitions"
            else None
        ),
        "target_orbit_count": len(target_orbits) if target_orbits else None,
        "active_target_orbit_count": (
            len({orbit_by_partition[target] for target in targets})
            if target_orbits
            else None
        ),
        "core_target_orbits": (
            [
                {
                    "orbit_position": orbit_position,
                    "size": len(target_orbits[orbit_position]),
                    "representative": [
                        list(bundle) for bundle in min(target_orbits[orbit_position])
                    ],
                }
                for orbit_position in core
            ]
            if core_dimension == "target_orbits"
            else None
        ),
        "core_low_pairs": (
            [list(lows) for lows in core]
            if core_dimension == "cells"
            else None
        ),
        "full_hall_cell_forbidden": require_no_full_cell,
        "full_hall_cell_constraints_present": require_no_full_cell,
        "full_cell_encoding": full_cell_encoding,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "workers": workers,
        "random_seed": random_seed,
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "proto_path": str(proto_output),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "warning": (
            "The returned core is sufficient, not necessarily minimal, and "
            "proves only the stated finite-cap terminal implication."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(TERMINAL_PARTITIONS), required=True)
    parser.add_argument("--matching-orbit", type=int, required=True)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument(
        "--core-dimension",
        choices=("partitions", "target_orbits", "cells"),
        default="partitions",
    )
    parser.add_argument("--allow-full-hall-cell", action="store_true")
    parser.add_argument(
        "--target",
        choices=(
            "radius2",
            "radius2_same_favorite",
            "radius2_new_favorite_partner",
            "radius2_triple_partner",
            "same_favorite",
        ),
        default="radius2",
    )
    args = parser.parse_args()
    if (
        args.cap < 2
        or args.time_limit <= 0
        or args.workers < 1
        or not 0
        <= args.matching_orbit
        < len(TERMINAL_MATCHING_REPRESENTATIVES[args.case])
        or (args.core_dimension == "cells" and args.allow_full_hall_cell)
        or (args.core_dimension == "cells" and args.source is not None)
    ):
        parser.error("invalid core-extraction parameters")
    result = run(
        args.case,
        args.matching_orbit,
        args.cap,
        args.time_limit,
        args.workers,
        args.random_seed,
        args.output,
        args.proto,
        args.source,
        args.core_dimension,
        not args.allow_full_hall_cell,
        args.target,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
