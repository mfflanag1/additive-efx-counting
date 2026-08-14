#!/usr/bin/env python3
"""Exact packet-ledger audit for five root-retained proof-core endpoints."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .run_fixed_u_full_packet_terminal_cegar import PACKETS, SUPPORT_STATE


ROOT = Path(__file__).resolve().parents[2]
OWNERS = ("r", "q", "d", "s")


def edges(allocation):
    supplier = {
        good: source
        for source, goods in SUPPORT_STATE.items()
        for good in goods
    }
    return sorted({
        (supplier[good], owner)
        for owner in OWNERS
        for good in allocation[owner]
        if supplier[good] != owner
    })


def run():
    A = frozenset(PACKETS["A"])
    H = frozenset(PACKETS["H"])
    Q = frozenset(PACKETS["Q"])
    J = frozenset(PACKETS["J"])
    E = frozenset(PACKETS["E"])
    L = frozenset(PACKETS["L"])
    W = frozenset(PACKETS["W"])
    M = frozenset(PACKETS["M"])
    P = frozenset(PACKETS["P"])
    universe = set().union(*(set(goods) for goods in SUPPORT_STATE.values()))

    rows = {
        1: {"r": A | H, "q": Q, "d": W | P, "s": E},
        2: {"r": A | H, "q": Q, "d": L | W, "s": (E - L) | P},
        3: {"r": A | H, "q": Q, "d": L | W, "s": (E - L) | P},
        4: {"r": A | H, "q": Q, "d": W | P, "s": E},
        6: {
            "r": A | H,
            "q": (Q - J) | P | M,
            "d": J | (W - M),
            "s": E,
        },
    }
    expected_edges = {
        1: [("charity", "d")],
        2: [("charity", "s"), ("s", "d")],
        3: [("charity", "s"), ("s", "d")],
        4: [("charity", "d")],
        6: [("charity", "q"), ("d", "q"), ("q", "d")],
    }
    audits = []
    for endpoint, allocation in rows.items():
        assert set().union(*(set(bundle) for bundle in allocation.values())) == universe
        assert sum(len(bundle) for bundle in allocation.values()) == len(universe)
        actual_edges = edges(allocation)
        assert actual_edges == expected_edges[endpoint]
        assert len(actual_edges) <= 3
        assert allocation["r"] == frozenset(SUPPORT_STATE["r"])
        if endpoint == 3:
            assert allocation["s"] == frozenset(ALLOCATED_E_BASE["s"])
        audits.append({
            "endpoint": endpoint,
            "edge_count": len(actual_edges),
            "edges": [list(edge) for edge in actual_edges],
        })

    theorem = ROOT / "results/FIVE_CORE_ENDPOINT_ROOT_RETENTION_LEDGER_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "five-core-endpoint-root-retention-ledger-audit-v1",
        "status": "AUDIT_PASSED",
        "endpoint_audits": audits,
        "maximum_edge_count": max(row["edge_count"] for row in audits),
        "all_complete": True,
        "root_bundle_retained_exactly": True,
        "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact packet partition and supplier-edge audit. Valuation margins "
            "are algebraic identities in the theorem; EFX is not asserted."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
