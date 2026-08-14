from .audit_gg_old_root_core_exterior_dominance_independent import run


def test_gg_old_root_core_exterior_dominance_independent() -> None:
    result = run()
    assert result["status"] == "INDEPENDENT_INTEGER_REPLAY_UNSAT"
    assert result["ordered_candidates_checked"] > 0
    assert result["feasible_chains"] == 0
    assert not result["imports_primary_audit"]
    assert not result["imports_z3"]
