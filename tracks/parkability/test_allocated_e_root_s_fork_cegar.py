from .run_allocated_e_root_s_fork_cegar import selector_allocations


def test_root_s_fork_contains_latest_three_edge_witness():
    allocations = selector_allocations()
    witness = {
        "r": ("a0", "a1"),
        "q": ("j", "k", "q0"),
        "d": ("h", "l", "m", "gq", "gr"),
        "s": ("e", "p"),
        "charity": (),
    }
    assert any(
        all(tuple(allocation[owner]) == witness[owner] for owner in witness)
        for allocation in allocations.values()
    )
