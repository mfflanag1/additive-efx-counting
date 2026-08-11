#!/usr/bin/env python3
"""Dependency audit for the exact resolution of the rank-reset objective."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


DEPENDENCIES = (
    ("gg_rank_reset_raw_potential_refutation_audit.json", "EXACT_SCALE_REFUTATION"),
    ("gg_rank_reset_raw_potential_globality_gap_audit.json", "GLOBALITY_GAP_CONFIRMED"),
    ("gg_historical_support_ledger_stagnation_audit.json", "EXACT_PLATEAU"),
    ("retained_bottom_ledger_stagnation_refutation_audit.json", "EXACT_BOTTOM_TAIL_PLATEAU"),
    ("anchor_constrained_q_priority_matching_audit.json", "ALL_CLASSIFIED"),
    ("bottom_tail_three_owner_cycle_splice_audit.json", "ALL_FORCED"),
    ("universal_paid_anchor_support_reset_audit.json", "ALL_FORCED"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    result_dir = root / "results"
    records = []
    payloads = {}
    for name, required_status in DEPENDENCIES:
        path = result_dir / name
        payload = json.loads(path.read_text())
        assert payload["status"] == required_status
        payloads[name] = payload
        records.append({
            "artifact": f"results/{name}",
            "sha256": sha256(path),
            "status": payload["status"],
        })

    raw = payloads["gg_rank_reset_raw_potential_refutation_audit.json"]
    historical = payloads["gg_historical_support_ledger_stagnation_audit.json"]
    globality = payloads["gg_rank_reset_raw_potential_globality_gap_audit.json"]

    structural_tie = (
        raw["maximum_response_rank_before"] == raw["maximum_response_rank_after"]
        and raw["represented_owner_union_size_before"]
        == raw["represented_owner_union_size_after"]
        and historical["saturated_ledger"]["retained_support_size"] == 0
    )
    original_falls = Fraction(raw["raw_residual_after"]) < Fraction(raw["raw_residual_before"])
    scaled_rises = (
        Fraction(raw["raw_residual_after_c_row_scaled_by_2"])
        > Fraction(raw["raw_residual_before"])
    )
    exact_countermodel = all((
        raw["positive_additive"],
        raw["subset_sum_injective"],
        raw["base_efx"],
        raw["charity_dominated"],
        raw["both_displayed_states_non_efx"],
        raw["response_relation_unchanged_by_scaling"],
        structural_tie,
        original_falls,
        scaled_rises,
        raw["response_neighborhoods"]["A_r"] == ["r"],
        raw["response_neighborhoods"]["W"] == ["r"],
        raw["missing_owner_before"] == "q",
        raw["missing_owner_after"] == "c",
    ))
    corrected_ledger_refuted = all((
        historical["ledger_identical_across_all_states"],
        historical["all_states_non_efx"],
        not historical["full_response_sdr"],
    ))

    script = Path(__file__).resolve()
    theorem = result_dir / "GG_RANK_RESET_MONOTONICITY_OBJECTIVE_RESOLUTION_20260811.md"
    return {
        "schema": "gg-rank-reset-monotonicity-objective-resolution-v1",
        "status": "OBJECTIVE_EXACTLY_REFUTED_AS_STATED",
        "exact_positive_additive_countermodel": exact_countermodel,
        "root_monopoly_pair": ["A_r", "W"],
        "sacrificed_hole_transition": ["q", "c"],
        "requested_structural_coordinates_tied": structural_tie,
        "raw_residual_direction_reversed_by_row_scaling": original_falls and scaled_rises,
        "corrected_historical_ledger_also_refuted": corrected_ledger_refuted,
        "full_gg_countermodel": False,
        "globality_boundary_verified": globality["globally_maximal_priorities"] == [],
        "smallest_missing_operation": (
            "anchor-compatible current-state priority plus retained paid-anchor support "
            "and a surplus-budgeted connected splice on repeated support"
        ),
        "dependencies": records,
        "claim_boundary": (
            "exact resolution of the requested four-coordinate monotonicity theorem; "
            "the corrected connected-splice theorem, GG closure, and EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "exact_positive_additive_countermodel": result["exact_positive_additive_countermodel"],
        "corrected_historical_ledger_also_refuted": result["corrected_historical_ledger_also_refuted"],
        "globality_boundary_verified": result["globality_boundary_verified"],
    }, indent=2))


if __name__ == "__main__":
    main()
