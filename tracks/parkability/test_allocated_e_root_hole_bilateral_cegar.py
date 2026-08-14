from .run_allocated_e_root_hole_bilateral_cegar import selector_allocations


def test_root_hole_bilateral_family_contains_reciprocal_exchange():
    allocations = selector_allocations()
    assert len(allocations) > 15
    witness = {
        owner: tuple(goods) for owner, goods in {
            "r": ["a1", "h", "gq", "gr", "p"],
            "q": ["j", "k", "q0"],
            "d": ["a0", "m"],
            "s": ["l", "e"],
            "charity": [],
        }.items()
    }
    assert any(
        all(tuple(allocation[owner]) == witness[owner] for owner in witness)
        for allocation in allocations.values()
    )
