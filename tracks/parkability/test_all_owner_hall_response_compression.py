#!/usr/bin/env python3
"""Focused regression test for all-owner Hall response compression."""

import json
from pathlib import Path

try:
    from .audit_all_owner_hall_response_compression import run
except ImportError:
    from audit_all_owner_hall_response_compression import run


ROOT = Path(__file__).resolve().parents[2]


def main():
    expected = json.loads(
        (
            ROOT
            / "results"
            / "all_owner_hall_response_compression_audit.json"
        ).read_text()
    )
    replay = run()
    assert replay == expected
    assert replay["relation_records"]["minimal_all_target_defects"] > 0
    assert replay["relation_records"]["neighborhood_size_histogram"] == {
        "3": replay["relation_records"]["minimal_all_target_defects"]
    }
    assert replay["relation_records"]["three_target_matching_failures"] == 0
    assert replay["relation_records"]["response_edges_checked"] > 0
    assert replay["relation_records"]["edge_extension_failures"] == 0

    theorem = (
        ROOT / "results" / "ALL_OWNER_HALL_RESPONSE_COMPRESSION_LEMMA_20260811.md"
    ).read_text()
    assert "deficiency exactly one" in theorem
    assert "every prescribed response edge extends" in theorem
    assert "missing-source residual" in theorem
    print("all-owner Hall response-compression tests passed")


if __name__ == "__main__":
    main()
