import json
from pathlib import Path


def test_two_survivor_named_topology_refutation_audit():
    path = Path("results/two_survivor_named_topology_refutation_audit.json")
    result = json.loads(path.read_text())
    assert result["all_exact_relation_replays_match"]
    assert result["all_named_families_have_no_efx"]
    assert result["all_profiles_have_unrestricted_four_edge_efx"]
    assert {record["form_index"] for record in result["records"]} == {0, 2}
