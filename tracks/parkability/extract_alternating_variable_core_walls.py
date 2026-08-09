#!/usr/bin/env python3
"""Extract possible EFX failure walls from a variable-packet rooted core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3

try:
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        bundles,
        lex_gt,
        make_cell,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        bundles,
        lex_gt,
        make_cell,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-variable-core-walls-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract(core_path: Path) -> dict:
    core_data = json.loads(core_path.read_text())
    sizes = tuple(core_data["packet_sizes"])
    order = tuple(core_data["agent_order"])
    cell = make_cell(sizes)
    rivals = [tuple(record["owner_by_good"]) for record in core_data["rivals"]]
    choices = []
    rival_records = []
    for rival_index, owner in enumerate(rivals):
        solver, values, base_own = structural_solver(cell)
        assigned = bundles(owner)
        rival_own = tuple(
            subset_sum(values, agent, assigned[agent]) for agent in range(4)
        )
        lex = lex_gt(rival_own, base_own, order)
        solver.push()
        solver.add(z3.Not(lex))
        lex_status = str(solver.check())
        solver.pop()
        possible = []
        for observer in range(4):
            for target in range(4):
                for removed in assigned[target]:
                    remainder = tuple(
                        good for good in assigned[target] if good != removed
                    )
                    failure = rival_own[observer] < subset_sum(
                        values, observer, remainder
                    )
                    solver.push()
                    solver.add(failure)
                    status = str(solver.check())
                    solver.pop()
                    if status == "sat":
                        label = (
                            f"{AGENTS[observer]}!>{AGENTS[target]}-"
                            f"{cell['goods'][removed]}"
                        )
                        possible.append((label, failure))
                    elif status != "unsat":
                        raise AssertionError((rival_index, observer, target, removed, status))
        if lex_status == "sat":
            possible.append(("not_lex", z3.Not(lex)))
        elif lex_status != "unsat":
            raise AssertionError((rival_index, "lex", lex_status))
        choices.append(possible)
        rival_records.append(
            {
                "index": rival_index + 1,
                "allocation": {
                    AGENTS[agent]: [cell["goods"][good] for good in assigned[agent]]
                    for agent in range(4)
                },
                "lex_improvement_implied": lex_status == "unsat",
                "possible_failure_walls": [label for label, _ in possible],
            }
        )

    selection_count = 0
    core_counts: Counter[tuple[str, ...]] = Counter()
    for selection in itertools.product(*choices):
        selection_count += 1
        solver, _, _ = structural_solver(cell)
        assumptions = []
        labels = {}
        for rival_index, (label, failure) in enumerate(selection):
            assumption = z3.Bool(f"selected_{rival_index}_{selection_count}")
            solver.add(z3.Implies(assumption, failure))
            assumptions.append(assumption)
            labels[str(assumption)] = f"R{rival_index + 1}:{label}"
        if solver.check(*assumptions) != z3.unsat:
            raise AssertionError(("feasible blocker selection", selection))
        core = tuple(sorted(labels[str(item)] for item in solver.unsat_core()))
        core_counts[core] += 1

    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "ALL_CORE_BLOCKER_SELECTIONS_UNSAT",
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "order": list(order),
        "order_names": [AGENTS[agent] for agent in order],
        "rivals": rival_records,
        "blocker_selection_count": selection_count,
        "failure_cores": [
            {"walls": list(core), "selection_count": count}
            for core, count in sorted(
                core_counts.items(), key=lambda item: (len(item[0]), item[0])
            )
        ],
        "claim_boundary": {
            "proved": "exact failure-wall anatomy of the recorded finite rooted core",
            "not_proved": "the rooted escape for arbitrary packet sizes",
        },
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
        },
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
            "core": str(core_path),
            "core_sha256": sha256(core_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = extract(args.core)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(
        json.dumps(
            {
                "status": result["status"],
                "blocker_selection_count": result["blocker_selection_count"],
                "failure_core_count": len(result["failure_cores"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
