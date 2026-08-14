import json
from pathlib import Path


def test_exact_response_functional_cover_boundary():
    result = json.loads(Path(
        "results/exact_response_functional_cover_form2_audit.json"
    ).read_text())
    assert result["master_exact_value_replay"] == "sat"
    assert result["exact_relation_matches_r3"]
    assert result["allocation_count_matches"]
    assert result["functional_menu_complete_efx_count"] == 0
    assert result["unrestricted_four_edge_complete_efx_count"] > 0
