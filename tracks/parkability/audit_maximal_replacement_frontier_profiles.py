#!/usr/bin/env python3
"""Adversarial census for value-maximal packet replacement frontiers."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


AGENTS = ("r", "q", "c", "s")
OLD_COMPONENTS = {
    "r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "q": ("aq_tq", "ar_bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}
DEFAULT_PROFILES = (
    "three_nonsingleton_flower_full_capture_swap_gate.json",
    "three_nonsingleton_flower_full_capture_path_gate.json",
    "three_nonsingleton_flower_full_capture_packet_gate.json",
    "three_nonsingleton_flower_full_capture_arm_hub_gate.json",
    "three_nonsingleton_flower_full_capture_arm_response_gate.json",
    "fixed_replacement_lex_completion_refutation.json",
    "maximal_packet_replacement_lex_completion_refutation.json",
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atom_names(component):
    if component == "z":
        return (component,)
    return tuple(f"{component}_{index}" for index in range(2))


def old_bundles():
    return {
        agent: tuple(
            good
            for component in components
            for good in atom_names(component)
        )
        for agent, components in OLD_COMPONENTS.items()
    }


def subsets(goods, nonempty=False, proper=False):
    lower = 1 if nonempty else 0
    upper = len(goods) if proper else len(goods) + 1
    for size in range(lower, upper):
        yield from map(frozenset, itertools.combinations(goods, size))


def value(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return value(values, observer, goods) - min(
        values[observer][good] for good in goods
    )


def common_safe(values, base, goods):
    return all(
        tail(values, observer, goods) <= base[observer]
        for observer in AGENTS
    )


def minimal_desired(values, base, source, offered):
    desired = [
        group
        for group in subsets(tuple(offered), nonempty=True)
        if value(values, source, group) > base[source]
        and common_safe(values, base, group)
    ]
    return inclusion_minimal(desired)


def inclusion_minimal(groups):
    return [
        group for group in groups
        if not any(other < group for other in groups)
    ]


def alternating_outcomes(values, tr, released, delta):
    initial = inclusion_minimal([
        packet for packet in subsets(tuple(tr), nonempty=True)
        if value(values, "q", packet) > delta
    ])
    pending = [(packet, frozenset()) for packet in initial]
    seen = set()
    outcomes = {"SUCCESS": 0, "R_EXHAUSTED": 0, "Q_EXHAUSTED": 0}
    while pending:
        payment, compensation = pending.pop()
        state = (payment, compensation)
        if state in seen:
            continue
        seen.add(state)
        q_paid = value(values, "q", payment) > (
            delta + value(values, "q", compensation)
        )
        r_paid = value(values, "r", compensation) >= value(
            values, "r", payment
        )
        if q_paid and r_paid:
            outcomes["SUCCESS"] += 1
            continue
        if not r_paid:
            if value(values, "r", released) < value(values, "r", payment):
                outcomes["R_EXHAUSTED"] += 1
                continue
            additions = inclusion_minimal([
                packet for packet in subsets(
                    tuple(released - compensation), nonempty=True
                )
                if value(values, "r", compensation | packet)
                >= value(values, "r", payment)
            ])
            pending.extend((payment, compensation | packet) for packet in additions)
            continue
        assert not q_paid
        if value(values, "q", tr) <= delta + value(
            values, "q", compensation
        ):
            outcomes["Q_EXHAUSTED"] += 1
            continue
        additions = inclusion_minimal([
            packet for packet in subsets(tuple(tr - payment), nonempty=True)
            if value(values, "q", payment | packet)
            > delta + value(values, "q", compensation)
        ])
        pending.extend((payment | packet, compensation) for packet in additions)
    return {"state_count": len(seen), **outcomes}


def inspect_profile(path):
    record = json.loads(path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in record["values"].items()
    }
    old = old_bundles()
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    xq = frozenset(old["q"])
    tr = frozenset(
        good
        for good in old["r"]
        if good.startswith("ar_tr") or good.startswith("tr_rest")
    )
    eligible = [
        packet
        for packet in subsets(tuple(xq), nonempty=True, proper=True)
        if value(values, "q", packet) < values["q"]["f"]
    ]
    assert eligible
    maximum = max(value(values, "q", packet) for packet in eligible)
    frontiers = [
        packet for packet in eligible
        if value(values, "q", packet) == maximum
    ]
    response_records = []
    for packet in frontiers:
        residual = xq - packet
        slack = values["q"]["f"] - value(values, "q", packet)
        assert all(value(values, "q", {good}) >= slack for good in residual)
        offer = residual | {"f"}
        for source in ("c", "s"):
            for desired in minimal_desired(values, base, source, offer):
                if "f" not in desired or len(desired) == 1:
                    continue
                core = desired - {"f"}
                released = xq - core
                direct = value(values, "q", desired) > base["q"]
                full_return = frozenset(old[source]) | released
                return_desired = value(values, "q", full_return) > base["q"]
                delta = value(values, "q", core) - value(
                    values, "q", old[source]
                )
                compensations = 0
                for payment in subsets(tuple(tr), nonempty=True):
                    for compensation in subsets(tuple(released)):
                        if (
                            value(values, "r", compensation)
                            >= value(values, "r", payment)
                            and value(values, "q", payment)
                            > delta + value(values, "q", compensation)
                        ):
                            compensations += 1
                response_records.append({
                    "frontier": sorted(packet),
                    "source": source,
                    "desired": sorted(desired),
                    "core": sorted(core),
                    "direct_q_desire": direct,
                    "q_desires_full_return": return_desired,
                    "strict_core_capture": delta > 0 and not return_desired,
                    "compensation_count": compensations,
                    "alternating_chain_outcomes": (
                        alternating_outcomes(values, tr, released, delta)
                        if delta > 0 and not return_desired else None
                    ),
                })
    assert all(
        item["direct_q_desire"]
        or item["q_desires_full_return"]
        or item["compensation_count"] > 0
        for item in response_records
    )
    return {
        "profile": path.name,
        "profile_sha256": sha256(path),
        "eligible_packet_count": len(eligible),
        "maximum_q_value": str(maximum),
        "frontiers": [sorted(packet) for packet in frontiers],
        "frontier_tie_count": sum(
            value(values, "q", {good})
            == values["q"]["f"] - value(values, "q", packet)
            for packet in frontiers for good in xq - packet
        ),
        "response_records": response_records,
        "all_displayed_responses_return_or_compensate": True,
    }


def run(profile_paths):
    records = [inspect_profile(path) for path in profile_paths]
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "maximal-replacement-frontier-profile-census-v1",
        "status": "ALL_FROZEN_RESPONSES_RETURN_OR_COMPENSATE",
        "profiles": records,
        "totals": {
            "profile_count": len(records),
            "frontier_count": sum(len(item["frontiers"]) for item in records),
            "external_response_count": sum(
                len(item["response_records"]) for item in records
            ),
            "strict_capture_count": sum(
                response["strict_core_capture"]
                for item in records for response in item["response_records"]
            ),
            "uncompensated_strict_capture_count": sum(
                response["strict_core_capture"]
                and response["compensation_count"] == 0
                for item in records for response in item["response_records"]
            ),
            "frontier_tie_count": sum(
                item["frontier_tie_count"] for item in records
            ),
        },
        "claim_boundary": (
            "exact adversarial replay on seven frozen two-atom profiles, "
            "including their unperturbed equality boundaries; this is not a "
            "cap-free exhaustion or a proof of the selector lemma"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = [args.results_dir / name for name in DEFAULT_PROFILES]
    result = run(paths)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], **result["totals"]}, indent=2))


if __name__ == "__main__":
    main()
