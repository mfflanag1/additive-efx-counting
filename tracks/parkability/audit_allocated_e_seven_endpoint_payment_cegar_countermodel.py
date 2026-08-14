#!/usr/bin/env python3
"""Independent exact audit of a terminal payment-CEGAR countermodel."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .audit_allocated_e_paid_strengthening_counterprofile import complete_efx
from .find_generalized_pi_cycle import find_closed_core_families
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


ROOT = Path(__file__).resolve().parents[2]


def run(source: Path, output: Path):
    source = source.resolve()
    payload = json.loads(source.read_text())
    assert payload["status"] == "SAT_PI_FREE_NO_REQUIRED_ENDPOINT"
    endpoint_source = ROOT / payload["endpoint_source"]
    endpoints = tuple(json.loads(endpoint_source.read_text())["allocations"])
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in payload["values"].items()
    }

    solver, symbolic = build_master(2)
    for owner in OWNERS:
        for good in GOODS:
            solver.add(symbolic[good, owner] == z3.RealVal(str(values[owner][good])))
    master_status = solver.check()
    assert master_status == z3.sat

    witnesses, minimal = find_closed_core_families(
        values, ALLOCATED_E_BASE, maximum=1,
    )
    assert not witnesses

    maximum_holes = payload["maximum_payment_holes"]
    required = tuple(payload["required_paid_owners"])
    diagnostics = []
    qualifying = []
    for index, allocation in enumerate(endpoints, start=1):
        is_efx = complete_efx(values, allocation)
        utilities = {
            owner: sum(
                (values[owner][good] for good in allocation[owner]),
                Fraction(0),
            )
            for owner in OWNERS
        }
        underpaid = tuple(owner for owner in OWNERS if utilities[owner] < 1)
        qualifies = (
            is_efx
            and len(underpaid) <= maximum_holes
            and not (set(underpaid) & set(required))
        )
        if qualifies:
            qualifying.append(index)
        diagnostics.append({
            "endpoint": index,
            "is_efx": is_efx,
            "underpaid_owners": list(underpaid),
            "owner_utilities": {
                owner: str(amount) for owner, amount in utilities.items()
            },
        })
    assert any(row["is_efx"] for row in diagnostics)
    assert not qualifying

    result = {
        "schema": "allocated-e-seven-endpoint-payment-cegar-countermodel-audit-v1",
        "status": "AUDIT_PASSED",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "endpoint_source_sha256": hashlib.sha256(endpoint_source.read_bytes()).hexdigest(),
        "master_fixed_profile_status": str(master_status),
        "full_generalized_pi_found": False,
        "full_minimal_core_counts": {
            owner: len(cores) for owner, cores in minimal.items()
        },
        "maximum_payment_holes": maximum_holes,
        "required_paid_owners": list(required),
        "qualifying_endpoint_count": len(qualifying),
        "endpoint_diagnostics": diagnostics,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact positive-rational countermodel to only the declared bounded "
            "payment strengthening. Complete EFX itself is not refuted."
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
