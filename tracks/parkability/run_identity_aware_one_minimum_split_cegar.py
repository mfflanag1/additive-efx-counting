#!/usr/bin/env python3
"""Identity-aware repair of the one-minimum-split four-edge selector.

`run_exact_response_one_minimum_split_cegar.py` splits a role into a least
good and its complement and then assigns *both* pieces the role minimum `M` as
their deletion floor.  That floor is sound but unattainable: no realization has
both pieces at minimum `M` while the pieces are worth `M` and `T-M`.  The
selector is identity-blind twice over -- it assumes one least good common to
all four observers, and it lets every observer's witness sit on whichever side
hurts most, independently in each constraint.  Its banked verdict
`SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION` is therefore an artifact.

This driver asks the real question instead.  For a candidate totals/minima
profile it tries, in order:

*Branch W (whole roles).*  An allocation that splits no role.  By the
cardinality-free form of Lemma C such an allocation sees only `T` and `M`, so
it is EFX in every physical realization at once, at every role cardinality.

*Branch S (one tame split).*  An allocation family splitting exactly one role
`C` of slack `rho(C) = 2`.  Lemma B forces `C` to have exactly two goods with
column `{M, T-M}`, so its only freedom is the side pattern `s : N -> {0,1}`
naming the good that carries each observer's minimum, and swapping the two
goods is a relabelling.  Eight patterns therefore exhaust the realizations of
`C`, and each is allowed its own allocation -- the quantifier the blind
selector got wrong.  A piece is a single good, so its deletion floor is its own
value, `M` on the witness side and `T-M` off it.

A wild role, `rho >= 3`, may carry three or more goods, and then the two-good
column is not forced; this driver never splits one, and reports the profile as
an obstruction if no branch closes it.

Both branches emit an exact symbolic cut in the master's `(T, M)` unknowns, so
the premise CEGAR continues against the fixed-`U` chart.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import support_supplier
from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


WHOLE = "whole"
LOW = "p0"
HIGH = "p1"


def pieces_for(split_role):
    """Named pieces of the move family: whole roles, plus C's two goods."""
    return tuple(
        piece
        for role in GOODS
        for piece in (
            ((role, LOW), (role, HIGH)) if role == split_role
            else ((role, WHOLE),)
        )
    )


def piece_is_witness_side(kind, pattern, observer):
    """Does this piece carry `observer`'s minimum under this side pattern?"""
    return (pattern[observer] == 0) if kind == LOW else (pattern[observer] == 1)


def numeric_piece_value(totals, minima, observer, piece, pattern):
    role, kind = piece
    if kind == WHOLE:
        return totals[observer][role]
    if piece_is_witness_side(kind, pattern, observer):
        return minima[observer][role]
    return totals[observer][role] - minima[observer][role]


def numeric_piece_floor(totals, minima, observer, piece, pattern):
    """Smallest deletion candidate this piece offers its bundle.

    A whole role of any cardinality offers exactly `M`.  A piece of a tame
    split role is a single good, so it offers its own value.
    """
    role, kind = piece
    if kind == WHOLE:
        return minima[observer][role]
    return numeric_piece_value(totals, minima, observer, piece, pattern)


def symbolic_piece_value(total, minimum, observer, piece, pattern):
    role, kind = piece
    if kind == WHOLE:
        return total[role, observer]
    if piece_is_witness_side(kind, pattern, observer):
        return minimum[role, observer]
    return total[role, observer] - minimum[role, observer]


def symbolic_piece_floor(total, minimum, observer, piece, pattern):
    role, kind = piece
    if kind == WHOLE:
        return minimum[role, observer]
    return symbolic_piece_value(total, minimum, observer, piece, pattern)


def side_patterns():
    """The eight side patterns, with observer r pinned to break relabelling."""
    others = [o for o in OWNERS if o != "r"]
    return tuple(
        {"r": 0, **dict(zip(others, bits))}
        for bits in itertools.product((0, 1), repeat=len(others))
    )


def numeric_oracle(totals, minima, split_role, pattern, edge_cap=4):
    """A complete four-edge EFX allocation for one concrete realization."""
    pieces = pieces_for(split_role)
    supplier = support_supplier()
    x = {(piece, owner): z3.Bool(f"x_{piece[0]}_{piece[1]}_{owner}")
         for piece in pieces for owner in OWNERS}
    edge = {(source, target): z3.Bool(f"e_{source}_{target}")
            for source in SUPPORT_STATE for target in OWNERS if source != target}
    solver = z3.Solver()
    for piece in pieces:
        solver.add(z3.PbEq([(x[piece, owner], 1) for owner in OWNERS], 1))
        source = supplier[piece[0]]
        for target in OWNERS:
            if target != source:
                solver.add(z3.Implies(x[piece, target], edge[source, target]))
    solver.add(z3.PbLe([(flag, 1) for flag in edge.values()], edge_cap))

    def rv(value):
        return z3.RealVal(f"{value.numerator}/{value.denominator}")

    utility = {
        (observer, target): z3.Sum(*(
            z3.If(x[piece, target],
                  rv(numeric_piece_value(totals, minima, observer, piece, pattern)),
                  z3.RealVal(0))
            for piece in pieces
        ))
        for observer in OWNERS for target in OWNERS
    }
    for observer in OWNERS:
        for target in OWNERS:
            if target == observer:
                continue
            for piece in pieces:
                floor = numeric_piece_floor(
                    totals, minima, observer, piece, pattern
                )
                solver.add(z3.Implies(
                    x[piece, target],
                    utility[observer, observer] >= utility[observer, target]
                    - rv(floor),
                ))
    if solver.check() != z3.sat:
        return None
    model = solver.model()
    return {
        owner: [list(p) for p in pieces if z3.is_true(model.eval(x[p, owner]))]
        for owner in OWNERS
    }


def exact_audit(allocation, totals, minima, split_role, pattern, edge_cap=4):
    """Re-check completeness, the edge budget and EFX outside z3."""
    placed = [tuple(p) for pieces in allocation.values() for p in pieces]
    assert sorted(placed) == sorted(pieces_for(split_role)), placed
    supplier = support_supplier()
    edges = sorted({
        (supplier[role], owner)
        for owner, pieces in allocation.items()
        for role, _ in pieces
        if supplier[role] != owner
    })
    assert len(edges) <= edge_cap, edges
    for observer in OWNERS:
        own = sum(
            (numeric_piece_value(totals, minima, observer, tuple(p), pattern)
             for p in allocation[observer]),
            Fraction(),
        )
        for target in OWNERS:
            if target == observer:
                continue
            gross = sum(
                (numeric_piece_value(totals, minima, observer, tuple(p), pattern)
                 for p in allocation[target]),
                Fraction(),
            )
            for piece in allocation[target]:
                floor = numeric_piece_floor(
                    totals, minima, observer, tuple(piece), pattern
                )
                assert own >= gross - floor, (observer, target, piece)
    return edges


def symbolic_efx(allocation, total, minimum, split_role, pattern):
    bundles = {o: [tuple(p) for p in allocation[o]] for o in OWNERS}
    utility = {
        (observer, target): z3.Sum(*(
            symbolic_piece_value(total, minimum, observer, piece, pattern)
            for piece in bundles[target]
        )) if bundles[target] else z3.RealVal(0)
        for observer in OWNERS for target in OWNERS
    }
    clauses = []
    for observer in OWNERS:
        for target in OWNERS:
            if target == observer:
                continue
            for piece in bundles[target]:
                clauses.append(
                    utility[observer, observer] >= utility[observer, target]
                    - symbolic_piece_floor(
                        total, minimum, observer, piece, pattern
                    )
                )
    return z3.And(*clauses)


def tame_guard(total, minimum, role):
    """Slack of `role` is exactly two: multi-good, and some observer sees T < 3M."""
    return z3.And(
        z3.And(*(2 * minimum[role, o] <= total[role, o] for o in OWNERS)),
        z3.Or(*(total[role, o] < 3 * minimum[role, o] for o in OWNERS)),
    )


def role_slack_is_two(totals, minima, role):
    ratios = [totals[o][role] // minima[o][role] for o in OWNERS]
    return min(ratios) == 2


def role_is_multi(totals, minima, role):
    return all(totals[o][role] >= 2 * minima[o][role] for o in OWNERS)


def close_profile(totals, minima, edge_cap, want_audit=True):
    """Try branch W, then branch S.  Return a closing certificate or None."""
    trivial = {o: 0 for o in OWNERS}
    whole = numeric_oracle(totals, minima, None, trivial, edge_cap)
    if whole is not None:
        if want_audit:
            exact_audit(whole, totals, minima, None, trivial, edge_cap)
        return {
            "branch": "W",
            "split_role": None,
            "allocations": {"whole": whole},
            "realization_free": True,
        }

    tame = [
        role for role in GOODS
        if role_is_multi(totals, minima, role)
        and role_slack_is_two(totals, minima, role)
    ]
    for role in tame:
        menu = {}
        for pattern in side_patterns():
            found = numeric_oracle(totals, minima, role, pattern, edge_cap)
            if found is None:
                menu = None
                break
            if want_audit:
                exact_audit(found, totals, minima, role, pattern, edge_cap)
            menu["".join(str(pattern[o]) for o in OWNERS)] = found
        if menu is not None:
            return {
                "branch": "S",
                "split_role": role,
                "allocations": menu,
                "realization_free": True,
            }
    return None


def certificate_cut(certificate, total, minimum):
    """The symbolic condition under which this certificate closes a profile."""
    if certificate["branch"] == "W":
        trivial = {o: 0 for o in OWNERS}
        return symbolic_efx(
            certificate["allocations"]["whole"], total, minimum, None, trivial
        )
    role = certificate["split_role"]
    clauses = [tame_guard(total, minimum, role)]
    for pattern in side_patterns():
        key = "".join(str(pattern[o]) for o in OWNERS)
        clauses.append(symbolic_efx(
            certificate["allocations"][key], total, minimum, role, pattern
        ))
    return z3.And(*clauses)


def summarize(certificate):
    if certificate is None:
        return None
    return {
        "branch": certificate["branch"],
        "split_role": certificate["split_role"],
        "allocation_count": len(certificate["allocations"]),
        "allocations": certificate["allocations"],
    }


def run_profile(profile_path, output_path, edge_cap):
    raw = json.loads(profile_path.read_text())
    totals = {
        o: {g: Fraction(a) for g, a in row.items()}
        for o, row in raw["countermodel_totals"].items()
    }
    minima = {
        o: {g: Fraction(a) for g, a in row.items()}
        for o, row in raw["countermodel_minima"].items()
    }
    certificate = close_profile(totals, minima, edge_cap)
    slacks = {
        role: str(min(totals[o][role] // minima[o][role] for o in OWNERS))
        for role in GOODS
    }
    result = {
        "schema": "identity-aware-one-minimum-split-profile-v1",
        "status": (
            "CLOSED_REALIZATION_FREE" if certificate is not None
            else "NO_TAME_BRANCH_CLOSES_THIS_PROFILE"
        ),
        "mode": "profile",
        "source_profile": str(profile_path),
        "source_profile_sha256":
            hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "superseded_status": raw.get("status"),
        "edge_cap": edge_cap,
        "role_slacks": slacks,
        "certificate": summarize(certificate),
        "claim_boundary": (
            "CLOSED_REALIZATION_FREE means every physical realization of this "
            "profile, at every role cardinality and every witness identity, "
            "admits a complete EFX allocation within the edge budget using at "
            "most one split role.  It supersedes the identity-blind verdict "
            "banked for this profile.  It does not establish chart coverage or "
            "the universal fixed-U theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def run_chart(output_path, form_index, maximum_rounds, timeout_seconds,
              random_seed, edge_cap):
    solver, total, minimum = build_physical_master(form_index)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    rounds = []
    result = {
        "schema": "identity-aware-one-minimum-split-chart-v1",
        "status": "RUNNING",
        "mode": "chart",
        "form_index": form_index,
        "edge_cap": edge_cap,
        "rounds": rounds,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_rounds):
        status = solver.check()
        if status != z3.sat:
            result["status"] = (
                "UNSAT_IDENTITY_AWARE_ONE_MINIMUM_SPLIT_CHART_THEOREM"
                if status == z3.unsat else "UNKNOWN"
            )
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            break
        model = solver.model()
        totals = {
            o: {g: Fraction(str(model.eval(total[g, o], model_completion=True)))
                for g in GOODS}
            for o in OWNERS
        }
        minima = {
            o: {g: Fraction(str(model.eval(minimum[g, o], model_completion=True)))
                for g in GOODS}
            for o in OWNERS
        }
        certificate = close_profile(totals, minima, edge_cap)
        if certificate is None:
            result["status"] = "SAT_IDENTITY_AWARE_ONE_MINIMUM_SPLIT_OBSTRUCTION"
            result["countermodel_totals"] = serialize(model, total)
            result["countermodel_minima"] = serialize(model, minimum)
            result["countermodel_iteration"] = iteration
            result["countermodel_role_slacks"] = {
                role: str(min(totals[o][role] // minima[o][role] for o in OWNERS))
                for role in GOODS
            }
            break
        solver.add(z3.Not(certificate_cut(certificate, total, minimum)))
        rounds.append({
            "iteration": iteration,
            "branch": certificate["branch"],
            "split_role": certificate["split_role"],
            "allocation_count": len(certificate["allocations"]),
            "totals": serialize(model, total),
            "minima": serialize(model, minimum),
        })
        print(iteration, certificate["branch"], certificate["split_role"],
              flush=True)
        output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        result["status"] = "ITERATION_LIMIT"

    result["branch_tally"] = {
        branch: sum(1 for r in rounds if r["branch"] == branch)
        for branch in ("W", "S")
    }
    result["claim_boundary"] = (
        "Every cut this run adds is realization-free: branch W sees only "
        "totals and minima, and branch S is guarded by slack exactly two on "
        "the split role, where Lemma B forces the two-good column and the "
        "eight side patterns exhaust the realizations.  UNSAT is therefore an "
        "identity-aware theorem for this move family on the declared chart.  "
        "SAT reports a profile no whole-role and no tame one-split family "
        "closes; because a wild role is never split, such a profile is open "
        "rather than refuted."
    )
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--form-index", type=int, choices=(0, 2))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--maximum-rounds", type=int, default=60)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    if (args.profile is None) == (args.form_index is None):
        parser.error("give exactly one of --profile and --form-index")
    if args.profile is not None:
        result = run_profile(args.profile, args.output, args.edge_cap)
        print(json.dumps({
            "status": result["status"],
            "superseded_status": result["superseded_status"],
            "certificate_branch": (
                result["certificate"]["branch"] if result["certificate"] else None
            ),
        }, indent=2))
        return
    result = run_chart(args.output, args.form_index, args.maximum_rounds,
                       args.timeout_seconds, args.random_seed, args.edge_cap)
    print(json.dumps({
        "status": result["status"],
        "rounds": len(result["rounds"]),
        "branch_tally": result["branch_tally"],
    }, indent=2))


if __name__ == "__main__":
    main()
