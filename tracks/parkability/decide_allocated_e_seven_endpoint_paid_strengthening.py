#!/usr/bin/env python3
"""Decide whether the seven-endpoint dichotomy can require owner payment."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import (
    ALLOCATED_E_BASE,
    build_master,
    linear_base_response,
)
from .audit_allocated_e_all_allocation_unsat import collect
from .run_fixed_u_full_packet_terminal_cegar import (
    OWNERS,
    allocation_formula,
    total,
)


ROOT = Path(__file__).resolve().parents[2]


def rational(model, expression):
    return Fraction(str(model.eval(expression, model_completion=True)))


def owner_paid_endpoint(value, allocation, paid_owners=OWNERS):
    return z3.And(
        allocation_formula(allocation, value, "complete_efx"),
        *(
            total(value, owner, allocation[owner])
            >= total(value, owner, ALLOCATED_E_BASE[owner])
            for owner in paid_owners
        ),
    )


def payment_hole_bounded_endpoint(
    value, allocation, maximum_payment_holes, required_paid_owners=(),
):
    paid = [
        total(value, owner, allocation[owner])
        >= total(value, owner, ALLOCATED_E_BASE[owner])
        for owner in OWNERS
    ]
    return z3.And(
        allocation_formula(allocation, value, "complete_efx"),
        z3.Sum(*(z3.If(predicate, 1, 0) for predicate in paid))
        >= len(OWNERS) - maximum_payment_holes,
        *(
            total(value, owner, allocation[owner])
            >= total(value, owner, ALLOCATED_E_BASE[owner])
            for owner in required_paid_owners
        ),
    )


def run(core_source: Path, output: Path, timeout_seconds: int, random_seed: int,
        allow_d_payment_hole: bool = False,
        maximum_payment_holes: int | None = None,
        full_pi_source: Path | None = None,
        required_paid_owners: tuple[str, ...] = ()):
    core_source = core_source.resolve()
    core = json.loads(core_source.read_text())
    solver, value = build_master(2)
    if full_pi_source is None:
        pi_signatures = tuple(
            tuple((source, tuple(pieces)) for source, pieces in signature)
            for signature in core["pi_signatures"]
        )
        pi_source_sha256 = hashlib.sha256(core_source.read_bytes()).hexdigest()
    else:
        full_pi_source = full_pi_source.resolve()
        _, collected, _ = collect(full_pi_source)
        pi_signatures = tuple(collected)
        pi_source_sha256 = hashlib.sha256(full_pi_source.read_bytes()).hexdigest()
    for signature in pi_signatures:
        solver.add(z3.Or(*(
            z3.Not(linear_base_response(value, source, tuple(pieces)))
            for source, pieces in signature
        )))
    paid_owners = tuple(owner for owner in OWNERS if not (allow_d_payment_hole and owner == "d"))
    for allocation in core["allocations"]:
        endpoint = (
            payment_hole_bounded_endpoint(
                value,
                allocation,
                maximum_payment_holes,
                required_paid_owners,
            )
            if maximum_payment_holes is not None
            else owner_paid_endpoint(value, allocation, paid_owners)
        )
        solver.add(z3.Not(endpoint))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    started = time.monotonic()
    status = solver.check()
    result = {
        "schema": "allocated-e-seven-endpoint-paid-strengthening-v1",
        "status": (
            "UNSAT_PI_OR_REQUIRED_PAID_SEVEN_ENDPOINT_EFX" if status == z3.unsat
            else "SAT_NO_PI_OR_REQUIRED_PAID_SEVEN_ENDPOINT_EFX" if status == z3.sat
            else "UNKNOWN"
        ),
        "solver_status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "pi_clause_count": len(pi_signatures),
        "full_pi_source": (
            None if full_pi_source is None else str(full_pi_source.relative_to(ROOT))
        ),
        "pi_source_sha256": pi_source_sha256,
        "endpoint_count": len(core["allocations"]),
        "required_paid_owners": list(
            required_paid_owners
            if maximum_payment_holes is not None
            else paid_owners
        ),
        "allow_d_payment_hole": allow_d_payment_hole,
        "maximum_payment_holes": maximum_payment_holes,
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "elapsed_seconds": time.monotonic() - started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact twelve-atom allocated-E form-2 decision for the recorded "
            "required-paid owner set. UNSAT strengthens the bounded dichotomy "
            "to such an EFX endpoint; SAT refutes only that strengthening, "
            "not complete EFX."
        ),
    }
    if status == z3.sat:
        model = solver.model()
        result["values"] = {
            owner: {
                good: str(rational(model, value[good, owner]))
                for good in ALLOCATED_E_BASE["r"] + ALLOCATED_E_BASE["q"]
                + ALLOCATED_E_BASE["d"] + ALLOCATED_E_BASE["s"]
                + ALLOCATED_E_BASE["charity"]
            }
            for owner in OWNERS
        }
        result["endpoint_diagnostics"] = []
        for index, allocation in enumerate(core["allocations"], start=1):
            is_efx = z3.is_true(model.eval(
                allocation_formula(allocation, value, "complete_efx"),
                model_completion=True,
            ))
            utilities = {
                owner: str(rational(model, total(value, owner, allocation[owner])))
                for owner in OWNERS
            }
            result["endpoint_diagnostics"].append({
                "endpoint": index,
                "is_efx": is_efx,
                "owner_utilities": utilities,
                "underpaid_owners": [
                    owner for owner in OWNERS if Fraction(utilities[owner]) < 1
                ],
            })
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=130363)
    parser.add_argument("--allow-d-payment-hole", action="store_true")
    parser.add_argument("--maximum-payment-holes", type=int, choices=range(5))
    parser.add_argument(
        "--required-paid-owners",
        nargs="*",
        choices=OWNERS,
        default=(),
        help="Owners that must be paid in addition to the payment-hole bound.",
    )
    parser.add_argument("--full-pi-source", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(
        args.core_source, args.output, args.timeout_seconds, args.random_seed,
        args.allow_d_payment_hole, args.maximum_payment_holes,
        args.full_pi_source,
        tuple(args.required_paid_owners),
    ), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
