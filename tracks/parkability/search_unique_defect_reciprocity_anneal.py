#!/usr/bin/env python3
"""Adversarially mutate a blocked state to falsify host reciprocity."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import random
from pathlib import Path

try:
    from .anneal import atomic_json
    from .analyze_charity_threshold_plateau import owner_minima
    from .audit_unique_defect_handoff import candidate_slacks, load_record_values
    from .scan_charity_threshold_absorption import absorption_signature, eligible, tables
    from .search_unique_defect_host_redirection import (
        acceptance_edges,
        identity_bad_agents,
    )
except ImportError:
    from anneal import atomic_json
    from analyze_charity_threshold_plateau import owner_minima
    from audit_unique_defect_handoff import candidate_slacks, load_record_values
    from scan_charity_threshold_absorption import absorption_signature, eligible, tables
    from search_unique_defect_host_redirection import (
        acceptance_edges,
        identity_bad_agents,
    )


SCHEMA = "unique-defect-radius-three-gradient-anneal-v1"


def fixed_host_signature(masks, floater, host, totals, thresholds, row_totals):
    n = len(masks)
    complete = list(masks)
    complete[host] |= 1 << floater
    best = None
    best_permutation = None
    for permutation in itertools.permutations(range(n)):
        signature = tuple(
            sorted(
                Fraction(
                    totals[agent][complete[permutation[agent]]]
                    - max(
                        thresholds[agent][complete[target]]
                        for target in range(n)
                        if target != permutation[agent]
                    ),
                    row_totals[agent],
                )
                for agent in range(n)
            )
        )
        if best is None or signature > best:
            best = signature
            best_permutation = permutation
    return best, best_permutation


def classify(values, masks, floater):
    n = len(values)
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    if not eligible(masks, 1 << floater, totals, thresholds):
        return {"premise": False, "reason": "ineligible"}
    signature, witness = absorption_signature(
        masks, 1 << floater, totals, thresholds, row_totals
    )
    if signature[0] >= 0:
        return {"premise": False, "reason": "absorbing"}
    if tuple(witness["permutation"]) != tuple(range(n)):
        return {"premise": False, "reason": "nonidentity optimum"}
    slacks = candidate_slacks(
        masks, floater, witness, totals, thresholds, row_totals
    )
    bad_agents = tuple(agent for agent, slack in enumerate(slacks) if slack < 0)
    if len(bad_agents) != 1 or sum(slack < 0 for slack in signature) != 1:
        return {"premise": False, "reason": "not unique defect"}
    bad = bad_agents[0]
    host = witness["host"]
    if bad == host:
        return {"premise": False, "reason": "self host"}
    edges = acceptance_edges(masks, floater, host, totals, thresholds)
    if any((agent, bad) in edges for agent in range(n)):
        return {"premise": False, "reason": "not full witness"}
    redirected_bad = identity_bad_agents(masks, floater, bad, totals, thresholds)
    redirected_signature, redirected_permutation = fixed_host_signature(
        masks, floater, bad, totals, thresholds, row_totals
    )
    redirected_identity_witness = {
        "host": bad,
        "permutation": list(range(n)),
    }
    redirected_identity_slacks = candidate_slacks(
        masks,
        floater,
        redirected_identity_witness,
        totals,
        thresholds,
        row_totals,
    )
    reciprocal = redirected_bad == (host,)
    current_theta = sum(
        Fraction(thresholds[owner][masks[owner]], row_totals[owner])
        for owner in range(n)
    )
    best_gradient = None
    seen_moves = set()

    def consider(candidate_masks, candidate_floater, move):
        nonlocal best_gradient
        state = (candidate_masks, candidate_floater)
        if state in seen_moves:
            return
        seen_moves.add(state)
        if not eligible(
            candidate_masks, 1 << candidate_floater, totals, thresholds
        ):
            return
        candidate_theta = sum(
            Fraction(
                thresholds[candidate_owner][candidate_masks[candidate_owner]],
                row_totals[candidate_owner],
            )
            for candidate_owner in range(n)
        )
        candidate_signature, candidate_witness = absorption_signature(
            candidate_masks,
            1 << candidate_floater,
            totals,
            thresholds,
            row_totals,
        )
        if not (
            candidate_theta > current_theta
            or (
                candidate_theta == current_theta
                and candidate_signature > signature
            )
        ):
            return
        key = (candidate_theta, candidate_signature)
        if best_gradient is None or key > best_gradient[0]:
            best_gradient = (
                key,
                {
                    "move": move,
                    "theta_change": str(candidate_theta - current_theta),
                    "signature": [str(value) for value in candidate_signature],
                    "witness": candidate_witness,
                },
            )

    m = len(values[0])
    for owner in range(n):
        for outgoing in range(m):
            if not masks[owner] & (1 << outgoing):
                continue
            candidate_masks = list(masks)
            candidate_masks[owner] = (
                candidate_masks[owner] & ~(1 << outgoing)
            ) | (1 << floater)
            consider(
                tuple(candidate_masks),
                outgoing,
                {
                    "kind": "charity_swap",
                    "owner": owner,
                    "outgoing": outgoing,
                    "owner_minimum": outgoing
                    in owner_minima(masks[owner], owner, values),
                },
            )
    for left in range(n):
        for right in range(left + 1, n):
            for left_good in range(m):
                if not masks[left] & (1 << left_good):
                    continue
                for right_good in range(m):
                    if not masks[right] & (1 << right_good):
                        continue
                    candidate_masks = list(masks)
                    candidate_masks[left] ^= (1 << left_good) | (1 << right_good)
                    candidate_masks[right] ^= (1 << left_good) | (1 << right_good)
                    consider(
                        tuple(candidate_masks),
                        floater,
                        {
                            "kind": "allocated_swap",
                            "left": left,
                            "left_good": left_good,
                            "right": right,
                            "right_good": right_good,
                        },
                    )
    for source in range(n):
        if masks[source].bit_count() <= 1:
            continue
        for target in range(n):
            if target == source:
                continue
            for good in range(m):
                if not masks[source] & (1 << good):
                    continue
                candidate_masks = list(masks)
                candidate_masks[source] &= ~(1 << good)
                candidate_masks[target] |= 1 << good
                consider(
                    tuple(candidate_masks),
                    floater,
                    {
                        "kind": "allocated_transfer",
                        "source": source,
                        "good": good,
                        "target": target,
                    },
                )
    if best_gradient is None:
        labels = []
        for good in range(m):
            if good == floater:
                labels.append(n)
            else:
                labels.append(
                    next(
                        owner
                        for owner in range(n)
                        if masks[owner] & (1 << good)
                    )
                )
        for radius in (2, 3):
            for changed_goods in itertools.combinations(range(m), radius):
                old_labels = tuple(labels[good] for good in changed_goods)
                for new_labels in itertools.product(range(n + 1), repeat=radius):
                    if any(old == new for old, new in zip(old_labels, new_labels)):
                        continue
                    candidate_labels = labels[:]
                    for good, new in zip(changed_goods, new_labels):
                        candidate_labels[good] = new
                    if candidate_labels.count(n) != 1:
                        continue
                    candidate_masks = tuple(
                        sum(
                            1 << good
                            for good, assigned in enumerate(candidate_labels)
                            if assigned == owner
                        )
                        for owner in range(n)
                    )
                    if any(mask == 0 for mask in candidate_masks):
                        continue
                    consider(
                        candidate_masks,
                        candidate_labels.index(n),
                        {
                            "kind": f"{radius}_good_transfer_union",
                            "goods": list(changed_goods),
                            "old_labels": list(old_labels),
                            "new_labels": list(new_labels),
                        },
                    )
            if best_gradient is not None:
                break
    return {
        "premise": True,
        "reciprocal": reciprocal,
        "elementary_gradient": (
            None if best_gradient is None else best_gradient[1]
        ),
        "radius_three_gradient_exists": best_gradient is not None,
        "signature": [str(value) for value in signature],
        "host": host,
        "bad": bad,
        "redirected_identity_bad_agents": list(redirected_bad),
        "redirected_identity_slacks": [
            str(value) for value in redirected_identity_slacks
        ],
        "redirected_identity_bottleneck_matches": (
            min(redirected_identity_slacks) == signature[0]
        ),
        "redirected_best_signature": [str(value) for value in redirected_signature],
        "redirected_best_permutation": list(redirected_permutation),
    }


def mutate(values, cap, rng):
    candidate = [list(row) for row in values]
    agent = rng.randrange(len(candidate))
    good = rng.randrange(len(candidate[0]))
    old = candidate[agent][good]
    choices = [value for value in range(1, cap + 1) if value != old]
    candidate[agent][good] = rng.choice(choices)
    return tuple(tuple(row) for row in candidate)


def run(source, record_index, transition_index, cap, steps, seed, output):
    if output.exists():
        raise ValueError("output must be new")
    document = json.loads(source.read_text())
    record = document["records"][record_index]
    values = load_record_values(record)
    transition = record["selected_transitions"][transition_index]
    masks = tuple(transition["blocked_masks"])
    floater = transition["blocked_floater"]
    initial = classify(values, masks, floater)
    if not initial.get("premise") or not initial.get("reciprocal"):
        raise ValueError("seed is not a reciprocal full unique-defect state")
    rng = random.Random(seed)
    current = values
    premise_preserving_steps = 0
    reciprocal_step_count = 0
    gradient_step_count = 0
    gradient_kind_counts = {}
    distinct = {current}
    counterexample = None
    rejection_reasons = {}
    for step in range(1, steps + 1):
        candidate = mutate(current, cap, rng)
        result = classify(candidate, masks, floater)
        if not result.get("premise"):
            reason = result["reason"]
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
            continue
        premise_preserving_steps += 1
        current = candidate
        distinct.add(current)
        if result["reciprocal"]:
            reciprocal_step_count += 1
        if result["elementary_gradient"] is not None:
            gradient_step_count += 1
            kind = result["elementary_gradient"]["move"]["kind"]
            gradient_kind_counts[kind] = gradient_kind_counts.get(kind, 0) + 1
        if result["radius_three_gradient_exists"]:
            continue
        counterexample = {
            "step": step,
            "values": [list(row) for row in current],
            "values_sha256": hashlib.sha256(
                json.dumps(current, separators=(",", ":")).encode()
            ).hexdigest(),
            "masks": list(masks),
            "floater": floater,
            **result,
        }
        break
    result = {
        "schema": SCHEMA,
        "status": (
            "FULL_UNIQUE_DEFECT_RADIUS_THREE_GRADIENT_COUNTEREXAMPLE_FOUND"
            if counterexample is not None
            else "FULL_UNIQUE_DEFECT_RADIUS_THREE_GRADIENT_SURVIVES_ANNEAL"
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "record_index": record_index,
        "transition_index": transition_index,
        "cap": cap,
        "seed": seed,
        "steps_requested": steps,
        "steps_executed": step if steps else 0,
        "premise_preserving_step_count": premise_preserving_steps,
        "reciprocal_step_count": reciprocal_step_count,
        "elementary_gradient_step_count": gradient_step_count,
        "elementary_gradient_kind_counts": dict(sorted(gradient_kind_counts.items())),
        "distinct_premise_profile_count": len(distinct),
        "rejection_reason_counts": dict(sorted(rejection_reasons.items())),
        "counterexample": counterexample,
        "claim_boundary": (
            "This tests whether every state-level optimal full unique-defect "
            "candidate has an eligible transfer union changing at most three "
            "goods and improving (Theta,Lambda). It does not impose global "
            "threshold maximality across all states."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--record-index", type=int, default=0)
    parser.add_argument("--transition-index", type=int, default=0)
    parser.add_argument("--cap", type=int, default=12)
    parser.add_argument("--steps", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260803)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(**vars(args)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
