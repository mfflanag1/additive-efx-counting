#!/usr/bin/env python3
"""Symbolic and cyclic audit of decorated-head localization."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    outgoing, residual, incoming, target_threshold, current, base = z3.Reals(
        "outgoing residual incoming target_threshold current base"
    )
    symbolic = {
        "decorated_outgoing_cannot_block": prove(
            [outgoing > current, residual >= 0, target_threshold <= current],
            outgoing + residual >= target_threshold,
        ),
        "residual_failure_forces_incoming_over_outgoing": prove(
            [outgoing + residual < target_threshold,
             target_threshold <= incoming + residual],
            incoming > outgoing,
        ),
        "old_incoming_becomes_base_desired": prove(
            [incoming > outgoing, outgoing > base], incoming > base,
        ),
    }
    assert all(symbolic.values())

    patterns = []
    for bits in itertools.product((0, 1), repeat=4):
        decorated_count = sum(bits)
        if decorated_count not in (1, 2, 3):
            continue
        heads = [
            index for index in range(4)
            if bits[index - 1] == 1 and bits[index] == 0
        ]
        assert 1 <= len(heads) <= 2
        patterns.append({
            "edges": ["D" if bit else "O" for bit in bits],
            "decorated_count": decorated_count,
            "decorated_head_positions": heads,
            "decorated_head_count": len(heads),
        })
    assert len(patterns) == 14
    distribution = {
        str(count): sum(record["decorated_head_count"] == count for record in patterns)
        for count in (1, 2)
    }
    assert distribution == {"1": 12, "2": 2}

    anchored = [record for record in patterns if record["edges"][0] == "O"]
    assert len(anchored) == 7
    assert max(record["decorated_head_count"] for record in anchored) == 2

    script = Path(__file__).resolve()
    theorem = root / "results/MIXED_CYCLE_DECORATED_HEAD_LOCALIZATION_LEMMA_20260813.md"
    return {
        "schema": "mixed-cycle-decorated-head-localization-audit-v1",
        "status": "TERMINAL_BLOCKERS_LOCALIZED_TO_AT_MOST_TWO_DECORATED_HEADS",
        "symbolic_checks": symbolic,
        "mixed_cycle_pattern_count": len(patterns),
        "head_count_distribution": distribution,
        "anchored_pattern_count": len(anchored),
        "maximum_terminal_blockers": 2,
        "unique_two_head_topology": "cyclically alternating D,O,D,O",
        "patterns": patterns,
        "claim_boundary": (
            "cap-free scalar and cyclic localization; one/two-head exchange, "
            "exact GG recurrence, and full-pool capture remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
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
        "patterns": result["mixed_cycle_pattern_count"],
        "head_distribution": result["head_count_distribution"],
    }, indent=2))


if __name__ == "__main__":
    main()
