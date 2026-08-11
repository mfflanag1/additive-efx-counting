#!/usr/bin/env python3
"""Audit support and scalar claims for replacement complement return."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    base, core, floater, external, release = z3.Reals(
        "base core floater external release"
    )
    identities = [
        base > 0,
        core > 0,
        floater > 0,
        external > 0,
        release > 0,
        release == base - core,
    ]

    lower = z3.SolverFor("QF_LRA")
    lower.add(*identities, external + release < base, core <= external)
    lower_status = str(lower.check())

    interval = z3.SolverFor("QF_LRA")
    interval.add(
        *identities,
        external + release < base,
        core + floater < base,
        z3.Or(core <= external, core >= base - floater),
    )
    interval_status = str(interval.check())

    top, bottom = z3.Reals("top bottom")
    mutual = z3.SolverFor("QF_LRA")
    mutual.add(
        base > 0,
        floater > 0,
        top > 0,
        bottom > 0,
        core > 0,
        top + floater > base,
        top + bottom < core,
        core < base - floater,
    )
    mutual_status = str(mutual.check())

    reservoir = z3.SolverFor("QF_LRA")
    reservoir.add(
        base > 0,
        floater > 0,
        top > 0,
        core > 0,
        external > 0,
        top + floater > base,
        core < base - floater,
        top <= core - external,
    )
    reservoir_status = str(reservoir.check())
    assert (
        lower_status
        == interval_status
        == mutual_status
        == reservoir_status
        == "unsat"
    )

    incoming = {"q": {"f"}, "a": {"Oq"}}
    released = {"q": {"Oq"}, "a": set()}
    assert not (incoming["q"] & incoming["a"])
    assert set().union(*incoming.values()) <= {"f"}.union(*released.values())

    root_flip_incoming = {
        "a": {"K", "f"},
        "q": {"Xa", "P"},
        "r": {"H"},
    }
    root_flip_released = {
        "a": {"Xa"},
        "q": {"K", "H"},
        "r": {"P"},
    }
    assert sum(map(len, root_flip_incoming.values())) == len(
        set().union(*root_flip_incoming.values())
    )
    assert set().union(*root_flip_incoming.values()) <= {
        "f"
    }.union(*root_flip_released.values())

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "packet-replacement-complement-return-audit-v1",
        "status": "ALL_FORCED",
        "support_record": {
            "incoming": {key: sorted(value) for key, value in incoming.items()},
            "released": {key: sorted(value) for key, value in released.items()},
            "sources": {"q": "a", "a": "q"},
            "initially_unallocated": ["f"],
        },
        "root_flip_support_record": {
            "incoming": {
                key: sorted(value) for key, value in root_flip_incoming.items()
            },
            "released": {
                key: sorted(value) for key, value in root_flip_released.items()
            },
            "initially_unallocated": ["f"],
            "internal_response_permutations_supported": 6,
        },
        "scalar_records": [
            {
                "claim": "strict_complement_low_forces_core_above_external",
                "status": lower_status,
            },
            {
                "claim": "no_direct_source_and_complement_low_force_capture_interval",
                "status": interval_status,
            },
            {
                "claim": "mutual_owner_cannot_satisfy_capture_interval",
                "status": mutual_status,
            },
            {
                "claim": "mutual_top_strictly_covers_external_capture_deficit",
                "status": reservoir_status,
            },
        ],
        "claim_boundary": (
            "finite symbolic support plus QF_LRA capture implications; floater "
            "retention, nondegenerate strictness, and source growth are analytic"
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
