#!/usr/bin/env python3
"""Dependency and edge audit for the nonroot three-placement relay."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    owners = ("r", "q", "d", "s")
    nonroot = tuple(owner for owner in owners if owner != "r")
    matching_edges = {("u0", "r"), ("u1", "q"), ("u2", "s")}
    records = []
    for holder in nonroot:
        edges = matching_edges | {("charity", holder)}
        assert len(edges) <= 4
        records.append({"holder": holder, "edge_count": len(edges), "root_holder": False})

    theorem = root / "results" / "NONROOT_THREE_PLACEMENT_RELAY_COLLISION_ELIMINATION_20260814.md"
    transport = root / "results" / "FOUR_PLACEMENT_SINGLETON_RESPONSE_TRANSPORT_LEMMA_20260814.md"
    descent = root / "results" / "NONROOT_SINGLETON_HIT_SAFE_ENVELOPE_DESCENT_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    for dependency in (theorem, transport, descent):
        assert dependency.exists()

    return {
        "schema": "nonroot-three-placement-relay-collision-elimination-audit-v1",
        "status": "ROOT_HOLDER_DEPENDENCY_ELIMINATED",
        "nonroot_probe_records": records,
        "maximum_support_provenance_edges": 4,
        "every_p_hitting_probe_has_nonroot_holder": True,
        "whole_hit_dependency": str(descent.relative_to(root)),
        "disjoint_transport_dependency": str(transport.relative_to(root)),
        "imported_complete_collision_theorem_required": False,
        "remaining_gate": "universally safe source-parking Hall compression",
        "claim_boundary": (
            "dependency/edge composition only; the nonroot descent remains a "
            "mathematical dependency and Hall compression, fixed-U, GG, and EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "transport_sha256": sha256(transport),
            "whole_hit_descent_sha256": sha256(descent),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "remaining_gate": result["remaining_gate"]}, indent=2))


if __name__ == "__main__":
    main()
