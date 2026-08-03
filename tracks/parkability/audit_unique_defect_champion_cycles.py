#!/usr/bin/env python3
"""Audit threshold-compatible basic champion cycles at unique-defect states."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_unique_defect_handoff import (
        acceptance_edges,
        candidate_slacks,
        load_record_values,
        obstruction_topology,
    )
    from .scan_charity_threshold_absorption import (
        absorption_signature,
        eligible,
        tables,
        theta,
    )
except ImportError:
    from anneal import atomic_json
    from audit_unique_defect_handoff import (
        acceptance_edges,
        candidate_slacks,
        load_record_values,
        obstruction_topology,
    )
    from scan_charity_threshold_absorption import (
        absorption_signature,
        eligible,
        tables,
        theta,
    )


SCHEMA = "unique-defect-champion-cycle-audit-v2"


def proper_submasks(mask):
    submask = (mask - 1) & mask
    while submask:
        yield submask
        submask = (submask - 1) & mask


def champion_desired_sets(source, target, masks, floater, totals, thresholds):
    augmented = masks[target] | (1 << floater)
    own_value = totals[source][masks[source]]
    desired = []
    for candidate in proper_submasks(augmented):
        if totals[source][candidate] <= own_value:
            continue
        if all(
            thresholds[agent][candidate] <= totals[agent][masks[agent]]
            for agent in range(len(masks))
        ):
            desired.append(candidate)
    if totals[source][augmented] > own_value and all(
        thresholds[agent][augmented] <= totals[agent][masks[agent]]
        for agent in range(len(masks))
    ):
        desired.append(augmented)
    return tuple(desired)


def envy_edges(masks, totals):
    return {
        (source, target)
        for source in range(len(masks))
        for target in range(len(masks))
        if source != target
        and totals[source][masks[target]] > totals[source][masks[source]]
    }


def simple_envy_paths(start, end, edges, n):
    paths = []

    def visit(path):
        tail = path[-1]
        if tail == end:
            paths.append(tuple(path))
            return
        for successor in range(n):
            if (tail, successor) in edges and successor not in path:
                visit(path + [successor])

    visit([start])
    return tuple(paths)


def basic_cycle_endpoint(masks, source, target, desired, path, all_mask):
    endpoint = list(masks)
    endpoint[source] = desired
    for old_source, old_target in zip(path, path[1:]):
        endpoint[old_source] = masks[old_target]
    used = 0
    for bundle in endpoint:
        if used & bundle:
            raise AssertionError("basic cycle produced overlapping bundles")
        used |= bundle
    return tuple(endpoint), all_mask ^ used


def run(source, output):
    if output.exists():
        raise ValueError("output must be new")
    document = json.loads(source.read_text())
    counts = Counter()
    adverse_examples = []
    seen = set()
    for profile in document["records"]:
        values = load_record_values(profile)
        totals, thresholds = tables(values)
        row_totals = tuple(sum(row) for row in values)
        all_mask = (1 << len(values[0])) - 1
        for transition in profile.get("selected_transitions", ()):
            blocked_masks = tuple(transition["blocked_masks"])
            floater = transition["blocked_floater"]
            state_key = (profile["values_sha256"], blocked_masks, floater)
            if state_key in seen:
                continue
            seen.add(state_key)
            counts["distinct_selected_states"] += 1
            signature, witness = absorption_signature(
                blocked_masks,
                1 << floater,
                totals,
                thresholds,
                row_totals,
            )
            if tuple(witness["permutation"]) != tuple(range(len(values))):
                continue
            slacks = candidate_slacks(
                blocked_masks,
                floater,
                witness,
                totals,
                thresholds,
                row_totals,
            )
            negative = [agent for agent, slack in enumerate(slacks) if slack < 0]
            if len(negative) != 1 or sum(value < 0 for value in signature) != 1:
                continue
            bad = negative[0]
            host = witness["host"]
            topology = obstruction_topology(
                acceptance_edges(
                    blocked_masks,
                    floater,
                    witness,
                    totals,
                    thresholds,
                ),
                bad,
                host,
                len(values),
            )
            if topology != "full_zero_bad_bundle":
                continue
            counts["full_unique_defect_states"] += 1
            desired_by_edge = {
                (agent, target): champion_desired_sets(
                    agent,
                    target,
                    blocked_masks,
                    floater,
                    totals,
                    thresholds,
                )
                for agent in range(len(values))
                for target in range(len(values))
            }
            forced_desired = desired_by_edge[(bad, host)]
            if not forced_desired:
                raise AssertionError("forced champion bridge did not replay")
            counts["forced_champion_replayed"] += 1
            if any(desired & (1 << floater) == 0 for desired in forced_desired):
                counts["forced_champion_can_discard_floater"] += 1
            if any(desired & (1 << floater) for desired in forced_desired):
                counts["forced_champion_can_retain_floater"] += 1
            reciprocal_desired = desired_by_edge[(host, bad)]
            if reciprocal_desired:
                counts["reciprocal_forced_pair"] += 1
            envy = envy_edges(blocked_masks, totals)
            if (bad, host) in envy:
                counts["bad_envies_host"] += 1
            base_theta = theta(
                blocked_masks,
                totals,
                thresholds,
                row_totals,
            )
            endpoints = []
            for (agent, target), desired_sets in desired_by_edge.items():
                if not desired_sets:
                    continue
                for path in simple_envy_paths(target, agent, envy, len(values)):
                    for desired in desired_sets:
                        endpoint, charity = basic_cycle_endpoint(
                            blocked_masks,
                            agent,
                            target,
                            desired,
                            path,
                            all_mask,
                        )
                        if not eligible(endpoint, charity, totals, thresholds):
                            counts["basic_pi_endpoints_failing_charity_eligibility"] += 1
                            continue
                        endpoints.append(
                            {
                                "source": agent,
                                "target": target,
                                "desired": desired,
                                "path": path,
                                "masks": endpoint,
                                "charity": charity,
                                "theta_change": theta(
                                    endpoint,
                                    totals,
                                    thresholds,
                                    row_totals,
                                )
                                - base_theta,
                            }
                        )
            if endpoints:
                counts["states_with_charity_eligible_basic_pi_cycle"] += 1
            same_cardinality = [
                endpoint
                for endpoint in endpoints
                if endpoint["charity"].bit_count() == 1
            ]
            if same_cardinality:
                counts["states_with_one_charity_basic_pi_cycle"] += 1
            compatible = [
                endpoint
                for endpoint in same_cardinality
                if endpoint["theta_change"] >= 0
            ]
            if compatible:
                counts["states_with_threshold_compatible_basic_pi_cycle"] += 1
                best_compatible = max(
                    compatible,
                    key=lambda endpoint: endpoint["theta_change"],
                )
                if best_compatible["theta_change"] > 0:
                    counts["states_with_positive_theta_basic_pi_cycle"] += 1
                else:
                    counts["states_with_zero_theta_basic_pi_cycle"] += 1
            direct_reciprocal = [
                endpoint
                for endpoint in same_cardinality
                if endpoint["source"] == host
                and endpoint["target"] == bad
                and endpoint["path"] == (bad, host)
                and endpoint["theta_change"] >= 0
            ]
            if direct_reciprocal:
                counts["states_with_direct_reciprocal_compatible_cycle"] += 1
            elif endpoints and len(adverse_examples) < 20:
                best = max(endpoints, key=lambda endpoint: endpoint["theta_change"])
                adverse_examples.append(
                    {
                        "source": profile["source"],
                        "values_sha256": profile["values_sha256"],
                        "blocked_masks": list(blocked_masks),
                        "floater": floater,
                        "bad": bad,
                        "host": host,
                        "reciprocal_forced_pair": bool(
                            desired_by_edge[(host, bad)]
                        ),
                        "charity_eligible_basic_pi_endpoint_count": len(endpoints),
                        "one_charity_endpoint_count": len(same_cardinality),
                        "best_theta_change": str(best["theta_change"]),
                        "best_charity_size": best["charity"].bit_count(),
                    }
                )
    full = counts["full_unique_defect_states"]
    compatible = counts["states_with_threshold_compatible_basic_pi_cycle"]
    result = {
        "schema": SCHEMA,
        "status": (
            "CORPUS_ALL_THRESHOLD_COMPATIBLE"
            if compatible == full
            else "CORPUS_HAS_RESIDUAL_STATES"
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "counts": dict(sorted(counts.items())),
        "adverse_examples": adverse_examples,
        "claim_boundary": (
            "This is an exact corpus audit of charity-eligible basic PI cycles "
            "only. It neither "
            "proves a champion-cycle theorem nor rules out generalized PI edge "
            "sets, connected transfers, or complete EFX allocations."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
