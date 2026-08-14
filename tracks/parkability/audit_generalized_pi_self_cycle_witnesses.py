#!/usr/bin/env python3
"""Independent exact audit of generalized BCFF self-PI witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
BASE = {
    "r": ("a0", "m"),
    "q": ("q0", "a1"),
    "d": ("h", "k", "gq"),
    "s": ("e", "p"),
    "charity": ("j", "l", "gr"),
}


def total(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction())


def tail(values, observer, goods):
    entries = [values[observer][good] for good in goods]
    return sum(entries, Fraction()) - min(entries, default=Fraction())


def audit_pair(source: Path, witness_path: Path):
    source_payload = json.loads(source.read_text())
    witness_payload = json.loads(witness_path.read_text())
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in source_payload["values"].items()
    }
    witness = witness_payload["witness"]
    edge = witness["edges"][0]
    owner = edge["source"]
    desired = set(edge["desired_core"])
    incoming = set(edge["incoming"])
    released = set(edge["released"])
    target = set(BASE[owner])
    charity = set(BASE["charity"])
    checks = {
        "search_reports_single_self_cycle": (
            witness_payload["status"] == "GENERALIZED_PI_CYCLE_FOUND"
            and witness["cycle"] == [owner]
            and edge["target"] == owner
        ),
        "incoming_is_exact_external_part": incoming == desired - target,
        "released_is_exact_target_complement": released == target - desired,
        "incoming_is_nonempty_base_charity": bool(incoming) and incoming <= charity,
        "desired_is_offered_bundle": desired == (target - released) | incoming,
        "source_strictly_desires_core": total(values, owner, desired) > 1,
        "core_is_common_safe": all(
            tail(values, observer, desired) <= 1 for observer in OWNERS
        ),
    }
    return {
        "source": f"results/{source.name}",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "witness_source": f"results/{witness_path.name}",
        "witness_source_sha256": hashlib.sha256(witness_path.read_bytes()).hexdigest(),
        "owner": owner,
        "incoming": sorted(incoming),
        "released": sorted(released),
        "desired_core": sorted(desired),
        "checks": checks,
        "valid_generalized_self_pi": all(checks.values()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--witness", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.source) != len(args.witness):
        raise ValueError("source/witness counts differ")
    records = [
        audit_pair(source, witness)
        for source, witness in zip(args.source, args.witness, strict=True)
    ]
    result = {
        "schema": "generalized-pi-self-cycle-witness-audit-v1",
        "status": (
            "ALL_STRENGTHENED_COUNTERPROFILES_EXCLUDED_BY_GENERALIZED_SELF_PI"
            if all(record["valid_generalized_self_pi"] for record in records)
            else "AUDIT_FAILED"
        ),
        "records": records,
        "claim_boundary": (
            "exact generalized BCFF one-edge PI certificates for the displayed "
            "bounded selector counterprofiles. This excludes those profiles from "
            "the saturated PI-free domain; it does not prove selector universality."
        ),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "owners": [record["owner"] for record in records],
    }, indent=2))


if __name__ == "__main__":
    main()
