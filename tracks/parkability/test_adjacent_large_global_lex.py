from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"


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


if __name__ == "__main__":
    test_safe_repartition_frozen_headlines()
    test_capfree_lemmas_cover_all_adjacent_orders()
    print("adjacent-large focused theorem tests passed")
