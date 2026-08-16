#!/usr/bin/env python3
"""Decide one fixed full-critical-cut two-source gradient cell."""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_threshold_plateau_exact_paths import (
        exact_best_hall_margin,
        hall_witnesses,
        margin_graph,
        mask_threshold,
        mask_value,
    )
    from .decide_threshold_hall_local_gradient import (
        BASE,
        FLOATER,
        completion_margins,
        eligible,
        global_audit,
        integer_values,
        maximum,
        minimum,
        threshold,
        total,
    )
    from .fast_count import FastParkability
except ImportError:
    from anneal import atomic_json
    from audit_threshold_plateau_exact_paths import (
        exact_best_hall_margin,
        hall_witnesses,
        margin_graph,
        mask_threshold,
        mask_value,
    )
    from decide_threshold_hall_local_gradient import (
        BASE,
        FLOATER,
        completion_margins,
        eligible,
        global_audit,
        integer_values,
        maximum,
        minimum,
        threshold,
        total,
    )
    from fast_count import FastParkability


SCHEMA = "threshold-full-cut-two-source-4x9-v1"


def complete_bundles(bundles, floater, host):
    result = list(bundles)
    result[host] = tuple(sorted((*result[host], floater)))
    return tuple(result)


def edge_slack(values, bundles, observer, assigned):
    required = maximum(
        threshold(values[observer], bundles[target])
        for target in range(4)
        if target != assigned
    )
    return total(values[observer], bundles[assigned]) - required


def owner_threshold_potential(values, bundles):
    return z3.Sum(
        *(
            threshold(values[owner], bundles[owner])
            for owner in range(4)
        )
    )


def strict_subset_hall(values, bundles, beta, agents):
    size = len(agents)
    matchings = []
    for assigned in itertools.permutations(range(4), size):
        matchings.append(
            z3.And(
                *(
                    edge_slack(values, bundles, observer, bundle) > beta
                    for observer, bundle in zip(agents, assigned)
                )
            )
        )
    return z3.Or(*matchings)


def exact_eligible(values, state):
    for observer in range(4):
        own = mask_value(values, observer, state["masks"][observer])
        if own < values[observer][state["floater"]]:
            return False
        for target in range(4):
            if target != observer and own < mask_threshold(
                values,
                observer,
                state["masks"][target],
            ):
                return False
    return True


def exact_local_audit(values):
    base = {
        "floater": FLOATER,
        "masks": tuple(
            sum(1 << good for good in bundle) for bundle in BASE
        ),
    }
    beta, best_host, best_permutation, _bottlenecks = exact_best_hall_margin(
        values,
        base,
    )
    complete_masks = list(base["masks"])
    complete_masks[best_host] |= 1 << FLOATER
    strict_graph = margin_graph(
        values,
        tuple(complete_masks),
        beta,
        strict=True,
    )
    witnesses = hall_witnesses(strict_graph)
    minimum_witness_size = min(len(item["agents"]) for item in witnesses)
    candidates = []
    for owner in (0, 1):
        goods = [
            good
            for good in range(9)
            if base["masks"][owner] & (1 << good)
        ]
        owner_minimum = min(values[owner][good] for good in goods)
        for outgoing in goods:
            if values[owner][outgoing] != owner_minimum:
                continue
            masks = list(base["masks"])
            masks[owner] &= ~(1 << outgoing)
            masks[owner] |= 1 << FLOATER
            candidate = {"floater": outgoing, "masks": tuple(masks)}
            candidate_margin, candidate_host, candidate_permutation, _ = (
                exact_best_hall_margin(values, candidate)
            )
            candidates.append(
                {
                    "source": owner,
                    "outgoing_good": outgoing,
                    "eligible": exact_eligible(values, candidate),
                    "margin": str(candidate_margin),
                    "best_host": candidate_host,
                    "best_permutation": list(candidate_permutation),
                    "strictly_improves": candidate_margin > beta,
                }
            )
    base_theta = sum(
        Fraction(
            mask_threshold(values, owner, base["masks"][owner]),
            sum(values[owner]),
        )
        for owner in range(4)
    )
    cross_source_exchanges = []
    for host_good in BASE[0]:
        for missing_good in BASE[1]:
            masks = list(base["masks"])
            masks[0] &= ~(1 << host_good)
            masks[0] |= 1 << missing_good
            masks[1] &= ~(1 << missing_good)
            masks[1] |= 1 << host_good
            exchanged = {"floater": FLOATER, "masks": tuple(masks)}
            exchanged_theta = sum(
                Fraction(
                    mask_threshold(
                        values,
                        owner,
                        exchanged["masks"][owner],
                    ),
                    sum(values[owner]),
                )
                for owner in range(4)
            )
            cross_source_exchanges.append(
                {
                    "host_good": host_good,
                    "missing_good": missing_good,
                    "eligible": exact_eligible(values, exchanged),
                    "theta": str(exchanged_theta),
                    "strictly_improves_theta": exchanged_theta > base_theta,
                }
            )
    return {
        "base_eligible": exact_eligible(values, base),
        "base_margin": str(beta),
        "base_best_host": best_host,
        "base_best_permutation": list(best_permutation),
        "minimum_strict_hall_witness_size": minimum_witness_size,
        "strict_graph": [list(row) for row in strict_graph],
        "two_source_candidates": candidates,
        "eligible_strict_improvement_exists": any(
            item["eligible"] and item["strictly_improves"]
            for item in candidates
        ),
        "base_theta": str(base_theta),
        "cross_source_exchanges": cross_source_exchanges,
        "eligible_improving_cross_source_exchange_exists": any(
            item["eligible"] and item["strictly_improves_theta"]
            for item in cross_source_exchanges
        ),
    }


def exact_global_escape(values):
    evaluator = FastParkability(4, 9)
    landscape = evaluator.partial_linear_potential_landscape(
        values,
        potential="normalized_threshold",
    )
    base_masks = tuple(
        sum(1 << good for good in bundle) for bundle in BASE
    )

    def theta(masks):
        return sum(
            Fraction(
                mask_threshold(values, owner, int(masks[owner])),
                sum(values[owner]),
            )
            for owner in range(4)
        )

    def owners(masks, floater):
        return tuple(
            -1
            if good == floater
            else next(
                owner
                for owner, mask in enumerate(masks)
                if int(mask) & (1 << good)
            )
            for good in range(9)
        )

    base_owners = owners(base_masks, FLOATER)
    records = []
    for winner in landscape["maximizers"]:
        masks = tuple(
            int(mask)
            for mask in evaluator.base_masks[winner["floater"]][
                winner["base_index"]
            ]
        )
        owner_vector = owners(masks, winner["floater"])
        records.append(
            {
                "distance": sum(
                    left != right
                    for left, right in zip(base_owners, owner_vector)
                ),
                "hall_insertable": winner["hall_insertable"],
                "floater": winner["floater"],
                "owners": list(owner_vector),
                "theta": str(theta(masks)),
            }
        )
    nearest = min(
        records,
        key=lambda record: (
            record["distance"],
            not record["hall_insertable"],
            record["floater"],
            record["owners"],
        ),
    )
    base_theta = theta(base_masks)
    maximum_theta = Fraction(nearest["theta"])
    return {
        "base_owners": list(base_owners),
        "base_theta": str(base_theta),
        "maximum_theta": str(maximum_theta),
        "theta_gap": str(maximum_theta - base_theta),
        "nearest_maximizer": nearest,
    }


def run(
    output: Path,
    smt2: Path,
    timeout_seconds: int,
    natural_matching_only: bool,
    forbid_cross_source_threshold_improvement: bool,
    host_minimum_good: int | None,
    missing_minimum_good: int | None,
):
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for row in values:
        solver.add(z3.Sum(*row) == 1)
        solver.add(*(entry > 0 for entry in row))
    solver.add(eligible(values, BASE, FLOATER))

    base_margins = completion_margins(values, BASE, FLOATER)
    beta = base_margins[0]
    solver.add(*(beta >= margin for margin in base_margins))
    solver.add(beta < 0)

    host = 0
    missing_bundle = 1
    equality_agent = 1
    complete = complete_bundles(BASE, FLOATER, host)

    selected_minima = {
        host: host_minimum_good,
        missing_bundle: missing_minimum_good,
    }
    for owner, selected_good in selected_minima.items():
        if selected_good is None:
            continue
        if selected_good not in BASE[owner]:
            raise ValueError(
                f"good {selected_good} does not belong to source {owner}"
            )
        solver.add(
            *(
                values[owner][selected_good] < values[owner][other]
                for other in BASE[owner]
                if other != selected_good
            )
        )

    solver.add(
        *(
            edge_slack(values, complete, observer, missing_bundle) <= beta
            for observer in range(4)
        )
    )
    solver.add(
        edge_slack(values, complete, equality_agent, missing_bundle) == beta
    )
    for observer in range(4):
        if observer != equality_agent:
            solver.add(
                edge_slack(values, complete, observer, observer) > beta
            )
    for size in range(1, 4):
        for agents in itertools.combinations(range(4), size):
            solver.add(strict_subset_hall(values, complete, beta, agents))

    local_implications = 0
    for owner in (host, missing_bundle):
        bundle = BASE[owner]
        old_threshold = threshold(values[owner], bundle)
        for outgoing in bundle:
            if (
                selected_minima[owner] is not None
                and outgoing != selected_minima[owner]
            ):
                continue
            is_owner_minimum = z3.And(
                *(
                    values[owner][outgoing] <= values[owner][other]
                    for other in bundle
                )
            )
            swapped = list(BASE)
            swapped[owner] = tuple(
                sorted(good for good in (*bundle, FLOATER) if good != outgoing)
            )
            swapped = tuple(swapped)
            premise = z3.And(
                is_owner_minimum,
                eligible(values, swapped, outgoing),
            )
            solver.add(
                z3.Implies(
                    premise,
                    threshold(values[owner], swapped[owner]) <= old_threshold,
                )
            )
            margins = completion_margins(values, swapped, outgoing)
            if natural_matching_only:
                successor_host = (
                    missing_bundle if owner == host else host
                )
                natural_margin = margins[successor_host * 24]
                solver.add(z3.Implies(premise, natural_margin <= beta))
                local_implications += 1
            else:
                for successor_host in range(4):
                    if successor_host == owner:
                        continue
                    start = successor_host * 24
                    for margin in margins[start : start + 24]:
                        solver.add(z3.Implies(premise, margin <= beta))
                        local_implications += 1

    cross_source_implications = 0
    if forbid_cross_source_threshold_improvement:
        base_theta = owner_threshold_potential(values, BASE)
        for host_good in BASE[host]:
            for missing_good in BASE[missing_bundle]:
                exchanged = list(BASE)
                exchanged[host] = tuple(
                    sorted(
                        good
                        for good in (*BASE[host], missing_good)
                        if good != host_good
                    )
                )
                exchanged[missing_bundle] = tuple(
                    sorted(
                        good
                        for good in (*BASE[missing_bundle], host_good)
                        if good != missing_good
                    )
                )
                exchanged = tuple(exchanged)
                solver.add(
                    z3.Implies(
                        eligible(values, exchanged, FLOATER),
                        owner_threshold_potential(values, exchanged)
                        <= base_theta,
                    )
                )
                cross_source_implications += 1

    verdict = solver.check()
    smt2.write_text(solver.to_smt2())
    model = solver.model() if verdict == z3.sat else None
    integers = integer_values(model, values) if model is not None else None
    local_audit = exact_local_audit(integers) if integers is not None else None
    artifact = {
        "schema": SCHEMA,
        "status": (
            "FIXED_FULL_CUT_TWO_SOURCE_COUNTERMODEL"
            if verdict == z3.sat
            else "FIXED_FULL_CUT_TWO_SOURCE_FORCED"
            if verdict == z3.unsat
            else "UNKNOWN"
        ),
        "meaning": (
            "SAT refutes only the fixed full-cut two-source local statement; "
            "it refutes the global selector only if the exact audit also "
            "makes the fixed base globally threshold-maximal. UNSAT proves "
            "only this canonical four-pair critical-cut cell."
        ),
        "base_bundles": [list(bundle) for bundle in BASE],
        "floater": FLOATER,
        "base_host": host,
        "base_permutation": [0, 1, 2, 3],
        "missing_bundle": missing_bundle,
        "equality_agent": equality_agent,
        "candidate_sources": [host, missing_bundle],
        "local_implication_count": local_implications,
        "natural_matching_only": natural_matching_only,
        "forbid_cross_source_threshold_improvement": (
            forbid_cross_source_threshold_improvement
        ),
        "cross_source_implication_count": cross_source_implications,
        "host_minimum_good": host_minimum_good,
        "missing_minimum_good": missing_minimum_good,
        "solver_verdict": str(verdict),
        "solver_reason_unknown": (
            solver.reason_unknown() if verdict == z3.unknown else None
        ),
        "timeout_seconds": timeout_seconds,
        "values": integers,
        "exact_local_audit": local_audit,
        "exact_global_escape": (
            exact_global_escape(integers) if integers is not None else None
        ),
        "global_audit": global_audit(integers) if integers is not None else None,
        "smt2": str(smt2),
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--natural-matching-only", action="store_true")
    parser.add_argument(
        "--forbid-cross-source-threshold-improvement",
        action="store_true",
    )
    parser.add_argument("--host-minimum-good", type=int)
    parser.add_argument("--missing-minimum-good", type=int)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.output,
                args.smt2,
                args.timeout_seconds,
                args.natural_matching_only,
                args.forbid_cross_source_threshold_improvement,
                args.host_minimum_good,
                args.missing_minimum_good,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
