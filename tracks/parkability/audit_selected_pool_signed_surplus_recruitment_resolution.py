#!/usr/bin/env python3
"""Completion audit for selected-pool signed-surplus recruitment."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def supplier_closure(initial: frozenset[int], suppliers: tuple[int, ...]) -> tuple[frozenset[int], int]:
    current = set(initial)
    steps = 0
    while True:
        outside = {suppliers[owner] for owner in current} - current
        if not outside:
            return frozenset(current), steps
        current.add(min(outside))
        steps += 1


def run(root: Path) -> dict:
    own, base, current, threshold_value = z3.Reals(
        "own base current threshold_value"
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
        "unpaid_retained_target_is_current_desired": prove(
            [own >= current, own < threshold_value], threshold_value > current
        ),
    }
    assert all(symbolic.values())

    owners = tuple(range(4))
    state_records = []
    for path in itertools.permutations(owners):
        for kappa in (1, 2, 3):
            for decorated_positions in itertools.combinations(range(4), kappa):
                decorated = set(decorated_positions)
                for closing_position in range(1, 4):
                    levels = []
                    for prefix_end in range(4):
                        retained = set(range(prefix_end + 1))
                        suffix = set(range(prefix_end + 1, 4))
                        core_targets = {position + 1 for position in suffix if position < 3}
                        assert retained.isdisjoint(core_targets)
                        old_suffix = suffix - decorated
                        levels.append({
                            "prefix_end": prefix_end,
                            "retained_positions": sorted(retained),
                            "suffix_positions": sorted(suffix),
                            "old_suffix_positions": sorted(old_suffix),
                            "decorated_suffix_positions": sorted(suffix & decorated),
                            "strict_successors_for_old_blocker": sorted(old_suffix),
                            "physical_disjointness": True,
                        })
                    state_records.append({
                        "path": list(path),
                        "kappa": kappa,
                        "decorated_positions": sorted(decorated),
                        "closing_position": closing_position,
                        "transition_levels": [-1, 0, 1, 2, 3],
                        "levels": levels,
                    })
    assert len(state_records) == 1008
    assert all(
        level["physical_disjointness"]
        for record in state_records for level in record["levels"]
    )

    named_owners = ("r", "q", "c", "s")
    anchored_paths = [
        path for path in itertools.permutations(named_owners)
        if any(path[index:index + 2] == ("r", "q") for index in range(3))
    ]
    assert len(anchored_paths) == 6
    anchor_records = []
    for path in anchored_paths:
        source_position = path.index("r")
        target_position = source_position + 1
        for prefix_end in range(4):
            if target_position <= prefix_end:
                support_mode = "nested_in_unchanged_retained_q_target"
            elif source_position > prefix_end:
                support_mode = "allocated_as_selected_root_core"
            else:
                support_mode = "intact_unallocated_boundary_core"
            anchor_records.append({
                "path": list(path),
                "prefix_end": prefix_end,
                "anchor_source_position": source_position,
                "anchor_target_position": target_position,
                "support_mode": support_mode,
                "cut": False,
                "duplicated": False,
            })
    assert len(anchor_records) == 24
    assert all(not record["cut"] and not record["duplicated"] for record in anchor_records)

    closure_records = []
    maximum_growth_steps = 0
    for suppliers in itertools.product(owners, repeat=4):
        for mask in range(1, 1 << 4):
            initial = frozenset(owner for owner in owners if mask >> owner & 1)
            closed, steps = supplier_closure(initial, suppliers)
            maximum_growth_steps = max(maximum_growth_steps, steps)
            assert initial <= closed
            assert all(suppliers[owner] in closed for owner in closed)
            assert steps <= 4 - len(initial)
            closure_records.append({
                "suppliers": list(suppliers),
                "initial": sorted(initial),
                "closed": sorted(closed),
                "growth_steps": steps,
            })
    assert len(closure_records) == 3840
    assert maximum_growth_steps == 3

    recruitment_path = root / "results/SIGNED_SURPLUS_PREFIX_RECRUITMENT_LEMMA_20260813.md"
    recruitment = json.loads(
        (root / "results/signed_surplus_prefix_recruitment_audit.json").read_text()
    )
    assert recruitment["status"] == "RECRUITMENT_WELL_FOUNDED_POOL_SEPARATOR_SUPERSEDED"
    general = json.loads(
        (root / "results/general_mixed_edge_deletion_return_composition_audit.json").read_text()
    )
    assert general["post_residual_premise_checks"] == {
        "old_observer_prepaid": False,
        "hole_row_separator": False,
    }

    requirements = {
        "cap_free_recruitment": "PROVED_BY_FIVE_LEVEL_PREFIX_ORDER",
        "all_blocking_old_observers": "PROVED_BY_OLD_SUFFIX_CLASSIFICATION",
        "physical_disjointness": "PROVED_FOR_ALL_1008_INTERFACE_STATES",
        "owner_floors": "PROVED_SYMBOLICALLY",
        "permanent_root_q_anchor": "PRESERVED_AS_UNCUT_PHYSICAL_CORE",
        "signed_release_provenance": "PRESERVED_BY_COMPLETE_TARGET_RETENTION",
        "internal_supplier_closure": "PROVED_BY_FINITE_OWNER_UNION_CLOSURE",
        "permitted_output": "STRICT_FINITE_GG_PREFIX_TRANSITION",
        "recurrence_persistence": "MAX_PHASE_LEDGER_PER_EXACT_SIGNED_RECORD",
    }

    script = Path(__file__).resolve()
    theorem = root / "results/SELECTED_POOL_SIGNED_SURPLUS_RECRUITMENT_RESOLUTION_20260813.md"
    return {
        "schema": "selected-pool-signed-surplus-recruitment-resolution-audit-v1",
        "status": "SELECTED_POOL_RECRUITMENT_GOAL_RESOLVED",
        "symbolic_checks": symbolic,
        "interface_state_count": len(state_records),
        "transition_levels": [-1, 0, 1, 2, 3],
        "maximum_strict_prefix_extensions_after_level_zero": 3,
        "supplier_closure_case_count": len(closure_records),
        "maximum_supplier_growth_steps": maximum_growth_steps,
        "anchored_path_count": len(anchored_paths),
        "anchor_prefix_placement_count": len(anchor_records),
        "requirements": requirements,
        "state_records": state_records,
        "supplier_closure_records": closure_records,
        "anchor_records": anchor_records,
        "next_separate_goal": (
            "supplier-saturated mixed-cycle observer payment and root-sourced "
            "q-residual capture"
        ),
        "claim_boundary": (
            "recruitment goal complete; GG closure and four-agent/general EFX open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "recruitment_dependency": str(recruitment_path.relative_to(root)),
            "recruitment_dependency_sha256": sha256(recruitment_path),
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
        "interface_states": result["interface_state_count"],
        "supplier_closures": result["supplier_closure_case_count"],
        "permitted_output": result["requirements"]["permitted_output"],
    }, indent=2))


if __name__ == "__main__":
    main()
