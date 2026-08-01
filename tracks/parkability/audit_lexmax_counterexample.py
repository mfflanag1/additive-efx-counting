#!/usr/bin/env python3
"""Replay the positive generic 4x9 counterexample to lex-max completion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from . import core
    from .anneal_lexmax_partial import exact_lexmax_audit
    from .fast_count import FastParkability
except ImportError:
    import core
    from anneal_lexmax_partial import exact_lexmax_audit
    from fast_count import FastParkability


def subset_sums(row: tuple[int, ...]) -> tuple[int, ...]:
    sums = [0]
    for value in row:
        sums += [total + value for total in sums]
    return tuple(sums)


def run(path: Path) -> dict:
    record = json.loads(path.read_text())
    if (
        record.get("schema") != "lexmax-partial-counterexample-v1"
        or record.get("status") != "COUNTEREXAMPLE_TO_LEXMAX_COMPLETION_LEMMA"
    ):
        raise ValueError("unexpected counterexample schema or status")

    n = record["n"]
    m = record["m"]
    original = core.validate_values(
        record["source"]["original_values"],
        expected_n=n,
        expected_m=m,
        lower=0,
    )
    lift = record["positive_nondegenerate_lift"]
    values = core.validate_values(
        lift["values"],
        expected_n=n,
        expected_m=m,
        lower=1,
    )
    scale = lift["scale"]
    perturbations = tuple(lift["perturbations"])
    expected_values = tuple(
        tuple(
            scale * original[agent][good] + perturbations[good]
            for good in range(m)
        )
        for agent in range(n)
    )
    if values != expected_values:
        raise AssertionError("positive lift does not match its stated formula")

    subset_nondegenerate = all(
        len(set(subset_sums(row))) == 1 << m
        for row in values
    )
    if not subset_nondegenerate:
        raise AssertionError("a lifted row has equal-valued distinct bundles")

    candidate = record["candidate"]
    floater = candidate["floater"]
    base_owner = tuple(candidate["base_owner"])
    classification = core.classify_base(values, floater, base_owner)
    nonenvy_slacks = [
        classification["own_values"][agent] - values[agent][floater]
        for agent in range(n)
    ]
    expected_candidate = {
        "bundles": candidate["bundles"],
        "utilities": candidate["utilities"],
        "nonenvy_floater_slacks": candidate["nonenvy_floater_slacks"],
        "base_min_efx_slack": candidate["base_min_efx_slack"],
        "host_min_insertion_slacks": candidate["host_min_insertion_slacks"],
    }
    observed_candidate = {
        "bundles": classification["bundles"],
        "utilities": classification["own_values"],
        "nonenvy_floater_slacks": nonenvy_slacks,
        "base_min_efx_slack": classification["base_min_efx_slack"],
        "host_min_insertion_slacks": classification["host_min_slack"],
    }
    if observed_candidate != expected_candidate:
        raise AssertionError("candidate classification changed")

    order = tuple(record["agent_order"])
    partial = exact_lexmax_audit(values, order)
    observed_partial = {
        key: partial[key]
        for key in (
            "eligible_base_count",
            "lexmax_key",
            "lexmax_base_count",
            "lexmax_insertable_count",
        )
    }
    if observed_partial != record["exact_partial_audit"]:
        raise AssertionError("partial-allocation replay changed")
    if (
        partial["lexmax_bases"][0]["floater"] != floater
        or tuple(partial["lexmax_bases"][0]["base_owner"]) != base_owner
    ):
        raise AssertionError("the stated candidate is not the unique lex maximum")

    complete_assignments = list(core.iter_efx0_assignments(values))
    agent_zero_utilities = [
        sum(
            values[0][good]
            for good, owner in enumerate(assignment)
            if owner == 0
        )
        for assignment in complete_assignments
    ]
    observed_complete = {
        "complete_efx_count": len(complete_assignments),
        "max_agent_0_utility": max(agent_zero_utilities),
        "candidate_agent_0_utility": classification["own_values"][0],
    }
    if observed_complete != record["exact_complete_audit"]:
        raise AssertionError("complete-allocation replay changed")
    if observed_complete["max_agent_0_utility"] >= partial["lexmax_key"][0]:
        raise AssertionError("a complete EFX allocation is lexicographically nonlower")

    all_orders = FastParkability(n, m).lexmax_all_agent_orders_landscape(values)
    blocked_orders = [
        record["agent_order"]
        for record in all_orders["order_records"]
        if record["lexmax_insertable_count"] == 0
    ]
    observed_all_orders = {
        "agent_order_count": all_orders["agent_order_count"],
        "insertable_agent_order_count": all_orders[
            "insertable_agent_order_count"
        ],
        "blocked_agent_order_count": all_orders["blocked_agent_order_count"],
        "blocked_orders_are_exactly_those_starting_with_agent": (
            0
            if blocked_orders
            and all(order[0] == 0 for order in blocked_orders)
            and len(blocked_orders) == 6
            else None
        ),
    }
    if observed_all_orders != record["all_agent_orders_audit"]:
        raise AssertionError("all-agent-order replay changed")

    return {
        "status": "PASS",
        "path": str(path.resolve()),
        "strictly_positive": True,
        "subset_nondegenerate": subset_nondegenerate,
        "candidate": observed_candidate,
        "partial": observed_partial,
        "complete": observed_complete,
        "all_agent_orders": observed_all_orders,
        "claim_scope": (
            "counterexample to lex-max direct completion only; "
            "complete additive EFX remains open"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "record",
        nargs="?",
        type=Path,
        default=Path("results/lexmax_partial_counterexample_4x9.json"),
    )
    args = parser.parse_args()
    print(json.dumps(run(args.record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
