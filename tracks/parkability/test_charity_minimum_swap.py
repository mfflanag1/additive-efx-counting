from pathlib import Path

try:
    from .audit_charity_minimum_swap import run
    from .scan_charity_threshold_absorption import scan_profile
except ImportError:
    from audit_charity_minimum_swap import run
    from scan_charity_threshold_absorption import scan_profile


def test_charity_minimum_swap_symbolic_audit(tmp_path: Path):
    result = run(tmp_path / "charity-minimum-swap.json")

    assert result["status"] == "ALL_SYMBOLIC_IMPLICATIONS_UNSAT"
    assert result["claim_count"] == 7
    assert {claim["verdict"] for claim in result["claims"]} == {"unsat"}


def test_charity_absorption_selector_on_identical_profile():
    result = scan_profile(((1,) * 8,) * 3, charity_size=2)

    assert result["status"] == "SELECTOR_ABSORBS"
    assert result["best_absorption_margin"] == "0"
