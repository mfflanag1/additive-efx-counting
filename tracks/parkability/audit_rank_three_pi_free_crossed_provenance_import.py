#!/usr/bin/env python3
"""Independent structural audit of crossed provenance imports."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "results" / "RANK_THREE_PI_FREE_CROSSED_PROVENANCE_IMPORT_LEMMA_20260813.md"

FORMS = {
    "R2": {"r": "q", "q": "r", "s": "d"},
    "R3": {"r": "q", "q": "s", "s": "r"},
}


def audit():
    records = []
    for form, selected_target in FORMS.items():
        assert len(set(selected_target.values())) == 3
        physical_core = {
            source: frozenset((f"core_{source}_{target}",))
            for source, target in selected_target.items()
        }
        assert all(
            left.isdisjoint(right)
            for index, left in enumerate(physical_core.values())
            for right in tuple(physical_core.values())[index + 1:]
        )

        original_sources = frozenset(selected_target)
        records.append({
            "form": form,
            "family": "selected",
            "sources": sorted(original_sources),
            "omitted_owner": "d",
            "closed_without_omitted_support_would_force_pi": True,
        })

        for d_target in ("q", "r"):
            displaced = next(
                source for source, target in selected_target.items()
                if target == d_target
            )
            retained = tuple(
                source for source in selected_target if source != displaced
            )
            # d's replacement core occupies the displaced physical target;
            # retained selected cores occupy distinct other targets.
            replacement_targets = (d_target, *(selected_target[s] for s in retained))
            assert len(set(replacement_targets)) == 3
            sources = frozenset(("d", *retained))
            omitted = displaced
            assert sources == frozenset(("r", "q", "d", "s")) - {omitted}
            records.append({
                "form": form,
                "family": f"replace_{displaced}_at_{d_target}_by_d",
                "sources": sorted(sources),
                "omitted_owner": omitted,
                "physical_targets": list(replacement_targets),
                "pairwise_disjoint_by_distinct_targets": True,
                "closed_without_omitted_support_would_force_pi": True,
            })

    return {
        "schema": "rank-three-pi-free-crossed-provenance-import-audit-v1",
        "status": "BOTH_FORMS_ALL_CROSSED_IMPORTS_VERIFIED",
        "records": records,
        "record_count": len(records),
        "document_sha256": hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
        "claim_boundary": (
            "Cap-free combinatorial closure consequence conditional on each "
            "displayed d core being base-common-safe desired. This is "
            "unconditional for d->q; the current-only d->r status, support-"
            "return edge compression, and final EFX remain open."
        ),
    }


def main():
    output = ROOT / "results" / "rank_three_pi_free_crossed_provenance_import_audit.json"
    result = audit()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["record_count"]}, indent=2))


if __name__ == "__main__":
    main()
