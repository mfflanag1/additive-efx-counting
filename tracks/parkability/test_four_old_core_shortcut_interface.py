from pathlib import Path

from .audit_four_old_core_shortcut_interface import run


ROOT = Path(__file__).resolve().parents[2]


def test_stated_splice_normal_form_is_vacuous() -> None:
    result = run(ROOT)
    assert result["status"] == "STATED_SPLICE_NORMAL_FORM_VACUOUS"
    assert all(result["symbolic_checks"].values())
    assert all(result["manuscript_premises_detected"].values())


def test_both_local_witnesses_have_immediate_four_core_efx_shortcut() -> None:
    result = run(ROOT)
    for replay in result["frozen_local_witness_shortcuts"].values():
        assert replay["efx"]
        assert replay["pareto_improves_all_owners"]
        assert replay["base_common_safe"]
