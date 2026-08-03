from collections import Counter
import hashlib
import json
from pathlib import Path

from .audit_unique_defect_champion_cycles import (
    champion_desired_sets,
    run as audit_corpus,
)
from .audit_unique_defect_champion_escapes import run as audit_escapes
from .audit_threshold_utility_tiebreak import analyze as analyze_utility_tiebreak
from .audit_unique_defect_handoff import candidate_slacks, load_record_values
from .scan_charity_threshold_absorption import scan_profile, tables
from .search_unique_defect_champion_threshold import classify
from .search_unique_defect_missing_reciprocal import classify as classify_reciprocity


RESULTS = Path("results")


def test_full_unique_defect_corpus_has_threshold_neutral_champion_cycles(tmp_path):
    output = tmp_path / "audit.json"
    result = audit_corpus(
        RESULTS / "partial_hall_threshold_plateau_completion_analysis.json",
        output,
    )
    assert result["status"] == "CORPUS_ALL_THRESHOLD_COMPATIBLE"
    assert result["counts"]["full_unique_defect_states"] == 4320
    assert (
        result["counts"]["states_with_direct_reciprocal_compatible_cycle"]
        == 4320
    )
    assert result["counts"]["states_with_zero_theta_basic_pi_cycle"] == 4320
    assert result["counts"]["bad_champion_replayed"] == 4320
    assert result["counts"].get("bad_champion_missing", 0) == 0


def test_unique_bad_agent_need_not_champion_augmented_host():
    record = json.loads(
        (RESULTS / "unique_defect_bad_champion_local_counterexample.json")
        .read_text()
    )
    values = tuple(tuple(row) for row in record["values"])
    masks = tuple(record["masks"])
    floater = record["floater"]
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    witness = {"host": record["host"], "permutation": list(range(len(values)))}
    slacks = candidate_slacks(
        masks, floater, witness, totals, thresholds, row_totals
    )
    assert [agent for agent, slack in enumerate(slacks) if slack < 0] == [
        record["bad"]
    ]
    assert not champion_desired_sets(
        record["bad"], record["host"], masks, floater, totals, thresholds
    )
    assert list(
        champion_desired_sets(
            record["host"], record["host"], masks, floater, totals, thresholds
        )
    ) == record["host_self_champion_desired_masks"]
    augmented = masks[record["host"]] | (1 << floater)
    assert thresholds[record["host"]][augmented] > totals[record["host"]][
        masks[record["host"]]
    ]
    for agent in range(len(values)):
        if agent not in (record["bad"], record["host"]):
            assert thresholds[agent][augmented] <= totals[agent][masks[agent]]

    selector = scan_profile(values, 1)
    assert selector["best_theta"] == record["global_theta_audit"]["best_theta"]
    assert not record["global_theta_audit"]["state_is_global_maximizer"]


def test_local_reciprocal_champion_cycle_can_lower_threshold():
    record = json.loads(
        (RESULTS / "unique_defect_champion_threshold_local_counterexample.json")
        .read_text()
    )
    values = tuple(tuple(row) for row in record["values"])
    result = classify(
        values,
        tuple(record["masks"]),
        record["floater"],
        Counter(),
    )
    assert result is not None
    assert result["bad"] == record["bad"]
    assert result["host"] == record["host"]
    assert {
        endpoint["theta_change"]
        for endpoint in result["reciprocal_one_charity_endpoints"]
    } == {"-31/1430"}
    assert result["owner_minimum_escapes"] == [
        {
            "outgoing_good": 0,
            "masks": [2, 36, 16, 8],
            "charity_mask": 1,
            "utility_gain": 7,
            "theta_change": "0",
        }
    ]

    selector = scan_profile(values, 1)
    assert selector["best_theta"] == "14/39"
    assert selector["insertable_theta_maximizer_count"] == 2


def test_combined_local_escape_needs_global_maximality():
    record = json.loads(
        (RESULTS / "unique_defect_champion_combined_local_counterexample.json")
        .read_text()
    )
    values = tuple(tuple(row) for row in record["values"])
    masks = tuple(record["masks"])
    result = classify(
        values,
        masks,
        record["floater"],
        Counter(),
        require_no_owner_minimum_escape=True,
    )
    assert result is not None
    assert result["owner_minimum_escapes"] == []
    assert [
        endpoint["theta_change"]
        for endpoint in result["reciprocal_one_charity_endpoints"]
    ] == ["-607/5561"]

    totals, _thresholds = tables(values)
    bad = record["bad"]
    host = record["host"]
    assert totals[host][masks[bad]] > totals[host][masks[host]]
    assert all(
        totals[agent][masks[agent]] > totals[agent][masks[bad]]
        for agent in range(len(values))
        if agent not in (bad, host)
    )
    selector = scan_profile(values, 1)
    assert selector["best_theta"] == "25/67"
    assert selector["insertable_theta_maximizer_count"] == 8


def test_full_unique_defect_does_not_force_local_reciprocity():
    record = json.loads(
        (RESULTS / "unique_defect_missing_reciprocal_local_counterexample.json")
        .read_text()
    )
    values = tuple(tuple(row) for row in record["values"])
    result = classify_reciprocity(
        values,
        tuple(record["masks"]),
        record["floater"],
        Counter(),
    )
    assert result is not None
    assert result["host"] == record["host"]
    assert result["bad"] == record["bad"]
    assert result["forced_desired_masks"] == [2]
    assert result["base_theta"] == "30/91"

    selector = scan_profile(values, 1)
    assert selector["best_theta"] == "29/84"
    assert selector["insertable_theta_maximizer_count"] == 2


def test_local_obstructions_have_connected_extremal_escapes(tmp_path):
    result = audit_escapes(
        [
            RESULTS / "unique_defect_champion_threshold_local_counterexample.json",
            RESULTS / "unique_defect_champion_combined_local_counterexample.json",
            RESULTS / "unique_defect_missing_reciprocal_local_counterexample.json",
        ],
        tmp_path / "escapes.json",
    )
    assert result["status"] == "EXACT_ESCAPES_EXTRACTED"
    assert [record["minimum_label_distance"] for record in result["records"]] == [
        1,
        2,
        2,
    ]
    assert all(
        len(record["selected_escape"]["transfer_components"]) == 1
        for record in result["records"]
    )
    assert all(
        not signature.startswith("-")
        for record in result["records"]
        for signature in record["selected_escape"]["absorption_signature"][:1]
    )


def test_threshold_utility_tiebreak_corpus_manifest_and_first_profile():
    audit = json.loads(
        (RESULTS / "threshold_utility_tiebreak_corpus_audit.json").read_text()
    )
    source = RESULTS / "partial_hall_threshold_plateau_completion_analysis.json"
    extra = RESULTS / "lexmax_partial_counterexample_4x9.json"
    assert audit["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert audit["extra_sources"] == [
        {
            "source": str(extra),
            "source_sha256": hashlib.sha256(extra.read_bytes()).hexdigest(),
        }
    ]
    assert audit["status"] == "ALL_UTILITY_TIEBREAKS_ABSORB"
    assert audit["profile_count"] == 47
    assert audit["agent_order_count"] == 1128
    assert audit["blocked_order_count"] == 0

    source_record = json.loads(source.read_text())["records"][0]
    replay = analyze_utility_tiebreak(load_record_values(source_record))
    stored = audit["records"][0]
    assert replay["theta_maximizer_count"] == stored["theta_maximizer_count"]
    assert replay["absorbing_order_count"] == 24
    assert replay["blocked_order_count"] == 0
