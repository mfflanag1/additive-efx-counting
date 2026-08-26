import json
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_four_edge_obstruction import (
    allocation_stats,
    exact_efx,
    load_rows,
    realization,
    widest_oracle,
)


ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "results/fixed_u_tame_or_anchor_cegar_20260821.json"
PRIMARY = ROOT / "results/fixed_u_four_edge_obstruction_20260826.json"
INDEPENDENT = ROOT / "results/fixed_u_four_edge_obstruction_independent_audit_20260826.json"


def rows():
    raw = json.loads(PROFILE.read_text())
    return load_rows(raw, "totals"), load_rows(raw, "minima")


def test_minimal_obstruction_pattern_is_three_bits_on_observer_s():
    primary = json.loads(PRIMARY.read_text())
    assert primary["status"] == "SAT_FOUR_EDGE_DECLARATION_OBSTRUCTION"
    assert primary["minimal_side_bits"] == 3
    on = sorted(k for k, v in primary["minimal_obstruction_pattern"].items() if v)
    assert on == ["gq:s", "j:s", "m:s"]


def test_verdict_matrix_four_edges_unsat_five_edges_sat():
    primary = json.loads(PRIMARY.read_text())
    for row in primary["verdict_matrix"]:
        if row["edge_cap"] in (3, 4):
            assert row["status"] == "unsat"
        else:
            assert row["status"] == "sat"
    zero = next(r for r in primary["verdict_matrix"] if r["edge_cap"] == 5 and r["split_cap"] == 0)
    assert zero["split_roles"] == [] and len(zero["edges"]) == 5
    assert primary["four_split_four_edge_pattern_cegar"]["result"] == "obstruction"
    assert primary["five_edge_zero_split_pattern_cegar"]["result"] == "closed"


def test_pinned_certificate_is_exact_efx_and_four_edge_oracle_refuses():
    totals, minima = rows()
    primary = json.loads(PRIMARY.read_text())
    bits = {tuple(k.split(":")): v for k, v in primary["minimal_obstruction_pattern"].items()}
    values, role_goods = realization(totals, minima, bits)
    for observer, row in primary["physical_values"].items():
        for good, value in row.items():
            assert Fraction(value) == values[observer, good]
    zero = next(r for r in primary["verdict_matrix"] if r["edge_cap"] == 5 and r["split_cap"] == 0)
    assert exact_efx(values, role_goods, zero["allocation"])
    edges, splits = allocation_stats(role_goods, zero["allocation"])
    assert len(edges) == 5 and splits == []
    status, _ = widest_oracle(values, role_goods, None, 4, timeout_seconds=120)
    assert status == "unsat"


def test_independent_cpsat_audit_agrees():
    independent = json.loads(INDEPENDENT.read_text())
    assert independent["status"].startswith("AUDIT_PASS_FOUR_EDGE_DECLARATION_REFUTED")
    verdicts = {(r["edge_cap"], r["split_cap"]): r["status"] for r in independent["cpsat_verdict_matrix"]}
    assert verdicts[(4, None)] == "unsat" and verdicts[(3, None)] == "unsat"
    assert verdicts[(5, 0)] == "sat"
    assert independent["primary_five_edge_certificate_recheck"]["split_roles"] == []
