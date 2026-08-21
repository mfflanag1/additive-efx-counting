import hashlib
import json
from fractions import Fraction

from .fixed_u_dynamic_anchor import anchor_scenarios, role_slack


def load(path):
    with open(path) as handle:
        return json.load(handle)


def rows(raw, key):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[key].items()
    }


def test_exact_anchor_normal_form_reduces_all_cardinalities_to_k2_and_k3():
    raw = load("results/fixed_u_wild_forced_terminal_profile_20260820.json")
    totals = rows(raw, "profile_totals")
    minima = rows(raw, "profile_minima")
    assert role_slack(totals, minima, "a1") == 7
    anchor = anchor_scenarios(totals, minima, "a1", "q", "q")
    assert {label for label, _, _ in anchor} == {"k2", "k3plus"}
    nonanchor = anchor_scenarios(totals, minima, "a1", "q", "d")
    assert {label for label, _, _ in nonanchor} == {"k2", "k3plus"}
    assert {x for _, x, _ in nonanchor} == {
        minima["d"]["a1"],
        totals["d"]["a1"] - minima["d"]["a1"],
        totals["d"]["a1"] - 2 * minima["d"]["a1"],
    }


def test_retained_profile_calibration_recovers_all_205_profiles():
    raw = load("results/fixed_u_dynamic_anchor_profile_calibration_20260821.json")
    assert raw["status"] == "ALL_RETAINED_PROFILES_CLOSED"
    assert raw["retained_profile_count"] == raw["processed_profile_count"] == 205
    assert raw["closure_counts"] == {"whole": 200, "anchor": 5}
    assert raw["terminal_status"] == "anchor"
    assert set(raw["required_terminal_calibrations"]) == {
        "A_q_min_a1", "B_r_min_k"
    }


def test_dynamic_anchor_obstruction_is_independently_audited():
    decision = load("results/fixed_u_dynamic_anchor_cegar_20260821.json")
    assert decision["status"] == "SAT_DYNAMIC_ANCHOR_OBSTRUCTION"
    assert decision["oracle_status"] == "unsat"
    assert decision["fresh_candidate_count"] == len(decision["rounds"]) == 7
    audit = load("results/fixed_u_dynamic_anchor_obstruction_independent_audit_20260821.json")
    assert audit["status"] == "AUDIT_PASS_DYNAMIC_ANCHOR_REFUTED_EFX_NOT_REFUTED"
    assert audit["master_replay_status"] == "sat"
    assert audit["independent_whole_role_status"] == "unsat"
    assert audit["independent_anchor_lane_count"] == 40
    assert audit["canonical_physical_repair"]["split_roles"] == ["a1"]


def test_obstruction_has_exact_64_pattern_tame_repair():
    raw = load("results/fixed_u_dynamic_anchor_obstruction_tame_menu_20260821.json")
    assert raw["status"] == "VERIFIED_REALIZATION_FREE_TAME_MENU"
    assert raw["certificate"]["split_roles"] == ["a1", "h"]
    assert raw["certificate"]["pattern_count"] == 64
    assert len(raw["certificate"]["allocations"]) == 64


def test_tame_or_anchor_correction_has_exact_second_obstruction():
    raw = load("results/fixed_u_tame_or_anchor_cegar_20260821.json")
    assert raw["status"] == "SAT_TAME_MENU_OR_DYNAMIC_ANCHOR_OBSTRUCTION"
    assert raw["menu_status"] == "wide_family_failed"
    assert raw["anchor_status"] == "unsat"
    assert raw["fresh_cut_count"] == len(raw["rounds"]) == 81
    physical = load(
        "results/fixed_u_tame_or_anchor_obstruction_canonical_physical_decision_20260821.json"
    )
    assert physical["status"] == "SAT_COMPLETE_EFX_SPLIT_REPAIR"
    assert physical["attempts"][:2] == [
        {"split_cap": 0, "status": "unsat"},
        {"split_cap": 1, "status": "sat"},
    ]
    assert physical["terminal"]["split_roles"] == ["gq"]
    mixed = load("results/fixed_u_tame_or_anchor_obstruction_mixed_menu_20260821.json")
    assert mixed["status"] == "SAT_ONE_TAME_PLUS_ONE_ANCHOR_MENU_OBSTRUCTION"
    assert mixed["terminal"]["status"] == "UNSAT"
    assert mixed["terminal"]["pattern"] == "gq:0001"


def test_dynamic_cut_ledgers_are_contiguous_and_hash_valid():
    for path, count in (
        ("results/fixed_u_dynamic_anchor_cuts_20260821.jsonl", 7),
        ("results/fixed_u_tame_or_anchor_cuts_20260821.jsonl", 81),
    ):
        records = [json.loads(line) for line in open(path) if line.strip()]
        assert len(records) == count
        assert [record["iteration"] for record in records] == list(range(count))
        for record in records:
            digest = record.pop("payload_sha256")
            encoded = json.dumps(record, sort_keys=True, separators=(",", ":"))
            assert hashlib.sha256(encoded.encode()).hexdigest() == digest
