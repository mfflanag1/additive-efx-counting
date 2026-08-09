#!/usr/bin/env python3
"""Audit the strict binary selected-root counterexample and unrestricted escapes."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .decide_adjacent_large_selected_root_completion import selected_bundle
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        make_cell,
        numeric_utilities,
        structural_solver,
    )
except ImportError:
    from decide_adjacent_large_selected_root_completion import selected_bundle
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        make_cell,
        numeric_utilities,
        structural_solver,
    )


SCHEMA = "adjacent-large-binary-selected-root-counterexample-audit-v1"
SIZES = (2, 2, 2, 2)
RAW_VALUES = (
    (8, 48, 56, 1697, 20, 24, 24, 48, 1813, 1797, 1761),
    (6, 226, 219, 232, 25, 209, 1, 234, 221, 1, 450),
    (24, 391, 20, 20, 1, 442, 4, 7, 458, 456, 1),
    (743, 24, 78, 1864, 899, 24, 12, 1798, 2727, 2757, 18),
)
SCALE = 4096
VALUES = tuple(
    tuple(SCALE * entry + (1 << good) for good, entry in enumerate(row))
    for row in RAW_VALUES
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subset_nondegenerate():
    for row in VALUES:
        totals = set()
        for mask in range(1 << len(row)):
            total = sum(row[good] for good in range(len(row)) if mask & (1 << good))
            if total in totals:
                return False
            totals.add(total)
    return True


def pin_structural(cell):
    solver, symbolic, _ = structural_solver(cell)
    row_sums = tuple(sum(row) for row in VALUES)
    solver.add(
        *(
            symbolic[agent][good] * row_sums[agent] == VALUES[agent][good]
            for agent in range(4)
            for good in range(cell["m"])
        )
    )
    return str(solver.check())


def allocation_solver(cell, order, fixed_root=None):
    m = cell["m"]
    owner = tuple(z3.Int(f"owner_{fixed_root}_{''.join(map(str, order))}_{good}") for good in range(m))
    solver = z3.SolverFor("QF_LIA")
    solver.add(*(z3.And(variable >= 0, variable <= 4) for variable in owner))
    utilities = tuple(
        z3.Sum(*(z3.If(owner[good] == agent, VALUES[agent][good], 0) for good in range(m)))
        for agent in range(4)
    )
    observed = tuple(
        tuple(
            z3.Sum(*(z3.If(owner[good] == target, VALUES[observer][good], 0) for good in range(m)))
            for target in range(4)
        )
        for observer in range(4)
    )
    solver.add(
        *(
            z3.Implies(
                owner[removed] == target,
                utilities[observer]
                >= observed[observer][target] - VALUES[observer][removed],
            )
            for observer in range(4)
            for target in range(4)
            for removed in range(m)
        )
    )
    base = numeric_utilities(VALUES, cell["base_owner"])
    solver.add(
        z3.Or(
            *(
                z3.And(
                    *(utilities[order[prefix]] == base[order[prefix]] for prefix in range(index)),
                    utilities[agent] > base[agent],
                )
                for index, agent in enumerate(order)
            )
        )
    )
    if fixed_root is not None:
        selected = set(selected_bundle(cell, fixed_root))
        solver.add(
            *(
                owner[good] == fixed_root
                if good in selected
                else owner[good] != fixed_root
                for good in range(m)
            )
        )
    return solver, owner, utilities


def allocation_record(cell, model, owner, utilities):
    concrete = tuple(model.eval(variable).as_long() for variable in owner)
    return {
        "allocation": {
            AGENTS[agent]: [
                cell["goods"][good]
                for good, assigned in enumerate(concrete)
                if assigned == agent
            ]
            for agent in range(4)
        },
        "charity": [
            cell["goods"][good]
            for good, assigned in enumerate(concrete)
            if assigned == 4
        ],
        "utilities": [model.eval(utility).as_long() for utility in utilities],
    }


def audit():
    cell = make_cell(SIZES)
    if not subset_nondegenerate():
        raise AssertionError("perturbed profile is not subset-nondegenerate")
    structural_status = pin_structural(cell)
    if structural_status != "sat":
        raise AssertionError(("profile outside strict adjacent cell", structural_status))

    selected_statuses = {}
    for root in (0, 1):
        order = (root,) + tuple(agent for agent in range(4) if agent != root)
        solver, _, _ = allocation_solver(cell, order, fixed_root=root)
        selected_statuses[AGENTS[root]] = str(solver.check())

    orders = []
    for order in itertools.permutations(range(4)):
        solver, owner, utilities = allocation_solver(cell, order)
        checked = solver.check()
        record = {
            "agent_order": list(order),
            "agent_order_names": [AGENTS[agent] for agent in order],
            "status": str(checked),
        }
        if checked == z3.sat:
            record["example"] = allocation_record(cell, solver.model(), owner, utilities)
        orders.append(record)

    unsat_orders = [record for record in orders if record["status"] == "unsat"]
    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": (
            "UNRESTRICTED_ADJACENT_GLOBAL_LEX_REFUTED"
            if unsat_orders
            else "SELECTED_ROOT_REFUTED_BUT_UNRESTRICTED_ESCAPE_SURVIVES"
        ),
        "packet_sizes": list(SIZES),
        "goods": list(cell["goods"]),
        "raw_values": [list(row) for row in RAW_VALUES],
        "values": [list(row) for row in VALUES],
        "perturbation": "v'[i,g] = 4096*v[i,g] + 2^g",
        "subset_nondegenerate": True,
        "base_utilities": list(numeric_utilities(VALUES, cell["base_owner"])),
        "structural_qf_lra_status": structural_status,
        "selected_root_qf_lia_statuses": selected_statuses,
        "orders": orders,
        "unsat_orders": unsat_orders,
        "claim_boundary": {
            "selected_root": "reported separately for p and r",
            "unrestricted": "an unsat priority order exactly refutes the unrestricted adjacent global-lex escape lemma in this strict subset-nondegenerate profile",
            "efx": "even an unrestricted global-lex refutation would not be a counterexample to EFX existence",
        },
        "solver": {"name": "z3", "version": z3.get_version_string()},
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
