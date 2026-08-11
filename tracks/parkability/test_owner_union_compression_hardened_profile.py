#!/usr/bin/env python3
"""Focused replay test for the hardened owner-union compression profile."""

import json
from pathlib import Path

try:
    from .audit_owner_union_compression_hardened_profile import run
except ImportError:
    from audit_owner_union_compression_hardened_profile import run


ROOT = Path(__file__).resolve().parents[2]


def main():
    source = ROOT / "results" / "owner_union_compression_hardened_profile.json"
    expected = json.loads(
        (
            ROOT / "results" / "owner_union_compression_hardened_profile_audit.json"
        ).read_text()
    )
    assert run(source) == expected
    assert expected["status"] == "VERIFIED_EFX_ESCAPE"
    assert expected["defect_record"]["minimal_defect_targets"] == ["q", "s"]
    print("owner-union compression hardened-profile tests passed")


if __name__ == "__main__":
    main()
