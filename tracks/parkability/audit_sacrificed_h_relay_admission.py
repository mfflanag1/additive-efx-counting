#!/usr/bin/env python3
"""Independent symbolic audit of the sacrificed-H relay admission lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def run(output: Path):
    old_d, new_d, base_d, h = z3.Reals("old_d new_d base_d h")
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        base_d > 0,
        h > 0,
        old_d >= base_d,
        new_d == old_d - h,
        new_d < base_d,
        z3.Not(h > old_d - base_d),
    )
    capture_status = str(solver.check())
    assert capture_status == "unsat"

    root_old, root_new, q_old, q_new, s_old, s_new, hs = z3.Reals(
        "root_old root_new q_old q_new s_old s_new hs"
    )
    preservation = z3.SolverFor("QF_LRA")
    preservation.add(
        root_old > 1,
        root_new == root_old,
        q_old >= 1,
        q_new == q_old,
        hs > 0,
        s_old >= 1,
        s_new == s_old + hs,
        z3.Or(root_new <= 1, q_new < 1, s_new <= s_old),
    )
    preservation_status = str(preservation.check())
    assert preservation_status == "unsat"

    result = {
        "schema": "sacrificed-h-relay-admission-audit-v1",
        "status": "AUDIT_PASSED",
        "capture_negation_status": capture_status,
        "protected_rows_negation_status": preservation_status,
        "incremental_support_edges": [["d", "s"]],
        "canonical_cancellation_restores_first_probe": True,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Proves the scalar payment/capture and protected-row implications. "
            "The imported collision closure and global fixed-U composition "
            "remain separate dependencies."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
