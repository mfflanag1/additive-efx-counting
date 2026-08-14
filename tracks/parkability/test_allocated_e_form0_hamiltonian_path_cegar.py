from .run_allocated_e_form0_hamiltonian_path_cegar import (
    CURRENT, hamiltonian_path_allocations,
)


def test_hamiltonian_path_allocation_family_is_exact():
    allocations = hamiltonian_path_allocations()
    assert len(allocations) == 343
    expected_goods = {
        good for goods in CURRENT.values() for good in goods
    }
    canonical = set()
    for allocation in allocations:
        assigned = [good for goods in allocation.values() for good in goods]
        assert len(assigned) == len(expected_goods)
        assert set(assigned) == expected_goods
        assert len(set(assigned)) == len(assigned)
        assert allocation["charity"] == []
        assert "p" in allocation["r"]
        canonical.add(tuple((owner, tuple(sorted(goods))) for owner, goods in sorted(allocation.items())))
    assert len(canonical) == 343
