from pathlib import Path

try:
    from .audit_unique_defect_handoff import run
except ImportError:
    from audit_unique_defect_handoff import run


def test_unique_defect_handoff_corpus(tmp_path: Path):
    result = run(
        Path("results/partial_hall_threshold_plateau_completion_analysis.json"),
        tmp_path / "unique-defect-handoff.json",
    )

    assert result["status"] == "CANONICAL_HANDOFFS_VERIFIED"
    assert result["identity_unique_defect_one_step_count"] == 4323
    assert result["canonical_bad_source_handoff_count"] == 4320
    assert result["verified_canonical_handoff_count"] == 4320
