#!/usr/bin/env python3
"""Decide the physically realizable total/minimum seven-endpoint lift."""

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
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def run(core_source: Path, output: Path, timeout_seconds: int, random_seed: int):
    core_source = core_source.resolve()
    core = json.loads(core_source.read_text())
    signatures = [
        tuple((source, tuple(pieces)) for source, pieces in signature)
        for signature in core["pi_signatures"]
    ]
    allocations = core["allocations"]
    solver, value, least = build_packet_master()

    singleton = {piece: z3.Bool(f"physical_singleton_{piece}") for piece in GOODS}
    for piece in GOODS:
        for observer in OWNERS:
            solver.add(z3.If(
                singleton[piece],
                value[piece, observer] == least[piece, observer],
                value[piece, observer] >= 2 * least[piece, observer],
            ))
    solver.add(singleton["p"])

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
        "schema": "allocated-e-seven-endpoint-physical-packet-tail-lift-v1",
        "status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "elapsed_seconds": time.monotonic() - started,
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "pi_clause_count": len(signatures),
        "endpoint_count": len(allocations),
        "physical_realizability": (
            "one shared cardinality branch per named packet: singleton gives "
            "total=least for every observer; nonsingleton gives total>=2*least "
            "for every observer and is realizable with two positive goods"
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "UNSAT proves the whole-named-packet seven-endpoint tail lift for "
            "all physically realizable finite positive packet refinements. SAT "
            "is an exact physical packet refinement defeating the seven endpoints "
            "and the 425 bounded-core PI families, but is not automatically a full "
            "saturated fixed-U countermodel because arbitrary subpacket PI and "
            "continuation exclusions remain to be audited."
        ),
    }
    if status == z3.sat:
        model = solver.model()
        result["packet_cardinality_class"] = {
            piece: "singleton" if z3.is_true(model.eval(singleton[piece])) else "two_or_more"
            for piece in GOODS
        }
        result["totals"] = serialize(model, value)
        result["least_values"] = serialize(model, least)
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=99991)
    args = parser.parse_args()
    result = run(args.core_source, args.output, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "pi_clauses": result["pi_clause_count"],
        "endpoints": result["endpoint_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
