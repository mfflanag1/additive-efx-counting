from __future__ import annotations

import json
from pathlib import Path

try:
    from .audit_adjacent_large_binary_selected_root_counterexample import audit as audit_selected
    from .audit_adjacent_large_dual_payment_cells import audit as audit_payment_cells
    from .audit_adjacent_large_dual_payment_counterexample import audit as audit_payment_profile
    from .audit_adjacent_large_frozen_cores import audit as audit_cores
except ImportError:
    from audit_adjacent_large_binary_selected_root_counterexample import audit as audit_selected
    from audit_adjacent_large_dual_payment_cells import audit as audit_payment_cells
    from audit_adjacent_large_dual_payment_counterexample import audit as audit_payment_profile
    from audit_adjacent_large_frozen_cores import audit as audit_cores


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"


def test_selected_root_refutation_preserves_unrestricted_escape():
    result = audit_selected()
    assert result["status"] == "SELECTED_ROOT_REFUTED_BUT_UNRESTRICTED_ESCAPE_SURVIVES"
    assert result["selected_root_qf_lia_statuses"] == {"p": "unsat", "r": "sat"}
    assert not result["unsat_orders"]


def test_dual_payment_counterexample_preserves_unrestricted_escape():
    result = audit_payment_profile()
    assert result["status"] == "DUAL_PAYMENT_REFUTED_BUT_UNRESTRICTED_ESCAPE_SURVIVES"
    assert result["packet_flow"]["direct_p_payment_count"] == 0
    assert result["packet_flow"]["direct_r_payment_count"] == 0
    assert not result["unsat_orders"]


def test_dual_payment_finite_boundary():
    result = audit_payment_cells(180)
    statuses = {
        tuple(record["packet_sizes"]): record["status"] for record in result["records"]
    }
    assert statuses[(2, 2, 2, 2)] == "sat"
    assert all(
        status == "unsat"
        for sizes, status in statuses.items()
        if sizes != (2, 2, 2, 2)
    )


def test_frozen_atomic_and_split_core_headlines():
    atomic = json.loads((RESULTS / "adjacent_large_global_lex_atomic_cores.json").read_text())
    assert atomic["status"] == "ALL_24_ADJACENT_ATOMIC_ORDERS_UNSAT"
    assert atomic["single_rival_order_count"] == 22
    assert atomic["maximum_core_size"] == 3
    assert atomic["total_order_specific_rivals"] == 27
    cores = {
        tuple(json.loads(path.read_text())["packet_sizes"]): json.loads(path.read_text())[
            "deletion_minimal_core_size"
        ]
        for path in RESULTS.glob("adjacent_large_split_*_2103_core.json")
    }
    assert cores == {
        (2, 1, 1, 1): 1,
        (1, 2, 1, 1): 7,
        (1, 1, 2, 1): 11,
        (1, 1, 1, 2): 1,
    }


def test_frozen_atomic_and_split_cores_replay_exactly():
    result = audit_cores(RESULTS)
    assert result["status"] == "ALL_ADJACENT_FROZEN_CORES_REPLAY_EXACTLY"
    assert len(result["atomic"]["records"]) == 24
    assert len(result["splits"]) == 4
