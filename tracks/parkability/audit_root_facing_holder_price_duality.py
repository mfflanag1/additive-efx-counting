#!/usr/bin/env python3
"""Exact QF_LRA audit of root-facing holder-price duality."""

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
    x, delta, d, c, compensation, new_root, price = z3.Reals(
        "x delta d c compensation new_root price"
    )
    base = [
        x > 0,
        delta > 0,
        d > 0,
        c > 0,
        c + d == x + delta,
        new_root == c + compensation,
        compensation >= 0,
    ]
    balance = prove(base, new_root - x == delta - d + compensation)
    weak_threshold = prove(base, (new_root >= x) == (compensation >= d - delta))
    strict_threshold = prove(base, (new_root > x) == (compensation > d - delta))
    band_price_identity = prove(
        [*base, d >= delta, price == d - delta],
        price == d - delta,
    )
    band_price_bounds = prove(
        [*base, d >= delta, d <= x, price == d - delta],
        z3.And(price >= 0, price <= x - delta),
    )
    assert all((balance, weak_threshold, strict_threshold,
                band_price_identity, band_price_bounds))

    results = repo / "results"
    theorem = results / "ROOT_FACING_HOLDER_PRICE_DUALITY_LEMMA_20260813.md"
    band = results / "ROOT_FACING_ANCHOR_SURPLUS_BAND_DICHOTOMY_20260813.md"
    contract = results / "RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-facing-holder-price-duality-audit-v1",
        "status": "ROOT_BAND_IDENTIFIED_WITH_BOUNDED_HOLDER_PRICE_SEPARATOR",
        "root_balance_identity": balance,
        "weak_compensation_threshold": weak_threshold,
        "strict_compensation_threshold": strict_threshold,
        "band_price_identity": band_price_identity,
        "band_price_bounds": band_price_bounds,
        "surviving_price": "0 <= pi_r(D) = v_r(D)-delta <= x-delta",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "exact root/holder price duality; existence of a physical paying "
            "packet and other observer debts remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "band_theorem": str(band.relative_to(repo)),
            "band_theorem_sha256": sha256(band),
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
        "surviving_price": result["surviving_price"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()

