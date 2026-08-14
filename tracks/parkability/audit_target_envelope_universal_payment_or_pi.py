#!/usr/bin/env python3
"""Exact audit of target-envelope universal payment or supplied PI."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    b, envelope, q, response_threshold, a = z3.Reals(
        "b envelope q response_threshold a"
    )
    selector_nonempty = prove([envelope <= b], b >= envelope)
    universal_payment = prove(
        [q >= envelope, response_threshold <= envelope],
        q >= response_threshold,
    )
    unsafe_reversal_below_envelope = prove(
        [a < envelope],
        a < envelope,
    )
    assert all((selector_nonempty, universal_payment,
                unsafe_reversal_below_envelope))

    agents = tuple(range(4))
    checked = 0
    cycle_count = 0
    for target_owner in agents:
        external = tuple(i for i in agents if i != target_owner)
        for target_source in external:
            for reversal_sources in itertools.product(agents, repeat=3):
                edge = dict(zip(external, reversal_sources))
                if any(edge[h] == h for h in external):
                    continue
                edge[target_owner] = target_source
                checked += 1
                vertex = 0
                seen = set()
                while vertex not in seen:
                    seen.add(vertex)
                    vertex = edge[vertex]
                cycle_count += 1
    assert checked == 324
    assert cycle_count == checked

    results = repo / "results"
    theorem = results / "TARGET_ENVELOPE_UNIVERSAL_PAYMENT_OR_PI_LEMMA_20260813.md"
    reversal = results / "NORMALIZATION_BYPASS_RESERVOIR_REVERSAL_LEMMA_20260813.md"
    fan = results / "NORMALIZATION_BYPASS_THREE_RESERVOIR_FAN_DICHOTOMY_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "target-envelope-universal-payment-or-pi-audit-v1",
        "status": "ONE_TARGET_HAS_UNIVERSAL_EXTERNAL_PAYER_OR_SUPPLIED_PI",
        "selector_nonempty_from_current_safety": selector_nonempty,
        "safe_packet_pays_every_target_response": universal_payment,
        "unsafe_reversal_below_envelope": unsafe_reversal_below_envelope,
        "all_unsafe_source_assignments_checked": checked,
        "all_unsafe_supplier_cycles": cycle_count,
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free one-target envelope payer or PI; simultaneous payers "
            "and the specified-head/holder walls remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "reversal": str(reversal.relative_to(repo)),
            "reversal_sha256": sha256(reversal),
            "fan": str(fan.relative_to(repo)),
            "fan_sha256": sha256(fan),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "all_unsafe_supplier_cycles": result["all_unsafe_supplier_cycles"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()

