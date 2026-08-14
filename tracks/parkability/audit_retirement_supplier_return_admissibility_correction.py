#!/usr/bin/env python3
"""Statement-integrity audit for the historical supplier-return correction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    contract = ROOT / "results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md"
    composition = ROOT / "results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md"
    handoff = ROOT / "results/ROOT_SOURCED_ANCHOR_RETAINING_SACRIFICE_HANDOFF_LEMMA_20260813.md"
    root_safe = ROOT / "results/ROOT_SAFE_WHOLE_HIT_COMPLETE_POOL_REDUCTION_THEOREM_20260814.md"
    whole = ROOT / "results/RETIREMENT_SUPPLIER_ROOT_PACKET_RELEASE_OR_UNDERPAYMENT_THEOREM_20260814.md"
    subpacket = ROOT / "results/RETIREMENT_SUPPLIER_SUBPACKET_RELEASE_OR_ATOMWISE_POOL_DOMINANCE_THEOREM_20260814.md"
    correction = ROOT / "results/RETIREMENT_SUPPLIER_RETURN_ADMISSIBILITY_CORRECTION_20260814.md"
    admission = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    equality = ROOT / "results/ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md"
    script = Path(__file__).resolve()

    contract_text = contract.read_text()
    composition_text = composition.read_text()
    handoff_text = handoff.read_text()
    root_safe_text = root_safe.read_text()
    whole_text = whole.read_text()
    subpacket_text = subpacket.read_text()
    correction_text = correction.read_text()
    admission_text = admission.read_text()
    equality_text = equality.read_text()

    assert "It is not admissible merely because it respects a new ledger convention" in contract_text
    assert "A nonroot sacrifice handoff is tested only when its exact" in composition_text
    assert "current-safe response" in handoff_text
    assert "actual protected-source/collision handoff" in root_safe_text
    assert "original residual-preserving historical-return candidate is" in whole_text
    assert "makes the atomwise cut strict" in subpacket_text
    assert "Historical provenance remains evidence about where" in correction_text
    assert "Clean controlled-release allocation" in admission_text
    assert "equality face is separately eliminated" in admission_text
    assert "No equality instance of the packet-price cut survives" in equality_text

    files = (contract, composition, handoff, root_safe, whole, subpacket, correction, admission, equality, script)
    return {
        "schema": "retirement-supplier-return-admissibility-correction-audit-v1",
        "status": "HISTORICAL_REVERSAL_INVALID_STRICT_AND_EQUALITY_RELEASES_REPAIRED",
        "signed_provenance_identifies_historical_recipient": True,
        "signed_provenance_implies_current_return_right": False,
        "root_safe_core_handoff_remains_admitted": True,
        "strict_clean_controlled_release_admitted": True,
        "packet_price_arithmetic_strict_branch_unconditional": True,
        "strict_atomwise_pool_dominance_unconditional": True,
        "root_equality_closed_by_packet_spread": True,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path) for path in files
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
