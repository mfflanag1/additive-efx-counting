#!/usr/bin/env python3
"""Independent algebra audit for the shared-target double-response gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def check_capture_implication():
    overlap, outside, floor = z3.Reals("overlap outside floor")
    desired = overlap + outside
    solver = z3.SolverFor("QF_LRA")
    solver.add(overlap >= 0, outside >= 0, floor >= 0)
    solver.add(desired > floor, outside <= floor)
    solver.add(overlap < desired - floor)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def check_strict_capture():
    overlap, outside, floor = z3.Reals("strict_overlap strict_outside strict_floor")
    desired = overlap + outside
    solver = z3.SolverFor("QF_LRA")
    solver.add(overlap >= 0, outside >= 0, floor >= 0)
    solver.add(desired > floor, outside < floor)
    solver.add(overlap <= desired - floor)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def check_packet_partition():
    # Labels stand for arbitrary disjoint physical packets.  The identities
    # establish that trimming C by A creates a core disjoint from A, while
    # the omitted packet is exactly A intersect C.
    target = {"only_A", "overlap", "only_C", "neither"}
    anchor = {"only_A", "overlap"}
    response = {"overlap", "only_C"}
    trimmed = response - anchor
    captured = response & anchor
    assert trimmed.isdisjoint(anchor)
    assert trimmed | captured == response
    assert target == anchor | trimmed | {"neither"}
    return {
        "trimmed_response": sorted(trimmed),
        "captured_overlap": sorted(captured),
        "partition_exact": True,
    }


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results/SHARED_TARGET_DOUBLE_RESPONSE_DISJOINT_OR_CAPTURE_LEMMA_20260813.md"
    return {
        "schema": "shared-target-double-response-disjoint-or-capture-v1",
        "status": "DISJOINT_OR_FULL_MARGIN_CAPTURE",
        "checks": {
            "weak_capture_implication": check_capture_implication(),
            "strict_capture_when_outside_strictly_below_floor": check_strict_capture(),
            "packet_partition": check_packet_partition(),
        },
        "exact_dichotomy": (
            "if C\\A remains desired, an inclusion-minimal subcore there is "
            "disjoint and inherits common safety; otherwise A intersection C "
            "captures at least the entire C-source response margin"
        ),
        "claim_boundary": (
            "cap-free set/algebra lemma; it does not reverse the capture "
            "inequality or prove endpoint owner-payment and observer safety"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
