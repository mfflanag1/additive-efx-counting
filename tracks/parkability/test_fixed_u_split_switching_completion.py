import json
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_split_switching_anchor_lemma import run as run_audit
from .decide_fixed_u_split_switching_templates import (
    TEMPLATES,
    accepted_masks,
    load_profile,
    run as run_decision,
)
from .scan_fixed_u_split_switching_anchor_ledger import run as run_census


PROFILE = Path("results/fixed_u_wild_forced_terminal_profile_20260820.json")
REPAIR = Path("results/fixed_u_terminal_profile_unrestricted_physical_decision_20260820.json")
LEDGER = Path("results/fixed_u_multi_split_chart_cuts_20260820.jsonl")


def canonical_role_values(role):
    raw = json.loads(REPAIR.read_text())["terminal"]["physical_values"]
    goods = sorted(good for good in raw["r"] if good.startswith(role + ":"))
    return {
        observer: [Fraction(raw[observer][good]) for good in goods]
        for observer in ("r", "q", "d", "s")
    }


def test_exact_template_decision_closes_every_lane(tmp_path):
    result = run_decision(PROFILE, tmp_path / "decision.json", 30)
    assert result["status"] == "UNSAT_NO_SPLIT_SWITCHING_SELECTOR_COUNTERMODEL"
    assert [(lane["template"], lane["cardinality"], lane["status"])
            for lane in result["lanes"]] == [
        *[("A_split_a1", cardinality, "unsat") for cardinality in range(2, 8)],
        *[("B_split_k", cardinality, "unsat") for cardinality in range(2, 4)],
    ]


def test_both_canonical_repairs_calibrate_the_template_formulas():
    _, totals, minima = load_profile(PROFILE)
    a_masks = accepted_masks(
        TEMPLATES["A_split_a1"], canonical_role_values("a1"), totals, minima
    )
    k_masks = accepted_masks(
        TEMPLATES["B_split_k"], canonical_role_values("k"), totals, minima
    )
    assert 1 in a_masks  # a1:0 to d, a1:1 to q
    assert 1 in k_masks  # k:0 to q, k:1 to r


def test_independent_anchor_audit_is_cap_free_and_strict(tmp_path):
    result = run_audit(PROFILE, tmp_path / "audit.json")
    assert result["status"] == "VERIFIED_BOTH_ANCHOR_SELECTORS_UNIVERSAL"
    assert result["lemmas"]["A_q_min_a1_anchor"]["minimum_certified_slack"] == "3/481"
    assert result["lemmas"]["B_r_min_k_anchor"]["minimum_certified_slack"] == "23/1924"
    assert [row["labelled_minimum_witness_pattern_count"]
            for row in result["coverage"]["a1"]] == [
        16, 1296, 38416, 810000, 14776336, 252047376
    ]
    assert [row["labelled_minimum_witness_pattern_count"]
            for row in result["coverage"]["k"]] == [16, 36]


def test_retained_profile_census_is_complete_and_exposes_nonimplication(tmp_path):
    result = run_census(LEDGER, PROFILE, tmp_path / "census.json")
    assert result["retained_profile_count"] == 205
    assert result["summary"] == {
        "A_q_min_a1_anchor": {
            "applicable_count": 160,
            "verified_count": 0,
            "failed_count": 160,
        },
        "B_r_min_k_anchor": {
            "applicable_count": 79,
            "verified_count": 2,
            "failed_count": 77,
        },
    }
    assert result["either_anchor_lemma_verified_count"] == 2
    assert all(
        result["terminal_profile_lemmas"][name]["verified"]
        for name in result["terminal_profile_lemmas"]
    )
