#!/usr/bin/env python3
"""Exact finite audit of full signed-transfer state reconstruction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = tuple(range(4))
CHARITY = 4
GOODS = tuple(range(4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundles(assignment):
    return tuple(
        frozenset(g for g, recipient in zip(GOODS, assignment) if recipient == owner)
        for owner in OWNERS
    )


def charity(assignment):
    return frozenset(
        g for g, recipient in zip(GOODS, assignment) if recipient == CHARITY
    )


def decoration(base, candidate):
    base_bundles = bundles(base)
    candidate_bundles = bundles(candidate)
    return tuple(
        (candidate_bundles[i] - base_bundles[i], base_bundles[i] - candidate_bundles[i])
        for i in OWNERS
    )


def reconstruct(base, signed):
    base_bundles = bundles(base)
    recovered = tuple(
        (base_bundles[i] - outgoing) | incoming
        for i, (incoming, outgoing) in enumerate(signed)
    )
    recovered_charity = frozenset(GOODS) - frozenset().union(*recovered)
    return recovered, recovered_charity


def run(root: Path) -> dict:
    assignments = tuple(itertools.product((*OWNERS, CHARITY), repeat=len(GOODS)))
    pair_count = 0
    for base in assignments:
        signatures = {}
        for candidate in assignments:
            signed = decoration(base, candidate)
            recovered_bundles, recovered_charity = reconstruct(base, signed)
            assert recovered_bundles == bundles(candidate)
            assert recovered_charity == charity(candidate)
            prior = signatures.setdefault(signed, candidate)
            assert prior == candidate
            pair_count += 1
        assert len(signatures) == len(assignments)

    script = Path(__file__).resolve()
    theorem = root / "results/FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md"
    return {
        "schema": "full-signed-transfer-state-reconstruction-audit-v1",
        "status": "ALL_EXHAUSTED",
        "owner_count": len(OWNERS),
        "good_count": len(GOODS),
        "allocation_count": len(assignments),
        "base_candidate_pair_count": pair_count,
        "owner_bundles_reconstructed": True,
        "charity_reconstructed_by_conservation": True,
        "signed_decoration_injective_for_fixed_base": True,
        "physical_state_consequence": (
            "equal full signed decoration fixes allocation, charity, target supports, "
            "and moved-good supplier graph"
        ),
        "remaining_gate": (
            "force and observer-safely pay the fixed-label alternating response cycle"
        ),
        "claim_boundary": (
            "physical-state reconstruction only; cycle payment, repeated-support GG, "
            "and EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
