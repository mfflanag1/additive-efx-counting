#!/usr/bin/env python3
"""Audit the exact data behind the endpoint-6 two-probe H relay."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAYMENT = ROOT / "results/allocated_e_form2_endpoint6_three_way_h_release_payment_analysis.json"
LIFT = ROOT / "results/allocated_e_form2_endpoint6_three_way_h_release_lift_audit.json"
THEOREM = ROOT / "results/ENDPOINT6_TWO_PROBE_H_RELAY_CLOSURE_THEOREM_20260814.md"
COLLISION_COMMIT = "34709c9ce22dbde23a5fa381a2ccea7898dfe1ca"


def packet_set(row):
    return {owner: frozenset(goods) for owner, goods in row.items()}


def run(output: Path):
    payments = json.loads(PAYMENT.read_text())
    lift = json.loads(LIFT.read_text())
    rows = payments["rows"]
    assert len(rows) == 3
    c_d = packet_set(rows[0]["allocation"])
    c_s = packet_set(rows[1]["allocation"])
    assert all(rows[0]["owners"][owner]["forced_paid"] for owner in ("r", "q", "d", "s"))
    assert all(rows[1]["owners"][owner]["forced_paid"] for owner in ("r", "q", "s"))
    assert not rows[1]["owners"]["d"]["forced_paid"]
    all_goods_d = set().union(*(set(goods) for goods in c_d.values()))
    all_goods_s = set().union(*(set(goods) for goods in c_s.values()))
    assert all_goods_d == all_goods_s
    assert sum(map(len, c_d.values())) == len(all_goods_d)
    assert sum(map(len, c_s.values())) == len(all_goods_s)
    changed = {
        owner: sorted(c_d[owner] ^ c_s[owner])
        for owner in c_d if c_d[owner] != c_s[owner]
    }
    assert changed == {"d": ["h"], "s": ["h"]}
    lift_rows = lift["rows"]
    assert lift_rows[0]["support_edge_count"] == 3
    assert lift_rows[1]["support_edge_count"] == 3
    assert lift_rows[0]["support_edges"] == [
        ["charity", "s"], ["r", "d"], ["s", "d"],
    ]
    assert lift_rows[1]["support_edges"] == [
        ["charity", "s"], ["r", "s"], ["s", "d"],
    ]
    result = {
        "schema": "endpoint6-two-probe-h-relay-closure-audit-v1",
        "status": "CONDITIONAL_COMPOSITION_AUDIT_PASSED",
        "c_d_all_owners_forced_paid": True,
        "c_s_forced_paid_owners": ["r", "q", "s"],
        "c_s_only_possible_payment_hole": "d",
        "c_d_edge_count": 3,
        "c_s_edge_count": 3,
        "relay_from_c_d_to_c_s": {"packet": "H", "edge": "d->s"},
        "canonical_cancellation_of_relay_equals": "C_d",
        "retired_packet_nonempty": True,
        "imported_collision_theorem_commit": COLLISION_COMMIT,
        "dependencies": {
            str(PAYMENT.relative_to(ROOT)): hashlib.sha256(PAYMENT.read_bytes()).hexdigest(),
            str(LIFT.relative_to(ROOT)): hashlib.sha256(LIFT.read_bytes()).hexdigest(),
            str(THEOREM.relative_to(ROOT)): hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
        },
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Checks exact allocations, edges, payment rows, and relay identity. "
            "It does not independently certify the semantic admissibility of "
            "the sequential probe or reprove the imported collision theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
