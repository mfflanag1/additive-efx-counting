from .audit_nonroot_normalization_bypass_collision_gap import run


def test_nonroot_normalization_bypass_collision_gap(tmp_path):
    result = run(tmp_path / "audit.json")
    assert result["status"] == "IMPORTED_FULL_COLLISION_COMPOSITION_GAP_CONFIRMED"
    assert result["local_positive_additive_witness_status"] == "sat"
    assert result["normalized_response_avoids_packet"]
    assert not result["nonroot_whole_hit_dependency_applies"]
    assert not result["root_holder_star_dependency_applies"]
    assert not result["full_GG_countermodel"]
