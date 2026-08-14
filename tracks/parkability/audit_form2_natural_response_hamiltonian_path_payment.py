#!/usr/bin/env python3
"""Audit the form-2 natural-response Hamiltonian-path payment lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def payment_checks():
    # A base-desired incoming core pays even after the whole current bundle
    # is released.
    x, b, loss, incoming = z3.Reals("x b loss incoming")
    base = z3.SolverFor("QF_LRA")
    base.add(b >= 0, loss >= 0, loss <= b, incoming > x)
    base.add(z3.Not(b - loss + incoming > x))
    base_status = str(base.check())
    assert base_status == "unsat"

    # A current-desired incoming core pays above a represented base floor.
    x2, b2, loss2, incoming2 = z3.Reals("x2 b2 loss2 incoming2")
    current = z3.SolverFor("QF_LRA")
    current.add(b2 > x2, loss2 >= 0, loss2 <= b2, incoming2 > b2)
    current.add(z3.Not(b2 - loss2 + incoming2 > x2))
    current_status = str(current.check())
    assert current_status == "unsat"

    delta_r, charity, cs = z3.Reals("delta_r charity cs")
    root = z3.SolverFor("QF_LRA")
    root.add(charity > 0, cs <= delta_r + charity)
    root.add(z3.Not(delta_r + charity - cs >= 0))
    root_status = str(root.check())
    assert root_status == "unsat"
    return {
        "base_response_recipient_paid": base_status,
        "current_response_recipient_paid": current_status,
        "root_margin_identity": root_status,
    }


def support_checks():
    initial = {
        "r": {"R", "Cs"},
        "s": {"S", "Cq"},
        "q": {"Q", "Cd"},
        "d": {"D"},
        "charity": {"p"},
    }
    final = {
        "r": {"R", "p"},
        "s": {"S", "Cs"},
        "q": {"Q", "Cq"},
        "d": {"D", "Cd"},
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
    expected = {
        ("charity", "r"), ("r", "s"), ("s", "q"), ("q", "d")
    }
    assert edges == expected
    return sorted(map(list, edges))


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = (
        root / "results" /
        "FORM2_NATURAL_RESPONSE_HAMILTONIAN_PATH_PAYMENT_LEMMA_20260814.md"
    )
    return {
        "schema": "form2-natural-response-hamiltonian-path-payment-v1",
        "status": "THREE_RECIPIENTS_PAID_OR_ROOT_CAPTURE",
        "payment_checks": payment_checks(),
        "support_edges": support_checks(),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "cap-free payment and support identities only; observer "
            "continuation and universal menu selection remain open"
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
