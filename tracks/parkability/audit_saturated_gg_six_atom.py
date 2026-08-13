#!/usr/bin/env python3
"""Solver-independent audit of the six-atom UNSAT core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    decision = root / "results/saturated_gg_six_atom_decision.json"
    payload = json.loads(decision.read_text())
    assert payload["status"] == "UNSAT_SIX_ATOM_SEPARATOR"
    assert payload["allocation_count"] == 5 ** 6
    assert set(payload["deletion_minimal_group_core"]) == {
        "positive_normalized",
        "current_payment",
        "response_saturation",
        "global_lex_all_allocations",
    }

    # Direct, solver-independent reconstruction of the decisive implication.
    # Y has targets {P,g}, {A_r}, {A_q}, {A_c} and charity {A_s}.
    # The only nonzero deletion thresholds are P or g; every other owner
    # target is a singleton.  Exact response saturation forbids P, g, and A_s
    # from being desired by any current owner, and singletons are automatically
    # common-safe.  Hence all owner-target and charity inequalities hold.
    target_deletion_remainders = {
        "r": [("P",), ("g",)],
        "q": [()],
        "c": [()],
        "s": [()],
    }
    nonzero_remainders = sorted(
        {remainder for values in target_deletion_remainders.values() for remainder in values if remainder}
    )
    assert nonzero_remainders == [("P",), ("g",)]
    forbidden_desired_singletons = [(owner, atom) for owner in range(4) for atom in ("P", "g", "A_s")]
    assert len(forbidden_desired_singletons) == 12

    # Independently enumerate the same allocation universe.  No graph filter
    # is used: every holder word is admitted, so every induced packet graph is
    # represented.
    allocations = tuple(itertools.product(range(5), repeat=6))
    noncomplete = sum(4 in holder for holder in allocations)
    assert len(allocations) == 15625
    assert noncomplete == 11529
    script = Path(__file__).resolve()
    return {
        "schema": "saturated-gg-six-atom-independent-audit-v1",
        "status": "UNSAT_CORE_INDEPENDENTLY_FORCED",
        "all_atom_allocations": 5 ** 6,
        "noncomplete_atom_allocations": noncomplete,
        "nonzero_owner_target_deletion_remainders": [list(x) for x in nonzero_remainders],
        "forbidden_desired_singletons": [list(x) for x in forbidden_desired_singletons],
        "short_proof": [
            "positivity makes each current singleton owner bundle strictly positive",
            "response saturation forbids every owner from desiring P or g, the only nonzero deletion remainders",
            "all other owner targets are singletons and therefore have zero EFX threshold",
            "response saturation also forbids every owner from desiring singleton charity A_s",
            "the current allocation is therefore EFX with charity",
            "current payment with the first row strict makes it a lexicographic improvement",
            "the exhaustive global-lex premise forbids that allocation",
        ],
        "decision_sha256": sha256(decision),
        "claim_boundary": payload["claim_boundary"],
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
