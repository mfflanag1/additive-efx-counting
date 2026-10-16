#!/usr/bin/env python3
"""Exact physical minimal-envied cores and decorated champion-cycle audit.

Standalone input is {schema: INPUT_SCHEMA, n: 4, m: ..., agent_order: [0,1,2,3],
values: four positive rational rows, candidate: {base_owner: [0..3 or null]}}.
Exactly one good must be in charity; the base allocation must be EFX and every
agent must weakly prefer its own bundle to that good. JSON decimals are read as
Fractions, never binary floats. The explicit --archive loader instead reads
arithmetic.values_scaled/common_denominator from the selector exact-audit schema.

All nonempty subsets of O_j + p are tested, including cores not containing p.
Every champion of every inclusion-minimal envied core is retained. All directed
simple cycles (including self-loops), with every choice of a core on each edge,
are examined. A disjoint-core cycle yields a physical EFX Pareto improvement;
Unused goods return to charity, which need not remain a singleton. The EFX
verification does not require a charity-safety assumption on the output.
Thus global lexmax over ALL partial EFX allocations excludes such cycles. This
script does not test that global premise or assert a downstream graph normal form.
No full allocation-space enumeration or project helper is used.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from math import lcm, prod
from pathlib import Path
import sys
from typing import Any


INPUT_SCHEMA = "physical-champion-cores-input-v1"
ARCHIVE_SCHEMA = "selector-compatibility-independent-audit-v1"
OUTPUT_SCHEMA = "physical-champion-cores-audit-v1"
AGENTS = (0, 1, 2, 3)


@dataclass(frozen=True)
class Instance:
    values_scaled: tuple[tuple[int, ...], ...]
    denominator: int
    base_owner: tuple[int | None, ...]

    @property
    def m(self) -> int:
        return len(self.base_owner)


def _rational(value: Any, location: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError(f"{location}: expected an exact integer or rational")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError, OverflowError) as error:
        raise ValueError(f"{location}: invalid rational") from error
    if result <= 0:
        raise ValueError(f"{location}: values must be strictly positive")
    return result


def _owners(value: Any, m: int) -> tuple[int | None, ...]:
    if not isinstance(value, (list, tuple)) or len(value) != m:
        raise ValueError(f"base_owner must contain exactly {m} entries")
    if any(owner is not None and (type(owner) is not int or owner not in AGENTS) for owner in value):
        raise ValueError("each physical good must have owner 0..3 or null")
    return tuple(value)


def allocation_record(instance: Instance, owners: Any) -> dict[str, Any]:
    """Independently check conservation and every physical deleted-good EFX test."""
    owners = _owners(owners, instance.m)
    bundles = [[g for g, owner in enumerate(owners) if owner == i] for i in AGENTS]
    charity = [g for g, owner in enumerate(owners) if owner is None]
    own = [sum(instance.values_scaled[i][g] for g in bundles[i]) for i in AGENTS]
    comparisons = []
    for i in AGENTS:
        for j in AGENTS:
            for deleted in bundles[j]:
                rhs = sum(instance.values_scaled[i][g] for g in bundles[j] if g != deleted)
                comparisons.append({"observer": i, "target": j, "deleted_good": deleted,
                                    "lhs_scaled": own[i], "rhs_scaled": rhs,
                                    "slack_scaled": own[i] - rhs})
    charity_slacks = [own[i] - sum(instance.values_scaled[i][g] for g in charity) for i in AGENTS]
    return {"base_owner": list(owners), "bundles": bundles, "charity": charity,
            "utilities_scaled": own, "efx_comparisons": comparisons,
            "is_efx": all(test["slack_scaled"] >= 0 for test in comparisons),
            "charity_nonenvy_slacks_scaled": charity_slacks,
            "whole_charity_nonenvy": all(slack >= 0 for slack in charity_slacks)}


def _validated_base(instance: Instance) -> dict[str, Any]:
    if type(instance.denominator) is not int or instance.denominator <= 0:
        raise ValueError("common_denominator must be a positive integer")
    if (len(instance.values_scaled) != 4
            or any(len(row) != instance.m or any(type(v) is not int or v <= 0 for v in row)
                   for row in instance.values_scaled)):
        raise ValueError("values_scaled must have four positive integer rows matching the goods")
    base = allocation_record(instance, instance.base_owner)
    if len(base["charity"]) != 1:
        raise ValueError("base allocation must have exactly one charity good")
    if not base["is_efx"]:
        raise ValueError("base allocation is not EFX")
    if not base["whole_charity_nonenvy"]:
        raise ValueError("the single charity good is not safe")
    return base


def _check_declarations(candidate: dict[str, Any], base: dict[str, Any]) -> None:
    for key in ("bundles", "charity"):
        if key not in candidate:
            continue
        declared = candidate[key]
        if key == "bundles":
            valid = (isinstance(declared, list) and len(declared) == 4
                     and all(isinstance(bundle, list) and all(type(g) is int for g in bundle)
                             for bundle in declared)
                     and [sorted(bundle) for bundle in declared] == base[key])
        else:
            valid = (isinstance(declared, list) and all(type(g) is int for g in declared)
                     and sorted(declared) == base[key])
        if not valid:
            raise ValueError(f"candidate.{key} disagrees with physical ownership")
    for key in ("utilities_scaled", "charity_nonenvy_slacks_scaled"):
        if key in candidate and (not isinstance(candidate[key], list)
                or any(type(v) is not int for v in candidate[key]) or candidate[key] != base[key]):
            raise ValueError(f"candidate.{key} disagrees with the recomputed allocation")
    for key in ("is_efx", "whole_charity_nonenvy"):
        if key in candidate and (type(candidate[key]) is not bool or candidate[key] != base[key]):
            raise ValueError(f"candidate.{key} disagrees with the recomputed allocation")


def parse_instance(document: Any, *, max_goods: int = 20, archive: bool = False) -> Instance:
    if type(max_goods) is not int or max_goods < 1:
        raise ValueError("max_goods must be a positive integer")
    schema = ARCHIVE_SCHEMA if archive else INPUT_SCHEMA
    if not isinstance(document, dict) or document.get("schema") != schema:
        raise ValueError(f"schema must be {schema!r}; use --archive only for the exact selector archive")
    if type(document.get("n")) is not int or document["n"] != 4:
        raise ValueError("exactly four agents are required")
    m = document.get("m")
    if type(m) is not int or not 1 <= m <= max_goods:
        raise ValueError(f"m must be between 1 and max_goods={max_goods}")
    order = document.get("agent_order")
    if not isinstance(order, list) or any(type(i) is not int for i in order) or order != list(AGENTS):
        raise ValueError("agent_order must be exactly [0, 1, 2, 3]")
    if archive:
        arithmetic = document.get("arithmetic")
        if not isinstance(arithmetic, dict):
            raise ValueError("archive arithmetic must be an object")
        denominator = arithmetic.get("common_denominator")
        if type(denominator) is not int or denominator <= 0:
            raise ValueError("archive common_denominator must be a positive integer")
        rows = arithmetic.get("values_scaled")
    else:
        rows = document.get("values")
    if not isinstance(rows, list) or len(rows) != 4 or any(not isinstance(row, list) or len(row) != m for row in rows):
        raise ValueError("values must contain four rows of m values")
    if archive:
        if any(type(value) is not int or value <= 0 for row in rows for value in row):
            raise ValueError("archive values_scaled must be strictly positive integers")
        scaled = tuple(tuple(row) for row in rows)
    else:
        values = tuple(tuple(_rational(v, f"values[{i}][{g}]") for g, v in enumerate(row))
                       for i, row in enumerate(rows))
        denominator = lcm(*(v.denominator for row in values for v in row))
        scaled = tuple(tuple(int(v * denominator) for v in row) for row in values)
    candidate = document.get("candidate")
    if not isinstance(candidate, dict):
        raise ValueError("candidate must be an object containing base_owner")
    instance = Instance(scaled, denominator, _owners(candidate.get("base_owner"), m))
    _check_declarations(candidate, _validated_base(instance))
    return instance


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON number: {token}")


def load_instance(path: str | Path, *, archive: bool = False, max_goods: int = 20) -> Instance:
    with Path(path).open(encoding="utf-8") as stream:
        document = json.load(stream, parse_float=Fraction, parse_constant=_reject_constant,
                             object_pairs_hook=_unique_object)
    return parse_instance(document, archive=archive, max_goods=max_goods)


def _core_data(instance: Instance, own: list[int], target: int, goods: tuple[int, ...]) -> dict[str, Any] | None:
    values = [sum(instance.values_scaled[i][g] for g in goods) for i in AGENTS]
    champions = [i for i in AGENTS if values[i] > own[i]]
    deletions = [{"deleted_good": g,
                  "slacks_scaled": [own[i] - (values[i] - instance.values_scaled[i][g]) for i in AGENTS]}
                 for g in goods]
    if not champions or any(slack < 0 for item in deletions for slack in item["slacks_scaled"]):
        return None
    return {"target": target, "goods": list(goods), "champions": champions,
            "values_scaled": values, "contains_charity": any(instance.base_owner[g] is None for g in goods),
            "single_deletion_slacks_scaled": deletions}


def extract_cores(instance: Instance) -> tuple[list[dict[str, Any]], list[int]]:
    base = _validated_base(instance)
    p = base["charity"][0]
    cores, checked = [], []
    for target in AGENTS:
        augmented = sorted(base["bundles"][target] + [p])
        visits = 0
        for size in range(1, len(augmented) + 1):
            for goods in combinations(augmented, size):
                visits += 1
                core = _core_data(instance, base["utilities_scaled"], target, goods)
                if core is not None:
                    core["core_id"] = len(cores)
                    cores.append(core)
        if visits != (1 << len(augmented)) - 1:
            raise RuntimeError("incomplete core-subset enumeration")
        checked.append(visits)
    return cores, checked


def construct_cycle_exchange(instance: Instance, selected_edges: Any) -> dict[str, Any]:
    """Validate a decorated simple cycle afresh, rejecting overlapping physical cores.

    Edges have source, target, and goods. core_id is only an output label; neither
    that label nor any supplied champion/deletion claims is trusted here.
    """
    base = _validated_base(instance)
    if not isinstance(selected_edges, (list, tuple)) or not 1 <= len(selected_edges) <= 4:
        raise ValueError("a simple cycle must contain one to four edges")
    edges = []
    for edge in selected_edges:
        if not isinstance(edge, dict):
            raise ValueError("cycle edge must be an object")
        source, target, goods = edge.get("source"), edge.get("target"), edge.get("goods")
        if any(type(i) is not int or i not in AGENTS for i in (source, target)):
            raise ValueError("cycle endpoints must be agents 0..3")
        if (not isinstance(goods, (list, tuple)) or not goods
                or any(type(g) is not int or not 0 <= g < instance.m for g in goods)
                or len(set(goods)) != len(goods)):
            raise ValueError("core goods must be a nonempty set of physical good indices")
        if any(instance.base_owner[g] not in (target, None) for g in goods):
            raise ValueError("core is not contained in its target bundle plus charity")
        core = _core_data(instance, base["utilities_scaled"], target, tuple(sorted(goods)))
        if core is None or source not in core["champions"]:
            raise ValueError("edge does not select a minimal envied core championed by its source")
        edges.append({"source": source, "target": target, "goods": core["goods"]})
    sources = [edge["source"] for edge in edges]
    if (len(set(sources)) != len(edges)
            or any(edge["target"] != edges[(k + 1) % len(edges)]["source"] for k, edge in enumerate(edges))):
        raise ValueError("edges must be ordered around one directed simple cycle")
    flattened = [g for edge in edges for g in edge["goods"]]
    if len(set(flattened)) != len(flattened):
        raise ValueError("selected cores overlap; this is not a physical exchange")
    owners = [owner if owner not in sources else None for owner in instance.base_owner]
    for edge in edges:
        for good in edge["goods"]:
            if owners[good] is not None:
                raise ValueError("cycle would take a nonparticipant's physical good")
            owners[good] = edge["source"]
    result = allocation_record(instance, owners)
    gains = [after - before for after, before in zip(result["utilities_scaled"], base["utilities_scaled"])]
    strict_participants = all(gains[i] > 0 for i in sources)
    unchanged_others = all(gains[i] == 0 for i in AGENTS if i not in sources)
    pareto = all(gain >= 0 for gain in gains) and any(gain > 0 for gain in gains)
    lex_better = tuple(result["utilities_scaled"]) > tuple(base["utilities_scaled"])
    if not (result["is_efx"] and strict_participants and unchanged_others and pareto and lex_better):
        raise RuntimeError("physical cycle exchange failed its independent EFX/Pareto verification")
    result.update({"utility_gains_scaled": gains, "strict_for_every_participant": strict_participants,
                   "unchanged_nonparticipants": unchanged_others, "is_pareto_improvement": pareto,
                   "fixed_order_lexicographic_improvement": lex_better})
    return result


def _vertex_cycles() -> list[tuple[int, ...]]:
    return [cycle for size in range(1, 5) for cycle in permutations(AGENTS, size) if cycle[0] == min(cycle)]


def audit(instance: Instance, *, max_decorated_cycles: int = 100000) -> dict[str, Any]:
    if type(max_decorated_cycles) is not int or max_decorated_cycles < 1:
        raise ValueError("max_decorated_cycles must be a positive integer")
    base = _validated_base(instance)
    cores, checked = extract_cores(instance)
    edges = [{"source": source, "target": core["target"], "core_id": core["core_id"], "goods": core["goods"]}
             for core in cores for source in core["champions"]]
    adjacency = {(i, j): [edge for edge in edges if (edge["source"], edge["target"]) == (i, j)]
                 for i in AGENTS for j in AGENTS}
    vertex_cycles = _vertex_cycles()
    expected = sum(prod(len(adjacency[cycle[k], cycle[(k + 1) % len(cycle)]]) for k in range(len(cycle)))
                   for cycle in vertex_cycles)
    if expected > max_decorated_cycles:
        raise ValueError(f"{expected} decorated cycles exceed max_decorated_cycles={max_decorated_cycles}")
    cycles = []
    p = base["charity"][0]
    for vertices in vertex_cycles:
        choices = [adjacency[vertices[k], vertices[(k + 1) % len(vertices)]] for k in range(len(vertices))]
        for selection in product(*choices):
            p_count = sum(p in edge["goods"] for edge in selection)
            flattened = [g for edge in selection for g in edge["goods"]]
            disjoint = len(flattened) == len(set(flattened))
            if disjoint != (p_count <= 1):
                raise RuntimeError("simple-cycle physical intersection invariant failed")
            cycles.append({"vertices": list(vertices), "edges": list(selection),
                           "charity_occurrences": p_count, "cores_disjoint": disjoint,
                           "exchange": construct_cycle_exchange(instance, selection) if disjoint else None})
    if len(cycles) != expected:
        raise RuntimeError("incomplete decorated-cycle enumeration")
    return {"schema": OUTPUT_SCHEMA, "n": 4, "m": instance.m, "agent_order": list(AGENTS),
            "arithmetic": {"method": "Exact common-denominator integer comparisons; no binary floats.",
                           "common_denominator": instance.denominator,
                           "values_scaled": [list(row) for row in instance.values_scaled]},
            "base_allocation": base, "cores": cores, "champion_records": edges, "decorated_cycles": cycles,
            "summary": {"nonempty_core_subsets_checked_by_target": checked,
                        "core_count": len(cores),
                        "core_count_by_target": [sum(core["target"] == i for core in cores) for i in AGENTS],
                        "champion_record_count": len(edges), "simple_vertex_cycles_examined": len(vertex_cycles),
                        "decorated_cycle_count": len(cycles),
                        "decorated_self_loop_count": sum(len(cycle["vertices"]) == 1 for cycle in cycles),
                        "decorated_cycle_count_by_length": {str(size): sum(len(cycle["vertices"]) == size for cycle in cycles)
                                                             for size in range(1, 5)},
                        "disjoint_core_cycle_count": sum(cycle["cores_disjoint"] for cycle in cycles),
                        "minimum_charity_occurrences_on_cycle": min((cycle["charity_occurrences"] for cycle in cycles), default=None)},
            "scope": {"global_lexmax_verified": False,
                      "global_maximality_claims_from_archive_used": False,
                      "conditional_cycle_exclusion": "If O is fixed-order lexmax over ALL partial EFX allocations, every decorated simple champion cycle uses p at least twice.",
                      "exchange_charity_safety_required": False,
                      "complete_efx_nonexistence_claimed": False,
                      "downstream_two_cycle_or_role_layout_proved": False}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--archive", action="store_true", help="explicitly load the exact selector audit archive")
    parser.add_argument("--max-goods", type=int, default=20)
    parser.add_argument("--max-decorated-cycles", type=int, default=100000)
    args = parser.parse_args(argv)
    try:
        instance = load_instance(args.input, archive=args.archive, max_goods=args.max_goods)
        report = audit(instance, max_decorated_cycles=args.max_decorated_cycles)
    except (ValueError, OSError, RuntimeError) as error:
        print(f"champion-core audit rejected input: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
