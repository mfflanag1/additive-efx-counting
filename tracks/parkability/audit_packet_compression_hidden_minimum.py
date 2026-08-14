#!/usr/bin/env python3
"""Exact audit of the packet-compression hidden-minimum dichotomy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def audit_arity(arity: int) -> dict:
    totals = [z3.Real(f"block_{arity}_{index}") for index in range(arity)]
    physical_min = z3.Real(f"physical_min_{arity}")
    threshold = z3.Real(f"threshold_{arity}")
    union_total = z3.Sum(*totals)
    compressed_min = totals[0]
    for amount in totals[1:]:
        compressed_min = z3.If(amount < compressed_min, amount, compressed_min)

    premises = [
        threshold >= 0,
        physical_min > 0,
        *(amount > 0 for amount in totals),
        *(physical_min <= amount for amount in totals),
        union_total - compressed_min <= threshold,
        union_total - physical_min > threshold,
    ]

    strict_solver = z3.Solver()
    strict_solver.add(*premises, physical_min >= compressed_min)

    singleton_solver = z3.Solver()
    singleton_index = z3.Int(f"singleton_index_{arity}")
    singleton_solver.add(*premises, singleton_index >= 0, singleton_index < arity)
    singleton_solver.add(z3.Or(*(
        z3.And(singleton_index == index, physical_min == amount)
        for index, amount in enumerate(totals)
    )))

    margin_solver = z3.Solver()
    margin_solver.add(
        *premises,
        z3.Or(
            physical_min >= union_total - threshold,
            union_total - threshold > compressed_min,
        ),
    )

    return {
        "arity": arity,
        "hidden_minimum_strictly_below_every_compressed_atom": str(strict_solver.check()),
        "hidden_minimum_cannot_be_singleton_atom": str(singleton_solver.check()),
        "margin_chain": str(margin_solver.check()),
    }


def run(output: Path) -> dict:
    checks = [audit_arity(arity) for arity in range(1, 13)]
    assert all(
        row[key] == "unsat"
        for row in checks
        for key in (
            "hidden_minimum_strictly_below_every_compressed_atom",
            "hidden_minimum_cannot_be_singleton_atom",
            "margin_chain",
        )
    )
    result = {
        "schema": "packet-compression-hidden-minimum-audit-v1",
        "status": "HIDDEN_MINIMUM_DICHOTOMY_VERIFIED",
        "arities_checked": [row["arity"] for row in checks],
        "checks": checks,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Cap-free algebraic implication for any finite packet partition; "
            "it reduces failure of physical EFX-tail safety after compressed "
            "safety to a proper hidden-minimum split, but does not itself "
            "convert that split into PI or a complete EFX allocation."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> None:
    output = ROOT / "results" / "packet_compression_hidden_minimum_audit.json"
    print(json.dumps(run(output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
