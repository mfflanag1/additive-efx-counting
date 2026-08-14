import json
from pathlib import Path


def test_paid_functional_four_edge_census():
    result = json.loads(Path(
        "results/paid_functional_four_edge_census_audit.json"
    ).read_text())
    assert result["profile_count"] == 25
    assert result["functional_allocation_menu_count"] == 76_692
    assert result["all_profiles_have_paid_functional_witness"]
    assert sum(result["minimum_paid_edge_histogram"].values()) == 25
