import json
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_a1_three_good_universal_allocation import audit


def test_independent_aggregate_audit(tmp_path):
    output = tmp_path / "audit.json"
    result = audit(
        Path("results/fixed_u_wild_forced_terminal_profile_20260820.json"),
        Path("results/fixed_u_terminal_profile_unrestricted_physical_decision_20260820.json"),
        Path("results/fixed_u_a1_three_good_cuts_20260820.jsonl"),
        output,
    )
    assert result["status"] == (
        "VERIFIED_ALL_FEASIBLE_A1_CARDINALITIES_UNIVERSAL_EFX_ALLOCATION"
    )
    assert result["target_owner"] == "r"
    assert result["labelled_witness_pattern_count"] == 1296
    assert result["feasible_target_cardinalities"] == [2, 3, 4, 5, 6, 7]
    assert result["maximum_feasible_target_cardinality"] == 7
    assert Fraction(result["minimum_worst_efx_slack"]) == Fraction(23, 1924)
    assert json.loads(output.read_text()) == result
