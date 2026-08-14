#!/usr/bin/env python3
"""Exact CEGAR with the necessary full rank-three response-relation gates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_fixed_u_full_packet_batch_cegar import oracle_menu, serialize_values
    from .run_fixed_u_full_packet_terminal_cegar import (
        BASE, GOODS, OWNERS, PACKETS, REASSEMBLY_STATE, SPLIT_STATE,
        SUPPORT_STATE, allocation_formula, build_master, fractions, tail, total,
    )
except ImportError:  # Permit direct replay from the script path.
    from run_fixed_u_full_packet_batch_cegar import oracle_menu, serialize_values
    from run_fixed_u_full_packet_terminal_cegar import (
        BASE, GOODS, OWNERS, PACKETS, REASSEMBLY_STATE, SPLIT_STATE,
        SUPPORT_STATE, allocation_formula, build_master, fractions, tail, total,
    )


TARGETS = (*OWNERS, "charity")


def transfer_edge_count(allocation, provenance):
    initial = {
        good: supplier for supplier, goods in provenance.items() for good in goods
    }
    final = {
        good: recipient for recipient, goods in allocation.items() for good in goods
    }
    return len({
        (initial[good], final[good])
        for good in initial if initial[good] != final[good]
    })


def functional_transfer(allocation, provenance):
    initial = {
        good: supplier for supplier, goods in provenance.items() for good in goods
    }
    final = {
        good: recipient for recipient, goods in allocation.items() for good in goods
    }
    edges = {
        (initial[good], final[good])
        for good in initial if initial[good] != final[good]
    }
    return len({source for source, _ in edges}) == len(edges)


def nonempty_subsets(goods):
    goods = tuple(goods)
    for size in range(1, len(goods) + 1):
        yield from itertools.combinations(goods, size)


def base_response(value, source, goods):
    return z3.And(
        total(value, source, goods) > 1,
        *(tail(value, observer, goods) <= 1 for observer in OWNERS),
    )


def response_edges(value, state, include_current, exclude_self=False):
    current_u = {owner: total(value, owner, state[owner]) for owner in OWNERS}
    edge = {}
    for source in OWNERS:
        for target in TARGETS:
            if exclude_self and target == source:
                edge[source, target] = z3.BoolVal(False)
                continue
            relations = []
            for goods in nonempty_subsets(state[target]):
                relations.append(base_response(value, source, goods))
                if include_current:
                    relations.append(z3.And(
                        total(value, source, goods) > current_u[source],
                        *(tail(value, observer, goods) <= current_u[observer]
                          for observer in OWNERS),
                    ))
            edge[source, target] = z3.Or(*relations) if relations else z3.BoolVal(False)
    return edge


def rank_four_exists(edge):
    matchings = []
    for targets in itertools.permutations(TARGETS, len(OWNERS)):
        matchings.append(z3.And(*(
            edge[source, target] for source, target in zip(OWNERS, targets)
        )))
    return z3.Or(*matchings)


def build_rank_three_master(required_minimal_normal_form=False,
                            exclude_self_responses=False,
                            required_owner_cycle_form=False,
                            exact_owner_cycle_response_relation=False,
                            owner_cycle_form_index=None):
    if required_minimal_normal_form and not exclude_self_responses:
        raise ValueError(
            "the exact normal-form census is defined on nonself responses"
        )
    if required_owner_cycle_form and not exclude_self_responses:
        raise ValueError(
            "the corrected owner-cycle census is defined on nonself responses"
        )
    if exact_owner_cycle_response_relation and not (
        required_owner_cycle_form and exclude_self_responses
    ):
        raise ValueError(
            "exact owner-cycle saturation requires the corrected nonself form"
        )
    if owner_cycle_form_index is not None and not exact_owner_cycle_response_relation:
        raise ValueError("form restriction requires exact owner-cycle saturation")
    solver, value = build_master()

    # The three retained cores are actual base-common-safe desired cores in
    # the support state, not merely source-row payment packets.
    for source, packet in (("r", "A"), ("q", "Q"), ("s", "E")):
        solver.add(base_response(value, source, PACKETS[packet]))

    # Exact surviving wall after rank-three compression: d holds W, and the
    # unique selected-core/charity EFX wall is against the permanent root
    # core A.  This is the root-facing branch named by the cap-free residual
    # split lemma; profiles blocked by Q, E, or charity belong to nonroot
    # descent/response augmentation and are not genuine repeats here.
    d_floor = total(value, "d", PACKETS["W"])
    solver.add(d_floor < tail(value, "d", PACKETS["A"]))
    solver.add(d_floor >= tail(value, "d", PACKETS["Q"]))
    solver.add(d_floor >= tail(value, "d", PACKETS["E"]))
    solver.add(d_floor >= total(value, "d", PACKETS["P"]))

    # The canonical support state already represents r,q,s via their retained
    # self-held cores.  A genuine rank-three recurrence cannot also admit a
    # fourth distinct response target for d after recomputing the complete
    # ordinary response relation.
    support_edge = response_edges(
        value, SUPPORT_STATE, include_current=True,
        exclude_self=exclude_self_responses,
    )
    solver.add(z3.Not(rank_four_exists(support_edge)))
    if required_minimal_normal_form:
        # Legacy abstract five-target forms from the independent graph census,
        # with d playing the sacrificed source c. In the canonical paid
        # singleton-charity cell these are expected to be inconsistent because
        # every form requires a response into the base-safe singleton p.
        minimal_forms = (
            (("q", "charity"), ("r", "q"), ("s", "r"), ("d", "q")),
            (("q", "charity"), ("r", "q"), ("s", "d"), ("d", "q")),
            (("q", "s"), ("r", "q"), ("s", "charity"), ("d", "q")),
        )
        solver.add(z3.Or(*(
            z3.And(*(support_edge[edge] for edge in form))
            for form in minimal_forms
        )))
    if required_owner_cycle_form:
        corrected_forms = (
            (("r", "q"), ("q", "r"), ("s", "d"), ("d", "q")),
            (("r", "q"), ("q", "d"), ("s", "r"), ("d", "q")),
            (("r", "q"), ("q", "s"), ("s", "r"), ("d", "q")),
            (("r", "q"), ("q", "s"), ("s", "d"), ("d", "q")),
        )
        selected_forms = (
            (corrected_forms[owner_cycle_form_index],)
            if owner_cycle_form_index is not None else corrected_forms
        )
        if exact_owner_cycle_response_relation:
            nonself_edges = tuple(
                (source, target)
                for source in OWNERS for target in TARGETS
                if target != source
            )
            solver.add(z3.Or(*(
                z3.And(*(
                    support_edge[edge] if edge in (*form, ("d", "r"))
                    else z3.Not(support_edge[edge])
                    for edge in nonself_edges
                ))
                for form in selected_forms
            )))
        else:
            solver.add(z3.Or(*(
                z3.And(*(support_edge[edge] for edge in form))
                for form in selected_forms
            )))

    # The sacrificed-donor split is also a physical target partition.  A
    # rank-four ordinary (base-common-safe) SDR there is already a generalized
    # PI/lex closure, even though the displayed split itself underpays s.
    split_edge = response_edges(
        value, SPLIT_STATE, include_current=False,
        exclude_self=exclude_self_responses,
    )
    solver.add(z3.Not(rank_four_exists(split_edge)))

    # At reassembly, globally minimal observer failures add current-safe
    # decorated responses to the old base-safe relation.  If their union has
    # rank four, the existing mixed rank-four/Hamiltonian endpoint applies;
    # it is not a live rank-three repeat.
    reassembly_edge = response_edges(
        value, REASSEMBLY_STATE, include_current=True,
        exclude_self=exclude_self_responses,
    )
    solver.add(z3.Not(rank_four_exists(reassembly_edge)))
    return solver, value


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(seed_path, output, maximum_iterations, timeout_seconds,
        maximum_escapes, radius_slack, resume, oracle_metric, extra_seeds,
        target_edge_bound, edge_origin, random_seed,
        required_minimal_normal_form=False, exclude_self_responses=False,
        required_owner_cycle_form=False,
        exact_owner_cycle_response_relation=False,
        owner_cycle_form_index=None):
    master, value = build_rank_three_master(
        required_minimal_normal_form, exclude_self_responses,
        required_owner_cycle_form,
        exact_owner_cycle_response_relation,
        owner_cycle_form_index,
    )
    master.set(timeout=timeout_seconds * 1000)
    master.set(random_seed=random_seed)
    seed = json.loads(seed_path.read_text())
    provenance = SUPPORT_STATE if edge_origin == "support" else BASE

    def admissible_seed(mode, allocation):
        within_bound = not (
            mode == "complete_efx"
            and oracle_metric in ("edges", "functional_edges")
            and target_edge_bound is not None
            and transfer_edge_count(allocation, provenance) > target_edge_bound
        )
        functional = not (
            mode == "complete_efx"
            and oracle_metric == "functional_edges"
            and not functional_transfer(allocation, provenance)
        )
        return within_bound and functional

    seed_cuts = []
    for record in seed["iterations"]:
        allocation = record.get("blocking_allocation")
        if allocation is not None and admissible_seed(record["mode"], allocation):
            seed_cuts.append((record["mode"], allocation))
            master.add(z3.Not(allocation_formula(allocation, value, record["mode"])))
    extra_seed_records = []
    for extra_seed_path in extra_seeds:
        extra = json.loads(extra_seed_path.read_text())
        records = extra.get("iterations", extra.get("rounds", []))
        for record in records:
            allocations = record.get("blocking_allocations")
            if allocations is None:
                single = record.get("blocking_allocation")
                allocations = [single] if single is not None else []
            for allocation in allocations:
                if not admissible_seed(record["mode"], allocation):
                    continue
                master.add(z3.Not(allocation_formula(allocation, value, record["mode"])))
                extra_seed_records.append((record["mode"], allocation))

    prior = json.loads(output.read_text()) if resume and output.exists() else None
    prior_rounds = [
        record for record in prior.get("rounds", [])
        if record.get("blocking_allocations")
    ] if prior else []
    for record in prior_rounds:
        for allocation in record["blocking_allocations"]:
            if not admissible_seed(record["mode"], allocation):
                continue
            master.add(z3.Not(allocation_formula(allocation, value, record["mode"])))

    result = {
        "schema": "fixed-u-rank-three-full-relation-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "seed": f"results/{seed_path.name}",
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "seed_cut_count": len(seed_cuts),
        "extra_seeds": [f"results/{path.name}" for path in extra_seeds],
        "extra_seed_cut_count": len(extra_seed_records),
        "seed_filter": (
            "complete-EFX seeds retained only when their selected provenance-edge "
            "count is within target_edge_bound; noncomplete global-maximality cuts "
            "are retained without this filter"
        ),
        "maximum_escapes_per_round": maximum_escapes,
        "radius_slack": radius_slack,
        "oracle_metric": oracle_metric,
        "target_edge_bound": target_edge_bound,
        "edge_origin": edge_origin,
        "random_seed": random_seed,
        "required_minimal_normal_form": required_minimal_normal_form,
        "exclude_self_responses": exclude_self_responses,
        "required_owner_cycle_form": required_owner_cycle_form,
        "exact_owner_cycle_response_relation": exact_owner_cycle_response_relation,
        "owner_cycle_form_index": owner_cycle_form_index,
        "rounds": prior_rounds,
        "response_gate": {
            "support_relation": (
                "union of all base-common-safe and same-state current-safe desired subsets"
            ),
            "support_rank_four_forbidden": True,
            "split_ordinary_rank_four_forbidden": True,
            "retained_named_cores": ["r:A", "q:Q", "s:E"],
            "unique_support_wall": "d strongly envies A; Q, E, and P are d-safe",
            "reassembly_relation": (
                "union of all base-common-safe and same-state current-safe desired subsets"
            ),
            "reassembly_mixed_rank_four_forbidden": True,
            "minimal_root_facing_normal_form_required": required_minimal_normal_form,
            "self_responses_excluded_from_matching": exclude_self_responses,
            "corrected_owner_cycle_form_required": required_owner_cycle_form,
            "exact_corrected_support_relation": exact_owner_cycle_response_relation,
        },
        "claim_boundary": (
            "exact twelve-atom CEGAR with necessary support-rank-three and mixed-"
            "reassembly-rank-three response gates; full signed-record reachability, "
            "deterministic priority selection, all Hall resets, and a genuine repeat "
            "remain unencoded, so SAT is not a recurrence countermodel and UNSAT is "
            "only a bounded-atom theorem"
        ),
    }
    checkpoint(output, result)
    for iteration in range(len(prior_rounds), maximum_iterations):
        status = master.check()
        record = {"iteration": iteration, "master_status": str(status)}
        result["rounds"].append(record)
        if status != z3.sat:
            result["status"] = str(status)
            if status == z3.unknown:
                result["reason_unknown"] = master.reason_unknown()
            checkpoint(output, result)
            return result
        values = fractions(master.model(), value)
        record["values"] = serialize_values(values)
        for mode in ("complete_efx", "efx_lex", "pareto"):
            radius, allocations, reason = oracle_menu(
                values, mode, maximum_escapes, radius_slack, oracle_metric,
                SUPPORT_STATE if edge_origin == "support" else None,
            )
            if reason is not None:
                result["status"] = "oracle_unknown"
                record["mode"] = mode
                record["reason_unknown"] = reason
                checkpoint(output, result)
                return result
            if (
                mode == "complete_efx"
                and target_edge_bound is not None
                and not allocations
            ):
                result["status"] = "sat_no_complete_efx_obstruction"
                result["countermodel_iteration"] = iteration
                record["mode"] = mode
                record["minimum_radius"] = None
                record["blocking_allocations"] = []
                checkpoint(output, result)
                return result
            if allocations:
                record["mode"] = mode
                record["minimum_radius"] = radius
                record["blocking_allocations"] = allocations
                if (
                    mode == "complete_efx"
                    and oracle_metric in ("edges", "functional_edges")
                    and target_edge_bound is not None
                    and radius > target_edge_bound
                ):
                    result["status"] = "sat_four_edge_obstruction"
                    result["countermodel_iteration"] = iteration
                    checkpoint(output, result)
                    return result
                for allocation in allocations:
                    master.add(z3.Not(allocation_formula(allocation, value, mode)))
                print(json.dumps({
                    "iteration": iteration,
                    "mode": mode,
                    "minimum_radius": radius,
                    "cuts": len(allocations),
                }), flush=True)
                break
        else:
            result["status"] = "sat_rank_three_packet_terminal_obstruction"
            result["countermodel_iteration"] = iteration
            checkpoint(output, result)
            return result
        checkpoint(output, result)
    result["status"] = "iteration_limit"
    checkpoint(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=50)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--maximum-escapes", type=int, default=64)
    parser.add_argument("--radius-slack", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--oracle-metric", choices=("goods", "edges", "functional_edges"),
        default="goods"
    )
    parser.add_argument("--extra-seed", type=Path, action="append", default=[])
    parser.add_argument("--target-edge-bound", type=int)
    parser.add_argument("--edge-origin", choices=("base", "support"), default="base")
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--require-minimal-normal-form", action="store_true")
    parser.add_argument("--exclude-self-responses", action="store_true")
    parser.add_argument("--require-owner-cycle-form", action="store_true")
    parser.add_argument("--exact-owner-cycle-response-relation", action="store_true")
    parser.add_argument("--owner-cycle-form-index", type=int, choices=range(4))
    args = parser.parse_args()
    result = run(
        args.seed, args.output, args.maximum_iterations, args.timeout_seconds,
        args.maximum_escapes, args.radius_slack, args.resume, args.oracle_metric,
        args.extra_seed, args.target_edge_bound, args.edge_origin, args.random_seed,
        args.require_minimal_normal_form,
        args.exclude_self_responses,
        args.require_owner_cycle_form,
        args.exact_owner_cycle_response_relation,
        args.owner_cycle_form_index,
    )
    print(json.dumps({"status": result["status"], "rounds": len(result["rounds"])}, indent=2))


if __name__ == "__main__":
    main()
