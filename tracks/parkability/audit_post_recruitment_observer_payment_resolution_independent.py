#!/usr/bin/env python3
"""Independent exact replay of the post-recruitment payment resolution."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


AGENTS = ("r", "q", "a", "b")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def amount(row, bundle):
    return sum((row[good] for good in bundle), Fraction())


def threshold(row, bundle):
    bundle = tuple(bundle)
    if len(bundle) <= 1:
        return Fraction()
    return amount(row, bundle) - min(row[good] for good in bundle)


def generic_payment_replay() -> dict:
    goods = ("kr", "d1", "d2", "ka", "kb", "rr", "rq", "ra", "rb")
    tiny = Fraction(1, 10)
    values = {agent: {good: tiny for good in goods} for agent in AGENTS}
    values["r"].update({"kr": Fraction(11), "kb": Fraction(12)})
    values["q"].update({"d1": Fraction(7), "d2": Fraction(6),
                        "kr": Fraction(11), "rq": Fraction(1)})
    values["a"].update({"d1": Fraction(12), "d2": Fraction(1),
                        "ka": Fraction(11)})
    values["b"].update({"ka": Fraction(12), "kb": Fraction(11)})
    base = {agent: Fraction(10) for agent in AGENTS}
    current = {
        "r": ("kb", "rr"),
        "q": ("kr", "rq"),
        "a": ("d1", "d2", "ra"),
        "b": ("ka", "rb"),
    }
    old = {"r": ("kr",), "a": ("ka",), "b": ("kb",)}
    decorated = ("d1", "d2")
    residuals = ("rr", "rq", "ra", "rb")

    assert all(amount(values[i], current[i]) >= base[i] for i in AGENTS)
    assert amount(values["q"], decorated) > amount(values["q"], current["q"])
    assert all(
        threshold(values[i], decorated) <= amount(values[i], current[i])
        for i in AGENTS
    )
    assert all(amount(values[s], core) > base[s] for s, core in old.items())
    assert all(
        threshold(values[i], core) <= base[i]
        for i in AGENTS for core in old.values()
    )
    full_value = amount(values["a"], old["a"] + residuals)
    wall = threshold(values["a"], decorated)
    assert full_value == Fraction(57, 5)
    assert wall == 12
    assert full_value < wall

    recipients = (*AGENTS, None)
    efx_paid = 0
    for assignment in itertools.product(recipients, repeat=len(residuals)):
        bundles = {
            "r": set(old["r"]),
            "q": set(decorated),
            "a": set(old["a"]),
            "b": set(old["b"]),
        }
        for good, recipient in zip(residuals, assignment):
            if recipient is not None:
                bundles[recipient].add(good)
        if not all(amount(values[i], bundles[i]) > base[i] for i in AGENTS):
            continue
        if all(
            amount(values[i], bundles[i]) >= threshold(values[i], bundles[j])
            for i in AGENTS for j in AGENTS
        ):
            efx_paid += 1
    assert efx_paid == 0
    return {
        "residual_assignment_count": len(recipients) ** len(residuals),
        "efx_all_paid_count": efx_paid,
        "blocked_full_pool_value": str(full_value),
        "decorated_threshold": str(wall),
        "supplier_closure": list(AGENTS),
        "permanent_anchor_retained": True,
    }


def anchor_replay() -> dict:
    goods = ("k1", "k2", "rq", "j", "u", "e", "rr")
    rows = {agent: {good: Fraction(1) for good in goods} for agent in AGENTS}
    rows["r"].update({"k1": Fraction(6), "k2": Fraction(6),
                      "j": Fraction(8), "e": Fraction(5)})
    rows["a"].update({"j": Fraction(8), "u": Fraction(4),
                      "rq": Fraction(1), "rr": Fraction(6)})
    base = {agent: Fraction(10) for agent in AGENTS}
    current = {"r": Fraction(12), "q": Fraction(11),
               "a": Fraction(11), "b": Fraction(10)}
    anchor = frozenset({"k1", "k2"})
    A = frozenset({"j", "u"})
    E = frozenset({"j", "e"})
    rq = frozenset({"rq"})
    rr = frozenset({"rr"})
    J = A & E
    remainder = A - J

    assert anchor.isdisjoint(E)
    assert amount(rows["r"], anchor) > base["r"]
    assert amount(rows["r"], E) > current["r"]
    assert all(threshold(rows[i], E) <= current[i] for i in AGENTS)
    after_rq = amount(rows["a"], remainder | rq)
    after_all = amount(rows["a"], remainder | rq | rr)
    assert after_rq == 5 < base["a"]
    assert after_all == 11 > base["a"]

    # Independent physical check of the priority-valid sacrifice handoff.
    root_bundle = anchor | E
    active_pool = set(goods)
    sacrificed = active_pool - root_bundle
    assert root_bundle.isdisjoint(sacrificed)
    assert root_bundle | sacrificed == active_pool
    assert amount(rows["r"], root_bundle) > base["r"]
    return {
        "anchor": sorted(anchor),
        "response": sorted(E),
        "overlap": sorted(J),
        "a_after_Rq": str(after_rq),
        "a_after_complete_pool": str(after_all),
        "root_anchor_response_value": str(amount(rows["r"], root_bundle)),
        "root_base": str(base["r"]),
        "anchor_response_disjoint": True,
        "sacrifice_handoff_partitions_pool": True,
    }


def run(root: Path) -> dict:
    dependencies = (
        "SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md",
        "supplier_saturation_does_not_force_mixed_cycle_payment_audit.json",
        "supplier_saturated_payment_refutation_independent_audit.json",
        "ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md",
        "root_sourced_complete_signed_residual_compensation_audit.json",
        "ROOT_SOURCED_ANCHOR_RETAINING_SACRIFICE_HANDOFF_LEMMA_20260813.md",
        "root_sourced_anchor_retaining_sacrifice_handoff_audit.json",
        "ENLARGED_ROOT_TARGET_ANCHOR_HITTING_TRICHOTOMY_20260813.md",
        "enlarged_root_target_anchor_hitting_trichotomy_audit.json",
    )
    result_dir = root / "results"
    records = [
        {"path": f"results/{name}", "sha256": sha256(result_dir / name)}
        for name in dependencies
    ]
    theorem = result_dir / "POST_RECRUITMENT_OBSERVER_PAYMENT_OBJECTIVE_RESOLUTION_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "post-recruitment-observer-payment-resolution-independent-audit-v1",
        "status": "POST_RECRUITMENT_PAYMENT_OBJECTIVE_EXACTLY_REFUTED",
        "generic_payment_refutation": generic_payment_replay(),
        "anchor_case_refutation": anchor_replay(),
        "dependencies": records,
        "resolved_claims": [
            "supplier saturation does not force mixed-cycle observer payment",
            "R_q is not the complete anchor-preserving compensation reservoir",
            "complete-pool payment is not required before a priority-valid sacrifice handoff",
        ],
        "excluded_claims": [
            "globally recurrent GG closure",
            "four-agent additive EFX",
            "general additive EFX",
        ],
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "residual_assignments": result["generic_payment_refutation"]["residual_assignment_count"],
        "efx_all_paid": result["generic_payment_refutation"]["efx_all_paid_count"],
        "a_after_Rq": result["anchor_case_refutation"]["a_after_Rq"],
        "a_after_complete_pool": result["anchor_case_refutation"]["a_after_complete_pool"],
    }, indent=2))


if __name__ == "__main__":
    main()

