#!/usr/bin/env python3
"""Profile-level adversarial CEGAR against the four-split conjecture (F4).

Master: the declared exact-response form-2 physical-minimum master (totals and
minima), seeded with the retained realization-free menu cuts of the earlier
campaigns.  Oracle: the exact per-profile (F4) decision of
``decide_fixed_u_f4`` (relaxed realization space, anchor-split templates,
split cap 4, edge cap 4).

Cuts installed after a closed profile:
* every closing template that is *realization-free* at the profile (EFX at
  all endpoint scenarios of its split roles) contributes the symbolic
  condition "this template is realization-free", a sound region cut;
* if no closing template is realization-free by itself (the profile is
  closed only by a realization-dependent union), the profile point is
  excluded with a small rational box.  Such rounds are recorded as
  ``union_closed``; they are search progress, not theorem content.

A profile at which the inner decision returns a relaxed obstruction is
recorded as ``relaxed_obstruction`` and the run stops; it must then be
realized and checked by the unrestricted allocation oracle before being
banked.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import time
from fractions import Fraction
from pathlib import Path

import z3

from .decide_fixed_u_f4 import (GOODS, OWNERS, SUPPLIER, Realization, decide, role_class, rv)
from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_multi_split_chart_theorem import (audit_cut_record, certificate_cut,
                                                    select_master_solver)
from .run_fixed_u_tame_or_anchor_cegar import (audit_fresh_record, concrete_profile,
                                               install_fresh_record)


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def scenarios_for_template(template, totals, minima):
    """All endpoint scenarios (concrete Realizations) of the template's split roles."""
    splits = [g for g, spec in template.items() if "anchor" in spec]
    per_role = []
    for g in splits:
        cls = role_class(totals, minima, g)
        opts = []
        for bits in itertools.product((0, 1), repeat=3):
            b = dict(zip([o for o in OWNERS if o != "r"], bits))
            b["r"] = 0
            opts.append((2, b, None))
        if cls == 3:
            a = template[g]["anchor"]
            others = [o for o in OWNERS if o != a]
            for corner in itertools.product((0, 1), repeat=3):
                box = {a: {o: (minima[o][g] if c == 0 else totals[o][g] - 2 * minima[o][g])
                           for o, c in zip(others, corner)}}
                opts.append((3, {o: 0 for o in OWNERS}, box))
        per_role.append(opts)
    for combo in itertools.product(*per_role):
        kappa = {g: 1 for g in GOODS}
        bits, box = {}, {}
        for g, (k, b, bx) in zip(splits, combo):
            kappa[g] = k
            bits[g] = b
            if bx is not None:
                box[g] = bx
        for g in GOODS:
            if g not in splits and role_class(totals, minima, g) != "single":
                kappa[g] = 2
                bits[g] = {o: 0 for o in OWNERS}
        yield Realization(totals, minima, kappa, bits, box)


def template_realization_free(template, totals, minima):
    from .decide_fixed_u_f4 import evaluate_template
    for real in scenarios_for_template(template, totals, minima):
        if evaluate_template(template, real) < 0:
            return False
    return True


def symbolic_realization_free_cut(template, total, minimum):
    """Symbolic condition: template is EFX at every endpoint scenario of its split roles."""
    splits = [g for g, spec in template.items() if "anchor" in spec]
    clauses = []
    # a split role must be non-singleton (2M <= T) in every row
    for g in splits:
        clauses += [2 * minimum[g, o] <= total[g, o] for o in OWNERS]

    def piece_values(g, a, o, scenario):
        T, M = total[g, o], minimum[g, o]
        k, bits, corner = scenario
        if o == a:
            x = M
        elif k == 2:
            x = M if bits[o] == bits[a] else T - M
        else:
            x = M if corner[o] == 0 else T - 2 * M
        comp = T - x
        floor = comp if k == 2 else M
        return x, x, comp, floor

    per_role = []
    for g in splits:
        a = template[g]["anchor"]
        opts = []
        for bits in itertools.product((0, 1), repeat=3):
            b = dict(zip([o for o in OWNERS if o != "r"], bits))
            b["r"] = 0
            opts.append((2, b, None))
        others = [o for o in OWNERS if o != a]
        for corner in itertools.product((0, 1), repeat=3):
            opts.append((3, None, dict(zip(others, corner))))
        per_role.append(opts)
    three_guard = {g: z3.And(*[3 * minimum[g, o] <= total[g, o] for o in OWNERS]) for g in splits}
    for combo in itertools.product(*per_role):
        guards = [three_guard[g] for g, sc in zip(splits, combo) if sc[0] == 3]
        cons = []
        for o in OWNERS:
            val = {t: [] for t in OWNERS}
            flo = {t: [] for t in OWNERS}
            for g, spec in template.items():
                if "whole" in spec:
                    val[spec["whole"]].append(total[g, o])
                    flo[spec["whole"]].append(minimum[g, o])
                else:
                    sc = combo[splits.index(g)]
                    x, xf, comp, cf = piece_values(g, spec["anchor"], o, sc)
                    val[spec["selected_to"]].append(x)
                    flo[spec["selected_to"]].append(xf)
                    val[spec["complement_to"]].append(comp)
                    flo[spec["complement_to"]].append(cf)
            util = {t: z3.Sum(*val[t]) if val[t] else z3.RealVal(0) for t in OWNERS}
            for t in OWNERS:
                if t != o:
                    cons += [util[o] >= util[t] - f for f in flo[t]]
        body = z3.And(*cons)
        clauses.append(z3.Implies(z3.And(*guards), body) if guards else body)
    return z3.And(*clauses)


def point_exclusion(totals, minima, total, minimum, radius=Fraction(1, 10**6)):
    return z3.Or(*[z3.Or(total[g, o] < rv(totals[o][g] - radius), total[g, o] > rv(totals[o][g] + radius),
                        minimum[g, o] < rv(minima[o][g] - radius), minimum[g, o] > rv(minima[o][g] + radius))
                   for g in GOODS for o in OWNERS])


def run(output, ledger, base_ledger, fresh_ledger, max_rounds, master_timeout, oracle_timeout,
        adversary_timeout, split_cap, edge_cap, seed, master_mode, time_budget):
    source, total, minimum = build_physical_master(2)
    solver = select_master_solver(source, master_mode, master_timeout, seed)
    seeded = 0
    if base_ledger and base_ledger.exists():
        for line in base_ledger.read_text().splitlines():
            if line.strip():
                cert = audit_cut_record(json.loads(line), edge_cap)
                solver.add(z3.Not(certificate_cut(cert, total, minimum)))
                seeded += 1
    if fresh_ledger and fresh_ledger.exists():
        for line in fresh_ledger.read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                rec.pop("payload_sha256", None)
                audit_fresh_record(rec, edge_cap)
                install_fresh_record(solver, rec, total, minimum)
                seeded += 1
    rounds = []
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            if line.strip():
                rounds.append(json.loads(line))
    for rec in rounds:  # re-install our own earlier cuts
        for t in rec.get("realization_free_templates", []):
            solver.add(z3.Not(symbolic_realization_free_cut(t, total, minimum)))
        if rec["kind"] == "union_closed":
            solver.add(point_exclusion(rec_profile(rec)[0], rec_profile(rec)[1], total, minimum))
    result = {"schema": "fixed-u-f4-profile-cegar-v1", "status": "RUNNING", "form_index": 2,
              "split_cap": split_cap, "edge_cap": edge_cap, "seeded_cuts": seeded,
              "master_mode": master_mode, "random_seed": seed, "rounds": len(rounds),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    atomic_write(output, result)
    t_start = time.time()
    for it in range(len(rounds), max_rounds):
        if time.time() - t_start > time_budget:
            result["status"] = "TIME_BUDGET"
            break
        status = solver.check()
        if status == z3.unsat:
            result["status"] = "UNSAT_F4_MASTER_CLOSED"
            break
        if status != z3.sat:
            result["status"] = "MASTER_UNKNOWN"
            result["reason"] = solver.reason_unknown()
            break
        model = solver.model()
        totals, minima = concrete_profile(model, total, minimum)
        dec = decide(totals, minima, split_cap, edge_cap, oracle_timeout=oracle_timeout,
                     adversary_timeout=adversary_timeout)
        rec = {"iteration": it, "profile_totals": {o: {g: str(v) for g, v in totals[o].items()} for o in OWNERS},
               "profile_minima": {o: {g: str(v) for g, v in minima[o].items()} for o in OWNERS},
               "decision": dec["status"], "decision_rounds": dec["rounds"], "seconds": dec["seconds"]}
        if dec["status"] == "F4_HOLDS":
            temps = [t["template"] for t in dec["templates"]]
            rf = [t for t in temps if template_realization_free(t, totals, minima)]
            rec["realization_free_templates"] = rf
            rec["template_count"] = len(temps)
            rec["max_splits_in_certificate"] = max((len([g for g in t if "anchor" in t[g]]) for t in temps), default=0)
            if rf:
                rec["kind"] = "realization_free_closed"
                for t in rf:
                    solver.add(z3.Not(symbolic_realization_free_cut(t, total, minimum)))
            else:
                rec["kind"] = "union_closed"
                rec["closing_templates"] = temps
                solver.add(point_exclusion(totals, minima, total, minimum))
        elif dec["status"] == "RELAXED_OBSTRUCTION":
            rec["kind"] = "relaxed_obstruction"
            rec["realization"] = dec["realization"]
            rec["templates_before"] = [t["template"] for t in dec["templates"]]
            rounds.append(rec)
            with open(ledger, "a") as f:
                f.write(json.dumps(rec, sort_keys=True) + "\n")
            result["status"] = "SAT_RELAXED_F4_OBSTRUCTION_CANDIDATE"
            result["rounds"] = len(rounds)
            break
        else:
            rec["kind"] = "undecided"
            rec["detail"] = dec["status"]
            solver.add(point_exclusion(totals, minima, total, minimum))
        rounds.append(rec)
        with open(ledger, "a") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
        result["rounds"] = len(rounds)
        result["kinds"] = {k: sum(1 for r in rounds if r["kind"] == k) for k in {r["kind"] for r in rounds}}
        atomic_write(output, result)
        print(f"round {it}: {rec['kind']} decision={dec['status']} templates={rec.get('template_count')} rf={len(rec.get('realization_free_templates', []))} max_splits={rec.get('max_splits_in_certificate')} s={dec['seconds']}", flush=True)
    else:
        result["status"] = "ROUND_LIMIT"
    result["rounds"] = len(rounds)
    result["kinds"] = {k: sum(1 for r in rounds if r["kind"] == k) for k in {r["kind"] for r in rounds}}
    atomic_write(output, result)
    return result


def rec_profile(rec):
    totals = {o: {g: Fraction(v) for g, v in rec["profile_totals"][o].items()} for o in OWNERS}
    minima = {o: {g: Fraction(v) for g, v in rec["profile_minima"][o].items()} for o in OWNERS}
    return totals, minima


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--ledger", type=Path, required=True)
    ap.add_argument("--base-ledger", type=Path, default=Path("results/fixed_u_multi_split_chart_cuts_20260820.jsonl"))
    ap.add_argument("--fresh-ledger", type=Path, default=Path("results/fixed_u_tame_or_anchor_cuts_20260821.jsonl"))
    ap.add_argument("--max-rounds", type=int, default=200)
    ap.add_argument("--master-timeout", type=int, default=300)
    ap.add_argument("--oracle-timeout", type=int, default=60)
    ap.add_argument("--adversary-timeout", type=int, default=300)
    ap.add_argument("--split-cap", type=int, default=4)
    ap.add_argument("--edge-cap", type=int, default=4)
    ap.add_argument("--seed", type=int, default=826)
    ap.add_argument("--master-mode", choices=("smt", "qflra"), default="smt")
    ap.add_argument("--time-budget", type=int, default=3600)
    args = ap.parse_args()
    r = run(args.output, args.ledger, args.base_ledger, args.fresh_ledger, args.max_rounds,
            args.master_timeout, args.oracle_timeout, args.adversary_timeout, args.split_cap,
            args.edge_cap, args.seed, args.master_mode, args.time_budget)
    print(json.dumps({k: r[k] for k in ("status", "rounds", "kinds") if k in r}, indent=2))


if __name__ == "__main__":
    main()
