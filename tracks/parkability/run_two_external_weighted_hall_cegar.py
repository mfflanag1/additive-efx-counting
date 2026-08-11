#!/usr/bin/env python3
"""CEGAR the complete minimal-payment residual-partition closure menu."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .analyze_flexible_lex_radius3_hardness_gap import desired_subsets
    from .analyze_flexible_two_external_weighted_hall import (
        BOTTOM_Q,
        BOTTOM_R,
        TOP_Q,
        TOP_R,
        find_sdr,
        is_efx,
        minimal_payment_packets,
    )
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
    )
    from .decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from .decide_flexible_later_owner_topology_menu import (
        build_master,
        fractions,
        true_tail,
    )
    from .run_flexible_lex_allocation_cegar import add_live_constraints, sha256
    from .run_flexible_lex_self_pi_free_cegar import (
        add_no_envy_cycles,
        add_no_self_champions,
        add_no_single_genuine_cycles,
    )
    from .analyze_weighted_hall_owner_union_compressions import (
        find_owner_union_closure,
    )
except ImportError:
    from analyze_flexible_lex_radius3_hardness_gap import desired_subsets
    from analyze_flexible_two_external_weighted_hall import (
        BOTTOM_Q,
        BOTTOM_R,
        TOP_Q,
        TOP_R,
        find_sdr,
        is_efx,
        minimal_payment_packets,
    )
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
    )
    from decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from decide_flexible_later_owner_topology_menu import (
        build_master,
        fractions,
        true_tail,
    )
    from run_flexible_lex_allocation_cegar import add_live_constraints, sha256
    from run_flexible_lex_self_pi_free_cegar import (
        add_no_envy_cycles,
        add_no_self_champions,
        add_no_single_genuine_cycles,
    )
    from analyze_weighted_hall_owner_union_compressions import (
        find_owner_union_closure,
    )


def allocation_key(allocation):
    return tuple(tuple(sorted(allocation[recipient])) for recipient in (*AGENTS, "_"))


def moved_good_count(old, allocation):
    base_owner = {
        good: recipient
        for recipient, goods in {**old, "_": ("f",)}.items()
        for good in goods
    }
    return sum(
        good not in allocation[base_owner[good]]
        for good in base_owner
    )


def find_closure(values, old):
    base_value = {
        agent: sum((values[agent][good] for good in old[agent]), Fraction())
        for agent in AGENTS
    }
    response_cache = {}
    examined = 0

    def response_sources(offer):
        key = tuple(sorted(offer))
        if key not in response_cache:
            response_cache[key] = sorted(
                source
                for source in AGENTS
                if desired_subsets(values, base_value, source, key)
            )
        return response_cache[key]

    payments = minimal_payment_packets(values)
    for payment in payments:
        residual = tuple(good for good in TOP_R if good not in payment) + BOTTOM_R
        root_core = TOP_Q + ("f",)
        evolved_q = BOTTOM_Q + payment
        for destinations in itertools.product(("r", "c", "s", "_"), repeat=len(residual)):
            examined += 1
            cells = {recipient: [] for recipient in ("r", "c", "s", "_")}
            for good, recipient in zip(residual, destinations):
                cells[recipient].append(good)
            allocation = {
                "r": tuple(root_core + tuple(cells["r"])),
                "q": tuple(evolved_q),
                "c": tuple(old["c"] + tuple(cells["c"])),
                "s": tuple(old["s"] + tuple(cells["s"])),
                "_": tuple(cells["_"]),
            }
            targets = ("r", "q") + tuple(
                owner for owner in ("c", "s") if cells[owner]
            )
            if is_efx(values, allocation):
                assert lex_endpoint_succeeds(values, old, allocation)
                return {
                    "kind": "EFX",
                    "payment": payment,
                    "allocation": allocation,
                    "targets": targets,
                    "examined_partitions": examined,
                }
            response = {
                target: sorted(set(response_sources(allocation[target])).intersection(targets))
                for target in targets
            }
            matching = find_sdr(targets, response)
            if matching is not None:
                return {
                    "kind": "INTERNAL_SDR",
                    "payment": payment,
                    "allocation": allocation,
                    "targets": targets,
                    "response": response,
                    "matching": matching,
                    "examined_partitions": examined,
                }
    return {
        "kind": "NONE",
        "minimal_payment_packets": payments,
        "examined_partitions": examined,
        "response_offer_cache_size": len(response_cache),
    }


def minimal_payment_formula(payment, value):
    payment_total = z3.Sum(*(value[good, "q"] for good in payment))
    top_q_total = z3.Sum(*(value[good, "q"] for good in TOP_Q))
    return z3.And(
        payment_total > top_q_total,
        *(
            z3.Sum(*(value[good, "q"] for good in payment if good != removed))
            <= top_q_total
            for removed in payment
        ),
    )


def run(
    output_path,
    maximum_iterations,
    timeout_seconds,
    exclude_connected_radius=0,
    separate_connected_radius=0,
):
    solver, atoms, old, symbolic_value, base = build_master()
    symmetry_count = add_live_constraints(solver, atoms, symbolic_value, symmetry=True)
    basic_counts = {
        "self_champion_subsets": add_no_self_champions(
            solver, old, symbolic_value, base
        ),
        "ordinary_envy_cycles": add_no_envy_cycles(
            solver, old, symbolic_value, base
        ),
        "single_genuine_cycles": add_no_single_genuine_cycles(
            solver, old, symbolic_value, base
        ),
    }
    excluded_connected = ()
    if exclude_connected_radius:
        excluded_connected = enumerate_connected(
            old,
            radius=exclude_connected_radius,
            rooted=False,
            structural_reductions=False,
        )
        for allocation in excluded_connected:
            solver.add(z3.Not(endpoint_formula(
                allocation, old, symbolic_value, base, "lex"
            )))
    separated_connected = ()
    if separate_connected_radius:
        separated_connected = enumerate_connected(
            old,
            radius=separate_connected_radius,
            rooted=False,
            structural_reductions=False,
        )
    solver.set(timeout=timeout_seconds * 1000)
    champion_cache = {}

    def champion_formula(source, offer):
        offer = tuple(sorted(offer))
        key = (source, offer)
        if key not in champion_cache:
            witnesses = []
            for size in range(1, len(offer) + 1):
                for subset in itertools.combinations(offer, size):
                    witnesses.append(z3.And(
                        z3.Sum(*(symbolic_value[good, source] for good in subset))
                        > base[source],
                        *(
                            true_tail([
                                symbolic_value[good, observer] for good in subset
                            ]) <= base[observer]
                            for observer in AGENTS
                        ),
                    ))
            champion_cache[key] = z3.Or(*witnesses)
        return champion_cache[key]

    installed = set()
    iterations = []
    script = Path(__file__).resolve()
    root = script.parents[2]
    result = {
        "schema": "two-external-weighted-hall-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "live_polarity": True,
        "symmetry_constraint_count": symmetry_count,
        "basic_pi_free_constraints": basic_counts,
        "excluded_connected_lex_radius": exclude_connected_radius,
        "excluded_connected_lex_allocation_count": len(excluded_connected),
        "separated_connected_lex_radius": separate_connected_radius,
        "separated_connected_lex_allocation_count": len(separated_connected),
        "iterations": iterations,
        "claim_boundary": (
            "bounded two-atom representative decision for closure over every "
            "minimal-payment residual partition; UNSAT is only a bounded theorem "
            "candidate, while SAT requires an exact nondegenerate audit"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {
            "iteration": iteration,
            "master_status": str(checked),
            "installed_closure_count": len(installed),
        }
        iterations.append(record)
        if checked == z3.unsat:
            result["status"] = "unsat"
            output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result
        if checked == z3.unknown:
            result["status"] = "unknown"
            result["reason_unknown"] = solver.reason_unknown()
            output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result
        model = solver.model()
        values = fractions(model, atoms, symbolic_value)
        closure = find_closure(values, old)
        record["closure_kind"] = closure["kind"]
        record["examined_partitions"] = closure["examined_partitions"]
        if closure["kind"] == "NONE":
            owner_union_closure = find_owner_union_closure(values, old)
            if owner_union_closure["kind"] != "NONE":
                closure = owner_union_closure
                record["closure_kind"] = closure["kind"]
                record["owner_union_path"] = closure["path"]
                record["recapture_states_examined"] = closure.get(
                    "states_examined", 0
                )
                record["owner_union_growth_steps"] = closure.get(
                    "growth_steps", 0
                )
        if closure["kind"] == "NONE":
            connected_escape = next(
                (
                    allocation for allocation in separated_connected
                    if lex_endpoint_succeeds(values, old, allocation)
                ),
                None,
            )
            if connected_escape is not None:
                key = ("GLOBAL_LEX_ESCAPE", allocation_key(connected_escape))
                if key in installed:
                    raise AssertionError(
                        "global separation oracle returned an installed escape"
                    )
                installed.add(key)
                solver.add(z3.Not(endpoint_formula(
                    connected_escape, old, symbolic_value, base, "lex"
                )))
                record["closure_kind"] = "GLOBAL_LEX_ESCAPE"
                record["allocation"] = {
                    recipient: list(goods)
                    for recipient, goods in connected_escape.items()
                }
                record["moved_good_count"] = moved_good_count(
                    old, connected_escape
                )
                output_path.write_text(
                    json.dumps(result, indent=2, sort_keys=True) + "\n"
                )
                print(json.dumps({
                    "iteration": iteration,
                    "closure_kind": "GLOBAL_LEX_ESCAPE",
                    "installed_closure_count": len(installed),
                    "moved_good_count": record["moved_good_count"],
                }, sort_keys=True), flush=True)
                continue
            result["status"] = "sat_no_closure"
            result["countermodel_iteration"] = iteration
            result["countermodel_diagnostics"] = {
                key: value for key, value in closure.items() if key != "kind"
            }
            result["values"] = {
                agent: {good: str(amount) for good, amount in row.items()}
                for agent, row in values.items()
            }
            output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            return result

        allocation = closure["allocation"]
        key = (
            closure["kind"],
            tuple(closure["payment"]),
            allocation_key(allocation),
            tuple(sorted((closure.get("matching") or {}).items())),
        )
        if key in installed:
            raise AssertionError("separation oracle returned an installed closure")
        installed.add(key)
        minimal = minimal_payment_formula(closure["payment"], symbolic_value)
        if closure["kind"] == "EFX":
            closes = endpoint_formula(
                allocation, old, symbolic_value, base, "lex"
            )
        else:
            closes = z3.And(*(
                champion_formula(closure["matching"][target], allocation[target])
                for target in closure["targets"]
            ))
        solver.add(z3.Not(z3.And(minimal, closes)))
        record["payment_packet"] = list(closure["payment"])
        record["allocation"] = {
            recipient: list(goods) for recipient, goods in allocation.items()
        }
        record["targets"] = list(closure["targets"])
        record["matching"] = closure.get("matching")
        output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps({
            "iteration": iteration,
            "closure_kind": closure["kind"],
            "installed_closure_count": len(installed),
            "payment_packet": list(closure["payment"]),
            "targets": list(closure["targets"]),
            "matching": closure.get("matching"),
        }, sort_keys=True), flush=True)
    result["status"] = "iteration_limit"
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=100)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--exclude-connected-radius", type=int, default=0)
    parser.add_argument("--separate-connected-radius", type=int, default=0)
    args = parser.parse_args()
    result = run(
        args.output.resolve(),
        args.maximum_iterations,
        args.timeout_seconds,
        args.exclude_connected_radius,
        args.separate_connected_radius,
    )
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
