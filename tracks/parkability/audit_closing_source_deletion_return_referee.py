#!/usr/bin/env python3
"""Independent referee audit of closing-source deletion return."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3


AGENTS = ("t", "u", "s", "w")
GOODS = ("d0", "d1", "a0", "a1", "a2", "a3", "x0", "x1", "x2", "x3")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(row: dict[str, Fraction], bundle: frozenset[str]) -> Fraction:
    return sum((row[good] for good in bundle), Fraction(0))


def threshold(row: dict[str, Fraction], bundle: frozenset[str]) -> Fraction:
    if len(bundle) <= 1:
        return Fraction(0)
    return value(row, bundle) - min(row[good] for good in bundle)


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def rational_witness() -> dict:
    tenth = Fraction(1, 10)
    rows = {
        "t": dict(zip(GOODS, map(Fraction, (2, 3, 2, 0, 0, 0, 1, 0, 0, 0)), strict=True)),
        "u": dict(zip(GOODS, map(Fraction, (1, 1, 1, 2, 0, 0, 1, 1, 0, 0)), strict=True)),
        "s": dict(zip(GOODS, map(Fraction, (4, 2, 0, 4, 2, 0, 1, 1, 1, 0)), strict=True)),
        "w": dict(zip(GOODS, map(Fraction, (1, 1, 0, 0, 1, 2, 0, 0, 1, 1)), strict=True)),
    }
    for row in rows.values():
        for good in GOODS:
            if row[good] == 0:
                row[good] = tenth
    rows["t"]["d0"] = Fraction(6, 5)
    rows["t"]["a0"] = Fraction(11, 10)

    base = {
        "t": frozenset({"x0"}),
        "u": frozenset({"x1"}),
        "s": frozenset({"x2"}),
        "w": frozenset({"x3"}),
    }
    current = {
        "t": frozenset({"d0", "d1"}),
        "u": frozenset({"a0", "x0"}),
        "s": frozenset({"a1", "x1"}),
        "w": frozenset({"a2", "x2"}),
    }
    old_core = {
        "t": frozenset({"a0"}),
        "u": frozenset({"a1"}),
        "s": frozenset({"a2"}),
        "w": frozenset({"a3"}),
    }
    incoming = {
        "u": old_core["t"],
        "s": old_core["u"],
        "w": old_core["s"],
    }
    residual = {
        owner: current[owner] - incoming[owner] for owner in ("u", "s", "w")
    }
    decorated = frozenset({"d0", "d1"})
    deleted_good = min(decorated, key=lambda good: rows["t"][good])
    returned = decorated - {deleted_good}
    candidate = {
        "t": returned,
        "u": old_core["u"] | residual["u"],
        "s": old_core["s"] | residual["s"],
        "w": old_core["w"] | residual["w"],
    }

    assert all(value(rows[i], old_core[i]) > value(rows[i], base[i]) for i in AGENTS)
    assert all(
        threshold(rows[i], decorated) <= value(rows[i], current[i]) for i in AGENTS
    )
    assert value(rows["s"], decorated) > value(rows["s"], current["s"])
    assert value(rows["t"], old_core["t"]) < threshold(rows["t"], decorated)
    assert all(value(rows[i], candidate[i]) > value(rows[i], base[i]) for i in AGENTS)
    assert all(
        left.isdisjoint(right)
        for index, left in enumerate(candidate.values())
        for right in list(candidate.values())[index + 1 :]
    )

    failed_observer = "s"
    failed_target = "u"
    assert value(rows[failed_observer], candidate[failed_observer]) < threshold(
        rows[failed_observer], candidate[failed_target]
    )
    repeated_core = frozenset({"a1"})
    assert repeated_core < candidate[failed_target]
    assert value(rows[failed_observer], repeated_core) > value(
        rows[failed_observer], candidate[failed_observer]
    )
    assert threshold(rows[failed_observer], repeated_core) == 0

    current_response_edges = []
    targets = dict(candidate)
    charity = frozenset(GOODS) - frozenset().union(*candidate.values())
    targets["charity"] = charity
    for source in AGENTS:
        source_value = value(rows[source], candidate[source])
        for target, bundle in targets.items():
            if source == target:
                continue
            for good in sorted(bundle):
                core = bundle - {good}
                if value(rows[source], core) > source_value:
                    current_response_edges.append((source, target, tuple(sorted(core))))
    current_response_edges.sort()
    distinct_sources = sorted({edge[0] for edge in current_response_edges})
    assert distinct_sources == ["s"]

    return {
        "valuations": {
            agent: {good: str(rows[agent][good]) for good in GOODS} for agent in AGENTS
        },
        "base": {agent: sorted(bundle) for agent, bundle in base.items()},
        "current": {agent: sorted(bundle) for agent, bundle in current.items()},
        "old_cores": {agent: sorted(bundle) for agent, bundle in old_core.items()},
        "decorated_core": sorted(decorated),
        "deleted_good": deleted_good,
        "candidate": {agent: sorted(bundle) for agent, bundle in candidate.items()},
        "candidate_utilities": {
            agent: str(value(rows[agent], candidate[agent])) for agent in AGENTS
        },
        "base_utilities": {agent: str(value(rows[agent], base[agent])) for agent in AGENTS},
        "failed_efx": {
            "observer": failed_observer,
            "target": failed_target,
            "observer_utility": str(value(rows[failed_observer], candidate[failed_observer])),
            "target_threshold": str(threshold(rows[failed_observer], candidate[failed_target])),
        },
        "repeated_response_core": sorted(repeated_core),
        "current_response_edges": [
            [source, target, list(core)] for source, target, core in current_response_edges
        ],
        "response_source_rank": len(distinct_sources),
        "interpretation": (
            "All local payment and disjointness premises hold, but the improving "
            "candidate is non-EFX. Its failed-target response may already be in "
            "history while the current response graph has only one source, so "
            "repetition alone implies neither a rank-four hole pivot nor PI."
        ),
    }


def trimmed_rational_witness() -> dict:
    goods = ("d0", "d1", "d2", "a0", "a1", "a2", "a3", "x0", "x1", "x2", "x3")
    tenth = Fraction(1, 10)
    rows = {
        "t": dict(zip(goods, map(Fraction, (1, 3, 2, 2, 0, 0, 0, 1, 0, 0, 0)), strict=True)),
        "u": dict(zip(goods, map(Fraction, (0, 3, 1, 3, 2, 0, 0, 1, 1, 0, 0)), strict=True)),
        "s": dict(zip(goods, map(Fraction, (0, 3, 2, 0, 4, 2, 0, 0, 1, 1, 0)), strict=True)),
        "w": dict(zip(goods, map(Fraction, (0, 3, 0, 0, 0, 0, 2, 0, 0, 1, 1)), strict=True)),
    }
    for row in rows.values():
        for good in goods:
            if row[good] == 0:
                row[good] = tenth
    rows["u"]["x0"] = Fraction(29, 10)
    rows["u"]["a0"] = Fraction(1, 5)
    rows["u"]["d2"] = tenth
    rows["w"]["d2"] = tenth
    rows["w"]["a2"] = Fraction(21, 10)
    rows["w"]["a3"] = Fraction(11, 5)
    rows["w"]["x3"] = tenth
    rows["t"]["a1"] = Fraction(5)

    base = {
        "t": frozenset({"x0"}), "u": frozenset({"x1"}),
        "s": frozenset({"x2"}), "w": frozenset({"x3"}),
    }
    old_core = {
        "t": frozenset({"a0"}), "u": frozenset({"a1"}),
        "s": frozenset({"a2"}), "w": frozenset({"a3"}),
    }
    current = {
        "t": frozenset({"d0", "d1", "d2"}),
        "u": frozenset({"a0", "x0"}),
        "s": frozenset({"a1", "x1"}),
        "w": frozenset({"a2", "x2"}),
    }
    decorated = current["t"]
    deleted_good = "d0"
    returned = decorated - {deleted_good}
    candidate = {
        "t": returned,
        "u": frozenset({"a1", "x0"}),
        "s": frozenset({"a2", "x1"}),
        "w": frozenset({"a3", "x2"}),
    }
    floor_u = max(value(rows["u"], base["u"]), threshold(rows["u"], returned))
    assert value(rows["u"], candidate["u"]) >= floor_u == 3
    assert all(
        value(rows["u"], candidate["u"] - {good}) < floor_u
        for good in candidate["u"]
    )
    direct_floor_t = max(
        value(rows["t"], base["t"]),
        *(threshold(rows["t"], candidate[owner]) for owner in ("u", "s", "w")),
    )
    assert value(rows["t"], returned) >= direct_floor_t == 5
    assert all(
        value(rows["t"], returned - {good}) < direct_floor_t for good in returned
    )
    assert value(rows["s"], candidate["s"] | {deleted_good}) < threshold(
        rows["s"], candidate["u"]
    )
    charity = frozenset(goods) - frozenset().union(*candidate.values())
    assert value(rows["s"], candidate["s"] | charity) < threshold(
        rows["s"], candidate["u"]
    )

    residual_pool = frozenset({"x0", "x1", "x2"}) | charity
    fixed_cores = {
        "u": frozenset({"a1"}),
        "s": frozenset({"a2"}),
        "w": frozenset({"a3"}),
    }
    floors = {
        owner: max(value(rows[owner], base[owner]), threshold(rows[owner], returned))
        for owner in ("u", "s", "w")
    }
    feasible_residual_partitions = 0
    efx_residual_partitions = 0
    first_efx_residual_partition = None
    ordered_pool = sorted(residual_pool)
    for code in range(4 ** len(ordered_pool)):
        allocation = {owner: set(fixed_cores[owner]) for owner in ("u", "s", "w")}
        cursor = code
        for good in ordered_pool:
            recipient = cursor % 4
            cursor //= 4
            if recipient < 3:
                allocation[("u", "s", "w")[recipient]].add(good)
        bundles = {"t": returned} | {
            owner: frozenset(bundle) for owner, bundle in allocation.items()
        }
        if any(
            value(rows[owner], bundles[owner]) < floors[owner]
            for owner in ("u", "s", "w")
        ):
            continue
        feasible_residual_partitions += 1
        if all(
            value(rows[observer], bundles[observer])
            >= threshold(rows[observer], bundles[target])
            for observer in AGENTS
            for target in AGENTS
            if observer != target
        ):
            efx_residual_partitions += 1
            if first_efx_residual_partition is None:
                first_efx_residual_partition = {
                    owner: sorted(bundle) for owner, bundle in bundles.items()
                }
    assert feasible_residual_partitions > 0
    assert efx_residual_partitions == 0

    edges = []
    targets = dict(candidate)
    targets["charity"] = charity
    for source in AGENTS:
        source_value = value(rows[source], candidate[source])
        for target, bundle in targets.items():
            if source == target:
                continue
            ordered = sorted(bundle)
            for mask in range(1, 1 << len(ordered)):
                core = frozenset(
                    ordered[index] for index in range(len(ordered)) if mask >> index & 1
                )
                if value(rows[source], core) <= source_value:
                    continue
                if all(
                    threshold(rows[observer], core) <= value(rows[observer], candidate[observer])
                    for observer in AGENTS
                ):
                    edges.append((source, target, tuple(sorted(core))))
    edges.sort()
    distinct_sources = sorted({source for source, _, _ in edges})
    assert distinct_sources == ["s"]
    assert ("s", "u", ("a1",)) in edges

    return {
        "goods": list(goods),
        "valuations": {
            agent: {good: str(rows[agent][good]) for good in goods} for agent in AGENTS
        },
        "candidate": {agent: sorted(bundle) for agent, bundle in candidate.items()},
        "charity": sorted(charity),
        "deleted_good": deleted_good,
        "owner_u_floor": str(floor_u),
        "owner_u_target_is_inclusion_minimal": True,
        "hole_packet_direct_floor": str(direct_floor_t),
        "hole_packet_is_inclusion_minimal": True,
        "deleted_good_topup_fails": True,
        "whole_charity_topup_fails": True,
        "residual_partition_family_size": 4 ** len(ordered_pool),
        "floor_feasible_residual_partitions": feasible_residual_partitions,
        "efx_floor_feasible_residual_partitions": efx_residual_partitions,
        "first_efx_residual_partition": first_efx_residual_partition,
        "current_response_edges": [
            [source, target, list(core)] for source, target, core in edges
        ],
        "response_source_rank": len(distinct_sources),
        "interpretation": (
            "The unsafe target is already inclusion-minimal for its owner's "
            "base/P floor. Parking its residual underpays that owner, while "
            "giving the deleted good or the whole charity to the blocker does "
            "not pay the EFX debt. Exhausting every floor-preserving partition "
            "of all residuals and charity yields no EFX member. The repeated "
            "safe-response graph still has only one source."
        ),
    }


def run(root: Path) -> dict:
    t_old, t_res, t_tau, t_base = z3.Reals("t_old t_res t_tau t_base")
    a_old, a_res, p_tau, d_tau, incoming, a_base = z3.Reals(
        "a_old a_res p_tau d_tau incoming a_base"
    )
    scalar_checks = {
        "target_owner_payment": prove(
            [t_old > t_base, t_res >= 0, t_old + t_res < t_tau],
            t_tau > t_base,
        ),
        "nonowner_payment_survives_deletion": prove(
            [a_old + a_res >= d_tau, p_tau <= d_tau],
            a_old + a_res >= p_tau,
        ),
        "strict_candidate_gain": prove(
            [a_old > a_base, a_res >= 0],
            a_old + a_res > a_base,
        ),
        "residual_failure_forces_self_response_value": prove(
            [
                a_old > a_base,
                a_res >= 0,
                a_old + a_res < p_tau,
                p_tau <= d_tau,
                d_tau <= incoming + a_res,
            ],
            incoming > a_old,
        ),
    }
    assert all(scalar_checks.values())

    witness = rational_witness()
    trimmed_witness = trimmed_rational_witness()
    script = Path(__file__).resolve()
    theorem = root / "results/CLOSING_SOURCE_DELETION_RETURN_RESIDUAL_COMPLETION_LEMMA_20260811.md"
    report = root / "results/CLOSING_SOURCE_DELETION_RETURN_REFEREE_REPORT_20260812.md"
    return {
        "schema": "closing-source-deletion-return-referee-audit-v1",
        "status": "TERMINATION_GAP_FOUND",
        "scalar_checks": scalar_checks,
        "physical_disjointness": "proved from target partition, not synthetic labels",
        "current_safe_not_base_safe": {
            "status": "SAT",
            "example": {
                "base_utility": "1",
                "current_utility": "5",
                "decorated_threshold": "4",
            },
        },
        "rational_local_countermodel": witness,
        "minimal_trimmed_countermodel": trimmed_witness,
        "smallest_gap": (
            "an unsafe deletion-return target yields one current-safe response, "
            "but neither a rank-four matching at that candidate state nor a "
            "strict finite state-order increase is proved; an already recorded "
            "rank-one response need not be PI or support progress"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "report": str(report.relative_to(root)),
            "report_sha256": sha256(report),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "smallest_gap": result["smallest_gap"]}, indent=2))


if __name__ == "__main__":
    main()
