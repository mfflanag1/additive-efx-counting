#!/usr/bin/env python3
"""Audit the form-2 root-star disjoint/double-capture frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def scalar_checks():
    whole, outside, floor = z3.Reals("whole outside floor")
    overlap = whole - outside
    margin = whole - floor
    capture = z3.SolverFor("QF_LRA")
    capture.add(whole > floor, outside <= floor, z3.Not(overlap >= margin))
    capture_status = str(capture.check())
    assert capture_status == "unsat"

    delta_d, dcore = z3.Reals("delta_d dcore")
    d_payment = z3.SolverFor("QF_LRA")
    d_payment.add(z3.Not((delta_d + dcore >= 0) == (delta_d >= -dcore)))
    d_payment_status = str(d_payment.check())
    assert d_payment_status == "unsat"

    delta_r, singleton, union = z3.Reals("delta_r singleton union")
    root_payment = z3.SolverFor("QF_LRA")
    root_payment.add(
        singleton > 0,
        z3.Not(
            (delta_r + singleton - union >= 0)
            == (union <= delta_r + singleton)
        ),
    )
    root_payment_status = str(root_payment.check())
    assert root_payment_status == "unsat"
    return {
        "single_margin_capture_schema": capture_status,
        "d_payment_identity": d_payment_status,
        "root_payment_identity": root_payment_status,
    }


def support_checks():
    initial = {
        "r": {"R", "D", "S"},
        "d": {"Bd"},
        "s": {"Bs"},
        "q": {"Bq"},
        "charity": {"p"},
    }
    final = {
        "r": {"R", "p"},
        "d": {"Bd", "D"},
        "s": {"Bs", "S"},
        "q": {"Bq"},
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
    expected = {("charity", "r"), ("r", "d"), ("r", "s")}
    assert edges == expected
    priority_final = {
        "r": {"R", "S", "p"},
        "d": {"Bd", "D"},
        "s": {"Bs"},
        "q": {"Bq"},
        "charity": set(),
    }
    assert set().union(*initial.values()) == set().union(*priority_final.values())
    priority_edges = {
        (supplier[packet], owner)
        for owner, packets in priority_final.items()
        for packet in packets if supplier[packet] != owner
    }
    assert priority_edges == {("charity", "r"), ("r", "d")}
    return {
        "disjoint_star": sorted(map(list, edges)),
        "priority_assignment": sorted(map(list, priority_edges)),
    }


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results" / "FORM2_ROOT_STAR_DISJOINT_OR_DOUBLE_CAPTURE_FRONTIER_20260814.md"
    return {
        "schema": "form2-root-star-disjoint-double-capture-v1",
        "status": "DISJOINT_ROOT_STAR_OR_DOUBLE_MARGIN_CAPTURE",
        "scalar_checks": scalar_checks(),
        "support_edges": support_checks(),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "cap-free frontier; current-only d payment, observer safety, and "
            "double-capture reversal remain open"
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
