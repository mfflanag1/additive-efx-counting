#!/usr/bin/env python3
"""Inject and split on the exact fixed-cell pair-deficiency theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import candidate_partitions
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import candidate_partitions


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_witness(edges, agents, bundle):
    return z3.And(
        *(
            z3.Not(edges[agent][other])
            for agent in agents
            for other in range(4)
            if other != bundle
        )
    )


def run(
    source: Path,
    output: Path,
    output_dir: Path,
    manifest: Path,
    core: Path | None,
    branch_axis: str,
    designated: bool,
) -> dict:
    solver = z3.Solver()
    solver.from_file(str(source))
    pairs = tuple(itertools.combinations(range(4), 2))
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    moves = list(candidate_partitions(base, 8))
    if core is None:
        selected_partitions = tuple(range(91))
    else:
        core_document = json.loads(core.read_text())
        selected_partitions = tuple(
            sorted(
                {
                    record["partition_index"]
                    for record in core_document["bounded_deletion_unsat_core"]
                    if record["kind"] == "no_pair_deficiency"
                }
            )
        )
    pair_formulas = []
    for pair in pairs:
        witnesses = []
        for partition in selected_partitions:
            edges = tuple(
                tuple(
                    z3.Bool(f"edge_{partition}_{agent}_{bundle}")
                    for bundle in range(4)
                )
                for agent in range(4)
            )
            bundles = (
                (
                    moves[partition]["move_destination"]
                    if moves[partition]["moved_good"] == 5
                    else moves[partition]["floater_host"]
                ),
            ) if designated else range(4)
            witnesses.extend(pair_witness(edges, pair, bundle) for bundle in bundles)
        pair_formulas.append(z3.Or(*witnesses))
    solver.add(z3.Or(*pair_formulas))
    output.write_text(solver.to_smt2())

    output_dir.mkdir(parents=True, exist_ok=True)
    if branch_axis == "pair":
        branch_keys = pairs
        branch_formulas = pair_formulas
        branch_records = [
            {"deficient_agents": list(pair)} for pair in pairs
        ]
        branch_names = [f"pair_{pair[0]}_{pair[1]}" for pair in pairs]
    elif branch_axis == "host":
        branch_keys = tuple(range(4))
        branch_formulas = []
        branch_records = []
        branch_names = []
        for host in branch_keys:
            host_partitions = tuple(
                partition
                for partition in selected_partitions
                if moves[partition]["floater_host"] == host
            )
            witnesses = []
            for partition in host_partitions:
                edges = tuple(
                    tuple(
                        z3.Bool(f"edge_{partition}_{agent}_{bundle}")
                        for bundle in range(4)
                    )
                    for agent in range(4)
                )
                for pair in pairs:
                    bundles = (
                        (
                            moves[partition]["move_destination"]
                            if moves[partition]["moved_good"] == 5
                            else moves[partition]["floater_host"]
                        ),
                    ) if designated else range(4)
                    witnesses.extend(
                        pair_witness(edges, pair, bundle) for bundle in bundles
                    )
            branch_formulas.append(z3.Or(*witnesses))
            branch_records.append(
                {"floater_host": host, "partition_indices": list(host_partitions)}
            )
            branch_names.append(f"host_{host}")
    elif branch_axis == "case":
        if not designated:
            raise ValueError("regular/exceptional cases require designated traps")
        regular = []
        exceptional = []
        for partition in selected_partitions:
            move = moves[partition]
            designated_bundle = (
                move["move_destination"]
                if move["moved_good"] == 5
                else move["floater_host"]
            )
            exceptional_pair = tuple(
                sorted((designated_bundle, move["move_source"]))
            )
            edges = tuple(
                tuple(
                    z3.Bool(f"edge_{partition}_{agent}_{bundle}")
                    for bundle in range(4)
                )
                for agent in range(4)
            )
            for pair in pairs:
                witness = pair_witness(edges, pair, designated_bundle)
                (exceptional if pair == exceptional_pair else regular).append(witness)
        branch_formulas = [z3.Or(*regular), z3.Or(*exceptional)]
        branch_records = [
            {"case": "regular", "witness_count": len(regular)},
            {"case": "owner_source_exception", "witness_count": len(exceptional)},
        ]
        branch_names = ["regular", "owner_source_exception"]
    else:
        raise ValueError(f"unsupported branch axis: {branch_axis}")
    branches = []
    previous = []
    for index, (formula, record, name) in enumerate(
        zip(branch_formulas, branch_records, branch_names)
    ):
        solver.push()
        solver.add(*(z3.Not(item) for item in previous), formula)
        path = output_dir / f"{name}.smt2"
        path.write_text(solver.to_smt2())
        branches.append(
            {
                "branch": index,
                **record,
                "prior_branch_exclusions": index,
                "path": str(path),
                "sha256": sha256(path),
            }
        )
        solver.pop()
        previous.append(formula)
    artifact = {
        "schema": "partial-hall-pair-deficiency-strengthening-v1",
        "status": "EXACT_STRENGTHENING_AND_COVER",
        "meaning": (
            "The injected pair-deficiency disjunction is implied by the "
            "fixed-cell obstruction constraints, as independently proved by "
            "the dual-verified pair-deficiency theorem. The disjoint branches "
            "select the first pair or floater-host class on the requested axis."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "output": str(output),
        "output_sha256": sha256(output),
        "pair_deficiency_proof": (
            "results/partial_hall_designated_pair_trap.json"
            if designated
            else "results/partial_hall_pair_deficiency_compact_core.json"
        ),
        "pair_deficiency_core": str(core) if core is not None else None,
        "selected_partition_count": len(selected_partitions),
        "selected_partition_indices": list(selected_partitions),
        "branch_axis": branch_axis,
        "designated_bundle_only": designated,
        "branch_count": len(branches),
        "branches": branches,
    }
    atomic_json(manifest, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--core", type=Path)
    parser.add_argument(
        "--branch-axis", choices=("pair", "host", "case"), default="pair"
    )
    parser.add_argument("--designated", action="store_true")
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.source,
                args.output,
                args.output_dir,
                args.manifest,
                args.core,
                args.branch_axis,
                args.designated,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
