#!/usr/bin/env python3
"""Chart-level attempt at the tame-covering-menu theorem.

Theorem 1 of `results/IDENTITY_AWARE_SLACK_TWO_20260816.md` reduces the
universal question to a chart-level one: does every fixed-`U`-admissible
profile admit a *tame covering menu* — a family of complete allocations, none
splitting a role of slack at least three, covering the side patterns of the
tame roles?

This driver attacks that question directly.  The premise master
`build_physical_master(form_index)` is the formalisation of
"fixed-`U`-admissible"; a `sat` model is an admissible profile, and each round
supplies a certificate closing it and cuts every profile that certificate
closes.  Because

```text
Not(OR_c closes(c))  ==  AND_c Not(closes(c)),
```

the accumulated cuts are exactly the statement "no certificate of the menu
closes this profile", so a master `unsat` is the theorem: every admissible
profile is closed by some certificate of the accumulated menu.

The one change from `run_identity_aware_one_minimum_split_cegar.py` is
**seeding**.  That driver discovered its whole-role certificates one round at a
time and ran out of iterations.  Here the menu is preloaded with the distinct
whole-role allocations already banked by the census, so the master starts from
a far stronger position.  A seed certificate is sound for any complete
allocation inside the edge budget, whether or not it is EFX anywhere: the cut
only ever excludes profiles on which that allocation *is* EFX, and there it is
a witness.  Completeness and the edge budget are therefore verified for every
seed; being EFX somewhere is not required and is not assumed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import support_supplier
from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_identity_aware_one_minimum_split_cegar import (
    WHOLE,
    certificate_cut,
    close_profile,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def whole_role_certificate(role_owner, edge_cap):
    """Turn a role -> owner map into a branch-W certificate, verifying it."""
    assert sorted(role_owner) == sorted(GOODS), sorted(role_owner)
    supplier = support_supplier()
    edges = sorted({
        (supplier[role], owner)
        for role, owner in role_owner.items()
        if supplier[role] != owner
    })
    assert len(edges) <= edge_cap, (edges, role_owner)
    allocation = {
        owner: [[role, WHOLE] for role in GOODS if role_owner[role] == owner]
        for owner in OWNERS
    }
    placed = sorted(role for pieces in allocation.values() for role, _ in pieces)
    assert placed == sorted(GOODS), placed
    return {
        "branch": "W",
        "split_role": None,
        "allocations": {"whole": allocation},
        "realization_free": True,
    }


def load_seed_menu(path, edge_cap):
    raw = json.loads(path.read_text())
    seeds = []
    seen = set()
    for entry in raw:
        key = tuple(sorted(entry.items()))
        if key in seen:
            continue
        seen.add(key)
        seeds.append(whole_role_certificate(entry, edge_cap))
    return seeds


def run(output_path, form_index, seed_path, maximum_rounds, timeout_seconds,
        random_seed, edge_cap):
    solver, total, minimum = build_physical_master(form_index)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    seeds = load_seed_menu(seed_path, edge_cap) if seed_path else []
    for certificate in seeds:
        solver.add(z3.Not(certificate_cut(certificate, total, minimum)))

    rounds = []
    result = {
        "schema": "fixed-u-tame-menu-chart-theorem-v1",
        "status": "RUNNING",
        "form_index": form_index,
        "edge_cap": edge_cap,
        "seed_certificates": len(seeds),
        "seed_source": str(seed_path) if seed_path else None,
        "seed_source_sha256": (
            hashlib.sha256(seed_path.read_bytes()).hexdigest() if seed_path else None
        ),
        "rounds": rounds,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_rounds):
        status = solver.check()
        if status != z3.sat:
            result["status"] = (
                "UNSAT_EVERY_ADMISSIBLE_PROFILE_HAS_A_TAME_COVERING_MENU"
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
            result["status"] = "SAT_NO_TAME_COVERING_MENU_FOR_THIS_PROFILE"
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
            "totals": serialize(model, total),
            "minima": serialize(model, minimum),
        })
        print(iteration, certificate["branch"], certificate["split_role"],
              flush=True)
        if iteration % 10 == 0:
            output_path.write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n"
            )
    else:
        result["status"] = "ITERATION_LIMIT"

    result["branch_tally"] = {
        branch: sum(1 for r in rounds if r["branch"] == branch)
        for branch in ("W", "S")
    }
    result["menu_size"] = len(seeds) + len(rounds)
    result["claim_boundary"] = (
        "The accumulated cuts state exactly that no certificate of the menu "
        "closes the profile, so UNSAT is the chart-level theorem: every "
        "fixed-U-admissible profile of this form admits a tame covering menu, "
        "hence by Theorem 1 a complete EFX allocation within the edge budget "
        "in every physical realization.  It is a theorem about the declared "
        "exact-response chart and this move family, not about four-agent EFX.  "
        "SAT reports an admissible profile that no whole-role and no tame "
        "one-split family closes; since a wild role is never split, such a "
        "profile is open rather than refuted."
    )
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--seed-menu", type=Path, default=None)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--maximum-rounds", type=int, default=400)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(args.output, args.form_index, args.seed_menu,
                 args.maximum_rounds, args.timeout_seconds, args.random_seed,
                 args.edge_cap)
    print(json.dumps({
        "status": result["status"],
        "seed_certificates": result["seed_certificates"],
        "rounds": len(result["rounds"]),
        "menu_size": result["menu_size"],
        "branch_tally": result["branch_tally"],
    }, indent=2))


if __name__ == "__main__":
    main()
