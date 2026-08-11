#!/usr/bin/env python3
"""Audit own-capture and lex-sacrifice response-compression inequalities."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    own, captured, external, residual = z3.Reals(
        "own captured external residual"
    )
    capture = z3.SolverFor("QF_LRA")
    capture.add(
        own > 0,
        captured >= 0,
        external >= 0,
        residual == own - captured + external,
        residual < own,
        captured <= external,
    )
    capture_status = str(capture.check())
    assert capture_status == "unsat"

    loss, threshold = z3.Reals("loss threshold")
    band = z3.SolverFor("QF_LRA")
    band.add(
        own > 0,
        loss > 0,
        threshold <= own,
        own - loss < threshold,
        z3.Or(threshold <= own - loss, threshold > own),
    )
    band_status = str(band.check())
    assert band_status == "unsat"

    improved, base, safe_threshold = z3.Reals(
        "improved base safe_threshold"
    )
    other_observer = z3.SolverFor("QF_LRA")
    other_observer.add(
        improved >= base,
        base >= safe_threshold,
        improved < safe_threshold,
    )
    other_status = str(other_observer.check())
    assert other_status == "unsat"

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "lex-sacrificed-response-compression-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {"claim": "unpaid_residual_is_own_packet_capture", "status": capture_status},
            {"claim": "sacrificed_owner_core_walls_lie_in_loss_band", "status": band_status},
            {"claim": "improving_observers_remain_safe_against_common_safe_cores", "status": other_status},
        ],
        "claim_boundary": (
            "QF_LRA audit of the capture identity and wall localization; "
            "lexicographic priority and the exhaustive target classification "
            "are analytic"
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
