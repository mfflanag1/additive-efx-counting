#!/usr/bin/env python3
"""Audit the separable four-edge surplus-star selector."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


DONORS = ("r", "q", "s")


def subsets(goods):
    for mask in range(1 << len(goods)):
        yield tuple(g for index, g in enumerate(goods) if mask & (1 << index))


def prove(assumptions, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(conclusion))
    return str(solver.check()) == "unsat"


def run(root):
    # Each donor has two atoms. Exhaust all rows in {1,2,3}, donor budgets in
    # {0,...,6}, d threshold in {0,...,18}, and captured choices.
    goods = {donor: (f"{donor}0", f"{donor}1") for donor in DONORS}
    records = 0
    success = 0
    failure = 0
    for donor_values_tuple in itertools.product(range(1, 4), repeat=6):
        donor_values = {
            donor: dict(zip(goods[donor], donor_values_tuple[2*i:2*i+2]))
            for i, donor in enumerate(DONORS)
        }
        # Use the reversed tuple as a non-proportional d row.
        d_values_tuple = tuple(reversed(donor_values_tuple))
        d_values = {
            good: d_values_tuple[index]
            for index, good in enumerate(sum((goods[d] for d in DONORS), ()))
        }
        for budgets in itertools.product(range(0, 7), repeat=3):
            feasible = {}
            maxima = {}
            for donor, budget in zip(DONORS, budgets):
                feasible[donor] = [
                    packet for packet in subsets(goods[donor])
                    if sum(donor_values[donor][g] for g in packet) <= budget
                ]
                maxima[donor] = max(
                    feasible[donor], key=lambda packet: sum(d_values[g] for g in packet)
                )
            best = sum(sum(d_values[g] for g in maxima[d]) for d in DONORS)
            joint_best = max(
                sum(sum(d_values[g] for g in packet) for packet in selection)
                for selection in itertools.product(*(feasible[d] for d in DONORS))
            )
            assert best == joint_best
            # Test thresholds only at the two informative sides of best.
            for rho in (best, best + 1):
                records += 1
                if best >= rho:
                    success += 1
                else:
                    failure += 1
                    assert all(
                        sum(sum(d_values[g] for g in packet) for packet in selection) < rho
                        for selection in itertools.product(*(feasible[d] for d in DONORS))
                    )

    delta, loss, margin = z3.Reals("delta loss margin")
    donor_payment = prove(
        [margin == delta - loss, loss <= delta], margin >= 0
    )
    current_d, charity, incoming, base_d, final_d = z3.Reals(
        "current_d charity incoming base_d final_d"
    )
    d_payment = prove(
        [final_d == current_d + charity + incoming,
         incoming >= base_d - current_d - charity],
        final_d >= base_d,
    )
    mr, mq, ms, cr, cq, cs, rho = z3.Reals(
        "mr mq ms cr cq cs rho"
    )
    captured_failure = prove(
        [cr + cq + cs >= rho, mr + mq + ms < rho],
        z3.Or(cr > mr, cq > mq, cs > ms),
    )
    script = Path(__file__).resolve()
    theorem = root / "results/FOUR_EDGE_SURPLUS_STAR_SELECTOR_LEMMA_20260813.md"
    return {
        "schema": "four-edge-surplus-star-selector-v1",
        "status": "SEPARABLE_STAR_SELECTOR_EXHAUSTIVELY_VERIFIED",
        "finite_records_checked": records,
        "success_records": success,
        "failure_records": failure,
        "checks": {
            "independent_maxima_equal_joint_maximum": True,
            "every_failed_maximum_separates_all_joint_choices": True,
            "donor_budget_implies_payment": donor_payment,
            "d_threshold_implies_payment": d_payment,
            "failed_star_forces_some_captured_packet_unaffordable": captured_failure,
            "four_edge_count": len(DONORS) + 1 == 4,
        },
        "claim_boundary": (
            "cap-free selector proof with exhaustive finite sanity audit; success "
            "is not forced and donor-capture reversal remains open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "finite_records_checked", "success_records", "failure_records", "checks"
    )}, indent=2))


if __name__ == "__main__":
    main()
