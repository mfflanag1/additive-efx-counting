#!/usr/bin/env python3
"""Census minimum flexible later-owner EFX escapes in frozen flower profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path

import z3


AGENTS = ("r", "q", "c", "s")
RECIPIENTS = AGENTS + ("_",)
OLD_COMPONENTS = {
    "r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "q": ("aq_tq", "ar_bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}
DEFAULT_PROFILES = (
    "three_nonsingleton_flower_full_capture_swap_gate.json",
    "three_nonsingleton_flower_full_capture_path_gate.json",
    "three_nonsingleton_flower_full_capture_packet_gate.json",
    "three_nonsingleton_flower_full_capture_arm_hub_gate.json",
    "three_nonsingleton_flower_full_capture_arm_response_gate.json",
    "fixed_replacement_lex_completion_refutation.json",
    "maximal_packet_replacement_lex_completion_refutation.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atom_names(component: str) -> tuple[str, ...]:
    if component in ("f", "z"):
        return (component,)
    return tuple(f"{component}_{index}" for index in range(2))


def old_bundles() -> dict[str, tuple[str, ...]]:
    return {
        agent: tuple(
            good
            for component in components
            for good in atom_names(component)
        )
        for agent, components in OLD_COMPONENTS.items()
    }


def value(values, observer, goods) -> Fraction:
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer, goods) -> Fraction:
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return value(values, observer, goods) - min(values[observer][good] for good in goods)


def validate(values, old, allocation) -> dict:
    atoms = tuple(values[AGENTS[0]])
    assigned = [good for recipient in RECIPIENTS for good in allocation[recipient]]
    assert len(assigned) == len(atoms) and set(assigned) == set(atoms)
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: value(values, agent, allocation[agent]) for agent in AGENTS}
    for observer in AGENTS:
        for target in AGENTS:
            assert own[observer] >= tail(values, observer, allocation[target])
        assert own[observer] >= value(values, observer, allocation["_"])
    assert own["r"] >= base["r"]
    assert own["q"] > base["q"]
    return {
        "base_utilities": {agent: str(amount) for agent, amount in base.items()},
        "owner_utilities": {agent: str(amount) for agent, amount in own.items()},
    }


def solve_at_radius(values, old, radius):
    atoms = tuple(values[AGENTS[0]])
    index = {recipient: position for position, recipient in enumerate(RECIPIENTS)}
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    owner = {good: z3.Int(f"owner_{radius}_{good}") for good in atoms}
    solver = z3.Solver()
    for good in atoms:
        solver.add(owner[good] >= 0, owner[good] < len(RECIPIENTS))

    def amount(observer, recipient):
        return z3.Sum(*(
            z3.If(
                owner[good] == index[recipient],
                z3.RealVal(str(values[observer][good])),
                0,
            )
            for good in atoms
        ))

    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: amount(agent, agent) for agent in AGENTS}
    for observer in AGENTS:
        for target in AGENTS:
            total = amount(observer, target)
            for good in atoms:
                solver.add(z3.Implies(
                    owner[good] == index[target],
                    amount(observer, observer)
                    >= total - z3.RealVal(str(values[observer][good])),
                ))
        solver.add(amount(observer, observer) >= amount(observer, "_"))
    solver.add(own["r"] >= z3.RealVal(str(base["r"])))
    solver.add(own["q"] > z3.RealVal(str(base["q"])))
    moved = z3.Sum(*(
        z3.If(owner[good] == index[base_owner[good]], 0, 1)
        for good in atoms
    ))
    solver.add(moved <= radius)
    checked = solver.check()
    if checked != z3.sat:
        return checked, None
    model = solver.model()
    allocation = {
        recipient: [
            good
            for good in atoms
            if model.eval(owner[good], model_completion=True).as_long()
            == index[recipient]
        ]
        for recipient in RECIPIENTS
    }
    return checked, allocation


def transfer_topology(old, allocation):
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    new_owner = {
        good: recipient for recipient in RECIPIENTS for good in allocation[recipient]
    }
    moved = sorted(good for good in new_owner if new_owner[good] != base_owner[good])
    edge_counts = Counter((base_owner[good], new_owner[good]) for good in moved)
    adjacency = defaultdict(set)
    for source, target in edge_counts:
        adjacency[source].add(target)
        adjacency[target].add(source)
    components = []
    unseen = set(adjacency)
    while unseen:
        root = min(unseen)
        queue = deque([root])
        seen = {root}
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        unseen -= seen
        components.append(sorted(seen))
    signature = ";".join(
        f"{source}->{target}:{count}"
        for (source, target), count in sorted(edge_counts.items())
    )
    return {
        "moved_goods": moved,
        "edge_counts": [
            {"source": source, "target": target, "count": count}
            for (source, target), count in sorted(edge_counts.items())
        ],
        "nontrivial_components": sorted(components),
        "signature": signature,
    }


def run(root: Path, profiles=DEFAULT_PROFILES, maximum_radius=6) -> dict:
    old = old_bundles()
    records = []
    topology_counts = Counter()
    for filename in profiles:
        path = root / "results" / filename
        payload = json.loads(path.read_text())
        values = {
            agent: {good: Fraction(str(amount)) for good, amount in row.items()}
            for agent, row in payload["values"].items()
        }
        allocation = None
        statuses = []
        for radius in range(maximum_radius + 1):
            checked, candidate = solve_at_radius(values, old, radius)
            statuses.append(str(checked))
            if checked == z3.sat:
                allocation = candidate
                break
        assert allocation is not None
        utility = validate(values, old, allocation)
        topology = transfer_topology(old, allocation)
        assert len(topology["moved_goods"]) == len(statuses) - 1
        topology_counts[topology["signature"]] += 1
        records.append({
            "profile": filename,
            "profile_sha256": sha256(path),
            "minimum_moved_goods": len(topology["moved_goods"]),
            "radius_statuses": statuses,
            "allocation": allocation,
            "utilities": utility,
            "topology": topology,
        })

    script = Path(__file__).resolve()
    return {
        "schema": "flexible-later-owner-escape-topology-census-v1",
        "status": "CLASSIFIED",
        "profile_count": len(records),
        "maximum_minimum_moved_goods": max(
            record["minimum_moved_goods"] for record in records
        ),
        "topology_counts": [
            {"signature": signature, "count": count}
            for signature, count in sorted(topology_counts.items())
        ],
        "records": records,
        "claim_boundary": (
            "exact minimum-radius flexible EFX escape census for frozen bounded "
            "flower profiles; it does not prove that radius four or the displayed "
            "topologies suffice cap-free"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "solver": f"Z3 {z3.get_version_string()}",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-radius", type=int, default=6)
    args = parser.parse_args()
    result = run(args.root.resolve(), maximum_radius=args.maximum_radius)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "profiles": result["profile_count"],
        "maximum_minimum_moved_goods": result["maximum_minimum_moved_goods"],
        "topology_counts": result["topology_counts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
