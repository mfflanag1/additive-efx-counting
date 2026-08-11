#!/usr/bin/env python3
"""Regression checks for the flower dual-full-capture escape theorem."""

import json
from pathlib import Path

import z3

try:
    from .audit_flower_dual_full_escape import run as run_scalar_audit
    from .audit_flower_early_root_charity_rotation import (
        run as run_root_rotation_audit,
    )
    from .audit_flower_complement_return_augmentation import (
        run as run_complement_return_audit,
    )
    from .audit_flower_minimal_payment_residual_rotation import (
        run as run_minimal_payment_audit,
    )
    from .audit_flower_residual_wall_payment_polarity import (
        run as run_wall_payment_audit,
    )
    from .audit_flower_three_rotation_polarity import run as run_rotation_audit
    from .audit_flower_two_root_residual_split_release import (
        run as run_two_root_audit,
    )
    from .audit_alternating_payment_compensation_chain import (
        run as run_alternating_chain_audit,
    )
    from .audit_charity_rooted_transfer_tree_release import (
        run as run_transfer_tree_audit,
    )
    from .audit_lex_rooted_owner_charity_donation import run as run_donation_audit
    from .audit_maximal_replacement_frontier_exchange import (
        run as run_maximal_frontier_audit,
    )
    from .audit_maximal_replacement_frontier_profiles import (
        DEFAULT_PROFILES as MAXIMAL_FRONTIER_PROFILES,
        run as run_maximal_frontier_census,
    )
    from .audit_minimal_flower_flexible_gate import run as run_core_audit
    from .audit_owner_rooted_hub_split_release import run as run_owner_hub_audit
    from .audit_packet_replacement_charity_absorption import (
        run as run_charity_absorption_audit,
    )
    from .audit_packet_replacement_aggregate_root_flip_polarity import (
        run as run_aggregate_root_flip_audit,
    )
    from .audit_packet_replacement_complement_return import (
        run as run_replacement_return_audit,
    )
    from .audit_q_exhaustion_root_switch import run as run_q_root_switch_audit
    from .audit_released_owner_compensation_chain import (
        run as run_released_owner_chain_audit,
    )
    from .audit_open_leaf_source_rotation import run as run_open_leaf_audit
    from .audit_outside_source_sink_augmentation import (
        run as run_sink_augmentation_audit,
    )
    from .audit_hardened_q_wall_sink_augmentation_pi import (
        run as run_hardened_sink_pi_audit,
    )
    from .audit_residual_flower_packet_countermodel import (
        run as run_packet_countermodel_audit,
    )
    from .audit_residual_flower_packet_core import run as run_packet_core_audit
    from .analyze_residual_top_champion_sources import run as run_source_census
    from .analyze_residual_flower_two_root_partitions import (
        run as run_two_root_partition_census,
    )
    from .run_minimal_flower_global_lex_cegar import build_master, rival_blocker
except ImportError:
    from audit_flower_dual_full_escape import run as run_scalar_audit
    from audit_flower_early_root_charity_rotation import (
        run as run_root_rotation_audit,
    )
    from audit_flower_complement_return_augmentation import (
        run as run_complement_return_audit,
    )
    from audit_flower_minimal_payment_residual_rotation import (
        run as run_minimal_payment_audit,
    )
    from audit_flower_residual_wall_payment_polarity import (
        run as run_wall_payment_audit,
    )
    from audit_flower_three_rotation_polarity import run as run_rotation_audit
    from audit_flower_two_root_residual_split_release import (
        run as run_two_root_audit,
    )
    from audit_alternating_payment_compensation_chain import (
        run as run_alternating_chain_audit,
    )
    from audit_charity_rooted_transfer_tree_release import (
        run as run_transfer_tree_audit,
    )
    from audit_lex_rooted_owner_charity_donation import run as run_donation_audit
    from audit_maximal_replacement_frontier_exchange import (
        run as run_maximal_frontier_audit,
    )
    from audit_maximal_replacement_frontier_profiles import (
        DEFAULT_PROFILES as MAXIMAL_FRONTIER_PROFILES,
        run as run_maximal_frontier_census,
    )
    from audit_minimal_flower_flexible_gate import run as run_core_audit
    from audit_owner_rooted_hub_split_release import run as run_owner_hub_audit
    from audit_packet_replacement_charity_absorption import (
        run as run_charity_absorption_audit,
    )
    from audit_packet_replacement_aggregate_root_flip_polarity import (
        run as run_aggregate_root_flip_audit,
    )
    from audit_packet_replacement_complement_return import (
        run as run_replacement_return_audit,
    )
    from audit_q_exhaustion_root_switch import run as run_q_root_switch_audit
    from audit_released_owner_compensation_chain import (
        run as run_released_owner_chain_audit,
    )
    from audit_open_leaf_source_rotation import run as run_open_leaf_audit
    from audit_outside_source_sink_augmentation import (
        run as run_sink_augmentation_audit,
    )
    from audit_hardened_q_wall_sink_augmentation_pi import (
        run as run_hardened_sink_pi_audit,
    )
    from audit_residual_flower_packet_countermodel import (
        run as run_packet_countermodel_audit,
    )
    from audit_residual_flower_packet_core import run as run_packet_core_audit
    from analyze_residual_top_champion_sources import run as run_source_census
    from analyze_residual_flower_two_root_partitions import (
        run as run_two_root_partition_census,
    )
    from run_minimal_flower_global_lex_cegar import build_master, rival_blocker


ROOT = Path(__file__).resolve().parents[2]


def main():
    scalar_path = ROOT / "results" / "flower_dual_full_capture_escape_audit.json"
    scalar = json.loads(scalar_path.read_text())
    scalar_replay = run_scalar_audit()
    assert scalar_replay["status"] == scalar["status"]
    assert scalar_replay["records"] == scalar["records"]
    assert scalar["status"] == "ALL_FORCED"
    assert {record["status"] for record in scalar["records"]} == {"unsat"}

    rotation_path = ROOT / "results" / "flower_three_rotation_polarity_audit.json"
    rotation = json.loads(rotation_path.read_text())
    rotation_replay = run_rotation_audit()
    assert rotation_replay["status"] == rotation["status"] == "ALL_FORCED"
    assert rotation_replay["records"] == rotation["records"]

    root_rotation_path = (
        ROOT / "results" / "flower_early_root_charity_rotation_audit.json"
    )
    root_rotation = json.loads(root_rotation_path.read_text())
    root_rotation_replay = run_root_rotation_audit()
    assert root_rotation_replay["status"] == root_rotation["status"] == "FORCED"
    assert root_rotation_replay["record"] == root_rotation["record"]

    donation_path = (
        ROOT
        / "results"
        / "lex_rooted_owner_charity_donation_obstruction_audit.json"
    )
    donation = json.loads(donation_path.read_text())
    donation_replay = run_donation_audit()
    assert donation_replay["status"] == donation["status"] == "ALL_FORCED"
    assert donation_replay["records"] == donation["records"]

    minimal_payment_path = (
        ROOT / "results" / "flower_minimal_payment_residual_rotation_audit.json"
    )
    minimal_payment = json.loads(minimal_payment_path.read_text())
    minimal_payment_replay = run_minimal_payment_audit()
    assert minimal_payment_replay["status"] == minimal_payment["status"] == "FORCED"
    assert minimal_payment_replay["record"] == minimal_payment["record"]

    wall_payment_path = (
        ROOT / "results" / "flower_residual_wall_payment_polarity_audit.json"
    )
    wall_payment = json.loads(wall_payment_path.read_text())
    wall_payment_replay = run_wall_payment_audit()
    assert wall_payment_replay["status"] == wall_payment["status"] == "FORCED"
    assert wall_payment_replay["record"] == wall_payment["record"]

    two_root_path = (
        ROOT / "results" / "flower_two_root_residual_split_release_audit.json"
    )
    two_root = json.loads(two_root_path.read_text())
    two_root_replay = run_two_root_audit()
    assert two_root_replay == two_root
    assert two_root["status"] == "ALL_RELEASE_COMPATIBLE"
    assert [
        record["response_permutations_checked"] for record in two_root["records"]
    ] == [2, 6, 24]

    packet_countermodel_path = (
        ROOT / "results" / "residual_flower_packet_countermodel.json"
    )
    partition_census_path = (
        ROOT / "results" / "residual_flower_two_root_partition_census.json"
    )
    partition_census = json.loads(partition_census_path.read_text())
    partition_census_replay = run_two_root_partition_census(
        packet_countermodel_path
    )
    assert partition_census_replay == partition_census
    assert partition_census["status"] == "RESPONSE_CLOSURE_FOUND"
    assert partition_census["counts"] == {
        "EFX": 0,
        "HALL_DEFICIENT": 13,
        "INTERNAL_SDR": 3,
    }

    packet_core_path = (
        ROOT / "results" / "residual_flower_packet_candidate_audit.json"
    )
    packet_core = json.loads(packet_core_path.read_text())
    packet_core_replay = run_packet_core_audit()
    assert (
        packet_core_replay["status"]
        == packet_core["status"]
        == "PACKET_LIFT_REFUTED"
    )
    assert packet_core_replay["atomic_candidate_core_status"] == "unsat"
    assert packet_core_replay["candidate_core_status"] == "sat"

    packet_countermodel_audit_path = (
        ROOT / "results" / "residual_flower_packet_countermodel_audit.json"
    )
    packet_countermodel_audit = json.loads(packet_countermodel_audit_path.read_text())
    packet_countermodel_replay = run_packet_countermodel_audit(packet_countermodel_path)
    for key in (
        "status",
        "candidate_count",
        "all_candidates_blocked",
        "subset_sum_injective",
        "displayed_escape_efx_and_lex_better",
        "minimum_moved_goods",
        "one_move_allocations_excluded",
    ):
        assert packet_countermodel_replay[key] == packet_countermodel_audit[key]

    gate_path = ROOT / "results" / "minimal_flower_flexible_completion_gate.json"
    core_path = ROOT / "results" / "minimal_flower_flexible_completion_audit.json"
    core = json.loads(core_path.read_text())
    core_replay = run_core_audit(gate_path)
    for key in (
        "status",
        "full_replay_status",
        "without_nondegeneracy_status",
        "recorded_rival_count",
        "core_rival_count",
        "core",
        "deletion_check_statuses",
    ):
        assert core_replay[key] == core[key]
    assert core["status"] == "DELETION_MINIMAL_UNSAT_CORE"
    assert core["without_nondegeneracy_status"] == "unsat"
    assert {entry["topology"] for entry in core["core"]} == {
        "_->q:f;q->_:bq",
        "_->r:f;q->r:tq;r->_:br;r->q:tr",
    }

    _, value, base = build_master()
    q_fixed = {
        "r": ("tr", "f"),
        "q": ("tq", "bq"),
        "c": ("tc", "bc"),
        "s": ("z",),
        "_": ("br",),
    }
    assert z3.is_true(z3.simplify(rival_blocker(value, base, q_fixed, "flexible")))

    theorem = (
        ROOT / "results" / "FLOWER_DUAL_FULL_CAPTURE_ESCAPE_LEMMA_20260810.md"
    ).read_text()
    assert "arbitrary-packet" in theorem
    assert "residual top packet `J`" in theorem
    assert "does **not** force" in theorem
    rotation_theorem = (
        ROOT / "results" / "FLOWER_THREE_ROTATION_POLARITY_LEMMA_20260810.md"
    ).read_text()
    assert "independent of the numbers of goods" in rotation_theorem
    assert "opposite ranking" in rotation_theorem
    root_rotation_theorem = (
        ROOT / "results" / "FLOWER_EARLY_ROOT_CHARITY_ROTATION_LEMMA_20260810.md"
    ).read_text()
    assert (
        "strictly rank the two bottom packets in opposite orders"
        in root_rotation_theorem
    )
    donation_theorem = (
        ROOT / "results" / "LEX_ROOTED_OWNER_CHARITY_DONATION_OBSTRUCTION_LEMMA_20260810.md"
    ).read_text()
    assert "later donor to lose" in donation_theorem
    minimal_payment_theorem = (
        ROOT
        / "results"
        / "FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810.md"
    ).read_text()
    assert "exactly one of the following occurs" in minimal_payment_theorem
    two_root_theorem = (
        ROOT
        / "results"
        / "FLOWER_TWO_ROOT_RESIDUAL_SPLIT_RESPONSE_HALL_LEMMA_20260810.md"
    ).read_text()
    assert "Every incoming set is supplied" in two_root_theorem
    wall_payment_theorem = (
        ROOT
        / "results"
        / "FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810.md"
    ).read_text()
    assert "root wall can be repaired" in wall_payment_theorem
    return_augmentation_theorem = (
        ROOT
        / "results"
        / "FLOWER_EXTERNAL_RETURN_AUGMENTATION_LEMMA_20260810.md"
    ).read_text()
    assert "independent of `|R|`" in return_augmentation_theorem
    assert "There is no fifth owner" in return_augmentation_theorem
    assert "does not yet close `GG`" in return_augmentation_theorem
    complement_return_path = (
        ROOT / "results" / "flower_complement_return_augmentation_audit.json"
    )
    complement_return = json.loads(complement_return_path.read_text())
    complement_return_replay = run_complement_return_audit()
    assert complement_return_replay["status"] == "ALL_FORCED"
    assert complement_return_replay["support_records"] == complement_return["support_records"]
    assert complement_return_replay["scalar_records"] == complement_return["scalar_records"]
    complement_return_theorem = (
        ROOT
        / "results"
        / "FLOWER_COMPLEMENT_RETURN_AUGMENTATION_LEMMA_20260810.md"
    ).read_text()
    assert "whole unused complement" in complement_return_theorem
    assert "strict capture system" in complement_return_theorem
    assert "does not yet eliminate" in complement_return_theorem
    charity_absorption_path = (
        ROOT / "results" / "packet_replacement_charity_absorption_audit.json"
    )
    charity_absorption = json.loads(charity_absorption_path.read_text())
    charity_absorption_replay = run_charity_absorption_audit()
    assert charity_absorption_replay["status"] == "ALL_FORCED"
    assert (
        charity_absorption_replay["support_record"]
        == charity_absorption["support_record"]
    )
    assert (
        charity_absorption_replay["scalar_records"]
        == charity_absorption["scalar_records"]
    )
    charity_absorption_theorem = (
        ROOT
        / "results"
        / "PACKET_REPLACEMENT_CHARITY_ABSORPTION_LEMMA_20260810.md"
    ).read_text()
    assert "isolated charity wall cannot survive" in charity_absorption_theorem
    assert "missing source is `q`" in charity_absorption_theorem
    assert "does not eliminate that Hall defect" in charity_absorption_theorem
    replacement_return_path = (
        ROOT / "results" / "packet_replacement_complement_return_audit.json"
    )
    replacement_return = json.loads(replacement_return_path.read_text())
    replacement_return_replay = run_replacement_return_audit()
    assert replacement_return_replay["status"] == "ALL_FORCED"
    assert (
        replacement_return_replay["support_record"]
        == replacement_return["support_record"]
    )
    assert (
        replacement_return_replay["root_flip_support_record"]
        == replacement_return["root_flip_support_record"]
    )
    assert (
        replacement_return_replay["scalar_records"]
        == replacement_return["scalar_records"]
    )
    replacement_return_theorem = (
        ROOT
        / "results"
        / "PACKET_REPLACEMENT_COMPLEMENT_RETURN_LEMMA_20260810.md"
    ).read_text()
    assert "Every such external response has the form" in replacement_return_theorem
    assert "strict interval" in replacement_return_theorem
    assert "two-row compensation system (13)" in replacement_return_theorem
    aggregate_root_path = (
        ROOT
        / "results"
        / "packet_replacement_aggregate_root_flip_polarity_audit.json"
    )
    aggregate_root = json.loads(aggregate_root_path.read_text())
    aggregate_root_replay = run_aggregate_root_flip_audit()
    assert aggregate_root_replay["status"] == "ALL_FORCED"
    assert aggregate_root_replay["scalar_records"] == aggregate_root["scalar_records"]
    aggregate_root_theorem = (
        ROOT
        / "results"
        / "PACKET_REPLACEMENT_AGGREGATE_ROOT_FLIP_POLARITY_LEMMA_20260810.md"
    ).read_text()
    assert "strict three-level order" in aggregate_root_theorem
    assert "named `R-wall` or `Q-wall`" in aggregate_root_theorem
    alternating_chain_path = (
        ROOT / "results" / "alternating_payment_compensation_chain_audit.json"
    )
    alternating_chain = json.loads(alternating_chain_path.read_text())
    alternating_chain_replay = run_alternating_chain_audit()
    assert alternating_chain_replay["status"] == "ALL_FORCED"
    assert (
        alternating_chain_replay["scalar_records"]
        == alternating_chain["scalar_records"]
    )
    alternating_chain_theorem = (
        ROOT
        / "results"
        / "ALTERNATING_PAYMENT_COMPENSATION_CHAIN_LEMMA_20260810.md"
    ).read_text()
    assert "finite repair tree" in alternating_chain_theorem
    assert "never ends in an unnamed two-row failure" in alternating_chain_theorem
    transfer_tree_path = (
        ROOT / "results" / "charity_rooted_transfer_tree_release_audit.json"
    )
    transfer_tree = json.loads(transfer_tree_path.read_text())
    assert run_transfer_tree_audit() == transfer_tree
    assert transfer_tree["total_tree_permutation_pairs"] == 405
    assert [
        record["rooted_tree_count"] for record in transfer_tree["records"]
    ] == [1, 1, 3, 16]
    transfer_tree_theorem = (
        ROOT
        / "results"
        / "CHARITY_ROOTED_TRANSFER_TREE_RESPONSE_HALL_LEMMA_20260810.md"
    ).read_text()
    assert "Stars, paths, and a hub followed by a donating leaf" in transfer_tree_theorem
    assert "exactly three outcomes" in transfer_tree_theorem
    q_root_switch_path = (
        ROOT / "results" / "q_exhaustion_root_switch_audit.json"
    )
    q_root_switch = json.loads(q_root_switch_path.read_text())
    q_root_switch_replay = run_q_root_switch_audit()
    assert q_root_switch_replay["status"] == "ALL_FORCED"
    assert q_root_switch_replay["scalar_records"] == q_root_switch["scalar_records"]
    assert q_root_switch_replay["support_record"] == q_root_switch["support_record"]
    q_root_switch_theorem = (
        ROOT / "results" / "Q_EXHAUSTION_ROOT_SWITCH_LEMMA_20260810.md"
    ).read_text()
    assert "stronger margin" in q_root_switch_theorem
    assert "one-edge charity-rooted transfer tree" in q_root_switch_theorem
    released_owner_path = (
        ROOT / "results" / "released_owner_compensation_chain_audit.json"
    )
    released_owner = json.loads(released_owner_path.read_text())
    released_owner_replay = run_released_owner_chain_audit()
    assert released_owner_replay["status"] == "ALL_FORCED"
    assert released_owner_replay["scalar_records"] == released_owner["scalar_records"]
    assert released_owner_replay["support_record"] == released_owner["support_record"]
    released_owner_theorem = (
        ROOT / "results" / "RELEASED_OWNER_COMPENSATION_CHAIN_LEMMA_20260810.md"
    ).read_text()
    assert "full released-reservoir" in released_owner_theorem
    assert "introduces no new Q-terminal case" in released_owner_theorem
    open_leaf_path = ROOT / "results" / "open_leaf_source_rotation_audit.json"
    open_leaf = json.loads(open_leaf_path.read_text())
    open_leaf_replay = run_open_leaf_audit()
    assert open_leaf_replay["status"] == "ALL_FORCED"
    assert open_leaf_replay["scalar_records"] == open_leaf["scalar_records"]
    assert open_leaf_replay["support_record"] == open_leaf["support_record"]
    open_leaf_theorem = (
        ROOT / "results" / "OPEN_LEAF_SOURCE_ROTATION_LEMMA_20260810.md"
    ).read_text()
    assert "strictly larger owner set" in open_leaf_theorem
    assert "cannot remain an unnamed dependency" in open_leaf_theorem
    sink_augmentation_path = (
        ROOT / "results" / "outside_source_sink_augmentation_audit.json"
    )
    sink_augmentation = json.loads(sink_augmentation_path.read_text())
    sink_augmentation_replay = run_sink_augmentation_audit()
    assert sink_augmentation_replay["status"] == "ALL_FORCED"
    assert (
        sink_augmentation_replay["scalar_records"]
        == sink_augmentation["scalar_records"]
    )
    assert (
        sink_augmentation_replay["support_record"]
        == sink_augmentation["support_record"]
    )
    sink_augmentation_theorem = (
        ROOT / "results" / "OUTSIDE_SOURCE_SINK_AUGMENTATION_LEMMA_20260810.md"
    ).read_text()
    assert "represented owner set strictly grows" in sink_augmentation_theorem
    assert "cannot run indefinitely" in sink_augmentation_theorem
    hardened_sink_path = (
        ROOT / "results" / "hardened_q_wall_sink_augmentation_pi_audit.json"
    )
    hardened_sink = json.loads(hardened_sink_path.read_text())
    hardened_sink_replay = run_hardened_sink_pi_audit(
        ROOT / "results" / "flexible_lex_basic_pi_free_hardened_countermodel.json"
    )
    assert hardened_sink_replay == hardened_sink
    assert hardened_sink["status"] == "PI_RESPONSE_MATCHING"
    assert hardened_sink["internal_matching"] == {
        "q": "s",
        "c": "c",
        "r": "r",
        "s": "q",
    }
    assert hardened_sink["incoming_disjoint"]
    assert hardened_sink["all_incoming_supplied"]
    maximal_frontier_path = (
        ROOT / "results" / "maximal_replacement_frontier_exchange_audit.json"
    )
    maximal_frontier = json.loads(maximal_frontier_path.read_text())
    maximal_frontier_replay = run_maximal_frontier_audit()
    assert maximal_frontier_replay["status"] == "ALL_FORCED"
    assert (
        maximal_frontier_replay["scalar_records"]
        == maximal_frontier["scalar_records"]
    )
    maximal_frontier_theorem = (
        ROOT
        / "results"
        / "MAXIMAL_REPLACEMENT_FRONTIER_EXCHANGE_LEMMA_20260810.md"
    ).read_text()
    assert "forbidden band `(0,sigma]`" in maximal_frontier_theorem
    assert "genuinely two-row indivisible exchange" in maximal_frontier_theorem
    frontier_census_path = (
        ROOT / "results" / "maximal_replacement_frontier_profile_census.json"
    )
    frontier_census = json.loads(frontier_census_path.read_text())
    frontier_profiles = [
        ROOT / "results" / name for name in MAXIMAL_FRONTIER_PROFILES
    ]
    assert run_maximal_frontier_census(frontier_profiles) == frontier_census
    assert frontier_census["totals"] == {
        "external_response_count": 4,
        "frontier_count": 7,
        "frontier_tie_count": 1,
        "profile_count": 7,
        "strict_capture_count": 1,
        "uncompensated_strict_capture_count": 0,
    }
    strict_frontier_responses = [
        response
        for profile in frontier_census["profiles"]
        for response in profile["response_records"]
        if response["strict_core_capture"]
    ]
    assert [
        response["alternating_chain_outcomes"]
        for response in strict_frontier_responses
    ] == [{
        "Q_EXHAUSTED": 1,
        "R_EXHAUSTED": 0,
        "SUCCESS": 1,
        "state_count": 3,
    }]
    assert [
        response["released_owner_chain_outcomes"]
        for response in strict_frontier_responses
    ] == [{
        "Q_EXHAUSTED": 5,
        "R_EXHAUSTED": 0,
        "SUCCESS": 2,
        "state_count": 16,
    }]

    source_path = ROOT / "results" / "residual_top_champion_source_census.json"
    source_census = json.loads(source_path.read_text())
    assert run_source_census(ROOT) == source_census
    assert len(source_census["records"]) == 7
    assert not any(
        record["survives_live_rotation_gate"]
        for record in source_census["records"]
    )

    owner_hub_path = ROOT / "results" / "owner_rooted_hub_split_release_audit.json"
    owner_hub = json.loads(owner_hub_path.read_text())
    assert run_owner_hub_audit() == owner_hub
    assert owner_hub["status"] == "ALL_RELEASE_COMPATIBLE"
    assert [record["response_permutations_checked"] for record in owner_hub["records"]] == [6, 24]
    print("flower dual-full-capture theorem tests passed")


if __name__ == "__main__":
    main()
