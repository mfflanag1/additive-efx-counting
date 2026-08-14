from .run_allocated_e_root_charity_exchange_cegar import selector_allocations


def test_root_charity_selector_family_is_two_exact_topologies():
    allocations = selector_allocations()
    # Y_r has three goods. The family contains the charity-to-r endpoint
    # with no root transfer plus every nonempty root-to-d subset under both
    # charity placements.
    assert len(allocations) == 15
    for allocation in allocations.values():
        assert allocation["charity"] == []
        assert "p" in allocation["r"] or "p" in allocation["d"]
    assert sum(
        not any(good in allocation["d"] for good in ("a0", "a1", "h"))
        for allocation in allocations.values()
    ) == 2
