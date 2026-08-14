import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_allocated_e_form0_pi_exclusion_manifest_is_bound_to_sources():
    audit = json.loads((
        ROOT / "results" / "allocated_e_form0_pi_exclusion_audit.json"
    ).read_text())
    assert audit["status"] == "ALLOCATED_E_FORM0_EXCLUDED_BY_GENERALIZED_PI"
    assert audit["solver_status"] == "unsat"
    assert audit["replayed_cut_count"] == 14249
    source = ROOT / "results" / "allocated_e_capture_form0_pairlinear_bulk_cegar.json"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == audit["source_sha256"]
    for row in audit["chain"]:
        path = ROOT / row["source"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
