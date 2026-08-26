"""Pinned facts of the exact response-relation chart of the rank-three fixed-U master."""
import json
import subprocess
import sys
from pathlib import Path

import z3

from . import independently_verify_fixed_u_relation_chart as V
from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
from .decide_fixed_u_chart_cells_complete_efx import decide_complete_efx, audit
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[2]
CHART = ROOT / "results/fixed_u_exact_response_relation_chart_20260826.json"


def test_named_forms_feasibility():
    expected = ["sat", "unsat", "sat", "unsat"]
    for i, exp in enumerate(expected):
        s, _ = build_rank_three_master(exclude_self_responses=True, required_owner_cycle_form=True,
                                       exact_owner_cycle_response_relation=True, owner_cycle_form_index=i)
        s.set(timeout=120000)
        assert str(s.check()) == exp, i


def test_pinned_chart_size_and_universal_edges():
    chart = json.loads(CHART.read_text())
    assert chart["status"] == "COMPLETE" and chart["relation_count"] == 316
    keys = {r["key"] for r in chart["relations"]}
    assert len(keys) == 316
    for r in chart["relations"]:
        E = {tuple(e) for e in r["edges"]}
        assert ("d", "q") in E and ("d", "r") in E
        assert not any(t == "charity" for _, t in E)
        assert r["rank"] <= 3


def test_independent_verifier_accepts_every_witness():
    chart = json.loads(CHART.read_text())
    for r in chart["relations"]:
        v = {tuple(k.split(":")): Fraction(val) for k, val in r["witness"].items()}
        E = V.edges(v, V.SUPPORT, True)
        assert sorted(E) == sorted(tuple(e) for e in r["edges"])
        assert all(f for _, f in V.check_master(v)), r["key"]


def test_form_witnesses_close_within_four_edges():
    chart = json.loads(CHART.read_text())
    for r in chart["relations"]:
        if r["corrected_form_index"] in (0, 2):
            v = {tuple(k.split(":")): Fraction(val) for k, val in r["witness"].items()}
            st, alloc = decide_complete_efx(v, 4, 120)
            assert st == "sat"
            assert audit(alloc, v) <= 4


def test_census_reproduces_chart():
    out = ROOT / "results" / "_tmp_chart_replay.json"
    subprocess.run([sys.executable, "-m", "tracks.parkability.census_fixed_u_exact_response_relations",
                    "--timeout-seconds", "300", "--output", str(out)], cwd=ROOT, check=True, capture_output=True)
    replay = json.loads(out.read_text()); out.unlink()
    chart = json.loads(CHART.read_text())
    assert replay["status"] == "COMPLETE"
    assert {r["key"] for r in replay["relations"]} == {r["key"] for r in chart["relations"]}


PHYSICAL = ROOT / "results/fixed_u_physical_exact_response_relation_chart_20260826.json"


def test_physical_chart_pinned_facts():
    from . import independently_verify_fixed_u_physical_relation_chart as PV
    chart = json.loads(PHYSICAL.read_text())
    assert chart["status"] == "COMPLETE" and chart["relation_count"] == 679
    atom = {r["key"] for r in json.loads(CHART.read_text())["relations"]}
    phys = {r["key"] for r in chart["relations"]}
    assert atom <= phys and len(phys - atom) == 363
    assert all(("d", "r") in {tuple(e) for e in r["edges"]} for r in chart["relations"] if r["key"] in atom)
    assert all(("d", "r") not in {tuple(e) for e in r["edges"]} for r in chart["relations"] if r["key"] not in atom)
    for r in chart["relations"]:
        E = {tuple(e) for e in r["edges"]}
        assert ("d", "q") in E and not any(t == "charity" for _, t in E) and r["rank"] <= 3
        v = {tuple(k.split(":")): Fraction(x) for k, x in r["witness_totals"].items()}
        PV.MIN.clear(); PV.MIN.update({tuple(k.split(":")): Fraction(x) for k, x in r["witness_minima"].items()})
        assert sorted(PV.edges(v, PV.SUPPORT, True)) == sorted(E)
