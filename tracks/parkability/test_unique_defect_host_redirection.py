from pathlib import Path

try:
    from .search_unique_defect_host_redirection import run
except ImportError:
    from search_unique_defect_host_redirection import run


def test_host_to_bad_reduction_small_sample(tmp_path: Path):
    result = run(
        n=4,
        m=5,
        cap=3,
        profiles=10,
        seed=20260803,
        output=tmp_path / "host-redirection.json",
    )

    assert result["status"] == "HOST_TO_BAD_REDUCTION_SURVIVES_SEARCH"
    assert result["full_unique_defect_count"] > 0
    assert result["redirected_absorption_count"] > 0
    assert result["other_redirected_defect_count"] == 0
    assert (
        result["redirected_absorption_count"]
        + result["redirected_two_cycle_count"]
        == result["full_unique_defect_count"]
    )
