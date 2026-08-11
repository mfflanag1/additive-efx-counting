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
    from .audit_lex_rooted_owner_charity_donation import run as run_donation_audit
    from .audit_minimal_flower_flexible_gate import run as run_core_audit
    from .audit_owner_rooted_hub_split_release import run as run_owner_hub_audit
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
    from audit_lex_rooted_owner_charity_donation import run as run_donation_audit
    from audit_minimal_flower_flexible_gate import run as run_core_audit
    from audit_owner_rooted_hub_split_release import run as run_owner_hub_audit
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
