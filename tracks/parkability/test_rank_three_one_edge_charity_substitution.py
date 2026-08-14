#!/usr/bin/env python3

from pathlib import Path

from .audit_rank_three_one_edge_charity_substitution import run


def test_all_corrected_forms_and_omissions():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "ALL_FOUR_FORMS_AND_OMISSIONS_CONSERVED"
    assert result["response_form_count"] == 4
    assert result["omission_case_count"] == 16
    assert all(result["checks"].values())
    assert all(len(record["transfer_edges"]) == 4 for record in result["records"])
