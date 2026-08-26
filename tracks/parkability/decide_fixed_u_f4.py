#!/usr/bin/env python3
"""Exact decision of the four-split conjecture (F4) for one totals/minima profile.

(F4): every physical realization of the profile admits a complete EFX
allocation using at most ``edge_cap`` support-transfer edges and at most
``split_cap`` split roles, every split being an anchor split (one
minimum-witness good of the anchor observer to one recipient, the remainder
of the role to a single other recipient).

Realization abstraction (adversary-favourable, hence sound for a theorem):

* an unsplit role contributes exactly (T, M) to every EFX inequality;
* a role split with anchor observer ``a`` at cardinality two has, for every
  other observer ``i``, selected value ``M_i`` or ``T_i - M_i`` according to
  whether ``i``'s witness coincides with ``a``'s (side bits), and the
  complement is the other good;
* at cardinality at least three the selected value ranges over
  ``[M_i, T_i - 2 M_i]`` (independently per anchor observer) and the
  complement deletion floor is ``M_i``.

The relaxed adversary chooses, per non-singleton role, the cardinality class,
the side bits and the box coordinates; the oracle chooses the allocation for
that realization; a template found by the oracle is turned into a cut on the
adversary.  Adversary UNSAT proves (F4) for the profile over every
realization.  An adversary point with no template is a *relaxed* obstruction
candidate only; it must be realized physically and re-checked by the
unrestricted allocation oracle before being banked.
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

OWNERS = ("r", "q", "d", "s")
GOODS = ("a0", "a1", "h", "j", "k", "q0", "l", "e", "m", "gq", "gr", "p")
SUPPORT_STATE = {
    "r": ("a0", "a1", "h"),
    "q": ("j", "k", "q0"),
    "d": ("l", "e", "m", "gq", "gr", "p"),
    "s": (),
    "charity": (),
}


def _load_support_state():
    """Use the repository's declared support state when importable."""
    try:
        from .run_fixed_u_full_packet_terminal_cegar import SUPPORT_STATE as S
        return {k: tuple(v) for k, v in S.items()}
    except Exception:  # pragma: no cover - standalone fallback
        return SUPPORT_STATE


SUPPORT = _load_support_state()
SUPPLIER = {role: source for source, roles in SUPPORT.items() for role in roles}
assert set(SUPPLIER) == set(GOODS), sorted(set(GOODS) - set(SUPPLIER))
SOURCES = tuple(SUPPORT)
ZERO_FLOORS = False  # ablation: zero-value goods make every whole-role and complement deletion floor 0


def rv(value):
    value = Fraction(value)
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def load_profile(path_or_dict):
    if isinstance(path_or_dict, (str, Path)):
        raw = json.loads(Path(path_or_dict).read_text())
    else:
        raw = path_or_dict
    for tkey, mkey in (("terminal_profile_totals", "terminal_profile_minima"),
                       ("profile_totals", "profile_minima"),
                       ("totals", "minima")):
        if tkey in raw and mkey in raw:
            totals = {o: {g: Fraction(v) for g, v in row.items()} for o, row in raw[tkey].items()}
            minima = {o: {g: Fraction(v) for g, v in row.items()} for o, row in raw[mkey].items()}
            return totals, minima
    raise ValueError("no totals/minima in profile")


def role_slack(totals, minima, role):
    return min(totals[o][role] // minima[o][role] for o in OWNERS)


def role_class(totals, minima, role):
    """'single' (T=M for every observer), else the largest admissible cardinality class 2 or 3."""
    if all(totals[o][role] == minima[o][role] for o in OWNERS):
        return "single"
    assert all(2 * minima[o][role] <= totals[o][role] for o in OWNERS), role
    return 3 if all(3 * minima[o][role] <= totals[o][role] for o in OWNERS) else 2


# ---------------------------------------------------------------------------
# concrete realizations (relaxed model) and the allocation oracle
# ---------------------------------------------------------------------------

class Realization:
    """Relaxed realization: per non-singleton role a cardinality class, side
    bits (class 2) and per-anchor selected-value vectors (class 3)."""

    def __init__(self, totals, minima, kappa, bits, box):
        self.totals, self.minima = totals, minima
        self.kappa, self.bits, self.box = kappa, bits, box

    def piece_values(self, role, anchor, observer):
        """(selected value, selected floor, complement value, complement floor)."""
        T, M = self.totals[observer][role], self.minima[observer][role]
        if observer == anchor:
            x = M
        elif self.kappa[role] == 2:
            x = M if self.bits[role][observer] == self.bits[role][anchor] else T - M
        else:
            x = self.box[role][anchor][observer]
        comp = T - x
        comp_floor = comp if self.kappa[role] == 2 else M
        if ZERO_FLOORS:
            comp_floor = Fraction(0)
        return x, x, comp, comp_floor

    def to_json(self):
        return {
            "kappa": dict(self.kappa),
            "bits": {g: dict(b) for g, b in self.bits.items()},
            "box": {g: {a: {i: str(v) for i, v in row.items()} for a, row in d.items()}
                    for g, d in self.box.items()},
        }


def oracle(realization, split_cap, edge_cap, timeout_ms=60000):
    """Find an anchor-split allocation for one concrete realization."""
    totals, minima = realization.totals, realization.minima
    classes = {g: role_class(totals, minima, g) for g in GOODS}
    s = z3.Solver()
    s.set(timeout=timeout_ms)
    own_sel = {g: z3.Int(f"os_{g}") for g in GOODS}
    own_comp = {g: z3.Int(f"oc_{g}") for g in GOODS}
    anchor = {g: z3.Int(f"an_{g}") for g in GOODS}
    for g in GOODS:
        s.add(own_sel[g] >= 0, own_sel[g] < 4, own_comp[g] >= 0, own_comp[g] < 4,
              anchor[g] >= 0, anchor[g] < 4)
        if classes[g] == "single":
            s.add(own_comp[g] == own_sel[g])
    split = {g: own_sel[g] != own_comp[g] for g in GOODS if classes[g] != "single"}
    s.add(z3.PbLe([(f, 1) for f in split.values()], split_cap))
    edges = []
    for src in SOURCES:
        for t_idx, t in enumerate(OWNERS):
            if t == src:
                continue
            flags = [z3.Or(own_sel[g] == t_idx, own_comp[g] == t_idx) for g in GOODS if SUPPLIER[g] == src]
            if flags:
                edges.append(z3.Or(*flags))
    s.add(z3.PbLe([(f, 1) for f in edges], edge_cap))
    # completeness: every owner receives something is not required by EFX; keep free.
    for o_idx, o in enumerate(OWNERS):
        # utility of each bundle in observer o's eyes
        util = {}
        for t_idx, t in enumerate(OWNERS):
            terms = []
            for g in GOODS:
                if classes[g] == "single":
                    terms.append(z3.If(own_sel[g] == t_idx, rv(totals[o][g]), z3.RealVal(0)))
                    continue
                # selected/complement values depend on anchor choice
                sel_val = z3.RealVal(0)
                comp_val = z3.RealVal(0)
                for a_idx, a in reversed(list(enumerate(OWNERS))):
                    x, _, comp, _ = realization.piece_values(g, a, o)
                    sel_val = z3.If(anchor[g] == a_idx, rv(x), sel_val) if a_idx < 3 else rv(x)
                    comp_val = z3.If(anchor[g] == a_idx, rv(comp), comp_val) if a_idx < 3 else rv(comp)
                terms.append(z3.If(own_sel[g] == t_idx, sel_val, z3.RealVal(0)))
                terms.append(z3.If(own_comp[g] == t_idx, comp_val, z3.RealVal(0)))
            util[t_idx] = z3.Sum(*terms)
        for t_idx, t in enumerate(OWNERS):
            if t_idx == o_idx:
                continue
            for g in GOODS:
                if classes[g] == "single":
                    s.add(z3.Implies(own_sel[g] == t_idx, util[o_idx] >= util[t_idx] - rv(0 if ZERO_FLOORS else minima[o][g])))
                    continue
                # whole role at t: floor M; split pieces: their floors
                sel_floor = z3.RealVal(0)
                comp_floor = z3.RealVal(0)
                for a_idx, a in reversed(list(enumerate(OWNERS))):
                    _, sf, _, cf = realization.piece_values(g, a, o)
                    sel_floor = z3.If(anchor[g] == a_idx, rv(sf), sel_floor) if a_idx < 3 else rv(sf)
                    comp_floor = z3.If(anchor[g] == a_idx, rv(cf), comp_floor) if a_idx < 3 else rv(cf)
                both = z3.And(own_sel[g] == t_idx, own_comp[g] == t_idx)
                s.add(z3.Implies(both, util[o_idx] >= util[t_idx] - rv(0 if ZERO_FLOORS else minima[o][g])))
                s.add(z3.Implies(z3.And(own_sel[g] == t_idx, own_comp[g] != t_idx),
                                 util[o_idx] >= util[t_idx] - sel_floor))
                s.add(z3.Implies(z3.And(own_comp[g] == t_idx, own_sel[g] != t_idx),
                                 util[o_idx] >= util[t_idx] - comp_floor))
    status = s.check()
    if status != z3.sat:
        return str(status), None
    m = s.model()
    template = {}
    for g in GOODS:
        a = OWNERS[m.eval(anchor[g], model_completion=True).as_long()]
        os_ = OWNERS[m.eval(own_sel[g], model_completion=True).as_long()]
        oc_ = OWNERS[m.eval(own_comp[g], model_completion=True).as_long()]
        if classes[g] == "single" or os_ == oc_:
            template[g] = {"whole": os_}
        else:
            template[g] = {"anchor": a, "selected_to": os_, "complement_to": oc_}
    return "sat", template


def template_edges(template):
    edges = set()
    for g, spec in template.items():
        for key in ("whole", "selected_to", "complement_to"):
            if key in spec and spec[key] != SUPPLIER[g]:
                edges.add((SUPPLIER[g], spec[key]))
    return sorted(edges)


def template_splits(template):
    return sorted(g for g, spec in template.items() if "anchor" in spec)


def evaluate_template(template, realization):
    """Exact Fraction re-check of every deletion inequality; returns minimum slack."""
    totals, minima = realization.totals, realization.minima
    worst = None
    for o in OWNERS:
        bundle_value = {t: Fraction(0) for t in OWNERS}
        floors = {t: [] for t in OWNERS}
        for g, spec in template.items():
            if "whole" in spec:
                bundle_value[spec["whole"]] += totals[o][g]
                floors[spec["whole"]].append(Fraction(0) if ZERO_FLOORS else minima[o][g])
            else:
                x, xf, comp, cf = realization.piece_values(g, spec["anchor"], o)
                bundle_value[spec["selected_to"]] += x
                floors[spec["selected_to"]].append(xf)
                bundle_value[spec["complement_to"]] += comp
                floors[spec["complement_to"]].append(cf)
        for t in OWNERS:
            if t == o:
                continue
            for f in floors[t]:
                slack = bundle_value[o] - bundle_value[t] + f
                worst = slack if worst is None else min(worst, slack)
    return worst


# ---------------------------------------------------------------------------
# symbolic adversary
# ---------------------------------------------------------------------------

class Adversary:
    def __init__(self, totals, minima, timeout_ms=120000):
        self.totals, self.minima = totals, minima
        self.classes = {g: role_class(totals, minima, g) for g in GOODS}
        self.s = z3.Solver()
        self.s.set(timeout=timeout_ms)
        self.kappa3 = {}
        self.bits = {}
        self.box = {}
        for g in GOODS:
            if self.classes[g] == "single":
                continue
            self.bits[g] = {o: z3.Bool(f"b_{g}_{o}") for o in OWNERS}
            self.s.add(z3.Not(self.bits[g]["r"]))  # global flip symmetry
            if self.classes[g] == 3:
                self.kappa3[g] = z3.Bool(f"k3_{g}")
                self.box[g] = {}
                for a in OWNERS:
                    self.box[g][a] = {}
                    for o in OWNERS:
                        if o == a:
                            continue
                        x = z3.Real(f"x_{g}_{a}_{o}")
                        self.box[g][a][o] = x
                        self.s.add(x >= rv(minima[o][g]), x <= rv(totals[o][g] - 2 * minima[o][g]))
        self.cuts = 0

    def sym_piece(self, g, a, o):
        """Symbolic (sel value, sel floor, comp value, comp floor) for anchor a, observer o."""
        T, M = self.totals[o][g], self.minima[o][g]
        if o == a:
            x = rv(M)
        else:
            two = z3.If(self.bits[g][o] == self.bits[g][a], rv(M), rv(T - M))
            if g in self.kappa3:
                x = z3.If(self.kappa3[g], self.box[g][a][o], two)
            else:
                x = two
        comp = rv(T) - x
        comp_floor = z3.If(self.kappa3[g], rv(M), comp) if g in self.kappa3 else comp
        if ZERO_FLOORS:
            comp_floor = rv(0)
        return x, x, comp, comp_floor

    def efx_formula(self, template):
        cons = []
        for o in OWNERS:
            value = {t: [] for t in OWNERS}
            floors = {t: [] for t in OWNERS}
            for g, spec in template.items():
                if "whole" in spec:
                    value[spec["whole"]].append(rv(self.totals[o][g]))
                    floors[spec["whole"]].append(rv(0 if ZERO_FLOORS else self.minima[o][g]))
                else:
                    x, xf, comp, cf = self.sym_piece(g, spec["anchor"], o)
                    value[spec["selected_to"]].append(x)
                    floors[spec["selected_to"]].append(xf)
                    value[spec["complement_to"]].append(comp)
                    floors[spec["complement_to"]].append(cf)
            util = {t: z3.Sum(*value[t]) if value[t] else z3.RealVal(0) for t in OWNERS}
            for t in OWNERS:
                if t == o:
                    continue
                for f in floors[t]:
                    cons.append(util[o] >= util[t] - f)
        return z3.And(*cons)

    def add_cut(self, template):
        self.s.add(z3.Not(self.efx_formula(template)))
        self.cuts += 1

    def sample(self):
        status = self.s.check()
        if status != z3.sat:
            return str(status), None
        m = self.s.model()
        kappa = {}
        bits = {}
        box = {}
        for g in GOODS:
            if self.classes[g] == "single":
                kappa[g] = 1
                continue
            k3 = g in self.kappa3 and z3.is_true(m.eval(self.kappa3[g], model_completion=True))
            kappa[g] = 3 if k3 else 2
            bits[g] = {o: int(z3.is_true(m.eval(self.bits[g][o], model_completion=True))) for o in OWNERS}
            if k3:
                box[g] = {}
                for a in OWNERS:
                    box[g][a] = {}
                    for o in OWNERS:
                        if o == a:
                            continue
                        v = m.eval(self.box[g][a][o], model_completion=True)
                        box[g][a][o] = Fraction(v.numerator_as_long(), v.denominator_as_long())
        return "sat", Realization(self.totals, self.minima, kappa, bits, box)


def decide(totals, minima, split_cap, edge_cap, max_rounds=2000, oracle_timeout=60,
           adversary_timeout=300, log=None):
    adv = Adversary(totals, minima, adversary_timeout * 1000)
    templates = []
    t0 = time.time()
    for rnd in range(max_rounds):
        status, realization = adv.sample()
        if status == "unsat":
            return {"status": "F4_HOLDS", "rounds": rnd, "templates": templates,
                    "seconds": round(time.time() - t0, 1)}
        if status != "sat":
            return {"status": "ADVERSARY_UNKNOWN", "rounds": rnd, "templates": templates,
                    "seconds": round(time.time() - t0, 1)}
        ostatus, template = oracle(realization, split_cap, edge_cap, oracle_timeout * 1000)
        if ostatus == "unsat":
            return {"status": "RELAXED_OBSTRUCTION", "rounds": rnd, "templates": templates,
                    "realization": realization.to_json(), "seconds": round(time.time() - t0, 1)}
        if ostatus != "sat":
            return {"status": "ORACLE_UNKNOWN", "rounds": rnd, "templates": templates,
                    "realization": realization.to_json(), "seconds": round(time.time() - t0, 1)}
        slack = evaluate_template(template, realization)
        assert slack is not None and slack >= 0, (template, slack)
        templates.append({"template": template, "edges": template_edges(template),
                          "splits": template_splits(template), "slack_at_sample": str(slack)})
        adv.add_cut(template)
        if log:
            log(f"round {rnd}: splits={template_splits(template)} edges={len(template_edges(template))} cuts={adv.cuts}")
    return {"status": "ROUND_LIMIT", "rounds": max_rounds, "templates": templates,
            "seconds": round(time.time() - t0, 1)}


def minima_table(totals, minima, edge_cap=4, split_cap=4, edge_loop=True, **kw):
    """Minimum split cap (at edge_cap) and minimum edge cap (at split_cap) for which F4 holds."""
    out = {"by_split_cap": {}, "by_edge_cap": {}}
    min_split = None
    for c in range(0, split_cap + 1):
        r = decide(totals, minima, c, edge_cap, **kw)
        out["by_split_cap"][c] = {k: v for k, v in r.items() if k != "templates"}
        out["by_split_cap"][c]["template_count"] = len(r["templates"])
        if r["status"] == "F4_HOLDS":
            min_split = c
            out["closing_templates_at_min_split"] = r["templates"]
            break
    out["min_split_cap"] = min_split
    min_edge = None
    if not edge_loop:
        out["min_edge_cap"] = edge_cap if min_split is not None else None
        out["edge_loop_skipped"] = True
        return out
    for e in range(0, edge_cap + 1):
        r = decide(totals, minima, split_cap, e, **kw)
        out["by_edge_cap"][e] = {k: v for k, v in r.items() if k != "templates"}
        out["by_edge_cap"][e]["template_count"] = len(r["templates"])
        if r["status"] == "F4_HOLDS":
            min_edge = e
            break
    out["min_edge_cap"] = min_edge
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--split-cap", type=int, default=4)
    ap.add_argument("--edge-cap", type=int, default=4)
    ap.add_argument("--minima-table", action="store_true")
    ap.add_argument("--oracle-timeout", type=int, default=60)
    ap.add_argument("--adversary-timeout", type=int, default=300)
    args = ap.parse_args()
    totals, minima = load_profile(args.profile)
    if args.minima_table:
        result = minima_table(totals, minima, args.edge_cap, args.split_cap,
                              oracle_timeout=args.oracle_timeout,
                              adversary_timeout=args.adversary_timeout, log=print)
    else:
        result = decide(totals, minima, args.split_cap, args.edge_cap,
                        oracle_timeout=args.oracle_timeout,
                        adversary_timeout=args.adversary_timeout, log=print)
    result["profile"] = str(args.profile)
    result["profile_sha256"] = hashlib.sha256(args.profile.read_bytes()).hexdigest()
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({k: v for k, v in result.items() if k not in ("templates", "closing_templates_at_min_split")}, indent=2))


if __name__ == "__main__":
    main()
