#!/usr/bin/env python3
"""Replay the reservoir theorem on the two frozen exact length-three models."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .analyze_alternating_singleton_return_models import make_cell
    from .analyze_dual_mode_adversarial_profiles import (
        allocation_efx,
        labels,
        parse_value,
        submasks,
        subset_tables,
    )
except ImportError:
    from analyze_alternating_singleton_return_models import make_cell
    from analyze_dual_mode_adversarial_profiles import (
        allocation_efx,
        labels,
        parse_value,
        submasks,
        subset_tables,
    )


# Frozen rows are converted to (p,r,s,q).
P, R, S, Q = range(4)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask(goods):
    return sum(1 << good for good in goods)


def common_safe(tails, base, bundle):
    return all(tails[agent][bundle] <= base[agent] for agent in range(4))


def desired_sources(totals, tails, base, bundle):
    if not common_safe(tails, base, bundle):
        return ()
    return tuple(agent for agent in range(4) if totals[agent][bundle] > base[agent])


def signs(totals, base, assigned, orientation):
    if orientation == "q_before_r":
        return (
            totals[P][assigned[P]] >= base[P]
            and totals[S][assigned[S]] >= base[S]
            and totals[Q][assigned[Q]] > base[Q]
        )
    return (
        totals[P][assigned[P]] >= base[P]
        and totals[S][assigned[S]] >= base[S]
        and totals[R][assigned[R]] > base[R]
    )


def serialize(cell, assigned, branch, source=None):
    return {
        "branch": branch,
        "source": source,
        "bundles": {
            name: labels(assigned[agent], cell["goods"])
            for agent, name in ((P, "p"), (R, "r"), (Q, "q"), (S, "s"))
        },
    }


def find_q_before_r(totals, tails, base, cell, external):
    tr, br, tq, bq = cell["packets"]
    x, y, f = (1 << cell[name] for name in ("x", "y", "floater"))
    desired = mask(tr) | f
    pool = mask(tq + bq + br)
    threshold = tails[R][desired]
    for payment in submasks(pool):
        assigned = [desired, payment, y, x]
        if (
            totals[R][payment] >= threshold
            and common_safe(tails, base, payment)
            and allocation_efx(totals, tails, assigned)
            and signs(totals, base, assigned, "q_before_r")
        ):
            return serialize(cell, assigned, "safe_payment")
    for boundary in submasks(pool):
        if totals[R][boundary] >= threshold:
            continue
        for source in desired_sources(totals, tails, base, boundary):
            if source == P:
                assigned = [boundary, desired, y, x]
            elif source == R:
                assigned = [desired, boundary, y, x]
            elif source == Q:
                assigned = [x, desired, y, boundary]
            elif external == P:
                assigned = [y, desired, boundary, x]
            elif external == R:
                assigned = [desired, y, boundary, x]
            else:
                assigned = [x, desired, boundary, y]
            if allocation_efx(totals, tails, assigned) and signs(
                totals, base, assigned, "q_before_r"
            ):
                return serialize(cell, assigned, "low_reversal", "prsq"[source])
    return None


def find_r_before_q(totals, tails, base, cell, external):
    tr, br, tq, bq = cell["packets"]
    x, y, f = (1 << cell[name] for name in ("x", "y", "floater"))
    desired = mask(tq) | f
    pool = mask(tr + br + bq)
    threshold = tails[Q][desired]
    for payment in submasks(pool):
        assigned = [x, desired, y, payment]
        if (
            totals[Q][payment] >= threshold
            and common_safe(tails, base, payment)
            and allocation_efx(totals, tails, assigned)
            and signs(totals, base, assigned, "r_before_q")
        ):
            return serialize(cell, assigned, "safe_payment")
    for boundary in submasks(pool):
        if totals[Q][boundary] >= threshold:
            continue
        for source in desired_sources(totals, tails, base, boundary):
            if source == R:
                assigned = [x, boundary, y, desired]
            elif source == S and external == P:
                assigned = [y, desired, boundary, x]
            elif source == S and external == R:
                assigned = [x, y, boundary, desired]
            elif source == S:
                assigned = [x, desired, boundary, y]
            else:
                continue
            if allocation_efx(totals, tails, assigned) and signs(
                totals, base, assigned, "r_before_q"
            ):
                return serialize(cell, assigned, "low_reversal", "prsq"[source])
    return None


def load_model(root, label, name, sizes):
    path = root / "results" / name
    raw = json.loads(path.read_text())
    packet_sizes = tuple(raw["packet_sizes"]) if sizes is None else sizes
    native = raw["values"]
    return label, [native[0], native[1], native[3], native[2]], packet_sizes, path


def analyze(label, raw_values, sizes):
    cell = make_cell(sizes)
    values = tuple(tuple(parse_value(value) for value in row) for row in raw_values)
    totals, tails = subset_tables(values, cell["m"])
    tr, br, tq, bq = cell["packets"]
    x, y, f = (1 << cell[name] for name in ("x", "y", "floater"))
    base_masks = (x, mask(tr + br), y, mask(tq + bq))
    base = tuple(totals[agent][base_masks[agent]] for agent in range(4))
    dp, dr = mask(tr) | f, mask(tq) | f
    assert allocation_efx(totals, tails, base_masks)
    assert P in desired_sources(totals, tails, base, dp)
    assert R in desired_sources(totals, tails, base, dr)
    assert totals[Q][x] > base[Q]
    external_sources = tuple(agent for agent in (P, R, Q) if totals[agent][y] > base[agent])
    records = []
    for external in external_sources:
        q_witness = find_q_before_r(totals, tails, base, cell, external)
        r_witness = find_r_before_q(totals, tails, base, cell, external)
        assert q_witness is not None and r_witness is not None
        records.append({
            "external_source": "prsq"[external],
            "q_before_r": q_witness,
            "r_before_q": r_witness,
        })
    return {
        "label": label,
        "packet_sizes": list(sizes),
        "extra_p_or_q_envy_of_xr": [
            "prsq"[agent]
            for agent in (P, Q)
            if totals[agent][base_masks[R]] > base[agent]
        ],
        "records": records,
    }


def run(output):
    root = Path(__file__).resolve().parents[2]
    models = (
        load_model(root, "length_three_dual_mode_atom_selected", "length_three_dual_mode_atom_selected.json", (1, 1, 1, 1)),
        load_model(root, "length_three_dual_mode_split_refutation", "length_three_dual_mode_split_refutation.json", None),
    )
    records = [analyze(label, values, sizes) for label, values, sizes, _path in models]
    result = {
        "schema": "length-three-reservoir-order-model-audit-v1",
        "status": "EXACT_FROZEN_MODEL_AUDIT",
        "model_count": len(records),
        "external_source_count": sum(len(record["records"]) for record in records),
        "orientation_escape_count": 2 * sum(len(record["records"]) for record in records),
        "models": records,
        "claim_boundary": {
            "proved": "exact reservoir-order escapes for both orientations and every external source present in the two frozen length-three models",
            "not_proved": "the arbitrary-packet theorem, which is analytic",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(root)),
            "script_sha256": sha256(Path(__file__).resolve()),
            "inputs": [
                {"path": str(path.relative_to(root)), "sha256": sha256(path)}
                for _label, _values, _sizes, path in models
            ],
        },
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({key: result[key] for key in (
        "model_count", "external_source_count", "orientation_escape_count"
    )}, indent=2))


if __name__ == "__main__":
    main()
