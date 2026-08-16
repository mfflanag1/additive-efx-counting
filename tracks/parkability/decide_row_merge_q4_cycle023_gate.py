#!/usr/bin/env python3
"""Decide the mined 0→2→3→0 exchange-cycle menu in one q=4 wall cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import canonical
    from .decide_row_merge_q4_small_step_pivot import pair_pivots
    from .decide_row_merge_single_wall_radius import (
        as_fraction,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        zsum,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_row_merge_q4_exchange_chain_cegar import (
        add_partition_obstruction,
        complete_audit,
    )
except ImportError:
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import canonical
    from decide_row_merge_q4_small_step_pivot import pair_pivots
    from decide_row_merge_single_wall_radius import (
        as_fraction,
        edge_matrix,
        has_matching_expression,
        literal_graph,
        make_bundles,
        matching_count,
        primitive_rows,
        zsum,
    )
    from lra_master import ParkabilityLRAMaster
    from run_row_merge_q4_exchange_chain_cegar import (
        add_partition_obstruction,
        complete_audit,
    )


SCHEMA = "row-merge-q4-cycle023-gate-v1"
N = 4
CYCLE_VERTICES = (0, 2, 3)
REVERSE_CYCLE_VERTICES = (0, 3, 2)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cycle_partitions(base, vertex_orders) -> tuple[tuple[tuple[int, ...], ...], ...]:
    found = set()
    for vertices in vertex_orders:
        edges = tuple(
            (
                vertices[index],
                vertices[(index + 1) % len(vertices)],
            )
            for index in range(len(vertices))
        )
        for goods in itertools.product(*(base[source] for source, _target in edges)):
            moved = [list(bundle) for bundle in base]
            for (source, target), good in zip(edges, goods):
                moved[source].remove(good)
                moved[target].append(good)
            found.add(canonical(moved))
    return tuple(sorted(found))


def path_partitions(base, start: int, end: int) -> tuple:
    found = set()
    internal_vertices = tuple(vertex for vertex in range(N) if vertex not in {start, end})
    for internal_count in (0, 1, 2):
        for internal in itertools.permutations(internal_vertices, internal_count):
            vertices = (start, *internal, end)
            edges = tuple(zip(vertices[:-1], vertices[1:]))
            for goods in itertools.product(*(base[source] for source, _target in edges)):
                moved = [list(bundle) for bundle in base]
                for (source, target), good in zip(edges, goods):
                    moved[source].remove(good)
                    moved[target].append(good)
                found.add(canonical(moved))
    return tuple(sorted(found))


def run(
    result_path: Path,
    formula_path: Path,
    fixed_graph_source_path: Path,
    time_limit: float,
    obstruction_encoding: str,
    block_base_pivots: bool,
    integer_upper: int | None,
    both_cycle_orientations: bool,
    path_start3_end2: bool,
    all_three_cycles: bool,
    all_three_cycles_touching0: bool,
    all_paths_start3: bool,
    all_hamiltonian_paths: bool,
    topology_cover_source_path: Path | None,
    fix_wall_graph: bool,
) -> None:
    if result_path.exists() or formula_path.exists():
        raise ValueError("result and formula outputs must be new")
    if time_limit <= 0 or (integer_upper is not None and integer_upper < 1):
        raise ValueError("time limit must be positive")
    if (
        sum(
            (
                both_cycle_orientations,
                path_start3_end2,
                all_three_cycles,
                all_three_cycles_touching0,
                all_paths_start3,
                all_hamiltonian_paths,
                topology_cover_source_path is not None,
            )
        )
        > 1
    ):
        raise ValueError("select at most one expanded exchange menu")
    sizes = (2, 1, 2, 3)
    original, w, critical_good, m = make_bundles(sizes)
    if original != ((0, 1), (2, 3), (4, 5), (6, 7, 8)):
        raise AssertionError("wall partition changed")
    u = original[0]
    perturb_good = w[0]
    small_step_goods = tuple(good for bundle in original[2:] for good in bundle)

    fixed_source = json.loads(fixed_graph_source_path.read_text())
    if (
        fixed_source.get("schema") != "row-merge-q4-exchange-chain-cegar-v1"
        or fixed_source.get("m") != m
    ):
        raise ValueError("fixed graph source describes another cell")
    sat_rounds = [
        record
        for record in fixed_source["rounds"]
        if record.get("solver_status") == "sat"
    ]
    if not sat_rounds:
        raise ValueError("fixed graph source has no SAT model")
    fixed_wall_values = tuple(
        tuple(row) for row in sat_rounds[-1]["wall_values"]
    )
    fixed_values = tuple(tuple(row) for row in sat_rounds[-1]["post_wall_values"])
    fixed_wall_graph = literal_graph(fixed_wall_values, original)
    fixed_graph = literal_graph(fixed_values, original)

    master = ParkabilityLRAMaster(N, m, integer_upper=integer_upper)
    solver = master.solver
    wall_rows = master.values
    epsilon = (
        z3.Int("wall_epsilon")
        if integer_upper is not None
        else z3.Real("wall_epsilon")
    )
    solver.add(epsilon > 0)
    post_row = tuple(
        value + epsilon if good == perturb_good else value
        for good, value in enumerate(wall_rows[0])
    )
    post_rows = (post_row, *wall_rows[1:])

    solver.add(zsum(wall_rows[0], u) == zsum(wall_rows[0], w))
    solver.add(wall_rows[0][critical_good] < wall_rows[0][w[0]])
    for target_index, target in enumerate(original):
        if target_index == 0:
            continue
        for removed in target:
            remainder = tuple(good for good in target if good != removed)
            if target_index == 1 and removed == critical_good:
                continue
            solver.add(zsum(wall_rows[0], u) > zsum(wall_rows[0], remainder))
    solver.add(*(epsilon < wall_rows[0][good] for good in small_step_goods))

    wall_edges = edge_matrix(solver, wall_rows, original, "wall_original")
    post_edges = edge_matrix(solver, post_rows, original, "post_original")
    solver.add(*(wall_edges[agent][agent] for agent in range(N)))
    solver.add(z3.Not(post_edges[0][0]))
    deficient_bundles = tuple(range(1, N))
    for agent in range(N):
        solver.add(z3.Not(post_edges[agent][0]))
    for size in range(1, N):
        for agents in itertools.combinations(range(N), size):
            solver.add(has_matching_expression(post_edges, agents, deficient_bundles))
    for agent in range(N):
        for bundle in range(N):
            solver.add(post_edges[agent][bundle] == fixed_graph[agent][bundle])
            if fix_wall_graph:
                solver.add(
                    wall_edges[agent][bundle]
                    == fixed_wall_graph[agent][bundle]
                )

    if all_three_cycles or all_three_cycles_touching0:
        vertex_orders = tuple(
            order
            for vertices in itertools.combinations(range(N), 3)
            if not all_three_cycles_touching0 or 0 in vertices
            for order in (
                vertices,
                (vertices[0], vertices[2], vertices[1]),
            )
        )
    else:
        vertex_orders = (
            (CYCLE_VERTICES, REVERSE_CYCLE_VERTICES)
            if both_cycle_orientations
            else (CYCLE_VERTICES,)
        )
    path_menu = path_start3_end2 or all_paths_start3 or all_hamiltonian_paths
    topology_cover_menu = topology_cover_source_path is not None
    topology_cover_source_sha256 = None
    topology_cover_records = None
    if topology_cover_source_path is not None:
        topology_cover_source = json.loads(topology_cover_source_path.read_text())
        source_schema = topology_cover_source.get("schema")
        if source_schema == "row-merge-q4-chain-trace-analysis-v1":
            if tuple(
                tuple(row)
                for row in topology_cover_source.get("fixed_post_wall_graph", ())
            ) != fixed_graph:
                raise ValueError("topology cover source describes another cell")
            menu = tuple(
                tuple(tuple(bundle) for bundle in partition)
                for partition in topology_cover_source[
                    "minimum_topology_cover_partitions"
                ]
            )
            expected_cover_count = topology_cover_source[
                "minimum_topology_cover_partition_count"
            ]
            menu_kind = "minimum_trace_topology_cover"
        elif source_schema == "row-merge-q4-hall-path-relaxation-analysis-v1":
            try:
                from .analyze_row_merge_q4_chain_trace import actions_by_partition
            except ImportError:
                from analyze_row_merge_q4_chain_trace import actions_by_partition
            topology_cover_records = topology_cover_source[
                "minimum_topology_cover"
            ]
            selected_topologies = {
                (record["kind"], tuple(record["vertices"]))
                for record in topology_cover_records
            }
            if (
                topology_cover_source.get("distinct_generic_model_count") < 1
                or len(selected_topologies)
                != topology_cover_source["minimum_topology_cover_size"]
            ):
                raise ValueError("relaxation topology cover is malformed")
            menu = tuple(
                sorted(
                    partition
                    for partition, actions in actions_by_partition().items()
                    if any(
                        (action["kind"], tuple(action["vertices"]))
                        in selected_topologies
                        for action in actions
                    )
                )
            )
            expected_cover_count = len(menu)
            menu_kind = "minimum_hall_relaxation_trace_topology_cover"
        else:
            raise ValueError("unsupported topology cover source")
        if (
            not menu
            or len(menu) != expected_cover_count
            or len(set(menu)) != len(menu)
        ):
            raise AssertionError("minimum topology cover changed")
        topology_cover_source_sha256 = sha256(topology_cover_source_path)
        topology_cover_records = topology_cover_source["minimum_topology_cover"]
    elif all_hamiltonian_paths:
        try:
            from .analyze_row_merge_q4_chain_trace import actions_by_partition
        except ImportError:
            from analyze_row_merge_q4_chain_trace import actions_by_partition
        menu = tuple(
            sorted(
                partition
                for partition, actions in actions_by_partition().items()
                if any(
                    action["kind"] == "path"
                    and action["length"] == N - 1
                    for action in actions
                )
            )
        )
        if len(menu) != 264:
            raise AssertionError("Hamiltonian-path menu changed")
        menu_kind = "all_oriented_hamiltonian_paths"
    elif all_paths_start3:
        menu_set = set()
        for end in range(N - 1):
            menu_set.update(path_partitions(original, 3, end))
        menu = tuple(sorted(menu_set))
        if len(menu) != 117:
            raise AssertionError("all-paths-from-3 menu changed")
        menu_kind = "all_paths_starting_at_3_of_length_1_to_3"
    elif path_start3_end2:
        menu = path_partitions(original, 3, 2)
        if len(menu) != 39:
            raise AssertionError("path menu changed")
        menu_kind = "paths_starting_at_3_and_ending_at_2_of_length_1_to_3"
    else:
        menu = cycle_partitions(original, vertex_orders)
        expected_cycle_count = (
            80
            if all_three_cycles
            else 56
            if all_three_cycles_touching0
            else 12 * len(vertex_orders)
        )
        if len(menu) != expected_cycle_count:
            raise AssertionError("cycle menu changed")
        menu_kind = (
            "all_three_cycles"
            if all_three_cycles
            else "all_three_cycles_touching_bundle_0"
            if all_three_cycles_touching0
            else "three_cycles"
        )
    for index, partition in enumerate(menu):
        edges = edge_matrix(solver, post_rows, partition, f"cycle023_{index}")
        add_partition_obstruction(
            solver,
            edges,
            f"cycle023_{index}",
            obstruction_encoding,
        )
    base_pivots = pair_pivots(original, w, critical_good, complete_bundle_menu=True)
    if block_base_pivots:
        for index, partition in enumerate(base_pivots):
            edges = edge_matrix(solver, post_rows, partition, f"base_pivot_{index}")
            add_partition_obstruction(
                solver,
                edges,
                f"base_pivot_{index}",
                obstruction_encoding,
            )

    solver.set(timeout=int(time_limit * 1000))
    started = time.time()
    status = solver.check()
    elapsed = time.time() - started
    wall_values = None
    post_values = None
    global_audit = None
    chain_support_count = None
    pair_pivot_support_count = None
    if status == z3.sat:
        model = solver.model()
        wall_fractions = tuple(
            tuple(as_fraction(model, value) for value in row) for row in wall_rows
        )
        post_fractions = tuple(as_fraction(model, value) for value in post_row)
        wall_values, post_values_row = primitive_rows(wall_fractions, post_fractions)
        post_values = (post_values_row, *wall_values[1:])
        if literal_graph(post_values, original) != fixed_graph:
            raise AssertionError("decoded model left the fixed graph cell")
        if any(matching_count(literal_graph(post_values, partition)) for partition in menu):
            raise AssertionError("decoded model failed a selected-menu obstruction")
        global_audit = complete_audit(post_values, original)
        all_chain = set()
        try:
            from .analyze_row_merge_q4_distance3_exchange import (
                exchange_chain_partitions,
            )
        except ImportError:
            from analyze_row_merge_q4_distance3_exchange import (
                exchange_chain_partitions,
            )
        all_chain.update(exchange_chain_partitions(original, 3))
        chain_support_count = sum(
            bool(matching_count(literal_graph(post_values, partition)))
            for partition in all_chain
        )
        pair_pivot_support_count = sum(
            bool(matching_count(literal_graph(post_values, partition)))
            for partition in base_pivots
        )
        if block_base_pivots and pair_pivot_support_count:
            raise AssertionError("decoded model failed a base-pivot obstruction")

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    if topology_cover_menu:
        status_label = (
            "TOPOLOGY_COVER_PLUS_BASE_CELL_VERIFIED"
            if status == z3.unsat
            else "TOPOLOGY_COVER_PLUS_BASE_REFUTATION_FOUND"
            if status == z3.sat
            else "TOPOLOGY_COVER_GATE_INCOMPLETE"
        )
        interpretation = (
            "UNSAT proves that one of the base pivots or a partition in the "
            "hash-bound minimum trace-topology cover supports complete EFX "
            "in the fixed wall cell."
            if status == z3.unsat
            else "SAT exactly refutes the combined base-pivot and minimum "
            "trace-topology cover menu."
            if status == z3.sat
            else "The exact-real topology-cover gate reached its solver limit."
        )
    elif path_menu:
        status_label = (
            "PATH_START3_PLUS_BASE_CELL_VERIFIED"
            if status == z3.unsat
            else "PATH_START3_PLUS_BASE_REFUTATION_FOUND"
            if status == z3.sat
            else "PATH_START3_GATE_INCOMPLETE"
        )
        path_description = (
            "an oriented Hamiltonian path"
            if all_hamiltonian_paths
            else
            "a length-one-to-three path from bundle 3"
            if all_paths_start3
            else "a length-one-to-three path from bundle 3 to bundle 2"
        )
        interpretation = (
            f"UNSAT proves that one of the base pivots or {path_description} "
            "supports complete EFX in the fixed wall cell."
            if status == z3.unsat
            else "SAT exactly refutes the combined base-pivot and selected "
            "path menu."
            if status == z3.sat
            else "The exact-real path gate reached its solver limit."
        )
    else:
        status_label = (
            "CYCLE023_PLUS_BASE_CELL_VERIFIED"
            if status == z3.unsat and block_base_pivots
            else "CYCLE023_CELL_VERIFIED"
            if status == z3.unsat
            else "CYCLE023_PLUS_BASE_REFUTATION_FOUND"
            if status == z3.sat and block_base_pivots
            else "CYCLE023_REFUTATION_FOUND"
            if status == z3.sat
            else "CYCLE023_GATE_INCOMPLETE"
        )
        orientation_word = "oriented cycles" if len(vertex_orders) > 1 else "cycle"
        interpretation = (
            f"UNSAT proves that one of the base pivots or selected {orientation_word} "
            "supports complete EFX in the fixed wall cell."
            if status == z3.unsat and block_base_pivots
            else f"UNSAT proves that one of the selected {orientation_word} supports "
            "complete EFX in the fixed wall cell."
            if status == z3.unsat
            else f"SAT exactly refutes the combined base-pivot and {orientation_word} "
            "menu."
            if status == z3.sat and block_base_pivots
            else f"SAT exactly refutes the selected {orientation_word} menu."
            if status == z3.sat
            else "The exact-real cycle gate reached its solver limit."
        )
    result = {
        "schema": SCHEMA,
        "status": status_label,
        "solver_status": str(status),
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
        "solver_wall_seconds": elapsed,
        "domain": (
            "positive additive integer wall valuations with each wall item "
            f"in 1..{integer_upper}; the perturbed post-wall entry may exceed "
            "the wall cap"
            if integer_upper is not None
            else "strictly positive additive real valuations"
        ),
        "n": N,
        "m": m,
        "wall_partition": [list(bundle) for bundle in original],
        "cycle_vertices": list(CYCLE_VERTICES) if len(vertex_orders) == 1 else None,
        "cycle_vertex_orders": [list(vertices) for vertices in vertex_orders],
        "cycle_edge_orders": [
            [
                [vertices[index], vertices[(index + 1) % len(vertices)]]
                for index in range(len(vertices))
            ]
            for vertices in vertex_orders
        ],
        "menu_kind": menu_kind,
        "cycle_partition_count": (
            len(menu) if not path_menu and not topology_cover_menu else None
        ),
        "cycle_partitions": (
            [[list(bundle) for bundle in partition] for partition in menu]
            if not path_menu and not topology_cover_menu
            else None
        ),
        "path_start": 3 if path_menu and not all_hamiltonian_paths else None,
        "path_end": 2 if path_start3_end2 else None,
        "path_lengths": (
            [3]
            if all_hamiltonian_paths
            else [1, 2, 3]
            if path_menu
            else None
        ),
        "path_partition_count": len(menu) if path_menu else None,
        "path_partitions": (
            [[list(bundle) for bundle in partition] for partition in menu]
            if path_menu
            else None
        ),
        "topology_cover_source": (
            str(topology_cover_source_path)
            if topology_cover_source_path is not None
            else None
        ),
        "topology_cover_source_sha256": topology_cover_source_sha256,
        "topology_cover_records": topology_cover_records,
        "topology_cover_partition_count": len(menu) if topology_cover_menu else None,
        "topology_cover_partitions": (
            [[list(bundle) for bundle in partition] for partition in menu]
            if topology_cover_menu
            else None
        ),
        "obstruction_encoding": obstruction_encoding,
        "integer_upper": integer_upper,
        "base_pivots_blocked": block_base_pivots,
        "base_pivot_partition_count": len(base_pivots),
        "combined_partition_count": len(set(menu) | set(base_pivots)),
        "fixed_post_wall_graph": [list(row) for row in fixed_graph],
        "fixed_wall_graph": (
            [list(row) for row in fixed_wall_graph]
            if fix_wall_graph
            else None
        ),
        "wall_graph_fixed": fix_wall_graph,
        "fixed_graph_source": str(fixed_graph_source_path),
        "fixed_graph_source_sha256": sha256(fixed_graph_source_path),
        "wall_values": [list(row) for row in wall_values] if wall_values else None,
        "post_wall_values": [list(row) for row in post_values] if post_values else None,
        "complete_efx_audit": global_audit,
        "simple_chain_support_count": chain_support_count,
        "pair_pivot_support_count": pair_pivot_support_count,
        "formula": str(formula_path),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": interpretation,
        "claim_boundary": (
            (
                "A bounded-integer verdict applies only to the stated wall "
                "cap. "
                if integer_upper is not None
                else ""
            )
            + "This decides only the displayed fixed nine-good Hall-size-four "
            "cell. It is not general row-merge continuation or complete EFX."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--fixed-graph-source", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=180.0)
    parser.add_argument(
        "--obstruction-encoding",
        choices=("matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument("--block-base-pivots", action="store_true")
    parser.add_argument("--integer-upper", type=int)
    parser.add_argument("--both-cycle-orientations", action="store_true")
    parser.add_argument("--path-start3-end2", action="store_true")
    parser.add_argument("--all-three-cycles", action="store_true")
    parser.add_argument("--all-three-cycles-touching0", action="store_true")
    parser.add_argument("--all-paths-start3", action="store_true")
    parser.add_argument("--all-hamiltonian-paths", action="store_true")
    parser.add_argument("--topology-cover-source", type=Path)
    parser.add_argument("--fix-wall-graph", action="store_true")
    args = parser.parse_args()
    run(
        args.result,
        args.formula,
        args.fixed_graph_source,
        args.time_limit,
        args.obstruction_encoding,
        args.block_base_pivots,
        args.integer_upper,
        args.both_cycle_orientations,
        args.path_start3_end2,
        args.all_three_cycles,
        args.all_three_cycles_touching0,
        args.all_paths_start3,
        args.all_hamiltonian_paths,
        args.topology_cover_source,
        args.fix_wall_graph,
    )


if __name__ == "__main__":
    main()
