#!/usr/bin/env python3
"""Exact scalar audit of minimal safe root anchor or atomwise core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    x, delta, total, good, deleted = z3.Reals(
        "x delta total good deleted"
    )
    atom = prove(
        [total == x + delta, deleted == total - good, deleted <= x],
        good >= delta,
    )

    multiplicity = all(
        prove(
            [total == x + delta, packet_size * delta <= total],
            (packet_size - 1) * delta <= x,
        )
        for packet_size in range(1, 13)
    )

    packet_value, slack, mode = z3.Reals("packet_value slack mode")
    protected_band = prove(
        [packet_value > slack + mode, mode >= 0],
        packet_value > slack,
    )
    assert atom and multiplicity and protected_band

    theorem = repo / "results/MINIMAL_SAFE_ROOT_ANCHOR_OR_ATOMWISE_CORE_LEMMA_20260813.md"
    cut = repo / "results/RETIRED_PACKET_BIROW_SPLIT_OR_CUT_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "minimal-safe-root-anchor-or-atomwise-core-audit-v1",
        "status": "ROOT_RESELECTS_PROPER_SAFE_CORE_OR_IS_ATOMWISE_BASE_CRITICAL",
        "critical_good_bound": atom,
        "multiplicity_bound": multiplicity,
        "protected_cut_exceeds_root_slack": protected_band,
        "terminal": "recipient_indivisibility_or_root_double_atomic_birow_cut",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free root-support reduction and scalar audit; double atomic "
            "cut and full theorem remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "birow_cut": str(cut.relative_to(repo)),
            "birow_cut_sha256": sha256(cut),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "terminal": result["terminal"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
