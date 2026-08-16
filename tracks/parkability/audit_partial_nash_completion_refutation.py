#!/usr/bin/env python3
"""Independent exhaustive audit of a blocked maximum-Nash partial state."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .fast_count import FastParkability
    from .run_partial_nash_cegar import eligible_states
except ImportError:
    import core
    from anneal import atomic_json
    from fast_count import FastParkability
    from run_partial_nash_cegar import eligible_states


SCHEMA = "partial-nash-completion-refutation-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle_value(values, observer: int, bundle) -> int:
    return sum(values[observer][good] for good in bundle)


def bundles_from_owner(owner, n: int):
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(n)
    )


def efx_slacks(values, owner) -> tuple[tuple[int, int, int], ...]:
    bundles = bundles_from_owner(owner, len(values))
    own = tuple(
        bundle_value(values, agent, bundles[agent])
        for agent in range(len(values))
    )
    return tuple(
        (
            observer,
            target,
            own[observer]
            - bundle_value(
                values,
                observer,
                tuple(good for good in bundles[target] if good != removed),
            ),
        )
        for observer in range(len(values))
        for target in range(len(values))
        if observer != target
        for removed in bundles[target]
    )


def insertable_hosts(values, floater: int, owner) -> tuple[int, ...]:
    n = len(values)
    bundles = bundles_from_owner(owner, n)
    own = tuple(
        bundle_value(values, agent, bundles[agent]) for agent in range(n)
    )
    hosts = []
    for host in range(n):
        enlarged = bundles[host] + (floater,)
        if all(
            own[observer]
            >= bundle_value(
                values,
                observer,
                tuple(good for good in enlarged if good != removed),
            )
            for observer in range(n)
            if observer != host
            for removed in enlarged
        ):
            hosts.append(host)
    return tuple(hosts)


def public_partial_state(state: dict) -> dict:
    return {
        "floater": state["floater"],
        "base_owner": list(state["base_owner"]),
        "utilities": list(state["utilities"]),
        "utility_product": state["utility_product"],
        "insertable_hosts": list(state["insertable_hosts"]),
    }


def literal_partial_census(values) -> dict:
    n = len(values)
    m = len(values[0])
    states = []
    assignment_count = 0
    for floater in range(m):
        allocated_goods = tuple(good for good in range(m) if good != floater)
        for choices in itertools.product(range(n), repeat=m - 1):
            assignment_count += 1
            owner: list[int | None] = [None] * m
            for good, agent in zip(allocated_goods, choices):
                owner[good] = agent
            bundles = bundles_from_owner(owner, n)
            utilities = tuple(
                bundle_value(values, agent, bundles[agent])
                for agent in range(n)
            )
            if any(
                utilities[agent] < values[agent][floater]
                for agent in range(n)
            ):
                continue
            if any(slack < 0 for _, _, slack in efx_slacks(values, owner)):
                continue
            states.append(
                {
                    "floater": floater,
                    "base_owner": tuple(owner),
                    "utilities": utilities,
                    "utility_product": math.prod(utilities),
                    "insertable_hosts": insertable_hosts(
                        values,
                        floater,
                        owner,
                    ),
                }
            )
    states.sort(
        key=lambda state: (
            state["utility_product"],
            bool(state["insertable_hosts"]),
            -state["floater"],
            repr(state["base_owner"]),
        ),
        reverse=True,
    )
    return {
        "assignment_count": assignment_count,
        "states": states,
    }


def literal_complete_census(values) -> dict:
    n = len(values)
    m = len(values[0])
    allocations = []
    assignment_count = 0
    for owner in itertools.product(range(n), repeat=m):
        assignment_count += 1
        if all(slack >= 0 for _, _, slack in efx_slacks(values, owner)):
            allocations.append(owner)
    payload = json.dumps(
        [list(owner) for owner in allocations],
        separators=(",", ":"),
    ).encode()
    return {
        "assignment_count": assignment_count,
        "efx_allocation_count": len(allocations),
        "efx_allocations_sha256": hashlib.sha256(payload).hexdigest(),
        "first_efx_allocations": [list(owner) for owner in allocations[:10]],
    }


def candidate_diagnostics(values, candidate, utilities) -> dict:
    floater, owner = candidate
    bundles = bundles_from_owner(owner, len(values))
    witnesses = {}
    for host in range(len(values)):
        enlarged = bundles[host] + (floater,)
        host_witnesses = []
        for observer in range(len(values)):
            if observer == host:
                continue
            for removed in enlarged:
                slack = utilities[observer] - bundle_value(
                    values,
                    observer,
                    tuple(good for good in enlarged if good != removed),
                )
                if slack < 0:
                    host_witnesses.append(
                        {
                            "observer": observer,
                            "removed_good": removed,
                            "slack": slack,
                        }
                    )
        witnesses[str(host)] = host_witnesses
    return {
        "bundles": [list(bundle) for bundle in bundles],
        "efx_min_slack": min(slack for _, _, slack in efx_slacks(values, owner)),
        "floater_nonenvy_slacks": [
            utilities[agent] - values[agent][floater]
            for agent in range(len(values))
        ],
        "insertion_witnesses_by_host": witnesses,
    }


def audit(source: Path, provenance: Path | None = None) -> dict:
    document = json.loads(source.read_text())
    if document.get("schema") != "partial-nash-completion-refutation-profile-v1":
        raise ValueError("source is not the fixed refutation profile")
    values = core.validate_values(
        document["values"],
        expected_n=document["n"],
        expected_m=document["m"],
        lower=1,
    )
    candidate = (
        document["candidate"]["floater"],
        tuple(document["candidate"]["base_owner"]),
    )
    provenance_record = None
    if provenance is not None:
        provenance_document = json.loads(provenance.read_text())
        if (
            provenance_document.get("schema") != "partial-nash-gap-anneal-v1"
            or provenance_document.get("status")
            != "BLOCKED_NASH_MAXIMIZER_COUNTEREXAMPLE"
            or tuple(tuple(row) for row in provenance_document["values"])
            != values
        ):
            raise ValueError("annealing provenance does not match the profile")
        provenance_record = {
            "path": str(provenance),
            "sha256": sha256(provenance),
            "random_seed": provenance_document["random_seed"],
            "discovery_iteration": provenance_document["iterations_completed"],
        }

    literal = literal_partial_census(values)
    states = literal["states"]
    candidate_record = next(
        state
        for state in states
        if (state["floater"], state["base_owner"]) == candidate
    )
    maximum_product = states[0]["utility_product"]
    maximizers = [
        state for state in states if state["utility_product"] == maximum_product
    ]
    if len(maximizers) != 1 or maximizers[0] is not candidate_record:
        raise AssertionError("candidate is not the unique literal Nash maximizer")
    if candidate_record["insertable_hosts"]:
        raise AssertionError("candidate unexpectedly permits insertion")
    second_product = next(
        state["utility_product"]
        for state in states
        if state["utility_product"] < maximum_product
    )

    core_states = eligible_states(values)
    core_maximum = max(state["nash"] for state in core_states)
    core_maximizers = [
        state for state in core_states if state["nash"] == core_maximum
    ]
    if (
        len(core_states) != len(states)
        or len(core_maximizers) != 1
        or core_maximizers[0]["identity"] != candidate
        or core_maximizers[0]["parkable_hosts"]
    ):
        raise AssertionError("core iterator disagrees with literal enumeration")

    vectorized = FastParkability(document["n"], document["m"]).partial_pareto_landscape(
        values
    )
    if (
        vectorized["eligible_base_count"] != len(states)
        or vectorized["maximum_product"] != maximum_product
        or vectorized["maximum_product_vector_count"] != 1
        or vectorized["maximum_product_has_insertable_realization"]
    ):
        raise AssertionError("vectorized landscape disagrees with literal audit")

    complete = literal_complete_census(values)
    core_complete_count = sum(1 for _ in core.iter_efx0_assignments(values))
    if complete["efx_allocation_count"] != core_complete_count:
        raise AssertionError("complete-EFX enumerators disagree")
    row_totals = tuple(map(sum, values))
    normalized_nash = math.prod(
        Fraction(candidate_record["utilities"][agent], row_totals[agent])
        for agent in range(document["n"])
    )
    canonical_states = [public_partial_state(state) for state in states]
    return {
        "schema": SCHEMA,
        "status": "EXACT_BLOCKED_UNIQUE_MAXIMUM_NASH_STATE",
        "meaning": (
            "The fixed candidate is the unique maximum-product state among "
            "every eligible one-floater EFX allocation and no host accepts "
            "its floater. The same profile has complete EFX allocations."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "discovery_provenance": provenance_record,
        "values": [list(row) for row in values],
        "partial_assignment_universe_count": literal["assignment_count"],
        "eligible_partial_state_count": len(states),
        "distinct_eligible_utility_vector_count": len(
            {state["utilities"] for state in states}
        ),
        "maximum_product": maximum_product,
        "second_largest_product": second_product,
        "maximum_product_gap": maximum_product - second_product,
        "maximum_product_state_count": len(maximizers),
        "candidate": public_partial_state(candidate_record),
        "candidate_normalized_nash": {
            "numerator": normalized_nash.numerator,
            "denominator": normalized_nash.denominator,
        },
        "candidate_diagnostics": candidate_diagnostics(
            values,
            candidate,
            candidate_record["utilities"],
        ),
        "independent_enumerators": {
            "literal_partial": "PASS",
            "core_partial": "PASS",
            "vectorized_partial": "PASS",
            "literal_complete": "PASS",
            "core_complete": "PASS",
        },
        "eligible_states": canonical_states,
        "complete_efx": complete,
        "claim_boundary": (
            "This refutes the partial-EFX maximum-Nash direct-completion "
            "conjecture. It does not refute complete additive EFX: the profile "
            "has complete EFX allocations."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("results/partial_nash_completion_refutation_profile.json"),
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=Path("results/partial_nash_gap_anneal_seed211.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source, args.provenance)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
