#!/usr/bin/env python3
"""Audit root anchoring and aligned compression-star cancellation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    residual, core, response = z3.Reals("residual core response")
    aligned = z3.SolverFor("QF_LRA")
    aligned.add(
        residual > 0,
        core > 0,
        response > 0,
        core > residual,
        response <= residual,
        core <= response,
    )
    aligned_status = str(aligned.check())
    assert aligned_status == "unsat"

    new_residual = z3.Real("new_residual")
    gain = z3.SolverFor("QF_LRA")
    gain.add(
        new_residual == residual + core - response,
        core > residual,
        response <= residual,
        new_residual <= residual,
    )
    gain_status = str(gain.check())
    assert gain_status == "unsat"

    low_core, high_core = z3.Reals("low_core high_core")
    cross_order = z3.SolverFor("QF_LRA")
    cross_order.add(
        high_core > residual,
        response <= residual,
        response > low_core,
        z3.Or(high_core <= response, response <= low_core),
    )
    cross_status = str(cross_order.check())
    assert cross_status == "unsat"

    root_target = {"T_q", "f", "R_r"}
    root_core = {"T_q", "f"}
    assert root_core <= root_target

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "root-anchored-compression-star-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {"claim": "aligned_wall_core_exceeds_residual_response", "status": aligned_status},
            {"claim": "aligned_recapture_strictly_increases_residual", "status": gain_status},
            {"claim": "maximal_cross_star_has_strict_four_level_order", "status": cross_status},
        ],
        "support_record": {
            "root_target": sorted(root_target),
            "common_safe_desired_root_core": sorted(root_core),
            "root_is_response_source": True,
        },
        "claim_boundary": (
            "QF_LRA audit of aligned/cross-star scalar implications and exact "
            "root-core containment; response-source membership uses the analytic "
            "common-safe desired-core definition"
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
