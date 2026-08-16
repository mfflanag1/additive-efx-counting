#!/usr/bin/env python3
"""Decide whether owner-minimum substitutions convert every Hall obstruction."""

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


SCHEMA = "partial-hall-owner-minimum-substitution-conversion-v1"


def minimum(*terms):
    result = terms[0]
    for term in terms[1:]:
        result = z3.If(result <= term, result, term)
    return result


def pair_orbit_representatives(candidates):
    permutations = tuple(itertools.permutations(range(4)))
    representatives = set()
    for candidate in candidates:
        for pair in itertools.combinations(range(4), 2):
            for neighbor in range(4):
                images = []
                for permutation in permutations:
                    host, source, destination = candidate
                    images.append(
                        (
                            (
                                permutation[host],
                                None if source is None else permutation[source],
                                None
                                if destination is None
                                else permutation[destination],
                            ),
                            tuple(sorted((permutation[pair[0]], permutation[pair[1]]))),
                            permutation[neighbor],
                        )
                    )
                representatives.add(min(images, key=repr))
    return tuple(sorted(representatives, key=repr))


def run(
    output: Path,
    smt2: Path,
    timeout_seconds: int,
    singleton_mask: int,
    remainder_multi_mask: int | None,
    pair_orbit_index: int | None,
    trap_witness_prefix: str | None,
    track_core: bool,
    cegar_batch: int,
    max_iterations: int,
    seed_blockers: tuple[str, ...],
    include_one_good_transfers: bool,
    cycle_specs: tuple[tuple[int, int, int, int, int, int], ...],
    include_pairwise_swaps: bool,
    swap_specs: tuple[tuple[int, int, int, int], ...],
    assert_complete_blockers: bool,
    selected_minimum_mask: int,
    solver_for_qf_lra: bool,
    integer_cap: int | None,
    hall_witness_encoding: bool,
    strict_owner_minima: bool,
) -> dict:
    variable = z3.Int if integer_cap is not None else z3.Real
    selected = [
        [variable(f"g_{observer}_{bundle}") for bundle in range(4)]
        for observer in range(4)
    ]
    remainder_total = [
        [variable(f"r_{observer}_{bundle}") for bundle in range(4)]
        for observer in range(4)
    ]
    remainder_minimum = [
        [variable(f"q_{observer}_{bundle}") for bundle in range(4)]
        for observer in range(4)
    ]
    floaters = [variable(f"f_{observer}") for observer in range(4)]
    solver = z3.SolverFor("QF_LRA") if solver_for_qf_lra else z3.Solver()
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
            == (integer_cap if integer_cap is not None else 1)
        )
        for bundle in range(4):
            solver.add(selected[observer][bundle] > 0)
            if not singleton_mask & (1 << bundle):
                solver.add(remainder_minimum[observer][bundle] > 0)
                if remainder_multi_mask is None:
                    solver.add(
                        remainder_total[observer][bundle]
                        >= remainder_minimum[observer][bundle]
                    )
                elif remainder_multi_mask & (1 << bundle):
                    solver.add(
                        remainder_total[observer][bundle]
                        >= 2 * remainder_minimum[observer][bundle]
                    )
                else:
                    solver.add(
                        remainder_total[observer][bundle]
                        == remainder_minimum[observer][bundle]
                    )
                if selected_minimum_mask & (1 << (4 * observer + bundle)):
                    solver.add(
                        selected[observer][bundle]
                        <= remainder_minimum[observer][bundle]
                    )
        if not singleton_mask & (1 << observer):
            owner_minimum_relation = (
                selected[observer][observer]
                < remainder_minimum[observer][observer]
                if strict_owner_minima
                else selected[observer][observer]
                <= remainder_minimum[observer][observer]
            )
            solver.add(owner_minimum_relation)
        own = base_total(observer, observer)
        solver.add(own >= floaters[observer])
        for target in range(4):
            if target != observer:
                solver.add(
                    own
                    >= base_total(observer, target)
                    - base_minimum(observer, target)
                )

    complete_candidates = [(host, None, None) for host in range(4)] + [
        (host, source, destination)
        for host in range(4)
        for source in range(4)
        for destination in range(4)
        if destination != source
        and (not singleton_mask & (1 << source) or host == source)
    ]
    completion_edges = {}
    completion_totals = {}
    completion_minima = {}
    pair_witnesses = []
    pair_witness_by_role = {}
    for index, (host, source, destination) in enumerate(complete_candidates):
        for observer in range(4):
            totals = []
            minima = []
            for bundle in range(4):
                if source is None:
                    total = base_total(observer, bundle)
                    least = base_minimum(observer, bundle)
                elif bundle == source:
                    if singleton_mask & (1 << source):
                        total = z3.RealVal(0)
                        least = None
                    else:
                        total = remainder_total[observer][source]
                        least = remainder_minimum[observer][source]
                else:
                    total = base_total(observer, bundle)
                    least = base_minimum(observer, bundle)
                if source is not None and bundle == destination:
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
                completion_totals[index, observer, bundle] = total
                completion_minima[index, observer, bundle] = least
            for bundle in range(4):
                edge = z3.Bool(f"ce_{index}_{observer}_{bundle}")
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
                completion_edges[index, observer, bundle] = edge
        if assert_complete_blockers and hall_witness_encoding:
            witnesses = []
            for deficient_size in range(1, 5):
                for deficient_agents in itertools.combinations(
                    range(4), deficient_size
                ):
                    for neighborhood in itertools.combinations(
                        range(4), deficient_size - 1
                    ):
                        allowed = set(neighborhood)
                        witnesses.append(
                            z3.And(
                                *(
                                    z3.Not(
                                        completion_edges[index, observer, bundle]
                                    )
                                    for observer in deficient_agents
                                    for bundle in range(4)
                                    if bundle not in allowed
                                )
                            )
                        )
            solver.add(z3.Or(*witnesses))
        elif assert_complete_blockers:
            for permutation in itertools.permutations(range(4)):
                blocker = z3.Not(
                    z3.And(
                        *(
                            completion_edges[index, observer, permutation[observer]]
                            for observer in range(4)
                        )
                    )
                )
                if track_core:
                    permutation_code = "".join(map(str, permutation))
                    solver.assert_and_track(
                        blocker, f"complete_{index}_{permutation_code}"
                    )
                else:
                    solver.add(blocker)
        for first, second in itertools.combinations(range(4), 2):
            for sole_neighbor in range(4):
                witness = z3.And(
                        completion_edges[index, first, sole_neighbor],
                        completion_edges[index, second, sole_neighbor],
                        *(
                            z3.Not(completion_edges[index, observer, bundle])
                            for observer in (first, second)
                            for bundle in range(4)
                            if bundle != sole_neighbor
                        ),
                    )
                pair_witnesses.append(witness)
                pair_witness_by_role[
                    ((host, source, destination), (first, second), sole_neighbor)
                ] = witness
    orbit_representatives = pair_orbit_representatives(complete_candidates)
    if pair_orbit_index is None:
        solver.add(z3.Or(*pair_witnesses))
        selected_pair_role = None
    else:
        if singleton_mask != 0 or remainder_multi_mask not in {0, 15}:
            raise ValueError("pair orbit branching requires a fully symmetric size case")
        selected_pair_role = orbit_representatives[pair_orbit_index]
        if track_core:
            solver.assert_and_track(pair_witness_by_role[selected_pair_role], "pair_branch")
        else:
            solver.add(pair_witness_by_role[selected_pair_role])
    if trap_witness_prefix:
        if selected_pair_role is None:
            raise ValueError("trap witness splitting requires --pair-orbit-index")
        candidate, pair, sole_neighbor = selected_pair_role
        candidate_index = complete_candidates.index(candidate)
        missing_edges = [
            (observer, bundle)
            for observer in pair
            for bundle in range(4)
            if bundle != sole_neighbor
        ]
        if len(trap_witness_prefix) > len(missing_edges):
            raise ValueError("trap witness prefix is too long")
        for digit, (observer, bundle) in zip(trap_witness_prefix, missing_edges):
            choices = [target for target in range(4) if target != bundle]
            choice = int(digit)
            if choice >= len(choices):
                raise ValueError("trap witness digits must be 0, 1, or 2")
            target = choices[choice]
            solver.add(
                completion_totals[candidate_index, observer, bundle]
                < completion_totals[candidate_index, observer, target]
                - completion_minima[candidate_index, observer, target]
            )

    base_potential = sum(base_total(agent, agent) for agent in range(4))
    substitution_count = 0
    transfer_partition_count = 0
    cycle_partition_count = 0
    swap_partition_count = 0
    maximality_records = []
    for host in range(4):
        for source in range(4):
            if singleton_mask & (1 << source) and host != source:
                continue
            substitution_count += 1
            totals_by_observer = []
            minima_by_observer = []
            for observer in range(4):
                totals = []
                minima = []
                for bundle in range(4):
                    if bundle == source:
                        if singleton_mask & (1 << source):
                            total = z3.RealVal(0)
                            least = None
                        else:
                            total = remainder_total[observer][source]
                            least = remainder_minimum[observer][source]
                    else:
                        total = base_total(observer, bundle)
                        least = base_minimum(observer, bundle)
                    if bundle == host:
                        total += floaters[observer]
                        least = (
                            floaters[observer]
                            if least is None
                            else minimum(least, floaters[observer])
                        )
                    totals.append(total)
                    minima.append(least)
                totals_by_observer.append(totals)
                minima_by_observer.append(minima)

            substitution_edges = {}
            for observer in range(4):
                for bundle in range(4):
                    own = totals_by_observer[observer][bundle]
                    edge = z3.Bool(f"pe_{host}_{source}_{observer}_{bundle}")
                    solver.add(
                        edge
                        == z3.And(
                            own >= selected[observer][source],
                            *(
                                own
                                >= totals_by_observer[observer][target]
                                - minima_by_observer[observer][target]
                                for target in range(4)
                                if target != bundle
                            ),
                        )
                    )
                    substitution_edges[observer, bundle] = edge

            for permutation in itertools.permutations(range(4)):
                potential_terms = []
                for observer in range(4):
                    own_bundle = permutation[observer]
                    own = totals_by_observer[observer][own_bundle]
                    potential_terms.append(own)
                maximality = z3.Implies(
                        z3.And(
                            *(
                                substitution_edges[observer, permutation[observer]]
                                for observer in range(4)
                            )
                        ),
                        sum(potential_terms) <= base_potential,
                    )
                permutation_code = "".join(map(str, permutation))
                label = f"maximality_{host}_{source}_{permutation_code}"
                maximality_records.append((maximality, label))
                if cegar_batch > 0:
                    continue
                if track_core:
                    solver.assert_and_track(
                        maximality,
                        label,
                    )
                else:
                    solver.add(maximality)

    if include_one_good_transfers:
        if singleton_mask != 0 or remainder_multi_mask != 0:
            raise ValueError(
                "one-good transfer encoding currently requires exactly two goods per bundle"
            )
        for source in range(4):
            for moved_type in range(2):
                for destination in range(4):
                    if destination == source:
                        continue
                    transfer_partition_count += 1
                    totals_by_observer = []
                    minima_by_observer = []
                    for observer in range(4):
                        source_items = (
                            selected[observer][source],
                            remainder_total[observer][source],
                        )
                        moved = source_items[moved_type]
                        retained = source_items[1 - moved_type]
                        totals = [
                            base_total(observer, bundle) for bundle in range(4)
                        ]
                        minima = [
                            base_minimum(observer, bundle) for bundle in range(4)
                        ]
                        totals[source] = retained
                        minima[source] = retained
                        totals[destination] += moved
                        minima[destination] = minimum(minima[destination], moved)
                        totals_by_observer.append(totals)
                        minima_by_observer.append(minima)

                    transfer_edges = {}
                    for observer in range(4):
                        for bundle in range(4):
                            own = totals_by_observer[observer][bundle]
                            edge = z3.Bool(
                                f"te_{source}_{moved_type}_{destination}_{observer}_{bundle}"
                            )
                            solver.add(
                                edge
                                == z3.And(
                                    own >= floaters[observer],
                                    *(
                                        own
                                        >= totals_by_observer[observer][target]
                                        - minima_by_observer[observer][target]
                                        for target in range(4)
                                        if target != bundle
                                    ),
                                )
                            )
                            transfer_edges[observer, bundle] = edge

                    for permutation in itertools.permutations(range(4)):
                        potential = sum(
                            totals_by_observer[observer][permutation[observer]]
                            for observer in range(4)
                        )
                        maximality = z3.Implies(
                            z3.And(
                                *(
                                    transfer_edges[observer, permutation[observer]]
                                    for observer in range(4)
                                )
                            ),
                            potential <= base_potential,
                        )
                        permutation_code = "".join(map(str, permutation))
                        label = (
                            f"transfer_{source}_{moved_type}_{destination}_"
                            f"{permutation_code}"
                        )
                        maximality_records.append((maximality, label))
                        if cegar_batch > 0:
                            continue
                        if track_core:
                            solver.assert_and_track(maximality, label)
                        else:
                            solver.add(maximality)

    if cycle_specs:
        if singleton_mask != 0 or remainder_multi_mask != 0:
            raise ValueError(
                "three-cycle encoding currently requires exactly two goods per bundle"
            )
        for specification in cycle_specs:
            first_bundle, first_type, second_bundle, second_type, third_bundle, third_type = specification
            if len({first_bundle, second_bundle, third_bundle}) != 3:
                raise ValueError("three-cycle bundles must be distinct")
            if any(item_type not in {0, 1} for item_type in (first_type, second_type, third_type)):
                raise ValueError("three-cycle item types must be 0 or 1")
            cycle_partition_count += 1
            totals_by_observer = []
            minima_by_observer = []
            for observer in range(4):
                bundles = (first_bundle, second_bundle, third_bundle)
                item_types = (first_type, second_type, third_type)
                items = {
                    bundle: (
                        selected[observer][bundle],
                        remainder_total[observer][bundle],
                    )
                    for bundle in bundles
                }
                totals = [base_total(observer, bundle) for bundle in range(4)]
                minima = [base_minimum(observer, bundle) for bundle in range(4)]
                for index, bundle in enumerate(bundles):
                    predecessor = bundles[(index - 1) % 3]
                    predecessor_type = item_types[(index - 1) % 3]
                    retained = items[bundle][1 - item_types[index]]
                    incoming = items[predecessor][predecessor_type]
                    totals[bundle] = retained + incoming
                    minima[bundle] = minimum(retained, incoming)
                totals_by_observer.append(totals)
                minima_by_observer.append(minima)

            cycle_edges = {}
            code = "_".join(map(str, specification))
            for observer in range(4):
                for bundle in range(4):
                    own = totals_by_observer[observer][bundle]
                    edge = z3.Bool(f"ye_{code}_{observer}_{bundle}")
                    solver.add(
                        edge
                        == z3.And(
                            own >= floaters[observer],
                            *(
                                own
                                >= totals_by_observer[observer][target]
                                - minima_by_observer[observer][target]
                                for target in range(4)
                                if target != bundle
                            ),
                        )
                    )
                    cycle_edges[observer, bundle] = edge

            for permutation in itertools.permutations(range(4)):
                potential = sum(
                    totals_by_observer[observer][permutation[observer]]
                    for observer in range(4)
                )
                maximality = z3.Implies(
                    z3.And(
                        *(
                            cycle_edges[observer, permutation[observer]]
                            for observer in range(4)
                        )
                    ),
                    potential <= base_potential,
                )
                permutation_code = "".join(map(str, permutation))
                label = f"cycle_{code}_{permutation_code}"
                maximality_records.append((maximality, label))
                if cegar_batch > 0:
                    continue
                if track_core:
                    solver.assert_and_track(maximality, label)
                else:
                    solver.add(maximality)

    if include_pairwise_swaps:
        if singleton_mask != 0 or remainder_multi_mask != 0:
            raise ValueError(
                "pairwise-swap encoding currently requires exactly two goods per bundle"
            )
        selected_swap_specs = (
            swap_specs
            if swap_specs
            else tuple(
                (first_bundle, first_type, second_bundle, second_type)
                for first_bundle, second_bundle in itertools.combinations(range(4), 2)
                for first_type in range(2)
                for second_type in range(2)
            )
        )
        for first_bundle, first_type, second_bundle, second_type in selected_swap_specs:
                    swap_partition_count += 1
                    totals_by_observer = []
                    minima_by_observer = []
                    for observer in range(4):
                        first_items = (
                            selected[observer][first_bundle],
                            remainder_total[observer][first_bundle],
                        )
                        second_items = (
                            selected[observer][second_bundle],
                            remainder_total[observer][second_bundle],
                        )
                        totals = [
                            base_total(observer, bundle) for bundle in range(4)
                        ]
                        minima = [
                            base_minimum(observer, bundle) for bundle in range(4)
                        ]
                        totals[first_bundle] = (
                            first_items[1 - first_type] + second_items[second_type]
                        )
                        minima[first_bundle] = minimum(
                            first_items[1 - first_type], second_items[second_type]
                        )
                        totals[second_bundle] = (
                            second_items[1 - second_type] + first_items[first_type]
                        )
                        minima[second_bundle] = minimum(
                            second_items[1 - second_type], first_items[first_type]
                        )
                        totals_by_observer.append(totals)
                        minima_by_observer.append(minima)

                    swap_edges = {}
                    for observer in range(4):
                        for bundle in range(4):
                            own = totals_by_observer[observer][bundle]
                            edge = z3.Bool(
                                f"se_{first_bundle}_{first_type}_{second_bundle}_"
                                f"{second_type}_{observer}_{bundle}"
                            )
                            solver.add(
                                edge
                                == z3.And(
                                    own >= floaters[observer],
                                    *(
                                        own
                                        >= totals_by_observer[observer][target]
                                        - minima_by_observer[observer][target]
                                        for target in range(4)
                                        if target != bundle
                                    ),
                                )
                            )
                            swap_edges[observer, bundle] = edge

                    for permutation in itertools.permutations(range(4)):
                        potential = sum(
                            totals_by_observer[observer][permutation[observer]]
                            for observer in range(4)
                        )
                        maximality = z3.Implies(
                            z3.And(
                                *(
                                    swap_edges[observer, permutation[observer]]
                                    for observer in range(4)
                                )
                            ),
                            potential <= base_potential,
                        )
                        permutation_code = "".join(map(str, permutation))
                        label = (
                            f"swap_{first_bundle}_{first_type}_{second_bundle}_"
                            f"{second_type}_{permutation_code}"
                        )
                        maximality_records.append((maximality, label))
                        if cegar_batch > 0:
                            continue
                        if track_core:
                            solver.assert_and_track(maximality, label)
                        else:
                            solver.add(maximality)

    cegar_iterations = 0
    maximality_by_label = {label: constraint for constraint, label in maximality_records}
    learned_maximality = []
    for label in seed_blockers:
        solver.add(maximality_by_label[label])
        learned_maximality.append(label)
    while True:
        verdict = solver.check()
        if verdict != z3.sat or cegar_batch <= 0:
            break
        model = solver.model()
        violated = [
            (constraint, label)
            for constraint, label in maximality_records
            if not z3.is_true(model.evaluate(constraint, model_completion=True))
            and label not in learned_maximality
        ]
        if not violated or cegar_iterations >= max_iterations:
            break
        for constraint, label in violated[:cegar_batch]:
            solver.add(constraint)
            learned_maximality.append(label)
        cegar_iterations += 1
    smt2.write_text(solver.to_smt2())
    model = solver.model() if verdict == z3.sat else None
    all_maximality_satisfied = (
        all(
            z3.is_true(model.evaluate(constraint, model_completion=True))
            for constraint, _ in maximality_records
        )
        if verdict == z3.sat
        else None
    )
    artifact = {
        "schema": SCHEMA,
        "status": (
            "SUBSTITUTION_CONVERSION_FORCED"
            if verdict == z3.unsat
            else "AGGREGATE_COUNTEREXAMPLE"
            if verdict == z3.sat and all_maximality_satisfied is True
            else "CEGAR_INCOMPLETE"
            if verdict == z3.sat
            else "UNKNOWN"
        ),
        "meaning": (
            "UNSAT proves that normalized-utilitarian maximality against all "
            "owner-minimum substitutions forces an owner-minimum Hall "
            "completion. SAT must be checked for item-level realizability."
        ),
        "singleton_bundle_labels": [
            bundle for bundle in range(4) if singleton_mask & (1 << bundle)
        ],
        "multi_good_remainder_bundle_labels": (
            [
                bundle
                for bundle in range(4)
                if remainder_multi_mask & (1 << bundle)
            ]
            if remainder_multi_mask is not None
            else None
        ),
        "selected_minimum_mask": selected_minimum_mask,
        "solver_for_qf_lra": solver_for_qf_lra,
        "integer_cap": integer_cap,
        "complete_candidate_count": len(complete_candidates),
        "complete_candidate_blockers_asserted": assert_complete_blockers,
        "hall_witness_encoding": hall_witness_encoding,
        "strict_owner_minima": strict_owner_minima,
        "pair_extraction_lemma_asserted": True,
        "pair_orbit_count": len(orbit_representatives),
        "pair_orbit_index": pair_orbit_index,
        "selected_pair_role": selected_pair_role,
        "trap_witness_prefix": trap_witness_prefix,
        "substitution_partition_count": substitution_count,
        "substitution_allocation_count": substitution_count * 24,
        "one_good_transfers_included": include_one_good_transfers,
        "transfer_partition_count": transfer_partition_count,
        "transfer_allocation_count": transfer_partition_count * 24,
        "cycle_partition_count": cycle_partition_count,
        "cycle_allocation_count": cycle_partition_count * 24,
        "cycle_specs": [list(specification) for specification in cycle_specs],
        "pairwise_swaps_included": include_pairwise_swaps,
        "swap_partition_count": swap_partition_count,
        "swap_allocation_count": swap_partition_count * 24,
        "swap_specs": [list(spec) for spec in swap_specs],
        "substitution_eligibility_factored": True,
        "cegar_batch": cegar_batch,
        "cegar_iterations": cegar_iterations,
        "learned_maximality_blocker_count": len(learned_maximality),
        "learned_maximality_blockers": learned_maximality,
        "all_maximality_constraints_satisfied": all_maximality_satisfied,
        "solver_verdict": str(verdict),
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "unsat_core": (
            [str(label) for label in solver.unsat_core()]
            if verdict == z3.unsat and track_core
            else None
        ),
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
    parser.add_argument("--singleton-mask", type=int, default=0)
    parser.add_argument("--remainder-multi-mask", type=int)
    parser.add_argument("--pair-orbit-index", type=int)
    parser.add_argument("--trap-witness-prefix")
    parser.add_argument("--track-core", action="store_true")
    parser.add_argument("--cegar-batch", type=int, default=0)
    parser.add_argument("--max-iterations", type=int, default=1000)
    parser.add_argument("--seed-blocker-file", type=Path)
    parser.add_argument("--seed-blocker", action="append", default=[])
    parser.add_argument("--include-one-good-transfers", action="store_true")
    parser.add_argument("--cycle-spec", action="append", default=[])
    parser.add_argument("--include-pairwise-swaps", action="store_true")
    parser.add_argument("--swap-spec", action="append", default=[])
    parser.add_argument("--omit-complete-blockers", action="store_true")
    parser.add_argument("--selected-minimum-mask", type=lambda value: int(value, 0), default=0)
    parser.add_argument("--solver-for-qf-lra", action="store_true")
    parser.add_argument("--integer-cap", type=int)
    parser.add_argument("--hall-witness-encoding", action="store_true")
    parser.add_argument("--strict-owner-minima", action="store_true")
    args = parser.parse_args()
    seed_blockers = ()
    if args.seed_blocker_file is not None:
        seed_document = json.loads(args.seed_blocker_file.read_text())
        seed_blockers = tuple(seed_document["learned_maximality_blockers"])
    seed_blockers += tuple(args.seed_blocker)
    swap_specs = tuple(
        tuple(map(int, specification.split(",")))
        for specification in args.swap_spec
    )
    if any(len(specification) != 4 for specification in swap_specs):
        raise ValueError("swap specs must be first_bundle,first_type,second_bundle,second_type")
    cycle_specs = tuple(
        tuple(map(int, specification.split(",")))
        for specification in args.cycle_spec
    )
    if any(len(specification) != 6 for specification in cycle_specs):
        raise ValueError(
            "cycle specs must be first_bundle,first_type,second_bundle,"
            "second_type,third_bundle,third_type"
        )
    print(
        json.dumps(
            run(
                args.output,
                args.smt2,
                args.timeout_seconds,
                args.singleton_mask,
                args.remainder_multi_mask,
                args.pair_orbit_index,
                args.trap_witness_prefix,
                args.track_core,
                args.cegar_batch,
                args.max_iterations,
                seed_blockers,
                args.include_one_good_transfers,
                cycle_specs,
                args.include_pairwise_swaps,
                swap_specs,
                not args.omit_complete_blockers,
                args.selected_minimum_mask,
                args.solver_for_qf_lra,
                args.integer_cap,
                args.hall_witness_encoding,
                args.strict_owner_minima,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
