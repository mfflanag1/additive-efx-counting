#!/usr/bin/env python3
"""Audit the uncovered nonroot normalization-bypass support pattern."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
GAP = ROOT / "results/NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md"


def run(output: Path):
    # Exact support geometry: the normalized response is disjoint from the
    # singleton retired packet, while the counterfactual selector hits it.
    retired = {"p"}
    holder_target = {"w", "p"}
    repeated_response = {"b"}
    colliding_selector_support = {"p"}
    assert retired <= holder_target
    assert not (repeated_response & retired)
    assert colliding_selector_support & retired
    assert not (retired <= repeated_response)

    # Positive-additive local realization.  Source s owns e, strongly envies
    # q={b,c}, and has a safe singleton desired response b avoiding p.
    e, b, c, p = z3.Reals("e b c p")
    witness = z3.SolverFor("QF_LRA")
    witness.add(
        e == 1,
        b == 2,
        c == 2,
        p == z3.RealVal("1/10"),
        b > e,
        c > e,
        p <= e,
        b + c - z3.If(b <= c, b, c) > e,
    )
    witness_status = str(witness.check())
    assert witness_status == "sat"

    # Negate the applicability predicates of the two cited closure branches.
    root_is_holder = False
    response_contains_retired_packet = retired <= repeated_response
    nonroot_whole_hit_applies = response_contains_retired_packet
    root_holder_star_applies = root_is_holder
    assert not nonroot_whole_hit_applies
    assert not root_holder_star_applies

    result = {
        "schema": "nonroot-normalization-bypass-collision-gap-audit-v1",
        "status": "IMPORTED_FULL_COLLISION_COMPOSITION_GAP_CONFIRMED",
        "local_positive_additive_witness_status": witness_status,
        "retired_packet": sorted(retired),
        "current_holder": "nonroot",
        "colliding_selector_hits_packet": True,
        "normalized_repeated_response": sorted(repeated_response),
        "normalized_response_avoids_packet": True,
        "nonroot_whole_hit_dependency_applies": nonroot_whole_hit_applies,
        "root_holder_star_dependency_applies": root_holder_star_applies,
        "full_GG_countermodel": False,
        "active_fixed_u_theorem_refuted": False,
        "gap_sha256": hashlib.sha256(GAP.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Refutes coverage of the nonroot disjoint-response normalization "
            "bypass by the two cited dependencies. It is not a full-premise "
            "countermodel to T_L_times, fixed-U, GG, or EFX existence."
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
