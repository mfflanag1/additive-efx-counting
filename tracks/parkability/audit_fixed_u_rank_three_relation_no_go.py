#!/usr/bin/env python3
"""Solver-independent audit of the rank-gated fixed-U radius-three no-go."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from .analyze_fixed_u_no_go_response_relations import run as response_analysis
from .audit_fixed_u_radius_three_exchange_no_go import (
    OWNERS,
    PACKETS,
    audit as packet_audit,
    tail,
)


def has_record(records, source, target, subset):
    wanted = sorted(subset)
    return any(
        record["source"] == source
        and record["target"] == target
        and sorted(record["subset"]) == wanted
        for record in records
    )


def audit(source: Path, iteration: int):
    base = packet_audit(source, iteration)
    response = response_analysis(source, iteration)
    payload = json.loads(source.read_text())
    record = next(record for record in payload["rounds"] if record["iteration"] == iteration)
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in record["values"].items()
    }
    support_ordinary = response["states"]["support"]["ordinary_base_floor"]
    named_core_checks = {
        "root_A_is_common_safe": all(tail(values, owner, PACKETS["A"]) <= 1 for owner in OWNERS),
        "q_Q_is_common_safe": all(tail(values, owner, PACKETS["Q"]) <= 1 for owner in OWNERS),
        "s_E_is_common_safe": all(tail(values, owner, PACKETS["E"]) <= 1 for owner in OWNERS),
        "root_A_edge_present": has_record(support_ordinary, "r", "r", PACKETS["A"]),
        "q_Q_edge_present": has_record(support_ordinary, "q", "q", PACKETS["Q"]),
        "s_E_edge_present": has_record(support_ordinary, "s", "s", PACKETS["E"]),
    }
    ranks = {
        state: {
            "ordinary": len(data["ordinary_maximum_matching"]),
            "current": len(data["current_maximum_matching"]),
            "mixed": len(data["mixed_maximum_matching"]),
        }
        for state, data in response["states"].items()
    }
    rank_gate_checks = {
        "support_mixed_rank_three": ranks["support"]["mixed"] == 3,
        "split_ordinary_rank_at_most_three": ranks["split"]["ordinary"] <= 3,
        "reassembly_mixed_rank_three": ranks["reassembly"]["mixed"] == 3,
    }
    checks = {
        "packet_premises": base["all_premises_hold"],
        "exact_radius_three_no_go": base["radius_three_no_go_verified"],
        **named_core_checks,
        **rank_gate_checks,
    }
    return {
        "schema": "fixed-u-rank-three-relation-radius-three-no-go-audit-v1",
        "status": "RANK_GATED_RADIUS_THREE_SELECTOR_REFUTED" if all(checks.values()) else "AUDIT_FAILED",
        "source": f"results/{source.name}",
        "source_iteration_sha256": hashlib.sha256(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "source_iteration": iteration,
        "checks": checks,
        "response_ranks": ranks,
        "response_matchings": {
            state: {
                "ordinary": data["ordinary_maximum_matching"],
                "current": data["current_maximum_matching"],
                "mixed": data["mixed_maximum_matching"],
            }
            for state, data in response["states"].items()
        },
        "efx_lex_escapes_by_exact_radius": base["efx_lex_escapes_by_exact_radius"],
        "allocations_examined_by_exact_radius": base["allocations_examined_by_exact_radius"],
        "recorded_radius_four_menu_size": base["recorded_radius_four_menu_size"],
        "recorded_menu_matches_exact_radius_four_set": base[
            "recorded_menu_matches_exact_radius_four_set"
        ],
        "claim_boundary": (
            "exact positive-rational twelve-atom profile satisfying the declared "
            "packet premises and necessary support/split/reassembly rank-three "
            "response gates, with no EFX lex improvement moving at most three goods; "
            "full signed-repeat reachability, deterministic priority records, all "
            "Hall resets, and cap-free packet exchange remain unencoded"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--iteration", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source, args.iteration)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "response_ranks": result["response_ranks"],
        "escapes": result["efx_lex_escapes_by_exact_radius"],
    }, indent=2))


if __name__ == "__main__":
    main()
