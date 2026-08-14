from .run_allocated_e_endpoint6_root_fixed_completion_cegar import (
    root_fixed_menu,
    run,
)


def test_root_fixed_menu_is_complete_and_bounded():
    menu = root_fixed_menu()
    assert menu
    assert all(len(edges) <= 4 for _, edges in menu)
    assert callable(run)
