from pathlib import Path

from .audit_selected_pool_signed_surplus_recruitment_resolution import run


ROOT = Path(__file__).resolve().parents[2]


def test_recruitment_goal_requirements_are_all_discharged() -> None:
    result = run(ROOT)
    assert result["status"] == "SELECTED_POOL_RECRUITMENT_GOAL_RESOLVED"
    assert result["requirements"] == {
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


def test_prefix_transition_is_finite_and_exhaustive() -> None:
    result = run(ROOT)
    assert result["interface_state_count"] == 1008
    assert result["transition_levels"] == [-1, 0, 1, 2, 3]
    assert result["maximum_strict_prefix_extensions_after_level_zero"] == 3
    assert all(result["symbolic_checks"].values())


def test_supplier_closure_is_finite() -> None:
    result = run(ROOT)
    assert result["supplier_closure_case_count"] == 3840
    assert result["maximum_supplier_growth_steps"] == 3
    assert all(
        record["growth_steps"] <= 4 - len(record["initial"])
        for record in result["supplier_closure_records"]
    )


def test_permanent_anchor_is_explicitly_preserved() -> None:
    result = run(ROOT)
    assert result["anchored_path_count"] == 6
    assert result["anchor_prefix_placement_count"] == 24
    assert all(not record["cut"] for record in result["anchor_records"])
    assert all(not record["duplicated"] for record in result["anchor_records"])
    assert {
        record["support_mode"] for record in result["anchor_records"]
    } == {
        "nested_in_unchanged_retained_q_target",
        "allocated_as_selected_root_core",
        "intact_unallocated_boundary_core",
    }
