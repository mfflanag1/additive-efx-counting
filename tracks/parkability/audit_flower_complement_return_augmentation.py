#!/usr/bin/env python3
"""Audit support and scalar claims for the flower complement return."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def support_records():
    incoming = {
        "r": {"Tq", "f"},
        "q": {"A_L"},
        "a": {"R", "L_minus_A", "Bq_minus_A"},
    }
    released = {
        "r": {"A_L", "L_minus_A", "R"},
        "q": {"Tq", "Bq_minus_A"},
        "a": set(),
    }
    selected = tuple(incoming.values())
    assert sum(map(len, selected)) == len(set().union(*selected))
    supply = {"f"}.union(*released.values())
    assert set().union(*selected) <= supply

    direct_incoming = {"r": incoming["r"], "q": incoming["q"]}
    direct_released = {"r": released["r"], "q": released["q"]}
    assert set().union(*direct_incoming.values()) <= {
        "f"
    }.union(*direct_released.values())
    return [
        {
            "case": "direct_q_source",
            "incoming": {key: sorted(value) for key, value in direct_incoming.items()},
            "released": {key: sorted(value) for key, value in direct_released.items()},
            "sources": {"r": "r", "q": "q"},
        },
        {
            "case": "complement_return",
            "incoming": {key: sorted(value) for key, value in incoming.items()},
            "released": {key: sorted(value) for key, value in released.items()},
            "sources": {"r": "r", "q": "a", "a": "q"},
        },
    ]


def scalar_records():
    base, reservoir, whole, selected, complement = z3.Reals(
        "base reservoir whole selected complement"
    )
    common = [
        base > 0,
        reservoir > 0,
        selected > 0,
        complement >= 0,
        whole == selected + complement,
        whole > base,
    ]

    capture = z3.SolverFor("QF_LRA")
    capture.add(*common)
    capture.add(reservoir + complement <= base)
    capture.add(
        z3.Or(
            complement > base - reservoir,
            selected < reservoir + (whole - base),
        )
    )

    deep = z3.SolverFor("QF_LRA")
    deep.add(*common)
    deep.add(reservoir + complement < base, selected < base)
    deep.add(reservoir >= base - (whole - base))
    return [
        {
            "claim": "complement_low_forces_capture",
            "status": str(capture.check()),
        },
        {
            "claim": "strict_capture_and_no_direct_q_source_force_deep_gap",
            "status": str(deep.check()),
        },
    ]


def run():
    records = scalar_records()
    assert {record["status"] for record in records} == {"unsat"}
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flower-complement-return-augmentation-audit-v1",
        "status": "ALL_FORCED",
        "support_records": support_records(),
        "scalar_records": records,
        "claim_boundary": (
            "finite symbolic support audit plus QF_LRA capture implications; "
            "most-envious-source existence and four-owner termination are analytic"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
