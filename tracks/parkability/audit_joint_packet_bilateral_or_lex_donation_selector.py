#!/usr/bin/env python3
"""QF_LRA checks for the joint-packet bilateral selector."""

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
    r_base, r_packet, r_exchange, r_new = z3.Reals(
        "r_base r_packet r_exchange r_new"
    )
    q_base, q_packet, q_exchange, q_new = z3.Reals(
        "q_base q_packet q_exchange q_new"
    )
    q_max, q_any = z3.Reals("q_max q_any")
    positive = [
        r_base > 0,
        r_packet > 0,
        r_exchange >= 0,
        q_base > 0,
        q_packet > 0,
        q_exchange >= 0,
        q_max >= 0,
        q_any >= 0,
    ]
    records = [
        checked(
            "bilateral_exchange_strictly_improves_root",
            positive
            + [r_packet > r_exchange, r_new == r_base - r_exchange + r_packet, r_new <= r_base],
        ),
        checked(
            "paying_exchange_keeps_q_nonworse",
            positive
            + [q_exchange >= q_packet, q_new == q_base - q_packet + q_exchange, q_new < q_base],
        ),
        checked(
            "maximum_failure_propagates_to_every_affordable_packet",
            positive + [q_max >= q_any, q_max < q_packet, q_any >= q_packet],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/JOINT_PACKET_BILATERAL_OR_LEX_DONATION_SELECTOR_LEMMA_20260811.md"
    return {
        "schema": "joint-packet-bilateral-or-lex-donation-selector-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of bilateral owner payment and extremal failure "
            "propagation; donor/external blocker termination is outside scope"
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
