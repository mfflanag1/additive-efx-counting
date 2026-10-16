#!/usr/bin/env python3
"""Bounded exact audit of physical one-p-winner shortest-cycle release probes.

Input/loading and exhaustive core/cycle coverage come from extract_champion_cores.
Every probe value, physical deletion, and ownership check below is recomputed with
Fractions. No global maximality declaration, complete exit, or role layout is used.
The minimum cycle is selected BEFORE checking release hypotheses or probe outcomes.
This verifies a finite instance, never universal GG, ADMIT4, or an admission theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


_SPEC = importlib.util.spec_from_file_location(
    "cycle_release_champion_extractor", Path(__file__).with_name("extract_champion_cores.py"))
extractor = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = extractor
_SPEC.loader.exec_module(extractor)
Instance = extractor.Instance
load_instance = extractor.load_instance
parse_instance = extractor.parse_instance
INPUT_SCHEMA = extractor.INPUT_SCHEMA
OUTPUT_SCHEMA = "physical-cycle-release-audit-v1"
AGENTS = (0, 1, 2, 3)


def _values(instance: Instance) -> tuple[tuple[Fraction, ...], ...]:
    if type(instance.denominator) is not int or instance.denominator <= 0:
        raise ValueError("common denominator must be a positive integer")
    if (len(instance.values_scaled) != 4
            or any(len(row) != instance.m
                   or any(type(value) is not int or value <= 0 for value in row)
                   for row in instance.values_scaled)):
        raise ValueError("four positive integer value rows matching the goods are required")
    return tuple(tuple(Fraction(value, instance.denominator) for value in row)
                 for row in instance.values_scaled)


def _sum(values: tuple[tuple[Fraction, ...], ...], observer: int, goods: Any) -> Fraction:
    return sum((values[observer][g] for g in goods), Fraction(0))


def _scaled(instance: Instance, value: Fraction) -> int:
    result = value * instance.denominator
    if result.denominator != 1:
        raise RuntimeError("value is outside the exact input lattice")
    return result.numerator


def physical_allocation(instance: Instance, owners: Any) -> dict[str, Any]:
    """Independent ownership and all-good-deletion EFX oracle (no extractor calls)."""
    values = _values(instance)
    if (not isinstance(owners, (list, tuple)) or len(owners) != instance.m
            or any(i is not None and (type(i) is not int or i not in AGENTS) for i in owners)):
        raise ValueError("physical ownership must give every good exactly one owner or charity")
    bundles = [[g for g, owner in enumerate(owners) if owner == i] for i in AGENTS]
    pool = [g for g, owner in enumerate(owners) if owner is None]
    partition = [g for bundle in bundles for g in bundle] + pool
    if sorted(partition) != list(range(instance.m)) or len(set(partition)) != instance.m:
        raise RuntimeError("physical ownership failed conservation")
    own = [_sum(values, i, bundles[i]) for i in AGENTS]
    comparisons = []
    for observer in AGENTS:
        for target in AGENTS:
            for deleted in bundles[target]:
                rhs = _sum(values, observer, (g for g in bundles[target] if g != deleted))
                slack = own[observer] - rhs
                comparisons.append({"observer": observer, "target": target,
                                    "deleted_good": deleted,
                                    "lhs_scaled": _scaled(instance, own[observer]),
                                    "rhs_scaled": _scaled(instance, rhs),
                                    "slack_scaled": _scaled(instance, slack)})
    return {"base_owner": list(owners), "bundles": bundles, "charity": pool,
            "utilities_scaled": [_scaled(instance, value) for value in own],
            "utilities_exact": [str(value) for value in own],
            "efx_comparisons": comparisons,
            "is_efx": all(item["slack_scaled"] >= 0 for item in comparisons),
            "physical_conservation_verified": True}


def _base(instance: Instance) -> tuple[dict[str, Any], tuple[tuple[Fraction, ...], ...], list[Fraction], int]:
    values = _values(instance)
    base = physical_allocation(instance, instance.base_owner)
    if len(base["charity"]) != 1 or not base["is_efx"]:
        raise ValueError("base must be physical EFX with singleton charity")
    p = base["charity"][0]
    own = [_sum(values, i, base["bundles"][i]) for i in AGENTS]
    if any(own[i] < values[i][p] for i in AGENTS):
        raise ValueError("base singleton charity is not safe")
    return base, values, own, p


def validate_cycle(instance: Instance, selected_edges: Any) -> list[dict[str, Any]]:
    """Check physical hypotheses; supplied IDs, champions and slack claims are ignored."""
    base, values, own, p = _base(instance)
    if not isinstance(selected_edges, (list, tuple)) or not 2 <= len(selected_edges) <= 4:
        raise ValueError("cycle release requires a cycle of length two to four, with no self edge")
    edges = []
    for edge in selected_edges:
        if not isinstance(edge, dict):
            raise ValueError("each cycle edge must be an object")
        source, target, goods = edge.get("source"), edge.get("target"), edge.get("goods")
        if any(type(i) is not int or i not in AGENTS for i in (source, target)) or source == target:
            raise ValueError("cycle endpoints must be distinct physical agents 0..3")
        if (not isinstance(goods, (list, tuple)) or not goods
                or any(type(g) is not int or not 0 <= g < instance.m for g in goods)
                or len(set(goods)) != len(goods)):
            raise ValueError("core goods must be a nonempty physical set")
        goods = sorted(goods)
        old_target = set(base["bundles"][target])
        if not set(goods) <= old_target | {p}:
            raise ValueError("nonphysical core: not contained in its target bundle plus p")
        contains_p = p in goods
        retained = sorted(set(goods) - {p}) if contains_p else goods
        residual = sorted(old_target - set(retained)) if contains_p else []
        if contains_p and (not retained or not set(retained) < old_target):
            raise ValueError("p-core retained part must be a nonempty proper target subset")
        if not contains_p and set(goods) != old_target:
            raise ValueError("ordinary core must equal the whole old target bundle")
        if _sum(values, source, goods) <= own[source]:
            raise ValueError("source is not a strict champion of its physical core")
        deletions = []
        for observer in AGENTS:
            for deleted in goods:
                slack = own[observer] - _sum(values, observer, (g for g in goods if g != deleted))
                if slack < 0:
                    raise ValueError("physical core is not common-safe at the old floors")
                deletions.append({"observer": observer, "deleted_good": deleted,
                                  "slack_scaled": _scaled(instance, slack)})
        edges.append({"source": source, "target": target, "goods": goods,
                      "kind": "p_core" if contains_p else "ordinary", "retained": retained,
                      "residual": residual, "common_safe_deletions": deletions})
    sources = [edge["source"] for edge in edges]
    if (len(set(sources)) != len(sources)
            or any(edge["target"] != edges[(index + 1) % len(edges)]["source"]
                   for index, edge in enumerate(edges))):
        raise ValueError("edges must follow one source-to-target directed simple cycle")
    if sum(edge["kind"] == "p_core" for edge in edges) < 2:
        raise ValueError("cycle release requires at least two p-containing edges")
    return edges


def priority_compatible_winners(edges: list[dict[str, Any]]) -> list[int]:
    earliest = min(edge["source"] for edge in edges)
    p_sources = sorted(edge["source"] for edge in edges if edge["kind"] == "p_core")
    return [earliest] if earliest in p_sources else p_sources


def _release_owners(instance: Instance, edges: list[dict[str, Any]], winner: int) -> list[int | None]:
    """Physical assignment only; release and return impose different winner rules."""
    sources = {edge["source"] for edge in edges}
    owners = [owner if owner not in sources else None for owner in instance.base_owner]
    for edge in edges:
        recipient = edge["source"]
        assigned = edge["goods"] if recipient == winner or edge["kind"] == "ordinary" else edge["retained"]
        for good in assigned:
            if owners[good] is not None:
                raise ValueError("probe duplicates or steals an already-owned physical good")
            owners[good] = recipient
    return owners


def construct_cycle_release_probe(instance: Instance, selected_edges: Any, winner: int,
                                  *, claimed_owners: Any = None) -> dict[str, Any]:
    """Rebuild and verify one physical probe; optional ownership claims must match exactly."""
    base, values, own, p = _base(instance)
    edges = validate_cycle(instance, selected_edges)
    compatible = priority_compatible_winners(edges)
    if type(winner) is not int or winner not in compatible:
        raise ValueError("p winner must be a priority-compatible p-edge SOURCE")
    sources = {edge["source"] for edge in edges}
    unpaid = sorted(edge["source"] for edge in edges
                    if edge["kind"] == "p_core" and edge["source"] != winner)
    owners = _release_owners(instance, edges, winner)
    if claimed_owners is not None:
        physical_allocation(instance, claimed_owners)
        if list(claimed_owners) != owners:
            raise ValueError("claimed ownership disagrees with the physical source-to-target release")
    result = physical_allocation(instance, owners)
    pool = sorted(g for edge in edges for g in edge["residual"])
    if result["charity"] != pool or owners[p] != winner:
        raise RuntimeError("pool is not exactly the p-target residual union, with p used once")
    if any(result["bundles"][i] != base["bundles"][i] for i in AGENTS if i not in sources):
        raise RuntimeError("nonparticipant bundle changed")
    after = [_sum(values, i, result["bundles"][i]) for i in AGENTS]
    if not tuple(after) > tuple(own):
        raise RuntimeError("probe failed fixed-priority 0,1,2,3 strict improvement")
    deficits = []
    for source in unpaid:
        deficit = own[source] - after[source]
        if not 0 <= deficit < values[source][p]:
            raise RuntimeError("unpaid source deficit is outside [0, v_source(p))")
        deficits.append({"source": source, "deficit_scaled": _scaled(instance, deficit),
                         "deficit_exact": str(deficit), "p_value_scaled": _scaled(instance, values[source][p]),
                         "lower_bound_is_strict": deficit > 0})
    if any(after[i] < own[i] for i in AGENTS if i not in unpaid):
        raise RuntimeError("a paid, ordinary or external observer lost own utility")
    common_safe = []
    violations = []
    source_kind = {edge["source"]: edge["kind"] for edge in edges}
    for item in result["efx_comparisons"]:
        observer, target = item["observer"], item["target"]
        old_slack = base["utilities_scaled"][observer] - item["rhs_scaled"]
        common_safe.append({"observer": observer, "target": target,
                            "deleted_good": item["deleted_good"], "old_floor_slack_scaled": old_slack})
        if old_slack < 0:
            raise RuntimeError("probe recipient failed common safety at original O floors")
        if item["slack_scaled"] >= 0:
            continue
        if observer not in unpaid:
            raise RuntimeError("physical EFX violation comes from a non-unpaid observer")
        deficit = own[observer] - after[observer]
        shortfall = Fraction(-item["slack_scaled"], instance.denominator)
        if not 0 < shortfall <= deficit < values[observer][p]:
            raise RuntimeError("EFX shortfall exceeds its unpaid source deficit or charity value")
        kind = ("winner" if target == winner else "external_fixed" if target not in sources
                else "other_trimmed" if source_kind[target] == "p_core" else "ordinary")
        violations.append({**item, "target_kind": kind,
                           "shortfall_scaled": _scaled(instance, shortfall),
                           "source_deficit_scaled": _scaled(instance, deficit),
                           "p_value_scaled": _scaled(instance, values[observer][p])})
    tail_deficits = []
    for source in unpaid:
        physical_tails = [max((_sum(values, source, (g for g in bundle if g != deleted))
                              for deleted in bundle), default=Fraction(0))
                          for bundle in result["bundles"]]
        shortfall = max(Fraction(0), max(physical_tails) - after[source])
        tail_deficits.append({"source": source, "tail_deficit_scaled": _scaled(instance, shortfall),
                              "tail_deficit_exact": str(shortfall),
                              "physical_tails_scaled": [_scaled(instance, value) for value in physical_tails]})
    result.update({"winner": winner, "unpaid_sources": unpaid, "p_edge_count": len(unpaid) + 1,
                   "source_deficits": deficits, "tail_deficits": tail_deficits,
                   "utility_gains_scaled": [_scaled(instance, after[i] - own[i]) for i in AGENTS],
                   "fixed_priority_lexicographic_improvement": True,
                   "priority": list(AGENTS), "pool_equals_residual_union": True,
                   "charity_good_used_exactly_once": True, "unchanged_nonparticipants": True,
                   "common_safe_old_floor_deletions": common_safe,
                   "all_recipients_common_safe_at_old_floors": True,
                   "all_other_observers_weakly_improve": True,
                   "every_violation_has_unpaid_observer": True,
                   "every_shortfall_at_most_source_deficit_and_below_p": True,
                   "efx_violations": violations,
                   "outcome": "genuine_efx_lex_improvement" if result["is_efx"] else "unpaid_observer_obstruction",
                   "excluded_if_input_is_global_lexmax": result["is_efx"]})
    return result


def residual_return_plan(edges: list[dict[str, Any]]) -> dict[str, Any]:
    """Count ordinary runs on an already validated directed cycle, without filtering."""
    starts = [edge["source"] for index, edge in enumerate(edges)
              if edge["kind"] == "p_core" and edges[index - 1]["kind"] == "ordinary"]
    runs = len(starts)
    winners = sorted(edge["source"] for edge in edges) if runs == 0 else starts if runs == 1 else []
    return {"ordinary_run_count": runs,
            "status": "mechanism_not_guaranteed" if runs > 1 else "verified_mechanism_instance",
            "return_compatible_winners": sorted(winners),
            "winner_rule": "All-G: any cycle source. One ordinary run: the unique incoming-ordinary/outgoing-G source. Multiple runs: no all-paid guarantee."}


def construct_cycle_return_probe(instance: Instance, selected_edges: Any, winner: int,
                                 *, claimed_owners: Any = None) -> dict[str, Any]:
    """Return every released D_j to original owner j, checking all physical deletions.

    At most one ordinary run and owner residual payments imply a complete strict
    Pareto improvement. They DO NOT imply EFX of the augmented junction bundles.
    """
    base, values, own, p = _base(instance)
    edges = validate_cycle(instance, selected_edges)
    plan = residual_return_plan(edges)
    if plan["ordinary_run_count"] > 1:
        raise ValueError("mechanism_not_guaranteed: residual return has multiple ordinary runs")
    if type(winner) is not int or winner not in plan["return_compatible_winners"]:
        raise ValueError("winner is not return-compatible with the ordinary-run structure")
    payments = []
    for edge in edges:
        if edge["kind"] != "p_core":
            continue
        target = edge["target"]
        payment = _sum(values, target, edge["residual"])
        if payment < values[target][p]:
            raise ValueError("G-target residual does not pay its original owner's p value")
        payments.append({"owner": target, "residual": edge["residual"],
                         "residual_value_scaled": _scaled(instance, payment),
                         "p_value_scaled": _scaled(instance, values[target][p]),
                         "payment_slack_scaled": _scaled(instance, payment - values[target][p])})
    owners = _release_owners(instance, edges, winner)
    released = physical_allocation(instance, owners)
    residual_union = sorted(g for edge in edges for g in edge["residual"])
    if released["charity"] != residual_union or owners[p] != winner:
        raise RuntimeError("residual return did not start from the exact physical release pool")
    for edge in edges:
        for good in edge["residual"]:
            if owners[good] is not None or instance.base_owner[good] != edge["target"]:
                raise RuntimeError("returned residual is not its original owner's unused physical good")
            owners[good] = edge["target"]
    if claimed_owners is not None:
        physical_allocation(instance, claimed_owners)
        if list(claimed_owners) != owners:
            raise ValueError("claimed ownership disagrees with physical residual return")
    result = physical_allocation(instance, owners)
    sources = {edge["source"] for edge in edges}
    junctions = sorted(edge["target"] for edge in edges if edge["kind"] == "p_core")
    after = [_sum(values, i, result["bundles"][i]) for i in AGENTS]
    if result["charity"] or owners[p] != winner:
        raise RuntimeError("residual-return probe is not complete with p used exactly once")
    if any(after[i] <= own[i] for i in sources):
        raise RuntimeError("residual return failed strict improvement for a participant")
    if any(result["bundles"][i] != base["bundles"][i] for i in AGENTS if i not in sources):
        raise RuntimeError("residual return changed a nonparticipant")
    if not tuple(after) > tuple(own):
        raise RuntimeError("residual return failed fixed-priority lex improvement")
    old_floor_failures, violations = [], []
    for item in result["efx_comparisons"]:
        old_slack = base["utilities_scaled"][item["observer"]] - item["rhs_scaled"]
        if old_slack < 0:
            old_floor_failures.append({**item, "old_floor_slack_scaled": old_slack})
            if item["target"] not in junctions:
                raise RuntimeError("a non-junction target lost original-floor common safety")
        if item["slack_scaled"] < 0:
            if item["target"] not in junctions:
                raise RuntimeError("residual-return EFX violation targets a non-junction bundle")
            violations.append({**item, "target_kind": "augmented_junction",
                               "shortfall_scaled": -item["slack_scaled"]})
    result.update({"winner": winner, "ordinary_run_count": plan["ordinary_run_count"],
                   "release_bundles": released["bundles"], "released_residual_pool": residual_union,
                   "returned_residual_payments": payments, "junction_targets": junctions,
                   "utility_gains_scaled": [_scaled(instance, after[i] - own[i]) for i in AGENTS],
                   "complete": True, "strict_for_every_participant": True,
                   "is_pareto_improvement": True, "unchanged_nonparticipants": True,
                   "fixed_priority_lexicographic_improvement": True,
                   "charity_good_used_exactly_once": True,
                   "non_junction_targets_common_safe_at_old_floors": True,
                   "every_violation_targets_augmented_junction": True,
                   "old_floor_common_safety_violations": old_floor_failures,
                   "efx_violations": violations,
                   "outcome": "genuine_complete_efx_improvement" if result["is_efx"] else "augmented_junction_obstruction",
                   "excluded_if_input_is_global_lexmax": result["is_efx"],
                   "unconditional_complete_efx_claimed": False})
    return result


def _cycle_key(cycle: dict[str, Any], p: int) -> tuple[Any, ...]:
    return (len(cycle["edges"]), sum(p in edge["goods"] for edge in cycle["edges"]),
            tuple((edge["source"], edge["target"], tuple(sorted(edge["goods"])), edge["core_id"])
                  for edge in cycle["edges"]))


def audit(instance: Instance, *, max_decorated_cycles: int = 100000) -> dict[str, Any]:
    base, values, own, p = _base(instance)
    coverage = extractor.audit(instance, max_decorated_cycles=max_decorated_cycles)
    cycles = coverage["decorated_cycles"]
    canonical = min(cycles, key=lambda cycle: _cycle_key(cycle, p)) if cycles else None
    report = {"schema": OUTPUT_SCHEMA, "status": "not_applicable", "n": 4, "m": instance.m,
              "agent_order": list(AGENTS), "arithmetic": {"method": "Independent Fraction values and physical-good deletions.",
                 "common_denominator": instance.denominator, "values_scaled": [list(row) for row in instance.values_scaled]},
              "base_allocation": base, "exhaustive_coverage": coverage["summary"],
              "selection_rule": "All decorated cycles: minimum length, then minimum p-edge count, then stable source/target/goods/core-id order; no favorable-outcome filtering.",
              "canonical_cycle": None if canonical is None else {
                  "vertices": canonical["vertices"], "edges": canonical["edges"],
                  "p_edge_count": canonical["charity_occurrences"]},
              "probes": [], "residual_return": {"status": "not_applicable", "probes": []}, "claims_boundary": {
                  "global_lexmax_verified": False, "global_maximality_claims_from_archive_used": False,
                  "complete_exit_claims_used": False, "nondegeneracy_required": False,
                  "universal_gg_claimed": False, "admit4_claimed": False,
                  "universal_admission_theorem_verified": False,
                  "physical_fixed_U_role_layout_constructed": False,
                  "conditional_meaning": "An EFX probe is a genuine fixed-priority improving partial allocation, excluded if the input additionally is globally lexmax. A failing probe only localizes its exact unpaid-observer obstructions."}}
    if canonical is None:
        report["not_applicable_reason"] = "No decorated cycle was found; no theorem is verified."
        return report
    try:
        edges = validate_cycle(instance, canonical["edges"])
    except ValueError as error:
        report["not_applicable_reason"] = str(error)
        return report
    vertices = {edge["source"] for edge in edges}
    successor = {edge["source"]: edge["target"] for edge in edges}
    chords = [edge for edge in coverage["champion_records"]
              if edge["source"] in vertices and edge["target"] in vertices
              and edge["target"] != successor[edge["source"]]]
    if chords:
        raise RuntimeError("canonical shortest cycle has an internal non-successor champion edge")
    parallel_checks = []
    for edge in edges:
        if edge["kind"] != "p_core":
            continue
        source, target = edge["source"], edge["target"]
        gap = own[source] - _sum(values, source, base["bundles"][target])
        if gap < 0:
            raise RuntimeError("minimum-p shortest cycle has parallel ordinary envy on a p edge")
        parallel_checks.append({"source": source, "target": target,
                                "ordinary_nonenvy_slack_scaled": _scaled(instance, gap)})
    winners = priority_compatible_winners(edges)
    return_plan = residual_return_plan(edges)
    return_plan["probes"] = [construct_cycle_return_probe(instance, edges, winner)
                              for winner in return_plan["return_compatible_winners"]]
    report.update({"status": "verified_instance", "validated_cycle_edges": edges,
                   "shortest_cycle_checks": {"no_internal_non_successor_champion_edges": True,
                                              "no_parallel_ordinary_envy_on_selected_p_edge": True,
                                              "parallel_ordinary_checks": parallel_checks},
                   "priority_compatible_winners": winners,
                   "residual_return": return_plan,
                   "probes": [construct_cycle_release_probe(instance, edges, winner) for winner in winners]})
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--archive", action="store_true")
    parser.add_argument("--max-goods", type=int, default=20)
    parser.add_argument("--max-decorated-cycles", type=int, default=100000)
    args = parser.parse_args(argv)
    try:
        instance = load_instance(args.input, archive=args.archive, max_goods=args.max_goods)
        report = audit(instance, max_decorated_cycles=args.max_decorated_cycles)
    except (ValueError, OSError, RuntimeError) as error:
        print(f"cycle-release audit rejected input: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
