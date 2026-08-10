#!/usr/bin/env python3
"""Audit the cap-free dual-mode potential on frozen adversarial profiles."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from .analyze_alternating_singleton_return_models import make_cell
except ImportError:
    from analyze_alternating_singleton_return_models import make_cell


SCHEMA = "dual-mode-adversarial-profile-audit-v1"
P, R, S, Q = range(4)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_value(value):
    return Fraction(value) if isinstance(value, str) else Fraction(value, 1)


def subset_tables(values, m):
    size = 1 << m
    totals = [[Fraction(0) for _ in range(size)] for _ in range(4)]
    minimums = [[None for _ in range(size)] for _ in range(4)]
    for mask in range(1, size):
        bit = mask & -mask
        good = bit.bit_length() - 1
        rest = mask ^ bit
        for agent in range(4):
            value = values[agent][good]
            totals[agent][mask] = totals[agent][rest] + value
            old_minimum = minimums[agent][rest]
            minimums[agent][mask] = value if old_minimum is None else min(value, old_minimum)
    tails = [[Fraction(0) for _ in range(size)] for _ in range(4)]
    for agent in range(4):
        for mask in range(1, size):
            tails[agent][mask] = totals[agent][mask] - minimums[agent][mask]
    return totals, tails


def submasks(mask):
    current = mask
    while True:
        yield current
        if current == 0:
            return
        current = (current - 1) & mask


def labels(mask, goods):
    return [goods[good] for good in range(len(goods)) if mask & (1 << good)]


def allocation_efx(totals, tails, assigned):
    return all(
        totals[observer][assigned[observer]] >= tails[observer][assigned[target]]
        for observer in range(4)
        for target in range(4)
    )


def compatible_pair(totals, tails, base, p_mask, q_mask):
    return (
        totals[P][p_mask] > base[P]
        and totals[Q][q_mask] > base[Q]
        and tails[P][q_mask] <= totals[P][p_mask]
        and tails[Q][p_mask] <= totals[Q][q_mask]
        and tails[R][p_mask] <= base[R]
        and tails[R][q_mask] <= base[R]
        and tails[S][p_mask] <= base[S]
        and tails[S][q_mask] <= base[S]
    )


def find_payment(totals, tails, base, y_mask, p_mask, q_mask, residual, mode):
    payment_agent = R if mode == "r" else S
    singleton_agent = S if mode == "r" else R
    for payment in submasks(residual):
        if totals[payment_agent][payment] < base[payment_agent]:
            continue
        assigned = [0, 0, 0, 0]
        assigned[P] = p_mask
        assigned[Q] = q_mask
        assigned[payment_agent] = payment
        assigned[singleton_agent] = y_mask
        if allocation_efx(totals, tails, assigned):
            return tuple(assigned)
    return None


def minimal_payment(totals, base, residual, agent):
    candidates = [mask for mask in submasks(residual) if totals[agent][mask] >= base[agent]]
    candidates.sort(key=lambda mask: (mask.bit_count(), totals[agent][mask], mask))
    for mask in candidates:
        if all(totals[agent][mask ^ (1 << good)] < base[agent] for good in range(mask.bit_length()) if mask & (1 << good)):
            return mask
    raise AssertionError("feasible mode has no minimal payment")


def minimal_relative_blocker(totals, thresholds, container):
    candidates = []
    for mask in submasks(container):
        sources = [agent for agent in range(4) if totals[agent][mask] > thresholds[agent]]
        if not sources:
            continue
        if all(
            all(totals[agent][mask ^ (1 << good)] <= thresholds[agent] for agent in range(4))
            for good in range(mask.bit_length())
            if mask & (1 << good)
        ):
            candidates.append((mask.bit_count(), mask, sources))
    if not candidates:
        return None
    _, mask, sources = min(candidates)
    return mask, sources


def extract_certificate(totals, tails, base, full_without_y, y_mask, feasible_pairs, goods):
    p_mask, q_mask, modes = max(
        feasible_pairs,
        key=lambda item: (totals[P][item[0]], totals[Q][item[1]]),
    )
    residual = full_without_y ^ p_mask ^ q_mask
    for mode in modes:
        payment_agent = R if mode == "r" else S
        payment = minimal_payment(totals, base, residual, payment_agent)
        assigned = [p_mask, 0, 0, q_mask]
        assigned[payment_agent] = payment
        assigned[S if mode == "r" else R] = y_mask
        if allocation_efx(totals, tails, assigned):
            continue
        thresholds = [totals[P][p_mask], base[R], base[S], totals[Q][q_mask]]
        for good in range(payment.bit_length()):
            if not payment & (1 << good):
                continue
            container = payment ^ (1 << good)
            blocker = minimal_relative_blocker(totals, thresholds, container)
            if blocker is None:
                continue
            blocker_mask, sources = blocker
            for source in sources:
                if source not in (P, Q):
                    continue
                old = p_mask if source == P else q_mask
                new_residual = (residual ^ blocker_mask) | old
                return {
                    "mode": mode,
                    "p_bundle": labels(p_mask, goods),
                    "q_bundle": labels(q_mask, goods),
                    "payment": labels(payment, goods),
                    "removed_payment_good": goods[good],
                    "source": "p" if source == P else "q",
                    "boundary_bundle": labels(blocker_mask, goods),
                    "old_source_bundle": labels(old, goods),
                    "new_residual": labels(new_residual, goods),
                    "new_residual_r_value": str(totals[R][new_residual]),
                    "new_residual_s_value": str(totals[S][new_residual]),
                    "r_base": str(base[R]),
                    "s_base": str(base[S]),
                    "simultaneous_deficit": (
                        totals[R][new_residual] < base[R]
                        and totals[S][new_residual] < base[S]
                    ),
                    "opposite_tail": str(tails[S if mode == "r" else R][blocker_mask]),
                    "opposite_base": str(base[S if mode == "r" else R]),
                }
    return None


def analyze_profile(label, raw_values, sizes):
    cell = make_cell(sizes)
    values = tuple(tuple(parse_value(value) for value in row) for row in raw_values)
    if any(len(row) != cell["m"] for row in values):
        raise ValueError((label, sizes, cell["m"], tuple(len(row) for row in values)))
    totals, tails = subset_tables(values, cell["m"])
    tr, br, tq, bq = cell["packets"]
    base_bundles = ((cell["x"],), tr + br, (cell["y"],), tq + bq)
    base_masks = tuple(sum(1 << good for good in bundle) for bundle in base_bundles)
    base = tuple(totals[agent][base_masks[agent]] for agent in range(4))
    y_mask = 1 << cell["y"]
    x_mask = 1 << cell["x"]
    floater_mask = 1 << cell["floater"]
    full_without_y = ((1 << cell["m"]) - 1) ^ y_mask
    canonical_p = sum(1 << good for good in tr) | floater_mask
    canonical = {
        "compatible": compatible_pair(totals, tails, base, canonical_p, x_mask),
        "escape": None,
    }
    if canonical["compatible"]:
        canonical_residual = full_without_y ^ canonical_p ^ x_mask
        for canonical_mode in ("r", "s"):
            canonical_agent = R if canonical_mode == "r" else S
            if totals[canonical_agent][canonical_residual] < base[canonical_agent]:
                continue
            canonical_assigned = find_payment(
                totals,
                tails,
                base,
                y_mask,
                canonical_p,
                x_mask,
                canonical_residual,
                canonical_mode,
            )
            if canonical_assigned is not None:
                canonical["escape"] = {
                    "mode": canonical_mode,
                    "bundles": {
                        name: labels(canonical_assigned[agent], cell["goods"])
                        for agent, name in enumerate(("p", "r", "s", "q"))
                    },
                }
                break
    compatible_count = 0
    mode_counts = {"r": 0, "s": 0}
    feasible_pairs = []
    witness = None
    p_mask = full_without_y
    while True:
        remaining = full_without_y ^ p_mask
        q_mask = remaining
        while True:
            if compatible_pair(totals, tails, base, p_mask, q_mask):
                compatible_count += 1
                residual = remaining ^ q_mask
                modes = []
                if totals[R][residual] >= base[R]:
                    modes.append("r")
                if totals[S][residual] >= base[S]:
                    modes.append("s")
                if modes:
                    feasible_pairs.append((p_mask, q_mask, tuple(modes)))
                for mode in modes:
                    mode_counts[mode] += 1
                    if witness is None:
                        assigned = find_payment(
                            totals, tails, base, y_mask, p_mask, q_mask, residual, mode
                        )
                        if assigned is not None:
                            witness = {
                                "mode": mode,
                                "bundles": {
                                    name: labels(assigned[agent], cell["goods"])
                                    for agent, name in enumerate(("p", "r", "s", "q"))
                                },
                                "utilities": [str(totals[agent][assigned[agent]]) for agent in range(4)],
                            }
            if q_mask == 0:
                break
            q_mask = (q_mask - 1) & remaining
        if p_mask == 0:
            break
        p_mask = (p_mask - 1) & full_without_y
    certificate = None
    if witness is None and feasible_pairs:
        certificate = extract_certificate(
            totals, tails, base, full_without_y, y_mask, feasible_pairs, cell["goods"]
        )
    return {
        "label": label,
        "packet_sizes": list(sizes),
        "compatible_pair_count": compatible_count,
        "mode_feasible_pair_counts": mode_counts,
        "canonical_pair": canonical,
        "direct_dual_mode_escape": witness,
        "surviving_certificate": certificate,
    }


def load_profiles(root):
    profiles = []
    atomic_path = root / "results/alternating_anchored_or_promoted_atomic_audit.json"
    atomic = json.loads(atomic_path.read_text())
    for index, record in enumerate(atomic["anchored_countermodels"]):
        profiles.append((f"fixed_hard_order_{index}", record["values"], (1, 1, 1, 1)))
    pareto_path = root / "results/alternating_cross_bottom_obstruction_audit.json"
    pareto = json.loads(pareto_path.read_text())
    profiles.append(("pareto_maximal_vstar", pareto["profile"]["values"], (1, 1, 1, 1)))

    session_path = root / "results/alternating_singleton_return_0213_session1.json"
    session = json.loads(session_path.read_text())
    for record in session["trace"]:
        profiles.append((f"frozen_iteration_{record['iteration']}", record["values"], (2, 2, 2, 2)))
    audit_names = (
        "alternating_bottom_partition_dichotomy_2222_audit.json",
        "alternating_any_root_subset_dichotomy_2222_audit.json",
        "alternating_any_cross_subset_dichotomy_2222_audit.json",
        "alternating_base_q_remainder_gate_2222.json",
        "alternating_base_q_remainder_recipient_relaxed_gate_2222.json",
        "alternating_base_q_remainder_exact_efx_gate_2222.json",
    )
    for name in audit_names:
        record = json.loads((root / "results" / name).read_text())
        profiles.append((Path(name).stem, record["values"], (2, 2, 2, 2)))

    qface_path = root / "results/alternating_safe_pair_qface_remainder_2222.json"
    qface = json.loads(qface_path.read_text())
    profiles.append(("augmented_q_face_remainder", qface["model"], tuple(qface["packet_sizes"])))
    inputs = [atomic_path, pareto_path, session_path, qface_path]
    inputs.extend(root / "results" / name for name in audit_names)
    return profiles, inputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    profiles, inputs = load_profiles(root)
    records = [analyze_profile(*profile) for profile in profiles]
    result = {
        "schema": SCHEMA,
        "status": "EXACT_ADVERSARIAL_CORPUS_AUDIT",
        "profile_count": len(records),
        "direct_escape_profile_count": sum(record["direct_dual_mode_escape"] is not None for record in records),
        "simultaneous_deficit_profile_count": sum(
            record["surviving_certificate"] is not None
            and record["surviving_certificate"]["simultaneous_deficit"]
            for record in records
        ),
        "profiles": records,
        "claim_boundary": {
            "proved": "the exact dual-mode census for the listed frozen profiles",
            "not_proved": "the cap-free length-three escape lemma",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(root)),
            "script_sha256": sha256(Path(__file__).resolve()),
            "inputs": [
                {"path": str(path.relative_to(root)), "sha256": sha256(path)} for path in inputs
            ],
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in ("profile_count", "direct_escape_profile_count", "simultaneous_deficit_profile_count")}, indent=2))


if __name__ == "__main__":
    main()
