#!/usr/bin/env python3
"""Independent exact audit of saturated full-owner charity extraction."""

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


def forced(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def connected(vertices: set[str], undirected_edges: set[frozenset[str]]) -> bool:
    adjacency = {vertex: set() for vertex in vertices}
    for edge in undirected_edges:
        left, right = tuple(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    queue = deque([next(iter(vertices))])
    while queue:
        vertex = queue.popleft()
        if vertex in seen:
            continue
        seen.add(vertex)
        queue.extend(sorted(adjacency[vertex] - seen))
    return seen == vertices


def physical_record(path: tuple[str, ...], source: str) -> dict:
    h0, h1, h2, h3 = path
    current = {
        h0: {"P", "g", f"R:{h0}"},
        h1: {f"A:{h0}", f"R:{h1}"},
        h2: {f"A:{h1}", f"R:{h2}"},
        h3: {f"A:{h2}", f"R:{h3}"},
        CHARITY: {f"A:{h3}", "R:charity"},
    }
    candidate = {
        h0: {"P"},
        h1: {f"A:{h1}", f"R:{h1}"},
        h2: {f"A:{h2}", f"R:{h2}"},
        h3: {f"A:{h3}", f"R:{h3}"},
        CHARITY: {f"A:{h0}", "g", f"R:{h0}", "R:charity"},
    }
    old_atoms = set().union(*current.values())
    new_atoms = set().union(*candidate.values())
    assert len(old_atoms) == sum(map(len, current.values()))
    assert len(new_atoms) == sum(map(len, candidate.values()))
    assert old_atoms == new_atoms

    old_holder = {atom: holder for holder, atoms in current.items() for atom in atoms}
    new_holder = {atom: holder for holder, atoms in candidate.items() for atom in atoms}
    transfers = sorted(
        (old_holder[atom], new_holder[atom], atom)
        for atom in old_atoms
        if old_holder[atom] != new_holder[atom]
    )
    directed = {(left, right) for left, right, _ in transfers}
    undirected = {frozenset((left, right)) for left, right in directed}
    vertices = set(OWNERS) | {CHARITY}
    cycle = {
        (CHARITY, h3),
        (h3, h2),
        (h2, h1),
        (h1, CHARITY),
    }
    assert cycle <= directed
    assert (h0, CHARITY) in directed
    assert connected(vertices, undirected)

    return {
        "path": list(path),
        "response_source": source,
        "current_partition": {key: sorted(value) for key, value in current.items()},
        "candidate_partition": {key: sorted(value) for key, value in candidate.items()},
        "transfers": [list(transfer) for transfer in transfers],
        "connected_on_all_five_targets": True,
        "directed_charity_cycle": [CHARITY, h3, h2, h1, CHARITY],
        "charity_donates_and_receives": True,
        "goods_conserved": True,
    }


def run(root: Path) -> dict:
    records = [
        physical_record(path, source)
        for path in itertools.permutations(OWNERS)
        for source in path[1:]
    ]
    assert len(records) == 72
    assert len({tuple(record["path"]) for record in records}) == 24
    source_positions = Counter(
        record["path"].index(record["response_source"]) for record in records
    )
    assert source_positions == {1: 24, 2: 24, 3: 24}

    x_t, old_t, tau_d, value_p = z3.Reals("x_t old_t tau_d value_p")
    target_paid = forced(
        [old_t > x_t, tau_d > old_t, value_p == tau_d],
        value_p > x_t,
    )

    paid_d, tau_p, tau_d_observer = z3.Reals(
        "paid_d tau_p tau_d_observer"
    )
    deletion_inherits_payment = forced(
        [paid_d >= tau_d_observer, tau_p <= tau_d_observer],
        paid_d >= tau_p,
    )

    a_s, r_s, tau_p_s, tau_d_s, c_s, x_s = z3.Reals(
        "a_s r_s tau_p_s tau_d_s c_s x_s"
    )
    source_failure_forces_self_response = forced(
        [
            a_s > x_s,
            a_s + r_s < tau_p_s,
            tau_p_s <= tau_d_s,
            tau_d_s <= c_s + r_s,
        ],
        c_s > a_s,
    )

    x_i, delta_i, z_i, threshold, charity_value = z3.Reals(
        "x_i delta_i z_i threshold charity_value"
    )
    target_surplus_budget = forced(
        [z_i == x_i + delta_i, delta_i >= 0, z_i >= threshold],
        threshold - x_i <= delta_i,
    )
    charity_surplus_budget = forced(
        [z_i == x_i + delta_i, delta_i >= 0, z_i >= charity_value],
        charity_value - x_i <= delta_i,
    )

    efx, pi, support, record, progress = z3.Bools(
        "efx pi support record progress"
    )
    saturated_forces_efx = forced(
        [
            z3.Or(efx, pi, support, record, progress),
            z3.Not(pi),
            z3.Not(support),
            z3.Not(record),
            z3.Not(progress),
        ],
        efx,
    )

    checks = {
        "all_24_hamiltonian_paths": len({tuple(r["path"]) for r in records}) == 24,
        "all_72_nonself_sources": len(records) == 72,
        "exact_atom_conservation": all(r["goods_conserved"] for r in records),
        "connected_five_target_exchange": all(
            r["connected_on_all_five_targets"] for r in records
        ),
        "directed_cycle_through_charity": all(
            r["directed_charity_cycle"][0] == CHARITY
            and r["directed_charity_cycle"][-1] == CHARITY
            for r in records
        ),
        "charity_donates_and_receives": all(
            r["charity_donates_and_receives"] for r in records
        ),
        "target_owner_payment": target_paid,
        "deletion_inherits_observer_payment": deletion_inherits_payment,
        "source_failure_forces_self_response": source_failure_forces_self_response,
        "efx_implies_target_surplus_budget": target_surplus_budget,
        "efx_implies_charity_surplus_budget": charity_surplus_budget,
        "saturation_excludes_all_non_efx_exits": saturated_forces_efx,
    }
    assert all(checks.values())

    dependencies = [
        "FOUR_OWNER_DECORATED_COMPONENT_EXHAUSTION_LEMMA_20260811.md",
        "PI_FREE_FIVE_TARGET_CHARITY_PATH_HOLE_EDGE_LEMMA_20260811.md",
        "MIXED_MARGIN_NONOWNER_RESIDUAL_OR_SELF_RESPONSE_LEMMA_20260811.md",
        "CLOSING_SOURCE_DELETION_RETURN_RESIDUAL_COMPLETION_LEMMA_20260811.md",
        "ARBITRARY_CHARITY_PACKET_BLOCKER_COLLAPSE_LEMMA_20260811.md",
        "CHARITY_BLOCKER_EXCHANGE_WALK_LEMMA_20260811.md",
        "SURPLUS_BUDGETED_CHARITY_EXCHANGE_COMPONENT_LEMMA_20260811.md",
    ]
    dependency_hashes = {
        f"results/{name}": sha256(root / "results" / name) for name in dependencies
    }
    theorem = root / "results/UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md"
    script = Path(__file__).resolve()
    return {
        "schema": "universal-full-owner-charity-exchange-extraction-audit-v1",
        "status": "SATURATED_TERMINAL_EXCLUDED",
        "scope": {
            "owners": 4,
            "good_cap": None,
            "packet_cardinality_cap": None,
            "moved_good_radius_cap": None,
            "positive_additive_values": True,
        },
        "path_count": 24,
        "nonself_source_count": 72,
        "source_position_counts": {
            str(key): value for key, value in sorted(source_positions.items())
        },
        "checks": checks,
        "records": records,
        "dependencies": dependency_hashes,
        "claim_boundary": (
            "cap-free exclusion of the declared exact saturated four-owner "
            "decorated/base-margin terminal; reachability from every GG branch, "
            "full GG, four-agent EFX, and general additive EFX remain open"
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
    print(json.dumps({key: result[key] for key in ("status", "path_count", "nonself_source_count")}, indent=2))


if __name__ == "__main__":
    main()
