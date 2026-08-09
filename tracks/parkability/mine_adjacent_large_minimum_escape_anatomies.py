#!/usr/bin/env python3
"""Mine minimum-change escapes for the two hard adjacent-large prefixes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from .audit_adjacent_large_dual_payment_counterexample import minimum_change_escape
    from .run_alternating_variable_packet_rooted_cegar import AGENTS, make_cell
except ImportError:
    from audit_adjacent_large_dual_payment_counterexample import minimum_change_escape
    from run_alternating_variable_packet_rooted_cegar import AGENTS, make_cell


SCHEMA = "adjacent-large-minimum-escape-anatomies-v1"
ORDERS = ((0, 1, 2, 3), (1, 0, 2, 3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def role(label: str) -> str:
    for prefix in ("tr", "br", "tq", "bq"):
        if label.startswith(prefix):
            return prefix
    return label


def owner_from_example(cell, example):
    owner = [None] * cell["m"]
    index = {label: good for good, label in enumerate(cell["goods"])}
    for agent, name in enumerate(AGENTS):
        for label in example["allocation"][name]:
            owner[index[label]] = agent
    return tuple(owner)


def transfer_signature(cell, example):
    owner = owner_from_example(cell, example)
    transfers = []
    for good, (old, new) in enumerate(zip(cell["base_owner"], owner)):
        if old == new:
            continue
        old_name = "charity" if old is None else AGENTS[old]
        new_name = "charity" if new is None else AGENTS[new]
        transfers.append(f"{role(cell['goods'][good])}:{old_name}->{new_name}")
    return tuple(sorted(transfers))


def load_profiles(result_path, selected_path, dual_path):
    result = json.loads(result_path.read_text())
    profiles = [
        (f"pool_iteration_{record['iteration']}", tuple(tuple(row) for row in record["values"]))
        for record in result["iterations"]
    ]
    selected = json.loads(selected_path.read_text())
    profiles.append(("selected_root_refutation", tuple(tuple(row) for row in selected["values"])))
    dual = json.loads(dual_path.read_text())
    profiles.append(("dual_payment_refutation", tuple(tuple(row) for row in dual["values"])))
    return tuple(result["packet_sizes"]), profiles


def run(result_path, selected_path, dual_path):
    sizes, profiles = load_profiles(result_path, selected_path, dual_path)
    cell = make_cell(sizes)
    records = []
    signature_counts = Counter()
    for label, values in profiles:
        for order in ORDERS:
            example = minimum_change_escape(cell, order, values)
            if example is None:
                status = "unsat"
                signature = ()
            else:
                status = "sat"
                signature = transfer_signature(cell, example)
                signature_counts[(order, signature)] += 1
            records.append(
                {
                    "profile": label,
                    "agent_order": list(order),
                    "agent_order_names": [AGENTS[agent] for agent in order],
                    "status": status,
                    "transfer_signature": list(signature),
                    "minimum_change_escape": example,
                }
            )
    return {
        "schema": SCHEMA,
        "status": "DIAGNOSTIC_ONLY",
        "packet_sizes": list(sizes),
        "profile_count": len(profiles),
        "records": records,
        "signature_counts": [
            {
                "agent_order": list(order),
                "agent_order_names": [AGENTS[agent] for agent in order],
                "transfer_signature": list(signature),
                "count": count,
            }
            for (order, signature), count in sorted(
                signature_counts.items(), key=lambda item: (-item[1], item[0])
            )
        ],
        "claim_boundary": "Finite exact anatomy mining only; no cap-free conclusion.",
        "provenance": {
            "unrestricted_result": str(result_path),
            "unrestricted_result_sha256": sha256(result_path),
            "selected_root_audit": str(selected_path),
            "selected_root_audit_sha256": sha256(selected_path),
            "dual_payment_audit": str(dual_path),
            "dual_payment_audit_sha256": sha256(dual_path),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--selected-audit", type=Path, required=True)
    parser.add_argument("--dual-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = run(args.result, args.selected_audit, args.dual_audit)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload["signature_counts"][:20], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
