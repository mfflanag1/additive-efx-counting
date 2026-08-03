#!/usr/bin/env python3
"""Audit lexicographic owner-utility tie-breaks on threshold maxima."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_unique_defect_handoff import load_record_values
    from .scan_charity_threshold_absorption import (
        absorption_margin,
        theta_maximizers,
    )
except ImportError:
    from anneal import atomic_json
    from audit_unique_defect_handoff import load_record_values
    from scan_charity_threshold_absorption import absorption_margin, theta_maximizers


SCHEMA = "threshold-utility-tiebreak-audit-v2"


def analyze(values):
    landscape = theta_maximizers(values, 1)
    n = len(values)
    totals = landscape["totals"]
    states = landscape["maximizers"]
    records = []
    for masks, charity in states:
        utilities = tuple(totals[agent][masks[agent]] for agent in range(n))
        margin, _witness = absorption_margin(
            masks,
            charity,
            totals,
            landscape["thresholds"],
            landscape["row_totals"],
        )
        records.append((masks, charity, utilities, margin))
    order_records = []
    for order in itertools.permutations(range(n)):
        best_key = max(
            tuple(record[2][agent] for agent in order) for record in records
        )
        maximizers = [
            record
            for record in records
            if tuple(record[2][agent] for agent in order) == best_key
        ]
        absorbing = [record for record in maximizers if record[3] >= 0]
        order_records.append(
            {
                "order": list(order),
                "utility_key": list(best_key),
                "maximizer_count": len(maximizers),
                "absorbing_maximizer_count": len(absorbing),
                "best_absorption_margin": str(max(record[3] for record in maximizers)),
            }
        )
    blocked = [
        record for record in order_records if record["absorbing_maximizer_count"] == 0
    ]
    return {
        "eligible_state_count": landscape["eligible_state_count"],
        "theta_maximizer_count": len(states),
        "agent_order_count": len(order_records),
        "absorbing_order_count": len(order_records) - len(blocked),
        "blocked_order_count": len(blocked),
        "blocked_orders": blocked,
    }


def load_extra_values(path):
    document = json.loads(path.read_text())
    raw = document.get("values", document.get("candidate_values"))
    if raw is None and "positive_nondegenerate_lift" in document:
        raw = document["positive_nondegenerate_lift"].get("values")
    if raw is None:
        raise ValueError(f"{path} contains no supported value matrix")
    return tuple(tuple(int(entry) for entry in row) for row in raw)


def run(source, output, extras=()):
    if output.exists():
        raise ValueError("output must be new")
    document = json.loads(source.read_text())
    records = []
    for profile in document["records"]:
        values = load_record_values(profile)
        records.append(
            {
                "source": profile["source"],
                "values_sha256": profile["values_sha256"],
                **analyze(values),
            }
        )
    for path in extras:
        values = load_extra_values(path)
        records.append(
            {
                "source": str(path),
                "values_sha256": hashlib.sha256(
                    json.dumps(values, separators=(",", ":")).encode()
                ).hexdigest(),
                **analyze(values),
            }
        )
    blocked_profiles = [record for record in records if record["blocked_order_count"]]
    result = {
        "schema": SCHEMA,
        "status": (
            "ALL_UTILITY_TIEBREAKS_ABSORB"
            if not blocked_profiles
            else "BLOCKED_UTILITY_TIEBREAK_FOUND"
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "extra_sources": [
            {
                "source": str(path),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in extras
        ],
        "profile_count": len(records),
        "agent_order_count": sum(record["agent_order_count"] for record in records),
        "absorbing_order_count": sum(
            record["absorbing_order_count"] for record in records
        ),
        "blocked_order_count": sum(record["blocked_order_count"] for record in records),
        "records": records,
        "claim_boundary": (
            "This is an exact finite-corpus audit. It does not prove the "
            "threshold/utility selector or complete EFX existence."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--extra", action="append", default=[], type=Path)
    args = parser.parse_args()
    result = run(args.source, args.output, args.extra)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "profile_count",
                    "agent_order_count",
                    "absorbing_order_count",
                    "blocked_order_count",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
