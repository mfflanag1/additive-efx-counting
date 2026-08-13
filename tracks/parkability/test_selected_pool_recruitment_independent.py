from pathlib import Path

from .audit_selected_pool_recruitment_independent import run


ROOT = Path(__file__).resolve().parents[2]


def test_independent_prefix_reconstruction() -> None:
    result = run(ROOT)
    assert result["status"] == "INDEPENDENT_PREFIX_RECONSTRUCTION_PASSED"
    assert result["interface_states"] == 1008
    assert result["prefix_level_checks"] == 4032
    assert result["old_blocker_checks"] > 0
    assert result["anchor_checks"] == 24
    assert "does not import" in result["implementation_relation"]
