from .audit_whole_h_release_collision_or_parked_support import COLLISION_COMMIT


def test_collision_theorem_dependency_is_full_sha():
    assert len(COLLISION_COMMIT) == 40
    int(COLLISION_COMMIT, 16)
