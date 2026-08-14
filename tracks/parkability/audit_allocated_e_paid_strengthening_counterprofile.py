#!/usr/bin/env python3
"""Exact arithmetic audit of a paid-endpoint strengthening counterprofile."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .find_generalized_pi_cycle import find_closed_core_families
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


ROOT = Path(__file__).resolve().parents[2]


def desired_common_safe(values, source, pieces):
    if sum((values[source][piece] for piece in pieces), Fraction(0)) <= 1:
        return False
    for observer in OWNERS:
        amounts = [values[observer][piece] for piece in pieces]
        if sum(amounts, Fraction(0)) - min(amounts) > 1:
            return False
    return True


def complete_efx(values, allocation):
    for observer in OWNERS:
        own = sum((values[observer][piece] for piece in allocation[observer]), Fraction(0))
        for target in OWNERS:
            if target == observer:
                continue
            pieces = allocation[target]
            target_total = sum((values[observer][piece] for piece in pieces), Fraction(0))
            if any(own < target_total - values[observer][piece] for piece in pieces):
                return False
    return True


def run(source: Path, output: Path):
    source = source.resolve()
    payload = json.loads(source.read_text())
    core_path = ROOT / payload["core_source"]
    core = json.loads(core_path.read_text())
    values = {
        owner: {piece: Fraction(amount) for piece, amount in row.items()}
        for owner, row in payload["values"].items()
    }

    solver, variables = build_master(2)
    for owner in OWNERS:
        for piece in GOODS:
            solver.add(variables[piece, owner] == z3.RealVal(str(values[owner][piece])))
    master_status = solver.check()
    assert master_status == z3.sat

    pi_clause_checks = []
    for signature in core["pi_signatures"]:
        active = [
            desired_common_safe(values, source_name, pieces)
            for source_name, pieces in signature
        ]
        pi_clause_checks.append(not all(active))
    assert all(pi_clause_checks)
    full_pi_witnesses, full_minimal = find_closed_core_families(
        values, ALLOCATED_E_BASE, maximum=1,
    )

    diagnostics = []
    qualifying = []
    maximum_holes = payload.get("maximum_payment_holes")
    required = tuple(payload.get("required_paid_owners", OWNERS))
    for index, allocation in enumerate(core["allocations"], start=1):
        is_efx = complete_efx(values, allocation)
        utilities = {
            owner: sum((values[owner][piece] for piece in allocation[owner]), Fraction(0))
            for owner in OWNERS
        }
        underpaid = tuple(owner for owner in OWNERS if utilities[owner] < 1)
        if maximum_holes is not None:
            qualifies = (
                is_efx
                and len(underpaid) <= maximum_holes
                and not (set(underpaid) & set(required))
            )
        else:
            qualifies = is_efx and not (set(underpaid) & set(required))
        if qualifies:
            qualifying.append(index)
        diagnostics.append({
            "endpoint": index,
            "is_efx": is_efx,
            "underpaid_owners": list(underpaid),
            "owner_utilities": {owner: str(amount) for owner, amount in utilities.items()},
        })
    assert any(row["is_efx"] for row in diagnostics)
    assert not qualifying

    result = {
        "schema": "allocated-e-paid-strengthening-counterprofile-audit-v1",
        "status": "COUNTERPROFILE_AUDIT_PASSED",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "core_source_sha256": hashlib.sha256(core_path.read_bytes()).hexdigest(),
        "master_fixed_profile_status": str(master_status),
        "pi_clause_count": len(pi_clause_checks),
        "all_pi_clauses_excluded_exactly": all(pi_clause_checks),
        "full_generalized_pi_found": bool(full_pi_witnesses),
        "full_generalized_pi_witness": (
            None if not full_pi_witnesses else full_pi_witnesses[0]
        ),
        "full_minimal_core_counts": {
            owner: len(rows) for owner, rows in full_minimal.items()
        },
        "maximum_payment_holes": maximum_holes,
        "required_paid_owners": list(required),
        "qualifying_endpoint_count": len(qualifying),
        "endpoint_diagnostics": diagnostics,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact Fraction audit of one minimized-core paid-endpoint shortcut "
            "counterprofile, including a full generalized-PI search. A profile "
            "with another PI does not refute a payment strengthening on the "
            "fully generalized-PI-free domain."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
