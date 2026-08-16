#!/usr/bin/env python3
"""Independent exhaustive audit of the source-completion selector refutation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .audit_partial_nash_one_transfer_refutation import (
        bundles_from_owner,
        bundle_value,
        classify_partial,
        insertion_witnesses,
        literal_complete_census,
        literal_partial_census,
        public_state,
    )
    from .fast_count import FastParkability
    from .run_partial_nash_cegar import eligible_states
    from .scan_partial_nash_source_completion import source_completion_landscape
except ImportError:
    import core
    from anneal import atomic_json
    from audit_partial_nash_one_transfer_refutation import (
        bundles_from_owner,
        bundle_value,
        classify_partial,
        insertion_witnesses,
        literal_complete_census,
        literal_partial_census,
        public_state,
    )
    from fast_count import FastParkability
    from run_partial_nash_cegar import eligible_states
    from scan_partial_nash_source_completion import source_completion_landscape


SCHEMA = "partial-nash-source-completion-refutation-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_profile(document: dict) -> tuple[tuple[int, ...], ...]:
    if document.get("schema") != "partial-nash-source-completion-refutation-profile-v1":
        raise ValueError("source is not a fixed source-completion profile")
    n = document.get("n")
    m = document.get("m")
    values = document.get("values")
    if type(n) is not int or type(m) is not int or n < 1 or m < 1:
        raise ValueError("profile dimensions must be positive integers")
    if not isinstance(values, list) or len(values) != n:
        raise ValueError("profile must contain one row per agent")
    if any(not isinstance(row, list) or len(row) != m for row in values):
        raise ValueError("profile rows must have length m")
    if any(type(value) is not int or value <= 0 for row in values for value in row):
        raise ValueError("profile values must be positive integers")
    return tuple(tuple(row) for row in values)


def literal_source_hosts(values, owner) -> tuple[tuple[int, ...], dict]:
    n = len(values)
    bundles = bundles_from_owner(owner, n)
    utilities = tuple(
        bundle_value(values, agent, bundles[agent]) for agent in range(n)
    )
    slacks = {
        str(host): [
            {
                "observer": observer,
                "slack": utilities[observer]
                - bundle_value(values, observer, bundles[host]),
            }
            for observer in range(n)
            if observer != host
        ]
        for host in range(n)
    }
    sources = tuple(
        host
        for host in range(n)
        if all(record["slack"] >= 0 for record in slacks[str(host)])
    )
    return sources, slacks


def rematched_owner(bundles, permutation, floater: int, m: int):
    owner: list[int | None] = [None] * m
    for agent, bundle_index in enumerate(permutation):
        for good in bundles[bundle_index]:
            if owner[good] is not None:
                raise AssertionError("source-rematched bundles overlap")
            owner[good] = agent
    if owner[floater] is not None or any(
        assigned is None for good, assigned in enumerate(owner) if good != floater
    ):
        raise AssertionError("source rematching is not a one-floater state")
    return tuple(owner)


def literal_source_substitutions(values, candidate) -> dict:
    floater, owner = candidate
    n = len(values)
    m = len(values[0])
    bundles = bundles_from_owner(owner, n)
    sources, source_slacks = literal_source_hosts(values, owner)
    records = []
    identities = set()
    for source in sources:
        for removed in bundles[source]:
            modified = list(bundles)
            modified[source] = tuple(
                good for good in bundles[source] if good != removed
            ) + (floater,)
            for permutation in itertools.permutations(range(n)):
                successor_owner = rematched_owner(
                    modified,
                    permutation,
                    removed,
                    m,
                )
                identity = (removed, successor_owner)
                if identity in identities:
                    raise AssertionError("duplicate source-substitution state")
                identities.add(identity)
                state = classify_partial(values, removed, successor_owner)
                records.append(
                    {
                        "source_host": source,
                        "removed_good": removed,
                        "permutation": list(permutation),
                        "floater": removed,
                        "base_owner": list(successor_owner),
                        "utilities": list(state["utilities"]),
                        "utility_product": state["utility_product"],
                        "base_min_efx_slack": state["efx_min_slack"],
                        "floater_nonenvy_slacks": list(
                            state["floater_nonenvy_slacks"]
                        ),
                        "eligible": state["eligible"],
                        "insertable_hosts": list(state["insertable_hosts"]),
                    }
                )
    records.sort(
        key=lambda record: (
            record["source_host"],
            record["removed_good"],
            record["permutation"],
        )
    )
    payload = json.dumps(records, separators=(",", ":"), sort_keys=True).encode()
    failure_counts = Counter()
    for record in records:
        efx = record["base_min_efx_slack"] >= 0
        floater_nonenvy = min(record["floater_nonenvy_slacks"]) >= 0
        if not efx:
            failure_counts["partial_efx_failure_count"] += 1
        if not floater_nonenvy:
            failure_counts["floater_nonenvy_failure_count"] += 1
        if not efx and not floater_nonenvy:
            failure_counts["both_failure_count"] += 1
    return {
        "source_hosts": list(sources),
        "source_host_slacks": source_slacks,
        "generated_state_count": len(records),
        "distinct_state_count": len(identities),
        "eligible_state_count": sum(record["eligible"] for record in records),
        "insertable_eligible_state_count": sum(
            record["eligible"] and bool(record["insertable_hosts"])
            for record in records
        ),
        "failure_counts": dict(sorted(failure_counts.items())),
        "records_sha256": hashlib.sha256(payload).hexdigest(),
        "records": records,
    }


def audit(source: Path) -> dict:
    document = json.loads(source.read_text())
    values = validate_profile(document)
    n = document["n"]
    m = document["m"]
    candidate = (
        document["candidate"]["floater"],
        tuple(document["candidate"]["base_owner"]),
    )
    floater, owner = candidate
    if (
        len(owner) != m
        or owner[floater] is not None
        or any(
            type(assigned) is not int or not 0 <= assigned < n
            for good, assigned in enumerate(owner)
            if good != floater
        )
    ):
        raise ValueError("candidate owner vector is malformed")

    provenance = document["discovery_provenance"]
    provenance_path = Path(provenance["path"])
    if sha256(provenance_path) != provenance["sha256"]:
        raise AssertionError("discovery provenance hash mismatch")
    provenance_document = json.loads(provenance_path.read_text())
    if (
        provenance_document.get("schema")
        != "partial-nash-source-completion-anneal-v1"
        or provenance_document.get("status")
        != "SOURCE_COMPLETION_COUNTEREXAMPLE"
        or provenance_document.get("random_seed") != provenance["random_seed"]
        or provenance_document.get("iterations_completed")
        != provenance["discovery_iteration"]
        or tuple(tuple(row) for row in provenance_document.get("values", ()))
        != values
    ):
        raise AssertionError("discovery provenance content mismatch")

    literal = literal_partial_census(values)
    states = literal["states"]
    by_identity = {
        (state["floater"], state["base_owner"]): state for state in states
    }
    candidate_record = by_identity.get(candidate)
    if candidate_record is None:
        raise AssertionError("candidate is not eligible")
    maximum_product = states[0]["utility_product"]
    maximizers = [
        state for state in states if state["utility_product"] == maximum_product
    ]
    if len(maximizers) != 1 or maximizers[0] is not candidate_record:
        raise AssertionError("candidate is not the unique maximum-product state")
    if candidate_record["insertable_hosts"]:
        raise AssertionError("candidate unexpectedly permits direct insertion")
    second_product = next(
        state["utility_product"]
        for state in states
        if state["utility_product"] < maximum_product
    )

    substitutions = literal_source_substitutions(values, candidate)
    if substitutions["source_hosts"] != [1, 2]:
        raise AssertionError("literal source hosts disagree with the profile")
    if (
        substitutions["generated_state_count"] != 120
        or substitutions["distinct_state_count"] != 120
        or substitutions["eligible_state_count"] != 0
        or substitutions["insertable_eligible_state_count"] != 0
    ):
        raise AssertionError("source-substitution refutation did not replay")

    core_state_list = eligible_states(values)
    core_by_identity = {state["identity"]: state for state in core_state_list}
    if set(core_by_identity) != set(by_identity):
        raise AssertionError("literal and core eligible-state universes disagree")
    for identity, state in by_identity.items():
        if (
            core_by_identity[identity]["utilities"] != state["utilities"]
            or tuple(core_by_identity[identity]["parkable_hosts"])
            != state["insertable_hosts"]
        ):
            raise AssertionError("literal and core state classifications disagree")

    vectorized = FastParkability(n, m).partial_linear_potential_landscape(
        values,
        potential="normalized_nash",
    )
    if (
        vectorized["eligible_base_count"] != len(states)
        or vectorized["maximizer_count"] != 1
        or vectorized["maximizers"][0]["floater"] != floater
        or vectorized["maximizers"][0]["utilities"]
        != list(candidate_record["utilities"])
        or vectorized["maximizers"][0]["insertable"]
    ):
        raise AssertionError("vectorized maximum-Nash landscape disagrees")
    core_source = source_completion_landscape(values, floater, owner)
    if (
        core_source["source_hosts"] != substitutions["source_hosts"]
        or core_source["generated_rematching_count"] != 120
        or core_source["distinct_rematched_state_count"] != 120
        or core_source["eligible_rematched_state_count"] != 0
        or core_source["insertable_eligible_rematched_state_count"] != 0
    ):
        raise AssertionError("core and literal source-substitution censuses disagree")

    complete = literal_complete_census(values)
    core_complete = tuple(core.iter_efx0_assignments(values))
    if complete["efx_allocation_count"] != len(core_complete):
        raise AssertionError("complete-EFX enumerators disagree")
    core_payload = json.dumps(
        [list(allocation) for allocation in core_complete],
        separators=(",", ":"),
    ).encode()
    if hashlib.sha256(core_payload).hexdigest() != complete["efx_allocations_sha256"]:
        raise AssertionError("complete-EFX allocation lists disagree")

    return {
        "schema": SCHEMA,
        "status": "EXACT_MAXIMUM_NASH_SOURCE_COMPLETION_REFUTATION",
        "meaning": (
            "The fixed eligible state uniquely maximizes own-utility product, "
            "is directly blocked, and none of the 120 states obtained from "
            "a source-good substitution and bundle permutation is eligible."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "discovery_provenance": provenance,
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
        "candidate": public_state(candidate_record),
        "candidate_diagnostics": {
            "bundles": [
                list(bundle) for bundle in bundles_from_owner(owner, n)
            ],
            "floater_nonenvy_slacks": list(
                candidate_record["floater_nonenvy_slacks"]
            ),
            "efx_min_slack": candidate_record["efx_min_slack"],
            "insertion_witnesses_by_host": insertion_witnesses(
                values, candidate_record
            ),
        },
        "source_substitution_census": substitutions,
        "independent_enumerators": {
            "literal_partial": "PASS",
            "core_partial": "PASS",
            "vectorized_partial": "PASS",
            "literal_source_substitutions": "PASS",
            "core_source_substitutions": "PASS",
            "literal_complete": "PASS",
            "core_complete": "PASS",
        },
        "eligible_states": [public_state(state) for state in states],
        "complete_efx": complete,
        "claim_boundary": (
            "This refutes direct completion by one source-good substitution "
            "and bundle permutation from a maximum-Nash eligible state. It "
            "does not refute complete additive EFX: the profile has complete "
            "EFX allocations."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "results/partial_nash_source_completion_refutation_profile.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
