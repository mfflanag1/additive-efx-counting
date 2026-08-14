from .audit_charity_collision_supplier_recruitment import OWNERS, SUPPLIER


def test_outside_supplier_strictly_grows_owner_union():
    for cycle in (("r", "q"), ("q", "s", "r")):
        assert SUPPLIER not in cycle
        assert len(set(cycle) | {SUPPLIER}) == len(cycle) + 1
    assert set(OWNERS) == {"r", "q", "d", "s"}
