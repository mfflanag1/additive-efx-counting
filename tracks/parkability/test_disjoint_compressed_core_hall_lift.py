from .audit_disjoint_compressed_core_hall_lift import audit_size


def test_three_and_four_owner_hall_census():
    for size in (3, 4):
        result = audit_size(size)
        assert result["nonempty_response_graph_count"] == (2 ** size - 1) ** size
        assert result["perfect_matching_count"] + result["hall_deficient_count"] \
            == result["nonempty_response_graph_count"]
        assert result["minimal_deficiency_one_hole_checks"] > 0
