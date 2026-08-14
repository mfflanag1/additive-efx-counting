#!/usr/bin/env python3

from pathlib import Path

from .audit_rank_three_disjoint_double_core_four_edge import run


def test_all_three_forms_close_conditionally():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "ALL_THREE_NORMAL_FORMS_CLOSE_CONDITIONALLY"
    assert result["normal_form_count"] == 3
    for record in result["records"]:
        assert len(record["transfer_edges"]) == 4
        assert all(record["checks"].values())


def test_shared_target_is_the_unique_nonfunctional_supplier():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    for record in result["records"]:
        targets = [edge[1] for edge in record["transfer_edges"]]
        assert targets.count("r") + targets.count("c") >= 1
        assert record["checks"]["q_must_supply_two_recipients"]
        assert record["checks"]["construction_is_not_functional"]
