from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

from .audit_unique_defect_champion_cycles import (
    champion_desired_sets,
    run as audit_corpus,
)
from .audit_unique_defect_champion_escapes import run as audit_escapes
from .audit_threshold_utility_tiebreak import analyze as analyze_utility_tiebreak
from .audit_unique_defect_handoff import (
    acceptance_edges,
    candidate_slacks,
    load_record_values,
)
from .scan_charity_threshold_absorption import eligible, scan_profile, tables
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


def test_host_interference_positive_wall_is_locally_realized():
    record = json.loads(
        (RESULTS / "host_interference_positive_wall_local_counterexample.json")
        .read_text()
    )
    values = tuple(tuple(row) for row in record["values"])
    masks = tuple(record["masks"])
    floater = record["floater"]
    host = record["host"]
    bad = record["bad"]
    minimum = record["host_minimum"]
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    witness = {"host": host, "permutation": list(range(len(values)))}
    slacks = candidate_slacks(
        masks, floater, witness, totals, thresholds, row_totals
    )
    assert [agent for agent, slack in enumerate(slacks) if slack < 0] == [bad]

    augmented = masks[host] | (1 << floater)
    target = (masks[host] ^ (1 << minimum)) | (1 << floater)
    swapped = list(masks)
    swapped[host] = target
    assert augmented == record["augmented_host_mask"]
    assert target == record["reduced_target_mask"]
    assert not eligible(tuple(swapped), 1 << minimum, totals, thresholds)
    assert [
        agent
        for agent in range(len(values))
        if agent != host
        and thresholds[agent][target] > totals[agent][masks[agent]]
    ] == [bad]
    assert thresholds[host][target] > totals[host][masks[host]]
    assert record["host_floater_value"] > (
        record["host_minimum_value"] + record["host_next_minimum_value"]
    )

    selector = scan_profile(values, 1)
    assert selector["best_theta"] == record["global_theta_audit"]["best_theta"]
    assert selector["insertable_theta_maximizer_count"] == 24


def test_bad_source_champion_can_force_multi_good_bottom():
    record = json.loads(
        (RESULTS / "unique_defect_multi_bottom_local_counterexample.json")
        .read_text()
    )
    values = tuple(tuple(row) for row in record["values"])
    masks = tuple(record["masks"])
    floater = record["floater"]
    host = record["host"]
    bad = record["bad"]
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    witness = {"host": host, "permutation": list(range(len(values)))}
    slacks = candidate_slacks(
        masks, floater, witness, totals, thresholds, row_totals
    )
    assert [agent for agent, slack in enumerate(slacks) if slack < 0] == [bad]
    assert not any(
        target == bad
        for _agent, target in acceptance_edges(
            masks, floater, witness, totals, thresholds
        )
    )
    assert totals[bad][masks[host]] <= totals[bad][masks[bad]]

    desired = champion_desired_sets(
        bad, host, masks, floater, totals, thresholds
    )
    augmented = masks[host] | (1 << floater)
    discards = [augmented ^ candidate for candidate in desired]
    assert list(desired) == record["bad_champion_desired_masks"]
    assert discards == record["bad_champion_discard_masks"]
    assert min(discard.bit_count() for discard in discards) == 2

    selector = scan_profile(values, 1)
    assert selector["best_theta"] == record["global_theta_audit"]["best_theta"]
    assert selector["insertable_theta_maximizer_count"] == 24


def test_exact_lra_witness_refutes_all_host_redistribution_matchings():
    record = json.loads(
        (RESULTS / "unique_defect_host_redistribution_lra_counterexample.json")
        .read_text()
    )
    values = tuple(tuple(row) for row in record["values"])
    masks = tuple(record["masks"])
    floater = record["floater"]
    host = record["host"]
    bad = record["bad"]
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    witness = {"host": host, "permutation": list(range(len(values)))}
    slacks = candidate_slacks(
        masks, floater, witness, totals, thresholds, row_totals
    )
    assert [agent for agent, slack in enumerate(slacks) if slack < 0] == [bad]
    assert not any(
        target == bad
        for _agent, target in acceptance_edges(
            masks, floater, witness, totals, thresholds
        )
    )
    assert totals[bad][masks[host]] <= totals[bad][masks[bad]]
    desired = champion_desired_sets(
        bad, host, masks, floater, totals, thresholds
    )
    assert list(desired) == record["bad_champion_desired_masks"]
    augmented = masks[host] | (1 << floater)
    assert [augmented ^ candidate for candidate in desired] == record[
        "bad_champion_discard_masks"
    ]

    host_goods = tuple(
        good for good in range(len(values[0])) if masks[host] & (1 << good)
    )
    partitions = set()
    complete_count = 0
    for destinations in itertools.product(range(len(values)), repeat=len(host_goods)):
        redistributed = list(masks)
        redistributed[host] = 0
        for good, owner in zip(host_goods, destinations):
            redistributed[owner] |= 1 << good
        for insertion_host in range(len(values)):
            candidates = list(redistributed)
            candidates[insertion_host] |= 1 << floater
            if not all(candidates):
                continue
            partitions.add(tuple(sorted(candidates)))
            for permutation in itertools.permutations(range(len(values))):
                allocation = tuple(
                    candidates[permutation[agent]]
                    for agent in range(len(values))
                )
                complete_count += eligible(allocation, 0, totals, thresholds)
    assert len(partitions) == record["reachable_host_redistribution_partition_count"]
    assert complete_count == record["complete_efx_matching_count"] == 0


def test_exact_lra_residual_saturates_local_extremal_menu():
    record = json.loads(
        (RESULTS / "unique_defect_extremal_local_menu_lra_counterexample.json")
        .read_text()
    )
    values = tuple(tuple(row) for row in record["values"])
    masks = tuple(record["masks"])
    floater = record["floater"]
    totals, thresholds = tables(values)
    owners = range(len(values))
    bundles = tuple(
        tuple(good for good in range(len(values[0])) if mask & (1 << good))
        for mask in masks
    )

    cycle_count = 0
    eligible_pareto_count = 0
    for length in (2, 3, 4):
        for cycle in itertools.permutations(owners, length):
            if cycle[0] != min(cycle):
                continue
            for goods in itertools.product(*(bundles[owner] for owner in cycle)):
                cycle_count += 1
                weak = all(
                    values[owner][goods[index - 1]]
                    >= values[owner][goods[index]]
                    for index, owner in enumerate(cycle)
                )
                strict = any(
                    values[owner][goods[index - 1]]
                    > values[owner][goods[index]]
                    for index, owner in enumerate(cycle)
                )
                if not (weak and strict):
                    continue
                endpoint = list(masks)
                for index, owner in enumerate(cycle):
                    endpoint[owner] ^= 1 << goods[index]
                    endpoint[owner] |= 1 << goods[index - 1]
                eligible_pareto_count += eligible(
                    tuple(endpoint), 1 << floater, totals, thresholds
                )
    assert cycle_count == record["owner_pareto_exchange_candidates_saturated"]
    assert eligible_pareto_count == 0

    minimum_swap_count = 0
    eligible_improving_minimum_count = 0
    for owner, bundle in enumerate(bundles):
        for good in bundle:
            minimum_swap_count += 1
            if values[owner][good] != min(values[owner][item] for item in bundle):
                continue
            if values[owner][floater] <= values[owner][good]:
                continue
            endpoint = list(masks)
            endpoint[owner] ^= 1 << good
            endpoint[owner] |= 1 << floater
            eligible_improving_minimum_count += eligible(
                tuple(endpoint), 1 << good, totals, thresholds
            )
    assert minimum_swap_count == record["owner_minimum_charity_swaps_saturated"]
    assert eligible_improving_minimum_count == 0


def test_adverse_branch_escape_audit_reaches_three_good_component():
    audit = json.loads(
        (RESULTS / "unique_defect_adverse_branch_escape_audit.json").read_text()
    )
    assert audit["status"] == "EXACT_ESCAPES_EXTRACTED"
    assert len(audit["records"]) == 7
    residual = audit["records"][-1]
    assert residual["minimum_label_distance"] == 3
    assert residual["selected_escape"]["theta_change"] == "28099/195720"
    assert residual["selected_escape"]["utility_changes"] == [0, 2897, -1141, 0]
    assert residual["selected_escape"]["transfer_components"] == [
        {"goods": [3, 4, 5], "slots": [1, 2]}
    ]


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
