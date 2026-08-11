import json
from pathlib import Path

from .audit_full_signed_transfer_state_reconstruction import run


ROOT = Path(__file__).resolve().parents[2]


def test_full_signed_transfer_state_reconstruction_replays():
    expected = json.loads(
        (ROOT / "results/full_signed_transfer_state_reconstruction_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_full_signed_transfer_state_is_injective():
    result = run(ROOT)
    assert result["status"] == "ALL_EXHAUSTED"
    assert result["base_candidate_pair_count"] == 390625
    assert result["owner_bundles_reconstructed"]
    assert result["charity_reconstructed_by_conservation"]
    assert result["signed_decoration_injective_for_fixed_base"]
