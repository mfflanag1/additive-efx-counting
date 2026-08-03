#!/usr/bin/env python3
"""CEGAR for a globally threshold-maximal blocked five-token orbit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np
import z3

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import audit_orbit, bundles_from_masks
    from .audit_threshold_plateau_exact_paths import (
        exact_best_hall_margin,
        mask_threshold,
        mask_value,
    )
    from .decide_threshold_hall_local_gradient import (
        integer_values,
        total,
    )
    from .fast_count import FastParkability
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import audit_orbit, bundles_from_masks
    from audit_threshold_plateau_exact_paths import (
        exact_best_hall_margin,
        mask_threshold,
        mask_value,
    )
    from decide_threshold_hall_local_gradient import (
        integer_values,
        total,
    )
    from fast_count import FastParkability


SCHEMA = "minimum-slot-orbit-global-threshold-cegar-v1"
BASE = ((0, 1), (2, 3), (4, 5), (6, 7))
CORES = (0, 2, 4, 6)
TOKENS = (1, 3, 5, 7, 8)
PAIR_HALL_CYCLE = ((0, 3), (0, 1), (1, 2), (2, 3))
FLOATER = 8


def masks_from_bundles(bundles):
    return tuple(
        sum(1 << good for good in bundle)
        for bundle in bundles
    )


def threshold_terms(row, bundle):
    return tuple(
        total(row, tuple(good for good in bundle if good != removed))
        for removed in bundle
    )


def eligible(values, bundles, floater):
    constraints = []
    for observer in range(4):
        own = total(values[observer], bundles[observer])
        constraints.append(own >= values[observer][floater])
        constraints.extend(
            own >= term
            for target in range(4)
            if target != observer
            for term in threshold_terms(values[observer], bundles[target])
        )
    return z3.And(*constraints)


def owner_cores_dominate_floater(values):
    return z3.And(
        *(
            values[owner][core] >= values[owner][FLOATER]
            for owner, core in enumerate(CORES)
        )
    )


def owner_cores_dominate_predecessor_tokens(values):
    return z3.And(
        *(
            values[owner][core] >= values[owner][(2 * owner - 1) % 8]
            for owner, core in enumerate(CORES)
        )
    )


def pair_hall_cross_row_core_clause(values, family, shift):
    if family not in {"a", "b"} or shift not in range(4):
        raise ValueError("cross-row clause requires family a/b and shift in [0,3]")

    def owner(agent):
        return (agent + shift) % 4

    def good(item):
        return (item + 2 * shift) % 8 if item < 8 else item

    if family == "a":
        return z3.Or(
            values[owner(0)][good(0)] >= values[owner(0)][good(3)],
            values[owner(2)][good(2)]
            <= values[owner(2)][good(3)] + values[owner(2)][good(4)],
        )
    return z3.Or(
        values[owner(3)][good(1)]
        <= values[owner(3)][good(3)] + values[owner(3)][good(6)],
        values[owner(0)][good(1)] + values[owner(0)][good(4)]
        >= values[owner(0)][good(3)] + values[owner(0)][good(8)],
    )


def pair_hall_cross_row_core_clauses(values):
    return z3.And(
        *(
            pair_hall_cross_row_core_clause(values, family, shift)
            for shift in range(4)
            for family in ("a", "b")
        )
    )


def theta_upper_bound(values, bundles, bound):
    choices = tuple(
        threshold_terms(values[owner], bundles[owner])
        for owner in range(4)
    )
    return z3.And(
        *(
            z3.Sum(*terms) <= bound
            for terms in itertools.product(*choices)
        )
    )


def complete_failure(values, bundles, floater, host, permutation):
    complete = list(bundles)
    complete[host] = tuple(sorted((*complete[host], floater)))
    failures = []
    for observer in range(4):
        assigned = permutation[observer]
        failures.extend(
            total(values[observer], complete[assigned])
            < term
            for target in range(4)
            if target != assigned
            for term in threshold_terms(values[observer], complete[target])
        )
    return z3.Or(*failures)


def efx_edge(values, complete, observer, assigned):
    return z3.And(
        *(
            total(values[observer], complete[assigned])
            >= term
            for target in range(4)
            if target != assigned
            for term in threshold_terms(values[observer], complete[target])
        )
    )


def numeric_complete_edges(values, complete):
    masks = masks_from_bundles(complete)
    return tuple(
        tuple(
            mask_value(values, observer, masks[assigned])
            >= max(
                mask_threshold(values, observer, masks[target])
                for target in range(4)
                if target != assigned
            )
            for assigned in range(4)
        )
        for observer in range(4)
    )


def hall_matching_failure(values, complete, prefix):
    selected = [z3.Bool(f"{prefix}_selected_{observer}") for observer in range(4)]
    neighbors = [z3.Bool(f"{prefix}_neighbor_{bundle}") for bundle in range(4)]
    constraints = [z3.Or(*selected)]
    for bundle in range(4):
        constraints.append(
            neighbors[bundle]
            == z3.Or(
                *(
                    z3.And(
                        selected[observer],
                        efx_edge(values, complete, observer, bundle),
                    )
                    for observer in range(4)
                )
            )
        )
    constraints.append(
        z3.Sum(*(z3.If(neighbor, 1, 0) for neighbor in neighbors))
        < z3.Sum(*(z3.If(selector, 1, 0) for selector in selected))
    )
    return z3.And(*constraints)


def orbit_hall_failure(values, assignment):
    bundles = orbit_bundles(assignment)
    failures = []
    assignment_key = "_".join(str(good) for good in assignment)
    for host in range(4):
        complete = list(bundles)
        complete[host] = tuple(sorted((*complete[host], assignment[4])))
        failures.append(
            hall_matching_failure(
                values,
                complete,
                f"orbit_{assignment_key}_host_{host}",
            )
        )
    return z3.And(*failures)


def orbit_matching_failure(values, assignment):
    bundles = orbit_bundles(assignment)
    failures = []
    for host in range(4):
        failures.extend(
            complete_failure(values, bundles, assignment[4], host, permutation)
            for permutation in itertools.permutations(range(4))
        )
    return z3.And(*failures)


def orbit_completion_failure(values, assignment, mode):
    if mode == "orbit_hall":
        return orbit_hall_failure(values, assignment)
    if mode == "orbit_matching":
        return orbit_matching_failure(values, assignment)
    raise ValueError(f"no whole-orbit blocker for mode: {mode}")


def orbit_bundles(assignment):
    return tuple(
        tuple(sorted((CORES[owner], assignment[owner])))
        for owner in range(4)
    )


def global_landscape(raw_values, witness_mode="any"):
    evaluator = FastParkability(4, 9)
    landscape = evaluator.partial_linear_potential_landscape(
        raw_values,
        potential="normalized_threshold",
    )
    base_masks = masks_from_bundles(BASE)
    fixed = next(
        (
            winner
            for winner in landscape["maximizers"]
            if winner["floater"] == FLOATER
            and tuple(
                int(mask)
                for mask in evaluator.base_masks[FLOATER][winner["base_index"]]
            )
            == base_masks
        ),
        None,
    )
    higher_state = None
    if fixed is None:
        higher_state = nearest_higher_state(
            raw_values,
            evaluator,
            base_masks,
            witness_mode=witness_mode,
        )
    return landscape, fixed, higher_state


def owner_assignment(state):
    assignment = [-1] * 9
    for owner, mask in enumerate(state["masks"]):
        for good in range(9):
            if int(mask) & (1 << good):
                assignment[good] = owner
    if assignment[state["floater"]] != -1:
        raise AssertionError("floater appears in an allocated bundle")
    if any(owner < 0 for good, owner in enumerate(assignment) if good != state["floater"]):
        raise AssertionError("allocated good is missing from the state")
    return tuple(assignment)


def nearest_higher_state(raw_values, evaluator, base_masks, witness_mode="any"):
    if witness_mode not in {"any", "hall_insertable"}:
        raise ValueError("witness mode must be any or hall_insertable")
    matrix = np.asarray(raw_values, dtype=np.int64)
    totals, thresholds = evaluator._tables(raw_values)
    row_totals = tuple(int(total) for total in matrix.sum(axis=1))
    common_denominator = math.lcm(*row_totals)
    weights = np.asarray(
        [common_denominator // total for total in row_totals],
        dtype=object,
    )
    base_score = sum(
        int(thresholds[owner, base_masks[owner]]) * int(weights[owner])
        for owner in range(4)
    )
    base_state = {"floater": FLOATER, "masks": base_masks}
    base_assignment = owner_assignment(base_state)
    candidates = []

    for floater, masks in enumerate(evaluator.base_masks):
        valid = np.ones(len(masks), dtype=bool)
        for observer in range(4):
            own = totals[observer, masks[:, observer]]
            valid &= own >= matrix[observer, floater]
            for target in range(4):
                if observer != target:
                    valid &= own >= thresholds[observer, masks[:, target]]
        indices = np.flatnonzero(valid)
        if not len(indices):
            continue
        owner_thresholds = np.column_stack(
            [
                thresholds[owner, masks[indices, owner]]
                for owner in range(4)
            ]
        )
        scores = owner_thresholds.astype(object) @ weights
        for offset in np.flatnonzero(scores > base_score):
            index = int(indices[offset])
            state = {
                "floater": floater,
                "masks": tuple(int(mask) for mask in masks[index]),
            }
            assignment = owner_assignment(state)
            owner_distance = sum(
                left != right
                for left, right in zip(base_assignment, assignment)
            )
            gain = int(scores[offset]) - base_score
            key = (owner_distance, gain, state_key(state))
            candidates.append(
                (
                    key,
                    {
                        **state,
                        "owner_distance": owner_distance,
                        "threshold_gain_numerator": gain,
                        "threshold_gain_denominator": common_denominator,
                    },
                )
            )
    if not candidates:
        raise AssertionError("nonmaximal base has no strictly higher eligible state")
    candidates.sort(key=lambda entry: entry[0])
    if witness_mode == "hall_insertable":
        for _key, state in candidates:
            margin, host, permutation, _bottlenecks = exact_best_hall_margin(
                raw_values,
                state,
            )
            if margin >= 0:
                return {
                    **state,
                    "hall_insertable": True,
                    "best_hall_margin": str(margin),
                    "best_host": host,
                    "best_permutation": list(permutation),
                }
    return {
        **candidates[0][1],
        "hall_insertable": False if witness_mode == "hall_insertable" else None,
    }


def state_key(state):
    return (state["floater"], tuple(int(mask) for mask in state["masks"]))


def owner_relabelings(mode):
    if mode == "none":
        return ((0, 1, 2, 3),)
    if mode == "cyclic":
        return tuple(
            tuple((owner + shift) % 4 for owner in range(4))
            for shift in range(4)
        )
    if mode == "full":
        return tuple(itertools.permutations(range(4)))
    raise ValueError(f"unknown relabeling mode: {mode}")


def relabeled_state_orbit(state, mode):
    results = {}
    for permutation in owner_relabelings(mode):
        good_map = {8: 8}
        for owner in range(4):
            good_map[2 * owner] = 2 * permutation[owner]
            good_map[2 * owner + 1] = 2 * permutation[owner] + 1
        masks = [0] * 4
        for owner, mask in enumerate(state["masks"]):
            mapped_owner = permutation[owner]
            for good in range(9):
                if int(mask) & (1 << good):
                    masks[mapped_owner] |= 1 << good_map[good]
        mapped = {
            "floater": good_map[state["floater"]],
            "masks": tuple(masks),
        }
        for field in (
            "owner_distance",
            "threshold_gain_numerator",
            "threshold_gain_denominator",
        ):
            if field in state:
                mapped[field] = state[field]
        if "preloaded" in state:
            mapped["preloaded"] = state["preloaded"]
        for field in ("hall_insertable", "best_hall_margin"):
            if field in state:
                mapped[field] = state[field]
        results[state_key(mapped)] = mapped
    return tuple(results.values())


def add_constraint(solver, constraint, tracker=None):
    if tracker is None:
        solver.add(constraint)
    else:
        solver.assert_and_track(constraint, z3.Bool(tracker))


def global_cut_tracker(state):
    return "global_{}_{}".format(
        state["floater"],
        "_".join(str(int(mask)) for mask in state["masks"]),
    )


def completion_cut_tracker(assignment, host, permutation):
    return "completion_{}_host_{}_perm_{}".format(
        "_".join(str(int(good)) for good in assignment),
        host,
        "_".join(str(int(bundle)) for bundle in permutation),
    )


def orbit_cut_tracker(assignment):
    return "orbit_{}".format(
        "_".join(str(int(good)) for good in assignment),
    )


def add_global_cut(solver, values, base_theta, state, *, track=False):
    bundles = bundles_from_masks(state["masks"], 9)
    add_constraint(
        solver,
        z3.Implies(
            eligible(values, bundles, state["floater"]),
            theta_upper_bound(values, bundles, base_theta),
        ),
        global_cut_tracker(state) if track else None,
    )


def local_pair_exchange_states(max_distance):
    if max_distance not in {0, 2, 3}:
        raise ValueError("local pair-exchange distance must be 0, 2, or 3")
    if max_distance == 0:
        return ()
    states = {}
    base_assignment = owner_assignment(
        {"floater": FLOATER, "masks": masks_from_bundles(BASE)}
    )
    for order in itertools.permutations(range(9)):
        bundles = tuple(
            tuple(sorted(order[2 * owner : 2 * owner + 2]))
            for owner in range(4)
        )
        state = {"floater": order[8], "masks": masks_from_bundles(bundles)}
        key = state_key(state)
        if key in states:
            continue
        distance = sum(
            left != right
            for left, right in zip(base_assignment, owner_assignment(state))
        )
        if 2 <= distance <= max_distance:
            states[key] = {**state, "owner_distance": distance, "preloaded": True}
    return tuple(states.values())


def run(
    output: Path,
    timeout_seconds: int,
    max_iterations: int,
    seed: Path | None,
    relabeling_mode: str,
    completion_batch_size: int,
    preload_local_exchange_distance: int = 0,
    completion_cut_mode: str = "witness",
    solver_profile: str = "default",
    global_witness_mode: str = "any",
    base_host_edge_cell_source: Path | None = None,
    base_host_pair_hall_cycle: bool = False,
    base_host_offhost_edge_cell_source: Path | None = None,
    base_host_diagonal_pattern: int | None = None,
    smt2_output: Path | None = None,
    track_unsat_core: bool = False,
    minimize_unsat_core: bool = False,
    base_owner_cores_dominate_floater: bool = False,
    refute_base_owner_core_below_floater: int | None = None,
    base_owner_cores_dominate_predecessor_tokens: bool = False,
    refute_base_owner_predecessor_token_above_core: int | None = None,
    base_pair_hall_cross_row_core_clauses: bool = False,
    refute_base_pair_hall_cross_row_core_clause: str | None = None,
):
    if completion_cut_mode not in {"witness", "orbit_hall", "orbit_matching"}:
        raise ValueError(
            "completion-cut mode must be witness, orbit_hall, or orbit_matching"
        )
    if solver_profile not in {"default", "qf_lra", "arith2"}:
        raise ValueError("solver profile must be default, qf_lra, or arith2")
    if global_witness_mode not in {"any", "hall_insertable"}:
        raise ValueError("global witness mode must be any or hall_insertable")
    if base_host_edge_cell_source is not None and base_host_pair_hall_cycle:
        raise ValueError("exact host-edge and pair-Hall cells are mutually exclusive")
    if (
        base_host_offhost_edge_cell_source is not None
        and not base_host_pair_hall_cycle
    ):
        raise ValueError("off-host edge cell requires the pair-Hall cycle")
    if (
        base_host_edge_cell_source is not None
        and base_host_offhost_edge_cell_source is not None
    ):
        raise ValueError("exact and off-host edge cells are mutually exclusive")
    if base_host_diagonal_pattern is not None and not 0 <= base_host_diagonal_pattern < 256:
        raise ValueError("diagonal pattern must be an integer from 0 to 255")
    if (
        base_host_diagonal_pattern is not None
        and base_host_offhost_edge_cell_source is None
    ):
        raise ValueError("diagonal pattern requires the off-host edge cell")
    if smt2_output is not None and track_unsat_core:
        raise ValueError(
            "standalone SMT2 output requires untracked assertions"
        )
    if minimize_unsat_core and not track_unsat_core:
        raise ValueError("UNSAT-core minimization requires tracked assertions")
    if (
        refute_base_owner_core_below_floater is not None
        and not 0 <= refute_base_owner_core_below_floater < 4
    ):
        raise ValueError("core-dominance refutation owner must lie in [0,3]")
    if (
        base_owner_cores_dominate_floater
        and refute_base_owner_core_below_floater is not None
    ):
        raise ValueError(
            "core-dominance assumption and refutation mode are mutually exclusive"
        )
    if (
        refute_base_owner_predecessor_token_above_core is not None
        and not 0 <= refute_base_owner_predecessor_token_above_core < 4
    ):
        raise ValueError("predecessor-token refutation owner must lie in [0,3]")
    if (
        base_owner_cores_dominate_predecessor_tokens
        and refute_base_owner_predecessor_token_above_core is not None
    ):
        raise ValueError(
            "predecessor-token dominance assumption and refutation mode are "
            "mutually exclusive"
        )
    if (
        refute_base_owner_core_below_floater is not None
        and refute_base_owner_predecessor_token_above_core is not None
    ):
        raise ValueError("only one core-dominance wall can be refuted at a time")
    if base_pair_hall_cross_row_core_clauses and not (
        base_owner_cores_dominate_floater
        and base_owner_cores_dominate_predecessor_tokens
    ):
        raise ValueError("cross-row core clauses require both proved cyclic walls")
    if refute_base_pair_hall_cross_row_core_clause is not None:
        if refute_base_pair_hall_cross_row_core_clause not in {
            f"{family}{shift}"
            for family in ("a", "b")
            for shift in range(4)
        }:
            raise ValueError("cross-row clause refutation must identify a0..a3/b0..b3")
        if not (
            base_owner_cores_dominate_floater
            and base_owner_cores_dominate_predecessor_tokens
        ):
            raise ValueError("cross-row clause refutation requires both proved walls")
        if base_pair_hall_cross_row_core_clauses:
            raise ValueError("cross-row clause assumption and refutation are exclusive")
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.SolverFor("QF_LRA") if solver_profile == "qf_lra" else z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    if minimize_unsat_core:
        solver.set("smt.core.minimize", True)
    if solver_profile == "arith2":
        solver.set("smt.arith.solver", 2)
    for row in values:
        solver.add(z3.Sum(*row) == 1)
        solver.add(*(entry > 0 for entry in row))
    solver.add(eligible(values, BASE, FLOATER))
    for owner, (core, token) in enumerate(zip(CORES, TOKENS[:4])):
        solver.add(values[owner][token] < values[owner][core])
    if base_owner_cores_dominate_floater:
        solver.add(owner_cores_dominate_floater(values))
    if refute_base_owner_core_below_floater is not None:
        owner = refute_base_owner_core_below_floater
        solver.add(values[owner][CORES[owner]] < values[owner][FLOATER])
    if base_owner_cores_dominate_predecessor_tokens:
        solver.add(owner_cores_dominate_predecessor_tokens(values))
    if refute_base_owner_predecessor_token_above_core is not None:
        owner = refute_base_owner_predecessor_token_above_core
        predecessor_token = (2 * owner - 1) % 8
        solver.add(values[owner][predecessor_token] > values[owner][CORES[owner]])
    if base_pair_hall_cross_row_core_clauses:
        solver.add(pair_hall_cross_row_core_clauses(values))
    if refute_base_pair_hall_cross_row_core_clause is not None:
        family = refute_base_pair_hall_cross_row_core_clause[0]
        shift = int(refute_base_pair_hall_cross_row_core_clause[1])
        solver.add(z3.Not(pair_hall_cross_row_core_clause(values, family, shift)))
    edge_cell_sha256 = None
    if base_host_edge_cell_source is not None:
        edge_document = json.loads(base_host_edge_cell_source.read_text())
        edge_values = edge_document.get("values", edge_document)
        edge_cell_sha256 = hashlib.sha256(
            base_host_edge_cell_source.read_bytes()
        ).hexdigest()
        for host in range(4):
            complete = [tuple(bundle) for bundle in BASE]
            complete[host] = tuple(sorted((*complete[host], FLOATER)))
            expected_edges = numeric_complete_edges(edge_values, complete)
            for observer in range(4):
                for assigned in range(4):
                    solver.add(
                        efx_edge(values, complete, observer, assigned)
                        == expected_edges[observer][assigned]
                    )
    if base_host_pair_hall_cycle:
        for host, observers in enumerate(PAIR_HALL_CYCLE):
            complete = [tuple(bundle) for bundle in BASE]
            complete[host] = tuple(sorted((*complete[host], FLOATER)))
            for observer in observers:
                for assigned in range(4):
                    solver.add(
                        efx_edge(values, complete, observer, assigned)
                        == (assigned == host)
                    )
    offhost_edge_cell_sha256 = None
    if base_host_offhost_edge_cell_source is not None:
        offhost_document = json.loads(base_host_offhost_edge_cell_source.read_text())
        offhost_values = offhost_document.get("values", offhost_document)
        offhost_edge_cell_sha256 = hashlib.sha256(
            base_host_offhost_edge_cell_source.read_bytes()
        ).hexdigest()
        for host, pair in enumerate(PAIR_HALL_CYCLE):
            complete = [tuple(bundle) for bundle in BASE]
            complete[host] = tuple(sorted((*complete[host], FLOATER)))
            expected_edges = numeric_complete_edges(offhost_values, complete)
            for observer in sorted(set(range(4)) - set(pair)):
                for assigned in range(4):
                    if assigned == host:
                        continue
                    solver.add(
                        efx_edge(values, complete, observer, assigned)
                        == expected_edges[observer][assigned]
                    )
    diagonal_edge_order = []
    if base_host_diagonal_pattern is not None:
        for host, pair in enumerate(PAIR_HALL_CYCLE):
            complete = [tuple(bundle) for bundle in BASE]
            complete[host] = tuple(sorted((*complete[host], FLOATER)))
            for observer in sorted(set(range(4)) - set(pair)):
                bit = len(diagonal_edge_order)
                expected = bool(base_host_diagonal_pattern & (1 << bit))
                solver.add(
                    efx_edge(values, complete, observer, host) == expected
                )
                diagonal_edge_order.append([host, observer])

    base_theta = z3.Sum(
        *(values[owner][core] for owner, core in enumerate(CORES))
    )
    for assignment in itertools.permutations(TOKENS):
        bundles = orbit_bundles(assignment)
        solver.add(
            z3.Implies(
                eligible(values, bundles, assignment[4]),
                z3.And(
                    *(
                        values[owner][assignment[owner]]
                        <= values[owner][CORES[owner]]
                        for owner in range(4)
                    )
                ),
            )
        )

    global_cuts = set()
    completion_cuts = set()
    orbit_hall_cuts = set()
    global_cut_records = []
    completion_cut_records = []
    orbit_hall_cut_records = []
    prior_iterations = 0
    seed_values_hint = None
    if seed is not None:
        seed_document = json.loads(seed.read_text())
        if seed_document.get("schema") != SCHEMA:
            raise ValueError("seed has incompatible schema")
        prior_iterations = int(seed_document.get("total_iterations", 0))
        if seed_document.get("values") is not None:
            seed_values_hint = seed_document["values"]
        for record in seed_document.get("global_cuts", []):
            seed_state = {
                "floater": int(record["floater"]),
                "masks": tuple(int(mask) for mask in record["masks"]),
                **{
                    field: int(record[field])
                    for field in (
                        "owner_distance",
                        "threshold_gain_numerator",
                        "threshold_gain_denominator",
                    )
                    if field in record
                },
                **({"preloaded": bool(record["preloaded"])} if "preloaded" in record else {}),
                **(
                    {"hall_insertable": bool(record["hall_insertable"])}
                    if "hall_insertable" in record
                    else {}
                ),
                **(
                    {"best_hall_margin": str(record["best_hall_margin"])}
                    if "best_hall_margin" in record
                    else {}
                ),
            }
            for state in relabeled_state_orbit(seed_state, relabeling_mode):
                key = state_key(state)
                if key in global_cuts:
                    continue
                global_cuts.add(key)
                global_cut_records.append(
                    {
                        "floater": state["floater"],
                        "masks": list(state["masks"]),
                        **{
                            field: state[field]
                            for field in (
                                "owner_distance",
                                "threshold_gain_numerator",
                                "threshold_gain_denominator",
                            )
                            if field in state
                        },
                        **({"preloaded": state["preloaded"]} if "preloaded" in state else {}),
                        **{
                            field: state[field]
                            for field in ("hall_insertable", "best_hall_margin")
                            if field in state
                        },
                    }
                )
                add_global_cut(
                    solver,
                    values,
                    base_theta,
                    state,
                    track=track_unsat_core,
                )
        for record in seed_document.get("completion_cuts", []):
            assignment = tuple(int(good) for good in record["assignment"])
            host = int(record["host"])
            permutation = tuple(int(bundle) for bundle in record["permutation"])
            key = (assignment, host, permutation)
            if key in completion_cuts:
                continue
            completion_cuts.add(key)
            completion_cut_records.append(
                {
                    "assignment": list(assignment),
                    "host": host,
                    "permutation": list(permutation),
                }
            )
            bundles = orbit_bundles(assignment)
            add_constraint(
                solver,
                z3.Implies(
                    eligible(values, bundles, assignment[4]),
                    complete_failure(
                        values,
                        bundles,
                        assignment[4],
                        host,
                        permutation,
                    ),
                ),
                (
                    completion_cut_tracker(assignment, host, permutation)
                    if track_unsat_core
                    else None
                ),
            )
        for record in seed_document.get("orbit_hall_cuts", []):
            assignment = tuple(int(good) for good in record["assignment"])
            if assignment in orbit_hall_cuts:
                continue
            orbit_hall_cuts.add(assignment)
            orbit_hall_cut_records.append({"assignment": list(assignment)})
            bundles = orbit_bundles(assignment)
            add_constraint(
                solver,
                z3.Implies(
                    eligible(values, bundles, assignment[4]),
                    orbit_completion_failure(
                        values,
                        assignment,
                        completion_cut_mode,
                    ),
                ),
                orbit_cut_tracker(assignment) if track_unsat_core else None,
            )
    for state in local_pair_exchange_states(preload_local_exchange_distance):
        key = state_key(state)
        if key in global_cuts:
            continue
        global_cuts.add(key)
        global_cut_records.append(
            {
                "floater": state["floater"],
                "masks": list(state["masks"]),
                "owner_distance": state["owner_distance"],
                "preloaded": True,
            }
        )
        add_global_cut(
            solver,
            values,
            base_theta,
            state,
            track=track_unsat_core,
        )
    if seed_values_hint is not None:
        for row, symbolic_row in zip(seed_values_hint, values):
            row_total = sum(int(entry) for entry in row)
            for entry, symbolic_entry in zip(row, symbolic_row):
                solver.set_initial_value(
                    symbolic_entry,
                    z3.Q(int(entry), row_total),
                )
    if smt2_output is not None:
        smt2_output.write_text(solver.to_smt2())
    started = time.monotonic()
    last_values = None
    last_orbit = None
    last_global = None
    last_higher_state = None
    last_orbit_blocked_values = None
    last_orbit_blocked_orbit = None
    last_orbit_blocked_global = None
    orbit_blocked_seed_path = output.with_name(
        f"{output.stem}_orbit_blocked_seed.json"
    )
    status = "ITERATION_LIMIT"
    reason_unknown = None
    unsat_core_labels = None

    iteration = 0
    for iteration in range(1, max_iterations + 1):
        verdict = solver.check()
        if verdict == z3.unsat:
            status = (
                "BASE_OWNER_CORE_DOMINANCE_FORCED"
                if refute_base_owner_core_below_floater is not None
                else "BASE_OWNER_PREDECESSOR_TOKEN_DOMINANCE_FORCED"
                if refute_base_owner_predecessor_token_above_core is not None
                else "BASE_PAIR_HALL_CROSS_ROW_CORE_CLAUSE_FORCED"
                if refute_base_pair_hall_cross_row_core_clause is not None
                else "FIXED_PAIR_TOKEN_ORBIT_FORCED"
            )
            if track_unsat_core:
                unsat_core_labels = sorted(str(label) for label in solver.unsat_core())
            break
        if verdict == z3.unknown:
            status = "UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break

        model = solver.model()
        raw_values = integer_values(model, values)
        last_values = raw_values
        last_global = None
        last_higher_state = None
        base_state = {
            "floater": FLOATER,
            "masks": masks_from_bundles(BASE),
        }
        last_orbit = audit_orbit(
            raw_values,
            base_state,
            TOKENS[:4],
            include_records=True,
        )
        completing_records = [
            record for record in last_orbit["records"] if record["completing"]
        ][:completion_batch_size]
        if completing_records:
            if completion_cut_mode in {"orbit_hall", "orbit_matching"}:
                for completing in completing_records:
                    assignment = tuple(completing["assignment"])
                    if assignment in orbit_hall_cuts:
                        raise AssertionError("repeated orbit Hall cut")
                    orbit_hall_cuts.add(assignment)
                    orbit_hall_cut_records.append(
                        {"assignment": list(assignment)}
                    )
                    bundles = orbit_bundles(assignment)
                    add_constraint(
                        solver,
                        z3.Implies(
                            eligible(values, bundles, assignment[4]),
                            orbit_completion_failure(
                                values,
                                assignment,
                                completion_cut_mode,
                            ),
                        ),
                        orbit_cut_tracker(assignment) if track_unsat_core else None,
                    )
            else:
                for completing in completing_records:
                    assignment = tuple(completing["assignment"])
                    key = (
                        assignment,
                        completing["best_host"],
                        tuple(completing["best_permutation"]),
                    )
                    if key in completion_cuts:
                        raise AssertionError(
                            "repeated token-orbit completion witness"
                        )
                    completion_cuts.add(key)
                    completion_cut_records.append(
                        {
                            "assignment": list(assignment),
                            "host": completing["best_host"],
                            "permutation": list(
                                completing["best_permutation"]
                            ),
                        }
                    )
                    bundles = orbit_bundles(assignment)
                    add_constraint(
                        solver,
                        z3.Implies(
                            eligible(values, bundles, assignment[4]),
                            complete_failure(
                                values,
                                bundles,
                                assignment[4],
                                completing["best_host"],
                                tuple(completing["best_permutation"]),
                            ),
                        ),
                        (
                            completion_cut_tracker(
                                assignment,
                                completing["best_host"],
                                tuple(completing["best_permutation"]),
                            )
                            if track_unsat_core
                            else None
                        ),
                    )
            continue

        landscape, fixed, higher_state = global_landscape(
            raw_values,
            witness_mode=global_witness_mode,
        )
        last_global = {
            "eligible_state_count": landscape["eligible_base_count"],
            "maximum_threshold_state_count": landscape["maximizer_count"],
            "hall_insertable_maximum_threshold_state_count": landscape[
                "hall_insertable_maximizer_count"
            ],
            "fixed_base_is_global_threshold_maximum": fixed is not None,
        }
        last_higher_state = higher_state
        last_orbit_blocked_values = raw_values
        last_orbit_blocked_orbit = last_orbit
        last_orbit_blocked_global = last_global
        atomic_json(
            orbit_blocked_seed_path,
            {
                "schema": "minimum-slot-orbit-blocked-seed-v1",
                "status": "EXACT_ORBIT_BLOCKED",
                "meaning": (
                    "Exact positive valuation whose canonical five-token "
                    "orbit has no eligible EFX completion. Global audit is "
                    "aligned to the same valuation."
                ),
                "source_session": str(output),
                "iteration": iteration,
                "values": raw_values,
                "orbit_audit": last_orbit,
                "global_audit": last_global,
                "nearest_higher_state": (
                    {
                        **last_higher_state,
                        "masks": list(last_higher_state["masks"]),
                    }
                    if last_higher_state is not None
                    else None
                ),
                "global_cut_count": len(global_cuts),
                "completion_cut_count": len(completion_cuts),
                "orbit_hall_cut_count": len(orbit_hall_cuts),
            },
        )

        if fixed is None:
            witness_key = state_key(higher_state)
            if witness_key in global_cuts:
                raise AssertionError("repeated global maximality witness")
            for state in relabeled_state_orbit(higher_state, relabeling_mode):
                key = state_key(state)
                if key in global_cuts:
                    continue
                global_cuts.add(key)
                global_cut_records.append(
                    {
                        "floater": state["floater"],
                        "masks": list(state["masks"]),
                        **{
                            field: state[field]
                            for field in (
                                "owner_distance",
                                "threshold_gain_numerator",
                                "threshold_gain_denominator",
                            )
                            if field in state
                        },
                        **{
                            field: state[field]
                            for field in ("hall_insertable", "best_hall_margin")
                            if field in state
                        },
                    }
                )
                add_global_cut(
                    solver,
                    values,
                    base_theta,
                    state,
                    track=track_unsat_core,
                )
            continue

        status = "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND"
        break

    artifact = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "Exact CEGAR for a positive canonical four-pair base with unique "
            "owner minima. Global cuts enforce normalized-threshold maximality; "
            "completion cuts adversarially block exact EFX matchings inside "
            "the fixed five-token orbit."
        ),
        "claim_boundary": (
            (
                "BASE_OWNER_CORE_DOMINANCE_FORCED proves only that the selected "
                "owner's core weakly dominates the floater under the imposed "
                "pair-Hall cell and archived finite consequences of global "
                "threshold maximality and token-orbit blockage. Cyclic lifting "
                "to the other owners is a separate symmetry step. It does not "
                "prove the full pair-Hall cell or four-agent EFX."
            )
            if refute_base_owner_core_below_floater is not None
            else (
                "BASE_OWNER_PREDECESSOR_TOKEN_DOMINANCE_FORCED proves only "
                "that the selected owner's core weakly dominates the preceding "
                "pair's token, conditional on any separately imposed core-"
                "floater wall. Cyclic lifting is a separate symmetry step. It "
                "does not prove the full pair-Hall cell or four-agent EFX."
            )
            if refute_base_owner_predecessor_token_above_core is not None
            else (
                "BASE_PAIR_HALL_CROSS_ROW_CORE_CLAUSE_FORCED proves only the "
                "selected two-literal clause, conditional on the two proved "
                "cyclic walls and the archived pair-Hall consequence pool. "
                "It does not close the pair-Hall cell or prove four-agent EFX."
            )
            if refute_base_pair_hall_cross_row_core_clause is not None
            else (
                "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND refutes the fixed-core "
                "orbit theorem inside the imposed host-edge subcell after exact "
                "replay. UNSAT proves only the subcell fixing every base-host EFX "
                "edge to the recorded source profile. Hall-insertable metadata "
                "describes each cut's discovery valuation, not every valuation "
                "satisfying that cut. Other statuses are not verdicts."
            )
            if base_host_edge_cell_source is not None
            else (
                (
                    (
                        "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND refutes the "
                        "fixed-core orbit theorem inside one fixed diagonal-pattern "
                        "edge cell after exact replay. UNSAT proves only that exact "
                        "pattern, not the eight-switch family or full pair-Hall cell."
                    )
                    if base_host_diagonal_pattern is not None
                    else (
                        (
                            "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND refutes the "
                            "fixed-core orbit theorem inside the imposed eight-"
                            "diagonal-switch subcell after exact replay. UNSAT fixes "
                            "the 24 off-host edge values and does not prove the full "
                            "pair-Hall cell. Hall-insertable metadata describes "
                            "discovery valuations only. Other statuses are not "
                            "verdicts."
                        )
                        if base_host_offhost_edge_cell_source is not None
                        else (
                            "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND refutes the "
                            "fixed-core orbit theorem inside the imposed cyclic "
                            "pair-Hall cell after exact replay. UNSAT proves only "
                            "that pair-Hall subcell. Hall-insertable metadata "
                            "describes each cut's discovery valuation, not every "
                            "valuation satisfying that cut. Other statuses are not "
                            "verdicts."
                        )
                    )
                )
                if base_host_pair_hall_cycle
                else (
                    "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND refutes the fixed-core "
                    "orbit theorem for this base cell after exact replay. UNSAT "
                    "proves only the canonical four-pair cell. Hall-insertable "
                    "metadata describes each cut's discovery valuation. Other "
                    "statuses are not verdicts."
                )
            )
        ),
        "global_cut_semantics": (
            "Every stored cut is eligibility(state) implies "
            "theta(state) <= theta(base). Completion metadata is not part of "
            "the cut formula."
        ),
        "iterations": iteration,
        "prior_iterations": prior_iterations,
        "total_iterations": prior_iterations + iteration,
        "max_iterations": max_iterations,
        "timeout_seconds_per_check": timeout_seconds,
        "relabeling_mode": relabeling_mode,
        "completion_batch_size": completion_batch_size,
        "preload_local_exchange_distance": preload_local_exchange_distance,
        "completion_cut_mode": completion_cut_mode,
        "solver_profile": solver_profile,
        "global_witness_mode": global_witness_mode,
        "base_host_edge_cell_source": (
            str(base_host_edge_cell_source)
            if base_host_edge_cell_source is not None
            else None
        ),
        "base_host_edge_cell_source_sha256": edge_cell_sha256,
        "base_host_pair_hall_cycle": base_host_pair_hall_cycle,
        "base_host_pair_hall_witnesses": (
            [list(pair) for pair in PAIR_HALL_CYCLE]
            if base_host_pair_hall_cycle
            else None
        ),
        "base_owner_cores_dominate_floater": (
            base_owner_cores_dominate_floater
        ),
        "refute_base_owner_core_below_floater": (
            refute_base_owner_core_below_floater
        ),
        "base_owner_cores_dominate_predecessor_tokens": (
            base_owner_cores_dominate_predecessor_tokens
        ),
        "refute_base_owner_predecessor_token_above_core": (
            refute_base_owner_predecessor_token_above_core
        ),
        "base_pair_hall_cross_row_core_clauses": (
            base_pair_hall_cross_row_core_clauses
        ),
        "refute_base_pair_hall_cross_row_core_clause": (
            refute_base_pair_hall_cross_row_core_clause
        ),
        "base_host_offhost_edge_cell_source": (
            str(base_host_offhost_edge_cell_source)
            if base_host_offhost_edge_cell_source is not None
            else None
        ),
        "base_host_offhost_edge_cell_source_sha256": offhost_edge_cell_sha256,
        "base_host_diagonal_pattern": base_host_diagonal_pattern,
        "base_host_diagonal_edge_order": (
            diagonal_edge_order if base_host_diagonal_pattern is not None else None
        ),
        "smt2_output": str(smt2_output) if smt2_output is not None else None,
        "track_unsat_core": track_unsat_core,
        "minimize_unsat_core": minimize_unsat_core,
        "unsat_core_labels": unsat_core_labels,
        "unsat_core_size": (
            len(unsat_core_labels) if unsat_core_labels is not None else None
        ),
        "seed_initial_values_applied": seed_values_hint is not None,
        "elapsed_seconds": time.monotonic() - started,
        "global_cut_count": len(global_cuts),
        "completion_cut_count": len(completion_cuts),
        "orbit_hall_cut_count": len(orbit_hall_cuts),
        "global_cuts": global_cut_records,
        "completion_cuts": completion_cut_records,
        "orbit_hall_cuts": orbit_hall_cut_records,
        "solver_reason_unknown": reason_unknown,
        "values": last_values,
        "global_audit": last_global,
        "nearest_higher_state": (
            {
                **last_higher_state,
                "masks": list(last_higher_state["masks"]),
            }
            if last_higher_state is not None
            else None
        ),
        "orbit_audit": last_orbit,
        "last_orbit_blocked_values": last_orbit_blocked_values,
        "last_orbit_blocked_orbit_audit": last_orbit_blocked_orbit,
        "last_orbit_blocked_global_audit": last_orbit_blocked_global,
        "orbit_blocked_seed": (
            str(orbit_blocked_seed_path)
            if last_orbit_blocked_values is not None
            else None
        ),
    }
    atomic_json(output, artifact)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--seed", type=Path)
    parser.add_argument(
        "--relabeling-mode",
        choices=("none", "cyclic", "full"),
        default="cyclic",
    )
    parser.add_argument("--completion-batch-size", type=int, default=8)
    parser.add_argument(
        "--preload-local-exchange-distance",
        type=int,
        choices=(0, 2, 3),
        default=0,
    )
    parser.add_argument(
        "--completion-cut-mode",
        choices=("witness", "orbit_hall", "orbit_matching"),
        default="witness",
    )
    parser.add_argument(
        "--solver-profile",
        choices=("default", "qf_lra", "arith2"),
        default="default",
    )
    parser.add_argument(
        "--global-witness-mode",
        choices=("any", "hall_insertable"),
        default="any",
    )
    parser.add_argument("--base-host-edge-cell-source", type=Path)
    parser.add_argument("--base-host-pair-hall-cycle", action="store_true")
    parser.add_argument(
        "--base-owner-cores-dominate-floater",
        action="store_true",
    )
    parser.add_argument(
        "--refute-base-owner-core-below-floater",
        type=int,
        choices=range(4),
    )
    parser.add_argument(
        "--base-owner-cores-dominate-predecessor-tokens",
        action="store_true",
    )
    parser.add_argument(
        "--refute-base-owner-predecessor-token-above-core",
        type=int,
        choices=range(4),
    )
    parser.add_argument(
        "--base-pair-hall-cross-row-core-clauses",
        action="store_true",
    )
    parser.add_argument(
        "--refute-base-pair-hall-cross-row-core-clause",
        choices=tuple(
            f"{family}{shift}"
            for family in ("a", "b")
            for shift in range(4)
        ),
    )
    parser.add_argument("--base-host-offhost-edge-cell-source", type=Path)
    parser.add_argument("--base-host-diagonal-pattern", type=int)
    parser.add_argument("--smt2-output", type=Path)
    parser.add_argument("--track-unsat-core", action="store_true")
    parser.add_argument("--minimize-unsat-core", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output,
        args.timeout_seconds,
        args.max_iterations,
        args.seed,
        args.relabeling_mode,
        args.completion_batch_size,
        args.preload_local_exchange_distance,
        args.completion_cut_mode,
        args.solver_profile,
        args.global_witness_mode,
        args.base_host_edge_cell_source,
        args.base_host_pair_hall_cycle,
        args.base_host_offhost_edge_cell_source,
        args.base_host_diagonal_pattern,
        args.smt2_output,
        args.track_unsat_core,
        args.minimize_unsat_core,
        args.base_owner_cores_dominate_floater,
        args.refute_base_owner_core_below_floater,
        args.base_owner_cores_dominate_predecessor_tokens,
        args.refute_base_owner_predecessor_token_above_core,
        args.base_pair_hall_cross_row_core_clauses,
        args.refute_base_pair_hall_cross_row_core_clause,
    )
    summary = {
        key: result[key]
        for key in (
            "schema",
            "status",
            "iterations",
            "total_iterations",
            "elapsed_seconds",
            "global_cut_count",
            "completion_cut_count",
            "orbit_hall_cut_count",
            "solver_reason_unknown",
            "global_audit",
        )
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
