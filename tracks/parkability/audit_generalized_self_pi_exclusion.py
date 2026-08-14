#!/usr/bin/env python3
"""Independent exact audit of the generalized self-PI residual-cell exclusion."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "results" / "GENERALIZED_SELF_PI_EXCLUSION_LEMMA_20260813.md"
OWNERS = ("r", "q", "d", "s")
GOODS = ("a0", "a1", "h", "j", "k", "q0", "l", "e", "m", "gq", "gr", "p")
E = frozenset(("e", "l"))

BASES = {
    "full_capture": {
        "s": frozenset(("e", "p")),
        "charity": frozenset(("j", "l", "gr")),
    },
    "two_bare": {
        "s": frozenset(("e", "p")),
        "charity": frozenset(("l", "gr")),
    },
}


def total(value, observer, goods):
    return z3.Sum(*(value[observer, good] for good in goods))


def tail(value, observer, goods):
    entries = [value[observer, good] for good in goods]
    if len(entries) <= 1:
        return z3.RealVal(0)
    return z3.Sum(*entries) - z3.If(entries[0] <= entries[1], entries[0], entries[1])


def audit():
    records = []
    for cell, base in BASES.items():
        own = base["s"]
        unallocated = base["charity"]
        incoming = E - own
        released = own - E
        assert incoming == frozenset(("l",))
        assert released == frozenset(("p",))
        assert incoming <= unallocated

        for form_index in (0, 2):
            value = {
                (observer, good): z3.Real(f"gspi_{cell}_{form_index}_{observer}_{good}")
                for observer in OWNERS for good in GOODS
            }
            solver = z3.SolverFor("QF_LRA")
            solver.add(*(entry > 0 for entry in value.values()))
            solver.add(total(value, "s", own) == 1)

            # Required common-safe desired response to E.
            required_response = z3.And(
                total(value, "s", E) > 1,
                *(tail(value, observer, E) <= 1 for observer in OWNERS),
            )
            # For this exact decomposition this is the generalized self edge.
            generalized_self_edge = z3.And(
                total(value, "s", (own - released) | incoming) > 1,
                *(tail(value, observer, (own - released) | incoming) <= 1
                  for observer in OWNERS),
            )
            solver.add(required_response, z3.Not(generalized_self_edge))
            checked = solver.check()
            if checked != z3.unsat:
                raise AssertionError((cell, form_index, checked))
            records.append({
                "cell": cell,
                "form_index": form_index,
                "source": "s",
                "target": "s",
                "desired_core": sorted(E),
                "incoming_unallocated": sorted(incoming),
                "released": sorted(released),
                "solver_status": str(checked),
            })

    return {
        "schema": "generalized-self-pi-exclusion-audit-v1",
        "status": "BOTH_RESIDUAL_CELLS_EXCLUDED_IN_BOTH_FORMS",
        "document_sha256": hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
        "records": records,
        "claim_boundary": (
            "Cap-free generalized self-PI lemma plus exact exclusion of the two "
            "declared residual atomizations. Nonself generalized PI dependencies "
            "and the universal four-edge conclusion remain open."
        ),
    }


def main():
    output = ROOT / "results" / "generalized_self_pi_exclusion_audit.json"
    result = audit()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": len(result["records"])}, indent=2))


if __name__ == "__main__":
    main()
