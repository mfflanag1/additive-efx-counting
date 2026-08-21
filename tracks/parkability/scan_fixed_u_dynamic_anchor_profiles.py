#!/usr/bin/env python3
"""Calibrate the exhaustive dynamic-anchor oracle on retained form-2 profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .fixed_u_dynamic_anchor import (
    anchor_oracle_for_role,
    dynamic_anchor_oracle,
    exact_audit_anchor,
    exact_audit_whole,
    placement_edges,
    whole_role_oracle,
)


OWNERS = ("r", "q", "d", "s")


def canonical_payload(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def fraction_rows(raw, key):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[key].items()
    }


def load_ledger(path):
    records = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        digest = record.pop("payload_sha256")
        assert hashlib.sha256(canonical_payload(record).encode()).hexdigest() == digest
        record["payload_sha256"] = digest
        assert record["iteration"] == len(records)
        records.append(record)
    return records


def serialize_candidate(kind, allocation, edges, slack, split_role=None, anchor=None):
    result = {
        "kind": kind,
        "allocation": allocation,
        "edges": [list(edge) for edge in edges],
        "minimum_certified_slack": str(slack),
    }
    if split_role is not None:
        result["split_role"] = split_role
        result["anchor_observer"] = anchor
    return result


def close_profile(totals, minima, timeout_seconds):
    status, allocation, reason = whole_role_oracle(
        totals, minima, timeout_seconds=timeout_seconds
    )
    if status == "sat":
        edges, slack = exact_audit_whole(allocation, totals, minima)
        return "whole", serialize_candidate("whole", allocation, edges, slack), None
    if status == "unknown":
        return "unknown", None, {"whole_reason": reason}

    status, candidate, reason = dynamic_anchor_oracle(
        totals, minima, timeout_seconds=timeout_seconds
    )
    if status == "sat":
        edges, slack = exact_audit_anchor(
            candidate["allocation"], totals, minima,
            candidate["split_role"], candidate["anchor_observer"],
        )
        return "anchor", serialize_candidate(
            "anchor", candidate["allocation"], edges, slack,
            candidate["split_role"], candidate["anchor_observer"],
        ), None
    return status, None, reason


def run(ledger_path, terminal_profile_path, output_path, timeout_seconds):
    records = load_ledger(ledger_path)
    rows = []
    for record in records:
        totals = fraction_rows(record["round"], "totals")
        minima = fraction_rows(record["round"], "minima")
        status, candidate, reason = close_profile(totals, minima, timeout_seconds)
        row = {
            "iteration": record["iteration"],
            "source_payload_sha256": record["payload_sha256"],
            "prior_branch": record["round"]["branch"],
            "status": status,
        }
        if candidate is not None:
            row["candidate"] = candidate
        if reason is not None:
            row["reason"] = reason
        rows.append(row)
        print(record["iteration"], status, flush=True)
        if status == "unknown":
            break

    terminal = json.loads(terminal_profile_path.read_text())
    terminal_totals = fraction_rows(terminal, "profile_totals")
    terminal_minima = fraction_rows(terminal, "profile_minima")
    terminal_status, terminal_candidate, terminal_reason = close_profile(
        terminal_totals, terminal_minima, timeout_seconds
    )

    calibration = {}
    for name, role, anchor in (
        ("A_q_min_a1", "a1", "q"),
        ("B_r_min_k", "k", "r"),
    ):
        status, allocation, reason = anchor_oracle_for_role(
            terminal_totals, terminal_minima, role, anchor,
            timeout_seconds=timeout_seconds,
        )
        assert status == "sat", (name, status, reason)
        edges, slack = exact_audit_anchor(
            allocation, terminal_totals, terminal_minima, role, anchor
        )
        calibration[name] = serialize_candidate(
            "anchor", allocation, edges, slack, role, anchor
        )

    counts = Counter(row["status"] for row in rows)
    anchor_types = Counter(
        (row["candidate"]["split_role"], row["candidate"]["anchor_observer"])
        for row in rows if row["status"] == "anchor"
    )
    result = {
        "schema": "fixed-u-dynamic-anchor-profile-calibration-v1",
        "status": (
            "ALL_RETAINED_PROFILES_CLOSED"
            if len(rows) == len(records) and set(counts) <= {"whole", "anchor"}
            else "INCOMPLETE_OR_OPEN_PROFILE"
        ),
        "ledger": str(ledger_path),
        "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        "retained_profile_count": len(records),
        "processed_profile_count": len(rows),
        "closure_counts": dict(counts),
        "anchor_type_counts": {
            f"{role}:{anchor}": count
            for (role, anchor), count in sorted(anchor_types.items())
        },
        "profiles": rows,
        "terminal_profile": str(terminal_profile_path),
        "terminal_profile_sha256": hashlib.sha256(
            terminal_profile_path.read_bytes()
        ).hexdigest(),
        "terminal_status": terminal_status,
        "terminal_candidate": terminal_candidate,
        "terminal_reason": terminal_reason,
        "required_terminal_calibrations": calibration,
        "normal_form": (
            "for rho=2, exact two-good selected-coordinate endpoints; for rho>=3, "
            "those endpoints plus the endpoints of the exact three-good interval "
            "[M,T-2M]; all higher cardinalities are nested"
        ),
        "claim_boundary": (
            "This is a complete calibration census, not the universal form-2 "
            "theorem. The CEGAR master must still prove no admissible profile "
            "defeats every whole-role and dynamic-anchor candidate."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--terminal-profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    args = parser.parse_args()
    result = run(
        args.ledger, args.terminal_profile, args.output, args.timeout_seconds
    )
    print(json.dumps({
        "status": result["status"],
        "closure_counts": result["closure_counts"],
        "anchor_type_counts": result["anchor_type_counts"],
        "terminal_status": result["terminal_status"],
    }, indent=2))


if __name__ == "__main__":
    main()
