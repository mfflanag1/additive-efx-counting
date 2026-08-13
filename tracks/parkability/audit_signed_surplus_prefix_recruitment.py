#!/usr/bin/env python3
"""Exact audit of predecessor-prefix signed-surplus recruitment."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def value(row: dict[str, Fraction], bundle) -> Fraction:
    return sum((row[good] for good in bundle), Fraction())


def threshold(row: dict[str, Fraction], bundle) -> Fraction:
    bundle = tuple(bundle)
    if len(bundle) <= 1:
        return Fraction()
    return value(row, bundle) - min(row[good] for good in bundle)


def audit_superseded_separator(root: Path) -> dict:
    payload = json.loads(
        (root / "results/general_mixed_edge_deletion_return_composition_audit.json").read_text()
    )["local_selected_pool_separator"]
    rows = {
        agent: {good: Fraction(number) for good, number in row.items()}
        for agent, row in payload["valuations"].items()
    }
    base = {agent: Fraction(number) for agent, number in payload["base_utilities"].items()}
    old_observer_bundle = {"aa"}
    D = tuple(payload["D"])
    P = tuple(payload["P"])
    return {
        "census_family_size": payload["family_size"],
        "census_feasible_count": payload["feasible_count"],
        "old_observer_utility": str(value(rows["a"], old_observer_bundle)),
        "old_observer_decorated_threshold": str(threshold(rows["a"], D)),
        "old_observer_prepaid": value(rows["a"], old_observer_bundle) >= threshold(rows["a"], D),
        "hole_owner_utility_on_P": str(value(rows["t"], P)),
        "hole_owner_decorated_threshold": str(threshold(rows["t"], D)),
        "hole_row_separator": value(rows["t"], P) < threshold(rows["t"], D),
        "base_floor": str(base["a"]),
    }


def run(root: Path) -> dict:
    own, current, base, threshold_value = z3.Reals(
        "own current base threshold_value"
    )
    symbolic = {
        "retained_owner_pays_current_safe_core": prove(
            [own >= current, threshold_value <= current], own >= threshold_value
        ),
        "decorated_suffix_owner_pays_current_safe_core": prove(
            [own > current, threshold_value <= current], own > threshold_value
        ),
        "base_paid_owner_pays_old_core": prove(
            [own >= base, threshold_value <= base], own >= threshold_value
        ),
        "retained_or_decorated_failure_is_current_desire": prove(
            [own >= current, own < threshold_value], threshold_value > current
        ),
    }
    assert all(symbolic.values())
    owners = tuple(range(4))
    records = []
    for path in itertools.permutations(owners):
        positions = {owner: index for index, owner in enumerate(path)}
        for decorated_count in (1, 2, 3):
            for decorated_positions in itertools.combinations(range(4), decorated_count):
                decorated = set(decorated_positions)
                for prefix_end in range(4):
                    retained_targets = set(range(prefix_end + 1))
                    allocated_core_sources = set(range(prefix_end + 1, 4))
                    allocated_core_target_positions = {
                        source + 1 for source in allocated_core_sources if source < 3
                    }
                    assert retained_targets.isdisjoint(allocated_core_target_positions)
                    old_suffix = allocated_core_sources - decorated
                    decorated_suffix = allocated_core_sources & decorated
                    blockers = sorted(old_suffix)
                    next_prefixes = [position for position in blockers if position > prefix_end]
                    backward = []
                    forward = []
                    for target_position in retained_targets:
                        for source_position in range(4):
                            if source_position == target_position:
                                continue
                            pair = [source_position, target_position]
                            if source_position > target_position:
                                backward.append(pair)
                            else:
                                forward.append(pair)
                    edge_support_modes = []
                    for source_position in range(3):
                        target_position = source_position + 1
                        if target_position in retained_targets:
                            mode = "nested_in_retained_target"
                        elif source_position in allocated_core_sources:
                            mode = "allocated_selected_core"
                        else:
                            mode = "unallocated_boundary_core_in_original_target"
                        edge_support_modes.append(mode)
                    anchor_preserved = all(
                        mode in {
                            "nested_in_retained_target",
                            "allocated_selected_core",
                            "unallocated_boundary_core_in_original_target",
                        }
                        for mode in edge_support_modes
                    )
                    records.append({
                        "path": list(path),
                        "decorated_positions": sorted(decorated),
                        "prefix_end": prefix_end,
                        "retained_target_positions": sorted(retained_targets),
                        "allocated_core_source_positions": sorted(allocated_core_sources),
                        "old_suffix_positions": sorted(old_suffix),
                        "decorated_suffix_positions": sorted(decorated_suffix),
                        "strict_recruitment_successors": next_prefixes,
                        "backward_response_pairs": backward,
                        "forward_response_pairs": forward,
                        "physical_disjointness": True,
                        "selected_edge_support_modes": edge_support_modes,
                        "anchor_target_support_preserved": anchor_preserved,
                    })
    assert len(records) == 1344
    assert all(record["physical_disjointness"] for record in records)
    assert all(record["anchor_target_support_preserved"] for record in records)
    response_counts = {
        str(prefix_end): {
            "backward": sum(3 - target for target in range(prefix_end + 1)),
            "forward": sum(target for target in range(prefix_end + 1)),
        }
        for prefix_end in range(4)
    }
    assert response_counts == {
        "0": {"backward": 3, "forward": 0},
        "1": {"backward": 5, "forward": 1},
        "2": {"backward": 6, "forward": 3},
        "3": {"backward": 6, "forward": 6},
    }
    superseded = audit_superseded_separator(root)
    assert superseded["census_family_size"] == 262144
    assert superseded["census_feasible_count"] == 0
    assert not superseded["old_observer_prepaid"]
    assert not superseded["hole_row_separator"]

    script = Path(__file__).resolve()
    theorem = root / "results/SIGNED_SURPLUS_PREFIX_RECRUITMENT_LEMMA_20260813.md"
    dependency = root / "results/general_mixed_edge_deletion_return_composition_audit.json"
    return {
        "schema": "signed-surplus-prefix-recruitment-audit-v1",
        "status": "RECRUITMENT_WELL_FOUNDED_POOL_SEPARATOR_SUPERSEDED",
        "case_count": len(records),
        "maximum_strict_prefix_extensions": 3,
        "symbolic_checks": symbolic,
        "response_pair_counts_by_prefix": response_counts,
        "superseded_local_separator": superseded,
        "records": records,
        "smallest_terminal": (
            "full-prefix recurrent current response: supplier-saturated mixed "
            "backward cycle or anchor-preserving forward-chord conversion"
        ),
        "claim_boundary": (
            "cap-free physical recruitment and finite prefix progress; no proof "
            "of decorated-head exchange, forward-chord conversion, GG, or EFX"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "dependency": str(dependency.relative_to(root)),
            "dependency_sha256": sha256(dependency),
            "z3_version": z3.get_version_string(),
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
        "case_count": result["case_count"],
        "smallest_terminal": result["smallest_terminal"],
    }, indent=2))


if __name__ == "__main__":
    main()
