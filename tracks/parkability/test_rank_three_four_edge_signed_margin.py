#!/usr/bin/env python3

from pathlib import Path

from .audit_rank_three_four_edge_signed_margin import run


def test_signed_margin_and_all_response_payment():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "EXACT_MARGIN_IDENTITY_AND_ALL_RESPONSE_PAYMENT"
    assert all(result["checks"].values())
