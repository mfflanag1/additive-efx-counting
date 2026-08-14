from .audit_allocated_e_form2_three_topology_menu import (
    MENU, allocations_for_topology, independent_menu_counts,
)


def test_independent_menu_counts():
    per_topology, union_count = independent_menu_counts()
    assert per_topology == [12, 84, 343]
    assert union_count == 439


def test_every_declared_edge_is_used():
    for topology in MENU:
        for allocation in allocations_for_topology(topology):
            holder = {
                good: owner for owner, goods in allocation.items() for good in goods
            }
            for supplier, recipient in topology:
                source_goods = {"p"} if supplier == "charity" else {
                    good for good, original in {
                        "a0": "r", "a1": "r", "h": "r",
                        "j": "q", "k": "q", "q0": "q",
                        "m": "d", "gq": "d", "gr": "d",
                        "l": "s", "e": "s", "p": "charity",
                    }.items() if original == supplier
                }
                assert any(holder[good] == recipient for good in source_goods)
