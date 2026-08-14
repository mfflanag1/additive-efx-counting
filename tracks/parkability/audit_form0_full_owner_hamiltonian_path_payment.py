#!/usr/bin/env python3
"""Audit the cap-free form-0 Hamiltonian-path payment identities."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def scalar_checks():
    br, p, cq, xr = z3.Reals("br p cq xr")
    zroot = br - cq + p

    paid = z3.SolverFor("QF_LRA")
    paid.add(p > 0, cq <= br + p - xr, z3.Not(zroot >= xr))
    paid_status = str(paid.check())
    assert paid_status == "unsat"

    failed = z3.SolverFor("QF_LRA")
    failed.add(p > 0, zroot < xr, z3.Not(cq > br + p - xr))
    failed_status = str(failed.check())
    assert failed_status == "unsat"

    qcore, qbase, qres = z3.Reals("qcore qbase qres")
    downstream = z3.SolverFor("QF_LRA")
    downstream.add(qcore > qbase, qres >= 0, z3.Not(qcore + qres > qbase))
    downstream_status = str(downstream.check())
    assert downstream_status == "unsat"
    return {
        "root_payment_identity": paid_status,
        "root_failure_separator": failed_status,
        "desired_core_plus_residual_payment": downstream_status,
    }


def support_checks():
    # Packet labels, rather than their internal goods, are sufficient for the
    # cap-free conservation and edge identity.
    initial = {
        "r": {"R", "Cq"},
        "q": {"Q", "Cd"},
        "d": {"D", "Cs"},
        "s": {"S"},
        "charity": {"p"},
    }
    final = {
        "r": {"R", "p"},
        "q": {"Q", "Cq"},
        "d": {"D", "Cd"},
        "s": {"S", "Cs"},
        "charity": set(),
    }
    assert set().union(*initial.values()) == set().union(*final.values())
    assert sum(map(len, initial.values())) == sum(map(len, final.values()))
    supplier = {
        packet: owner for owner, packets in initial.items() for packet in packets
    }
    edges = {
        (supplier[packet], owner)
        for owner, packets in final.items()
        for packet in packets if supplier[packet] != owner
    }
    expected = {
        ("charity", "r"), ("r", "q"), ("q", "d"), ("d", "s")
    }
    assert edges == expected
    return sorted(map(list, edges))


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results" / "FORM0_FULL_OWNER_HAMILTONIAN_PATH_PAYMENT_LEMMA_20260814.md"
    return {
        "schema": "form0-full-owner-hamiltonian-path-payment-v1",
        "status": "PATH_PAYMENT_OR_EXACT_ROOT_SEPARATOR",
        "scalar_checks": scalar_checks(),
        "support_edges": support_checks(),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "cap-free identities; full-owner saturated composition remains "
            "conditional on complete signed-interface verification"
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
