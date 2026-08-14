from pathlib import Path

from .audit_nonroot_double_sacrifice_proper_split_compression import run


ROOT = Path(__file__).resolve().parents[2]


def test_nonroot_double_sacrifice_proper_split_compression() -> None:
    result = run(ROOT)
    assert result["status"] == "NONROOT_MULTI_GOOD_PACKET_REDUCED_TO_SINGLETON"
    assert result["single_target_response_hits_only_proper_split"]
    assert result["protected_head_graphs_checked"] == 225
    assert result["root_covered_maximum_exists"]
    assert result["nonroot_terminal_packet_size"] == 1
    assert not result["full_T_L_times_theorem_closed"]

