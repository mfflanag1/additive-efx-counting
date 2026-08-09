#!/usr/bin/env python3
"""Audit Pareto handoffs on the frozen eleven-good alternating corpus."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from analyze_alternating_singleton_return_models import (
    AGENTS,
    SIZES,
    bundles,
    make_cell,
    numeric_efx,
    numeric_utilities,
    singleton_return_candidates,
)


SCHEMA = "alternating-adaptive-order-frozen-handoff-audit-v1"
AUDIT_NAMES = (
    "alternating_bottom_partition_dichotomy_2222_audit.json",
    "alternating_any_root_subset_dichotomy_2222_audit.json",
    "alternating_any_cross_subset_dichotomy_2222_audit.json",
    "alternating_base_q_remainder_gate_2222.json",
    "alternating_base_q_remainder_recipient_relaxed_gate_2222.json",
    "alternating_base_q_remainder_exact_efx_gate_2222.json",
)


def parse_number(value):
    return Fraction(value) if isinstance(value, str) else Fraction(value)


def load_profiles(results: Path):
    session = json.loads((results / "alternating_singleton_return_0213_session1.json").read_text())
    profiles = [
        (
            f"cegar_iteration_{record['iteration']}",
            tuple(tuple(parse_number(entry) for entry in row) for row in record["values"]),
        )
        for record in session["trace"]
    ]
    for name in AUDIT_NAMES:
        payload = json.loads((results / name).read_text())
        profiles.append(
            (
                Path(name).stem,
                tuple(tuple(parse_number(entry) for entry in row) for row in payload["values"]),
            )
        )
    qface = json.loads((results / "alternating_safe_pair_qface_remainder_2222.json").read_text())
    profiles.append(
        (
            "qface_complement_refutation",
            tuple(tuple(parse_number(entry) for entry in row) for row in qface["model"]),
        )
    )
    return profiles


def audit_profile(label, values, cell, candidates):
    base_utility = numeric_utilities(values, cell["base_owner"])
    weak_pareto = []
    mode_counts = {"p_root": 0, "s_root": 0}
    efx_count = 0
    for owner in candidates:
        if not numeric_efx(values, owner):
            continue
        efx_count += 1
        utility = numeric_utilities(values, owner)
        delta = tuple(right - left for left, right in zip(base_utility, utility))
        if not any(entry > 0 for entry in delta) or any(entry < 0 for entry in delta):
            continue
        assigned = bundles(owner)
        allocation_mode = "p_root" if assigned[2] == (cell["y"],) else "s_root"
        mode_counts[allocation_mode] += 1
        weak_pareto.append(
            (
                sum(left != right for left, right in zip(owner, cell["base_owner"])),
                owner,
                utility,
                delta,
            )
        )
    weak_pareto.sort(key=lambda record: (record[0], str(record[1])))
    canonical = None
    if weak_pareto:
        changed, owner, utility, delta = weak_pareto[0]
        canonical = {
            "owner": list(owner),
            "bundles": {
                AGENTS[agent]: [cell["goods"][good] for good in bundle]
                for agent, bundle in enumerate(bundles(owner))
            },
            "utility": [str(entry) for entry in utility],
            "delta": [str(entry) for entry in delta],
            "changed_goods": changed,
        }
    return {
        "label": label,
        "base_utility": [str(entry) for entry in base_utility],
        "efx_singleton_return_count": efx_count,
        "weak_pareto_singleton_return_count": len(weak_pareto),
        "weak_pareto_root_counts": mode_counts,
        "canonical_weak_pareto_handoff": canonical,
    }


def main() -> None:
    repo = Path(__file__).resolve().parents[2]
    results = repo / "results"
    cell = make_cell(SIZES)
    candidates = tuple(singleton_return_candidates(cell))
    records = [
        audit_profile(label, values, cell, candidates)
        for label, values in load_profiles(results)
    ]
    payload = {
        "schema": SCHEMA,
        "status": "EXACT_FROZEN_CORPUS_AUDIT",
        "claim_boundary": (
            "Exhaustive over the 39,366 singleton-return allocations for each "
            "frozen profile, not over arbitrary allocations or valuations."
        ),
        "packet_sizes": list(SIZES),
        "candidate_count": len(candidates),
        "profile_count": len(records),
        "profiles_with_weak_pareto_handoff": sum(
            record["weak_pareto_singleton_return_count"] > 0 for record in records
        ),
        "profiles": records,
    }
    output = results / "alternating_adaptive_order_frozen_handoff_audit.json"
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "status",
                    "profile_count",
                    "candidate_count",
                    "profiles_with_weak_pareto_handoff",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
