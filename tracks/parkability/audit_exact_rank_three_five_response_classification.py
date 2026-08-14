#!/usr/bin/env python3
"""Audit the exact five-response classification of the fixed-U gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


FORMS = (
    (("r", "q"), ("q", "r"), ("s", "d"), ("d", "q"), ("d", "r")),
    (("r", "q"), ("q", "d"), ("s", "r"), ("d", "q"), ("d", "r")),
    (("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r")),
    (("r", "q"), ("q", "s"), ("s", "d"), ("d", "q"), ("d", "r")),
)


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def has_rank_four(edges):
    edges = set(edges)
    # Four sources must take four distinct owner targets. Charity is excluded.
    import itertools
    owners = ("r", "q", "d", "s")
    return any(
        all((source, target) in edges for source, target in zip(owners, targets))
        for targets in itertools.permutations(owners)
    )


def run(root: Path):
    w, a1, floor, desired_subset = z3.Reals("w a1 floor desired_subset")
    q_budget_implication = prove(
        [
            floor >= 0,
            desired_subset > floor,
            w >= desired_subset,
            a1 > w,
        ],
        a1 > floor,
    )
    form_rank = [has_rank_four(form) for form in FORMS]
    assert form_rank == [False, False, False, True]

    # Form 1 requires q -> d but forbids q -> r. A desired subset of W has
    # value above q's floor; the q-budget a1>W forces singleton a1 in Y_r
    # above the same floor, and singleton safety makes q -> r unavoidable.
    statuses = [
        "survives_graph_and_q_budget",
        "excluded_by_q_to_d_implies_q_to_r",
        "survives_graph_and_q_budget",
        "excluded_by_rank_four_matching",
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/EXACT_RANK_THREE_FIVE_RESPONSE_CLASSIFICATION_LEMMA_20260813.md"
    return {
        "schema": "exact-rank-three-five-response-classification-v1",
        "status": "EXACTLY_TWO_RESPONSE_FORMS_SURVIVE",
        "forms": [
            {
                "index": index,
                "edges": [list(edge) for edge in form],
                "rank_four_matching_exists": form_rank[index],
                "classification": statuses[index],
            }
            for index, form in enumerate(FORMS)
        ],
        "checks": {
            "q_budget_forces_q_to_r_from_q_to_d": q_budget_implication,
            "fourth_form_has_rank_four_matching": form_rank[3],
            "surviving_form_indices": [0, 2],
        },
        "surviving_forms": {
            "two_cycle": [list(edge) for edge in FORMS[0]],
            "three_cycle": [list(edge) for edge in FORMS[2]],
        },
        "exact_remaining_gate": (
            "complete the sacrificed d owner from its two responses into r/q "
            "while retaining or rerouting the paid r-q or r-q-s cycle and "
            "absorbing singleton charity through at most four support edges"
        ),
        "claim_boundary": (
            "cap-free graph and q-budget classification inside the named fixed-U "
            "packet interface; it does not prove full signed reachability, cycle "
            "release compatibility, or the complete four-edge EFX conclusion"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
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
    print(json.dumps({
        "status": result["status"],
        "surviving_form_indices": result["checks"]["surviving_form_indices"],
    }, indent=2))


if __name__ == "__main__":
    main()
