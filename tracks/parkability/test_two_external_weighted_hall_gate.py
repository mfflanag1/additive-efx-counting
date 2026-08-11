from pathlib import Path

try:
    from .audit_flower_weighted_residual_complement_polarity import (
        run as run_polarity_audit,
    )
    from .audit_two_external_weighted_hall_hardened_countermodel import (
        run as run_countermodel_audit,
    )
except ImportError:
    from audit_flower_weighted_residual_complement_polarity import (
        run as run_polarity_audit,
    )
    from audit_two_external_weighted_hall_hardened_countermodel import (
        run as run_countermodel_audit,
    )


ROOT = Path(__file__).resolve().parents[2]


def test_weighted_residual_complement_polarity_is_forced():
    result = run_polarity_audit()
    assert result["status"] == "FORCED"
    assert result["record"]["status"] == "unsat"


def test_hardened_local_no_closure_replays_exactly():
    source = ROOT / "results/two_external_weighted_hall_hardened_countermodel.json"
    result = run_countermodel_audit(source)
    assert result["status"] == "VERIFIED"
    assert result["residual_partition_count"] == 1024
    assert result["classification_counts"]["HALL_DEFICIENT"] == 1024
    assert result["classification_counts"].get("EFX", 0) == 0
    assert result["classification_counts"].get("INTERNAL_SDR", 0) == 0


def test_radius_two_excluded_survivor_replays_exactly():
    source = (
        ROOT
        / "results/two_external_weighted_hall_radius2_hardened_countermodel.json"
    )
    result = run_countermodel_audit(source)
    assert result["status"] == "VERIFIED"
    assert result["residual_partition_count"] == 256
    assert result["classification_counts"]["HALL_DEFICIENT"] == 256
