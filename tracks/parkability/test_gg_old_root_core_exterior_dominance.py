from .audit_gg_old_root_core_exterior_dominance import run


def test_gg_old_root_core_exterior_dominance() -> None:
    result = run()
    assert result["status"] == "ROOT_HELD_T_L_TIMES_SURVIVOR_CONTRADICTED"
    assert result["scalar_chain_qf_lra_unsat"]
    assert result["support_cases_checked"] > 0
    assert result["packet_is_base_contained"]
    assert result["old_root_core_is_exterior"]
    assert result["old_root_core_is_base_desired"]
    assert result["permanent_old_edge_retained_at_fixed_label"]
    assert result["new_root_or_anchor_label_is_contracted_progress"]
    assert result["root_held_collision_closed"]
