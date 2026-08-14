#!/usr/bin/env python3
"""Audit the form-2 six-branch payment compression."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


CYCLE_TRANSFER = {"R": ("q", "r"), "Q": ("s", "q"), "S": ("r", "s")}
D_TRANSFER = {"Dr": ("r", "d"), "Dq": ("q", "d")}
OMITTED_CORE = {"r": "R", "q": "Q", "s": "S"}
OUTGOING_CORE = {"r": "S", "q": "R", "s": "Q"}


def scalar_equivalence():
    s, dr, r_budget = z3.Reals("s dr r_budget")
    rcore, dq, q_budget = z3.Reals("rcore dq q_budget")
    qcore, s_budget = z3.Reals("qcore s_budget")
    nonnegative = [s >= 0, dr >= 0, rcore >= 0, dq >= 0, qcore >= 0]
    six_failures = z3.And(
        s > r_budget,
        s + dr > r_budget,
        rcore > q_budget,
        rcore + dq > q_budget,
        qcore > s_budget,
        qcore > s_budget,
    )
    compressed = z3.And(
        s > r_budget, rcore > q_budget, qcore > s_budget,
    )
    forward = z3.SolverFor("QF_LRA")
    forward.add(*nonnegative, six_failures, z3.Not(compressed))
    forward_status = str(forward.check())
    assert forward_status == "unsat"
    reverse = z3.SolverFor("QF_LRA")
    reverse.add(*nonnegative, compressed, z3.Not(six_failures))
    reverse_status = str(reverse.check())
    assert reverse_status == "unsat"
    return {
        "six_failures_imply_three_captures": forward_status,
        "three_captures_imply_six_failures": reverse_status,
    }


def branch_table():
    initial = {
        "r": {"r0", "S", "Dr"},
        "q": {"q0", "R", "Dq"},
        "s": {"s0", "Q"},
        "d": {"d0"},
        "charity": {"p"},
    }
    supplier = {
        packet: owner for owner, packets in initial.items() for packet in packets
    }
    rows = []
    for d_core, d_edge in D_TRANSFER.items():
        for omitted in ("r", "q", "s"):
            final = {owner: set(packets) for owner, packets in initial.items()}
            final["charity"].remove("p")
            final[omitted].add("p")
            d_supplier, _ = d_edge
            final[d_supplier].remove(d_core)
            final["d"].add(d_core)
            for core, (source, recipient) in CYCLE_TRANSFER.items():
                if core == OMITTED_CORE[omitted]:
                    continue
                final[source].remove(core)
                final[recipient].add(core)
            assert set().union(*initial.values()) == set().union(*final.values())
            edges = {
                (supplier[packet], owner)
                for owner, packets in final.items()
                for packet in packets if supplier[packet] != owner
            }
            assert len(edges) == 4
            lost = initial[omitted] - final[omitted]
            expected_lost = {OUTGOING_CORE[omitted]}
            if d_supplier == omitted:
                expected_lost.add(d_core)
            assert lost == expected_lost
            rows.append({
                "d_core": d_core,
                "omitted_source": omitted,
                "lost_packets": sorted(lost),
                "support_edges": sorted(map(list, edges)),
            })
    assert len(rows) == 6
    return rows


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results" / "FORM2_SIX_BRANCH_PAYMENT_COMPRESSION_LEMMA_20260814.md"
    return {
        "schema": "form2-six-branch-payment-compression-v1",
        "status": "SIX_FAILURES_IFF_THREE_SUPPLIER_CAPTURES",
        "scalar_checks": scalar_equivalence(),
        "branches": branch_table(),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "cap-free owner-payment compression on the disjoint branch; "
            "observer and saturation closure remain open"
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
        "status": result["status"], "branch_count": len(result["branches"])
    }, indent=2))


if __name__ == "__main__":
    main()
