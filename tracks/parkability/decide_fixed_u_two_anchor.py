#!/usr/bin/env python3
"""Fail-closed exhaustive decision of the universal two-anchor mechanism."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from fractions import Fraction
from pathlib import Path

from .fixed_u_dynamic_anchor import role_slack
from .fixed_u_two_anchor import audit_two_anchor, two_anchor_oracle_for_pair
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def load_rows(raw, stem):
    key = next(
        key for key in (f"terminal_profile_{stem}", f"countermodel_{stem}")
        if key in raw
    )
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[key].items()
    }


def atomic_write(path, payload):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def lane_key(split_roles, anchors):
    return "|".join(f"{role}:{anchors[role]}" for role in split_roles)


def run(profile_path, output_path, edge_cap, timeout_seconds,
        pair_modulus=1, pair_remainder=0):
    raw = json.loads(profile_path.read_text())
    totals = load_rows(raw, "totals")
    minima = load_rows(raw, "minima")
    eligible = [role for role in GOODS if role_slack(totals, minima, role) >= 2]
    pairs = [
        pair for index, pair in enumerate(itertools.combinations(eligible, 2))
        if index % pair_modulus == pair_remainder
    ]

    previous = json.loads(output_path.read_text()) if output_path.exists() else None
    records = previous["records"] if previous is not None else []
    completed = {record["key"] for record in records}
    result = {
        "schema": "fixed-u-two-anchor-decision-v1",
        "status": "RUNNING",
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "edge_cap": edge_cap,
        "timeout_seconds_per_lane": timeout_seconds,
        "pair_modulus": pair_modulus,
        "pair_remainder": pair_remainder,
        "eligible_roles": eligible,
        "assigned_role_pairs": [list(pair) for pair in pairs],
        "records": records,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_write(output_path, result)

    for split_roles in pairs:
        for anchor_pair in itertools.product(OWNERS, repeat=2):
            anchors = dict(zip(split_roles, anchor_pair))
            key = lane_key(split_roles, anchors)
            if key in completed:
                continue
            status, allocation, reason = two_anchor_oracle_for_pair(
                totals, minima, split_roles, anchors,
                edge_cap, timeout_seconds,
            )
            record = {
                "key": key,
                "split_roles": list(split_roles),
                "anchors": anchors,
                "status": status,
            }
            if status == "sat":
                edges, slack = audit_two_anchor(
                    allocation, totals, minima, split_roles, anchors, edge_cap
                )
                record.update({
                    "allocation": allocation,
                    "edges": [list(edge) for edge in edges],
                    "minimum_certified_slack": str(slack),
                })
            elif status == "unknown":
                record["reason_unknown"] = reason
            records.append(record)
            completed.add(key)
            atomic_write(output_path, result)
            if status == "sat":
                result["status"] = "SAT_TWO_ANCHOR_CERTIFICATE"
                result["certificate"] = record
                atomic_write(output_path, result)
                return result

    unknowns = [record for record in records if record["status"] == "unknown"]
    result["status"] = (
        "UNKNOWN_TWO_ANCHOR_DECISION" if unknowns
        else "UNSAT_NO_UNIVERSAL_TWO_ANCHOR_CERTIFICATE"
    )
    result["lane_count"] = len(records)
    result["unknown_count"] = len(unknowns)
    atomic_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=10)
    parser.add_argument("--pair-modulus", type=int, default=1)
    parser.add_argument("--pair-remainder", type=int, default=0)
    args = parser.parse_args()
    result = run(
        args.profile, args.output, args.edge_cap, args.timeout_seconds,
        args.pair_modulus, args.pair_remainder,
    )
    print(json.dumps({
        "status": result["status"],
        "lane_count": len(result["records"]),
        "unknown_count": sum(
            record["status"] == "unknown" for record in result["records"]
        ),
        "certificate": result.get("certificate", {}).get("key"),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
