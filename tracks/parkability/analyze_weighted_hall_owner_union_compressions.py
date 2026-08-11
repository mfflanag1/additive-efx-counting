#!/usr/bin/env python3
"""Census owner-union compressions of weighted-Hall response boundaries."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

try:
    from .analyze_flexible_lex_radius3_hardness_gap import desired_subsets
    from .analyze_flexible_two_external_weighted_hall import (
        AGENTS,
        BOTTOM_Q,
        BOTTOM_R,
        TOP_Q,
        TOP_R,
        find_sdr,
        is_efx,
        minimal_payment_packets,
        sha256,
    )
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        lex_endpoint_succeeds,
        value,
    )
    from .analyze_flexible_later_owner_escape_topologies import old_bundles
except ImportError:
    from analyze_flexible_lex_radius3_hardness_gap import desired_subsets
    from analyze_flexible_two_external_weighted_hall import (
        AGENTS,
        BOTTOM_Q,
        BOTTOM_R,
        TOP_Q,
        TOP_R,
        find_sdr,
        is_efx,
        minimal_payment_packets,
        sha256,
    )
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        lex_endpoint_succeeds,
        value,
    )
    from analyze_flexible_later_owner_escape_topologies import old_bundles


def response_sources(values, base_value, offer):
    result = {}
    for source in AGENTS:
        subsets = desired_subsets(values, base_value, source, tuple(offer))
        if subsets:
            result[source] = subsets
    return result


def matchings(targets, response, sources):
    targets = tuple(targets)
    for selected in itertools.permutations(sources, len(targets)):
        if all(selected[index] in response[target] for index, target in enumerate(targets)):
            yield dict(zip(targets, selected))


def maximum_matchings(targets, response):
    targets = tuple(targets)
    for size in range(len(targets), 0, -1):
        found = []
        for matched_targets in itertools.combinations(targets, size):
            for selected_sources in itertools.permutations(AGENTS, size):
                if all(
                    selected_sources[index] in response[target]
                    for index, target in enumerate(matched_targets)
                ):
                    found.append(dict(zip(matched_targets, selected_sources)))
        if found:
            return found
    return []


def compression_candidates(values, base_value, allocation, targets, response):
    selected_matchings = maximum_matchings(targets, response)
    boundary_records = [
        (
            "FULL_MATCHING" if len(matching) == len(targets)
            else "MAXIMUM_DEFICIENT_MATCHING",
            tuple(targets),
            matching,
        )
        for matching in selected_matchings
    ]

    for kind, boundary_targets, target_to_source in boundary_records:
        source_to_target = {source: target for target, source in target_to_source.items()}
        sources = tuple(sorted(source_to_target, key=AGENTS.index))
        core_families = [
            desired_subsets(
                values,
                base_value,
                source,
                tuple(allocation[source_to_target[source]]),
            )
            for source in sources
        ]
        assert all(core_families)
        for selected_cores in itertools.product(*core_families):
            cores = {
                source: tuple(core)
                for source, core in zip(sources, selected_cores)
            }
            owner_union = tuple(sorted(
                set(boundary_targets).union(sources), key=AGENTS.index
            ))
            unmatched = tuple(owner for owner in owner_union if owner not in sources)
            assert unmatched
            union_goods = tuple(
                good for owner in owner_union for good in allocation[owner]
            )
            selected_goods = {good for core in cores.values() for good in core}
            assert sum(len(core) for core in cores.values()) == len(selected_goods)
            pool = tuple(good for good in union_goods if good not in selected_goods)
            for destinations in itertools.product(unmatched, repeat=len(pool)):
                candidate = {
                    owner: tuple(allocation[owner])
                    for owner in AGENTS
                    if owner not in owner_union
                }
                candidate.update(cores)
                for owner in unmatched:
                    candidate[owner] = tuple(
                        good for good, destination in zip(pool, destinations)
                        if destination == owner
                    )
                candidate["_"] = tuple(allocation["_"])
                paid = all(
                    value(values, owner, candidate[owner]) >= base_value[owner]
                    for owner in unmatched
                )
                internal_response = {
                    owner: sorted(
                        set(response_sources(
                            values, base_value, candidate[owner]
                        )).intersection(owner_union)
                    )
                    for owner in owner_union
                }
                internal_sdr = find_sdr(owner_union, internal_response)
                yield {
                    "kind": kind,
                    "boundary_targets": boundary_targets,
                    "sources": sources,
                    "owner_union": owner_union,
                    "unmatched": unmatched,
                    "matching": target_to_source,
                    "cores": cores,
                    "pool": pool,
                    "candidate": candidate,
                    "paid": paid,
                    "efx": is_efx(values, candidate),
                    "internal_sdr": internal_sdr,
                }


def recapture_closure(values, base_value, record, maximum_states=10000):
    if not record["paid"] or len(record["unmatched"]) != 1:
        return None
    missing = record["unmatched"][0]
    initial = record["candidate"]
    queue = [(initial, tuple(record["owner_union"]), 0)]
    visited = set()
    terminal = None
    while queue and len(visited) < maximum_states:
        allocation, owner_union, growth_steps = queue.pop()
        key = (owner_union,) + tuple(
            tuple(sorted(allocation[owner]))
            for owner in (*AGENTS, "_")
        )
        if key in visited:
            continue
        visited.add(key)
        if is_efx(values, allocation):
            return {
                "kind": "EFX",
                "allocation": allocation,
                "owner_union": owner_union,
                "states_examined": len(visited),
                "growth_steps": growth_steps,
            }
        response = {
            target: sorted(
                set(response_sources(
                    values, base_value, allocation[target]
                )).intersection(owner_union)
            )
            for target in owner_union
        }
        matching = find_sdr(owner_union, response)
        if matching is not None:
            return {
                "kind": "INTERNAL_SDR",
                "allocation": allocation,
                "matching": matching,
                "owner_union": owner_union,
                "states_examined": len(visited),
                "growth_steps": growth_steps,
            }
        full_residual_response = response_sources(
            values, base_value, allocation[missing]
        )
        walls = [
            [observer, target]
            for observer in AGENTS
            for target in AGENTS
            if value(values, observer, allocation[observer])
            < value(values, observer, allocation[target])
            - min(values[observer][good] for good in allocation[target])
        ]
        terminal = {
            "allocation": allocation,
            "owner_union": owner_union,
            "growth_steps": growth_steps,
            "residual_response_sources": sorted(full_residual_response),
            "walls": walls,
        }
        residual = tuple(allocation[missing])
        for source in AGENTS:
            if source == missing:
                continue
            old_core = tuple(allocation[source])
            for new_core in desired_subsets(
                values, base_value, source, residual
            ):
                new_core = tuple(new_core)
                new_core_set = set(new_core)
                new_residual = old_core + tuple(
                    good for good in residual if good not in new_core_set
                )
                if value(values, missing, new_residual) < base_value[missing]:
                    continue
                successor = {
                    owner: tuple(goods) for owner, goods in allocation.items()
                }
                successor[source] = new_core
                successor[missing] = new_residual
                if source in owner_union:
                    successor_union = owner_union
                    successor_growth = growth_steps
                else:
                    successor_union = tuple(sorted(
                        (*owner_union, source), key=AGENTS.index
                    ))
                    successor_growth = growth_steps + 1
                queue.append((
                    successor,
                    successor_union,
                    successor_growth,
                ))
    return {
        "kind": "NONE",
        "states_examined": len(visited),
        "exhausted": not queue,
        "terminal": terminal,
    }


def find_owner_union_closure(values, old):
    base_value = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    for payment in minimal_payment_packets(values):
        residual = tuple(good for good in TOP_R if good not in payment) + BOTTOM_R
        root_core = TOP_Q + ("f",)
        evolved_q = BOTTOM_Q + payment
        for destinations in itertools.product(("r", "c", "s"), repeat=len(residual)):
            cells = {recipient: [] for recipient in ("r", "c", "s")}
            for good, recipient in zip(residual, destinations):
                cells[recipient].append(good)
            allocation = {
                "r": tuple(root_core + tuple(cells["r"])),
                "q": tuple(evolved_q),
                "c": tuple(old["c"] + tuple(cells["c"])),
                "s": tuple(old["s"] + tuple(cells["s"])),
                "_": (),
            }
            targets = ("r", "q") + tuple(
                owner for owner in ("c", "s") if cells[owner]
            )
            response = {
                target: sorted(response_sources(
                    values, base_value, allocation[target]
                ))
                for target in targets
            }
            internal = {
                target: sorted(set(response[target]).intersection(targets))
                for target in targets
            }
            if is_efx(values, allocation) or find_sdr(targets, internal) is not None:
                continue
            for record in compression_candidates(
                values, base_value, allocation, targets, response
            ):
                if record["efx"]:
                    return {
                        "kind": "EFX",
                        "payment": payment,
                        "allocation": record["candidate"],
                        "targets": record["owner_union"],
                        "path": "MAXIMUM_MATCHING_COMPRESSION",
                    }
                if record["internal_sdr"] is not None:
                    return {
                        "kind": "INTERNAL_SDR",
                        "payment": payment,
                        "allocation": record["candidate"],
                        "targets": record["owner_union"],
                        "matching": record["internal_sdr"],
                        "path": "MAXIMUM_MATCHING_COMPRESSION",
                    }
                recapture = recapture_closure(values, base_value, record)
                if recapture is None or recapture["kind"] == "NONE":
                    continue
                return {
                    "kind": recapture["kind"],
                    "payment": payment,
                    "allocation": recapture["allocation"],
                    "targets": recapture["owner_union"],
                    "matching": recapture.get("matching"),
                    "path": "MAXIMUM_MATCHING_RECAPTURE",
                    "states_examined": recapture["states_examined"],
                    "growth_steps": recapture["growth_steps"],
                }
    return {"kind": "NONE"}


def run(source_path):
    payload = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in payload["values"].items()
    }
    old = old_bundles()
    base_value = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    counts = Counter()
    examples = {}
    payments = minimal_payment_packets(values)
    for payment in payments:
        residual = tuple(good for good in TOP_R if good not in payment) + BOTTOM_R
        root_core = TOP_Q + ("f",)
        evolved_q = BOTTOM_Q + payment
        for destinations in itertools.product(("r", "c", "s"), repeat=len(residual)):
            cells = {recipient: [] for recipient in ("r", "c", "s")}
            for good, recipient in zip(residual, destinations):
                cells[recipient].append(good)
            allocation = {
                "r": tuple(root_core + tuple(cells["r"])),
                "q": tuple(evolved_q),
                "c": tuple(old["c"] + tuple(cells["c"])),
                "s": tuple(old["s"] + tuple(cells["s"])),
                "_": (),
            }
            targets = ("r", "q") + tuple(
                owner for owner in ("c", "s") if cells[owner]
            )
            response = {
                target: sorted(response_sources(
                    values, base_value, allocation[target]
                ))
                for target in targets
            }
            internal = {
                target: sorted(set(response[target]).intersection(targets))
                for target in targets
            }
            if is_efx(values, allocation) or find_sdr(targets, internal) is not None:
                continue
            counts["BOUNDARIES"] += 1
            closure = None
            best = None
            for record in compression_candidates(
                values, base_value, allocation, targets, response
            ):
                counts["COMPRESSIONS_EXAMINED"] += 1
                if best is None or record["paid"]:
                    best = record
                if record["efx"]:
                    assert lex_endpoint_succeeds(values, old, record["candidate"])
                    closure = ("EFX", record)
                    break
                if record["internal_sdr"] is not None:
                    closure = ("INTERNAL_SDR", record)
                    break
                recapture = recapture_closure(values, base_value, record)
                if recapture is not None:
                    record["recapture"] = recapture
                counts["RECAPTURE_STATES_EXAMINED"] += recapture[
                    "states_examined"
                ] if recapture is not None else 0
                if recapture is not None and recapture["kind"] != "NONE":
                    if recapture["kind"] == "EFX":
                        assert lex_endpoint_succeeds(
                            values, old, recapture["allocation"]
                        )
                    closure = (f"RECAPTURE_{recapture['kind']}", record)
                    break
            classification = closure[0] if closure else "NO_COMPRESSION_CLOSURE"
            counts[classification] += 1
            chosen = closure[1] if closure else best
            if classification not in examples and chosen is not None:
                examples[classification] = {
                    key: (
                        {name: list(goods) for name, goods in value_.items()}
                        if key in ("cores", "candidate")
                        else list(value_) if isinstance(value_, tuple)
                        else value_
                    )
                    for key, value_ in chosen.items()
                    if key not in ("pool", "recapture")
                }
                if "recapture" in chosen:
                    examples[classification]["recapture"] = {
                        key: (
                            {name: list(goods) for name, goods in value_.items()}
                            if key == "allocation"
                            else value_
                        )
                        for key, value_ in chosen["recapture"].items()
                    }
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "weighted-hall-owner-union-compression-census-v1",
        "status": (
            "ALL_CLOSED" if counts["NO_COMPRESSION_CLOSURE"] == 0
            else "SURVIVORS"
        ),
        "minimal_payment_packets": [list(packet) for packet in payments],
        "counts": dict(sorted(counts.items())),
        "examples": examples,
        "claim_boundary": (
            "solver-free exact-Fraction census of every no-charity residual "
            "split and every owner-union compression in one bounded flower; "
            "closure is adversarial evidence, not a cap-free partition theorem"
        ),
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "counts": result["counts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
