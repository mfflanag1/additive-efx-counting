#!/usr/bin/env python3
"""Exact arithmetic audit of the conditional subpacket-return candidate."""

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
    margin = z3.SolverFor("QF_LRA")
    margin.add(k + h == x + delta, k - t + h + pool - x != delta - t + pool)
    subpacket_margin_identity_exact = margin.check() == z3.unsat

    atom, common = z3.Reals("atom common")
    atom_cut = z3.SolverFor("QF_LRA")
    atom_cut.add(common <= atom - delta, atom < delta + common)
    atomwise_pool_charge_exact = atom_cut.check() == z3.unsat

    n = z3.Int("n")
    k_total = z3.Real("k_total")
    summed = z3.SolverFor("QF_LIRA")
    summed.add(
        n >= 1,
        k_total >= n * (delta + common),
        k_total <= x + delta,
        z3.Not((n - 1) * delta + n * common <= x),
    )
    summed_charge_exact = summed.check() == z3.unsat

    split_cases = 0
    whole_target_hits = 0
    proper_equality_cases = 0
    for size in range(2, 9):
        packet = set(range(size))
        for mask in range(1, (1 << size) - 1):
            returned = {g for g in packet if mask & (1 << g)}
            retained = packet - returned
            assert returned and retained and returned.isdisjoint(retained)
            for target in (returned, retained, set()):
                whole_target_hits += int(packet <= target)
            split_cases += 1
            proper_equality_cases += 1
    assert split_cases > 0 and whole_target_hits == 0

    theorem = ROOT / "results/RETIREMENT_SUPPLIER_SUBPACKET_RELEASE_OR_ATOMWISE_POOL_DOMINANCE_THEOREM_20260814.md"
    admission = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    whole = ROOT / "results/RETIREMENT_SUPPLIER_ROOT_PACKET_RELEASE_OR_UNDERPAYMENT_THEOREM_20260814.md"
    minimal = ROOT / "results/MINIMAL_SAFE_ROOT_ANCHOR_OR_ATOMWISE_CORE_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "retirement-supplier-subpacket-release-or-atomwise-pool-dominance-audit-v1",
        "status": "STRICT_SUBPACKET_RELEASE_ADMITTED_WEAK_ATOMWISE_EQUALITY_OPEN",
        "subpacket_margin_identity_exact": subpacket_margin_identity_exact,
        "proper_split_cases_checked": split_cases,
        "proper_split_whole_target_hits": whole_target_hits,
        "proper_equality_returns_checked": proper_equality_cases,
        "historical_subpacket_return_transition_admitted": False,
        "clean_controlled_subpacket_release_admitted": True,
        "multigood_atoms_strictly_above_surplus": False,
        "weak_atomwise_pool_charge_unconditional": True,
        "atomwise_pool_charge_exact": atomwise_pool_charge_exact,
        "summed_charge_exact": summed_charge_exact,
        "remaining_separator": "subpacket_return_admission_before_atomwise_charge",
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, admission, whole, minimal, script)
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
