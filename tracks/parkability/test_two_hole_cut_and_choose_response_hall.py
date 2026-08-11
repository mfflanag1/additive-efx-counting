#!/usr/bin/env python3
"""Focused replay for the two-hole cut-and-choose lemma."""

import json
from pathlib import Path

try:
    from .audit_two_hole_cut_and_choose_response_hall import run
except ImportError:
    from audit_two_hole_cut_and_choose_response_hall import run


ROOT = Path(__file__).resolve().parents[2]


def test_two_hole_cut_and_choose_replays():
    expected = json.loads(
        (ROOT / "results/two_hole_cut_and_choose_response_hall_audit.json").read_text()
    )
    replay = run(ROOT)
    for field in (
        "status",
        "scalar_records",
        "response_block_records",
        "support_record",
        "claim_boundary",
    ):
        assert replay[field] == expected[field]
    for field in ("script", "script_sha256", "theorem", "theorem_sha256"):
        assert replay["provenance"][field] == expected["provenance"][field]
    assert expected["status"] == "ALL_FORCED"
    assert set(expected["scalar_records"].values()) == {"unsat"}
    assert expected["response_block_records"]["full_sdr_failures"] == 0


def test_claim_boundary_keeps_live_gate_open():
    theorem = (
        ROOT / "results/TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md"
    ).read_text()
    assert "root-facing" in theorem
    assert "Strict inherited potential" in theorem
    assert "strictly more valuable" in theorem
    assert "does not prove that either 2-by-2" in theorem
