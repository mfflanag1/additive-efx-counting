#!/usr/bin/env python3
"""Audit the 2+2 terminal role split and cross-exchange identities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3

from .audit_canonical_path_base_response_prefix_or_terminal_split import run as parent_run


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT) -> dict[str, object]:
    parent = parent_run(root)
    terminal = []
    predecessor_duplicate = 0
    first_duplicate = 0
    for mapping in parent["terminal_position_mappings"]:
        mapping = tuple(mapping)
        # For fixed roles, path is reconstructed from the known terminal records.
        missing = 0
        duplicate = next(source for source in range(4) if mapping.count(source) == 2)
        # Follow the unique path from the missing source to terminal q=1.
        order = [missing]
        while len(order) < 4:
            order.append(mapping[order[-1]])
        assert order[-1] == 1
        omitted_source = mapping[1]
        category = "predecessor" if omitted_source == order[2] else "first"
        assert omitted_source in (order[1], order[2])
        predecessor_duplicate += category == "predecessor"
        first_duplicate += category == "first"
        terminal.append({
            "mapping": list(mapping),
            "path": order,
            "omitted_source": omitted_source,
            "category": category,
        })

    old_m, old_y, old_x, old_q, base_m, base_y, base_x, base_q = z3.Reals(
        "old_m old_y old_x old_q base_m base_y base_x base_q"
    )
    c_m, e_x, d_q, p_m = z3.Reals("c_m e_x d_q p_m")
    payment = z3.SolverFor("QF_LRA")
    payment.add(
        old_m >= 0,
        c_m > base_m,
        old_x >= base_x,
        old_q >= base_q,
        e_x > old_x,
        d_q > old_q,
        old_y >= base_y,
        p_m > 0,
    )
    payment.add(z3.Or(
        old_m + c_m + p_m <= base_m,
        e_x <= base_x,
        d_q <= base_q,
        old_y < base_y,
    ))

    e_total, e_outside, floor = z3.Reals("e_total e_outside floor")
    capture = z3.SolverFor("QF_LRA")
    capture.add(e_total > floor, e_outside <= floor)
    capture.add(z3.Not(e_total - e_outside >= e_total - floor))

    theorem = root / "results/TERMINAL_PATH_OMITTED_CORE_CROSS_EXCHANGE_FRONTIER_20260814.md"
    parent_theorem = root / "results/CANONICAL_PATH_BASE_RESPONSE_PREFIX_OR_TERMINAL_SPLIT_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Predecessor-duplicate cross exchange" in text
    assert "two predecessor-duplicate" in text

    return {
        "schema": "terminal-path-omitted-core-cross-exchange-frontier-audit-v1",
        "status": "TWO_CROSS_EXCHANGE_OR_CAPTURE_TWO_TERMINAL_SPLIT",
        "terminal_map_count": len(terminal),
        "predecessor_duplicate_maps": predecessor_duplicate,
        "first_source_duplicate_maps": first_duplicate,
        "terminal_records": terminal,
        "cross_exchange_owner_payments": payment.check() == z3.unsat,
        "overlap_capture_identity": capture.check() == z3.unsat,
        "current_holder_edge_count": 4,
        "packet_size_bound_used": False,
        "frozen_supplier_edge_bound_proved": False,
        "observer_safety_proved": False,
        "capture_reversed": False,
        "fixed_u_theorem_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent_theorem, script)
        },
        "claim_boundary": (
            "two terminal maps close by predecessor cross exchange when "
            "uncrossed; failure is capture, while two retain the split gate"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
