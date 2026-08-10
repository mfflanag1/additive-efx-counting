#!/usr/bin/env python3
"""Audit Pareto-maximal r-tail compatible pairs on frozen profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .analyze_alternating_singleton_return_models import make_cell
    from .analyze_dual_mode_adversarial_profiles import (
        P,
        Q,
        R,
        S,
        allocation_efx,
        compatible_pair,
        labels,
        load_profiles,
        minimal_relative_blocker,
        parse_value,
        submasks,
        subset_tables,
    )
except ImportError:
    from analyze_alternating_singleton_return_models import make_cell
    from analyze_dual_mode_adversarial_profiles import (
        P,
        Q,
        R,
        S,
        allocation_efx,
        compatible_pair,
        labels,
        load_profiles,
        minimal_relative_blocker,
        parse_value,
        submasks,
        subset_tables,
    )


def pareto_vectors(records):
    vectors = sorted({(record[0], record[1]) for record in records}, reverse=True)
    frontier = set()
    best_q = None
    for p_value, q_value in vectors:
        if best_q is None or q_value > best_q:
            frontier.add((p_value, q_value))
            best_q = q_value
    return frontier


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_tail_profiles(root):
    profiles, inputs = load_profiles(root)
    additions = (
        ("length_three_dual_mode_atom_selected", "length_three_dual_mode_atom_selected.json", (1, 1, 1, 1)),
        ("length_three_dual_mode_split_refutation", "length_three_dual_mode_split_refutation.json", None),
    )
    for label, name, sizes in additions:
        path = root / "results" / name
        record = json.loads(path.read_text())
        packet_sizes = tuple(record["packet_sizes"]) if sizes is None else sizes
        native = record["values"]
        alternating_row_order = [native[0], native[1], native[3], native[2]]
        profiles.append((label, alternating_row_order, packet_sizes))
        inputs.append(path)
    return profiles, inputs


def analyze_profile(label, raw_values, sizes):
    cell = make_cell(sizes)
    values = tuple(tuple(parse_value(value) for value in row) for row in raw_values)
    totals, tails = subset_tables(values, cell["m"])
    tr, br, tq, bq = cell["packets"]
    base_bundles = ((cell["x"],), tr + br, (cell["y"],), tq + bq)
    base_masks = tuple(sum(1 << good for good in bundle) for bundle in base_bundles)
    base = tuple(totals[agent][base_masks[agent]] for agent in range(4))
    y_mask = 1 << cell["y"]
    full_without_y = ((1 << cell["m"]) - 1) ^ y_mask
    feasible = []
    for p_mask in submasks(full_without_y):
        remaining = full_without_y ^ p_mask
        for q_mask in submasks(remaining):
            if not compatible_pair(totals, tails, base, p_mask, q_mask):
                continue
            residual = remaining ^ q_mask
            threshold = max(tails[R][p_mask], tails[R][q_mask])
            if totals[R][residual] >= threshold:
                feasible.append(
                    (totals[P][p_mask], totals[Q][q_mask], p_mask, q_mask, residual, threshold)
                )
    frontier = pareto_vectors(feasible)
    maximal = [record for record in feasible if record[:2] in frontier]
    failures = []
    escapes = 0
    for p_value, q_value, p_mask, q_mask, residual, threshold in maximal:
        witness = None
        for payment in submasks(residual):
            assigned = [p_mask, payment, y_mask, q_mask]
            if allocation_efx(totals, tails, assigned):
                witness = payment
                break
        if witness is not None:
            escapes += 1
            continue
        failure = {
                "p_bundle": labels(p_mask, cell["goods"]),
                "q_bundle": labels(q_mask, cell["goods"]),
                "residual": labels(residual, cell["goods"]),
                "p_value": str(p_value),
                "q_value": str(q_value),
                "r_tail_threshold": str(threshold),
                "r_residual_value": str(totals[R][residual]),
                "derived_blocker_count": 0,
                "derived_blockers": [],
                "s_reversal_escape": None,
                "pivot_escape": None,
            }
        thresholds = [p_value, base[R], base[S], q_value]
        minimal_payments = []
        for payment in submasks(residual):
            if totals[R][payment] < threshold:
                continue
            if all(
                totals[R][payment ^ (1 << good)] < threshold
                for good in range(cell["m"])
                if payment & (1 << good)
            ):
                minimal_payments.append(payment)
        seen_blockers = set()
        for payment in minimal_payments:
            assigned = [p_mask, payment, y_mask, q_mask]
            for observer in (P, Q, S):
                for good in range(cell["m"]):
                    if not payment & (1 << good):
                        continue
                    container = payment ^ (1 << good)
                    if totals[observer][assigned[observer]] >= totals[observer][container]:
                        continue
                    blocker = minimal_relative_blocker(totals, thresholds, container)
                    if blocker is None:
                        continue
                    f_mask, sources = blocker
                    if S in sources:
                        reversal = [p_mask, y_mask, f_mask, q_mask]
                        if allocation_efx(totals, tails, reversal):
                            failure["s_reversal_escape"] = {
                                "boundary_bundle": labels(f_mask, cell["goods"]),
                                "bundles": {
                                    name: labels(reversal[agent], cell["goods"])
                                    for agent, name in enumerate(("p", "r", "s", "q"))
                                },
                            }
                    for source in sources:
                        if source not in (P, Q):
                            continue
                        key = (f_mask, source)
                        if key in seen_blockers:
                            continue
                        seen_blockers.add(key)
                        b_k = p_mask if source == P else q_mask
                        b_l = q_mask if source == P else p_mask
                        minimum = min(
                            totals[R][1 << h]
                            for h in range(cell["m"])
                            if b_l & (1 << h)
                        )
                        for h in range(cell["m"]):
                            h_mask = 1 << h
                            if not b_l & h_mask or totals[R][h_mask] != minimum:
                                continue
                            a_mask = b_l ^ h_mask
                            c_mask = b_k | h_mask
                            orientations = (
                                [f_mask, a_mask, y_mask, c_mask]
                                if source == P
                                else [c_mask, a_mask, y_mask, f_mask],
                                [f_mask, c_mask, y_mask, a_mask]
                                if source == P
                                else [a_mask, c_mask, y_mask, f_mask],
                            )
                            blocker_record = {
                                "source": "p" if source == P else "q",
                                "boundary_bundle": labels(f_mask, cell["goods"]),
                                "pivot_good": cell["goods"][h],
                                "orientation_failures": [],
                            }
                            for orientation, pivot_assigned in enumerate(orientations):
                                if (
                                    totals[P][pivot_assigned[P]] > base[P]
                                    and allocation_efx(totals, tails, pivot_assigned)
                                ):
                                    failure["pivot_escape"] = {
                                        "source": "p" if source == P else "q",
                                        "boundary_bundle": labels(f_mask, cell["goods"]),
                                        "pivot_good": cell["goods"][h],
                                        "orientation": orientation,
                                        "bundles": {
                                            name: labels(pivot_assigned[agent], cell["goods"])
                                            for agent, name in enumerate(("p", "r", "s", "q"))
                                        },
                                    }
                                    break
                                violations = []
                                for observing_agent in range(4):
                                    for target_agent in range(4):
                                        if (
                                            totals[observing_agent][pivot_assigned[observing_agent]]
                                            < tails[observing_agent][pivot_assigned[target_agent]]
                                        ):
                                            violations.append(
                                                {
                                                    "observer": ("p", "r", "s", "q")[observing_agent],
                                                    "target": ("p", "r", "s", "q")[target_agent],
                                                }
                                            )
                                blocker_record["orientation_failures"].append(
                                    {
                                        "orientation": orientation,
                                        "p_above_base": totals[P][pivot_assigned[P]] > base[P],
                                        "violations": violations,
                                    }
                                )
                            failure["derived_blockers"].append(blocker_record)
                            if failure["pivot_escape"] is not None:
                                break
                        if failure["pivot_escape"] is not None:
                            break
                    if failure["pivot_escape"] is not None:
                        break
                if failure["pivot_escape"] is not None:
                    break
            if failure["pivot_escape"] is not None:
                break
        failure["derived_blocker_count"] = len(seen_blockers)
        failures.append(failure)
    return {
        "label": label,
        "packet_sizes": list(sizes),
        "tail_feasible_pair_count": len(feasible),
        "pareto_vector_count": len(frontier),
        "pareto_pair_count": len(maximal),
        "pareto_pair_escape_count": escapes,
        "pareto_pair_failures": failures,
    }


def run(output):
    root = Path(__file__).resolve().parents[2]
    profiles, inputs = load_tail_profiles(root)
    records = [analyze_profile(*profile) for profile in profiles]
    result = {
        "schema": "length-three-tail-extremal-adversarial-audit-v1",
        "status": "EXACT_ADVERSARIAL_CORPUS_AUDIT",
        "profile_count": len(records),
        "pareto_pair_count": sum(record["pareto_pair_count"] for record in records),
        "pareto_pair_failure_count": sum(
            len(record["pareto_pair_failures"]) for record in records
        ),
        "pareto_pair_pivot_escape_count": sum(
            failure["pivot_escape"] is not None
            for record in records
            for failure in record["pareto_pair_failures"]
        ),
        "pareto_pair_s_reversal_escape_count": sum(
            failure["s_reversal_escape"] is not None
            for record in records
            for failure in record["pareto_pair_failures"]
        ),
        "profiles": records,
        "claim_boundary": {
            "proved": "the exact extremal-tail census on the frozen profiles",
            "not_proved": "the cap-free extremal-tail escape lemma",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(root)),
            "script_sha256": sha256(Path(__file__).resolve()),
            "inputs": [
                {"path": str(path.relative_to(root)), "sha256": sha256(path)}
                for path in inputs
            ],
        },
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "profile_count",
                    "pareto_pair_count",
                    "pareto_pair_failure_count",
                    "pareto_pair_pivot_escape_count",
                    "pareto_pair_s_reversal_escape_count",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
