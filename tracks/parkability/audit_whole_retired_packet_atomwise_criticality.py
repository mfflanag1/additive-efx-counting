#!/usr/bin/env python3
"""Exact QF_LRA audit of whole retired-packet atomwise criticality."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    a, b, k, floor, mu, deficit, good, reduced = z3.Reals(
        "a b k floor mu deficit good reduced"
    )
    base = [
        a == b + k,
        mu == a - floor,
        deficit == floor - b,
        reduced == b + k - good,
    ]
    deletion_identity = prove(base, reduced - floor == mu - good)
    proper_candidate = prove([*base, good < mu], reduced > floor)
    capture_identity = prove(base, k == mu + deficit)

    # Aggregate every good except one into `rest`.  If a nonsingleton packet
    # is atomwise critical, both the selected good and the nonempty rest carry
    # at least one margin.  This proves the key singleton corollary without a
    # fixed packet-size enumeration; the general multiplicity bound is the
    # same sum over all goods.
    rest = z3.Real("rest")
    nonsingleton_charge = prove(
        [k == good + rest, good >= mu, rest >= mu, k == mu + deficit],
        deficit >= mu,
    )
    singleton_if_margin_exceeds_deficit = prove(
        [
            k == good + rest,
            good >= mu,
            rest >= mu,
            k == mu + deficit,
            mu > deficit,
        ],
        z3.BoolVal(False),
    )
    assert all((deletion_identity, proper_candidate, capture_identity,
                nonsingleton_charge, singleton_if_margin_exceeds_deficit))

    results = repo / "results"
    theorem = results / "WHOLE_RETIRED_PACKET_ATOMWISE_CRITICALITY_LEMMA_20260813.md"
    contract = results / "RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "whole-retired-packet-atomwise-criticality-audit-v1",
        "status": "PROPER_PACKET_REDUCTION_OR_ATOMWISE_CRITICAL_SURVIVOR",
        "deletion_identity": deletion_identity,
        "proper_candidate_below_margin": proper_candidate,
        "capture_identity": capture_identity,
        "nonsingleton_implies_margin_at_most_deficit": nonsingleton_charge,
        "margin_above_deficit_forces_singleton": singleton_if_margin_exceeds_deficit,
        "general_charge": "(|K|-1)*mu <= d",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "exact strict-capture packet reduction and criticality charge; "
            "holder payment and atomwise-critical survivors remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "contract": str(contract.relative_to(repo)),
            "contract_sha256": sha256(contract),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "general_charge": result["general_charge"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()

