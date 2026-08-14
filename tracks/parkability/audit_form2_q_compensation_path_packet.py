#!/usr/bin/env python3
"""Audit the form-2 q-compensation path-packet frontier."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def scalar_checks():
    delta_q, c_q, p_q = z3.Reals("delta_q c_q p_q")
    alpha = c_q - delta_q
    q_paid = z3.SolverFor("QF_LRA")
    q_paid.add(p_q >= alpha, z3.Not(delta_q - c_q + p_q >= 0))
    q_status = str(q_paid.check())
    assert q_status == "unsat"

    delta_r, singleton_r, p_r = z3.Reals("delta_r singleton_r p_r")
    beta = delta_r + singleton_r
    root_paid = z3.SolverFor("QF_LRA")
    root_paid.add(singleton_r > 0, p_r <= beta,
                  z3.Not(delta_r + singleton_r - p_r >= 0))
    root_status = str(root_paid.check())
    assert root_status == "unsat"

    d_core, d_base, d_residual = z3.Reals("d_core d_base d_residual")
    d_paid = z3.SolverFor("QF_LRA")
    d_paid.add(d_core > d_base, d_residual >= 0,
               z3.Not(d_residual + d_core > d_base))
    d_status = str(d_paid.check())
    assert d_status == "unsat"
    return {
        "q_payment_threshold": q_status,
        "root_payment_threshold": root_status,
        "ordinary_d_core_payment": d_status,
    }


def subset_checks():
    checked = 0
    for n in range(1, 6):
        universe = tuple(range(n))
        for weights in itertools.product(range(1, 4), repeat=n):
            total = sum(weights)
            for alpha in range(1, total + 1):
                feasible = [
                    set(row)
                    for size in range(1, n + 1)
                    for row in itertools.combinations(universe, size)
                    if sum(weights[g] for g in row) >= alpha
                ]
                if not feasible:
                    continue
                minimal = min(feasible, key=len)
                assert all(
                    sum(weights[h] for h in minimal if h != g) < alpha
                    for g in minimal
                )
                checked += 1
    return checked


def support_checks():
    initial = {
        "r": {"R", "P"},
        "q": {"Q", "Cd"},
        "d": {"D"},
        "s": {"S"},
        "charity": {"p"},
    }
    final = {
        "r": {"R", "p"},
        "q": {"Q", "P"},
        "d": {"D", "Cd"},
        "s": {"S"},
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
    expected = {("charity", "r"), ("r", "q"), ("q", "d")}
    assert edges == expected
    return sorted(map(list, edges))


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results" / "FORM2_Q_COMPENSATION_PATH_PACKET_FRONTIER_20260814.md"
    return {
        "schema": "form2-q-compensation-path-packet-v1",
        "status": "PAID_THREE_EDGE_PATH_OR_BICRITERIA_PACKET",
        "scalar_checks": scalar_checks(),
        "minimal_packet_calibrations_checked": subset_checks(),
        "support_edges": support_checks(),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "cap-free path identities; q-feasible packet existence, observer "
            "continuation, and critical-packet elimination remain open"
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
        "status": result["status"],
        "minimal_packet_calibrations_checked": result[
            "minimal_packet_calibrations_checked"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
