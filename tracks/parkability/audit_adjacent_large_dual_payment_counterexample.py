#!/usr/bin/env python3
"""Audit the binary counterexample to the mirrored-payment dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .analyze_adjacent_large_packet_flow import (
        AGENTS,
        desired_sources,
        profile_analysis,
    )
except ImportError:
    from analyze_adjacent_large_packet_flow import (
        AGENTS,
        desired_sources,
        profile_analysis,
    )
try:
    from .run_adjacent_large_unrestricted_owner_cegar import fixed_owner_solver
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        make_cell,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )
except ImportError:
    from run_adjacent_large_unrestricted_owner_cegar import fixed_owner_solver
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        make_cell,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )


SCHEMA = "adjacent-large-dual-payment-counterexample-audit-v1"
SIZES = (2, 2, 2, 2)
RAW_VALUES = (
    (8, 9, 114, 115, 3, 12, 2, 3, 263, 262, 247),
    (260, 792, 961, 1078, 1065, 39, 1104, 39, 3078, 3078, 2000),
    (14, 6, 6, 20, 6, 4, 28, 8, 889, 47, 10),
    (3, 1, 16, 16, 24, 4, 7, 4, 38, 920, 5),
)
SCALE = 4096
VALUES = tuple(
    tuple(SCALE * entry + (1 << good) for good, entry in enumerate(row))
    for row in RAW_VALUES
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_subset_nondegenerate(values) -> bool:
    for row in values:
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


def concrete_owner(model, owner):
    return tuple(
        None if model.eval(variable).as_long() == 4 else model.eval(variable).as_long()
        for variable in owner
    )


def named_allocation(cell, owner):
    return {
        "allocation": {
            AGENTS[agent]: [
                cell["goods"][good]
                for good, assigned in enumerate(owner)
                if assigned == agent
            ]
            for agent in range(4)
        },
        "charity": [
            cell["goods"][good]
            for good, assigned in enumerate(owner)
            if assigned is None
        ],
    }


def minimum_change_escape(cell, order, values=VALUES):
    base_destination = tuple(4 if owner is None else owner for owner in cell["base_owner"])
    for changed in range(1, cell["m"] + 1):
        solver, owner, utilities = fixed_owner_solver(values, cell, order)
        solver.add(
            z3.Sum(
                *(z3.If(variable == destination, 0, 1) for variable, destination in zip(owner, base_destination))
            )
            <= changed
        )
        if solver.check() != z3.sat:
            continue
        concrete = concrete_owner(solver.model(), owner)
        if not numeric_efx(values, concrete):
            raise AssertionError("SMT escape fails direct EFX replay")
        base = numeric_utilities(values, cell["base_owner"])
        rival = numeric_utilities(values, concrete)
        if tuple(rival[agent] for agent in order) <= tuple(base[agent] for agent in order):
            raise AssertionError("SMT escape fails direct lex replay")
        bundles = tuple(
            tuple(good for good, assigned in enumerate(concrete) if assigned == agent)
            for agent in range(4)
        )
        return {
            "changed_good_count": changed,
            **named_allocation(cell, concrete),
            "utilities": list(rival),
            "bundle_desired_sources_at_base": {
                AGENTS[agent]: [
                    AGENTS[source]
                    for source in desired_sources(values, base, bundles[agent])
                ]
                for agent in range(4)
            },
        }
    return None


def audit():
    cell = make_cell(SIZES)
    if not is_subset_nondegenerate(VALUES):
        raise AssertionError("perturbed profile is not subset-nondegenerate")
    structural_status = pin_structural(cell)
    if structural_status != "sat":
        raise AssertionError(("profile outside strict adjacent cell", structural_status))
    flow = profile_analysis(VALUES, cell)
    if flow["direct_p_payment_count"] or flow["direct_r_payment_count"]:
        raise AssertionError("perturbed profile no longer refutes the dual-payment gate")

    order_records = []
    for order in itertools.permutations(range(4)):
        example = minimum_change_escape(cell, order)
        order_records.append(
            {
                "agent_order": list(order),
                "agent_order_names": [AGENTS[agent] for agent in order],
                "status": "sat" if example else "unsat",
                "minimum_change_escape": example,
            }
        )
    unsat_orders = [record for record in order_records if record["status"] == "unsat"]
    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": (
            "UNRESTRICTED_ADJACENT_GLOBAL_LEX_REFUTED"
            if unsat_orders
            else "DUAL_PAYMENT_REFUTED_BUT_UNRESTRICTED_ESCAPE_SURVIVES"
        ),
        "packet_sizes": list(SIZES),
        "goods": list(cell["goods"]),
        "raw_values": [list(row) for row in RAW_VALUES],
        "values": [list(row) for row in VALUES],
        "perturbation": "v'[i,g] = 4096*v[i,g] + 2^g",
        "subset_nondegenerate": True,
        "structural_qf_lra_status": structural_status,
        "packet_flow": flow,
        "orders": order_records,
        "unsat_orders": unsat_orders,
        "claim_boundary": {
            "refuted": "the mirrored direct-payment dichotomy in the full binary adjacent-large cell",
            "not_refuted": "the unrestricted adjacent-large escape lemma or complete EFX existence",
        },
        "solver": {"name": "z3", "version": z3.get_version_string()},
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print(
        json.dumps(
            {
                "minimum_change_histogram": dict(
                    sorted(
                        __import__("collections").Counter(
                            record["minimum_change_escape"]["changed_good_count"]
                            for record in result["orders"]
                        ).items()
                    )
                ),
                "unsat_order_count": len(result["unsat_orders"]),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
