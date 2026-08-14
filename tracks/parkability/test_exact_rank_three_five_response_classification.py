#!/usr/bin/env python3

from pathlib import Path

from .audit_exact_rank_three_five_response_classification import run


def test_exact_five_response_classification():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "EXACTLY_TWO_RESPONSE_FORMS_SURVIVE"
    assert result["checks"]["q_budget_forces_q_to_r_from_q_to_d"]
    assert result["checks"]["fourth_form_has_rank_four_matching"]
    assert result["checks"]["surviving_form_indices"] == [0, 2]
