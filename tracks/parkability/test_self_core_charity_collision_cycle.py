from .audit_self_core_charity_collision_cycle import cycles


def test_fixed_point_free_function_has_cycle():
    assert cycles((1, 0, 1)) == ((0, 1),)
    assert cycles((1, 2, 0, 2)) == ((0, 1, 2),)
