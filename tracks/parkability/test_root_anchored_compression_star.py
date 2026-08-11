#!/usr/bin/env python3
"""Focused regression test for the root-anchored compression star."""

import json
from pathlib import Path

try:
    from .audit_root_anchored_compression_star import run
except ImportError:
    from audit_root_anchored_compression_star import run


ROOT = Path(__file__).resolve().parents[2]


def main():
    expected = json.loads(
        (ROOT / "results" / "root_anchored_compression_star_audit.json").read_text()
    )
    replay = run()
    assert replay["status"] == "ALL_FORCED"
    assert replay["scalar_records"] == expected["scalar_records"]
    assert replay["support_record"] == expected["support_record"]

    theorem = (
        ROOT / "results" / "ROOT_ANCHORED_COMPRESSION_STAR_LEMMA_20260811.md"
    ).read_text()
    assert "unique missing source `d` is never `r`" in theorem
    assert "global recapture potential" in theorem
    assert "strict four-level order" in theorem
    print("root-anchored compression-star tests passed")


if __name__ == "__main__":
    main()
