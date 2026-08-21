#!/usr/bin/env python3
"""Exhaust every tame cell and its pattern-dependent one-anchor repairs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

from .decide_fixed_u_mixed_anchor_menu import audit_mixed, mixed_oracle
from .fixed_u_dynamic_anchor import role_slack
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS
from .run_fixed_u_multi_split_chart_theorem import (
    exact_audit,
    numeric_oracle,
    pattern_key,
    role_patterns,
)


def rows(raw, key):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[key].items()
    }


def atomic_write(path, payload):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def run(profile_path, output_path, edge_cap=4, timeout_seconds=60):
    raw = json.loads(profile_path.read_text())
    totals = rows(raw, "terminal_profile_totals")
    minima = rows(raw, "terminal_profile_minima")
    tame_roles = [
        role for role in GOODS if role_slack(totals, minima, role) == 2
    ]
    eligible_anchors = [
        role for role in GOODS if role_slack(totals, minima, role) >= 2
    ]
    result = {
        "schema": "fixed-u-pattern-dependent-mixed-menu-audit-v1",
        "status": "RUNNING",
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "edge_cap": edge_cap,
        "timeout_seconds_per_lane": timeout_seconds,
        "tame_roles": tame_roles,
        "eligible_anchor_roles": eligible_anchors,
        "cells": [],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_write(output_path, result)

    unknowns = []
    for tame_role in tame_roles:
        for side_pattern in role_patterns():
            vector = {tame_role: side_pattern}
            key = pattern_key((tame_role,), vector)
            allocation = numeric_oracle(
                totals, minima, (tame_role,), vector, edge_cap
            )
            if allocation is not None:
                edges = exact_audit(
                    allocation, totals, minima, (tame_role,), vector, edge_cap
                )
                cell = {
                    "tame_role": tame_role,
                    "pattern": key,
                    "status": "sat",
                    "kind": "tame",
                    "edges": [list(edge) for edge in edges],
                    "allocation": allocation,
                }
                result["cells"].append(cell)
                atomic_write(output_path, result)
                continue

            found = None
            lane_unknowns = []
            lanes_examined = 0
            for anchor_role in eligible_anchors:
                if anchor_role == tame_role:
                    continue
                for anchor in OWNERS:
                    lanes_examined += 1
                    status, allocation = mixed_oracle(
                        totals, minima, tame_role, vector,
                        anchor_role, anchor, edge_cap, timeout_seconds,
                    )
                    if status == "sat":
                        edges, slack = audit_mixed(
                            allocation, totals, minima, tame_role, vector,
                            anchor_role, anchor, edge_cap,
                        )
                        found = {
                            "tame_role": tame_role,
                            "pattern": key,
                            "status": "sat",
                            "kind": "mixed_anchor",
                            "anchor_role": anchor_role,
                            "anchor_observer": anchor,
                            "lanes_examined": lanes_examined,
                            "edges": edges,
                            "minimum_certified_slack": str(slack),
                            "allocation": allocation,
                        }
                        break
                    if status == "unknown":
                        lane_unknowns.append({
                            "anchor_role": anchor_role,
                            "anchor_observer": anchor,
                        })
                if found is not None:
                    break

            if found is not None:
                cell = found
            else:
                status = "unknown" if lane_unknowns else "unsat"
                cell = {
                    "tame_role": tame_role,
                    "pattern": key,
                    "status": status,
                    "kind": "no_mixed_anchor",
                    "lanes_examined": lanes_examined,
                    "unknown_lanes": lane_unknowns,
                }
                if lane_unknowns:
                    unknowns.append(cell)
            result["cells"].append(cell)
            atomic_write(output_path, result)

    failing = {
        role: [cell["pattern"] for cell in result["cells"]
               if cell["tame_role"] == role and cell["status"] == "unsat"]
        for role in tame_roles
    }
    result["cell_count"] = len(result["cells"])
    result["sat_cell_count"] = sum(
        cell["status"] == "sat" for cell in result["cells"]
    )
    result["unsat_cell_count"] = sum(
        cell["status"] == "unsat" for cell in result["cells"]
    )
    result["unknown_cell_count"] = len(unknowns)
    result["failing_patterns_by_tame_role"] = failing
    if unknowns:
        result["status"] = "UNKNOWN_PATTERN_DEPENDENT_MIXED_MENU"
    elif all(failing[role] for role in tame_roles):
        result["status"] = "SAT_PATTERN_DEPENDENT_MIXED_MENU_OBSTRUCTION"
    else:
        closing = next(role for role in tame_roles if not failing[role])
        result["status"] = "VERIFIED_PATTERN_DEPENDENT_MIXED_MENU"
        result["closing_tame_role"] = closing
    result["claim_boundary"] = (
        "A SAT obstruction means that every possible tame conditioning role "
        "has an exact witness-side cell with no tame allocation and no "
        "one-anchor repair over any role, observer, recipients, or four-edge "
        "support topology. It does not rule out three split roles or EFX."
    )
    atomic_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    result = run(
        args.profile, args.output, args.edge_cap, args.timeout_seconds
    )
    print(json.dumps({
        key: result[key] for key in (
            "status", "cell_count", "sat_cell_count",
            "unsat_cell_count", "unknown_cell_count",
            "failing_patterns_by_tame_role",
        )
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
