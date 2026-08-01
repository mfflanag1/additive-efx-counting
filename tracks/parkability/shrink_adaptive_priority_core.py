#!/usr/bin/env python3
"""Extract a deletion-minimal rival core from an adaptive-priority cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster
    from .normalize_smt2_for_cvc5 import atomic_write
    from .run_adaptive_priority_cegar import (
        Cell,
        derive_unique_seed_cells,
        load_pool,
    )
    from .run_lexmax_partial_cegar import (
        add_candidate,
        add_rival_blocker,
        bundles_of,
        subset_sum,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster
    from normalize_smt2_for_cvc5 import atomic_write
    from run_adaptive_priority_cegar import (
        Cell,
        derive_unique_seed_cells,
        load_pool,
    )
    from run_lexmax_partial_cegar import (
        add_candidate,
        add_rival_blocker,
        bundles_of,
        subset_sum,
    )


SCHEMA = "adaptive-priority-rival-core-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_master(
    n: int,
    m: int,
    cells: list[Cell],
    *,
    require_distinct_item_values: bool,
    activate_candidates: bool = False,
) -> tuple[
    ParkabilityLRAMaster,
    list[tuple[int, tuple[int | None, ...]]],
    dict[tuple[int, tuple[int | None, ...]], tuple[z3.ArithRef, ...]],
    list[z3.BoolRef],
]:
    unique_candidates = list(dict.fromkeys(candidate for _, candidate in cells))
    master = ParkabilityLRAMaster(
        n,
        m,
        require_distinct_item_values=require_distinct_item_values,
    )
    selectors = [
        z3.Bool(f"active_candidate_{index}")
        for index in range(len(unique_candidates))
    ] if activate_candidates else []
    utilities = {
        candidate: add_candidate(
            master,
            *candidate,
            activation=(
                selectors[index]
                if activate_candidates
                else None
            ),
        )
        for index, candidate in enumerate(unique_candidates)
    }
    return master, unique_candidates, utilities, selectors


def run(
    *,
    seed_path: Path,
    pool_path: Path,
    output_path: Path,
    smt2_path: Path,
    time_limit_s: float,
    require_distinct_item_values: bool,
    shrink_candidates: bool,
    preserve_rival_dependencies: bool,
) -> dict:
    if (
        output_path.exists()
        or smt2_path.exists()
        or time_limit_s <= 0
        or (preserve_rival_dependencies and not shrink_candidates)
    ):
        raise ValueError(
            "new outputs, a positive time limit, and candidate shrinking "
            "for dependency preservation are required"
        )
    raw_seed = json.loads(seed_path.read_text())
    raw_values = raw_seed.get("values", raw_seed.get("candidate_values"))
    if raw_values is None:
        raise ValueError("seed JSON contains no values")
    seed_values = core.validate_values(raw_values, lower=1)
    n = len(seed_values)
    m = len(seed_values[0])
    cells = derive_unique_seed_cells(seed_values)
    rivals_by_order = load_pool(pool_path, n, m, cells)

    master, unique_candidates, utilities, candidate_selectors = build_master(
        n,
        m,
        cells,
        require_distinct_item_values=require_distinct_item_values,
        activate_candidates=shrink_candidates,
    )
    records = [
        {
            "kind": "candidate",
            "candidate_index": index,
            "candidate": {
                "floater": candidate[0],
                "base_owner": list(candidate[1]),
            },
        }
        for index, candidate in enumerate(unique_candidates)
    ] if shrink_candidates else []
    selectors = candidate_selectors[:]
    for cell_index, (order, candidate) in enumerate(cells):
        for rival_index, rival in enumerate(rivals_by_order[order]):
            selector = z3.Bool(
                f"active_cell_{cell_index}_rival_{rival_index}"
            )
            add_rival_blocker(
                master,
                utilities[candidate],
                candidate[1],
                rival,
                order,
                "exact",
                activation=selector,
            )
            if preserve_rival_dependencies:
                master.solver.add(
                    z3.Implies(
                        selector,
                        candidate_selectors[
                            unique_candidates.index(candidate)
                        ],
                    )
                )
            selectors.append(selector)
            records.append(
                {
                    "kind": "rival",
                    "cell_index": cell_index,
                    "agent_order": list(order),
                    "candidate_index": unique_candidates.index(candidate),
                    "rival": {
                        "floater": rival[0],
                        "base_owner": list(rival[1]),
                    },
                }
            )

    master.solver.set(timeout=round(time_limit_s * 1000))
    started = time.time()
    first = master.solver.check(*selectors)
    if first != z3.unsat:
        raise RuntimeError(
            f"full rival pool is not UNSAT: {first} "
            f"{master.solver.reason_unknown()}"
        )
    by_name = {
        selector.decl().name(): index
        for index, selector in enumerate(selectors)
    }
    initial_core = [
        by_name[item.decl().name()]
        for item in master.solver.unsat_core()
    ]
    active = initial_core[:]
    checks = 1
    for index in initial_core:
        trial = [other for other in active if other != index]
        verdict = master.solver.check(*(selectors[other] for other in trial))
        checks += 1
        if verdict == z3.unsat:
            active = trial
        elif verdict != z3.sat:
            raise RuntimeError(
                f"core-shrinking check is {verdict}: "
                f"{master.solver.reason_unknown()}"
            )

    active_set = set(active)
    necessity = []
    for index in active:
        trial = [other for other in active if other != index]
        verdict = master.solver.check(*(selectors[other] for other in trial))
        checks += 1
        necessity.append(
            {
                "pool_index": index,
                "status_without": str(verdict),
            }
        )
        if verdict != z3.sat:
            raise AssertionError("reported core is not deletion-minimal")
    explicitly_active_candidate_indices = (
        {
            records[index]["candidate_index"]
            for index in active
            if records[index]["kind"] == "candidate"
        }
        if shrink_candidates
        else set(range(len(unique_candidates)))
    )
    dependency_candidate_indices = (
        {
            records[index]["candidate_index"]
            for index in active
            if records[index]["kind"] == "rival"
        }
        if preserve_rival_dependencies
        else set()
    )
    active_candidate_indices = (
        explicitly_active_candidate_indices | dependency_candidate_indices
    )
    frozen = ParkabilityLRAMaster(
        n,
        m,
        require_distinct_item_values=require_distinct_item_values,
    )
    frozen_utilities = {}
    for candidate_index, candidate in enumerate(unique_candidates):
        if candidate_index in active_candidate_indices:
            frozen_utilities[candidate] = add_candidate(frozen, *candidate)
        else:
            bundles = bundles_of(candidate[1], n)
            frozen_utilities[candidate] = tuple(
                subset_sum(frozen, observer, bundles[observer])
                for observer in range(n)
            )
    for index in active:
        record = records[index]
        if record["kind"] != "rival":
            continue
        order, candidate = cells[record["cell_index"]]
        rival_record = record["rival"]
        add_rival_blocker(
            frozen,
            frozen_utilities[candidate],
            candidate[1],
            (
                rival_record["floater"],
                tuple(rival_record["base_owner"]),
            ),
            order,
            "exact",
        )
    final = frozen.solve(time_limit_s=time_limit_s)
    if final.status != "UNSAT":
        raise AssertionError("frozen deletion-minimal assumption core is not UNSAT")
    atomic_write(smt2_path, frozen.to_smt2().encode())
    result = {
        "schema": SCHEMA,
        "status": "UNSAT_DELETION_MINIMAL_RIVAL_CORE",
        "meaning": (
            "the fixed candidate identities cannot all be strict blocked "
            "lexicographic maxima for their 24 seed-derived orders; this "
            "does not prove the adaptive-priority conjecture"
        ),
        "n": n,
        "m": m,
        "seed_path": str(seed_path.resolve()),
        "seed_sha256": sha256(seed_path),
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": sha256(pool_path),
        "require_distinct_item_values": require_distinct_item_values,
        "shrink_candidates": shrink_candidates,
        "preserve_rival_dependencies": preserve_rival_dependencies,
        "candidate_count": len(unique_candidates),
        "cell_count": len(cells),
        "initial_rival_count": sum(
            record["kind"] == "rival"
            for record in records
        ),
        "initial_assumption_count": len(selectors),
        "solver_unsat_core_count": len(initial_core),
        "deletion_minimal_assumption_count": len(active),
        "deletion_minimal_candidate_count": sum(
            records[index]["kind"] == "candidate"
            for index in active
        ),
        "dependency_closed_candidate_count": len(active_candidate_indices),
        "dependency_candidate_indices": sorted(dependency_candidate_indices),
        "deletion_minimal_rival_count": sum(
            records[index]["kind"] == "rival"
            for index in active
        ),
        "solver_checks": checks,
        "elapsed_seconds": time.time() - started,
        "core": [
            {
                "pool_index": index,
                **records[index],
            }
            for index in active
        ],
        "necessity_replay": necessity,
        "discarded_assumption_count": len(selectors) - len(active_set),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": sha256(smt2_path),
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--require-distinct-item-values", action="store_true")
    parser.add_argument("--shrink-candidates", action="store_true")
    parser.add_argument("--preserve-rival-dependencies", action="store_true")
    args = parser.parse_args()
    result = run(
        seed_path=args.seed,
        pool_path=args.pool,
        output_path=args.output,
        smt2_path=args.smt2,
        time_limit_s=args.time_limit,
        require_distinct_item_values=args.require_distinct_item_values,
        shrink_candidates=args.shrink_candidates,
        preserve_rival_dependencies=args.preserve_rival_dependencies,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
