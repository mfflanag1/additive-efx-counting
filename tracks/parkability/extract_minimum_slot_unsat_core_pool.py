#!/usr/bin/env python3
"""Extract a portable minimum-slot CEGAR seed from tracked UNSAT labels."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_minimum_slot_orbit_cegar import (
        completion_cut_tracker,
        global_cut_tracker,
        orbit_cut_tracker,
    )
except ImportError:
    from anneal import atomic_json
    from run_minimum_slot_orbit_cegar import (
        completion_cut_tracker,
        global_cut_tracker,
        orbit_cut_tracker,
    )


SCHEMA = "minimum-slot-orbit-global-threshold-cegar-v1"


def run(source, output):
    document = json.loads(source.read_text())
    labels = set(document.get("unsat_core_labels") or ())
    if document.get("status") != "FIXED_PAIR_TOKEN_ORBIT_FORCED" or not labels:
        raise ValueError("source must be a tracked UNSAT CEGAR session")
    global_cuts = [
        record
        for record in document["global_cuts"]
        if global_cut_tracker(record) in labels
    ]
    completion_cuts = [
        record
        for record in document["completion_cuts"]
        if completion_cut_tracker(
            record["assignment"], record["host"], record["permutation"]
        )
        in labels
    ]
    orbit_hall_cuts = [
        record
        for record in document["orbit_hall_cuts"]
        if orbit_cut_tracker(record["assignment"]) in labels
    ]
    recovered = {
        *(global_cut_tracker(record) for record in global_cuts),
        *(
            completion_cut_tracker(
                record["assignment"], record["host"], record["permutation"]
            )
            for record in completion_cuts
        ),
        *(orbit_cut_tracker(record["assignment"]) for record in orbit_hall_cuts),
    }
    if recovered != labels:
        raise AssertionError("UNSAT labels do not match persisted cut records")
    result = {
        "schema": SCHEMA,
        "status": "EXTRACTED_UNSAT_CORE_POOL",
        "meaning": (
            "Raw Z3 UNSAT core over tracked global-maximality and all-blocked-"
            "orbit consequences, serialized as a portable CEGAR seed."
        ),
        "claim_boundary": (
            "The core retains the source session's exact fixed edge-cell hypotheses. "
            "It is not a pair-Hall-cell or general EFX theorem."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "total_iterations": int(document.get("total_iterations", 0)),
        "values": document.get("values"),
        "global_cut_count": len(global_cuts),
        "completion_cut_count": len(completion_cuts),
        "orbit_hall_cut_count": len(orbit_hall_cuts),
        "unsat_core_size": len(labels),
        "global_cuts": global_cuts,
        "completion_cuts": completion_cuts,
        "orbit_hall_cuts": orbit_hall_cuts,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "schema",
                    "status",
                    "unsat_core_size",
                    "global_cut_count",
                    "completion_cut_count",
                    "orbit_hall_cut_count",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
