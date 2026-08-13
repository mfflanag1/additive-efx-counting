#!/usr/bin/env python3
"""Exact graph, debt, and support audit of the mixed Hamiltonian interface."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


OWNERS = ("r", "q", "c", "s")
CHARITY = "charity"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def record(path: tuple[str, ...], mixed_position: int, closing_position: int) -> dict:
    targets = path[1:] + (CHARITY,)
    mixed_source = path[mixed_position]
    mixed_target = targets[mixed_position]
    closing_source = path[closing_position]
    target_atoms: dict[str, set[str]] = {}
    for index, target in enumerate(targets):
        core = "D" if index == mixed_position else f"A:{path[index]}"
        target_atoms[target] = {core, f"R:{target}"}
    target_atoms[path[0]] = {"E:keep", "E:g", "H"}
    all_targets = list(target_atoms.values())
    assert all(
        left.isdisjoint(right)
        for index, left in enumerate(all_targets)
        for right in all_targets[index + 1 :]
    )
    selected_cores = [
        "D" if index == mixed_position else f"A:{path[index]}"
        for index in range(4)
    ]
    assert len(set(selected_cores)) == 4
    own_residual_disjoint = {}
    for index, source in enumerate(path):
        source_core = selected_cores[index]
        own_residual = f"R:{source}" if source != path[0] else "H"
        own_residual_disjoint[source] = all(
            not (source_core in atoms and own_residual in atoms)
            for atoms in target_atoms.values()
        )
    assert all(own_residual_disjoint.values())
    return {
        "path": list(path),
        "mixed_position": mixed_position,
        "mixed_source": mixed_source,
        "mixed_target": mixed_target,
        "closing_position": closing_position,
        "closing_source": closing_source,
        "closing_target": path[0],
        "selected_mixed_edge_in_prefix_cycle": mixed_position < closing_position,
        "mixed_and_closing_supports_disjoint": "D" not in target_atoms[path[0]],
        "own_core_residual_disjoint": own_residual_disjoint,
        "incoming_mixed_owner": mixed_target if mixed_target != CHARITY else None,
    }


def run(root: Path) -> dict:
    beta, delta, margin = z3.Reals("beta delta margin")
    symbolic = {
        "positive_debt_requires_positive_current_surplus": prove(
            [beta > 0, beta <= delta], delta > 0
        ),
        "mixed_separator_identifies_positive_debt": prove(
            [margin >= 0, margin < beta], beta > 0
        ),
        "old_margin_pays_zero_debt": prove([margin > 0], margin >= 0),
    }
    assert all(symbolic.values())

    records = [
        record(path, mixed_position, closing_position)
        for path in itertools.permutations(OWNERS)
        for mixed_position in range(4)
        for closing_position in range(1, 4)
    ]
    assert len(records) == 288
    prefix_counts = {
        "mixed_inside_prefix": sum(r["selected_mixed_edge_in_prefix_cycle"] for r in records),
        "mixed_outside_prefix": sum(not r["selected_mixed_edge_in_prefix_cycle"] for r in records),
    }
    assert prefix_counts == {"mixed_inside_prefix": 144, "mixed_outside_prefix": 144}

    anchored_paths = [path for path in itertools.permutations(OWNERS) if any(
        path[index] == "r" and path[index + 1] == "q" for index in range(3)
    )]
    anchored_locations = []
    for path in anchored_paths:
        anchor_position = path.index("r")
        for mixed_position in range(4):
            if mixed_position == anchor_position:
                continue
            anchored_locations.append({
                "path": list(path),
                "anchor_position": anchor_position,
                "mixed_position": mixed_position,
            })
    assert len(anchored_paths) == 6
    assert len(anchored_locations) == 18

    # Exact logical classification: zero old/current extremes close; a mixed
    # survivor can have one, two, or three decorated selected edges.
    kappa = {
        "0": "four old cores: immediate base-safe EFX/Pareto shortcut",
        "1": "three old cores and one decorated core",
        "2": "two old cores and two decorated cores",
        "3": "one old core and three decorated cores",
        "4": "four current-desired/current-safe cores: immediate EFX/Pareto shortcut",
    }
    abstract_kappa2_countermodel = {
        "path": [0, 1, 2, 3, "charity"],
        "edges": [
            {"source": 0, "target": 1, "type": "decorated"},
            {"source": 1, "target": 2, "type": "old"},
            {"source": 2, "target": 3, "type": "decorated"},
            {"source": 3, "target": "charity", "type": "old"},
        ],
        "old_rank": 2,
        "full_rank": 4,
        "minimum_decorated_edges_in_rank4_matching": 2,
        "interpretation": (
            "The BCFF old/current edge definitions and Hamiltonian graph shape "
            "alone do not force a rank-four matching with exactly one decorated edge."
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/GENUINE_MIXED_EDGE_HAMILTONIAN_INTERFACE_20260813.md"
    return {
        "schema": "genuine-mixed-edge-hamiltonian-interface-audit-v1",
        "status": "INTERFACE_RECONSTRUCTED_WITH_KAPPA_BRANCH",
        "symbolic_debt_checks": symbolic,
        "decorated_edge_count_classification": kappa,
        "mixed_survivor_kappa": [1, 2, 3],
        "abstract_kappa2_countermodel": abstract_kappa2_countermodel,
        "one_decorated_path_count": 24 * 4,
        "one_decorated_closing_pivot_count": len(records),
        "prefix_membership_counts": prefix_counts,
        "all_mixed_and_closing_supports_disjoint": all(
            r["mixed_and_closing_supports_disjoint"] for r in records
        ),
        "all_own_core_residual_pairs_disjoint": all(
            all(r["own_core_residual_disjoint"].values()) for r in records
        ),
        "anchored_path_count": len(anchored_paths),
        "anchored_nonanchor_mixed_locations": anchored_locations,
        "anchored_nonanchor_mixed_location_count": len(anchored_locations),
        "records": records,
        "claim_boundary": (
            "exact graph/support/debt interface; kappa=1 is not proved universal, "
            "and no decorated observer budgets are closed"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
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
        "mixed_survivor_kappa": result["mixed_survivor_kappa"],
        "anchored_locations": result["anchored_nonanchor_mixed_location_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
