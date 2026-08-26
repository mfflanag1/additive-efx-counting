"""Calibration tests for the (F4) decider (fast lanes only)."""
from fractions import Fraction
from pathlib import Path

from .decide_fixed_u_f4 import (decide, evaluate_template, load_profile, minima_table,
                                template_edges, template_splits)
from .independently_verify_fixed_u_f4 import verify_cover

ROOT = Path(__file__).resolve().parents[2]
WILD = ROOT / "results" / "fixed_u_wild_forced_terminal_profile_20260820.json"


def test_wild_forced_profile_needs_exactly_one_anchor_split():
    totals, minima = load_profile(WILD)
    table = minima_table(totals, minima, 4, 4, oracle_timeout=60, adversary_timeout=120)
    assert table["min_split_cap"] == 1
    assert table["by_split_cap"][0]["status"] == "RELAXED_OBSTRUCTION"
    assert table["min_edge_cap"] == 4
    templates = table["closing_templates_at_min_split"]
    assert templates and all(len(template_splits(t["template"])) == 1 for t in templates)
    # the split-switching completion theorem's template B is the closing certificate
    splits = {template_splits(t["template"])[0] for t in templates}
    assert splits <= {"k", "a1"}
    assert min(Fraction(t["slack_at_sample"]) for t in templates) in (Fraction(23, 1924), Fraction(3, 481))


def test_wild_forced_cover_is_confirmed_by_independent_encoding():
    totals, minima = load_profile(WILD)
    result = decide(totals, minima, 1, 4, oracle_timeout=60, adversary_timeout=120)
    assert result["status"] == "F4_HOLDS"
    assert verify_cover(totals, minima, [t["template"] for t in result["templates"]], timeout_ms=120000) == "unsat"


def test_edge_and_split_accounting():
    totals, minima = load_profile(WILD)
    result = decide(totals, minima, 1, 4, oracle_timeout=60, adversary_timeout=120)
    for t in result["templates"]:
        assert len(template_edges(t["template"])) <= 4
        assert len(template_splits(t["template"])) <= 1


def test_refuting_cell_needs_a_fifth_edge():
    """The parallel session's two-good cell: no four-edge EFX allocation at any split count; five edges close it whole-role."""
    from .decide_fixed_u_f4 import GOODS, OWNERS, Realization, oracle, role_class
    totals, minima = load_profile(ROOT / "results" / "fixed_u_tame_or_anchor_cegar_20260821.json")
    ones = {("gq", "r"), ("h", "r"), ("j", "d"), ("j", "q"), ("l", "r"), ("m", "s")}
    kappa, bits = {}, {}
    for g in GOODS:
        if role_class(totals, minima, g) == "single":
            kappa[g] = 1
            continue
        kappa[g] = 2
        b = {o: int((g, o) in ones) for o in OWNERS}
        bits[g] = {o: 1 - v for o, v in b.items()} if b["r"] else b
    cell = Realization(totals, minima, kappa, bits, {})
    assert oracle(cell, 4, 4, 300000)[0] == "unsat"
    status, template = oracle(cell, 0, 5, 60000)
    assert status == "sat" and template_splits(template) == [] and len(template_edges(template)) == 5
    assert evaluate_template(template, cell) >= 0
