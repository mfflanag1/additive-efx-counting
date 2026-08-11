import json
from pathlib import Path

from .audit_fixed_u_charity_tree_countermodel import run


ROOT = Path(__file__).resolve().parents[2]


def test_fixed_u_charity_tree_countermodel_replays_exactly():
    source = ROOT / "results/fixed_u_charity_tree_countermodel.json"
    expected = json.loads(
        (ROOT / "results/fixed_u_charity_tree_countermodel_audit.json").read_text()
    )
    assert run(source) == expected


def test_fixed_u_charity_tree_countermodel_decides_full_topology_menu():
    expected = json.loads(
        (ROOT / "results/fixed_u_charity_tree_countermodel_audit.json").read_text()
    )
    assert expected["status"] == "VERIFIED_COUNTERMODEL"
    assert expected["source_margin_frontier"]["exchange_pairs_checked"] == 512
    assert expected["charity_rooted_topologies"]["by_owner_count"] == {
        "1": 4,
        "2": 12,
        "3": 36,
        "4": 64,
    }
    assert (
        expected["charity_rooted_topologies"]["all_efx_improving_packet_systems"]
        == "UNSAT"
    )
