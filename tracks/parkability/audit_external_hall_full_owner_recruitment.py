#!/usr/bin/env python3
"""Classify which external Hall defects recruit the full owner component."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
FORMS = {
    "R2": (("r", "q"), ("q", "r"), ("s", "d")),
    "R3": (("r", "q"), ("q", "s"), ("s", "r")),
}
NONSELF = tuple((source, target) for source in OWNERS for target in OWNERS
                if source != target)


def components(edges):
    adjacency = {owner: set() for owner in OWNERS}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    result = []
    unseen = set(OWNERS)
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component = set()
        while stack:
            owner = stack.pop()
            if owner in component:
                continue
            component.add(owner)
            stack.extend(adjacency[owner] - component)
        unseen -= component
        result.append(frozenset(component))
    return tuple(sorted(result, key=lambda part: tuple(sorted(part))))


def neighborhood(edges, targets):
    return frozenset(source for source, target in edges if target in targets)


def minimal_external_defects(edges):
    defects = []
    targets_with_edges = {target for _, target in edges}
    for size in range(2, 5):
        for target_tuple in itertools.combinations(OWNERS, size):
            targets = frozenset(target_tuple)
            if not targets <= targets_with_edges:
                continue
            sources = neighborhood(edges, targets)
            if len(sources) >= len(targets):
                continue
            if any(
                len(neighborhood(edges, frozenset(subset))) < len(subset)
                for proper_size in range(1, size)
                for subset in itertools.combinations(targets, proper_size)
            ):
                continue
            assert len(sources) == len(targets) - 1
            if sources <= targets:
                continue
            defects.append((targets, sources))
    return defects


def run(root: Path) -> dict:
    occurrences = Counter()
    residual_shapes = set()
    checked = 0
    for mask in range(1 << len(NONSELF)):
        edges = {
            edge for index, edge in enumerate(NONSELF)
            if mask & (1 << index)
        }
        for targets, sources in minimal_external_defects(edges):
            defect_edges = {
                (source, target) for source, target in edges
                if source in sources and target in targets
            }
            for form, matching_edges in FORMS.items():
                checked += 1
                joined = components((*matching_edges, *defect_edges))
                full_owner = len(joined) == 1
                shape = f"{len(targets)}x{len(sources)}"
                occurrences[(form, shape, full_owner)] += 1
                if not full_owner:
                    residual_shapes.add((
                        form,
                        tuple(sorted(targets)),
                        tuple(sorted(sources)),
                        tuple(sorted(defect_edges)),
                    ))

    residual = [
        {
            "form": form,
            "targets": list(targets),
            "sources": list(sources),
            "defect_edges": [list(edge) for edge in defect_edges],
        }
        for form, targets, sources, defect_edges in sorted(residual_shapes)
    ]
    assert residual
    assert all(row["form"] == "R3" for row in residual)
    assert all(len(row["targets"]) == 2 and len(row["sources"]) == 1
               for row in residual)
    assert all("d" not in (*row["targets"], *row["sources"]) for row in residual)
    assert {
        (tuple(row["targets"]), tuple(row["sources"])) for row in residual
    } == {
        (("q", "r"), ("s",)),
        (("q", "s"), ("r",)),
        (("r", "s"), ("q",)),
    }

    script = Path(__file__).resolve()
    theorem = root / "results" / "EXTERNAL_HALL_FULL_OWNER_RECRUITMENT_LEMMA_20260814.md"
    return {
        "schema": "external-hall-full-owner-recruitment-audit-v1",
        "status": "ONLY_R3_REPRESENTED_2X1_STARS_AVOID_FULL_OWNER_RECRUITMENT",
        "defect_form_occurrences_checked": checked,
        "occurrence_counts": {
            f"{form}_{shape}_{'full' if full else 'residual'}": count
            for (form, shape, full), count in sorted(occurrences.items())
        },
        "distinct_residual_decorations": len(residual),
        "residual_decorations": residual,
        "claim_boundary": (
            "exact owner-component and Hall-incidence classification only; "
            "application of the full-owner separator still requires the frozen "
            "decorated-response, payment, and saturation premises"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "checked": result["defect_form_occurrences_checked"],
        "residual": result["distinct_residual_decorations"],
    }, indent=2))


if __name__ == "__main__":
    main()
