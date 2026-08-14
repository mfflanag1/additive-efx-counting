#!/usr/bin/env python3
"""Audit canonical path positions, prefix edges, and terminal split algebra."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3

from .audit_image_three_unique_hamiltonian_omission_and_hole import path_order


ROOT = Path(__file__).resolve().parents[2]
OWNERS = tuple(range(4))
MISSING = 0
BASE_TARGET = 1


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT) -> dict[str, object]:
    position_histogram = Counter()
    prefix_edge_histogram = Counter()
    records = []
    for mapping in itertools.product(OWNERS, repeat=4):
        if any(mapping[target] == target for target in OWNERS):
            continue
        if len(set(mapping)) != 3 or MISSING in mapping:
            continue
        duplicate = next(owner for owner in OWNERS if mapping.count(owner) == 2)
        choices = []
        for omitted in [target for target in OWNERS if mapping[target] == duplicate]:
            order = path_order(mapping, omitted)
            if order is None:
                continue
            if order[-1] != omitted:
                order.reverse()
            if order[0] == MISSING and all(
                mapping[order[index]] == order[index + 1] for index in range(3)
            ):
                choices.append((omitted, order))
        assert len(choices) == 1
        omitted, order = choices[0]
        position = order.index(BASE_TARGET)
        position_histogram[position] += 1
        if position < 3:
            prefix_edge_histogram[position + 2] += 1
        records.append({
            "mapping": list(mapping),
            "path": order,
            "base_target_position": position,
            "hamiltonian_omission": omitted,
        })

    delta_b, c_b, p_b, incoming_b, x_b = z3.Reals(
        "delta_b c_b p_b incoming_b x_b"
    )
    existence = z3.SolverFor("QF_LRA")
    existence.add(delta_b >= 0, c_b >= 0, c_b <= x_b + delta_b)
    existence.add(incoming_b > x_b + delta_b)
    theta = c_b - delta_b
    existence.add(z3.Not(incoming_b >= theta))

    old_b, old_pred, x_pred, c_value, packet_b, packet_pred = z3.Reals(
        "old_b old_pred x_pred c_value packet_b packet_pred"
    )
    payments = z3.SolverFor("QF_LRA")
    payments.add(old_b >= 0, old_pred >= x_pred, c_value >= 0)
    payments.add(packet_b >= c_value - (old_b - x_b))
    payments.add(packet_pred <= old_pred - x_pred)
    payments.add(z3.Or(
        old_b - c_value + packet_b < x_b,
        old_pred - packet_pred < x_pred,
    ))

    theorem = root / "results/CANONICAL_PATH_BASE_RESPONSE_PREFIX_OR_TERMINAL_SPLIT_LEMMA_20260814.md"
    parent = root / "results/IMAGE_THREE_UNIQUE_HAMILTONIAN_OMISSION_AND_HOLE_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Terminal-target bicriteria split" in text
    assert "4+4+4" in text

    return {
        "schema": "canonical-path-base-response-prefix-terminal-split-audit-v1",
        "status": "EIGHT_PREFIX_MAPS_PAID_FOUR_TERMINAL_SPLIT_GATES",
        "fixed_role_map_count": len(records),
        "base_target_path_position_histogram": {
            str(position): position_histogram[position] for position in (1, 2, 3)
        },
        "internal_prefix_current_holder_edge_histogram": {
            str(edges): prefix_edge_histogram[edges] for edges in sorted(prefix_edge_histogram)
        },
        "terminal_compensator_exists": existence.check() == z3.unsat,
        "terminal_payment_identities": payments.check() == z3.unsat,
        "packet_size_bound_used": False,
        "frozen_supplier_edge_bound_proved": False,
        "observer_safety_proved": False,
        "terminal_separator_eliminated": False,
        "fixed_u_theorem_proved": False,
        "terminal_position_mappings": [
            record["mapping"] for record in records if record["base_target_position"] == 3
        ],
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "base-response target internal on the canonical path gives paid "
            "prefix closure; terminal position leaves one bicriteria packet"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
