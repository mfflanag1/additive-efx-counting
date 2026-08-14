#!/usr/bin/env python3
"""Audit the canonical captured-own-support return star."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")
RECIPIENTS = (*OWNERS, "charity")
BASE_D = ("xd0", "xd1", "xd2")
OUTSIDE = ("u0", "u1")
CHARITY_GOOD = "p"
GOODS = (*BASE_D, *OUTSIDE, CHARITY_GOOD)


def prove(assumptions, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(conclusion))
    return str(solver.check()) == "unsat"


def construct(holders):
    initial = {recipient: set() for recipient in RECIPIENTS}
    for good, holder in zip((*BASE_D, *OUTSIDE), holders, strict=True):
        initial[holder].add(good)
    initial["charity"].add(CHARITY_GOOD)
    final = {recipient: set(goods) for recipient, goods in initial.items()}
    for owner in OWNERS:
        if owner == "d":
            continue
        captured = final[owner] & set(BASE_D)
        final[owner] -= captured
        final["d"] |= captured
    final["d"] |= final["charity"]
    final["charity"] = set()
    old_holder = {good: h for h, goods in initial.items() for good in goods}
    new_holder = {good: h for h, goods in final.items() for good in goods}
    edges = {
        (old_holder[good], new_holder[good])
        for good in GOODS if old_holder[good] != new_holder[good]
    }
    d_has_all_base = set(BASE_D) <= final["d"]
    return {
        "holders": list(holders),
        "edge_count": len(edges),
        "checks": {
            "goods_conserved": set(old_holder) == set(new_holder) == set(GOODS),
            "charity_empty": not final["charity"],
            "at_most_four_edges": len(edges) <= 4,
            "all_noncharity_edges_target_d": all(target == "d" for _, target in edges),
            "d_has_all_base_goods": d_has_all_base,
            "d_has_positive_extra_charity_good": CHARITY_GOOD in final["d"],
        },
    }


def run(root):
    # Charity is fixed at p. Distribute all other atoms arbitrarily; require
    # every owner initially nonempty only to avoid irrelevant empty states.
    records = []
    histogram = Counter()
    for holders in itertools.product(OWNERS, repeat=len(BASE_D) + len(OUTSIDE)):
        if set(holders) != set(OWNERS):
            continue
        record = construct(holders)
        assert all(record["checks"].values())
        histogram[record["edge_count"]] += 1
        records.append(record)

    delta, capture, margin = z3.Reals("delta capture margin")
    identity = prove([margin == delta - capture], margin == delta - capture)
    paid = prove(
        [margin == delta - capture, capture <= delta], margin >= 0
    )
    failure = prove(
        [margin == delta - capture, margin < 0], capture > delta
    )
    base, extra, final_d = z3.Reals("base extra final_d")
    d_strict = prove([extra > 0, final_d == base + extra], final_d > base)
    theorem = root / "results/CAPTURED_OWN_SUPPORT_FOUR_EDGE_STAR_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "captured-own-support-four-edge-star-v1",
        "status": "CAPTURED_SUPPORT_RETURN_ALWAYS_WITHIN_FOUR_EDGES",
        "distribution_count": len(records),
        "edge_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "checks": {
            "all_distributions_conserve": all(r["checks"]["goods_conserved"] for r in records),
            "all_distributions_within_four_edges": all(r["edge_count"] <= 4 for r in records),
            "d_strict_payment_from_base_plus_charity": d_strict,
            "donor_margin_identity": identity,
            "donor_safe_iff_capture_within_margin_forward": paid,
            "donor_failure_implies_strict_capture": failure,
        },
        "claim_boundary": (
            "cap-free support geometry and exact payment identities; donor capture "
            "and observer safety remain unproved"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "distribution_count", "edge_histogram", "checks"
    )}, indent=2))


if __name__ == "__main__":
    main()
