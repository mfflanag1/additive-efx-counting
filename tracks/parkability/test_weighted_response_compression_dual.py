#!/usr/bin/env python3
"""Focused regression test for weighted response compression."""

import json
from pathlib import Path

try:
    from .audit_weighted_response_compression_dual import run
except ImportError:
    from audit_weighted_response_compression_dual import run


ROOT = Path(__file__).resolve().parents[2]


def main():
    expected = json.loads(
        (
            ROOT / "results" / "weighted_response_compression_dual_audit.json"
        ).read_text()
    )
    replay = run()
    assert replay["status"] == "ALL_FORCED"
    assert replay["scalar_records"] == expected["scalar_records"]
    assert len(replay["scalar_records"]) == 5

    theorem = (
        ROOT / "results" / "WEIGHTED_RESPONSE_COMPRESSION_DUAL_LEMMA_20260811.md"
    ).read_text()
    assert "canonical global packet selector" in theorem
    assert "at most one EFX wall" in theorem
    assert "strict recapture wall" in theorem
    print("weighted response-compression dual tests passed")


if __name__ == "__main__":
    main()
