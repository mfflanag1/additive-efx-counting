#!/usr/bin/env python3
"""Run the identity-aware witness-side CEGAR over a banked CEGAR trace.

Each round of a form-2 physical CEGAR trace carries an exact totals/minima
profile that the solver produced as an adversarial candidate.  This driver
replays the witness-side CEGAR on every distinct such profile, so the question
"does witness identity ever defeat the four-support-edge conclusion?" is asked
of the banked adversarial population rather than of one hand-picked profile.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .run_identity_aware_witness_side_cegar import (
    concrete_values,
    decide,
    failure_clause,
    partition_of,
    role_layout,
    symbolic_values,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS

import z3


def distinct_profiles(trace_paths):
    """Distinct (totals, minima) profiles across the given traces, in order."""
    seen = {}
    for path in trace_paths:
        raw = json.loads(path.read_text())
        candidates = list(raw.get("rounds", []))
        if "countermodel_totals" in raw:
            candidates.append({
                "totals": raw["countermodel_totals"],
                "minima": raw["countermodel_minima"],
                "iteration": "terminal",
            })
        for entry in candidates:
            key = json.dumps(
                {"t": entry["totals"], "m": entry["minima"]}, sort_keys=True
            )
            if key in seen:
                continue
            seen[key] = {
                "source": path.name,
                "iteration": entry.get("iteration"),
                "totals": {
                    o: {g: Fraction(a) for g, a in row.items()}
                    for o, row in entry["totals"].items()
                },
                "minima": {
                    o: {g: Fraction(a) for g, a in row.items()}
                    for o, row in entry["minima"].items()
                },
            }
    return list(seen.values())


def slack(totals, minima, role):
    return min(totals[o][role] // minima[o][role] for o in OWNERS)


def solve_profile(totals, minima, edge_cap, maximum_rounds, timeout_seconds):
    role_goods, multi = role_layout(totals, minima)
    side = {
        (role, observer): z3.Bool(f"side_{role}_{observer}")
        for role in multi for observer in OWNERS
    }
    master = z3.Solver()
    master.add(*(z3.Not(side[role, "r"]) for role in multi))
    symbolic = symbolic_values(totals, minima, role_goods, side)

    canonical = {(role, o): False for role in multi for o in OWNERS}
    baseline_status, baseline_found, _ = decide(
        concrete_values(totals, minima, role_goods, canonical),
        role_goods, edge_cap, timeout_seconds,
    )
    used_rounds = 0
    if baseline_found is not None:
        master.add(failure_clause(baseline_found[0], symbolic))
        used_rounds = 1

    status = "ROUND_LIMIT"
    terminal_pattern = None
    for _ in range(maximum_rounds):
        outcome = master.check()
        if outcome == z3.unsat:
            status = "UNSAT_EVERY_SIDE_PATTERN_ADMITS_A_BANKED_ALLOCATION"
            break
        if outcome == z3.unknown:
            status = "UNKNOWN"
            break
        model = master.model()
        sides = {k: z3.is_true(model.eval(f)) for k, f in side.items()}
        physical = concrete_values(totals, minima, role_goods, sides)
        concrete_status, found, _ = decide(
            physical, role_goods, edge_cap, timeout_seconds
        )
        used_rounds += 1
        if concrete_status == "unsat":
            status = "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL"
            terminal_pattern = {
                role: partition_of(sides, multi, role) for role in multi
            }
            break
        if concrete_status != "sat":
            status = "UNKNOWN"
            break
        master.add(failure_clause(found[0], symbolic))
    return {
        "status": status,
        "baseline_status": baseline_status,
        "baseline_split_roles": baseline_found[1] if baseline_found else None,
        "cegar_rounds": used_rounds,
        "multi_good_roles": list(multi),
        "maximum_role_slack": str(max(slack(totals, minima, g) for g in GOODS)),
        "two_good_family_is_exhaustive": all(
            slack(totals, minima, g) <= 2 for g in GOODS
        ),
        "terminal_coincidence_partitions": terminal_pattern,
    }


def run(trace_paths, output_path, limit, edge_cap, maximum_rounds, timeout_seconds):
    profiles = distinct_profiles(trace_paths)
    if limit is not None:
        profiles = profiles[:limit]
    records = []
    for index, profile in enumerate(profiles):
        outcome = solve_profile(
            profile["totals"], profile["minima"],
            edge_cap, maximum_rounds, timeout_seconds,
        )
        outcome.update({
            "index": index,
            "source": profile["source"],
            "source_iteration": profile["iteration"],
        })
        records.append(outcome)
        print(index, profile["source"], profile["iteration"],
              outcome["status"], "rounds", outcome["cegar_rounds"],
              "exhaustive", outcome["two_good_family_is_exhaustive"], flush=True)

    tally = Counter(record["status"] for record in records)
    result = {
        "schema": "identity-aware-witness-side-batch-v1",
        "traces": [
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in trace_paths
        ],
        "distinct_profiles_available": len(distinct_profiles(trace_paths)),
        "profiles_examined": len(records),
        "status_tally": dict(tally),
        "exhaustive_profile_count": sum(
            1 for record in records if record["two_good_family_is_exhaustive"]
        ),
        "edge_cap": edge_cap,
        "records": records,
        "claim_boundary": (
            "For a profile whose every role slack is at most two, the two-good "
            "family is every physical realization of that profile, so an "
            "unsat verdict is exact for the profile.  For a profile with a "
            "wider role it covers only the two-good realizations.  Nothing "
            "here establishes chart coverage or the universal fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--maximum-rounds", type=int, default=40)
    parser.add_argument("--timeout-seconds", type=int, default=45)
    args = parser.parse_args()
    result = run(tuple(args.trace), args.output, args.limit, args.edge_cap,
                 args.maximum_rounds, args.timeout_seconds)
    print(json.dumps({
        "profiles_examined": result["profiles_examined"],
        "status_tally": result["status_tally"],
        "exhaustive_profile_count": result["exhaustive_profile_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
