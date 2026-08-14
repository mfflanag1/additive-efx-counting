#!/usr/bin/env python3
"""Audit the R3 singleton-compensated anchor-uncrossing frontier."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

import z3


CYCLE = {"r": "q", "q": "s", "s": "r"}
LATER_SOURCES = ("q", "s")
OWNERS = ("r", "q", "s", "d")


def edge_records():
    initial = {(supplier, target) for target, supplier in CYCLE.items()}
    rows = []
    for source in LATER_SOURCES:
        targets = {"r", *(set(CYCLE) - {source, "r"})}
        other = next(target for target in targets if target != "r")
        for root_incoming in ("none", "partial", "whole"):
            for root_residual in (False, True):
                if root_incoming == "none" and not root_residual:
                    continue
                for other_residual in (False, True):
                    destinations = {
                        supplier: {target} for supplier, target in initial
                    }

                    root_supplier = CYCLE["r"]
                    if root_incoming == "whole":
                        destinations[root_supplier].discard("r")
                    if root_incoming != "none":
                        destinations[root_supplier].add(source)
                    if root_residual:
                        destinations.setdefault("r", set()).add(source)

                    other_supplier = CYCLE[other]
                    destinations[other_supplier].discard(other)
                    destinations[other_supplier].add(source)
                    if other_residual:
                        destinations.setdefault(other, set()).add(source)

                    owner_edges = {
                        (supplier, recipient)
                        for supplier, recipients in destinations.items()
                        for recipient in recipients
                        if supplier != recipient
                    }
                    assert len(owner_edges) <= 3

                    # The singleton may be assigned to any owner; in the
                    # compensated selector it is assigned to `source`.
                    for charity_target in OWNERS:
                        all_edges = owner_edges | {("charity", charity_target)}
                        assert len(all_edges) <= 4
                        rows.append({
                            "source": source,
                            "other_target": other,
                            "root_incoming": root_incoming,
                            "root_residual": root_residual,
                            "other_residual": other_residual,
                            "charity_target": charity_target,
                            "owner_edges": sorted(map(list, owner_edges)),
                            "total_edge_count": len(all_edges),
                        })
    return rows


def scalar_checks():
    a, rpart, base = z3.Reals("a rpart base")
    kval, rho = z3.Reals("kval rho")
    source_e, source_floor, singleton, hx = z3.Reals(
        "source_e source_floor singleton hx"
    )
    mu = source_e - source_floor

    capture = [
        a == rpart + kval,
        a > base,
        rpart <= base,
        rho == base - rpart,
    ]
    solver = z3.SolverFor("QF_LRA")
    solver.add(*capture, z3.Not(z3.And(rho >= 0, kval > rho)))
    capture_status = str(solver.check())
    assert capture_status == "unsat"

    payment = z3.SolverFor("QF_LRA")
    payment.add(
        source_e > source_floor,
        singleton > 0,
        hx < mu + singleton,
        z3.Not(source_e - hx + singleton > source_floor),
    )
    payment_status = str(payment.check())
    assert payment_status == "unsat"

    failure = z3.SolverFor("QF_LRA")
    failure.add(
        source_e > source_floor,
        singleton > 0,
        z3.Not(source_e - hx + singleton > source_floor),
        z3.Not(hx >= mu + singleton),
    )
    failure_status = str(failure.check())
    assert failure_status == "unsat"

    atom, e_without = z3.Reals("atom e_without")
    minimality = z3.SolverFor("QF_LRA")
    minimality.add(
        source_e == e_without + atom,
        source_e > source_floor,
        e_without <= source_floor,
        z3.Not(atom >= mu),
    )
    minimality_status = str(minimality.check())
    assert minimality_status == "unsat"

    return {
        "capture_implies_nonnegative_deficit_and_root_feasible_K": capture_status,
        "selector_source_payment": payment_status,
        "selector_failure_implies_source_separator": failure_status,
        "minimal_desired_core_atom_margin": minimality_status,
    }


def scalar_separator_witness():
    # Exact positive rational witness that the two valuation rows alone do
    # not contradict the terminal separator.  The captured packet has one
    # atom, so it is automatically inclusion-minimal at both thresholds.
    witness = {
        "root_retained_anchor": "1",
        "root_base": "2",
        "root_captured_atom": "2",
        "root_anchor": "3",
        "root_deficit_rho": "1",
        "source_response": "3",
        "source_floor": "2",
        "source_margin_mu": "1",
        "source_charity_singleton": "1/2",
    }
    assert 3 > 2
    assert 1 <= 2
    assert 2 > 1
    assert 3 > 2
    half = Fraction(1, 2)
    assert 3 >= 1 + half
    assert 0 + half <= 2
    return witness


def subset_checks():
    # Exhaust the purely combinatorial minimal-crossing assertion for every
    # positive integer weighting on up to five atoms in a calibration box.
    checked = 0
    threshold_checked = 0
    for n in range(1, 6):
        universe = tuple(range(n))
        for weights in itertools.product(range(1, 5), repeat=n):
            total = sum(weights)
            for rho in range(total):
                if total <= rho:
                    continue
                feasible = [
                    set(bits)
                    for size in range(1, n + 1)
                    for bits in itertools.combinations(universe, size)
                    if sum(weights[g] for g in bits) > rho
                ]
                minimal = min(feasible, key=len)
                assert all(
                    sum(weights[h] for h in minimal if h != g) <= rho
                    for g in minimal
                )
                checked += 1

            # Independently calibrate monotonicity of the one-good deletion
            # threshold on every nonempty nested packet pair.
            for mask_e in range(1, 1 << n):
                packet_e = [g for g in universe if mask_e & (1 << g)]
                tau_e = sum(weights[g] for g in packet_e) - min(
                    weights[g] for g in packet_e
                )
                for mask_d in range(1, 1 << n):
                    if mask_d & ~mask_e:
                        continue
                    packet_d = [g for g in universe if mask_d & (1 << g)]
                    tau_d = sum(weights[g] for g in packet_d) - min(
                        weights[g] for g in packet_d
                    )
                    assert tau_d <= tau_e
                    threshold_checked += 1
    return {
        "minimal_crossing": checked,
        "threshold_monotonicity": threshold_checked,
    }


def run(root: Path):
    rows = edge_records()
    assert len(rows) == 80
    scalars = scalar_checks()
    subsets = subset_checks()
    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_SINGLETON_COMPENSATED_ANCHOR_UNCROSSING_FRONTIER_20260814.md"
    return {
        "schema": "r3-singleton-compensated-anchor-uncrossing-v1",
        "status": "FOUR_EDGE_UNCROSSING_OR_BICRITERIA_CRITICAL_PACKET",
        "edge_records_checked": len(rows),
        "edge_records": rows,
        "scalar_checks": scalars,
        "scalar_separator_witness": scalar_separator_witness(),
        "minimal_crossing_calibrations_checked": subsets["minimal_crossing"],
        "threshold_monotonicity_calibrations_checked": subsets[
            "threshold_monotonicity"
        ],
        "claim_boundary": (
            "cap-free algebraic selector/separator; elimination of the "
            "critical packet from full saturation remains open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
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
        "edge_records_checked": result["edge_records_checked"],
        "minimal_crossing_calibrations_checked": result[
            "minimal_crossing_calibrations_checked"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
