#!/usr/bin/env python3
"""Focused regression test for the top-core residual-reset lemma."""

import json
from pathlib import Path

try:
    from .audit_top_core_residual_reset import run
except ImportError:
    from audit_top_core_residual_reset import run


ROOT = Path(__file__).resolve().parents[2]


def main():
    expected = json.loads(
        (ROOT / "results" / "top_core_residual_reset_audit.json").read_text()
    )
    replay = run()
    assert replay["status"] == "ALL_FORCED"
    assert replay["scalar_records"] == expected["scalar_records"]

    theorem = (
        ROOT / "results" / "TOP_CORE_RESIDUAL_RESET_LEMMA_20260811.md"
    ).read_text()
    assert "canonically factors back" in theorem
    assert "does not by itself prove a strict global-potential increase" in theorem
    print("top-core residual-reset tests passed")


if __name__ == "__main__":
    main()
