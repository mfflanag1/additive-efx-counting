from .run_allocated_e_endpoint6_one_packet_repair_cegar import repair_allocations, run


def test_endpoint6_repair_menu():
    repairs = repair_allocations()
    assert len(repairs) == 17
    assert {donor for donor, _, _ in repairs} == {"r", "d", "s"}
    assert callable(run)
