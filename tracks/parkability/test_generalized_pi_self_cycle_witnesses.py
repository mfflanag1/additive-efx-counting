import json
from pathlib import Path


def test_generalized_pi_self_cycle_witness_audit():
    result = json.loads(Path(
        "results/generalized_pi_self_cycle_counterprofile_audit.json"
    ).read_text())
    assert result["status"] == (
        "ALL_STRENGTHENED_COUNTERPROFILES_EXCLUDED_BY_GENERALIZED_SELF_PI"
    )
    assert len(result["records"]) == 4
    assert all(record["valid_generalized_self_pi"] for record in result["records"])
