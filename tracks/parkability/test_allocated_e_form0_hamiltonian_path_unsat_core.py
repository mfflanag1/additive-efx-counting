from .extract_allocated_e_form0_hamiltonian_path_unsat_core import (
    CURRENT, independent_path_allocations,
)


def test_independent_path_family():
    rows = independent_path_allocations()
    expected = {good for goods in CURRENT.values() for good in goods}
    assert len(rows) == 343
    assert len({
        tuple((owner, tuple(sorted(goods))) for owner, goods in sorted(row.items()))
        for row in rows
    }) == 343
    for row in rows:
        assigned = [good for goods in row.values() for good in goods]
        assert set(assigned) == expected
        assert len(assigned) == len(set(assigned))
