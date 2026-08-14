#!/usr/bin/env python3
"""Independent exact audit of the support-provenance three-edge no-go."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .analyze_fixed_u_no_go_response_relations import (
    SUPPORT,
    maximum_matching,
    relation,
)
from .audit_fixed_u_radius_three_exchange_no_go import (
    OWNERS,
    PACKETS,
    check_premises,
    tail,
    total,
)
from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
    provenance_holder,
)


def complete_efx(values, allocation):
    if allocation["charity"]:
        return False
    for observer in OWNERS:
        own = total(values, observer, allocation[observer])
        for target in OWNERS:
            if target != observer and own < tail(values, observer, allocation[target]):
                return False
    return True


def edge_count(allocation):
    initial = provenance_holder(SUPPORT)
    final = {
        good: owner for owner, goods in allocation.items() for good in goods
    }
    return len({
        (initial[good], final[good])
        for good in initial if initial[good] != final[good]
    })


def response_ranks(values):
    from .audit_fixed_u_radius_three_exchange_no_go import BASE, REASSEMBLY, SPLIT

    states = {"support": SUPPORT, "split": SPLIT, "reassembly": REASSEMBLY}
    result = {}
    for name, state in states.items():
        ordinary = relation(values, state, BASE)
        current = relation(values, state, state)
        result[name] = {
            "ordinary": len(maximum_matching(ordinary)),
            "current": len(maximum_matching(current)),
            "mixed": len(maximum_matching(ordinary + current)),
        }
    return result


def audit(source: Path, iteration: int):
    payload = json.loads(source.read_text())
    record = next(r for r in payload["rounds"] if r["iteration"] == iteration)
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in record["values"].items()
    }
    premise_checks = check_premises(values)
    named_core_checks = {
        f"{source_owner}_{packet}_common_safe": all(
            tail(values, observer, PACKETS[packet]) <= 1 for observer in OWNERS
        )
        and total(values, source_owner, PACKETS[packet]) > 1
        for source_owner, packet in (("r", "A"), ("q", "Q"), ("s", "E"))
    }
    d_floor = total(values, "d", PACKETS["W"])
    root_checks = {
        "d_strongly_envies_A": d_floor < tail(values, "d", PACKETS["A"]),
        "d_safe_against_Q": d_floor >= tail(values, "d", PACKETS["Q"]),
        "d_safe_against_E": d_floor >= tail(values, "d", PACKETS["E"]),
        "d_safe_against_P": d_floor >= total(values, "d", PACKETS["P"]),
    }
    ranks = response_ranks(values)
    rank_checks = {
        "support_mixed_rank_three": ranks["support"]["mixed"] == 3,
        "split_ordinary_rank_at_most_three": ranks["split"]["ordinary"] <= 3,
        "reassembly_mixed_rank_three": ranks["reassembly"]["mixed"] == 3,
    }

    examined = Counter()
    escapes = Counter()
    escape_keys = {edge: set() for edge in range(5)}
    for allocation in allocations_with_at_most_edges(4, SUPPORT):
        edges = edge_count(allocation)
        examined[edges] += 1
        if complete_efx(values, allocation):
            escapes[edges] += 1
            canonical = {owner: sorted(goods) for owner, goods in allocation.items()}
            escape_keys[edges].add(json.dumps(canonical, sort_keys=True))
    recorded = {
        json.dumps({owner: sorted(goods) for owner, goods in allocation.items()}, sort_keys=True)
        for allocation in record["blocking_allocations"]
    }
    exact_menu = recorded == escape_keys[4]
    checks = {
        **premise_checks,
        **named_core_checks,
        **root_checks,
        **rank_checks,
        "no_complete_efx_through_three_edges": sum(escapes[e] for e in range(4)) == 0,
        "four_edge_completion_exists": escapes[4] > 0,
        "recorded_menu_is_exact_four_edge_set": exact_menu,
    }
    return {
        "schema": "fixed-u-support-edge-three-no-go-audit-v1",
        "status": "SUPPORT_EDGE_BOUND_THREE_REFUTED" if all(checks.values()) else "AUDIT_FAILED",
        "source": f"results/{source.name}",
        "source_iteration_sha256": hashlib.sha256(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "source_iteration": iteration,
        "checks": checks,
        "response_ranks": ranks,
        "allocations_examined_by_exact_edge_count": {
            str(edge): examined[edge] for edge in range(5)
        },
        "complete_efx_by_exact_edge_count": {
            str(edge): escapes[edge] for edge in range(5)
        },
        "recorded_four_edge_menu_size": len(recorded),
        "claim_boundary": (
            "exact positive-rational twelve-atom profile satisfying the declared "
            "packet, root-facing, and necessary rank-three gates, with no complete "
            "EFX allocation through at most three support-provenance packet edges "
            "and exactly the recorded four-edge completions. Full response "
            "saturation and signed recurrence reachability remain unencoded; this "
            "proves sharpness only in the declared atomization."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--iteration", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source, args.iteration)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "complete_efx": result["complete_efx_by_exact_edge_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
