#!/usr/bin/env python3
"""Audit the count and scalar implications in the R2 role compression."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def prove(assumptions, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(conclusion))
    return str(solver.check()) == "unsat"


def run(root):
    response_target_regions = {
        "A+H": ("a0", "a1", "h"),
        "Q": ("j", "k", "q0"),
        "W": ("m", "gq", "gr"),
    }
    unaffected = ("l", "e", "p")
    role_count = 2 * sum(map(len, response_target_regions.values())) + len(unaffected)

    total, physical_minimum, compressed_minimum, floor = z3.Reals(
        "total physical_minimum compressed_minimum floor"
    )
    safety_monotonicity = prove(
        [compressed_minimum >= physical_minimum,
         total - physical_minimum <= floor],
        total - compressed_minimum <= floor,
    )
    retained_minimum_tail_identity = prove(
        [compressed_minimum == physical_minimum],
        total - compressed_minimum == total - physical_minimum,
    )
    hidden_minimum_chain = prove(
        [total - compressed_minimum <= floor,
         total - physical_minimum > floor],
        z3.And(
            physical_minimum < total - floor,
            total - floor <= compressed_minimum,
        ),
    )
    assert role_count == 21
    assert safety_monotonicity
    assert retained_minimum_tail_identity
    assert hidden_minimum_chain

    script = Path(__file__).resolve()
    theorem = root / "results/R2_RESPONSE_ROLE_CRITICAL_COMPRESSION_LEMMA_20260814.md"
    return {
        "schema": "r2-response-role-critical-compression-audit-v1",
        "status": "R2_ROLE_COMPRESSION_SCALARS_VERIFIED",
        "response_target_regions": response_target_regions,
        "unaffected_regions": list(unaffected),
        "response_role_count": role_count,
        "maximum_with_retained_d_minimum": role_count + 1,
        "checks": {
            "weak_tail_safety_survives_contraction": safety_monotonicity,
            "retained_d_minimum_preserves_strict_root_wall": retained_minimum_tail_identity,
            "unsafe_expansion_forces_hidden_minimum_chain": hidden_minimum_chain,
        },
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
            "z3_version": z3.get_version_string(),
        },
        "claim_boundary": (
            "Cap-free premise compression and scalar lift dichotomy only; "
            "hidden-minimum split conversion and the fixed-U theorem remain open."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))


if __name__ == "__main__":
    main()
