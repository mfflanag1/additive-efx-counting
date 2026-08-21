#!/usr/bin/env python3
"""Independent Fraction audit of the terminal anchor-good split lemmas.

No SMT or decision-driver code is imported.  The proof bounds every exact EFX
slack after assigning one anchor-minimum good to the first recipient and all
remaining split-role goods to the second recipient.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
SUPPLIER = {
    role: source
    for source, roles in {
        "r": ("a0", "a1", "h"),
        "q": ("j", "k", "q0"),
        "d": ("m", "gq", "gr"),
        "s": ("l", "e"),
        "charity": ("p",),
    }.items()
    for role in roles
}
LEMMAS = {
    "A_q_min_a1_anchor": {
        "split_role": "a1",
        "anchor_observer": "q",
        "first_recipient": "d",
        "second_recipient": "q",
        "whole_roles": {
            "d": ("h", "m", "gq", "gr"),
            "q": ("j",),
            "r": ("a0", "k", "q0"),
            "s": ("l", "e", "p"),
        },
    },
    "B_r_min_k_anchor": {
        "split_role": "k",
        "anchor_observer": "r",
        "first_recipient": "q",
        "second_recipient": "r",
        "whole_roles": {
            "d": ("l", "m", "gq", "gr"),
            "q": ("j", "q0", "p"),
            "r": ("a0", "a1"),
            "s": ("h", "e"),
        },
    },
}


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def load_rows(raw, key):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[key].items()
    }


def bundle_affine(lemma, observer, owner, totals):
    """Return constant and chosen-good coefficient for a bundle total."""
    constant = sum(
        (totals[observer][role] for role in lemma["whole_roles"][owner]),
        Fraction(),
    )
    role_total = totals[observer][lemma["split_role"]]
    if owner == lemma["first_recipient"]:
        return constant, Fraction(1)
    if owner == lemma["second_recipient"]:
        return constant + role_total, Fraction(-1)
    return constant, Fraction()


def lower_bound_affine(constant, coefficient, lower, upper):
    endpoint = lower if coefficient >= 0 else upper
    return constant + coefficient * endpoint


def audit_lemma(name, lemma, totals, minima, require_nonnegative=True):
    role = lemma["split_role"]
    anchor = lemma["anchor_observer"]
    if any(
        totals[observer][role] < 2 * minima[observer][role]
        for observer in OWNERS
    ):
        return {
            "split_role": role,
            "anchor_observer": anchor,
            "applicable": False,
            "reason": "no joint realization with a selected good and nonempty complement",
        }
    inequalities = []
    for observer in OWNERS:
        total = totals[observer][role]
        minimum = minima[observer][role]
        x_lower = x_upper = minimum if observer == anchor else None
        if observer != anchor:
            x_lower, x_upper = minimum, total - minimum
            if x_upper < x_lower:
                return {
                    "split_role": role,
                    "anchor_observer": anchor,
                    "applicable": False,
                    "reason": "no realization with a selected good and nonempty complement",
                }
        own_constant, own_coefficient = bundle_affine(
            lemma, observer, observer, totals
        )
        for target in OWNERS:
            if target == observer:
                continue
            target_constant, target_coefficient = bundle_affine(
                lemma, observer, target, totals
            )
            base_constant = own_constant - target_constant
            base_coefficient = own_coefficient - target_coefficient
            candidates = [
                (f"whole:{whole_role}", minima[observer][whole_role], Fraction())
                for whole_role in lemma["whole_roles"][target]
            ]
            if target == lemma["first_recipient"]:
                # Delete the selected anchor good: add x.
                candidates.append(("selected_split_good", Fraction(), Fraction(1)))
            elif target == lemma["second_recipient"]:
                # Every complement good is at least the prescribed role minimum.
                candidates.append(("arbitrary_complement_good", minimum, Fraction()))
            assert candidates
            for deletion, deletion_constant, deletion_coefficient in candidates:
                constant = base_constant + deletion_constant
                coefficient = base_coefficient + deletion_coefficient
                lower_bound = lower_bound_affine(
                    constant, coefficient, x_lower, x_upper
                )
                if require_nonnegative:
                    assert lower_bound >= 0, (
                        name, observer, target, deletion, lower_bound
                    )
                inequalities.append({
                    "observer": observer,
                    "target": target,
                    "deletion": deletion,
                    "constant": str(constant),
                    "chosen_good_coefficient": str(coefficient),
                    "chosen_good_lower": str(x_lower),
                    "chosen_good_upper": str(x_upper),
                    "certified_slack_lower_bound": str(lower_bound),
                })

    role_assignment = {
        role_name: owner
        for owner, roles in lemma["whole_roles"].items() for role_name in roles
    }
    role_assignment[role] = lemma["second_recipient"]
    edges = {
        (SUPPLIER[role_name], owner)
        for role_name, owner in role_assignment.items()
        if SUPPLIER[role_name] != owner
    }
    # The selected good adds the split role's first-recipient edge.
    if SUPPLIER[role] != lemma["first_recipient"]:
        edges.add((SUPPLIER[role], lemma["first_recipient"]))
    assert len(edges) <= 4
    return {
        "split_role": role,
        "anchor_observer": anchor,
        "applicable": True,
        "verified": all(
            Fraction(item["certified_slack_lower_bound"]) >= 0
            for item in inequalities
        ),
        "selector": (
            f"choose any {role} good attaining observer {anchor}'s prescribed "
            f"minimum; give it alone to {lemma['first_recipient']} and every "
            f"remaining {role} good to {lemma['second_recipient']}"
        ),
        "edge_count": len(edges),
        "edges": [list(edge) for edge in sorted(edges)],
        "minimum_certified_slack": str(min(
            Fraction(item["certified_slack_lower_bound"])
            for item in inequalities
        )),
        "inequalities": inequalities,
    }


def witness_pattern_count(role, cardinality, totals, minima):
    count = 1
    row_counts = {}
    for observer in OWNERS:
        total = totals[observer][role]
        minimum = minima[observer][role]
        if total < cardinality * minimum:
            row_count = 0
        elif total == cardinality * minimum:
            row_count = 1
        else:
            row_count = (1 << cardinality) - 2
        row_counts[observer] = row_count
        count *= row_count
    return count, row_counts


def run(profile_path, output_path):
    raw = json.loads(profile_path.read_text())
    totals = load_rows(raw, "profile_totals")
    minima = load_rows(raw, "profile_minima")
    audits = {
        name: audit_lemma(name, lemma, totals, minima)
        for name, lemma in LEMMAS.items()
    }
    coverage = {}
    for role, cardinalities in {"a1": range(2, 8), "k": range(2, 4)}.items():
        coverage[role] = []
        for cardinality in cardinalities:
            count, rows = witness_pattern_count(
                role, cardinality, totals, minima
            )
            assert count > 0
            coverage[role].append({
                "cardinality": cardinality,
                "labelled_minimum_witness_pattern_count": count,
                "row_pattern_counts": rows,
                "packet_assignment_count_exhausted_by_decision": 1 << cardinality,
            })
    result = {
        "schema": "fixed-u-split-switching-anchor-lemma-audit-v1",
        "status": "VERIFIED_BOTH_ANCHOR_SELECTORS_UNIVERSAL",
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "method": (
            "independent exact Fraction lower bounds; no SMT or template-decision "
            "module imported"
        ),
        "lemmas": audits,
        "coverage": coverage,
        "abstract_lemma": (
            "For a two-recipient split template, if every exact EFX slack after "
            "sending one anchor-minimum good to the first recipient and the "
            "nonempty complement to the second is nonnegative over x_i in "
            "[M_i,T_i-M_i] (with anchor row x=M), then that allocation is EFX "
            "for every finite realization with at least two goods."
        ),
        "claim_boundary": (
            "Both selectors are cap-free for the immutable terminal totals/minima "
            "and arbitrary realizations of every whole role. This does not show "
            "that the anchor inequalities follow from every saturated GG state."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.profile, args.output)
    print(json.dumps({
        "status": result["status"],
        "selectors": {
            name: {
                "minimum_certified_slack": audit["minimum_certified_slack"],
                "edges": audit["edges"],
            }
            for name, audit in result["lemmas"].items()
        },
    }, indent=2))


if __name__ == "__main__":
    main()
