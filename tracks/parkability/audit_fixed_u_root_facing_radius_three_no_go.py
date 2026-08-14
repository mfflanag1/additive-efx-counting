#!/usr/bin/env python3
"""Independent exact audit of the root-facing rank-three radius-3 no-go."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_rank_three_relation_no_go import audit as rank_audit
from .audit_fixed_u_radius_three_exchange_no_go import OWNERS, PACKETS, tail, total


def audit(source: Path, iteration: int):
    prior = rank_audit(source, iteration)
    payload = json.loads(source.read_text())
    record = next(record for record in payload["rounds"] if record["iteration"] == iteration)
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in record["values"].items()
    }
    d_floor = total(values, "d", PACKETS["W"])
    root_facing = {
        "d_strongly_envies_root_A": d_floor < tail(values, "d", PACKETS["A"]),
        "d_safe_against_q_Q": d_floor >= tail(values, "d", PACKETS["Q"]),
        "d_safe_against_s_E": d_floor >= tail(values, "d", PACKETS["E"]),
        "d_safe_against_support_charity_P": d_floor >= total(values, "d", PACKETS["P"]),
        "root_A_common_safe": all(tail(values, owner, PACKETS["A"]) <= 1 for owner in OWNERS),
    }
    checks = {**prior["checks"], **root_facing}
    return {
        "schema": "fixed-u-root-facing-radius-three-no-go-audit-v1",
        "status": "ROOT_FACING_RADIUS_THREE_SELECTOR_REFUTED" if all(checks.values()) else "AUDIT_FAILED",
        "source": f"results/{source.name}",
        "source_iteration_sha256": hashlib.sha256(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "source_iteration": iteration,
        "checks": checks,
        "root_facing_values": {
            "d_W": str(d_floor),
            "tail_d_A": str(tail(values, "d", PACKETS["A"])),
            "tail_d_Q": str(tail(values, "d", PACKETS["Q"])),
            "tail_d_E": str(tail(values, "d", PACKETS["E"])),
            "d_P": str(total(values, "d", PACKETS["P"])),
        },
        "response_ranks": prior["response_ranks"],
        "response_matchings": prior["response_matchings"],
        "efx_lex_escapes_by_exact_radius": prior["efx_lex_escapes_by_exact_radius"],
        "allocations_examined_by_exact_radius": prior["allocations_examined_by_exact_radius"],
        "recorded_radius_four_menu_size": prior["recorded_radius_four_menu_size"],
        "recorded_menu_matches_exact_radius_four_set": prior[
            "recorded_menu_matches_exact_radius_four_set"
        ],
        "claim_boundary": (
            "exact positive-rational root-facing twelve-atom profile satisfying the "
            "declared packet and necessary rank-three gates with no EFX lex "
            "improvement moving at most three goods; exact historical reachability, "
            "full signed-repeat consistency, deterministic selector records, all "
            "Hall resets, and cap-free four-packet exchange remain unencoded"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--iteration", type=int, default=13)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source, args.iteration)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "root_facing_values": result["root_facing_values"],
        "escapes": result["efx_lex_escapes_by_exact_radius"],
    }, indent=2))


if __name__ == "__main__":
    main()
