#!/usr/bin/env python3
"""Independent exhaustive audit of the maximum-Nash one-transfer refutation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
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


SCHEMA = "partial-nash-one-transfer-refutation-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_profile(document: dict) -> tuple[tuple[int, ...], ...]:
    if document.get("schema") != "partial-nash-one-transfer-refutation-profile-v1":
        raise ValueError("source is not a fixed one-transfer refutation profile")
    n = document.get("n")
    m = document.get("m")
    values = document.get("values")
    if type(n) is not int or type(m) is not int or n < 1 or m < 1:
        raise ValueError("profile dimensions must be positive integers")
    if not isinstance(values, list) or len(values) != n:
        raise ValueError("profile must contain one value row per agent")
    if any(not isinstance(row, list) or len(row) != m for row in values):
        raise ValueError("profile value rows must have length m")
    if any(type(value) is not int or value <= 0 for row in values for value in row):
        raise ValueError("profile values must be positive integers")
    return tuple(tuple(row) for row in values)


def bundles_from_owner(owner, n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(n)
    )


def bundle_value(values, observer: int, bundle) -> int:
    return sum(values[observer][good] for good in bundle)


def efx_slacks(values, owner) -> tuple[tuple[int, int, int, int], ...]:
    bundles = bundles_from_owner(owner, len(values))
    utilities = tuple(
        bundle_value(values, agent, bundles[agent])
        for agent in range(len(values))
    )
    return tuple(
        (
            observer,
            target,
            removed,
            utilities[observer]
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
    utilities = tuple(
        bundle_value(values, agent, bundles[agent]) for agent in range(n)
    )
    hosts = []
    for host in range(n):
        enlarged = bundles[host] + (floater,)
        if all(
            utilities[observer]
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


def classify_partial(values, floater: int, owner) -> dict:
    n = len(values)
    bundles = bundles_from_owner(owner, n)
    utilities = tuple(
        bundle_value(values, agent, bundles[agent]) for agent in range(n)
    )
    floater_slacks = tuple(
        utilities[agent] - values[agent][floater] for agent in range(n)
    )
    slacks = efx_slacks(values, owner)
    eligible = min(floater_slacks) >= 0 and all(
        slack >= 0 for _, _, _, slack in slacks
    )
    hosts = insertable_hosts(values, floater, owner) if eligible else ()
    return {
        "floater": floater,
        "base_owner": tuple(owner),
        "utilities": utilities,
        "utility_product": math.prod(utilities),
        "floater_nonenvy_slacks": floater_slacks,
        "efx_min_slack": min((slack for _, _, _, slack in slacks), default=0),
        "eligible": eligible,
        "insertable_hosts": hosts,
    }


def eligible_partial_state(values, floater: int, owner) -> dict | None:
    n = len(values)
    bundles = bundles_from_owner(owner, n)
    utilities = tuple(
        bundle_value(values, agent, bundles[agent]) for agent in range(n)
    )
    floater_slacks = tuple(
        utilities[agent] - values[agent][floater] for agent in range(n)
    )
    if min(floater_slacks) < 0:
        return None
    minimum = None
    for observer in range(n):
        for target in range(n):
            if observer == target:
                continue
            for removed in bundles[target]:
                slack = utilities[observer] - bundle_value(
                    values,
                    observer,
                    tuple(
                        good for good in bundles[target] if good != removed
                    ),
                )
                if slack < 0:
                    return None
                minimum = slack if minimum is None else min(minimum, slack)
    return {
        "floater": floater,
        "base_owner": tuple(owner),
        "utilities": utilities,
        "utility_product": math.prod(utilities),
        "floater_nonenvy_slacks": floater_slacks,
        "efx_min_slack": minimum if minimum is not None else 0,
        "eligible": True,
        "insertable_hosts": insertable_hosts(values, floater, owner),
    }


def literal_partial_census(values) -> dict:
    n = len(values)
    m = len(values[0])
    states = []
    checked = 0
    for floater in range(m):
        allocated = tuple(good for good in range(m) if good != floater)
        for choices in itertools.product(range(n), repeat=m - 1):
            checked += 1
            owner: list[int | None] = [None] * m
            for good, assigned in zip(allocated, choices):
                owner[good] = assigned
            state = eligible_partial_state(values, floater, owner)
            if state is not None:
                states.append(state)
    states.sort(
        key=lambda state: (
            -state["utility_product"],
            state["floater"],
            repr(state["base_owner"]),
        )
    )
    return {"assignment_count": checked, "states": states}


def owner_distance(left, right, floater: int) -> int:
    return sum(
        left[good] != right[good]
        for good in range(len(left))
        if good != floater
    )


def literal_local_neighborhood(values, candidate) -> dict:
    floater, base_owner = candidate
    records = []
    base_record = classify_partial(values, floater, base_owner)
    records.append({"changed_good": None, "new_owner": None, **base_record})
    for good, old_owner in enumerate(base_owner):
        if good == floater:
            continue
        for new_owner in range(len(values)):
            if new_owner == old_owner:
                continue
            neighbor = list(base_owner)
            neighbor[good] = new_owner
            records.append(
                {
                    "changed_good": good,
                    "new_owner": new_owner,
                    **classify_partial(values, floater, neighbor),
                }
            )
    if len(records) != 1 + (len(base_owner) - 1) * (len(values) - 1):
        raise AssertionError("one-transfer neighborhood has the wrong size")
    return {
        "state_count": len(records),
        "eligible_state_count": sum(record["eligible"] for record in records),
        "eligible_insertable_state_count": sum(
            record["eligible"] and bool(record["insertable_hosts"])
            for record in records
        ),
        "records": records,
    }


def literal_complete_census(values) -> dict:
    n = len(values)
    m = len(values[0])
    allocations = []
    for owner in itertools.product(range(n), repeat=m):
        bundles = bundles_from_owner(owner, n)
        utilities = tuple(
            bundle_value(values, agent, bundles[agent]) for agent in range(n)
        )
        valid = True
        for observer in range(n):
            if not valid:
                break
            for target in range(n):
                if observer == target:
                    continue
                for removed in bundles[target]:
                    if utilities[observer] < bundle_value(
                        values,
                        observer,
                        tuple(
                            good
                            for good in bundles[target]
                            if good != removed
                        ),
                    ):
                        valid = False
                        break
                if not valid:
                    break
        if valid:
            allocations.append(owner)
    payload = json.dumps(
        [list(owner) for owner in allocations], separators=(",", ":")
    ).encode()
    return {
        "assignment_count": n**m,
        "efx_allocation_count": len(allocations),
        "efx_allocations_sha256": hashlib.sha256(payload).hexdigest(),
        "first_efx_allocations": [list(owner) for owner in allocations[:10]],
    }


def insertion_witnesses(values, candidate_record) -> dict:
    floater = candidate_record["floater"]
    owner = candidate_record["base_owner"]
    utilities = candidate_record["utilities"]
    bundles = bundles_from_owner(owner, len(values))
    witnesses = {}
    for host in range(len(values)):
        enlarged = bundles[host] + (floater,)
        failures = []
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
                    failures.append(
                        {
                            "observer": observer,
                            "removed_good": removed,
                            "slack": slack,
                        }
                    )
        witnesses[str(host)] = failures
    return witnesses


def public_state(state: dict, *, distance: int | None = None) -> dict:
    result = {
        "floater": state["floater"],
        "base_owner": list(state["base_owner"]),
        "utilities": list(state["utilities"]),
        "utility_product": state["utility_product"],
        "insertable_hosts": list(state["insertable_hosts"]),
    }
    if distance is not None:
        result["owner_hamming_distance"] = distance
    return result


def public_local_record(record: dict) -> dict:
    return {
        "changed_good": record["changed_good"],
        "new_owner": record["new_owner"],
        "base_owner": list(record["base_owner"]),
        "utilities": list(record["utilities"]),
        "utility_product": record["utility_product"],
        "floater_nonenvy_slacks": list(record["floater_nonenvy_slacks"]),
        "efx_min_slack": record["efx_min_slack"],
        "eligible": record["eligible"],
        "insertable_hosts": list(record["insertable_hosts"]),
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
    floater, base_owner = candidate
    if (
        len(base_owner) != m
        or base_owner[floater] is not None
        or any(
            type(owner) is not int or not 0 <= owner < n
            for good, owner in enumerate(base_owner)
            if good != floater
        )
    ):
        raise ValueError("candidate owner vector is malformed")

    provenance = document.get("discovery_provenance")
    provenance_path = Path(provenance["path"])
    if sha256(provenance_path) != provenance["sha256"]:
        raise AssertionError("discovery provenance hash mismatch")
    provenance_document = json.loads(provenance_path.read_text())
    if (
        provenance_document.get("discovery_random_seed")
        != provenance["random_seed"]
        or provenance_document.get("discovery_iteration")
        != provenance["discovery_iteration"]
        or tuple(tuple(row) for row in provenance_document.get("values", ()))
        != values
    ):
        raise AssertionError("discovery provenance content mismatch")

    literal = literal_partial_census(values)
    states = literal["states"]
    identities = {
        (state["floater"], state["base_owner"]): state for state in states
    }
    candidate_record = identities.get(candidate)
    if candidate_record is None:
        raise AssertionError("candidate is not an eligible partial state")
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

    local = literal_local_neighborhood(values, candidate)
    local_eligible_identities = {
        (record["floater"], record["base_owner"])
        for record in local["records"]
        if record["eligible"]
    }
    global_local_identities = {
        identity
        for identity in identities
        if identity[0] == floater
        and owner_distance(identity[1], base_owner, floater) <= 1
    }
    if local_eligible_identities != global_local_identities:
        raise AssertionError("local and global literal enumerations disagree")
    if local["eligible_insertable_state_count"]:
        raise AssertionError("one-transfer repair unexpectedly exists")

    same_floater_insertable = [
        (
            owner_distance(state["base_owner"], base_owner, floater),
            state,
        )
        for state in states
        if state["floater"] == floater and state["insertable_hosts"]
    ]
    if not same_floater_insertable:
        raise AssertionError("candidate has no same-floater completion at any radius")
    nearest_distance = min(distance for distance, _ in same_floater_insertable)
    nearest = [
        state
        for distance, state in same_floater_insertable
        if distance == nearest_distance
    ]
    if nearest_distance <= 1:
        raise AssertionError("nearest completion is not beyond one transfer")

    core_state_list = eligible_states(values)
    core_by_identity = {state["identity"]: state for state in core_state_list}
    if set(core_by_identity) != set(identities):
        raise AssertionError("core and literal eligible-state universes disagree")
    for identity, literal_state in identities.items():
        core_state = core_by_identity[identity]
        if (
            core_state["utilities"] != literal_state["utilities"]
            or tuple(core_state["parkable_hosts"])
            != literal_state["insertable_hosts"]
        ):
            raise AssertionError("core and literal state classifications disagree")

    evaluator = FastParkability(n, m)
    vectorized_radius_three = evaluator.partial_pareto_landscape(
        values,
        completion_radius=3,
    )
    if (
        vectorized_radius_three["eligible_base_count"] != len(states)
        or vectorized_radius_three["maximum_product"] != maximum_product
        or vectorized_radius_three["maximum_product_vector_count"] != 1
        or vectorized_radius_three[
            "maximum_product_has_insertable_realization"
        ]
        or vectorized_radius_three[
            "maximum_product_completion_within_radius"
        ]
        or vectorized_radius_three["maximum_product_completion_target_count"]
        != 0
    ):
        raise AssertionError("vectorized radius-three landscape disagrees")
    vectorized_radius_four = evaluator.partial_pareto_landscape(
        values,
        completion_radius=4,
    )
    if (
        not vectorized_radius_four[
            "maximum_product_completion_within_radius"
        ]
        or vectorized_radius_four["maximum_product_completion_target_count"]
        != len(nearest)
        or vectorized_radius_four["nearest_maximum_product_completion"][
            "distance"
        ]
        != nearest_distance
    ):
        raise AssertionError("vectorized radius-four landscape disagrees")

    complete = literal_complete_census(values)
    core_complete = tuple(core.iter_efx0_assignments(values))
    if complete["efx_allocation_count"] != len(core_complete):
        raise AssertionError("complete-EFX enumerators disagree")
    core_payload = json.dumps(
        [list(owner) for owner in core_complete], separators=(",", ":")
    ).encode()
    if hashlib.sha256(core_payload).hexdigest() != complete["efx_allocations_sha256"]:
        raise AssertionError("complete-EFX allocation lists disagree")

    return {
        "schema": SCHEMA,
        "status": "EXACT_MAXIMUM_NASH_LOCAL_RADIUS_THREE_REFUTATION",
        "meaning": (
            "The fixed eligible partial state uniquely maximizes own-utility "
            "product, is directly blocked, is isolated under eligible "
            "same-floater one-good transfers, and has no same-floater "
            "eligible completion within three good-owner changes."
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
                list(bundle) for bundle in bundles_from_owner(base_owner, n)
            ],
            "floater_nonenvy_slacks": list(
                candidate_record["floater_nonenvy_slacks"]
            ),
            "efx_min_slack": candidate_record["efx_min_slack"],
            "insertion_witnesses_by_host": insertion_witnesses(
                values, candidate_record
            ),
        },
        "one_transfer_neighborhood": {
            "scope": (
                "same floater; owner Hamming distance at most one over the "
                "eight allocated goods"
            ),
            "raw_state_count": local["state_count"],
            "eligible_state_count": local["eligible_state_count"],
            "eligible_insertable_state_count": local[
                "eligible_insertable_state_count"
            ],
            "records": [
                public_local_record(record) for record in local["records"]
            ],
        },
        "nearest_same_floater_completion": {
            "owner_hamming_distance": nearest_distance,
            "state_count_at_distance": len(nearest),
            "states": [
                public_state(state, distance=nearest_distance)
                for state in sorted(
                    nearest,
                    key=lambda state: (
                        -state["utility_product"],
                        repr(state["base_owner"]),
                    ),
                )
            ],
        },
        "independent_enumerators": {
            "literal_partial_global": "PASS",
            "literal_partial_local": "PASS",
            "core_partial": "PASS",
            "vectorized_radius_three": "PASS",
            "vectorized_radius_four": "PASS",
            "literal_complete": "PASS",
            "core_complete": "PASS",
        },
        "eligible_states": [public_state(state) for state in states],
        "complete_efx": complete,
        "claim_boundary": (
            "This refutes the same-floater one-good-transfer repair of the "
            "maximum-Nash direct-completion selector and every same-floater "
            "direct-completion radius at most three. It does not refute "
            "complete additive EFX: this profile has complete EFX allocations."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "results/partial_nash_one_transfer_refutation_profile.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
