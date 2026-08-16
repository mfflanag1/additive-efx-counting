#!/usr/bin/env python3
"""Ask the fixed-U physical master which coincidence partitions each role can carry.

A named role admits a witness partition with `b` blocks exactly when
`T[i,g] >= b * M[i,g]` for every observer `i` (the block-count realizability
lemma, audited constructively in
`audit_identity_aware_witness_realizability.py`).  This sweep pushes that
condition into the exact-response physical master and asks, per role and per
block count, whether the fixed-U premises admit any profile meeting it.

`sat` exhibits an exact rational profile whose role carries every partition of
that width; `unsat` proves the premises forbid every such partition at that
role.  `unknown` is a timing diagnostic and carries no mathematical content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def probe(form_index, role, blocks, timeout_seconds, random_seed):
    solver, value, minimum = build_physical_master(form_index)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    solver.add(*(
        value[role, observer] >= blocks * minimum[role, observer]
        for observer in OWNERS
    ))
    status = solver.check()
    witness = None
    if status == z3.sat:
        model = solver.model()
        witness = {
            observer: {
                "total": str(Fraction(str(model.eval(
                    value[role, observer], model_completion=True)))),
                "minimum": str(Fraction(str(model.eval(
                    minimum[role, observer], model_completion=True)))),
            }
            for observer in OWNERS
        }
        for observer in OWNERS:
            total = Fraction(witness[observer]["total"])
            least = Fraction(witness[observer]["minimum"])
            assert least > 0 and total >= blocks * least, (role, observer)
    return str(status), witness, (
        solver.reason_unknown() if status == z3.unknown else None
    )


def run(output_path, form_index, block_counts, timeout_seconds, random_seed):
    rows = {}
    for role in GOODS:
        rows[role] = {}
        for blocks in block_counts:
            status, witness, reason = probe(
                form_index, role, blocks, timeout_seconds, random_seed
            )
            entry = {"status": status}
            if witness is not None:
                entry["witness"] = witness
            if reason is not None:
                entry["reason_unknown"] = reason
            rows[role][str(blocks)] = entry
            # A role that cannot reach `b` blocks cannot reach more than `b`.
            if status == "unsat":
                for wider in block_counts:
                    if wider > blocks:
                        rows[role][str(wider)] = {
                            "status": "unsat",
                            "inherited_from_block_count": blocks,
                        }
                break
    result = {
        "schema": "identity-aware-partition-admission-sweep-v1",
        "form_index": form_index,
        "block_counts": list(block_counts),
        "observers": list(OWNERS),
        "roles": rows,
        "admission_rule": (
            "role g admits a b-block coincidence partition iff "
            "T[i,g] >= b*M[i,g] for every observer i; every b-block partition "
            "of the four observers then becomes realizable, so the fifteen-row "
            "partition table is determined by these block-count verdicts"
        ),
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "claim_boundary": (
            "sat is an exact rational admission witness for the declared "
            "exact-response physical master; unsat proves that master forbids "
            "the block count at that role; unknown is a timing diagnostic "
            "only.  Nothing here decides an EFX allocation."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--random-seed", type=int, default=8160)
    args = parser.parse_args()
    result = run(args.output, args.form_index, (2, 3, 4),
                 args.timeout_seconds, args.random_seed)
    for role, row in result["roles"].items():
        print(role, {blocks: entry["status"] for blocks, entry in sorted(row.items())})


if __name__ == "__main__":
    main()
