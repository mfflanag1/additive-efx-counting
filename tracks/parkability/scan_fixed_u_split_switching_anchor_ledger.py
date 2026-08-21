#!/usr/bin/env python3
"""Test the two anchor lemmas on every retained form-2 chart profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_split_switching_anchor_lemma import (
    LEMMAS,
    audit_lemma,
    load_rows,
)


def canonical_payload(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def load_ledger(path):
    records = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        digest = record.pop("payload_sha256")
        assert hashlib.sha256(canonical_payload(record).encode()).hexdigest() == digest
        record["payload_sha256"] = digest
        assert record["iteration"] == len(records)
        assert "totals" in record["round"] and "minima" in record["round"]
        records.append(record)
    return records


def summarize_audit(audit):
    if not audit["applicable"]:
        return {
            "applicable": False,
            "verified": False,
            "reason": audit["reason"],
        }
    worst = min(
        audit["inequalities"],
        key=lambda item: Fraction(item["certified_slack_lower_bound"]),
    )
    return {
        "applicable": True,
        "verified": audit["verified"],
        "minimum_certified_slack": audit["minimum_certified_slack"],
        "worst_inequality": {
            key: worst[key]
            for key in (
                "observer", "target", "deletion",
                "certified_slack_lower_bound",
            )
        },
    }


def evaluate_profile(totals, minima):
    return {
        name: summarize_audit(audit_lemma(
            name, lemma, totals, minima, require_nonnegative=False
        ))
        for name, lemma in LEMMAS.items()
    }


def run(ledger_path, terminal_profile_path, output_path):
    records = load_ledger(ledger_path)
    rows = []
    for record in records:
        totals = load_rows(record["round"], "totals")
        minima = load_rows(record["round"], "minima")
        rows.append({
            "iteration": record["iteration"],
            "branch": record["round"]["branch"],
            "source_payload_sha256": record["payload_sha256"],
            "lemmas": evaluate_profile(totals, minima),
        })

    terminal = json.loads(terminal_profile_path.read_text())
    terminal_audit = evaluate_profile(
        load_rows(terminal, "profile_totals"),
        load_rows(terminal, "profile_minima"),
    )
    names = tuple(LEMMAS)
    summary = {}
    for name in names:
        summary[name] = {
            "applicable_count": sum(row["lemmas"][name]["applicable"] for row in rows),
            "verified_count": sum(row["lemmas"][name]["verified"] for row in rows),
            "failed_count": sum(
                row["lemmas"][name]["applicable"]
                and not row["lemmas"][name]["verified"]
                for row in rows
            ),
        }
    either_count = sum(
        any(row["lemmas"][name]["verified"] for name in names)
        for row in rows
    )
    result = {
        "schema": "fixed-u-split-switching-anchor-ledger-census-v1",
        "status": "COMPLETE_RETAINED_PROFILE_CENSUS",
        "ledger": str(ledger_path),
        "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        "retained_profile_count": len(rows),
        "summary": summary,
        "either_anchor_lemma_verified_count": either_count,
        "terminal_profile": str(terminal_profile_path),
        "terminal_profile_sha256": hashlib.sha256(
            terminal_profile_path.read_bytes()
        ).hexdigest(),
        "terminal_profile_lemmas": terminal_audit,
        "profiles": rows,
        "premise_implication_boundary": (
            "Every ledger round is an exact admissible profile returned by the "
            "declared form-2 chart master. Any applicable negative anchor margin "
            "therefore proves that the numerical anchor inequalities do not follow "
            "from those declared chart premises alone. This census does not assert "
            "that each retained round satisfies any stronger, unencoded GG premise."
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
    args = parser.parse_args()
    result = run(args.ledger, args.terminal_profile, args.output)
    print(json.dumps({
        "status": result["status"],
        "retained_profile_count": result["retained_profile_count"],
        "summary": result["summary"],
        "either_anchor_lemma_verified_count": result["either_anchor_lemma_verified_count"],
        "terminal_profile_lemmas": result["terminal_profile_lemmas"],
    }, indent=2))


if __name__ == "__main__":
    main()
