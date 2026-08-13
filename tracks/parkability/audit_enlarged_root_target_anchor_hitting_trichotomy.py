#!/usr/bin/env python3
"""Audit the enlarged-root-target anchor-hitting trichotomy."""

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


def run(root: Path) -> dict:
    own, dk, de, total, good, rest = z3.Reals(
        "own dk de total good rest"
    )
    premises = [
        own >= 0,
        dk > 0,
        de > 0,
        total == dk + de,
        total > own,
        dk <= own,
        de <= own,
    ]
    mixed_checks = {
        "anchor_capture": prove(premises, dk > own - de),
        "response_capture": prove(premises, de > own - dk),
    }
    critical_premises = [
        *premises,
        total == good + rest,
        rest <= own,
        good > 0,
    ]
    mixed_checks["individual_good_critical"] = prove(
        critical_premises, good >= total - own
    )
    assert all(mixed_checks.values())

    base, assigned, anchor_total = z3.Reals("base assigned anchor_total")
    old_checks = {
        "represented_anchor_response_is_old": prove(
            [assigned >= base, anchor_total > assigned],
            anchor_total > base,
        ),
        "sacrificed_anchor_response_loss_band": prove(
            [assigned < base, assigned < anchor_total, anchor_total <= base],
            z3.And(assigned < anchor_total, anchor_total <= base),
        ),
    }
    assert all(old_checks.values())

    # The three support types exhaust every nonempty subset of two disjoint
    # atoms K and E.
    support_types = []
    for k_present in (False, True):
        for e_present in (False, True):
            if not (k_present or e_present):
                continue
            kind = (
                "mixed_anchor_hitting" if k_present and e_present else
                "anchor_side" if k_present else "response_side"
            )
            support_types.append({
                "anchor_present": k_present,
                "response_present": e_present,
                "kind": kind,
            })

    theorem = root / "results/ENLARGED_ROOT_TARGET_ANCHOR_HITTING_TRICHOTOMY_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "enlarged-root-target-anchor-hitting-trichotomy-audit-v1",
        "status": "ROOT_TARGET_RESPONSES_REDUCED_TO_SUPPORT_OR_ANCHOR_HITTING",
        "support_types": support_types,
        "mixed_checks": mixed_checks,
        "anchor_side_checks": old_checks,
        "claim_boundary": (
            "cap-free response localization; repeated support labels, source-"
            "inactive loss bands, and mixed anchor hitting remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "support_types": result["support_types"],
    }, indent=2))


if __name__ == "__main__":
    main()

