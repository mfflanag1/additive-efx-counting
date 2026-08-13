#!/usr/bin/env python3
"""Symbolic audit and adversarial replay of the one-head split selector."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3


AGENTS = ("r", "q", "a", "b")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def subbundles(bundle):
    bundle = tuple(bundle)
    for size in range(1, len(bundle) + 1):
        yield from itertools.combinations(bundle, size)


def replay_frozen_countermodel(root: Path):
    source_path = root / "results/supplier_saturation_does_not_force_mixed_cycle_payment_audit.json"
    source = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(number) for good, number in row.items()}
        for agent, row in source["values"].items()
    }
    floors = {agent: Fraction(number) for agent, number in source["base_floors"].items()}
    cells = {
        "r": ("kr", "rr"),
        "q": ("d1", "d2", "rq"),
        "a": ("ka", "ra"),
        "b": ("kb", "rb"),
    }

    def value(agent, bundle):
        return sum((values[agent][good] for good in bundle), Fraction())

    def threshold(agent, bundle):
        bundle = tuple(bundle)
        if len(bundle) <= 1:
            return Fraction()
        return value(agent, bundle) - min(values[agent][good] for good in bundle)

    raw_lambdas = {
        agent: max(floors[agent], *(threshold(agent, cells[target]) for target in AGENTS))
        for agent in AGENTS
    }
    raw_blockers = {
        agent for agent in AGENTS
        if value(agent, cells[agent]) < raw_lambdas[agent]
    }

    # Remove the two old-incoming self-response rows without changing the
    # decorated-head row. This creates an exact positive one-head stress
    # profile from the generic supplier-saturation witness.
    values["r"]["kr"] = Fraction(13)
    values["b"]["kb"] = Fraction(13)
    lambdas = {
        agent: max(floors[agent], *(threshold(agent, cells[target]) for target in AGENTS))
        for agent in AGENTS
    }
    blockers = {
        agent for agent in AGENTS
        if value(agent, cells[agent]) < lambdas[agent]
    }
    head = "a"
    entry_premise = blockers == {head}

    records = []
    for target in AGENTS if entry_premise else ():
        if target == head or value(head, cells[target]) < lambdas[head]:
            continue
        for packet in subbundles(cells[target]):
            if value(head, packet) < lambdas[head]:
                continue
            if any(
                value(head, tuple(g for g in packet if g != removed)) >= lambdas[head]
                for removed in packet
            ):
                continue
            returned = tuple(g for g in cells[target] if g not in packet) + cells[head]
            paid = value(target, returned) >= lambdas[target]
            new_cells = dict(cells)
            new_cells[head] = packet
            new_cells[target] = returned
            efx = paid and all(
                value(observer, new_cells[observer])
                >= threshold(observer, new_cells[other])
                for observer in AGENTS for other in AGENTS
            )
            walls = [] if not paid else [
                observer for observer in AGENTS
                if value(observer, new_cells[observer]) < threshold(observer, returned)
            ]
            records.append({
                "target": target,
                "packet": list(packet),
                "returned": list(returned),
                "target_paid": paid,
                "efx": efx,
                "new_return_wall_observers": walls,
            })
    complete_residual_return = ("rq", "ka", "ra", "rr", "rb")
    complete_residual_source_value = value("q", complete_residual_return)
    direct_source_floor_after_anchor_retaining_split = max(
        threshold("q", ("d1", "d2")),
        threshold("q", ("kr",)),
        threshold("q", ("kb",)),
    )
    assert complete_residual_source_value < direct_source_floor_after_anchor_retaining_split
    return {
        "source": str(source_path.relative_to(root)),
        "source_sha256": sha256(source_path),
        "raw_generic_blockers": sorted(raw_blockers),
        "terminalizing_overrides": {"r.kr": "13", "b.kb": "13"},
        "protected_thresholds": {agent: str(number) for agent, number in lambdas.items()},
        "blockers": sorted(blockers),
        "one_head_entry_premise": entry_premise,
        "selector_record_count": len(records),
        "paid_split_count": sum(record["target_paid"] for record in records),
        "efx_split_count": sum(record["efx"] for record in records),
        "complete_residual_return_to_decorated_source": list(complete_residual_return),
        "complete_residual_source_value": str(complete_residual_source_value),
        "direct_source_floor_after_anchor_retaining_split": str(
            direct_source_floor_after_anchor_retaining_split
        ),
        "complete_residual_return_fails": True,
        "records": records,
    }


def run(root: Path):
    za, zh, packet, threshold_a, slack = z3.Reals(
        "za zh packet threshold_a slack"
    )
    packet_threshold, whole_threshold, protected, own = z3.Reals(
        "packet_threshold whole_threshold protected own"
    )
    symbolic = {
        "failed_return_forces_capture": prove(
            [za - packet + zh < threshold_a],
            packet > za + zh - threshold_a,
        ),
        "capture_equals_bundle_plus_slack": prove(
            [slack == za - threshold_a,
             packet > za + zh - threshold_a],
            packet > zh + slack,
        ),
        "subtarget_preserves_old_safety": prove(
            [packet_threshold <= whole_threshold,
             whole_threshold <= protected,
             protected <= own],
            packet_threshold <= own,
        ),
    }
    assert all(symbolic.values())
    frozen = replay_frozen_countermodel(root)
    script = Path(__file__).resolve()
    theorem = root / "results/ONE_HEAD_PROTECTED_SPLIT_OR_CAPTURE_LEMMA_20260813.md"
    return {
        "schema": "one-head-protected-split-or-capture-audit-v1",
        "status": "EXACT_TWO_BUNDLE_SPLIT_OR_CAPTURE",
        "symbolic_checks": symbolic,
        "frozen_countermodel_replay": frozen,
        "claim_boundary": (
            "cap-free two-bundle selector and exact capture; simultaneous "
            "multi-target capture and global GG recurrence remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "frozen_selector_records": result["frozen_countermodel_replay"]["selector_record_count"],
        "frozen_paid_splits": result["frozen_countermodel_replay"]["paid_split_count"],
        "frozen_efx_splits": result["frozen_countermodel_replay"]["efx_split_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
