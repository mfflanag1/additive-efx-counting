from .extract_allocated_e_form2_response_branch_menu_unsat_core import (
    MENU, independent_allocations_for_topology, independent_menu_allocations,
)


def test_independent_form2_response_branch_menu():
    assert len(MENU) == 9
    assert [len(independent_allocations_for_topology(row)) for row in MENU] == [
        12, 84, 343, 36, 84, 147, 147, 84, 36,
    ]
    assert len(independent_menu_allocations()) == 973
