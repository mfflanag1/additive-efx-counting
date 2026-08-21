#!/usr/bin/env python3
"""Independent exact audit of the universal unsplit-a1 allocation.

This audit deliberately does not import the CEGAR driver or rebuild its SMT
formula.  It uses the elementary additive EFX identity

    v_i(X_i) - v_i(X_j) + min_{g in X_j} v_i(g) >= 0.

The three-good search supplies an allocation template in which every a1 good
occurs in one bundle.  Substituting *any* realization of a1 into that same
bundle leaves its value and least-good value equal to the frozen aggregate
T_i and minimum M_i.  Thus the exact arithmetic audit is cardinality-free.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
TARGET_ROLE = "a1"
TARGET_GOODS = tuple(f"a1:{index}" for index in range(3))
SUPPLIER = {
    role: source
    for source, roles in {
        "r": ("a0", "a1", "h"),
        "q": ("j", "k", "q0"),
        "d": ("m", "gq", "gr"),
        "s": ("l", "e"),
        "charity": ("p",),
    }.items()
    for role in roles
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def load_first_record(path):
    lines = [line for line in path.read_text().splitlines() if line.strip()]
    assert len(lines) == 1
    record = json.loads(lines[0])
    digest = record.pop("payload_sha256")
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":"))
    assert hashlib.sha256(encoded.encode()).hexdigest() == digest
    record["payload_sha256"] = digest
    return record


def audit(profile_path, repair_path, ledger_path, output_path, edge_cap=4):
    profile = json.loads(profile_path.read_text())
    repair = json.loads(repair_path.read_text())
    record = load_first_record(ledger_path)
    allocation = record["allocation"]
    assert set(allocation) == set(OWNERS)

    totals = {
        observer: Fraction(profile["profile_totals"][observer][TARGET_ROLE])
        for observer in OWNERS
    }
    minima = {
        observer: Fraction(profile["profile_minima"][observer][TARGET_ROLE])
        for observer in OWNERS
    }
    assert all(totals[observer] > 3 * minima[observer] for observer in OWNERS)
    maximum_cardinality = min(
        totals[observer] // minima[observer] for observer in OWNERS
    )
    assert maximum_cardinality == 7
    feasible_cardinalities = list(range(2, maximum_cardinality + 1))
    for cardinality in feasible_cardinalities:
        # k-1 minimum goods plus the residual explicitly witnesses feasibility.
        assert all(
            totals[observer] - (cardinality - 1) * minima[observer]
            >= minima[observer]
            for observer in OWNERS
        )
    assert any(
        (maximum_cardinality + 1) * minima[observer] > totals[observer]
        for observer in OWNERS
    )

    frozen = {
        observer: {good: Fraction(amount) for good, amount in row.items()
                   if not good.startswith(TARGET_ROLE + ":")}
        for observer, row in repair["terminal"]["physical_values"].items()
    }
    allocated = [good for bundle in allocation.values() for good in bundle]
    assert len(allocated) == len(set(allocated))
    assert set(TARGET_GOODS).issubset(allocated)
    expected_frozen = set(frozen[OWNERS[0]])
    assert set(allocated) == expected_frozen | set(TARGET_GOODS)

    target_owner = next(owner for owner in OWNERS
                        if set(TARGET_GOODS).issubset(allocation[owner]))
    assert all(
        (good in allocation[target_owner])
        for good in TARGET_GOODS
    )
    assert all(
        not (set(TARGET_GOODS) & set(allocation[owner]))
        for owner in OWNERS if owner != target_owner
    )

    edges = sorted({
        (SUPPLIER[good.split(":", 1)[0]], owner)
        for owner, goods in allocation.items() for good in goods
        if SUPPLIER[good.split(":", 1)[0]] != owner
    })
    assert len(edges) <= edge_cap
    assert [list(edge) for edge in edges] == record["edges"]

    bundle_value = {}
    bundle_minimum = {}
    for observer in OWNERS:
        for owner in OWNERS:
            fixed_goods = [good for good in allocation[owner]
                           if good not in TARGET_GOODS]
            value = sum((frozen[observer][good] for good in fixed_goods), Fraction())
            candidates = [frozen[observer][good] for good in fixed_goods]
            if owner == target_owner:
                value += totals[observer]
                candidates.append(minima[observer])
            assert candidates
            bundle_value[observer, owner] = value
            bundle_minimum[observer, owner] = min(candidates)

    slacks = {}
    for observer in OWNERS:
        slacks[observer] = {}
        for target in OWNERS:
            if target == observer:
                continue
            slack = (
                bundle_value[observer, observer]
                - bundle_value[observer, target]
                + bundle_minimum[observer, target]
            )
            assert slack >= 0, (observer, target, slack)
            slacks[observer][target] = str(slack)

    minimum_slack = min(
        Fraction(amount) for row in slacks.values() for amount in row.values()
    )
    result = {
        "schema": "fixed-u-a1-three-good-independent-aggregate-audit-v1",
        "status": "VERIFIED_ALL_FEASIBLE_A1_CARDINALITIES_UNIVERSAL_EFX_ALLOCATION",
        "method": (
            "independent exact Fraction audit of own minus target plus the "
            "least target-good value; no CEGAR code or SMT formula imported"
        ),
        "profile": str(profile_path),
        "profile_sha256": sha256(profile_path),
        "repair": str(repair_path),
        "repair_sha256": sha256(repair_path),
        "ledger": str(ledger_path),
        "ledger_sha256": sha256(ledger_path),
        "target_owner": target_owner,
        "feasible_target_cardinalities": feasible_cardinalities,
        "maximum_feasible_target_cardinality": maximum_cardinality,
        "edge_cap": edge_cap,
        "edges": [list(edge) for edge in edges],
        "universal_reason": (
            "the allocation keeps the entire a1 realization together, so every "
            "bundle total uses only T_i and every hardest deletion uses only M_i; "
            "substitution is valid at every feasible cardinality"
        ),
        "pairwise_worst_efx_slacks": slacks,
        "minimum_worst_efx_slack": str(minimum_slack),
        "labelled_witness_pattern_count": 6 ** len(OWNERS),
        "claim_boundary": (
            "Every positive finite realization of a1 with this immutable terminal "
            "profile's totals and minima has this complete EFX allocation using "
            "four support-transfer edges. Exactly cardinalities 2 through 7 are "
            "feasible across all observers; cardinality 8 and above is impossible "
            "because 8 M_d > T_d. Other roles remain in the canonical physical "
            "realization; this is not a theorem for every fixed-U state."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--repair", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    args = parser.parse_args()
    result = audit(
        args.profile, args.repair, args.ledger, args.output, args.edge_cap
    )
    print(json.dumps({
        "status": result["status"],
        "minimum_worst_efx_slack": result["minimum_worst_efx_slack"],
        "feasible_target_cardinalities": result["feasible_target_cardinalities"],
        "edges": result["edges"],
    }, indent=2))


if __name__ == "__main__":
    main()
