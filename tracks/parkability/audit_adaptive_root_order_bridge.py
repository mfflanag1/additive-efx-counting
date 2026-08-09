#!/usr/bin/env python3
"""Direct audit of the adaptive-root/order bridge counterexample."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from decide_adaptive_root_promotion_bridge import ROOT_OWNERS, SURVIVING_ORDERS
from run_alternating_global_lex_cegar import (
    AGENTS,
    ALL_OWNERS,
    BASE_OWNER,
    N,
    bundles,
    numeric_efx,
    numeric_utilities,
    structural_solver,
)


SCHEMA = "alternating-adaptive-root-order-bridge-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def efx_failures(values, owner):
    assigned = bundles(owner)
    own = numeric_utilities(values, owner)
    return [
        {
            "observer": AGENTS[observer],
            "target": AGENTS[target],
            "removed_good": removed,
            "own": own[observer],
            "remainder": sum(
                values[observer][good]
                for good in assigned[target]
                if good != removed
            ),
        }
        for observer in range(N)
        for target in range(N)
        for removed in assigned[target]
        if own[observer]
        < sum(
            values[observer][good]
            for good in assigned[target]
            if good != removed
        )
    ]


def pin_structural(values):
    solver, symbolic, _ = structural_solver()
    solver.add(
        *(
            symbolic[agent][good] * sum(values[agent]) == values[agent][good]
            for agent in range(N)
            for good in range(len(BASE_OWNER))
        )
    )
    return str(solver.check())


def exact_order_census(values, order):
    base = numeric_utilities(values, BASE_OWNER)
    base_key = tuple(base[agent] for agent in order)
    improving = []
    for owner in ALL_OWNERS:
        if not numeric_efx(values, owner):
            continue
        utility = numeric_utilities(values, owner)
        if tuple(utility[agent] for agent in order) <= base_key:
            continue
        changed = sum(left != right for left, right in zip(owner, BASE_OWNER))
        improving.append((changed, owner, utility))
    minimum = min(record[0] for record in improving)
    witnesses = [record for record in improving if record[0] == minimum]
    return {
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "improving_efx_count": len(improving),
        "minimum_changed_goods": minimum,
        "minimum_witness_count": len(witnesses),
        "canonical_minimum_witness": {
            "owner": list(witnesses[0][1]),
            "utility": list(witnesses[0][2]),
            "delta": [right - left for left, right in zip(base, witnesses[0][2])],
        },
    }


def audit(source_path: Path):
    source = json.loads(source_path.read_text())
    values = tuple(tuple(row) for row in source["values"])
    if pin_structural(values) != "sat":
        raise AssertionError("countermodel does not satisfy the structural premises")
    base = numeric_utilities(values, BASE_OWNER)
    root_records = {}
    for name, owner in ROOT_OWNERS.items():
        utility = numeric_utilities(values, owner)
        root_records[name] = {
            "owner": list(owner),
            "efx": numeric_efx(values, owner),
            "utility": list(utility),
            "delta": [right - left for left, right in zip(base, utility)],
            "strict_efx_failures": efx_failures(values, owner),
        }
    required_failures = (
        "p_promoted",
        "s_promoted",
        "q_bottom_for_charity",
        "r_bottom_for_charity",
        "cross_bottom_swap",
    )
    if any(root_records[name]["efx"] for name in required_failures):
        raise AssertionError("an operation meant to be blocked is EFX")
    if not root_records["p_anchored"]["efx"] or not root_records["s_anchored"]["efx"]:
        raise AssertionError("root-flip fallback did not replay")
    order_records = [exact_order_census(values, order) for order in SURVIVING_ORDERS]
    if order_records[1]["minimum_changed_goods"] != 1:
        raise AssertionError("the claimed one-good missing operation is not minimal")
    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "EXACT_RESTRICTED_ADAPTIVE_ROOT_BRIDGE_REFUTATION",
        "claim_boundary": {
            "refuted": (
                "canonical promoted-root choice, even augmented by the two "
                "bottom-charity swaps and direct cross-bottom swap"
            ),
            "not_refuted": (
                "the broader anchored suffix escape or the cap-free two-safe-bundle "
                "packing lemma"
            ),
        },
        "values": [list(row) for row in values],
        "base_owner": list(BASE_OWNER),
        "base_utility": list(base),
        "structural_replay_status": "sat",
        "operation_records": root_records,
        "surviving_order_censuses": order_records,
        "smallest_missing_operation": {
            "description": (
                "transfer the one-good top subpacket tr from r to q, preserving p=x, "
                "s=y, the charity good, and all other ownership"
            ),
            "owner": order_records[1]["canonical_minimum_witness"]["owner"],
            "order": list(SURVIVING_ORDERS[1]),
            "changed_goods": 1,
        },
        "provenance": {
            "source": str(source_path),
            "source_sha256": sha256(source_path),
            "audit_script": str(script.relative_to(script.parents[2])),
            "audit_script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("results/alternating_adaptive_root_or_two_good_bridge.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
