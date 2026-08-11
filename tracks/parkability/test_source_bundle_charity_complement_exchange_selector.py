import json
from pathlib import Path

from .audit_source_bundle_charity_complement_exchange_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_source_bundle_charity_complement_exchange_selector_replays():
    expected = json.loads(
        (ROOT / "results/source_bundle_charity_complement_exchange_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_source_bundle_charity_complement_exchange_selector_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["bilateral_partitions_checked"] > 0
    assert result["charity_exchange_partitions_checked"] > 0
    assert result["all_two_owner_pool_partitions_checked"] > 0
    assert result["initial_final_transfer_pairs_checked"] > 0
    assert result["core_partition_conservation"]
    assert result["charity_exchange_conservation"]
    assert result["final_charity_singleton"]
    assert result["at_most_one_nontrivial_transfer_component"]
    assert all(value == "unsat" for value in result["symbolic_checks"].values())
