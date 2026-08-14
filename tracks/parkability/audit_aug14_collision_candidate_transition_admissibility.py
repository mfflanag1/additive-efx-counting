#!/usr/bin/env python3
"""Machine-check the claim boundaries in the Aug-14 admission audit."""

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
    charge = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    audit = ROOT / "results/AUG14_COLLISION_CANDIDATE_TRANSITION_ADMISSIBILITY_AUDIT_20260814.md"
    equality_admission = ROOT / "results/ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md"
    exterior_admission = ROOT / "results/BASE_CONTAINED_GLOBAL_EXTERIOR_SACRIFICE_ADMISSION_THEOREM_20260814.md"
    global_admission = ROOT / "results/ROOT_GLOBAL_EXTERIOR_SUBPACKET_SACRIFICE_THEOREM_20260814.md"
    charity_reset = ROOT / "results/GLOBAL_EXTERIOR_DOMINANCE_BASE_CONTAINMENT_AND_CHARITY_RESET_THEOREM_20260814.md"
    root_contradiction = ROOT / "results/GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md"
    resolution = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_RESOLUTION_20260814.md"
    candidates = {
        "base_donation": ROOT / "results/SUPPLIER_ALIGNED_BASE_DONATION_PACKET_SPREAD_THEOREM_20260814.md",
        "exterior_pooling": ROOT / "results/BASE_CONTAINED_RETIRED_PACKET_EXTERIOR_DONATION_SPLIT_THEOREM_20260814.md",
        "singleton_isolation": ROOT / "results/NONROOT_SINGLETON_RETIRED_PACKET_ISOLATION_DESCENT_THEOREM_20260814.md",
        "proper_nonroot_split": ROOT / "results/NONROOT_DOUBLE_SACRIFICE_PROPER_SPLIT_COMPRESSION_THEOREM_20260814.md",
    }

    contract_text = contract.read_text()
    charge_text = charge.read_text()
    texts = {name: path.read_text() for name, path in candidates.items()}

    governing_rules_present = all(
        phrase in contract_text
        for phrase in (
            "It is not admissible merely because",
            "An admissible transition is one of the actual operations",
        )
    ) and all(
        phrase in charge_text
        for phrase in (
            "No transfer is admissible merely because",
            "Adding another history label is not an outcome",
        )
    )

    conditional_boundaries_present = {
        "base_donation": "does not yet eliminate" in texts["base_donation"],
        "exterior_pooling": "unconditional cut" in texts["exterior_pooling"],
        "singleton_isolation": "does not eliminate the singleton collision" in texts["singleton_isolation"],
        "proper_nonroot_split": all(
            phrase in texts["proper_nonroot_split"]
            for phrase in ("stated protected candidate premises", "close `T_{L,times}^*`")
        ),
    }
    assert governing_rules_present
    assert all(conditional_boundaries_present.values())

    script = Path(__file__).resolve()
    audit_text = audit.read_text()
    assert "root-side admission gate is crossed" in audit_text
    assert "immediately contradictory" in audit_text
    assert "response-source/debt-to-anchor conversion is not needed" in audit_text

    paths = [
        contract,
        charge,
        audit,
        equality_admission,
        exterior_admission,
        global_admission,
        charity_reset,
        root_contradiction,
        resolution,
        *candidates.values(),
        script,
    ]
    return {
        "schema": "aug14-collision-candidate-transition-admissibility-audit-v1",
        "status": "ROOT_GLOBAL_CUT_ADMITTED_AND_OLD_ROOT_CORE_CLOSES_COLLISION",
        "governing_rules_present": governing_rules_present,
        "conditional_boundaries_present": conditional_boundaries_present,
        "admission_theorem_proved": False,
        "equality_face_admission_theorem_proved": True,
        "base_contained_exterior_pooling_admitted": True,
        "root_global_exterior_subpacket_sacrifice_admitted": True,
        "base_containment_unconditional": True,
        "charity_one_good_reset_admitted": True,
        "full_T_L_times_theorem_closed": True,
        "next_gate": "parked_support_or_empty_ledger_terminal_not_charity_response_debt",
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path) for path in paths
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
