#!/usr/bin/env python3
"""Focused regression test for minimal-Hall owner-union compression."""

import json
from pathlib import Path

try:
    from .audit_minimal_hall_owner_union_compression import run
except ImportError:
    from audit_minimal_hall_owner_union_compression import run


ROOT = Path(__file__).resolve().parents[2]


def main():
    expected = json.loads(
        (
            ROOT
            / "results"
            / "minimal_hall_owner_union_compression_audit.json"
        ).read_text()
    )
    replay = run()
    assert replay == expected
    records = replay["relation_records"]
    assert records["deficiency_one_failures"] == 0
    assert records["near_perfect_matching_failures"] == 0
    assert records["edge_extension_failures"] == 0

    theorem = (
        ROOT
        / "results"
        / "MINIMAL_HALL_OWNER_UNION_COMPRESSION_LEMMA_20260811.md"
    ).read_text()
    assert "Every minimal defect has deficiency exactly one" in theorem
    assert "two-way partition" in theorem
    assert "release-compatible owner component" in theorem
    print("minimal-Hall owner-union compression tests passed")


if __name__ == "__main__":
    main()
