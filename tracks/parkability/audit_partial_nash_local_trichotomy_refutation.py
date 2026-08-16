#!/usr/bin/env python3
"""Exact replay of the local bundle-cycle/source-substitution refutation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_partial_nash_cegar import (
        bundles,
        eligible_states,
        source_substitution_rivals,
        state_identity,
    )
except ImportError:
    from anneal import atomic_json
    from run_partial_nash_cegar import (
        bundles,
        eligible_states,
        source_substitution_rivals,
        state_identity,
    )


SCHEMA = "partial-nash-local-trichotomy-refutation-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle_value(values, observer: int, bundle) -> int:
    return sum(values[observer][good] for good in bundle)


def strict_envy_cycles(values, candidate):
    candidate_bundles = bundles(candidate[1], len(values))
    utilities = tuple(
        bundle_value(values, agent, candidate_bundles[agent])
        for agent in range(len(values))
    )
    edges = {
        (observer, target)
        for observer in range(len(values))
        for target in range(len(values))
        if observer != target
        and bundle_value(values, observer, candidate_bundles[target])
        > utilities[observer]
    }
    cycles = []
    for length in range(2, len(values) + 1):
        for cycle in itertools.permutations(range(len(values)), length):
            if cycle[0] != min(cycle):
                continue
            if all(
                (cycle[index], cycle[(index + 1) % length]) in edges
                for index in range(length)
            ):
                cycles.append(cycle)
    return edges, cycles


def public_fraction(value) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def public_state(record: dict) -> dict:
    identity = record["identity"]
    return {
        "floater": identity[0],
        "base_owner": list(identity[1]),
        "utilities": list(record["utilities"]),
        "parkable_hosts": list(record["parkable_hosts"]),
        "nash": public_fraction(record["nash"]),
    }


def audit(source: Path) -> dict:
    document = json.loads(source.read_text())
    if document.get("status") != "ITERATION_LIMIT" or len(document["trace"]) != 1:
        raise ValueError("source must contain the single SAT local model")
    values = tuple(tuple(row) for row in document["trace"][0]["values"])
    candidate = state_identity(
        document["candidate"]["floater"],
        document["candidate"]["base_owner"],
    )
    states = eligible_states(values)
    by_identity = {record["identity"]: record for record in states}
    candidate_record = by_identity[candidate]
    if candidate_record["parkable_hosts"]:
        raise AssertionError("candidate is not all-host blocked")
    candidate_bundles = bundles(candidate[1], len(values))
    source_hosts = tuple(
        host
        for host in range(len(values))
        if all(
            candidate_record["utilities"][observer]
            >= bundle_value(values, observer, candidate_bundles[host])
            for observer in range(len(values))
            if observer != host
        )
    )
    if 0 not in source_hosts:
        raise AssertionError("fixed source host 0 is not unenvied")
    envy_edges, cycles = strict_envy_cycles(values, candidate)
    if cycles:
        raise AssertionError("candidate has a strict bundle-envy cycle")

    substitutions = {
        rival
        for host in range(len(values))
        for rival in source_substitution_rivals(candidate, len(values), host)
    }
    eligible_substitutions = [
        by_identity[rival]
        for rival in substitutions
        if rival in by_identity
    ]
    improving_substitutions = [
        rival
        for rival in eligible_substitutions
        if rival["nash"] > candidate_record["nash"]
    ]
    equal_insertable_substitutions = [
        rival
        for rival in eligible_substitutions
        if rival["nash"] == candidate_record["nash"]
        and rival["parkable_hosts"]
    ]
    if improving_substitutions or equal_insertable_substitutions:
        raise AssertionError("a forbidden source substitution survived")

    global_violations = [
        record
        for record in states
        if record["identity"] != candidate
        and (
            record["nash"] > candidate_record["nash"]
            or (
                record["nash"] == candidate_record["nash"]
                and record["parkable_hosts"]
            )
        )
    ]
    if len(global_violations) != document["trace"][0]["violating_rival_count"]:
        raise AssertionError("global rival count changed")
    global_violations.sort(key=lambda record: record["nash"], reverse=True)
    return {
        "schema": SCHEMA,
        "status": "EXACT_LOCAL_TRICHOTOMY_REFUTATION",
        "meaning": (
            "The candidate is eligible, all-host blocked, has no strict bundle "
            "cycle, and has no Nash-improving eligible source substitution "
            "rematching. It is not a maximum-Nash counterexample because many "
            "other eligible states have larger Nash product."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "values": [list(row) for row in values],
        "candidate": public_state(candidate_record),
        "source_hosts": list(source_hosts),
        "strict_envy_edges": [list(edge) for edge in sorted(envy_edges)],
        "strict_envy_cycle_count": len(cycles),
        "source_substitution_identity_count": len(substitutions),
        "eligible_source_substitution_count": len(eligible_substitutions),
        "improving_source_substitution_count": len(improving_substitutions),
        "equal_insertable_source_substitution_count": len(
            equal_insertable_substitutions
        ),
        "global_eligible_state_count": len(states),
        "global_violating_rival_count": len(global_violations),
        "largest_global_rival": public_state(global_violations[0]),
        "claim_boundary": (
            "This refutes the local cycle-or-source-substitution trichotomy. "
            "It does not refute maximum-Nash completion or complete additive EFX."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("results/partial_nash_local_trichotomy_source0_session1.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
