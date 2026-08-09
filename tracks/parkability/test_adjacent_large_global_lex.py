from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

try:
    from .audit_adjacent_large_binary_selected_root_counterexample import audit as audit_selected
    from .audit_adjacent_large_dual_payment_cells import audit as audit_payment_cells
    from .audit_adjacent_large_dual_payment_counterexample import audit as audit_payment_profile
    from .audit_adjacent_large_frozen_cores import audit as audit_cores
    from .decide_adjacent_large_safe_repartition_gate import run as run_safe_repartition
except ImportError:
    from audit_adjacent_large_binary_selected_root_counterexample import audit as audit_selected
    from audit_adjacent_large_dual_payment_cells import audit as audit_payment_cells
    from audit_adjacent_large_dual_payment_counterexample import audit as audit_payment_profile
    from audit_adjacent_large_frozen_cores import audit as audit_cores
    from decide_adjacent_large_safe_repartition_gate import run as run_safe_repartition


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


def test_safe_repartition_atom_is_exact_unsat():
    result = run_safe_repartition((1, 1, 1, 1), 60)
    assert result["status"] == "unsat"


def test_safe_repartition_frozen_headlines():
    audit = json.loads(
        (RESULTS / "adjacent_large_safe_repartition_cells_audit.json").read_text()
    )
    assert audit["status"] == "ALL_FIXED_CELLS_UNSAT"
    assert {tuple(record["packet_sizes"]) for record in audit["records"]} == {
        (1, 1, 1, 1),
        (2, 1, 1, 1),
        (1, 2, 1, 1),
        (1, 1, 2, 1),
        (1, 1, 1, 2),
        (2, 2, 2, 2),
    }
    assert all(record["status"] == "unsat" for record in audit["records"])
    gate = ROOT / audit["provenance"]["gate_script"]
    audit_script = ROOT / audit["provenance"]["audit_script"]
    assert hashlib.sha256(gate.read_bytes()).hexdigest() == audit["provenance"][
        "gate_script_sha256"
    ]
    assert hashlib.sha256(audit_script.read_bytes()).hexdigest() == audit[
        "provenance"
    ]["audit_script_sha256"]
    core = json.loads(
        (RESULTS / "adjacent_large_safe_repartition_core_2222.json").read_text()
    )
    assert core["status"] == "UNSAT_SOLVER_CORE"
    assert core["core_size"] == 28
    assert {record["kind"] for record in core["core"]} == {
        "safe_rq_repartition"
    }
    extractor = ROOT / core["provenance"]["extractor_script"]
    assert hashlib.sha256(extractor.read_bytes()).hexdigest() == core["provenance"][
        "extractor_script_sha256"
    ]
    assert hashlib.sha256(gate.read_bytes()).hexdigest() == core["provenance"][
        "gate_script_sha256"
    ]


def test_capfree_lemmas_cover_all_adjacent_orders():
    agents = ("p", "r", "s", "q")
    orders = set(itertools.permutations(agents))
    singleton_first = {order for order in orders if order[0] in {"q", "s"}}
    r_first = {order for order in orders if order[0] == "r"}
    earlier_p_first = {
        ("p", "q", "r", "s"),
        ("p", "q", "s", "r"),
        ("p", "s", "q", "r"),
    }
    safe_repartition = {
        ("p", "r", "s", "q"),
        ("p", "r", "q", "s"),
        ("p", "s", "r", "q"),
    }
    families = (singleton_first, r_first, earlier_p_first, safe_repartition)
    assert [len(family) for family in families] == [12, 6, 3, 3]
    assert set().union(*families) == orders
    assert sum(len(family) for family in families) == len(orders)
