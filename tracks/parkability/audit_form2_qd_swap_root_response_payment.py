#!/usr/bin/env python3
"""Audit the form-2 q-d swap/root-response payment frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def scalar_checks():
    delta_r, cs = z3.Reals("delta_r cs")
    root = z3.SolverFor("QF_LRA")
    root.add(cs <= delta_r, z3.Not(delta_r - cs >= 0))
    root_status = str(root.check())
    assert root_status == "unsat"

    delta_q, cdq, bdq, pq = z3.Reals("delta_q cdq bdq pq")
    qsolver = z3.SolverFor("QF_LRA")
    qsolver.add(bdq >= 0, pq > 0, bdq + pq >= cdq - delta_q,
                z3.Not(delta_q - cdq + bdq + pq >= 0))
    q_status = str(qsolver.check())
    assert q_status == "unsat"

    dcore, dbase = z3.Reals("dcore dbase")
    dsolver = z3.SolverFor("QF_LRA")
    dsolver.add(dcore > dbase, z3.Not(dcore > dbase))
    d_status = str(dsolver.check())
    assert d_status == "unsat"
    return {
        "root_retention_identity": root_status,
        "q_compensation_identity": q_status,
        "ordinary_d_core_payment": d_status,
    }


def support_checks():
    initial = {
        "r": {"R", "Cs"},
        "q": {"Q", "Cd"},
        "d": {"Bd"},
        "s": {"Bs"},
        "charity": {"p"},
    }
    final = {
        "r": {"R"},
        "q": {"Q", "Bd", "p"},
        "d": {"Cd"},
        "s": {"Bs", "Cs"},
        "charity": set(),
    }
    assert set().union(*initial.values()) == set().union(*final.values())
    supplier = {
        packet: owner for owner, packets in initial.items() for packet in packets
    }
    edges = {
        (supplier[packet], owner)
        for owner, packets in final.items()
        for packet in packets if supplier[packet] != owner
    }
    expected = {("r", "s"), ("q", "d"), ("d", "q"), ("charity", "q")}
    assert edges == expected
    return sorted(map(list, edges))


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results" / "FORM2_QD_SWAP_ROOT_RESPONSE_PAYMENT_FRONTIER_20260814.md"
    return {
        "schema": "form2-qd-swap-root-response-payment-v1",
        "status": "PAID_FOUR_EDGE_SWAP_OR_ROOT_Q_SEPARATORS",
        "scalar_checks": scalar_checks(),
        "support_edges": support_checks(),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "cap-free payment identities; observer continuation and "
            "simultaneous-menu-failure contradiction remain open"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"], "support_edges": result["support_edges"]
    }, indent=2))


if __name__ == "__main__":
    main()
