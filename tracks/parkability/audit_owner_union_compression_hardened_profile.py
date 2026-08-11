#!/usr/bin/env python3
"""Solver-independent audit of the hardened owner-union compression escape."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        tail,
        validate_flower_master,
        value,
    )
    from .harden_flexible_lex_basic_pi_free_countermodel import basic_pi_free
    from .harden_flexible_lex_radius3_countermodel import live_polarity
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        tail,
        validate_flower_master,
        value,
    )
    from harden_flexible_lex_basic_pi_free_countermodel import basic_pi_free
    from harden_flexible_lex_radius3_countermodel import live_polarity


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def common_safe(values, base_value, goods):
    return all(
        tail(values, observer, goods) <= base_value[observer]
        for observer in AGENTS
    )


def desired_subsets(values, base_value, source, offered):
    desired = []
    for size in range(1, len(offered) + 1):
        for subset in itertools.combinations(offered, size):
            if (
                value(values, source, subset) > base_value[source]
                and common_safe(values, base_value, subset)
            ):
                desired.append(frozenset(subset))
    return [
        subset for subset in desired
        if not any(other < subset for other in desired)
    ]


def is_efx(values, allocation):
    return all(
        value(values, observer, allocation[observer])
        >= tail(values, observer, allocation[target])
        for observer in AGENTS
        for target in AGENTS
    ) and all(
        value(values, observer, allocation[observer])
        >= value(values, observer, allocation["_"])
        for observer in AGENTS
    )


def subset_sum_injective(row):
    denominator = math.lcm(*(amount.denominator for amount in row.values()))
    integers = [int(amount * denominator) for amount in row.values()]
    sums = {0}
    for amount in integers:
        shifted = {current + amount for current in sums}
        if sums & shifted:
            return False
        sums |= shifted
    return True


def run(source_path):
    payload = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in payload["values"].items()
    }
    old = validate_flower_master(values)
    base_value = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    assert all(amount > 0 for row in values.values() for amount in row.values())
    assert all(subset_sum_injective(values[agent]) for agent in AGENTS)
    assert live_polarity(values)
    assert basic_pi_free(values, old)

    original = {
        owner: tuple(goods) for owner, goods in payload["original_allocation"].items()
    }
    escape = {
        owner: tuple(goods) for owner, goods in payload["escape_allocation"].items()
    }
    all_goods = set().union(*(set(goods) for goods in old.values()), {"f"})
    assert set().union(*(set(goods) for goods in original.values())) == all_goods
    assert set().union(*(set(goods) for goods in escape.values())) == all_goods
    assert sum(len(goods) for goods in original.values()) == len(all_goods)
    assert sum(len(goods) for goods in escape.values()) == len(all_goods)

    relation = {
        target: sorted(
            source
            for source in AGENTS
            if desired_subsets(values, base_value, source, original[target])
        )
        for target in ("r", "q", "c", "s")
    }
    assert relation == {
        "r": ["r", "s"],
        "q": ["c"],
        "c": ["c"],
        "s": ["c"],
    }
    assert frozenset({"z"}) in desired_subsets(
        values, base_value, "c", original["s"]
    )
    assert not is_efx(values, original)
    assert is_efx(values, escape)
    assert lex_endpoint_succeeds(values, old, escape)

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "owner-union-compression-hardened-profile-audit-v1",
        "status": "VERIFIED_EFX_ESCAPE",
        "profile_flags": {
            "positive": True,
            "subset_sum_injective": True,
            "flower_master_valid": True,
            "live_polarity_valid": True,
            "basic_pi_free": True,
        },
        "defect_record": {
            "response_relation": relation,
            "minimal_defect_targets": ["q", "s"],
            "sole_source": "c",
            "selected_core": ["z"],
        },
        "escape_record": {
            "efx": True,
            "lex_endpoint": True,
            "owner_union": ["c", "q", "s"],
            "moved_good_count": sum(
                good not in escape[owner]
                for owner, goods in old.items()
                for good in goods
            ) + int("f" not in escape["_"]),
        },
        "claim_boundary": payload["claim_boundary"],
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
