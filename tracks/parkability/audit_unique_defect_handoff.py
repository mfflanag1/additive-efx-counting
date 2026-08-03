#!/usr/bin/env python3
"""Audit the unique-defect handoff pattern in the exact plateau corpus."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .scan_charity_threshold_absorption import (
        absorption_signature,
        eligible,
        tables,
    )
    from .scan_partial_nash_potential import matrices
except ImportError:
    from anneal import atomic_json
    from scan_charity_threshold_absorption import absorption_signature, eligible, tables
    from scan_partial_nash_potential import matrices


SCHEMA = "unique-defect-handoff-audit-v1"


def values_sha256(values):
    return hashlib.sha256(
        json.dumps(values, separators=(",", ":")).encode()
    ).hexdigest()


def load_record_values(record):
    for _key, values in matrices(Path(record["source"])):
        if values_sha256(values) == record["values_sha256"]:
            return tuple(values)
    raise ValueError(f"cannot reconstruct {record['source']}")


def candidate_slacks(masks, floater, witness, totals, thresholds, row_totals):
    complete = list(masks)
    complete[witness["host"]] |= 1 << floater
    permutation = witness["permutation"]
    slacks = []
    for agent in range(len(masks)):
        assigned = permutation[agent]
        right = max(
            thresholds[agent][complete[target]]
            for target in range(len(masks))
            if target != assigned
        )
        slacks.append(
            Fraction(totals[agent][complete[assigned]] - right, row_totals[agent])
        )
    return tuple(slacks)


def run(source, output):
    if output.exists():
        raise ValueError("output must be new")
    document = json.loads(source.read_text())
    selected_count = 0
    unique_defect_count = 0
    canonical_count = 0
    verified_count = 0
    exceptions = []
    for profile in document["records"]:
        values = load_record_values(profile)
        totals, thresholds = tables(values)
        row_totals = tuple(sum(row) for row in values)
        for transition in profile.get("selected_transitions", ()):
            selected_count += 1
            if transition.get("strict_hall_margin_swap_path_length") != 1:
                continue
            blocked_masks = tuple(transition["blocked_masks"])
            old_floater = transition["blocked_floater"]
            signature, witness = absorption_signature(
                blocked_masks,
                1 << old_floater,
                totals,
                thresholds,
                row_totals,
            )
            slacks = candidate_slacks(
                blocked_masks,
                old_floater,
                witness,
                totals,
                thresholds,
                row_totals,
            )
            if tuple(witness["permutation"]) != tuple(range(len(values))):
                continue
            negative_agents = [agent for agent, slack in enumerate(slacks) if slack < 0]
            if len(negative_agents) != 1 or sum(value < 0 for value in signature) != 1:
                continue
            unique_defect_count += 1
            bad = negative_agents[0]
            host = witness["host"]
            completing_masks = tuple(transition["completing_masks"])
            new_floater = transition["completing_floater"]
            changed_sources = [
                owner
                for owner in range(len(values))
                if blocked_masks[owner] != completing_masks[owner]
            ]
            if changed_sources != [bad] or bad == host:
                exceptions.append(
                    {
                        "source": profile["source"],
                        "blocked_masks": list(blocked_masks),
                        "old_floater": old_floater,
                        "reason": "noncanonical source or host",
                    }
                )
                continue
            canonical_count += 1
            endpoint_signature, endpoint_witness = absorption_signature(
                completing_masks,
                1 << new_floater,
                totals,
                thresholds,
                row_totals,
            )
            external = [
                agent
                for agent in range(len(values))
                if agent not in (bad, host)
            ]
            checks = {
                "swap_state_eligible": eligible(
                    completing_masks,
                    1 << new_floater,
                    totals,
                    thresholds,
                ),
                "same_completion_host": endpoint_witness["host"] == host,
                "identity_completion": tuple(endpoint_witness["permutation"])
                == tuple(range(len(values))),
                "completion_nonnegative": endpoint_signature[0] >= 0,
                "external_order": all(
                    values[agent][new_floater] <= values[agent][old_floater]
                    for agent in external
                ),
                "bad_owner_order": values[bad][old_floater]
                >= values[bad][new_floater],
            }
            if all(checks.values()):
                verified_count += 1
            else:
                exceptions.append(
                    {
                        "source": profile["source"],
                        "blocked_masks": list(blocked_masks),
                        "old_floater": old_floater,
                        "new_floater": new_floater,
                        "bad": bad,
                        "host": host,
                        "checks": checks,
                    }
                )
    result = {
        "schema": SCHEMA,
        "status": (
            "CANONICAL_HANDOFFS_VERIFIED"
            if verified_count == canonical_count
            else "CANONICAL_HANDOFF_FAILURE_FOUND"
        ),
        "meaning": (
            "Exact reconstruction of the identity-matched, unique-negative-"
            "edge, one-step handoff pattern in the threshold plateau corpus."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "selected_transition_count": selected_count,
        "identity_unique_defect_one_step_count": unique_defect_count,
        "canonical_bad_source_handoff_count": canonical_count,
        "verified_canonical_handoff_count": verified_count,
        "exception_count": len(exceptions),
        "exceptions": exceptions,
        "claim_boundary": (
            "The counts are corpus facts. The handoff implication is proved "
            "separately; the audit does not prove the conditional good exists."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
