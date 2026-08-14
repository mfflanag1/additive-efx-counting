#!/usr/bin/env python3
"""Exact finite-source audit of the three-reservoir response fan."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(repo: Path) -> dict:
    agents = tuple(range(4))
    full_source_count = 0
    cycle_count = 0
    checked = 0
    for target_owner in agents:
        reservoirs = tuple(a for a in agents if a != target_owner)
        for e_source in agents:
            if e_source == target_owner:
                continue
            for heads in itertools.product(agents, repeat=3):
                edge = dict(zip(reservoirs, heads))
                # Positivity and strict containment prohibit self-sourcing.
                if any(edge[h] == h for h in reservoirs):
                    continue
                checked += 1
                sources = {e_source, *heads}
                if len(sources) == 4:
                    full_source_count += 1

                # Include the omitted fourth provenance edge: the target
                # owner supplies E to its nonself source.
                edge[target_owner] = e_source
                has_cycle = False
                for start in agents:
                    seen = []
                    vertex = start
                    while vertex not in seen:
                        seen.append(vertex)
                        vertex = edge[vertex]
                    if vertex in seen:
                        has_cycle = True
                        break
                assert has_cycle
                cycle_count += 1

    assert checked == 324
    assert cycle_count == checked

    results = repo / "results"
    theorem = results / "NORMALIZATION_BYPASS_THREE_RESERVOIR_FAN_DICHOTOMY_20260813.md"
    reversal = results / "NORMALIZATION_BYPASS_RESERVOIR_REVERSAL_LEMMA_20260813.md"
    reversal_audit = results / "normalization_bypass_reservoir_reversal_audit.json"
    script = Path(__file__).resolve()
    return {
        "schema": "normalization-bypass-three-reservoir-fan-audit-v1",
        "status": "ALL_UNSAFE_FAN_ALWAYS_HAS_SUPPLIER_CLOSED_PI_CYCLE",
        "source_assignments_checked": checked,
        "rank_four_assignments": full_source_count,
        "supplier_cycle_assignments": cycle_count,
        "full_source_route": "rank_four_current_response_EFX",
        "cycle_route": "release_compatible_PI_cycle",
        "survivor": "safe_threshold_payment_branch_only",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "exact four-edge supplied-cycle endpoint for the all-unsafe fan; "
            "the safe threshold-payment branch remains open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "reversal": str(reversal.relative_to(repo)),
            "reversal_sha256": sha256(reversal),
            "reversal_audit": str(reversal_audit.relative_to(repo)),
            "reversal_audit_sha256": sha256(reversal_audit),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "rank_four_assignments": result["rank_four_assignments"],
        "supplier_cycle_assignments": result["supplier_cycle_assignments"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
