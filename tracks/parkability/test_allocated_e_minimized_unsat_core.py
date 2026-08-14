import hashlib
import json
from pathlib import Path

from .audit_allocated_e_all_allocation_unsat import structural_pi_signature


ROOT = Path(__file__).resolve().parents[2]


def test_minimized_core_and_independent_audit_are_hash_linked():
    core_path = ROOT / "results/allocated_e_form2_all_allocation_minimized_unsat_core.json"
    audit_path = ROOT / "results/allocated_e_form2_all_allocation_minimized_unsat_core_audit.json"
    core = json.loads(core_path.read_text())
    audit = json.loads(audit_path.read_text())
    signatures = [
        tuple((owner, tuple(goods)) for owner, goods in signature)
        for signature in core["pi_signatures"]
    ]
    assert core["status"] == "UNSAT_CORE_MINIMIZED"
    assert core["pi_clause_count"] == len(signatures) == 425
    assert core["allocation_clause_count"] == len(core["allocations"]) == 7
    assert core["response_atom_count"] == 277
    assert all(structural_pi_signature(signature) for signature in signatures)
    assert audit["status"] == "AUDIT_PASSED"
    assert audit["solver_status"] == "unsat"
    assert audit["source_sha256"] == hashlib.sha256(core_path.read_bytes()).hexdigest()
    assert audit["pi_clause_count"] == 425
    assert audit["allocation_clause_count"] == 7
