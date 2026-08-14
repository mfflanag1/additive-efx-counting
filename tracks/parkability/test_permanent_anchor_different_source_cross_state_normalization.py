from pathlib import Path

from .audit_permanent_anchor_different_source_cross_state_normalization import run


def test_permanent_anchor_different_source_cross_state_normalization():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "COMMON_PROBE_SAFE_NORMALIZATION_OR_SOURCE_COLLISION"
    assert result["source_pair_count"] == 3
    assert result["common_probe_edge_count"] == 2
    assert result["desire_transport"]
    assert result["unsafe_gives_desired_deletion"]
    assert result["finite_cardinality_descent"]
    assert result["source_collision_or_distinct_exhaustive"]
