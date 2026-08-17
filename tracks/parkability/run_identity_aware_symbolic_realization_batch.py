#!/usr/bin/env python3
"""Symbolic-realization CEGAR over the high-slack banked adversarial profiles.

Profiles whose every role has slack at most two are already settled by the
witness-side driver, because there the two-good family is every realization
(Corollary B1).  This driver targets the rest: for each profile with a role of
slack three or more it sweeps role-cardinality vectors up to `cap` and runs the
symbolic-value CEGAR, in which every physical good value is a solver unknown
constrained to sum to `T` with minimum `M`.

Profiles are ordered by maximum role slack, so the ones the cap actually closes
are decided first.  A profile is reported exhaustive exactly when the cap
covers every role, that is when `cap >= rho(g)` for all `g`; otherwise its
verdict covers only realizations with at most `cap` goods per role, and the
record says so.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from .run_identity_aware_symbolic_realization_cegar import (
    cardinality_vectors,
    slack,
    solve_configuration,
)
from .run_identity_aware_witness_side_batch import distinct_profiles
from .run_fixed_u_full_packet_terminal_cegar import GOODS


def run(trace_paths, output_path, cap, edge_cap, maximum_rounds,
        timeout_seconds, max_vectors, profile_budget_seconds, limit):
    population = distinct_profiles(trace_paths)
    targets = []
    for index, profile in enumerate(population):
        slacks = {
            role: int(slack(profile["totals"], profile["minima"], role))
            for role in GOODS
        }
        peak = max(slacks.values())
        if peak <= 2:
            continue
        targets.append((peak, index, profile, slacks))
    targets.sort(key=lambda entry: (entry[0], entry[1]))
    high_slack_population = len(targets)
    if limit is not None:
        targets = targets[:limit]

    records = []
    countermodel = None
    for peak, index, profile, slacks in targets:
        vectors = list(cardinality_vectors(profile["totals"], profile["minima"], cap))
        record = {
            "population_index": index,
            "source": profile["source"],
            "source_iteration": profile["iteration"],
            "maximum_role_slack": peak,
            "role_slacks": slacks,
            "cap_covers_every_role": peak <= cap,
            "cardinality_vectors_available": len(vectors),
        }
        if len(vectors) > max_vectors:
            record["status"] = "VECTOR_LIMIT"
            record["cardinality_vectors_examined"] = 0
            records.append(record)
            print(index, "peak", peak, "VECTOR_LIMIT", len(vectors), flush=True)
            continue

        started = time.monotonic()
        outcomes = []
        for counts in vectors:
            if time.monotonic() - started > profile_budget_seconds:
                outcomes.append({"status": "TIME_BUDGET", "rounds": 0,
                                 "role_cardinalities": counts})
                continue
            outcome = solve_configuration(
                profile["totals"], profile["minima"], counts,
                edge_cap, maximum_rounds, timeout_seconds,
            )
            outcome["role_cardinalities"] = counts
            outcomes.append(outcome)
            if outcome["status"] == "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL":
                break

        statuses = {outcome["status"] for outcome in outcomes}
        record["cardinality_vectors_examined"] = len(outcomes)
        record["configuration_statuses"] = dict(Counter(statuses))
        record["cegar_rounds"] = sum(o.get("rounds", 0) for o in outcomes)
        record["elapsed_seconds"] = round(time.monotonic() - started, 1)
        if "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL" in statuses:
            record["status"] = "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL"
            record["terminal"] = next(
                o for o in outcomes
                if o["status"] == "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL"
            )
            countermodel = record
        elif statuses == {"UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION"}:
            record["status"] = "UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION"
        else:
            record["status"] = "INCOMPLETE"
        records.append(record)
        print(index, "peak", peak, record["status"],
              "vectors", len(outcomes), "rounds", record["cegar_rounds"],
              "exhaustive", record["cap_covers_every_role"],
              f"{record['elapsed_seconds']}s", flush=True)
        if countermodel is not None:
            break

    settled = [
        record for record in records
        if record["status"] == "UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION"
    ]
    result = {
        "schema": "identity-aware-symbolic-realization-batch-v1",
        "status": (
            "IDENTITY_SENSITIVE_FOUR_EDGE_COUNTERMODEL" if countermodel
            else "NO_COUNTERMODEL_IN_EXAMINED_POPULATION"
        ),
        "traces": [
            {"path": str(path),
             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in trace_paths
        ],
        "population_size": len(population),
        "slack_two_profiles_already_exact": len(population) - high_slack_population,
        "high_slack_population": high_slack_population,
        "high_slack_targets_after_limit": len(targets),
        "profiles_examined": len(records),
        "maximum_slack_examined": max(
            (record["maximum_role_slack"] for record in records), default=None
        ),
        "cardinality_cap": cap,
        "edge_cap": edge_cap,
        "status_tally": dict(Counter(record["status"] for record in records)),
        "newly_exhaustive_profiles": sum(
            1 for record in settled if record["cap_covers_every_role"]
        ),
        "settled_but_capped_profiles": sum(
            1 for record in settled if not record["cap_covers_every_role"]
        ),
        "records": records,
        "terminal": countermodel,
        "claim_boundary": (
            "A record with cap_covers_every_role true and status unsat is exact "
            "for every physical realization of that profile.  A record with the "
            "flag false covers only realizations with at most `cap` goods per "
            "role.  Profiles whose every role has slack at most two are not in "
            "this population; they are already exact from the witness-side "
            "driver.  Nothing here establishes chart coverage or the universal "
            "fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cap", type=int, default=3)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--maximum-rounds", type=int, default=200)
    parser.add_argument("--timeout-seconds", type=int, default=90)
    parser.add_argument("--max-vectors", type=int, default=16)
    parser.add_argument("--profile-budget-seconds", type=int, default=1800)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    result = run(tuple(args.trace), args.output, args.cap, args.edge_cap,
                 args.maximum_rounds, args.timeout_seconds, args.max_vectors,
                 args.profile_budget_seconds, args.limit)
    print(json.dumps({
        "status": result["status"],
        "profiles_examined": result["profiles_examined"],
        "status_tally": result["status_tally"],
        "newly_exhaustive_profiles": result["newly_exhaustive_profiles"],
    }, indent=2))


if __name__ == "__main__":
    main()
