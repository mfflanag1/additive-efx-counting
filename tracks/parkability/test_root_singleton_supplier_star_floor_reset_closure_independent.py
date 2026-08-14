from .audit_root_singleton_supplier_star_floor_reset_closure_independent import run


def test_root_singleton_supplier_star_floor_reset_closure_independent() -> None:
    result = run()
    assert result["status"] == (
        "INDEPENDENT_ROOT_SINGLETON_STAR_CLOSURE_REPLAY_PASSED"
    )
    assert result["arithmetic_cases_checked"] > 0
    assert result["arithmetic_failures"] == 0
    assert result["support_cases_checked"] > 0
    assert result["support_failures"] == 0
    assert not result["imports_primary_audit"]
    assert not result["imports_z3"]
    assert result["full_T_L_times_theorem_closed_in_replayed_statement"]
    assert not result["full_GG_closed"]
    assert not result["general_EFX_closed"]
