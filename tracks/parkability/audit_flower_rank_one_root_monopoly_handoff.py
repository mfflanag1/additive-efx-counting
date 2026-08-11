#!/usr/bin/env python3
"""Audit the flower rank-one root-monopoly handoff."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    q_tr, q_tq, q_f, q_bq = z3.Reals("q_Tr q_Tq q_f q_Bq")
    live_q_target = check_unsat(
        q_tr + q_f > q_tq + q_bq,
        q_f <= q_bq,
        z3.Not(z3.And(q_tr > q_tq, q_tr + q_bq > q_tq + q_bq)),
    )

    r_dt, r_db, r_tr, r_br = z3.Reals("r_D_T r_D_B r_Tr r_Br")
    bottom_capture_forced = check_unsat(
        r_dt <= r_tr,
        r_br > 0,
        r_dt + r_db > r_tr + r_br,
        r_db <= 0,
    )

    response_relations = []
    sources = ("r", "q", "c", "s")
    for mask in range(1, 1 << len(sources)):
        c_u = {source for bit, source in enumerate(sources) if mask & (1 << bit)}
        response_relations.append({
            "sources": sorted(c_u),
            "rank_two_available": any(source != "r" for source in c_u),
            "root_monopoly": c_u == {"r"},
        })
    assert len(response_relations) == 15
    assert sum(record["root_monopoly"] for record in response_relations) == 1
    assert all(
        record["rank_two_available"] or record["root_monopoly"]
        for record in response_relations
    )

    script = Path(__file__).resolve()
    theorem = root / "results/FLOWER_RANK_ONE_ROOT_MONOPOLY_HANDOFF_LEMMA_20260811.md"
    return {
        "schema": "flower-rank-one-root-monopoly-handoff-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "live_branch_forces_q_desired_disjoint_target": live_q_target,
            "root_desired_subset_forces_nonempty_bottom_capture": bottom_capture_forced,
        },
        "response_relation_count": len(response_relations),
        "rank_two_relation_count": sum(
            record["rank_two_available"] for record in response_relations
        ),
        "root_monopoly_relation_count": sum(
            record["root_monopoly"] for record in response_relations
        ),
        "support_record": {
            "anchored_root_target": ["T_q", "f"],
            "live_q_target": ["T_r", "B_q"],
            "targets_disjoint": True,
            "root_monopoly_capture": "nonempty subset of B_q",
        },
        "claim_boundary": (
            "cap-free rank-two-or-root-bottom-capture handoff; compensation "
            "and recurrence termination are not proved"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results/flower_rank_one_root_monopoly_handoff_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
