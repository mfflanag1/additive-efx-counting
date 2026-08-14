#!/usr/bin/env python3
"""Named-core audit of the bounded anchor/charity bypass contradiction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from .run_allocated_e_form0_role_split_pi_cegar import (
    OWNERS,
    PACKET,
    RESPONSE_CORE,
    SUPPORT,
    base_response,
    build_master,
    complete_efx_formula,
    total,
)


def _components(value, present):
    anchor = set(RESPONSE_CORE["r"])
    rotated = {owner: set(SUPPORT[owner]) for owner in OWNERS}
    rotated["q"] -= anchor
    rotated["r"] |= anchor
    rows = {"anchor_is_base_response": base_response(
        value, "r", RESPONSE_CORE["r"], present
    )}
    for observer in OWNERS:
        rows[f"p_parked_for_{observer}"] = (
            total(value, observer, PACKET["P"])
            <= total(value, observer, rotated[observer])
        )
    allocations = {}
    for holder in OWNERS:
        allocation = {owner: tuple(rotated[owner]) for owner in OWNERS}
        allocation[holder] = (*allocation[holder], *PACKET["P"])
        allocations[holder] = allocation
        rows[f"charity_at_{holder}_not_efx"] = z3.Not(
            complete_efx_formula(value, present, allocation)
        )
    return rotated, allocations, rows


def _check(labels):
    solver, value, present = build_master()
    _, _, rows = _components(value, present)
    for label in labels:
        solver.add(rows[label])
    solver.set(timeout=60_000)
    return str(solver.check())


def run(output: Path):
    solver, value, present = build_master()
    rotated, allocations, rows = _components(value, present)
    assumptions = {label: z3.Bool(f"bypass_assume_{index}")
                   for index, label in enumerate(rows)}
    for label, formula in rows.items():
        solver.add(z3.Implies(assumptions[label], formula))
    solver.set(timeout=60_000)
    status = str(solver.check(*assumptions.values()))
    assert status == "unsat"
    raw_core = [
        label for label, literal in assumptions.items()
        if literal in set(solver.unsat_core())
    ]

    # Deletion-minimize independently by rebuilding from the original master.
    core = list(raw_core)
    for label in list(core):
        trial = [candidate for candidate in core if candidate != label]
        if _check(trial) == "unsat":
            core = trial
    assert _check(core) == "unsat"
    for label in core:
        assert _check([candidate for candidate in core if candidate != label]) == "sat"

    groups = {
        "base_anchor_only": _check(["anchor_is_base_response"]),
        "parked_only": _check([
            label for label in rows if label.startswith("p_parked_for_")
        ]),
        "endpoint_failures_only": _check([
            label for label in rows if label.endswith("_not_efx")
        ]),
        "base_anchor_and_parked": _check([
            label for label in rows
            if label == "anchor_is_base_response" or label.startswith("p_parked_for_")
        ]),
        "base_anchor_and_endpoint_failures": _check([
            label for label in rows
            if label == "anchor_is_base_response" or label.endswith("_not_efx")
        ]),
        "parked_and_endpoint_failures": _check([
            label for label in rows
            if label.startswith("p_parked_for_") or label.endswith("_not_efx")
        ]),
    }

    # Extract a formula-level core for the surprising one-row contradiction
    # p <= q's post-anchor residual.  This rebuild shares no assumptions with
    # the named optional-component core above.
    core_master, core_value, core_present = build_master()
    core_rotated, _, _ = _components(core_value, core_present)
    master_assertions = list(core_master.assertions())
    parked_q = (
        total(core_value, "q", PACKET["P"])
        <= total(core_value, "q", core_rotated["q"])
    )
    formula_solver = z3.SolverFor("QF_LRA")
    formula_literals = [z3.Bool(f"master_formula_{index}")
                        for index in range(len(master_assertions))]
    parked_literal = z3.Bool("master_formula_parked_q")
    for literal, formula in zip(formula_literals, master_assertions, strict=True):
        formula_solver.add(z3.Implies(literal, formula))
    formula_solver.add(z3.Implies(parked_literal, parked_q))
    formula_solver.set(timeout=60_000)
    all_literals = [*formula_literals, parked_literal]
    formula_status = str(formula_solver.check(*all_literals))
    assert formula_status == "unsat"
    raw_formula_core = list(formula_solver.unsat_core())

    formula_core = list(raw_formula_core)
    for literal in list(formula_core):
        trial = [
            candidate for candidate in formula_core
            if not z3.eq(candidate, literal)
        ]
        if formula_solver.check(*trial) == z3.unsat:
            formula_core = trial
    assert formula_solver.check(*formula_core) == z3.unsat
    formula_rows = []
    for literal in formula_core:
        if z3.eq(literal, parked_literal):
            formula_rows.append({"label": "p_parked_for_q", "formula": str(parked_q)})
        else:
            index = int(literal.decl().name().removeprefix("master_formula_"))
            formula_rows.append({
                "label": f"master_assertion_{index}",
                "formula": str(master_assertions[index]),
            })

    result = {
        "schema": "allocated-e-form0-anchor-charity-bypass-audit-v1",
        "status": "UNSAT_ANCHOR_CHARITY_PARKED_BYPASS",
        "full_status": status,
        "raw_unsat_core": raw_core,
        "deletion_minimal_unsat_core": core,
        "deletion_minimal_core_size": len(core),
        "group_statuses": groups,
        "formula_level_status": formula_status,
        "formula_level_raw_core_size": len(raw_formula_core),
        "formula_level_deletion_minimal_core": formula_rows,
        "formula_level_deletion_minimal_core_size": len(formula_rows),
        "rotated_partial": {
            owner: sorted(goods) for owner, goods in rotated.items()
        },
        "charity_holders_tested": list(allocations),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact UNSAT only in the optional 21-role allocated-E form0 "
            "necessary-premise cell. It is not a cap-free normalization-"
            "bypass theorem and does not prove fixed-U or general EFX."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
