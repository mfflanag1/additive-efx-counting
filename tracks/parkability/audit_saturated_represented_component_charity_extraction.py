#!/usr/bin/env python3
"""Exact audit of saturated extraction for represented owner components."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path

import z3


OWNERS = ("r", "q", "c", "s")
CHARITY = "charity"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def forced(premises, conclusion) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def is_connected(vertices, edges) -> bool:
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    queue = deque([CHARITY])
    while queue:
        vertex = queue.popleft()
        if vertex in seen:
            continue
        seen.add(vertex)
        queue.extend(adjacency[vertex] - seen)
    return seen == set(vertices)


def record(component, path, source):
    hole = path[0]
    current = {hole: {"P", "g", f"R:{hole}"}}
    for index in range(1, len(path)):
        current[path[index]] = {f"A:{path[index - 1]}", f"R:{path[index]}"}
    current[CHARITY] = {f"A:{path[-1]}", "R:charity"}

    candidate = {hole: {"P"}}
    for owner in path[1:]:
        candidate[owner] = {f"A:{owner}", f"R:{owner}"}
    candidate[CHARITY] = {f"A:{hole}", "g", f"R:{hole}", "R:charity"}

    old_atoms = set().union(*current.values())
    new_atoms = set().union(*candidate.values())
    assert old_atoms == new_atoms
    assert len(old_atoms) == sum(map(len, current.values()))
    assert len(new_atoms) == sum(map(len, candidate.values()))
    old_holder = {atom: holder for holder, atoms in current.items() for atom in atoms}
    new_holder = {atom: holder for holder, atoms in candidate.items() for atom in atoms}
    transfers = {
        (old_holder[atom], new_holder[atom])
        for atom in old_atoms
        if old_holder[atom] != new_holder[atom]
    }
    expected_cycle = {(CHARITY, path[-1]), (path[1], CHARITY)}
    expected_cycle |= {(path[index], path[index - 1]) for index in range(2, len(path))}
    assert expected_cycle <= transfers
    assert (hole, CHARITY) in transfers
    vertices = set(component) | {CHARITY}
    assert is_connected(vertices, transfers)
    return {
        "component": list(component),
        "path": list(path),
        "source": source,
        "goods_conserved": True,
        "connected": True,
        "cycle": [CHARITY, *reversed(path[1:]), CHARITY],
    }


def run(root: Path) -> dict:
    records = []
    for size in range(2, 5):
        for component in itertools.combinations(OWNERS, size):
            for path in itertools.permutations(component):
                for source in path[1:]:
                    records.append(record(component, path, source))
    counts = Counter(len(item["component"]) for item in records)
    assert counts == {2: 12, 3: 48, 4: 72}

    x_t, old_t, tau_d, p = z3.Reals("x_t old_t tau_d p")
    target_payment = forced([old_t > x_t, tau_d > old_t, p == tau_d], p > x_t)
    a, residual, tau_p, tau_old, incoming, x = z3.Reals(
        "a residual tau_p tau_old incoming x"
    )
    source_failure = forced(
        [a > x, a + residual < tau_p, tau_p <= tau_old, tau_old <= incoming + residual],
        incoming > a,
    )
    efx, pi, support, response, progress, outsider_failure = z3.Bools(
        "efx pi support response progress outsider_failure"
    )
    saturated_endpoint = forced(
        [
            z3.Or(efx, pi, support, response, progress, outsider_failure),
            z3.Not(pi), z3.Not(support), z3.Not(response), z3.Not(progress),
            z3.Not(outsider_failure),
        ],
        efx,
    )

    checks = {
        "all_component_path_source_cases": len(records) == 132,
        "all_goods_conserved": all(item["goods_conserved"] for item in records),
        "all_incremental_graphs_connected": all(item["connected"] for item in records),
        "target_deletion_payment": target_payment,
        "source_failure_forces_self_response": source_failure,
        "saturation_and_outsider_safety_force_efx": saturated_endpoint,
    }
    assert all(checks.values())
    theorem = root / "results/SATURATED_REPRESENTED_COMPONENT_CHARITY_EXTRACTION_THEOREM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "saturated-represented-component-charity-extraction-audit-v1",
        "status": "ALL_SATURATED_COMPONENTS_EXCLUDED",
        "case_count": len(records),
        "component_size_counts": {str(key): value for key, value in sorted(counts.items())},
        "checks": checks,
        "records": records,
        "dependencies": {
            "results/UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md": sha256(
                root / "results/UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md"
            ),
            "results/ARBITRARY_CHARITY_PACKET_BLOCKER_COLLAPSE_LEMMA_20260811.md": sha256(
                root / "results/ARBITRARY_CHARITY_PACKET_BLOCKER_COLLAPSE_LEMMA_20260811.md"
            ),
        },
        "claim_boundary": (
            "cap-free exclusion of saturated represented components of size 2-4 "
            "with directly safe unchanged outsiders; reachability from every fixed-U "
            "state and other GG classes are not established by this audit"
        ),
        "provenance": {
            "python": __import__("platform").python_version(),
            "z3": z3.get_version_string(),
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
    print(json.dumps({k: result[k] for k in ("status", "case_count", "component_size_counts")}, indent=2))


if __name__ == "__main__":
    main()
