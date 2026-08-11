#!/usr/bin/env python3
"""Focused regression test for lex-sacrificed response compression."""

import json
from pathlib import Path

try:
    from .audit_lex_sacrificed_response_compression import run
except ImportError:
    from audit_lex_sacrificed_response_compression import run


ROOT = Path(__file__).resolve().parents[2]


def main():
    expected = json.loads(
        (
            ROOT / "results" / "lex_sacrificed_response_compression_audit.json"
        ).read_text()
    )
    replay = run()
    assert replay["status"] == "ALL_FORCED"
    assert replay["scalar_records"] == expected["scalar_records"]

    theorem = (
        ROOT / "results" / "LEX_SACRIFICED_RESPONSE_COMPRESSION_LEMMA_20260811.md"
    ).read_text()
    assert "two-sided star" in theorem
    assert "If the missing source is the singleton owner" in theorem
    assert "strict global\nlexicographic improvement" in theorem
    print("lex-sacrificed response-compression tests passed")


if __name__ == "__main__":
    main()
