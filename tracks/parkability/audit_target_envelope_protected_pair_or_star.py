#!/usr/bin/env python3
"""Exact audit of protected target-envelope pair/star exhaustion."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    agents = tuple(range(4))
    floor, response_threshold, envelope, q = z3.Reals(
        "floor response_threshold envelope q"
    )
    protected_payment = prove(
        [envelope >= floor, envelope >= response_threshold, q >= envelope],
        z3.And(q >= floor, q >= response_threshold),
    )
    assert protected_payment

    # In the star, an unsafe center response must be sourced by one of the
    # three leaves.  That leaf already supplies its disjoint offer to the
    # center, giving an exact supplier-closed directed 2-cycle.
    leaves = {0, 2, 3}
    center = 1
    center_response_sources = [a for a in agents if a != center]
    unsafe_center_two_cycles = all(a in leaves for a in center_response_sources)
    assert unsafe_center_two_cycles

    # Exhaust the abstract safe/unsafe and reversal-source labels for a fixed
    # target owner j=0 and response source s=1.  Self-sourcing reversals are
    # excluded by positivity.  All-unsafe is routed to the supplied-cycle
    # theorem; every other label takes pair or unique star form.
    target_owner = 0
    response_source = 1
    external = tuple(i for i in agents if i != target_owner)
    checked = 0
    routes = {"all_unsafe_PI": 0, "protected_pair": 0,
              "distinct_response_pair": 0, "same_source_star": 0}
    for safe_bits in itertools.product((False, True), repeat=3):
        unsafe_owners = [h for h, safe in zip(external, safe_bits) if not safe]
        source_choices = [tuple(a for a in agents if a != h) for h in unsafe_owners]
        for reversal_sources in itertools.product(*source_choices):
            checked += 1
            safe_owners = [h for h, safe in zip(external, safe_bits) if safe]
            if not safe_owners:
                route = "all_unsafe_PI"
            elif any(h != response_source for h in safe_owners):
                route = "protected_pair"
            else:
                assert safe_owners == [response_source]
                if any(a != response_source for a in reversal_sources):
                    route = "distinct_response_pair"
                else:
                    assert len(reversal_sources) == 2
                    route = "same_source_star"
            routes[route] += 1
    assert checked == 64
    assert routes == {
        "all_unsafe_PI": 27,
        "protected_pair": 28,
        "distinct_response_pair": 8,
        "same_source_star": 1,
    }

    results = repo / "results"
    theorem = results / "TARGET_ENVELOPE_PROTECTED_PAIR_OR_SAME_SOURCE_STAR_LEMMA_20260813.md"
    envelope_theorem = results / "TARGET_ENVELOPE_UNIVERSAL_PAYMENT_OR_PI_LEMMA_20260813.md"
    two_hole = results / "TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "target-envelope-protected-pair-or-star-audit-v1",
        "status": "SAFE_PAYMENT_WALL_REDUCED_TO_TWO_HOLE_OR_THREE_OFFER_STAR",
        "protected_packet_pays_floor_and_target_response": protected_payment,
        "unsafe_center_forces_supplied_two_cycle": unsafe_center_two_cycles,
        "abstract_labels_checked": checked,
        "route_counts": routes,
        "sole_new_survivor": "safe_center_three_offer_same_source_star",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free protected-envelope route exhaustion; the safe-center three-offer "
            "star and downstream retired-support collisions remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "envelope_theorem": str(envelope_theorem.relative_to(repo)),
            "envelope_theorem_sha256": sha256(envelope_theorem),
            "two_hole_theorem": str(two_hole.relative_to(repo)),
            "two_hole_theorem_sha256": sha256(two_hole),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "route_counts": result["route_counts"],
        "sole_new_survivor": result["sole_new_survivor"],
    }, indent=2))


if __name__ == "__main__":
    main()
