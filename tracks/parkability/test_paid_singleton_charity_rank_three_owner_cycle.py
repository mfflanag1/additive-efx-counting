#!/usr/bin/env python3

from pathlib import Path

from .audit_paid_singleton_charity_rank_three_owner_cycle import run


def test_charity_exclusion_and_forced_owner_cycles():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == (
        "PAID_SOURCE_CHARITY_RESPONSE_EXCLUDED_AND_FIVE_EDGE_CYCLE_FORCED"
    )
    assert result["checks"][
        "base_safe_singleton_not_base_or_current_desired_by_paid_source"
    ]
    assert result["checks"]["rank_three_matching_forms_checked"] == 4
    assert result["checks"]["every_form_contains_owner_cycle"]
    assert result["checks"]["cycle_length_histogram"] == {"2": 2, "3": 2}
