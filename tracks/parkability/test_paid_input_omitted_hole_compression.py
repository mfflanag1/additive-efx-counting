import json
from pathlib import Path

from .audit_paid_input_omitted_hole_compression import run


ROOT = Path(__file__).resolve().parents[2]


def test_paid_input_omitted_hole_compression_replays():
    expected = json.loads(
        (ROOT / "results/paid_input_omitted_hole_compression_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_paid_input_omitted_hole_compression_is_exhaustive():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["violations"] == []
    assert result["source_union_sizes"] == [3]
