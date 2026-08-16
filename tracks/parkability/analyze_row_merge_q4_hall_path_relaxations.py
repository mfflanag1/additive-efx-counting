#!/usr/bin/env python3
"""Classify the smallest repair-menu relaxations after the Hall-path gate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .analyze_row_merge_q4_adaptive_hall_paths import (
        BASE,
        collect_models,
        is_generic_model,
        values_sha256,
    )
    from .analyze_row_merge_q4_chain_trace import actions_by_partition
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import minimal_hall_witnesses
    from .decide_row_merge_single_wall_radius import literal_graph, matching_count
except ImportError:
    from analyze_row_merge_q4_adaptive_hall_paths import (
        BASE,
        collect_models,
        is_generic_model,
        values_sha256,
    )
    from analyze_row_merge_q4_chain_trace import actions_by_partition
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import minimal_hall_witnesses
    from decide_row_merge_single_wall_radius import literal_graph, matching_count


SCHEMA = "row-merge-q4-hall-path-relaxation-analysis-v1"
N = 4


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def labeled_partition(action: dict) -> tuple:
    moved = [list(bundle) for bundle in BASE]
    vertices = action["vertices"]
    if action["kind"] == "path":
        edges = tuple(zip(vertices[:-1], vertices[1:]))
    else:
        edges = tuple(
            (vertices[index], vertices[(index + 1) % len(vertices)])
            for index in range(len(vertices))
        )
    for (source, target), good in zip(edges, action["goods"]):
        moved[source].remove(good)
        moved[target].append(good)
    return tuple(tuple(sorted(bundle)) for bundle in moved)


def action_record(action: dict, partition, count: int) -> dict:
    return {
        "kind": action["kind"],
        "length": action["length"],
        "vertices": action["vertices"],
        "goods": action["goods"],
        "partition": [list(bundle) for bundle in partition],
        "matching_count": count,
    }


def categories(action: dict) -> tuple[str, ...]:
    kind = action["kind"]
    vertices = action["vertices"]
    found = {"all_chain"}
    if kind == "path":
        found.add("all_paths")
        if 0 in vertices:
            found.add("paths_touching_0")
        if vertices[0] == 0:
            found.add("paths_starting_0")
        if vertices[-1] == 0:
            found.add("paths_ending_0")
        if vertices[0] == 0 or vertices[-1] == 0:
            found.add("paths_endpoint_0")
        if 0 in vertices[1:-1]:
            found.add("paths_with_0_internal")
            found.add(f"paths_length_{action['length']}_with_0_internal")
        if len(vertices) == N:
            found.add("hamiltonian_paths")
            if vertices[-1] == 0:
                found.add("hamiltonian_paths_ending_0")
    else:
        found.add("all_cycles")
        found.add(f"cycles_length_{action['length']}")
        if 0 in vertices:
            found.add("cycles_touching_0")
            found.add(f"cycles_length_{action['length']}_touching_0")
    if (
        kind == "path"
        and vertices[-1] == 0
        or kind == "cycle"
        and 0 in vertices
    ):
        found.add("paths_ending_0_or_cycles_touching_0")
    if (
        kind == "path"
        and (vertices[0] == 0 or vertices[-1] == 0)
        or kind == "cycle"
        and 0 in vertices
    ):
        found.add("endpoint_0_paths_or_cycles_touching_0")
    return tuple(sorted(found))


def reverse_hall_signature(values, action: dict) -> dict | None:
    if action["kind"] != "path" or action["vertices"][-1] != 0:
        return None
    partition = BASE
    vertices = action["vertices"]
    goods = action["goods"]
    steps = []
    for index in reversed(range(action["length"])):
        source = vertices[index]
        target = vertices[index + 1]
        feasible = literal_graph(values, partition)
        witnesses = [
            (agents, neighbors)
            for agents, neighbors in minimal_hall_witnesses(feasible)
            if target not in neighbors
        ]
        containing = [
            (agents, neighbors)
            for agents, neighbors in witnesses
            if source in neighbors
        ]
        moved = [list(bundle) for bundle in partition]
        moved[source].remove(goods[index])
        moved[target].append(goods[index])
        partition = tuple(tuple(sorted(bundle)) for bundle in moved)
        count = matching_count(literal_graph(values, partition))
        steps.append(
            {
                "source": source,
                "target": target,
                "good": goods[index],
                "omitting_witness_count": len(witnesses),
                "source_in_omitting_neighborhood": bool(containing),
                "minimal_witness_sizes": sorted({len(agents) for agents, _ in witnesses}),
                "matching_count_after": count,
            }
        )
        if count:
            break
    if not steps or not steps[-1]["matching_count_after"]:
        raise AssertionError("supporting path lost its matching under replay")
    outside_steps = sum(
        not step["source_in_omitting_neighborhood"] for step in steps
    )
    no_omitting_witness_steps = sum(
        step["omitting_witness_count"] == 0 for step in steps
    )
    return {
        "executed_step_count": len(steps),
        "outside_neighborhood_step_count": outside_steps,
        "no_omitting_witness_step_count": no_omitting_witness_steps,
        "steps": steps,
    }


def run(
    topology_path: Path,
    ranked_paths: tuple[Path, ...],
    extra_gate_paths: tuple[Path, ...],
    hall_gate_path: Path,
    output_path: Path,
    omit_internal_length_categories: bool = False,
) -> None:
    if output_path.exists():
        raise ValueError("output must be new")
    hall_gate = json.loads(hall_gate_path.read_text())
    if (
        hall_gate.get("schema") != "row-merge-q4-adaptive-hall-path-analysis-v1"
        or hall_gate.get("status")
        != "ADAPTIVE_HALL_HOLE_PATH_HAS_FROZEN_COUNTERMODEL"
    ):
        raise AssertionError("adaptive Hall-path source is not the frozen gate")
    generic, non_generic, sources = collect_models(topology_path, ranked_paths)
    if non_generic != hall_gate["non_generic_models"]:
        raise AssertionError("generic-wall filter changed")
    expected_hashes = {
        record["post_values_sha256"] for record in hall_gate["models"]
    }
    if not expected_hashes <= {
        record["post_values_sha256"] for record in generic
    }:
        raise AssertionError("the frozen adaptive-gate corpus is no longer present")
    known_hashes = {record["post_values_sha256"] for record in generic}
    for path in extra_gate_paths:
        gate = json.loads(path.read_text())
        if (
            gate.get("schema") != "row-merge-q4-cycle023-gate-v1"
            or gate.get("solver_status") != "sat"
            or not gate.get("wall_graph_fixed")
            or gate.get("wall_values") is None
            or gate.get("post_wall_values") is None
            or not is_generic_model(gate["wall_values"], gate["post_wall_values"])
        ):
            raise AssertionError(f"extra gate is not an exact generic SAT model: {path}")
        post_hash = values_sha256(gate["post_wall_values"])
        if post_hash not in known_hashes:
            generic.append(
                {
                    "wall_values": gate["wall_values"],
                    "post_values": gate["post_wall_values"],
                    "wall_values_sha256": values_sha256(gate["wall_values"]),
                    "post_values_sha256": post_hash,
                    "provenance": [
                        {
                            "source": str(path),
                            "source_sha256": sha256(path),
                            "round": 0,
                            "corpus": "extra_generic_gate",
                        }
                    ],
                }
            )
            known_hashes.add(post_hash)
        sources.append({"path": str(path), "sha256": sha256(path)})
    generic.sort(key=lambda record: record["post_values_sha256"])
    sources.sort(key=lambda record: record["path"])

    indexed = actions_by_partition()
    if len(indexed) != 515:
        raise AssertionError("chain universe changed")
    category_names = [
        "all_chain",
        "all_paths",
        "all_cycles",
        "paths_touching_0",
        "paths_starting_0",
        "paths_ending_0",
        "paths_endpoint_0",
        "paths_with_0_internal",
        "paths_length_2_with_0_internal",
        "paths_length_3_with_0_internal",
        "hamiltonian_paths",
        "hamiltonian_paths_ending_0",
        "cycles_touching_0",
        "cycles_length_2",
        "cycles_length_3",
        "cycles_length_2_touching_0",
        "cycles_length_3_touching_0",
        "paths_ending_0_or_cycles_touching_0",
        "endpoint_0_paths_or_cycles_touching_0",
    ]
    if omit_internal_length_categories:
        category_names.remove("paths_length_2_with_0_internal")
        category_names.remove("paths_length_3_with_0_internal")
    category_names = tuple(category_names)
    category_coverage = Counter()
    hall_relaxation_coverage = Counter()
    topology_masks = Counter()
    models = []
    for model_index, model in enumerate(generic):
        values = model["post_values"]
        category_supports = {name: [] for name in category_names}
        ending_zero_signatures = []
        total_supporting_partitions = 0
        total_supporting_actions = 0
        supported_topologies = set()
        for partition, actions in indexed.items():
            count = matching_count(literal_graph(values, partition))
            if not count:
                continue
            total_supporting_partitions += 1
            for action in actions:
                total_supporting_actions += 1
                supported_topologies.add(
                    (action["kind"], tuple(action["vertices"]))
                )
                record = action_record(action, partition, count)
                for category in categories(action):
                    if category in category_supports:
                        category_supports[category].append(record)
                signature = reverse_hall_signature(values, action)
                if signature is not None:
                    ending_zero_signatures.append({**record, **signature})

        counts = {
            name: len(category_supports[name]) for name in category_names
        }
        for name, count in counts.items():
            if count:
                category_coverage[name] += 1
        hall_counts = {
            "strict_current_neighborhood": sum(
                record["outside_neighborhood_step_count"] == 0
                and record["no_omitting_witness_step_count"] == 0
                for record in ending_zero_signatures
            ),
            "one_outside_neighborhood_step": sum(
                record["outside_neighborhood_step_count"] <= 1
                and record["no_omitting_witness_step_count"] == 0
                for record in ending_zero_signatures
            ),
            "unrestricted_source_with_omitting_witness": sum(
                record["no_omitting_witness_step_count"] == 0
                for record in ending_zero_signatures
            ),
            "unrestricted_ending_zero_path": len(ending_zero_signatures),
        }
        for name, count in hall_counts.items():
            if count:
                hall_relaxation_coverage[name] += 1
        for topology in supported_topologies:
            topology_masks[topology] |= 1 << model_index
        models.append(
            {
                "post_values_sha256": model["post_values_sha256"],
                "provenance": model["provenance"],
                "was_strict_hall_failure": hall_counts[
                    "strict_current_neighborhood"
                ]
                == 0,
                "supporting_chain_partition_count": total_supporting_partitions,
                "supporting_chain_action_count": total_supporting_actions,
                "category_support_action_counts": counts,
                "hall_relaxation_support_action_counts": hall_counts,
                "minimum_outside_neighborhood_steps": (
                    min(
                        record["outside_neighborhood_step_count"]
                        for record in ending_zero_signatures
                        if record["no_omitting_witness_step_count"] == 0
                    )
                    if any(
                        record["no_omitting_witness_step_count"] == 0
                        for record in ending_zero_signatures
                    )
                    else None
                ),
                "sample_strict_hall_repair": next(
                    (
                        record
                        for record in ending_zero_signatures
                        if record["outside_neighborhood_step_count"] == 0
                        and record["no_omitting_witness_step_count"] == 0
                    ),
                    None,
                ),
                "sample_minimum_relaxed_repair": min(
                    ending_zero_signatures,
                    key=lambda record: (
                        record["no_omitting_witness_step_count"],
                        record["outside_neighborhood_step_count"],
                        record["length"],
                        record["vertices"],
                        record["goods"],
                    ),
                    default=None,
                ),
                "sample_any_chain_repair": next(
                    (
                        category_supports[name][0]
                        for name in category_names
                        if category_supports[name]
                    ),
                    None,
                ),
            }
        )

    model_count = len(models)
    full_mask = (1 << model_count) - 1
    topology_keys = tuple(sorted(topology_masks))
    minimum_topology_cover = None
    for size in range(1, 5):
        for cover in itertools.combinations(topology_keys, size):
            mask = 0
            for topology in cover:
                mask |= topology_masks[topology]
            if mask == full_mask:
                minimum_topology_cover = cover
                break
        if minimum_topology_cover is not None:
            break
    result = {
        "schema": SCHEMA,
        "status": "EXACT_HALL_PATH_RELAXATIONS_CLASSIFIED",
        "domain": "frozen exact integer models in one generic q=4 row-merge cell",
        "adaptive_hall_gate": str(hall_gate_path),
        "adaptive_hall_gate_sha256": sha256(hall_gate_path),
        "source_records": sources,
        "distinct_generic_model_count": model_count,
        "category_model_coverage": {
            name: category_coverage[name] for name in category_names
        },
        "hall_relaxation_model_coverage": {
            name: hall_relaxation_coverage[name]
            for name in (
                "strict_current_neighborhood",
                "one_outside_neighborhood_step",
                "unrestricted_source_with_omitting_witness",
                "unrestricted_ending_zero_path",
            )
        },
        "universal_categories": [
            name for name in category_names if category_coverage[name] == model_count
        ],
        "universal_hall_relaxations": [
            name
            for name in (
                "strict_current_neighborhood",
                "one_outside_neighborhood_step",
                "unrestricted_source_with_omitting_witness",
                "unrestricted_ending_zero_path",
            )
            if hall_relaxation_coverage[name] == model_count
        ],
        "topology_model_coverage": [
            {
                "kind": topology[0],
                "vertices": list(topology[1]),
                "covered_model_count": topology_masks[topology].bit_count(),
            }
            for topology in sorted(
                topology_keys,
                key=lambda topology: (
                    -topology_masks[topology].bit_count(),
                    topology,
                ),
            )
        ],
        "minimum_topology_cover_size": (
            len(minimum_topology_cover)
            if minimum_topology_cover is not None
            else None
        ),
        "minimum_topology_cover": [
            {
                "kind": topology[0],
                "vertices": list(topology[1]),
                "covered_model_count": topology_masks[topology].bit_count(),
            }
            for topology in minimum_topology_cover or ()
        ],
        "models": models,
        "interpretation": (
            "Coverage is exact only for the hash-bound finite corpus. The table "
            "locates which topology or Hall-source relaxation supplies at least "
            "one EFX-supporting chain action in each stored model."
        ),
        "claim_boundary": (
            "No universal category is a theorem. This analysis neither decides "
            "the full exchange-chain candidate nor proves complete additive EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topology", type=Path, required=True)
    parser.add_argument("--ranked", type=Path, action="append", required=True)
    parser.add_argument("--extra-gate", type=Path, action="append", default=[])
    parser.add_argument("--hall-gate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--omit-internal-length-categories", action="store_true")
    args = parser.parse_args()
    run(
        args.topology,
        tuple(args.ranked),
        tuple(args.extra_gate),
        args.hall_gate,
        args.output,
        args.omit_internal_length_categories,
    )


if __name__ == "__main__":
    main()
