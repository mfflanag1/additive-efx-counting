"""Calibration gates and pinned results for the universal split oracle (PXC-style controls)."""
import json
from pathlib import Path

import pytest

from . import fixed_u_universal_split as U
from . import independently_verify_fixed_u_universal_split_cell as I

ROOT = Path(__file__).resolve().parents[2]
TERMINAL = ROOT / "results/fixed_u_wild_forced_terminal_profile_20260820.json"
DYNAMIC = ROOT / "results/fixed_u_dynamic_anchor_cegar_20260821.json"
MIXED = ROOT / "results/fixed_u_tame_or_anchor_cegar_20260821.json"
PINNED = ROOT / "results/fixed_u_universal_split_mixed_profile_edge4_20260826.json"

# The realization cell of the pattern-mixed profile with no four-edge EFX allocation at any split count.
OBSTRUCTING_CELL = {
    "a0:d": 0, "a0:q": 0, "a0:r": 0, "a0:s": 0, "a1:d": 0, "a1:q": 0, "a1:r": 0, "a1:s": 0,
    "e:d": 0, "e:q": 0, "e:r": 0, "e:s": 0, "gq:d": 0, "gq:q": 0, "gq:r": 1, "gq:s": 0,
    "h:d": 0, "h:q": 0, "h:r": 1, "h:s": 0, "j:d": 1, "j:q": 1, "j:r": 0, "j:s": 0,
    "k:d": 0, "k:q": 0, "k:r": 0, "k:s": 0, "l:d": 0, "l:q": 0, "l:r": 1, "l:s": 0,
    "m:d": 0, "m:q": 0, "m:r": 0, "m:s": 1, "p:d": 0, "p:q": 0, "p:r": 0, "p:s": 0,
    "q0:d": 0, "q0:q": 0, "q0:r": 0, "q0:s": 0,
}


def cell_tuple():
    return {tuple(k.split(":")): v for k, v in OBSTRUCTING_CELL.items()}


def test_terminal_profile_closes_with_one_split():
    totals, minima = U.load_profile(TERMINAL)
    r = U.universal_decide(totals, minima, 1, 4, 60)
    assert r["status"] == "CLOSED" and r["max_split_used"] == 1


def test_dynamic_anchor_profile_needs_two_splits_universally():
    totals, minima = U.load_profile(DYNAMIC)
    assert U.universal_decide(totals, minima, 0, 4, 60)["status"] == "OBSTRUCTED"
    assert U.universal_decide(totals, minima, 1, 4, 60)["status"] == "OBSTRUCTED"
    assert U.universal_decide(totals, minima, 2, 4, 120)["status"] == "CLOSED"


def test_mixed_profile_pinned_cell_has_no_four_edge_allocation_at_any_split_count():
    totals, minima = U.load_profile(MIXED)
    cell = cell_tuple()
    for split_cap in (0, 3, 4, len(U.multi_roles(totals, minima))):
        assert U.decide_cell(totals, minima, cell, split_cap, 4, 120)[0] == "unsat"
    status, allocation, _ = U.decide_cell(totals, minima, cell, 0, 5, 120)
    assert status == "sat"
    edges, split = U.audit_allocation(totals, minima, cell, allocation, 0, 5)
    assert len(edges) == 5 and split == []


def test_mixed_profile_closes_universally_with_zero_splits_at_five_edges():
    totals, minima = U.load_profile(MIXED)
    r = U.universal_decide(totals, minima, 0, 5, 60)
    assert r["status"] == "CLOSED" and r["menu_size"] == 1


def test_independent_boolean_encoding_agrees_on_pinned_cell():
    raw = json.loads(MIXED.read_text())
    from fractions import Fraction
    totals = {o: {r: Fraction(v) for r, v in row.items()} for o, row in raw["terminal_profile_totals"].items()}
    minima = {o: {r: Fraction(v) for r, v in row.items()} for o, row in raw["terminal_profile_minima"].items()}
    goods, values = I.realization(totals, minima, OBSTRUCTING_CELL)
    assert len(goods) == 24
    assert I.decide(goods, values, len(goods), 4, 120)[0] == "unsat"
    st, alloc = I.decide(goods, values, 0, 5, 120)
    assert st == "sat"
    edges, split = I.audit(alloc, goods, values, 0, 5)
    assert len(edges) == 5 and split == 0


def test_broken_oracle_negative_control_has_teeth():
    totals, minima = U.load_profile(MIXED)
    cell = cell_tuple()
    U.NEGATIVE_CONTROL["mode"] = "drop-charity-edge"
    try:
        assert U.decide_cell(totals, minima, cell, 0, 4, 120)[0] == "sat"
    finally:
        U.NEGATIVE_CONTROL["mode"] = None
    assert U.decide_cell(totals, minima, cell, 0, 4, 120)[0] == "unsat"


def test_pinned_artifact_matches_cell():
    if not PINNED.exists():
        pytest.skip("artifact not yet pinned")
    raw = json.loads(PINNED.read_text())
    assert raw["status"] == "OBSTRUCTED" and raw["obstructing_cell"] == OBSTRUCTING_CELL
    assert raw["escalation"]["4"]["minimal_split"] is None
    assert raw["escalation"]["5"]["minimal_split"] == 0
