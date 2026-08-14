from .run_allocated_e_root_retention_new_debt_cegar import CREDITOR, RETAINED, run


def test_root_retention_debt_cases_are_typed():
    assert set(RETAINED) == {3, 6}
    assert CREDITOR == {3: "s", 6: "q"}
    assert callable(run)
