#!/usr/bin/env python3
"""Independent replay of the two-payment-hole seven-endpoint theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from .audit_allocated_e_all_allocation_unsat import collect, structural_pi_signature
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, total
from .run_fixed_u_rank_three_relation_cegar import base_response


ROOT = Path(__file__).resolve().parents[2]


def direct_atomic_efx(value, allocation):
    rows = []
    for observer in OWNERS:
        own = total(value, observer, allocation[observer])
        for target in OWNERS:
            if target == observer:
                continue
            pieces = tuple(allocation[target])
            target_total = total(value, observer, pieces)
            rows.extend(
                own >= target_total - value[piece, observer]
                for piece in pieces
            )
    return z3.And(*rows)


def at_most_two_payment_holes(value, allocation, required_paid_owners=()):
    paid = [
        total(value, owner, allocation[owner])
        >= total(value, owner, ALLOCATED_E_BASE[owner])
        for owner in OWNERS
    ]
    return z3.And(
        z3.Sum(*(z3.If(predicate, 1, 0) for predicate in paid)) >= 2,
        *(
            total(value, owner, allocation[owner])
            >= total(value, owner, ALLOCATED_E_BASE[owner])
            for owner in required_paid_owners
        ),
    )


def run(source: Path, output: Path, timeout_seconds: int, random_seed: int,
        compact_core_source: Path | None = None):
    source = source.resolve()
    payload = json.loads(source.read_text())
    assert payload["status"] == "UNSAT_PI_OR_REQUIRED_PAID_SEVEN_ENDPOINT_EFX"
    assert payload["maximum_payment_holes"] == 2
    required_paid_owners = tuple(payload.get("required_paid_owners", ()))
    pi_source = ROOT / payload["full_pi_source"]
    core_source = ROOT / payload["core_source"]
    core = json.loads(core_source.read_text())
    assert hashlib.sha256(pi_source.read_bytes()).hexdigest() == payload["pi_source_sha256"]
    if compact_core_source is None:
        _, signature_map, _ = collect(pi_source)
        signatures = tuple(signature_map)
        allocations = tuple(core["allocations"])
    else:
        compact_core_source = compact_core_source.resolve()
        compact = json.loads(compact_core_source.read_text())
        assert compact["status"] == "UNSAT_CORE_EXTRACTED"
        assert compact["pi_source_sha256"] == payload["pi_source_sha256"]
        assert compact["core_source_sha256"] == payload["core_source_sha256"]
        assert tuple(compact.get("required_paid_owners", ())) == required_paid_owners
        signatures = tuple(
            tuple((source_owner, tuple(pieces)) for source_owner, pieces in signature)
            for signature in compact["pi_signatures"]
        )
        allocations = tuple(compact["allocations"])
        assert len(signatures) == compact["core_pi_clause_count"]
        assert len(allocations) == compact["core_endpoint_count"]
    assert payload["pi_clause_count"] == 46_683
    assert all(structural_pi_signature(signature) for signature in signatures)

    solver, value = build_master(2)
    for signature in signatures:
        solver.add(z3.Or(*(
            z3.Not(base_response(value, source_owner, core_pieces))
            for source_owner, core_pieces in signature
        )))
    for allocation in allocations:
        solver.add(z3.Not(z3.And(
            direct_atomic_efx(value, allocation),
            at_most_two_payment_holes(value, allocation, required_paid_owners),
        )))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    status = solver.check()
    result = {
        "schema": "allocated-e-two-hole-endpoint-unsat-audit-v1",
        "status": (
            "AUDIT_PASSED" if status == z3.unsat
            else "AUDIT_UNKNOWN" if status == z3.unknown
            else "AUDIT_FAILED"
        ),
        "solver_status": str(status),
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
        "producer": str(source.relative_to(ROOT)),
        "producer_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "pi_source_sha256": hashlib.sha256(pi_source.read_bytes()).hexdigest(),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "compact_core_source": (
            None if compact_core_source is None
            else str(compact_core_source.relative_to(ROOT))
        ),
        "compact_core_source_sha256": (
            None if compact_core_source is None
            else hashlib.sha256(compact_core_source.read_bytes()).hexdigest()
        ),
        "pi_clause_count": len(signatures),
        "endpoint_count": len(allocations),
        "endpoint_encoding": "direct literal atomic deletion inequalities",
        "pi_encoding": "independent nested-minimum base_response",
        "payment_encoding": "direct count of utilities at least normalized base",
        "required_paid_owners": list(required_paid_owners),
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Independent exact replay of the twelve-atom two-payment-hole "
            "endpoint theorem. It does not establish physical-tail safety or "
            "a cap-free packet theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=786433)
    parser.add_argument("--compact-core-source", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(
        args.source, args.output, args.timeout_seconds, args.random_seed,
        args.compact_core_source,
    ), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
