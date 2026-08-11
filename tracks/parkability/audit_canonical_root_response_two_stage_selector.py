#!/usr/bin/env python3
"""QF_LRA checks for the canonical two-stage root-response selector."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name: str, constraints) -> dict:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def run(root: Path) -> dict:
    q_min, q_any, threshold = z3.Reals("q_min q_any threshold")
    r_max, r_any, xr = z3.Reals("r_max r_any xr")
    kq, omitted_q, floater_q = z3.Reals("kq omitted_q floater_q")
    kr, floater_r, margin_r = z3.Reals("kr floater_r margin_r")
    positive = [
        q_min > 0,
        q_any > 0,
        threshold > 0,
        r_max > 0,
        r_any > 0,
        xr > 0,
        kq > 0,
        omitted_q >= 0,
        floater_q > 0,
        kr > 0,
        floater_r > 0,
        margin_r > 0,
    ]
    records = [
        checked(
            "minimum_failure_propagates_to_every_root_response",
            positive + [q_min <= q_any, q_min >= threshold, q_any < threshold],
        ),
        checked(
            "maximum_failure_propagates_to_every_floater_substitution",
            positive + [r_max >= r_any, r_max < xr, r_any >= xr],
        ),
        checked(
            "selected_q_packet_capture",
            positive + [kq > omitted_q + floater_q, kq <= omitted_q + floater_q],
        ),
        checked(
            "selected_root_packet_capture",
            positive + [kr > floater_r + margin_r, kr <= floater_r + margin_r],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/CANONICAL_ROOT_RESPONSE_TWO_STAGE_SELECTOR_LEMMA_20260811.md"
    return {
        "schema": "canonical-root-response-two-stage-selector-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of the two extremal-selection implications and selected "
            "joint capture; joint-packet termination is outside scope"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
