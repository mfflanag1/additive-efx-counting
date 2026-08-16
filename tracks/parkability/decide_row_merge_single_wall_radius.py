#!/usr/bin/env python3
"""Search for additive single-wall states with no nearby partition pivot."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .core import iter_unlabeled_nonempty_partitions
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from core import iter_unlabeled_nonempty_partitions
    from lra_master import ParkabilityLRAMaster


SCHEMA = "row-merge-single-wall-radius-lra-v1"
N = 4
MATCHINGS = tuple(itertools.permutations(range(N)))


def canonical_partition(bundles):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in bundles))


def partition_neighbors(partition):
    neighbors = set()
    for source, bundle in enumerate(partition):
        if len(bundle) == 1:
            continue
        for good in bundle:
            for target in range(N):
                if target == source:
                    continue
                moved = [list(block) for block in partition]
                moved[source].remove(good)
                moved[target].append(good)
                neighbors.add(canonical_partition(moved))
    return tuple(sorted(neighbors))


def radius_partitions(partition, radius):
    start = canonical_partition(partition)
    distances = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if distances[current] == radius:
            continue
        for neighbor in partition_neighbors(current):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances


def make_bundles(sizes):
    u_size, w_size, c_size, d_size = sizes
    cursor = 0
    u = tuple(range(cursor, cursor + u_size))
    cursor += u_size
    w = tuple(range(cursor, cursor + w_size))
    cursor += w_size
    good = cursor
    cursor += 1
    c = tuple(range(cursor, cursor + c_size))
    cursor += c_size
    d = tuple(range(cursor, cursor + d_size))
    cursor += d_size
    return (u, (*w, good), c, d), w, good, cursor


def zsum(row, bundle):
    if not bundle:
        return z3.RealVal(0)
    if len(bundle) == 1:
        return row[bundle[0]]
    return z3.Sum(*(row[good] for good in bundle))


def edge_expression(row, partition, own_index):
    own = zsum(row, partition[own_index])
    return z3.And(
        *(
            own >= zsum(row, tuple(g for g in target if g != removed))
            for target_index, target in enumerate(partition)
            if target_index != own_index
            for removed in target
        )
    )


def edge_matrix(solver, rows, partition, prefix):
    edges = tuple(
        tuple(z3.Bool(f"{prefix}_a{agent}_b{bundle}") for bundle in range(N))
        for agent in range(N)
    )
    for agent in range(N):
        for bundle in range(N):
            solver.add(
                edges[agent][bundle]
                == edge_expression(rows[agent], partition, bundle)
            )
    return edges


def has_matching_expression(edges, agents=range(N), bundles=range(N)):
    agents = tuple(agents)
    bundles = tuple(bundles)
    if len(agents) > len(bundles):
        return z3.BoolVal(False)
    return z3.Or(
        *(
            z3.And(
                *(edges[agent][matching[index]] for index, agent in enumerate(agents))
            )
            for matching in itertools.permutations(bundles, len(agents))
        )
    )


def disjoint_subset_pairs(m):
    pairs = []
    for labels in itertools.product(range(3), repeat=m):
        left = tuple(good for good, label in enumerate(labels) if label == 1)
        right = tuple(good for good, label in enumerate(labels) if label == 2)
        if left and right and left < right:
            pairs.append((left, right))
    return tuple(pairs)


def as_fraction(model, expression):
    value = model.eval(expression, model_completion=True)
    if z3.is_int_value(value):
        return Fraction(value.as_long())
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def primitive_rows(wall_rows, post_row):
    converted_wall = []
    converted_post = None
    for agent, row in enumerate(wall_rows):
        combined = (*row, *post_row) if agent == 0 else row
        denominator = math.lcm(*(value.denominator for value in combined))
        integers = [int(value * denominator) for value in combined]
        divisor = math.gcd(*integers)
        integers = [value // divisor for value in integers]
        converted_wall.append(tuple(integers[: len(row)]))
        if agent == 0:
            converted_post = tuple(integers[len(row) :])
    return tuple(converted_wall), converted_post


def literal_edge(row, partition, own_index):
    own = sum(row[good] for good in partition[own_index])
    return all(
        own >= sum(row[good] for good in target if good != removed)
        for target_index, target in enumerate(partition)
        if target_index != own_index
        for removed in target
    )


def literal_graph(values, partition):
    return tuple(
        tuple(literal_edge(values[agent], partition, bundle) for bundle in range(N))
        for agent in range(N)
    )


def matching_count(graph):
    return sum(
        all(graph[agent][matching[agent]] for agent in range(N))
        for matching in MATCHINGS
    )


def partition_distance(left, right):
    retained = max(
        sum(len(set(left[index]) & set(right[permutation[index]])) for index in range(N))
        for permutation in MATCHINGS
    )
    return sum(map(len, left)) - retained


def audit_model(
    wall_values,
    post_values,
    original,
    w,
    critical_good,
    perturb_good,
    radius,
):
    wall_graph = literal_graph(wall_values, original)
    post_graph = literal_graph(post_values, original)
    changed_edges = tuple(
        (agent, bundle, wall_graph[agent][bundle], post_graph[agent][bundle])
        for agent in range(N)
        for bundle in range(N)
        if wall_graph[agent][bundle] != post_graph[agent][bundle]
    )
    if changed_edges != ((0, 0, True, False),):
        raise AssertionError(f"wall crossing changed unexpected edges: {changed_edges}")
    if any(not wall_graph[agent][agent] for agent in range(N)):
        raise AssertionError("the designated wall allocation is not EFX")
    neighborhood = radius_partitions(original, radius)
    if any(
        matching_count(literal_graph(post_values, partition))
        for partition in neighborhood
    ):
        raise AssertionError("the model gained an EFX partition inside the radius")

    support_count = 0
    allocation_count = 0
    minimum_distance = None
    distance_histogram = Counter()
    nearest = None
    m = len(post_values[0])
    for partition in iter_unlabeled_nonempty_partitions(N, m):
        graph = literal_graph(post_values, partition)
        count = matching_count(graph)
        if not count:
            continue
        distance = partition_distance(canonical_partition(original), partition)
        support_count += 1
        allocation_count += count
        distance_histogram[distance] += 1
        if minimum_distance is None or (distance, partition) < (
            minimum_distance,
            nearest,
        ):
            minimum_distance = distance
            nearest = partition
    if minimum_distance is None:
        raise AssertionError("an additive EFX counterexample was found; audit separately")
    if minimum_distance <= radius:
        raise AssertionError("global distance audit disagrees with the solver obstruction")

    u = original[0]
    if sum(wall_values[0][good] for good in u) != sum(
        wall_values[0][good] for good in w
    ):
        raise AssertionError("critical wall equality was lost")
    if post_values[0][perturb_good] <= wall_values[0][perturb_good]:
        raise AssertionError("post-wall perturbation has the wrong direction")
    return {
        "wall_feasibility_graph": [list(row) for row in wall_graph],
        "post_feasibility_graph": [list(row) for row in post_graph],
        "changed_original_partition_edges": [list(item) for item in changed_edges],
        "radius_partition_count": len(neighborhood),
        "complete_efx_supporting_partition_count": support_count,
        "complete_efx_allocation_count": allocation_count,
        "minimum_supporting_partition_transfer_distance": minimum_distance,
        "supporting_partition_transfer_distance_histogram": {
            str(distance): distance_histogram[distance]
            for distance in sorted(distance_histogram)
        },
        "nearest_supporting_partition": [list(bundle) for bundle in nearest],
        "nearest_supporting_partition_graph": [
            list(row) for row in literal_graph(post_values, nearest)
        ],
    }


def run(
    result_path,
    smt2_path,
    sizes,
    witness_size,
    radius,
    time_limit,
    skip_global_wall_isolation=False,
):
    if result_path.exists() or smt2_path.exists():
        raise ValueError("result and SMT2 output paths must not exist")
    if any(size < 1 for size in sizes):
        raise ValueError("all four noncritical bundle sizes must be positive")
    original, w, critical_good, m = make_bundles(sizes)
    u = original[0]
    transferred = canonical_partition(((*u, critical_good), w, original[2], original[3]))
    candidates = radius_partitions(original, radius)

    master = ParkabilityLRAMaster(N, m)
    solver = master.solver
    wall_rows = master.values
    epsilon = z3.Real("wall_epsilon")
    solver.add(epsilon > 0)
    perturb_good = w[0]
    post_row = tuple(
        value + epsilon if good == perturb_good else value
        for good, value in enumerate(wall_rows[0])
    )
    post_rows = (post_row, *wall_rows[1:])

    solver.add(zsum(wall_rows[0], u) == zsum(wall_rows[0], w))
    solver.add(
        *(wall_rows[0][critical_good] < wall_rows[0][good] for good in w)
    )
    for target_index, target in enumerate(original):
        if target_index == 0:
            continue
        for removed in target:
            remainder = tuple(good for good in target if good != removed)
            if target_index == 1 and removed == critical_good:
                continue
            solver.add(zsum(wall_rows[0], u) > zsum(wall_rows[0], remainder))

    if not skip_global_wall_isolation:
        critical_pair = {tuple(sorted((u, w)))}
        for left, right in disjoint_subset_pairs(m):
            if tuple(sorted((left, right))) in critical_pair:
                continue
            wall_left = zsum(wall_rows[0], left)
            wall_right = zsum(wall_rows[0], right)
            post_left = zsum(post_row, left)
            post_right = zsum(post_row, right)
            solver.add(wall_left != wall_right)
            solver.add(
                z3.Or(
                    z3.And(wall_left > wall_right, post_left > post_right),
                    z3.And(wall_left < wall_right, post_left < post_right),
                )
            )

    wall_edges = edge_matrix(solver, wall_rows, original, "wall_original")
    post_edges = edge_matrix(solver, post_rows, original, "post_original")
    solver.add(*(wall_edges[agent][agent] for agent in range(N)))
    solver.add(z3.Not(post_edges[0][0]))
    if skip_global_wall_isolation:
        solver.add(
            *(post_edges[0][bundle] == wall_edges[0][bundle] for bundle in range(1, N))
        )

    deficient_agents = tuple(range(witness_size))
    deficient_bundles = tuple(range(1, witness_size))
    for agent in deficient_agents:
        for bundle in range(N):
            if bundle not in deficient_bundles:
                solver.add(z3.Not(post_edges[agent][bundle]))
    for size in range(1, witness_size):
        for agents in itertools.combinations(deficient_agents, size):
            solver.add(
                has_matching_expression(post_edges, agents, deficient_bundles)
            )

    for index, partition in enumerate(sorted(candidates)):
        edges = edge_matrix(solver, post_rows, partition, f"candidate_{index}")
        solver.add(z3.Not(has_matching_expression(edges)))

    solver.set(timeout=int(time_limit * 1000))
    started = time.time()
    status = solver.check()
    elapsed = time.time() - started
    model = solver.model() if status == z3.sat else None
    audit = None
    wall_values = None
    post_values = None
    scaled_epsilon = None
    if model is not None:
        wall_fractions = tuple(
            tuple(as_fraction(model, value) for value in row) for row in wall_rows
        )
        epsilon_fraction = as_fraction(model, epsilon)
        post_fraction = tuple(
            value + (epsilon_fraction if good == perturb_good else 0)
            for good, value in enumerate(wall_fractions[0])
        )
        wall_values, post_row_values = primitive_rows(wall_fractions, post_fraction)
        post_values = (post_row_values, *wall_values[1:])
        scaled_epsilon = post_row_values[perturb_good] - wall_values[0][perturb_good]
        audit = audit_model(
            wall_values,
            post_values,
            original,
            w,
            critical_good,
            perturb_good,
            radius,
        )

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": (
            "RADIUS_PIVOT_REFUTATION_FOUND"
            if status == z3.sat
            else "UNSAT_CANDIDATE"
            if status == z3.unsat
            else "MASTER_UNKNOWN"
        ),
        "solver_status": str(status),
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
        "domain": "strictly positive additive real valuations",
        "n": N,
        "m": m,
        "bundle_sizes_excluding_critical_good": list(sizes),
        "minimal_hall_witness_size": witness_size,
        "obstructed_transfer_radius": radius,
        "wall_partition": [list(bundle) for bundle in original],
        "critical_wall": {
            "moving_bundle_u": list(u),
            "envied_remainder_w": list(w),
            "critical_good": critical_good,
            "perturbed_good": perturb_good,
            "transferred_partition": [list(bundle) for bundle in transferred],
        },
        "wall_values": [list(row) for row in wall_values] if wall_values else None,
        "post_wall_values": [list(row) for row in post_values] if post_values else None,
        "scaled_wall_epsilon": scaled_epsilon,
        "audit": audit,
        "candidate_partition_count": len(candidates),
        "candidate_partition_count_by_radius": {
            str(distance): sum(value == distance for value in candidates.values())
            for distance in range(radius + 1)
        },
        "global_wall_isolation": not skip_global_wall_isolation,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "smt2_path": str(smt2_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "SAT refutes the claim that every generic essential single-wall "
            f"failure has an EFX partition within transfer radius {radius}. "
            "It is not an EFX counterexample unless the global EFX count is zero."
            if status == z3.sat
            else "UNSAT excludes such a local-radius obstruction in this exact "
            "Hall-size and bundle-shape cell; independent solver replay is required."
            if status == z3.unsat
            else "The exact-real master reached its resource boundary without a "
            "model or an infeasibility proof."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument(
        "--bundle-sizes",
        default="2,1,2,1",
        help="sizes of U,W,C,D before adding the critical good to W",
    )
    parser.add_argument("--witness-size", type=int, choices=(2, 3, 4), required=True)
    parser.add_argument("--radius", type=int, choices=range(5), default=1)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--skip-global-wall-isolation", action="store_true")
    args = parser.parse_args()
    sizes = tuple(int(value) for value in args.bundle_sizes.split(","))
    if len(sizes) != 4:
        parser.error("--bundle-sizes must contain four comma-separated integers")
    if args.time_limit < 0:
        parser.error("--time-limit cannot be negative")
    run(
        args.result,
        args.smt2,
        sizes,
        args.witness_size,
        args.radius,
        args.time_limit,
        args.skip_global_wall_isolation,
    )


if __name__ == "__main__":
    main()
