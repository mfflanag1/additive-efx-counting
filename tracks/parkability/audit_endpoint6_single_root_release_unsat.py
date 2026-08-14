#!/usr/bin/env python3
"""Independent nested-minimum replay of the single-root-release theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from .audit_allocated_e_two_hole_endpoint_unsat import direct_atomic_efx
from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_allocated_e_root_retention_new_debt_cegar import RETAINED
from .run_fixed_u_full_packet_terminal_cegar import total
from .run_fixed_u_rank_three_relation_cegar import base_response


ROOT = Path(__file__).resolve().parents[2]


def run(
    core_source: Path,
    endpoint_source: Path,
    output: Path,
    timeout_seconds: int,
    random_seed: int,
):
    core_source = core_source.resolve()
    endpoint_source = endpoint_source.resolve()
    core = json.loads(core_source.read_text())
    assert core["status"] == "UNSAT_CORE_EXTRACTED"
    endpoint6 = json.loads(endpoint_source.read_text())["allocations"][5]
    retained = RETAINED[6]
    signatures = tuple(
        tuple((source, tuple(pieces)) for source, pieces in signature)
        for signature in core["pi_signatures"]
    )
    allocations = tuple(core["allocations"])

    solver, value = build_master(2)
    solver.add(
        direct_atomic_efx(value, endpoint6),
        total(value, "q", endpoint6["q"]) >= 1,
        total(value, "s", endpoint6["s"]) >= 1,
        total(value, "q", retained["q"]) < 1,
    )
    for signature in signatures:
        solver.add(z3.Or(*(
            z3.Not(base_response(value, source, pieces))
            for source, pieces in signature
        )))
    for allocation in allocations:
        solver.add(z3.Not(direct_atomic_efx(value, allocation)))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    status = solver.check()
    result = {
        "schema": "endpoint6-single-root-release-unsat-audit-v1",
        "status": (
            "AUDIT_PASSED" if status == z3.unsat
            else "AUDIT_UNKNOWN" if status == z3.unknown
            else "AUDIT_FAILED"
        ),
        "solver_status": str(status),
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "endpoint_source_sha256": hashlib.sha256(endpoint_source.read_bytes()).hexdigest(),
        "pi_clause_count": len(signatures),
        "allocation_count": len(allocations),
        "endpoint_encoding": "direct literal atomic deletion inequalities",
        "pi_encoding": "independent nested-minimum base_response",
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Independent exact replay of the bounded single-root-release "
            "theorem. It does not prove its cap-free physical lift."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--endpoint-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=67867967)
    args = parser.parse_args()
    print(json.dumps(run(
        args.core_source,
        args.endpoint_source,
        args.output,
        args.timeout_seconds,
        args.random_seed,
    ), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
