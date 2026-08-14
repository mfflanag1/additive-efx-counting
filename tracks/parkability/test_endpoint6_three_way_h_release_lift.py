from .audit_endpoint6_three_way_h_release_lift import EXPECTED, PACKET_FORMS
from .run_allocated_e_endpoint6_root_fixed_completion_cegar import support_edges


def test_three_release_allocations_preserve_a_release_h_and_use_four_edges():
    assert len(EXPECTED) == len(PACKET_FORMS) == 3
    for allocation in EXPECTED:
        assert allocation["r"] == ["a0", "a1"]
        assert "h" not in allocation["r"]
        assert len(support_edges(allocation)) <= 4
