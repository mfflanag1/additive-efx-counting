from .run_allocated_e_form2_response_branch_menu_cegar import (
    MENU, SIX_RESPONSE_BRANCHES, menu_allocations,
)
from .run_allocated_e_form2_three_topology_menu_cegar import (
    CURRENT, allocations_for_topology,
)


def test_form2_response_branch_menu():
    expected = {good for goods in CURRENT.values() for good in goods}
    assert len(SIX_RESPONSE_BRANCHES) == 6
    assert len(MENU) == 9
    assert [len(allocations_for_topology(row)) for row in MENU] == [
        12, 84, 343, 36, 84, 147, 147, 84, 36,
    ]
    rows = menu_allocations()
    assert len(rows) == 973
    for allocation in rows:
        assigned = [good for goods in allocation.values() for good in goods]
        assert set(assigned) == expected
        assert len(assigned) == len(set(assigned))
        assert allocation["charity"] == []
