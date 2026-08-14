#!/usr/bin/env python3
"""Exact symbolic audit of the first T_{L,times} packet-charge gate.

This is not a valuation-cell search and does not claim a GG counterexample.
It proves the packet accounting identities and gives exact QF_LRA
countermodels to invalid cross-row implications.
"""

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


def exact_number(value: z3.RatNumRef) -> str:
    return str(value)


def fixed_model(equal: bool) -> dict[str, str]:
    fs, b, ks, a, mu, deficit = z3.Reals("fs b ks a mu deficit")
    fh, hh, kh, yh, slack, jmax = z3.Reals("fh hh kh yh slack jmax")
    solver = z3.SolverFor("QF_LRA")
    if equal:
        solver.add(fs == 10, b == 8, ks == 2, a == 10, mu == 0, deficit == 2)
    else:
        solver.add(fs == 10, b == 9, ks == 3, a == 12, mu == 2, deficit == 1)
    solver.add(
        a == b + ks,
        mu == a - fs,
        deficit == fs - b,
        fh == 10,
        hh == 1,
        kh == 9,
        yh == hh + kh,
        slack == yh - fh,
        jmax == 2,
        kh - slack > 0,
        jmax < kh - slack,
    )
    assert solver.check() == z3.sat
    model = solver.model()
    variables = (fs, b, ks, a, mu, deficit, fh, hh, kh, yh, slack, jmax)
    return {str(variable): exact_number(model.eval(variable)) for variable in variables}


def run(repo: Path) -> dict:
    a, b, k, floor, mu, deficit = z3.Reals("a b k floor mu deficit")
    accounting = [a == b + k, mu == a - floor, deficit == floor - b]
    capture_identity = prove(accounting, k == mu + deficit)
    assert capture_identity

    holder_floor, holder_rest, holder_k, holder_total, slack, compensation = z3.Reals(
        "holder_floor holder_rest holder_k holder_total slack compensation"
    )
    holder = [
        holder_total == holder_rest + holder_k,
        slack == holder_total - holder_floor,
    ]
    holder_payment_identity = prove(
        holder,
        (holder_rest + compensation >= holder_floor)
        == (compensation >= holder_k - slack),
    )
    assert holder_payment_identity

    strict = fixed_model(equal=False)
    equality = fixed_model(equal=True)

    # The root-surplus loss band is compatible with strict recipient capture
    # because the two statements live in independent valuation rows.
    root_x, root_delta, root_h, root_d, root_c = z3.Reals(
        "root_x root_delta root_h root_d root_c"
    )
    root_band_solver = z3.SolverFor("QF_LRA")
    root_band_solver.add(
        root_x == 10,
        root_delta == 4,
        root_h == root_x + root_delta,
        root_d == 5,
        root_c == root_h - root_d,
        root_delta <= root_d,
        root_d <= root_x,
        root_c <= root_x,
    )
    assert root_band_solver.check() == z3.sat
    root_band_model = root_band_solver.model()

    # The mixed old/new response separator is feasible over positive exact
    # rationals: base-paid does not imply payment of a current-safe target.
    base, current, old_core, decorated_threshold = z3.Reals(
        "base current old_core decorated_threshold"
    )
    mixed_solver = z3.SolverFor("QF_LRA")
    mixed_solver.add(
        base == 10,
        current == 13,
        old_core == 11,
        decorated_threshold == 12,
        old_core >= base,
        old_core < decorated_threshold,
        decorated_threshold <= current,
    )
    assert mixed_solver.check() == z3.sat
    mixed_model = mixed_solver.model()

    # A desired-edge cycle is not release compatible when one selected packet
    # is supplied by an owner outside the selected owner component.
    selected_component = {0, 1, 2}
    packet_suppliers = {0: 3, 1: 0, 2: 1}
    outside_suppliers = sorted(set(packet_suppliers.values()) - selected_component)
    assert outside_suppliers == [3]

    contract = repo / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "retired-packet-charge-anchor-gate-audit-v1",
        "status": "RECIPIENT_CAPTURE_DOES_NOT_PAY_HOLDER_GATE_OPEN",
        "capture_identity": capture_identity,
        "holder_payment_identity": holder_payment_identity,
        "strict_capture_cross_row_countermodel": strict,
        "equality_critical_cross_row_countermodel": equality,
        "indivisible_whole_packet_deadlock": {
            "packet_atoms": 1,
            "recipient_requires_packet": True,
            "holder_return_pool_underpays": True,
            "values": strict,
        },
        "root_band_cross_row_countermodel": {
            "x": exact_number(root_band_model.eval(root_x)),
            "delta": exact_number(root_band_model.eval(root_delta)),
            "root_target": exact_number(root_band_model.eval(root_h)),
            "response": exact_number(root_band_model.eval(root_d)),
            "complement": exact_number(root_band_model.eval(root_c)),
            "coexists_with_strict_recipient_capture": True,
        },
        "base_floor_debt_countermodel": {
            "base": exact_number(mixed_model.eval(base)),
            "current": exact_number(mixed_model.eval(current)),
            "old_core": exact_number(mixed_model.eval(old_core)),
            "decorated_threshold": exact_number(mixed_model.eval(decorated_threshold)),
        },
        "release_closure_countermodel": {
            "selected_component": sorted(selected_component),
            "packet_suppliers": {str(k): v for k, v in packet_suppliers.items()},
            "outside_suppliers": outside_suppliers,
        },
        "full_T_L_times_theorem_refuted": False,
        "smallest_unproved_gate": (
            "holder compensation from a physically releasable packet, or a "
            "separately valid root/anchor operation"
        ),
        "claim_boundary": (
            "exact symbolic no-go for recipient-row charging, base-floor "
            "promotion, root-band reversal, and unsupplied cycles; not a globally maximal GG "
            "counterexample"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
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
        "full_theorem_refuted": result["full_T_L_times_theorem_refuted"],
        "smallest_unproved_gate": result["smallest_unproved_gate"],
    }, indent=2))


if __name__ == "__main__":
    main()
