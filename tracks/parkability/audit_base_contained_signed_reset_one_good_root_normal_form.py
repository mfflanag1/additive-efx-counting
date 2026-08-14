#!/usr/bin/env python3
"""Exact support/value audit of the one-good signed root reset."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subsets(items: tuple[int, ...]):
    for size in range(len(items) + 1):
        for chosen in combinations(items, size):
            yield frozenset(chosen)


def run() -> dict[str, object]:
    x, plus, minus, delta, good, residual = z3.Reals(
        "x plus minus delta good residual"
    )
    reset = z3.SolverFor("QF_LRA")
    reset.add(plus - minus == delta, good > 0, x + good <= x)
    reset_root_strict = reset.check() == z3.unsat

    loss = z3.SolverFor("QF_LRA")
    loss.add(good > 0, residual > 0, x - residual + good < x, residual <= good)
    loss_band_equivalence_forward = loss.check() == z3.unsat

    support_cases = 0
    whole_response_cases = 0
    bad_residual_cases = 0
    on_good_cases = 0
    off_good_cases = 0
    exact_base_response_cases = 0
    universe = tuple(range(7))
    for base in subsets(universe):
        outside = frozenset(universe) - base
        if not base or not outside:
            continue
        for plus_support in subsets(tuple(outside)):
            if not plus_support:
                continue
            for minus_support in subsets(tuple(base)):
                current = (base - minus_support) | plus_support
                for packet in subsets(tuple(base - minus_support)):
                    if not packet:
                        continue
                    for good_support in plus_support:
                        reset_target = base | {good_support}
                        assert packet <= reset_target
                        assert reset_target - base == {good_support}
                        for response in subsets(tuple(reset_target)):
                            if not packet <= response or response == reset_target:
                                continue
                            omitted_base = base - response
                            whole_response_cases += 1
                            bad_residual_cases += int(
                                not omitted_base <= (base - packet)
                            )
                            if good_support in response:
                                on_good_cases += 1
                                bad_residual_cases += int(not omitted_base)
                                assert response == (base - omitted_base) | {good_support}
                            else:
                                off_good_cases += 1
                                assert response == base - omitted_base
                                exact_base_response_cases += int(not omitted_base)
                        support_cases += 1

    assert support_cases > 0 and whole_response_cases > 0
    assert bad_residual_cases == 0
    assert on_good_cases > 0 and off_good_cases > 0
    assert exact_base_response_cases > 0

    theorem = ROOT / "results/BASE_CONTAINED_SIGNED_RESET_ONE_GOOD_ROOT_NORMAL_FORM_THEOREM_20260814.md"
    signed = ROOT / "results/SIGNED_MISSING_BASE_PACKET_CHARGE_OR_BASE_CONTAINMENT_THEOREM_20260814.md"
    spread = ROOT / "results/SUPPLIER_ALIGNED_BASE_DONATION_PACKET_SPREAD_THEOREM_20260814.md"
    exterior = ROOT / "results/BASE_CONTAINED_GLOBAL_EXTERIOR_SACRIFICE_ADMISSION_THEOREM_20260814.md"
    sources = ROOT / "results/EXTERIOR_DOMINANCE_THREE_AGENT_SOURCE_REDUCTION_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "one-good enlarged base root" in theorem_text
    assert "strict loss band" in theorem_text
    assert "source-inactive" in theorem_text and "base-root response" in theorem_text

    return {
        "schema": "base-contained-signed-reset-one-good-root-normal-form-audit-v1",
        "status": "BASE_CONTAINED_PACKET_NORMALIZED_TO_ONE_GOOD_ON_OFF_RESPONSE",
        "reset_root_strict": reset_root_strict,
        "loss_band_equivalence_forward": loss_band_equivalence_forward,
        "support_cases_checked": support_cases,
        "whole_packet_response_cases_checked": whole_response_cases,
        "bad_residual_support_cases": bad_residual_cases,
        "on_good_whole_response_cases": on_good_cases,
        "off_good_whole_response_cases": off_good_cases,
        "exact_base_response_cases": exact_base_response_cases,
        "new_label_or_exact_one_good_repeat": True,
        "on_good_loss_band_closed": False,
        "off_good_base_response_closed": False,
        "global_multilabel_well_foundedness_proved": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, signed, spread, exterior, sources, script)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
