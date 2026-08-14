from .run_allocated_e_form2_three_topology_menu_cegar import (
    CURRENT, MENU, allocations_for_topology, menu_allocations,
)


def test_form2_menu_allocation_family():
    expected = {good for goods in CURRENT.values() for good in goods}
    rows = menu_allocations()
    assert len(MENU) == 3
    assert [len(allocations_for_topology(topology)) for topology in MENU] == [12, 84, 343]
    assert len(rows) == 439
    for allocation in rows:
        assigned = [good for goods in allocation.values() for good in goods]
        assert set(assigned) == expected
        assert len(assigned) == len(set(assigned))
        assert allocation["charity"] == []
