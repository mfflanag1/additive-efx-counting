#!/usr/bin/env python3
"""Regression checks for the packet-minimum flower normal form."""

import json
from pathlib import Path

try:
    from .analyze_two_leaf_hub_split_census import run as run_hub_split_census
    from .audit_charity_rooted_hub_split import run as run_hub_split_audit
    from .audit_packet_charity_replacement import run as run_packet_charity_audit
    from .audit_three_target_hub_hall_patterns import run as run_hub_hall_audit
    from .decide_three_target_leaf_mutual_trap import (
        audit_frozen as audit_leaf_mutual_frozen,
        run as run_leaf_mutual_gate,
    )
    from .decide_three_nonsingleton_flower_full_capture_swap_gate import run as run_swap_gate
except ImportError:
    from analyze_two_leaf_hub_split_census import run as run_hub_split_census
    from audit_charity_rooted_hub_split import run as run_hub_split_audit
    from audit_packet_charity_replacement import run as run_packet_charity_audit
    from audit_three_target_hub_hall_patterns import run as run_hub_hall_audit
    from decide_three_target_leaf_mutual_trap import (
        audit_frozen as audit_leaf_mutual_frozen,
        run as run_leaf_mutual_gate,
    )
    from decide_three_nonsingleton_flower_full_capture_swap_gate import run as run_swap_gate


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    support = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_support_mask_audit.json").read_text()
    )
    assert support["status"] == "OPEN"
    assert support["mask_count"] == 64
    assert support["counts"] == {"unsat": 60, "sat": 4, "unknown": 0}

    family = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_packet_min_family_audit.json").read_text()
    )
    assert family["status"] == "CLASSIFIED"
    assert family["cell_count"] == 6144
    assert family["counts"] == {"IMPOSSIBLE": 5124, "sat": 1020}
    expected = {
        ("c", "c"): {"IMPOSSIBLE": 1404, "sat": 132, "unknown": 0},
        ("s", "s"): {"IMPOSSIBLE": 1416, "sat": 120, "unknown": 0},
        ("c", "s"): {"IMPOSSIBLE": 1152, "sat": 384, "unknown": 0},
        ("s", "c"): {"IMPOSSIBLE": 1152, "sat": 384, "unknown": 0},
    }
    for summary in family["summaries"]:
        key = (summary["left_bottom_source"], summary["right_bottom_source"])
        assert summary["classification_verified"]
        assert summary["counts"] == expected[key]
        signatures = summary["survivor_signature_counts"]
        assert all(entry["aq_support"] == entry["ar_support"] == "both" for entry in signatures)
        if key[0] != key[1]:
            assert len(signatures) == 16
            assert all(entry["order_count"] == 24 for entry in signatures)
        elif key == ("c", "c"):
            assert sorted(entry["order_count"] for entry in signatures) == [12, 12, 12, 24, 24, 24, 24]
        else:
            assert sorted(entry["order_count"] for entry in signatures) == [8, 8, 8, 24, 24, 24, 24]

    witness = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_full_q_capture_witness.json").read_text()
    )
    assert witness["status"] == "sat"
    assert witness["aq_support"] == witness["ar_support"] == "both"
    assert witness["empty_rest"] == ["bq_rest", "tq_rest"]

    improvement = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_full_q_capture_improvement.json").read_text()
    )
    partial = improvement["nearest_partial_improvement"]
    assert partial["status"] == "SAT"
    assert partial["minimum_moved_goods"] == 2
    assert any(good.startswith("ar_bq") for good in partial["allocation"]["r"])
    assert any(good.startswith("aq_br") for good in partial["allocation"]["q"])
    assert partial["allocation"]["_"] == ["f"]

    swap_audit = json.loads(
        (ROOT / "results" / "bilateral_swap_obstruction_audit.json").read_text()
    )
    assert swap_audit["status"] == "ALL_FORCED"
    assert len(swap_audit["records"]) == 4
    swap_theorem = (
        ROOT / "results" / "BILATERAL_SWAP_OBSTRUCTION_LEMMA_20260810.md"
    ).read_text()
    assert "Agent `r` cannot fail any comparison" in swap_theorem
    assert "Wall-to-edge consequence" in swap_theorem

    gate = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_full_capture_swap_gate.json").read_text()
    )
    assert run_swap_gate(True, True) == gate
    assert gate["status"] == "sat"
    assert gate["require_source_safe_improving_pair"]
    assert gate["block_priority_directed_pair_exchanges"]
    assert not gate["block_three_good_owner_paths"]
    assert not gate["block_charity_packet_replacements"]
    assert any(
        pair["improves_r"] and pair["source_safe"]
        for pair in gate["pair_diagnostics"]
    )
    gate_improvement = json.loads(
        (
            ROOT
            / "results"
            / "three_nonsingleton_flower_full_capture_swap_gate_improvement.json"
        ).read_text()
    )
    assert gate_improvement["nearest_partial_improvement"]["minimum_moved_goods"] == 3
    assert gate_improvement["nearest_complete_improvement"]["minimum_moved_goods"] == 3
    primary_graph = gate_improvement["nearest_partial_improvement"]["transfer_multigraph"]
    assert primary_graph["base_charity_cardinality"] == 1
    assert primary_graph["new_charity_cardinality"] == 2
    assert primary_graph["nontrivial_components"][0]["slots"] == ["q", "c", "_"]
    path_gate = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_full_capture_path_gate.json").read_text()
    )
    path_replay = run_swap_gate(True, True, True)
    assert path_replay["status"] == path_gate["status"] == "sat"
    assert path_replay["block_three_good_owner_paths"]
    assert path_gate["block_three_good_owner_paths"]
    assert not path_gate["block_charity_packet_replacements"]
    path_improvement = json.loads(
        (
            ROOT
            / "results"
            / "three_nonsingleton_flower_full_capture_path_gate_improvement.json"
        ).read_text()
    )
    assert path_improvement["nearest_partial_improvement"]["minimum_moved_goods"] == 3
    assert path_improvement["nearest_complete_improvement"]["minimum_moved_goods"] == 7
    assert min(path_improvement["nearest_partial_improvement"]["owner_charity_slack_vector"]) >= 0
    path_graph = path_improvement["nearest_partial_improvement"]["transfer_multigraph"]
    assert path_graph["base_charity_cardinality"] == 1
    assert path_graph["new_charity_cardinality"] == 2
    assert path_graph["nontrivial_components"][0]["slots"] == ["q", "_"]
    complete_graph = path_improvement["nearest_complete_improvement"]["transfer_multigraph"]
    assert complete_graph["nontrivial_components"][0]["slots"] == [
        "r", "q", "c", "s", "_"
    ]
    packet_gate = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_full_capture_packet_gate.json").read_text()
    )
    packet_replay = run_swap_gate(True, True, True, True)
    assert packet_replay["status"] == packet_gate["status"] == "sat"
    assert packet_gate["block_charity_packet_replacements"]
    packet_improvement = json.loads(
        (
            ROOT
            / "results"
            / "three_nonsingleton_flower_full_capture_packet_gate_improvement.json"
        ).read_text()
    )
    assert packet_improvement["nearest_partial_improvement"]["minimum_moved_goods"] == 3
    assert packet_improvement["nearest_complete_improvement"]["minimum_moved_goods"] == 3
    packet_graph = packet_improvement["nearest_partial_improvement"]["transfer_multigraph"]
    assert packet_graph["nontrivial_components"][0]["slots"] == ["r", "c", "s"]
    packet_complete_graph = packet_improvement["nearest_complete_improvement"][
        "transfer_multigraph"
    ]
    assert packet_complete_graph["nontrivial_components"][0]["slots"] == [
        "r", "c", "s", "_"
    ]
    arm_hub_gate_path = (
        ROOT / "results" / "three_nonsingleton_flower_full_capture_arm_hub_gate.json"
    )
    arm_hub_gate = json.loads(arm_hub_gate_path.read_text())
    arm_hub_replay = run_swap_gate(True, True, True, True, True)
    assert arm_hub_replay["status"] == arm_hub_gate["status"] == "sat"
    assert arm_hub_replay["block_arm_owner_hub_splits"]
    assert arm_hub_gate["status"] == "sat"
    assert arm_hub_gate["block_arm_owner_hub_splits"]
    arm_hub_census = json.loads(
        (
            ROOT
            / "results"
            / "three_nonsingleton_flower_arm_hub_gate_split_census.json"
        ).read_text()
    )
    assert run_hub_split_census(arm_hub_gate_path) == arm_hub_census
    assert arm_hub_census["counts"] == {
        "eligible": 5436,
        "open_champion_source": 1892,
        "pi_response_matching": 3542,
        "response_hall_deficient": 2,
    }
    assert arm_hub_census["by_hub"]["c"] == {
        "eligible": 6,
        "open_champion_source": 2,
        "pi_response_matching": 2,
        "response_hall_deficient": 2,
    }
    arm_hub_improvement = json.loads(
        (
            ROOT
            / "results"
            / "three_nonsingleton_flower_full_capture_arm_hub_gate_improvement.json"
        ).read_text()
    )
    assert arm_hub_improvement["nearest_partial_improvement"]["minimum_moved_goods"] == 2
    assert arm_hub_improvement["nearest_complete_improvement"]["minimum_moved_goods"] == 5
    assert arm_hub_improvement["nearest_complete_improvement"]["transfer_multigraph"][
        "nontrivial_components"
    ][0]["slots"] == ["q", "c", "s", "_"]
    arm_response_gate_path = (
        ROOT / "results" / "three_nonsingleton_flower_full_capture_arm_response_gate.json"
    )
    arm_response_gate = json.loads(arm_response_gate_path.read_text())
    assert arm_response_gate["status"] == "sat"
    assert arm_response_gate["block_arm_owner_hub_splits"]
    assert arm_response_gate["block_arm_owner_response_matchings"]
    arm_response_census = json.loads(
        (
            ROOT
            / "results"
            / "three_nonsingleton_flower_arm_response_gate_split_census.json"
        ).read_text()
    )
    assert run_hub_split_census(arm_response_gate_path) == arm_response_census
    assert arm_response_census["by_hub"]["c"] == {}
    assert arm_response_census["by_hub"]["q"] == {
        "efx": 1,
        "eligible": 6,
        "open_champion_source": 4,
        "response_hall_deficient": 1,
    }
    gate_note = (
        ROOT / "results" / "FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md"
    ).read_text()
    assert "release compatibility" in gate_note
    assert "component-growth theorem" in gate_note
    assert "transfer multigraph" in gate_note
    assert "hub-splitting component" in gate_note
    component_theorem = (
        ROOT / "results" / "GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA.md"
    ).read_text()
    assert "charity cardinalities may differ" in component_theorem
    assert "Distinguished lex-component corollary" in component_theorem
    packet_charity = json.loads(
        (ROOT / "results" / "packet_charity_replacement_obstruction_audit.json").read_text()
    )
    assert run_packet_charity_audit() == packet_charity
    assert packet_charity["status"] == "ALL_FORCED"
    assert len(packet_charity["records"]) == 4
    packet_charity_theorem = (
        ROOT / "results" / "PACKET_CHARITY_REPLACEMENT_OBSTRUCTION_LEMMA_20260810.md"
    ).read_text()
    assert "opposite aggregate signs" in packet_charity_theorem
    assert "arbitrary-packet and cap-free" in packet_charity_theorem

    hub_split = json.loads(
        (ROOT / "results" / "charity_rooted_hub_split_obstruction_audit.json").read_text()
    )
    assert run_hub_split_audit() == hub_split
    assert hub_split["status"] == "ALL_FORCED"
    assert len(hub_split["records"]) == 4
    hub_split_theorem = (
        ROOT / "results" / "CHARITY_ROOTED_HUB_SPLIT_OBSTRUCTION_LEMMA_20260810.md"
    ).read_text()
    assert "label records the whole offered set" in hub_split_theorem
    assert "actual most-envious sources" in hub_split_theorem
    assert "need not equal the wall observer" in hub_split_theorem
    response_hall_theorem = (
        ROOT / "results" / "HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810.md"
    ).read_text()
    assert "Strong-envy observers" in response_hall_theorem
    assert "system of distinct representatives" in response_hall_theorem

    hub_hall = json.loads(
        (ROOT / "results" / "three_target_hub_hall_pattern_audit.json").read_text()
    )
    assert run_hub_hall_audit() == hub_hall
    assert hub_hall["status"] == "CLASSIFIED"
    assert hub_hall["graph_count"] == 64
    assert hub_hall["counts"] == {
        "minimum_hall_size_1": 29,
        "minimum_hall_size_2": 2,
        "minimum_hall_size_3": 1,
        "pi_hub_cycle": 32,
    }
    assert hub_hall["pi_free_size_three_remainder"]["missing_source"] == "h"

    leaf_mutual = json.loads(
        (ROOT / "results" / "three_target_leaf_mutual_trap_cap6.json").read_text()
    )
    assert run_leaf_mutual_gate(6)["status"] == "sat"
    assert audit_leaf_mutual_frozen(leaf_mutual)
    assert leaf_mutual["status"] == "sat"
    assert min(leaf_mutual["diagnostics"]["strict_wall_margins"].values()) > 0
    assert min(leaf_mutual["diagnostics"]["hub_to_leaf_safety_slacks"].values()) >= 0

    theorem = (
        ROOT
        / "results"
        / "THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md"
    ).read_text()
    assert "packet-minimum normal form" in theorem
    assert "fully captures `X_q`" in theorem
    assert "5,124 of 6,144" in theorem
    assert "component-growth lemma" in theorem
    print("three-nonsingleton flower packet-minimum tests passed")


if __name__ == "__main__":
    main()
