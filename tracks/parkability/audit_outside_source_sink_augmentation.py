#!/usr/bin/env python3
"""Audit sink-augmentation capture and abstract release preservation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    sink_old, sink_target, desired, source_old = z3.Reals(
        "sink_old sink_target desired source_old"
    )
    capture = z3.SolverFor("QF_LRA")
    capture.add(
        sink_old > 0,
        sink_target > sink_old,
        desired > 0,
        source_old > 0,
        source_old + sink_target - desired <= sink_old,
        desired != source_old + sink_target - sink_old,
        desired <= source_old + sink_target - sink_old,
    )
    capture_status = str(capture.check())
    assert capture_status == "unsat"

    incoming = {
        "b": {"B_X", "B_I"},
        "a": {"Xb", "I_minus_B_I"},
    }
    released = {
        "b": {"Xb"},
        "a": {"O_a", "B_X"},
        "old_component": {"B_I", "I_minus_B_I"},
    }
    assert sum(map(len, incoming.values())) == len(set().union(*incoming.values()))
    assert set().union(*incoming.values()) <= set().union(*released.values())

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "outside-source-sink-augmentation-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {
                "claim": "failed_sink_payment_captures_source_plus_margin",
                "status": capture_status,
            }
        ],
        "support_record": {
            "incoming": {
                key: sorted(value) for key, value in incoming.items()
            },
            "released_or_previously_supplied": {
                key: sorted(value) for key, value in released.items()
            },
        },
        "claim_boundary": (
            "QF_LRA capture implication and abstract one-step support "
            "preservation; induction over a finite source chain is analytic"
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
