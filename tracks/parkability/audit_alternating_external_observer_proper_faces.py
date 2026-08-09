#!/usr/bin/env python3
"""Audit every proper face of the binary rooted packet-splitting cube."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_alternating_variable_packet_rooted_cegar import (
        load_pool,
        make_cell,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_alternating_variable_packet_rooted_cegar import (
        load_pool,
        make_cell,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-external-observer-proper-faces-audit-v1"
ORDER = (0, 2, 1, 3)
CASES = (
    ((2, 1, 1, 1), "tr2"),
    ((1, 2, 1, 1), "br2"),
    ((1, 1, 2, 1), "tq2"),
    ((1, 1, 1, 2), "bq2"),
    ((2, 2, 1, 1), "trbr"),
    ((2, 1, 2, 1), "trtq"),
    ((2, 1, 1, 2), "trbq"),
    ((1, 2, 2, 1), "brtq"),
    ((1, 2, 1, 2), "brbq"),
    ((1, 1, 2, 2), "tqbq"),
    ((2, 2, 2, 1), "no_bq"),
    ((2, 2, 1, 2), "no_tq"),
    ((2, 1, 2, 2), "no_br"),
    ((1, 2, 2, 2), "no_tr"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(results_dir: Path) -> dict:
    records = []
    for sizes, tag in CASES:
        pool_path = results_dir / f"alternating_external_observer_0213_{tag}_broad_pool.json"
        session_path = results_dir / f"alternating_external_observer_0213_{tag}_broad_session1.json"
        session = json.loads(session_path.read_text())
        if session.get("status") != "UNSAT_ROOTED_VARIABLE_PACKET_CELL":
            raise AssertionError((tag, "session status", session.get("status")))
        cell = make_cell(sizes)
        rivals = load_pool(pool_path, cell, ORDER)
        if len(rivals) != session.get("pool_size"):
            raise AssertionError((tag, "pool size mismatch"))
        solver, values, own = structural_solver(cell)
        solver.add(*(rival_blocker(values, own, rival, ORDER) for rival in rivals))
        status = str(solver.check())
        if status != "unsat":
            raise AssertionError((tag, "replay", status))
        records.append(
            {
                "tag": tag,
                "packet_sizes": list(sizes),
                "goods": list(cell["goods"]),
                "rival_count": len(rivals),
                "replay_status": status,
                "pool_sha256": sha256(pool_path),
                "session_sha256": sha256(session_path),
            }
        )

    script = Path(__file__).resolve()
    search_script = script.with_name("run_alternating_variable_packet_rooted_cegar.py")
    return {
        "schema": SCHEMA,
        "status": "ALL_14_BINARY_PROPER_FACES_UNSAT",
        "claim_boundary": {
            "proved_exactly": "the rooted external-observer escape for order (p,s,r,q) in every binary packet-size cell with at least one atomic packet",
            "symmetry": "the half-turn order (s,p,q,r) follows after swapping the two large and two singleton roles",
            "not_proved": "the fully split (2,2,2,2) cell, packet sizes above two, or the cap-free lemma",
        },
        "symmetry_break": "within each nontrivial packet, goods are ordered only in p's valuation row; no cross-agent comonotonicity is imposed",
        "agent_order": list(ORDER),
        "case_count": len(records),
        "cases": records,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "provenance": {
            "audit_script": str(script.relative_to(script.parents[2])),
            "audit_script_sha256": sha256(script),
            "search_script": str(search_script.relative_to(search_script.parents[2])),
            "search_script_sha256": sha256(search_script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.results_dir)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered)


if __name__ == "__main__":
    main()
