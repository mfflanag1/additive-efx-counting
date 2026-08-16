#!/usr/bin/env python3
"""Augment a cyclic pair-Hall CEGAR pool from an exact audited SAT model."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


TOKENS = (1, 3, 5, 7, 8)


def run(pool_path, audit_path, values_path, output_path, all_orbit_cuts=False):
    pool = json.loads(pool_path.read_text())
    audit = json.loads(audit_path.read_text())
    values_document = json.loads(values_path.read_text())
    if audit.get("status") != "FINITE_POOL_SAT_REPLAYED":
        raise ValueError("SAT model must pass the exact finite-pool audit")

    orbit_witness = audit["full_orbit_audit"]["best_orbit_state"]
    if not orbit_witness["completing"]:
        raise ValueError("audited model has no completing orbit witness")
    assignment = tuple(int(good) for good in orbit_witness["assignment"])
    orbit_keys = {
        tuple(int(good) for good in record["assignment"])
        for record in pool["orbit_hall_cuts"]
    }
    if assignment not in orbit_keys:
        pool["orbit_hall_cuts"].append({"assignment": list(assignment)})
    if all_orbit_cuts:
        pool["orbit_hall_cuts"] = [
            {"assignment": list(assignment)}
            for assignment in itertools.permutations(TOKENS)
        ]

    higher = audit["full_global_audit"]["nearest_higher_state"]
    if higher is None:
        raise ValueError("audited model has no higher global witness")
    global_key = (int(higher["floater"]), tuple(int(mask) for mask in higher["masks"]))
    global_keys = {
        (int(record["floater"]), tuple(int(mask) for mask in record["masks"]))
        for record in pool["global_cuts"]
    }
    if global_key not in global_keys:
        pool["global_cuts"].append(
            {
                "floater": global_key[0],
                "masks": list(global_key[1]),
                "owner_distance": int(higher["owner_distance"]),
                "threshold_gain_numerator": int(higher["threshold_gain_numerator"]),
                "threshold_gain_denominator": int(higher["threshold_gain_denominator"]),
                "hall_insertable": bool(higher["hall_insertable"]),
                "best_hall_margin": str(higher["best_hall_margin"]),
            }
        )

    pool.update(
        {
            "status": "AUGMENTED_CEGAR_SEED",
            "meaning": (
                "Persisted pair-Hall cut pool augmented by the exact completing "
                "orbit witness and higher global witness from one audited SAT model"
                + (" and all 120 token-orbit blockers." if all_orbit_cuts else ".")
            ),
            "claim_boundary": (
                "This is a resumable cut pool, not a theorem or counterexample."
            ),
            "source_pool": str(pool_path),
            "source_pool_sha256": sha256(pool_path),
            "source_audit": str(audit_path),
            "source_audit_sha256": sha256(audit_path),
            "values": values_document.get("values", values_document),
            "global_cut_count": len(pool["global_cuts"]),
            "orbit_hall_cut_count": len(pool["orbit_hall_cuts"]),
            "all_orbit_cuts_preloaded": all_orbit_cuts,
        }
    )
    atomic_json(output_path, pool)
    return pool


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--values", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--all-orbit-cuts", action="store_true")
    args = parser.parse_args()
    result = run(
        args.pool,
        args.audit,
        args.values,
        args.output,
        args.all_orbit_cuts,
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "global_cut_count": result["global_cut_count"],
                "orbit_hall_cut_count": result["orbit_hall_cut_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
