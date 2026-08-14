#!/usr/bin/env python3
"""Exact arithmetic/support audit of clean root-strict subpacket release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    x, delta, k, h, t, pool = z3.Reals("x delta k h t pool")
    base = [x > 0, delta > 0, k > 0, h >= 0, k + h == x + delta]

    margin = z3.SolverFor("QF_LRA")
    margin.add(*base, k - t + h + pool - x != delta - t + pool)
    margin_identity_exact = margin.check() == z3.unsat

    strict = z3.SolverFor("QF_LRA")
    strict.add(*base, pool > t - delta, k - t + h + pool <= x)
    strict_test_exact = strict.check() == z3.unsat

    singleton = z3.SolverFor("QF_LRA")
    own, atom = z3.Reals("own atom")
    singleton.add(own >= 0, atom > 0, own < atom - atom)
    singleton_target_never_strongly_envied = singleton.check() == z3.unsat

    atom_value, common = z3.Reals("atom_value common")
    atom_cut = z3.SolverFor("QF_LRA")
    atom_cut.add(common <= atom_value - delta, atom_value < delta + common)
    weak_atomwise_charge_exact = atom_cut.check() == z3.unsat

    n = z3.Int("n")
    total = z3.Real("total")
    summed = z3.SolverFor("QF_LIRA")
    summed.add(
        n >= 1,
        total >= n * (delta + common),
        total <= x + delta,
        z3.Not((n - 1) * delta + n * common <= x),
    )
    summed_charge_exact = summed.check() == z3.unsat

    support_cases = 0
    proper_split_whole_hits = 0
    full_return_deletions_checked = 0
    for size in range(1, 9):
        packet = set(range(size))
        h_support = {100, 101}
        u_old = {200, 201}
        exterior = {300, 301, 302}
        universe = packet | h_support | u_old | exterior
        for t_mask in range(1, 1 << size):
            returned = {g for g in packet if t_mask & (1 << g)}
            retained = packet - returned
            for r_mask in range(1 << len(exterior)):
                ordered = tuple(sorted(exterior))
                pool_support = {
                    ordered[j] for j in range(len(ordered)) if r_mask & (1 << j)
                }
                targets = (
                    retained | h_support | pool_support,
                    returned,
                    exterior - pool_support,
                    u_old,
                )
                assert set().union(*targets) == universe
                assert sum(map(len, targets)) == len(universe)
                intersections = [target & packet for target in targets]
                if returned != packet:
                    proper_split_whole_hits += sum(packet <= hit for hit in intersections)
                else:
                    assert intersections[0] == set()
                    assert intersections[1] == packet
                    if size >= 2:
                        for good in packet:
                            assert packet - {good} < packet
                            full_return_deletions_checked += 1
                support_cases += 1

    assert proper_split_whole_hits == 0
    assert support_cases > 0 and full_return_deletions_checked > 0

    theorem = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    correction = ROOT / "results/RETIREMENT_SUPPLIER_RETURN_ADMISSIBILITY_CORRECTION_20260814.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "controlled root/anchor release candidate" in theorem_text
    assert "equality face is separately eliminated" in theorem_text

    return {
        "schema": "root-strict-clean-subpacket-release-admission-audit-v1",
        "status": "STRICT_CLEAN_SUBPACKET_RELEASE_ADMITTED_EQUALITY_OPEN",
        "margin_identity_exact": margin_identity_exact,
        "strict_test_exact": strict_test_exact,
        "physical_support_cases_checked": support_cases,
        "proper_split_whole_packet_hits": proper_split_whole_hits,
        "full_return_proper_deletions_checked": full_return_deletions_checked,
        "singleton_target_never_strongly_envied": singleton_target_never_strongly_envied,
        "weak_atomwise_charge_exact": weak_atomwise_charge_exact,
        "summed_charge_exact": summed_charge_exact,
        "historical_reversibility_used": False,
        "root_equality_closed": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, contract, correction, script)
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
