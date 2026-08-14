#!/usr/bin/env python3
"""Exact signed-support census for the external-source 3x2 Hall fork."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
FORMS = {
    "R2": {"r": "q", "q": "r", "s": "d"},
    "R3": {"r": "q", "q": "s", "s": "r"},
}
INCOMING_STATES = ("none", "partial", "whole")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enumerate_records():
    records = []
    for form, matching in FORMS.items():
        cells = [(owner, owner, f"R_{owner}") for owner in OWNERS]
        cells.extend(
            (supplier, source, f"C_{source}")
            for source, supplier in matching.items()
        )
        initial_edges = {(supplier, source) for source, supplier in matching.items()}
        assert len(initial_edges) == 3

        for external, intermediate, leaf, other_leaf in itertools.permutations(OWNERS):
            for use_intermediate_residual, use_leaf_residual in itertools.product((False, True), repeat=2):
                for intermediate_incoming, leaf_incoming in itertools.product(INCOMING_STATES, repeat=2):
                    if intermediate not in matching and intermediate_incoming != "none":
                        continue
                    if leaf not in matching and leaf_incoming != "none":
                        continue
                    if not use_intermediate_residual and intermediate_incoming == "none":
                        continue
                    if not use_leaf_residual and leaf_incoming == "none":
                        continue

                    destinations = {owner: set() for owner in OWNERS}
                    for supplier, holder, label in cells:
                        state = "none"
                        recipient = None
                        if label == f"R_{intermediate}" and use_intermediate_residual:
                            state, recipient = "partial", external
                        elif label == f"C_{intermediate}":
                            state, recipient = intermediate_incoming, external
                        elif label == f"R_{leaf}" and use_leaf_residual:
                            state, recipient = "partial", intermediate
                        elif label == f"C_{leaf}":
                            state, recipient = leaf_incoming, intermediate

                        if state == "none":
                            destinations[supplier].add(holder)
                        elif state == "whole":
                            destinations[supplier].add(recipient)
                        else:
                            destinations[supplier].update((holder, recipient))

                    owner_edges = {
                        (supplier, recipient)
                        for supplier, recipients in destinations.items()
                        for recipient in recipients
                        if supplier != recipient
                    }
                    final_edges = owner_edges | {("charity", leaf)}
                    added = owner_edges - initial_edges
                    deleted = initial_edges - owner_edges
                    edge_count = len(final_edges)
                    identity_count = 4 + len(added) - len(deleted)
                    assert edge_count == identity_count
                    within_four = edge_count <= 4
                    assert within_four == (len(added) <= len(deleted))

                    records.append({
                        "form": form,
                        "roles": {
                            "external": external,
                            "intermediate": intermediate,
                            "sacrificed_leaf": leaf,
                            "other_leaf": other_leaf,
                        },
                        "support": {
                            "intermediate_residual_used": use_intermediate_residual,
                            "intermediate_incoming": intermediate_incoming,
                            "leaf_residual_used": use_leaf_residual,
                            "leaf_incoming": leaf_incoming,
                        },
                        "added_edges": sorted([list(edge) for edge in added]),
                        "deleted_edges": sorted([list(edge) for edge in deleted]),
                        "final_edges": sorted([list(edge) for edge in final_edges]),
                        "edge_count": edge_count,
                        "within_four": within_four,
                    })
    return records


def run(root: Path) -> dict:
    records = enumerate_records()
    edge_distribution = Counter(record["edge_count"] for record in records)
    form_counts = {}
    feasible_role_counts = {}
    for form in FORMS:
        form_records = [record for record in records if record["form"] == form]
        form_counts[form] = {
            "patterns": len(form_records),
            "within_four": sum(record["within_four"] for record in form_records),
        }
        feasible_roles = {
            tuple(record["roles"].values())
            for record in form_records if record["within_four"]
        }
        feasible_role_counts[form] = len(feasible_roles)

    assert len(records) == 720
    assert form_counts == {
        "R2": {"patterns": 360, "within_four": 78},
        "R3": {"patterns": 360, "within_four": 78},
    }
    assert dict(sorted(edge_distribution.items())) == {
        2: 3, 3: 25, 4: 128, 5: 282, 6: 225, 7: 53, 8: 4,
    }
    assert feasible_role_counts == {"R2": 18, "R3": 15}

    theorem = root / "results" / "THREE_TARGET_EXTERNAL_SOURCE_FORK_EDGE_CANCELLATION_FRONTIER_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "three-target-external-source-fork-edge-cancellation-audit-v1",
        "status": "EXACT_3X2_SUPPORT_CENSUS_COMPLETE",
        "patterns_checked": len(records),
        "form_counts": form_counts,
        "feasible_role_counts": feasible_role_counts,
        "edge_distribution": {str(key): value for key, value in sorted(edge_distribution.items())},
        "feasible_patterns": [record for record in records if record["within_four"]],
        "edge_cancellation_identity": "|E_final| = 4 + |E_added| - |E_deleted|",
        "remaining_gate": (
            "decide desired/safety/global-maximality feasibility on the 156 "
            "edge-cancelling fork patterns together with the 2x1 frontier"
        ),
        "claim_boundary": (
            "signed support and edge counts only; valuation feasibility, full "
            "saturation, fixed-U, GG, and EFX remain open"
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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "patterns_checked": result["patterns_checked"],
        "form_counts": result["form_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
