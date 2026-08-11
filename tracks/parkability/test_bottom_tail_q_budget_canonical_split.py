import json
from pathlib import Path

from .audit_bottom_tail_q_budget_canonical_split import run


ROOT = Path(__file__).resolve().parents[2]


def test_bottom_tail_q_budget_split_replays():
    expected = json.loads(
        (ROOT / "results/bottom_tail_q_budget_canonical_split_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_bottom_tail_q_budget_split_is_exact():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert result["exact_admissibility"] == "q(K) <= mu_q + q(W)"
