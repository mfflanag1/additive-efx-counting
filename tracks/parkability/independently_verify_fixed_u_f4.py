#!/usr/bin/env python3
"""Independent re-verification of (F4) decisions.

Shares only the public role/owner labels and the declared support state with
the primary decider.  Encodings differ: one-hot Boolean owner variables, an
explicit per-anchor selection, and a single monolithic covering query instead
of a CEGAR loop.

For a profile with a claimed closing template set {T_k}: decide the single
formula  EXISTS R . AND_k NOT EFX(T_k, R)  over the relaxed realization space
(cardinality class, side bits, per-anchor box coordinates).  UNSAT confirms the
covering claim exactly; SAT refutes it and prints the realization.
For a claimed relaxed obstruction R: decide, with the one-hot oracle, that no
anchor-split allocation within the caps is EFX at R.
"""
from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

OWNERS = ("r", "q", "d", "s")
GOODS = ("a0", "a1", "h", "j", "k", "q0", "l", "e", "m", "gq", "gr", "p")


def support():
    from .run_fixed_u_full_packet_terminal_cegar import SUPPORT_STATE
    return {role: src for src, roles in SUPPORT_STATE.items() for role in roles}


def rv(v):
    v = Fraction(v)
    return z3.RealVal(f"{v.numerator}/{v.denominator}")


def rows(raw, key):
    return {o: {g: Fraction(x) for g, x in raw[key][o].items()} for o in OWNERS}


def classes(totals, minima):
    out = {}
    for g in GOODS:
        if all(totals[o][g] == minima[o][g] for o in OWNERS):
            out[g] = 1
        elif all(3 * minima[o][g] <= totals[o][g] for o in OWNERS):
            out[g] = 3
        else:
            assert all(2 * minima[o][g] <= totals[o][g] for o in OWNERS)
            out[g] = 2
    return out


class RelaxedSpace:
    """Symbolic relaxed realization with an independent encoding (explicit
    cardinality-two/three Booleans, side bits as Booleans, box reals)."""

    def __init__(self, totals, minima, solver):
        self.totals, self.minima, self.s = totals, minima, solver
        self.cls = classes(totals, minima)
        self.three = {g: z3.Bool(f"iv_three_{g}") for g in GOODS if self.cls[g] == 3}
        self.side = {g: {o: z3.Bool(f"iv_side_{g}_{o}") for o in OWNERS} for g in GOODS if self.cls[g] >= 2}
        for g in self.side:
            solver.add(z3.Not(self.side[g]["r"]))
        self.x = {}
        for g in self.three:
            for a in OWNERS:
                for o in OWNERS:
                    if o != a:
                        v = z3.Real(f"iv_x_{g}_{a}_{o}")
                        self.x[g, a, o] = v
                        solver.add(v >= rv(minima[o][g]), v <= rv(totals[o][g] - 2 * minima[o][g]))

    def selected(self, g, a, o):
        T, M = self.totals[o][g], self.minima[o][g]
        if o == a:
            return rv(M)
        two = z3.If(self.side[g][o] == self.side[g][a], rv(M), rv(T - M))
        return z3.If(self.three[g], self.x[g, a, o], two) if g in self.three else two

    def complement_floor(self, g, a, o):
        comp = rv(self.totals[o][g]) - self.selected(g, a, o)
        return z3.If(self.three[g], rv(self.minima[o][g]), comp) if g in self.three else comp

    def efx(self, template):
        cons = []
        for o in OWNERS:
            val = {t: [] for t in OWNERS}
            flo = {t: [] for t in OWNERS}
            for g, spec in template.items():
                if "whole" in spec:
                    val[spec["whole"]].append(rv(self.totals[o][g]))
                    flo[spec["whole"]].append(rv(self.minima[o][g]))
                else:
                    a = spec["anchor"]
                    sel = self.selected(g, a, o)
                    val[spec["selected_to"]].append(sel)
                    flo[spec["selected_to"]].append(sel)
                    val[spec["complement_to"]].append(rv(self.totals[o][g]) - sel)
                    flo[spec["complement_to"]].append(self.complement_floor(g, a, o))
            util = {t: z3.Sum(*val[t]) if val[t] else z3.RealVal(0) for t in OWNERS}
            for t in OWNERS:
                if t != o:
                    cons += [util[o] >= util[t] - f for f in flo[t]]
        return z3.And(*cons)


def verify_cover(totals, minima, templates, timeout_ms=600000):
    s = z3.Solver()
    s.set(timeout=timeout_ms)
    space = RelaxedSpace(totals, minima, s)
    for t in templates:
        s.add(z3.Not(space.efx(t)))
    status = s.check()
    return str(status)


def concrete_pieces(realization, totals, minima, g, a, o):
    T, M = totals[o][g], minima[o][g]
    k = realization["kappa"][g]
    if o == a:
        x = M
    elif k == 2:
        x = M if realization["bits"][g][o] == realization["bits"][g][a] else T - M
    else:
        x = Fraction(realization["box"][g][a][o])
    return x, T - x, (T - x if k == 2 else M)


def verify_obstruction(totals, minima, realization, split_cap, edge_cap, timeout_ms=600000):
    """One-hot oracle: is there any anchor-split allocation within the caps that is EFX at R?"""
    sup = support()
    cls = classes(totals, minima)
    s = z3.Solver()
    s.set(timeout=timeout_ms)
    own = {}  # (g, piece, owner) -> Bool ; piece in {'sel','comp'}
    anc = {}  # (g, a) -> Bool
    for g in GOODS:
        for piece in ("sel", "comp"):
            for o in OWNERS:
                own[g, piece, o] = z3.Bool(f"iv_own_{g}_{piece}_{o}")
            s.add(z3.PbEq([(own[g, piece, o], 1) for o in OWNERS], 1))
        for a in OWNERS:
            anc[g, a] = z3.Bool(f"iv_anc_{g}_{a}")
        s.add(z3.PbEq([(anc[g, a], 1) for a in OWNERS], 1))
        if cls[g] == 1:
            for o in OWNERS:
                s.add(own[g, "sel", o] == own[g, "comp", o])
    split = {g: z3.Or(*[z3.And(own[g, "sel", o], z3.Not(own[g, "comp", o])) for o in OWNERS]) for g in GOODS if cls[g] >= 2}
    s.add(z3.PbLe([(f, 1) for f in split.values()], split_cap))
    # the anchor is immaterial for an unsplit role: pin it to break symmetry
    for g in GOODS:
        s.add(z3.Implies(z3.Not(split[g]) if g in split else z3.BoolVal(True), anc[g, OWNERS[0]]))
    edges = []
    for src in set(sup.values()):
        for t in OWNERS:
            if t == src:
                continue
            fl = [own[g, p, t] for g in GOODS if sup[g] == src for p in ("sel", "comp")]
            if fl:
                edges.append(z3.Or(*fl))
    s.add(z3.PbLe([(f, 1) for f in edges], edge_cap))
    for o in OWNERS:
        util = {}
        for t in OWNERS:
            terms = []
            for g in GOODS:
                if cls[g] == 1:
                    terms.append(z3.If(own[g, "sel", t], rv(totals[o][g]), z3.RealVal(0)))
                    continue
                for a in OWNERS:
                    x, comp, _ = concrete_pieces(realization, totals, minima, g, a, o)
                    terms.append(z3.If(z3.And(anc[g, a], own[g, "sel", t]), rv(x), z3.RealVal(0)))
                    terms.append(z3.If(z3.And(anc[g, a], own[g, "comp", t]), rv(comp), z3.RealVal(0)))
            util[t] = z3.Sum(*terms)
        for t in OWNERS:
            if t == o:
                continue
            for g in GOODS:
                both = z3.And(own[g, "sel", t], own[g, "comp", t])
                s.add(z3.Implies(both, util[o] >= util[t] - rv(minima[o][g])))
                if cls[g] == 1:
                    continue
                for a in OWNERS:
                    x, comp, cf = concrete_pieces(realization, totals, minima, g, a, o)
                    s.add(z3.Implies(z3.And(anc[g, a], own[g, "sel", t], z3.Not(own[g, "comp", t])),
                                     util[o] >= util[t] - rv(x)))
                    s.add(z3.Implies(z3.And(anc[g, a], own[g, "comp", t], z3.Not(own[g, "sel", t])),
                                     util[o] >= util[t] - rv(cf)))
    return str(s.check())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", type=Path, required=True)
    ap.add_argument("--decision", type=Path, required=True, help="output of decide_fixed_u_f4 (single decide or minima table)")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    raw = json.loads(args.profile.read_text())
    for tk, mk in (("terminal_profile_totals", "terminal_profile_minima"), ("profile_totals", "profile_minima"), ("totals", "minima")):
        if tk in raw:
            totals, minima = rows(raw, tk), rows(raw, mk)
            break
    dec = json.loads(args.decision.read_text())
    report = {"profile": str(args.profile), "checks": []}
    if "closing_templates_at_min_split" in dec:
        temps = [t["template"] for t in dec["closing_templates_at_min_split"]]
        st = verify_cover(totals, minima, temps)
        report["checks"].append({"kind": "cover", "split_cap": dec["min_split_cap"], "templates": len(temps), "status": st,
                                 "verdict": "confirmed" if st == "unsat" else "REFUTED" if st == "sat" else "unknown"})
        for c, r in dec["by_split_cap"].items():
            if r["status"] == "RELAXED_OBSTRUCTION" and "realization" in r:
                st = verify_obstruction(totals, minima, r["realization"], int(c), 4)
                report["checks"].append({"kind": "obstruction", "split_cap": int(c), "status": st,
                                         "verdict": "confirmed" if st == "unsat" else "REFUTED" if st == "sat" else "unknown"})
    elif "templates" in dec:
        temps = [t["template"] for t in dec["templates"]]
        if dec["status"] == "F4_HOLDS":
            st = verify_cover(totals, minima, temps)
            report["checks"].append({"kind": "cover", "templates": len(temps), "status": st,
                                     "verdict": "confirmed" if st == "unsat" else "REFUTED" if st == "sat" else "unknown"})
        elif dec["status"] == "RELAXED_OBSTRUCTION":
            st = verify_obstruction(totals, minima, dec["realization"], dec.get("split_cap", 4), dec.get("edge_cap", 4))
            report["checks"].append({"kind": "obstruction", "status": st,
                                     "verdict": "confirmed" if st == "unsat" else "REFUTED" if st == "sat" else "unknown"})
    report["verdict"] = "pass" if all(c["verdict"] == "confirmed" for c in report["checks"]) else "FAIL"
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
