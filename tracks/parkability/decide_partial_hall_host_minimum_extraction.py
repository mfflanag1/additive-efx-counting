#!/usr/bin/env python3
"""Decide cap-free Hall extraction using host owner-minimum replacements."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "partial-hall-host-minimum-extraction-aggregate-v2"


def minimum(*terms):
    result = terms[0]
    for term in terms[1:]:
        result = z3.If(result <= term, result, term)
    return result


def run(
    output: Path,
    smt2: Path,
    timeout_seconds: int,
    any_source: bool = False,
    allow_owner_ties: bool = False,
    singleton_mask: int = 0,
) -> dict:
    selected = [
        [z3.Real(f"g_{observer}_{bundle}") for bundle in range(4)]
        for observer in range(4)
    ]
    remainder_total = [
        [z3.Real(f"r_{observer}_{bundle}") for bundle in range(4)]
        for observer in range(4)
    ]
    remainder_minimum = [
        [z3.Real(f"q_{observer}_{bundle}") for bundle in range(4)]
        for observer in range(4)
    ]
    floaters = [z3.Real(f"f_{observer}") for observer in range(4)]
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)

    def base_total(observer, bundle):
        if singleton_mask & (1 << bundle):
            return selected[observer][bundle]
        return selected[observer][bundle] + remainder_total[observer][bundle]

    def base_minimum(observer, bundle):
        if singleton_mask & (1 << bundle):
            return selected[observer][bundle]
        return minimum(
            selected[observer][bundle], remainder_minimum[observer][bundle]
        )

    for observer in range(4):
        solver.add(floaters[observer] > 0)
        solver.add(
            sum(base_total(observer, bundle) for bundle in range(4))
            + floaters[observer]
            == 1
        )
        for bundle in range(4):
            solver.add(selected[observer][bundle] > 0)
            if not singleton_mask & (1 << bundle):
                solver.add(remainder_minimum[observer][bundle] > 0)
                solver.add(
                    remainder_total[observer][bundle]
                    >= remainder_minimum[observer][bundle]
                )
        if not singleton_mask & (1 << observer):
            if allow_owner_ties:
                solver.add(
                    selected[observer][observer]
                    <= remainder_minimum[observer][observer]
                )
            else:
                solver.add(
                    selected[observer][observer]
                    < remainder_minimum[observer][observer]
                )
        own = base_total(observer, observer)
        solver.add(own >= floaters[observer])
        for target in range(4):
            if target != observer:
                solver.add(
                    own
                    >= base_total(observer, target)
                    - base_minimum(observer, target)
                )

    candidates = [(host, None, None) for host in range(4)]
    if any_source:
        candidates += [
            (host, source, destination)
            for host in range(4)
            for source in range(4)
            for destination in range(4)
            if destination != source
            and (
                not singleton_mask & (1 << source)
                or host == source
            )
        ]
    else:
        candidates += [
            (host, host, destination)
            for host in range(4)
            for destination in range(4)
            if destination != host
        ]
    edges = {}
    for candidate_index, (host, source, destination) in enumerate(candidates):
        for observer in range(4):
            totals = []
            minima = []
            for bundle in range(4):
                if source is None:
                    total = base_total(observer, bundle)
                    least = base_minimum(observer, bundle)
                    if bundle == host:
                        total += floaters[observer]
                        least = minimum(least, floaters[observer])
                else:
                    if bundle == source:
                        if singleton_mask & (1 << source):
                            assert host == source
                            total = z3.RealVal(0)
                            least = None
                        else:
                            total = remainder_total[observer][source]
                            least = remainder_minimum[observer][source]
                    else:
                        total = base_total(observer, bundle)
                        least = base_minimum(observer, bundle)
                    if bundle == destination:
                        total += selected[observer][source]
                        least = minimum(least, selected[observer][source])
                    if bundle == host:
                        total += floaters[observer]
                        least = (
                            floaters[observer]
                            if least is None
                            else minimum(least, floaters[observer])
                        )
                totals.append(total)
                minima.append(least)
            for bundle in range(4):
                edge = z3.Bool(f"e_{candidate_index}_{observer}_{bundle}")
                solver.add(
                    edge
                    == z3.And(
                        *(
                            totals[bundle] >= totals[target] - minima[target]
                            for target in range(4)
                            if target != bundle
                        )
                    )
                )
                edges[candidate_index, observer, bundle] = edge

        for permutation in itertools.permutations(range(4)):
            solver.add(
                z3.Not(
                    z3.And(
                        *(
                            edges[candidate_index, observer, permutation[observer]]
                            for observer in range(4)
                        )
                    )
                )
            )
        for first, second in itertools.combinations(range(4), 2):
            for sole_neighbor in range(4):
                solver.add(
                    z3.Not(
                        z3.And(
                            edges[candidate_index, first, sole_neighbor],
                            edges[candidate_index, second, sole_neighbor],
                            *(
                                z3.Not(edges[candidate_index, observer, bundle])
                                for observer in (first, second)
                                for bundle in range(4)
                                if bundle != sole_neighbor
                            ),
                        )
                    )
                )

    verdict = solver.check()
    smt2.write_text(solver.to_smt2())
    model = solver.model() if verdict == z3.sat else None
    artifact = {
        "schema": (
            "partial-hall-owner-minimum-extraction-aggregate-v1"
            if any_source
            else SCHEMA
        ),
        "status": (
            (
                "OWNER_MINIMUM_PAIR_EXTRACTION_FORCED"
                if any_source
                else "HOST_MINIMUM_PAIR_EXTRACTION_FORCED"
            )
            if verdict == z3.unsat
            else "AGGREGATE_COUNTEREXAMPLE"
            if verdict == z3.sat
            else "UNKNOWN"
        ),
        "meaning": (
            "UNSAT proves the selected owner-minimum pair-extraction disjunction "
            "for four-agent one-floater EFX states with the stated singleton "
            "bundle labels. SAT must be checked for item-level realizability."
        ),
        "candidate_count": len(candidates),
        "candidate_family": (
            "four direct insertions plus every transfer of a source owner's "
            "selected minimum good, with host and source independent"
            if any_source
            else "four direct insertions plus, for each host, replacement of an "
            "owner-minimum good by the floater and transfer of that good to "
            "one of the other three bundles"
        ),
        "abstraction": (
            "Each nonsingleton bundle is its owner's selected minimum good plus "
            "a nonempty remainder; singleton bundles contain only the selected "
            "good. Per-observer values, remainder totals, and remainder minima "
            "determine all encoded EFX edges. Remainder realizability is "
            "relaxed, so UNSAT is sound."
        ),
        "solver_verdict": str(verdict),
        "owner_minimum_ties_allowed": allow_owner_ties,
        "singleton_bundle_labels": [
            bundle for bundle in range(4) if singleton_mask & (1 << bundle)
        ],
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "model": (
            {
                "selected_goods": [
                    [model.evaluate(value).sexpr() for value in row]
                    for row in selected
                ],
                "remainder_totals": [
                    [model.evaluate(value).sexpr() for value in row]
                    for row in remainder_total
                ],
                "remainder_minima": [
                    [model.evaluate(value).sexpr() for value in row]
                    for row in remainder_minimum
                ],
                "floaters": [model.evaluate(value).sexpr() for value in floaters],
                "candidate_graphs": {
                    f"host={host},source={source},destination={destination}": [
                        [
                            bundle
                            for bundle in range(4)
                            if z3.is_true(
                                model.evaluate(edges[index, observer, bundle])
                            )
                        ]
                        for observer in range(4)
                    ]
                    for index, (host, source, destination) in enumerate(candidates)
                },
            }
            if model is not None
            else None
        ),
        "timeout_seconds": timeout_seconds,
        "smt2": str(smt2),
        "smt2_sha256": hashlib.sha256(smt2.read_bytes()).hexdigest(),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--smt2", required=True, type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--any-source", action="store_true")
    parser.add_argument("--allow-owner-ties", action="store_true")
    parser.add_argument("--singleton-mask", type=int, default=0)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.output,
                args.smt2,
                args.timeout_seconds,
                args.any_source,
                args.allow_owner_ties,
                args.singleton_mask,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
