#!/usr/bin/env python3
"""Find unrestricted Pareto-EFX handoffs for selected frozen profiles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

from analyze_alternating_singleton_return_models import (
    AGENTS,
    SIZES,
    make_cell,
    numeric_efx,
    numeric_utilities,
)
from audit_adaptive_order_frozen_handoffs import load_profiles


SCHEMA = "alternating-adaptive-order-unrestricted-pareto-handoff-v1"


def encode_number(value):
    return int(value) if value.denominator == 1 else str(value)


def solve_profile(label, values, cell, timeout_seconds):
    m = cell["m"]
    owners = tuple(z3.Int(f"owner_{label}_{good}") for good in range(m))
    solver = z3.SolverFor("QF_LIA")
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(*(z3.And(owner >= -1, owner < len(AGENTS)) for owner in owners))
    utilities = tuple(
        z3.Sum(
            *(z3.If(owners[good] == agent, int(values[agent][good]), 0) for good in range(m))
        )
        for agent in range(len(AGENTS))
    )
    base = numeric_utilities(values, cell["base_owner"])
    solver.add(*(utilities[agent] >= int(base[agent]) for agent in range(len(AGENTS))))
    solver.add(z3.Or(*(utilities[agent] > int(base[agent]) for agent in range(len(AGENTS)))))
    for observer in range(len(AGENTS)):
        for target in range(len(AGENTS)):
            for removed in range(m):
                remainder = z3.Sum(
                    *(
                        z3.If(owners[good] == target, int(values[observer][good]), 0)
                        for good in range(m)
                        if good != removed
                    )
                )
                solver.add(z3.Implies(owners[removed] == target, utilities[observer] >= remainder))
    status = solver.check()
    record = {
        "label": label,
        "solver_status": str(status),
        "base_utility": [encode_number(entry) for entry in base],
    }
    if status == z3.sat:
        changed = z3.Sum(
            *(
                z3.If(
                    owners[good]
                    == (-1 if cell["base_owner"][good] is None else cell["base_owner"][good]),
                    0,
                    1,
                )
                for good in range(m)
            )
        )
        minimum_changed = None
        model = solver.model()
        for limit in range(1, m + 1):
            solver.push()
            solver.add(changed <= limit)
            bounded_status = solver.check()
            if bounded_status == z3.sat:
                minimum_changed = limit
                model = solver.model()
                solver.pop()
                break
            solver.pop()
            if bounded_status == z3.unknown:
                break
        owner = tuple(model.eval(entry).as_long() for entry in owners)
        owner = tuple(None if entry == -1 else entry for entry in owner)
        utility = numeric_utilities(values, owner)
        if not numeric_efx(values, owner):
            raise AssertionError("reported witness is not EFX")
        if not all(right >= left for left, right in zip(base, utility)) or utility == base:
            raise AssertionError("reported witness is not a Pareto improvement")
        record.update(
            {
                "status": "SAT_PARETO_EFX_HANDOFF",
                "owner": list(owner),
                "bundles": {
                    AGENTS[agent]: [
                        cell["goods"][good]
                        for good, assigned in enumerate(owner)
                        if assigned == agent
                    ]
                    for agent in range(len(AGENTS))
                },
                "utility": [encode_number(entry) for entry in utility],
                "delta": [encode_number(right - left) for left, right in zip(base, utility)],
                "minimum_changed_goods": minimum_changed,
            }
        )
    elif status == z3.unsat:
        record["status"] = "UNSAT_BASE_IS_PARETO_MAXIMAL_EFX"
    else:
        record.update({"status": "UNKNOWN", "reason_unknown": solver.reason_unknown()})
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", default="8,9")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    wanted = {f"cegar_iteration_{int(part)}" for part in args.iterations.split(",")}
    repo = Path(__file__).resolve().parents[2]
    cell = make_cell(SIZES)
    records = [
        solve_profile(label, values, cell, args.timeout_seconds)
        for label, values in load_profiles(repo / "results")
        if label in wanted
    ]
    if {record["label"] for record in records} != wanted:
        raise ValueError("requested profile was not found")
    payload = {
        "schema": SCHEMA,
        "status": "EXACT_UNRESTRICTED_PARETO_HANDOFF_AUDIT",
        "claim_boundary": (
            "Each SAT witness is directly replayable; an UNSAT result would establish "
            "Pareto maximality only for its frozen valuation profile."
        ),
        "profiles": records,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LIA"},
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
