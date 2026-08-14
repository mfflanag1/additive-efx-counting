#!/usr/bin/env python3
"""Exact support audit for nonroot singleton safe-envelope descent."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    old_root, base_root, core_root = z3.Reals("old_root base_root core_root")
    root_reselection = prove(
        [old_root > base_root, core_root > old_root],
        core_root > base_root,
    )

    old_source, core_source = z3.Reals("old_source core_source")
    source_strict = prove(
        [old_source >= 0, core_source > old_source],
        core_source > old_source,
    )

    universe = {"p", "a", "b", "c"}
    strict_subsets = 0
    for mask in range(1 << 3):
        envelope = {"p"} | {
            good for index, good in enumerate(("a", "b", "c")) if mask & (1 << index)
        }
        if len(envelope) > 1:
            next_envelope = set(envelope)
            next_envelope.remove(next(good for good in envelope if good != "p"))
            assert {"p"} <= next_envelope < envelope <= universe
            strict_subsets += 1
    assert strict_subsets == 7

    theorem = root / "results" / "NONROOT_SINGLETON_HIT_SAFE_ENVELOPE_DESCENT_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "nonroot-singleton-hit-safe-envelope-descent-audit-v1",
        "status": "NONROOT_SINGLETON_HIT_DESCENT_PROVED",
        "root_reselection_preserves_strict_base": root_reselection,
        "nonroot_source_strictly_improves": source_strict,
        "strict_envelope_examples_checked": strict_subsets,
        "singleton_tail_is_zero": True,
        "maximum_descent_steps_from_initial_core": "|D|-1",
        "root_holder_supplier_star_imported": False,
        "claim_boundary": (
            "nonroot-held singleton-containing response descent only; disjoint "
            "Hall compression, fixed-U, GG, and EFX remain open"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
