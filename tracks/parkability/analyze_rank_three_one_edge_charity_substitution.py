#!/usr/bin/env python3
"""Exact finite-profile audit of the one-edge charity-substitution selector."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .run_fixed_u_full_packet_terminal_cegar import OWNERS, SUPPORT_STATE


FORMS = (
    (("r", "q"), ("q", "r"), ("s", "d"), ("d", "q")),
    (("r", "q"), ("q", "d"), ("s", "r"), ("d", "q")),
    (("r", "q"), ("q", "s"), ("s", "r"), ("d", "q")),
    (("r", "q"), ("q", "s"), ("s", "d"), ("d", "q")),
)


def total(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return total(values, observer, goods) - min(values[observer][good] for good in goods)


def response_cores(values, source, target):
    target_goods = tuple(SUPPORT_STATE[target])
    current = {
        owner: total(values, owner, SUPPORT_STATE[owner]) for owner in OWNERS
    }
    cores = []
    for size in range(1, len(target_goods) + 1):
        for goods in itertools.combinations(target_goods, size):
            base_safe = (
                total(values, source, goods) > 1
                and all(tail(values, observer, goods) <= 1 for observer in OWNERS)
            )
            current_safe = (
                total(values, source, goods) > current[source]
                and all(
                    tail(values, observer, goods) <= current[observer]
                    for observer in OWNERS
                )
            )
            if base_safe or current_safe:
                cores.append(goods)
    return tuple(cores)


def allocations_for(form, omitted, selected):
    active = tuple(edge for edge in form if edge[0] != omitted)
    required = {edge: set(goods) for edge, goods in zip(active, selected, strict=True)}
    choices = []
    goods_order = []
    for supplier in OWNERS:
        outgoing = tuple(edge for edge in active if edge[1] == supplier)
        required_goods = set().union(*(required[edge] for edge in outgoing)) if outgoing else set()
        for good in SUPPORT_STATE[supplier]:
            goods_order.append((supplier, good))
            forced = [edge[0] for edge in outgoing if good in required[edge]]
            if forced:
                assert len(forced) == 1
                choices.append(tuple(forced))
            else:
                # Any residual good may stay or join one existing supplier edge.
                choices.append((supplier, *(edge[0] for edge in outgoing)))
    seen = set()
    for recipients in itertools.product(*choices):
        allocation = {owner: [] for owner in OWNERS}
        allocation["charity"] = []
        allocation[omitted].extend(SUPPORT_STATE["charity"])
        for (_, good), recipient in zip(goods_order, recipients, strict=True):
            allocation[recipient].append(good)
        for goods in allocation.values():
            goods.sort()
        key = tuple(tuple(allocation[owner]) for owner in (*OWNERS, "charity"))
        if key in seen:
            continue
        seen.add(key)
        yield allocation


def profile_analysis(record):
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in record["values"].items()
    }
    active_forms = []
    witnesses = []
    candidate_count = 0
    for form_index, form in enumerate(FORMS):
        menus = {edge: response_cores(values, *edge) for edge in form}
        if not all(menus.values()):
            continue
        active_forms.append(form_index)
        for omitted in OWNERS:
            active = tuple(edge for edge in form if edge[0] != omitted)
            for selected in itertools.product(*(menus[edge] for edge in active)):
                by_target = {}
                disjoint = True
                for edge, goods in zip(active, selected, strict=True):
                    used = by_target.setdefault(edge[1], set())
                    if used & set(goods):
                        disjoint = False
                        break
                    used.update(goods)
                if not disjoint:
                    continue
                for allocation in allocations_for(form, omitted, selected):
                    candidate_count += 1
                    if complete_efx(values, allocation):
                        witnesses.append({
                            "form_index": form_index,
                            "omitted_source": omitted,
                            "selected_cores": [
                                {"edge": list(edge), "goods": list(goods)}
                                for edge, goods in zip(active, selected, strict=True)
                            ],
                            "allocation": allocation,
                        })
    return {
        "iteration": record["iteration"],
        "active_form_indices": active_forms,
        "selector_candidate_count": candidate_count,
        "efx_witness_count": len(witnesses),
        "witnesses": witnesses,
    }


def run(source: Path, maximum_iteration=None):
    payload = json.loads(source.read_text())
    records = [
        profile_analysis(record) for record in payload.get("rounds", [])
        if record.get("values")
        and (maximum_iteration is None or record["iteration"] <= maximum_iteration)
    ]
    script = Path(__file__).resolve()
    return {
        "schema": "rank-three-one-edge-charity-substitution-profile-analysis-v1",
        "source": f"results/{source.name}",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "profile_count": len(records),
        "all_profiles_have_selector_witness": bool(records) and all(
            record["efx_witness_count"] for record in records
        ),
        "profiles": records,
        "claim_boundary": (
            "exact arbitrary-residual selector census for recorded twelve-atom "
            "profiles; a failure refutes only the one-edge response-topology "
            "substitution selector under "
            "the encoded necessary premises, while universal success remains "
            "bounded evidence rather than a cap-free theorem"
        ),
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iteration", type=int)
    args = parser.parse_args()
    result = run(args.source, args.maximum_iteration)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "profile_count": result["profile_count"],
        "all_profiles_have_selector_witness": result[
            "all_profiles_have_selector_witness"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
