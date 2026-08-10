#!/usr/bin/env python3
"""Audit the r-tail/s-base extremal pair potential on frozen profiles."""

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
        parse_value,
        submasks,
        subset_tables,
    )
    from .analyze_length_three_tail_extremal_profiles import load_tail_profiles, pareto_vectors
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
        parse_value,
        submasks,
        subset_tables,
    )
    from analyze_length_three_tail_extremal_profiles import load_tail_profiles, pareto_vectors


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
            r_threshold = max(tails[R][p_mask], tails[R][q_mask])
            modes = []
            if totals[R][residual] >= r_threshold:
                modes.append("r_tail")
            if totals[S][residual] >= base[S]:
                modes.append("s_base")
            if modes:
                feasible.append(
                    (
                        totals[P][p_mask],
                        totals[Q][q_mask],
                        p_mask,
                        q_mask,
                        residual,
                        r_threshold,
                        tuple(modes),
                    )
                )
    frontier = pareto_vectors(feasible)
    maximal = [record for record in feasible if record[:2] in frontier]
    failures = []
    witnesses = []
    escapes = 0
    mode_escapes = {"r_tail": 0, "s_base": 0}

    def has_direct_escape(record):
        _pv, _qv, local_p, local_q, local_residual, local_r_threshold, local_modes = record
        for local_mode in local_modes:
            for local_payment in submasks(local_residual):
                if local_mode == "r_tail":
                    if totals[R][local_payment] < local_r_threshold:
                        continue
                    local_assigned = [local_p, local_payment, y_mask, local_q]
                else:
                    if totals[S][local_payment] < base[S]:
                        continue
                    local_assigned = [local_p, y_mask, local_payment, local_q]
                if allocation_efx(totals, tails, local_assigned):
                    return True
        return False
    for p_value, q_value, p_mask, q_mask, residual, r_threshold, modes in maximal:
        witness = None
        witness_assigned = None
        for mode in modes:
            for payment in submasks(residual):
                if mode == "r_tail":
                    if totals[R][payment] < r_threshold:
                        continue
                    assigned = [p_mask, payment, y_mask, q_mask]
                else:
                    if totals[S][payment] < base[S]:
                        continue
                    assigned = [p_mask, y_mask, payment, q_mask]
                if allocation_efx(totals, tails, assigned):
                    witness = mode
                    witness_assigned = assigned
                    break
            if witness is not None:
                break
        if witness is not None:
            escapes += 1
            mode_escapes[witness] += 1
            witnesses.append(
                {
                    "mode": witness,
                    "p_value": str(p_value),
                    "q_value": str(q_value),
                    "bundles": {
                        name: labels(witness_assigned[agent], cell["goods"])
                        for agent, name in enumerate(("p", "r", "s", "q"))
                    },
                }
            )
        else:
            failures.append(
                {
                    "p_bundle": labels(p_mask, cell["goods"]),
                    "q_bundle": labels(q_mask, cell["goods"]),
                    "residual": labels(residual, cell["goods"]),
                    "modes": list(modes),
                    "p_value": str(p_value),
                    "q_value": str(q_value),
                    "r_tail_threshold": str(r_threshold),
                }
            )
    f_mask = 1 << cell["floater"]
    x_mask = 1 << cell["x"]
    anchor_summaries = {}
    for anchor, predicate in (
        ("canonical", lambda record: record[2] & f_mask and record[3] & x_mask),
        (
            "two_way",
            lambda record: (record[2] & f_mask and record[3] & x_mask)
            or (record[2] & x_mask and record[3] & f_mask),
        ),
    ):
        anchored = [record for record in feasible if predicate(record)]
        anchored_frontier = pareto_vectors(anchored)
        anchored_maximal = [record for record in anchored if record[:2] in anchored_frontier]
        anchor_summaries[anchor] = {
            "feasible_pair_count": len(anchored),
            "pareto_pair_count": len(anchored_maximal),
            "pareto_pair_failure_count": sum(
                not has_direct_escape(record) for record in anchored_maximal
            ),
        }
    canonical_p = sum(1 << good for good in tr) | f_mask
    fixed_candidates = [
        record
        for record in feasible
        if record[2] == canonical_p
        and record[3] & x_mask
        and "r_tail" in record[6]
        and tails[P][record[3]] <= totals[P][y_mask]
        and tails[R][record[3]] <= totals[R][canonical_p]
    ]
    maximum_q = max((record[1] for record in fixed_candidates), default=None)
    fixed_maximal = [record for record in fixed_candidates if record[1] == maximum_q]
    fixed_failures = 0
    for record in fixed_maximal:
        _pv, _qv, local_p, local_q, local_residual, local_threshold, _modes = record
        if not any(
            totals[R][payment] >= local_threshold
            and allocation_efx(totals, tails, [local_p, payment, y_mask, local_q])
            for payment in submasks(local_residual)
        ):
            fixed_failures += 1
    anchor_summaries["fixed_p_qmax"] = {
        "feasible_pair_count": len(fixed_candidates),
        "maximal_pair_count": len(fixed_maximal),
        "maximal_pair_failure_count": fixed_failures,
    }
    return {
        "label": label,
        "packet_sizes": list(sizes),
        "hybrid_feasible_pair_count": len(feasible),
        "pareto_vector_count": len(frontier),
        "pareto_pair_count": len(maximal),
        "pareto_pair_escape_count": escapes,
        "mode_escape_counts": mode_escapes,
        "pareto_pair_witnesses": witnesses,
        "pareto_pair_failures": failures,
        "anchor_summaries": anchor_summaries,
    }


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(output):
    root = Path(__file__).resolve().parents[2]
    dependency = root / "tracks/parkability/analyze_length_three_tail_extremal_profiles.py"
    profiles, inputs = load_tail_profiles(root)
    records = [analyze_profile(*profile) for profile in profiles]
    result = {
        "schema": "length-three-hybrid-extremal-adversarial-audit-v1",
        "status": "EXACT_ADVERSARIAL_CORPUS_AUDIT",
        "profile_count": len(records),
        "pareto_pair_count": sum(record["pareto_pair_count"] for record in records),
        "pareto_pair_failure_count": sum(
            len(record["pareto_pair_failures"]) for record in records
        ),
        "canonical_anchor_failure_count": sum(
            record["anchor_summaries"]["canonical"]["pareto_pair_failure_count"]
            for record in records
        ),
        "two_way_anchor_failure_count": sum(
            record["anchor_summaries"]["two_way"]["pareto_pair_failure_count"]
            for record in records
        ),
        "fixed_p_qmax_failure_count": sum(
            record["anchor_summaries"]["fixed_p_qmax"]["maximal_pair_failure_count"]
            for record in records
        ),
        "profiles": records,
        "claim_boundary": {
            "proved": "the exact hybrid-extremal census on the frozen profiles",
            "not_proved": "the cap-free hybrid-extremal escape lemma",
            "source_scope": "the loaded corpus uses the a=r singleton-source pattern",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(root)),
            "script_sha256": sha256(Path(__file__).resolve()),
            "inputs": [
                {"path": str(path.relative_to(root)), "sha256": sha256(path)}
                for path in inputs
            ],
            "dependencies": [
                {"path": str(dependency.relative_to(root)), "sha256": sha256(dependency)}
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
                    "canonical_anchor_failure_count",
                    "two_way_anchor_failure_count",
                    "fixed_p_qmax_failure_count",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
