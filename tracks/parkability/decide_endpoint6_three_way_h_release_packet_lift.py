#!/usr/bin/env python3
"""Cap-free total/least-good decision for the three-way H-release core."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .decide_allocated_e_seven_endpoint_packet_lift import (
    ROOT,
    build_packet_master,
    endpoint_efx,
    response,
    serialize,
    total,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS
from .run_allocated_e_root_retention_new_debt_cegar import RETAINED


def run(
    core_source: Path,
    endpoint_source: Path,
    output: Path,
    timeout_seconds: int,
    random_seed: int,
    require_physical_realizability: bool = False,
):
    core_source = core_source.resolve()
    endpoint_source = endpoint_source.resolve()
    core = json.loads(core_source.read_text())
    endpoint6 = json.loads(endpoint_source.read_text())["allocations"][5]
    retained = RETAINED[6]
    signatures = tuple(
        tuple((source, tuple(pieces)) for source, pieces in signature)
        for signature in core["pi_signatures"]
    )
    allocations = tuple(core["allocations"])

    solver, value, least = build_packet_master()
    singleton = None
    if require_physical_realizability:
        singleton = {piece: z3.Bool(f"h_release_singleton_{piece}") for piece in GOODS}
        for piece in GOODS:
            for observer in OWNERS:
                solver.add(z3.If(
                    singleton[piece],
                    value[piece, observer] == least[piece, observer],
                    value[piece, observer] >= 2 * least[piece, observer],
                ))
        solver.add(singleton["p"])
    solver.add(
        endpoint_efx(value, least, endpoint6),
        total(value, "q", endpoint6["q"]) >= 1,
        total(value, "s", endpoint6["s"]) >= 1,
        total(value, "q", retained["q"]) < 1,
    )
    for signature in signatures:
        solver.add(z3.Or(*(
            z3.Not(response(value, least, source, pieces))
            for source, pieces in signature
        )))
    for allocation in allocations:
        solver.add(z3.Not(endpoint_efx(value, least, allocation)))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    started = time.monotonic()
    status = solver.check()
    result = {
        "schema": "endpoint6-three-way-h-release-packet-tail-lift-v1",
        "status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "elapsed_seconds": time.monotonic() - started,
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "endpoint_source": str(endpoint_source.relative_to(ROOT)),
        "endpoint_source_sha256": hashlib.sha256(endpoint_source.read_bytes()).hexdigest(),
        "pi_clause_count": len(signatures),
        "release_allocation_count": len(allocations),
        "packet_model": "independent total and least-good value per named piece/observer",
        "physical_relaxation": (
            "exact common singleton-or-two-good realizability per named piece"
            if require_physical_realizability
            else "0 < least <= total; singleton equality imposed only for P"
        ),
        "require_physical_realizability": require_physical_realizability,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "UNSAT proves the three-way whole-named-packet tail lift in the "
            "declared physical form-2 chart under a relaxation containing every "
            "packet cardinality. SAT may be physically unrealizable and does not "
            "refute the universal fixed-U theorem without a realization audit."
        ),
    }
    if status == z3.sat:
        model = solver.model()
        result["totals"] = serialize(model, value)
        result["least_values"] = serialize(model, least)
        if singleton is not None:
            result["packet_cardinality_class"] = {
                piece: (
                    "singleton" if z3.is_true(model.eval(flag, model_completion=True))
                    else "two"
                )
                for piece, flag in singleton.items()
            }
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--endpoint-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=86028121)
    parser.add_argument("--require-physical-realizability", action="store_true")
    args = parser.parse_args()
    result = run(
        args.core_source,
        args.endpoint_source,
        args.output,
        args.timeout_seconds,
        args.random_seed,
        args.require_physical_realizability,
    )
    print(json.dumps({
        "status": result["status"],
        "pi_clauses": result["pi_clause_count"],
        "release_allocations": result["release_allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
