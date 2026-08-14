from .run_allocated_e_endpoint6_single_root_release_cegar import (
    single_root_release_menu,
    run,
)


def test_single_root_release_menu():
    menu = single_root_release_menu()
    assert len(menu) == 10_428
    assert {tuple(sorted(allocation["r"])) for allocation in menu} == {
        ("a0", "a1"), ("a0", "h"), ("a1", "h"),
    }
    assert callable(run)
