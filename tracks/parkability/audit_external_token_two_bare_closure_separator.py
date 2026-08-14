#!/usr/bin/env python3
"""Audit the strict-response cycle and two-bare closure separator."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from .run_full_capture_rank_three_cegar import FULL_CAPTURE_BASE
from .run_fixed_u_full_packet_terminal_cegar import SUPPORT_STATE


OWNERS = ("r", "q", "d", "s")
DOC = Path(__file__).parents[2] / "results" / (
    "EXTERNAL_TOKEN_TWO_BARE_CLOSURE_SEPARATOR_LEMMA_20260813.md"
)


def signed_conservation_audit():
    recipients = (*OWNERS, "charity")
    goods = range(4)
    records = 0
    failures = 0
    for base_holders in itertools.product(recipients, repeat=len(goods)):
        for final_holders in itertools.product(OWNERS, repeat=len(goods)):
            records += 1
            incoming = {
                good for good in goods
                if final_holders[good] in OWNERS
                and final_holders[good] != base_holders[good]
            }
            outgoing_or_charity = {
                good for good in goods
                if base_holders[good] == "charity"
                or (base_holders[good] in OWNERS
                    and final_holders[good] != base_holders[good])
            }
            failures += incoming != outgoing_or_charity
    return records, failures


def base_owner_map(base):
    return {good: owner for owner, goods in base.items() for good in goods}


def holder_map(allocation):
    return {good: owner for owner, goods in allocation.items() for good in goods}


def owner_closure(base, allocation, seed):
    base_owner = base_owner_map(base)
    holder = holder_map(allocation)
    edges = {
        (base_owner[good], holder[good])
        for good in holder
        if base_owner[good] in OWNERS and holder[good] in OWNERS
        and base_owner[good] != holder[good]
    }
    closure = {seed}
    while True:
        enlarged = closure | {right for left, right in edges if left in closure}
        if enlarged == closure:
            return closure
        closure = enlarged


def audit():
    conservation_records, conservation_failures = signed_conservation_audit()

    strictness_records = 0
    selector_failures = 0
    for closure_size in range(2, len(OWNERS) + 1):
        closure = tuple(OWNERS[:closure_size])
        for bare_mask in range(1 << closure_size):
            bare = {
                owner for index, owner in enumerate(closure)
                if bare_mask & (1 << index)
            }
            if len(bare) > 1:
                continue
            strictness_records += 1
            recipient = next(iter(bare), closure[0])
            strict = {
                owner for owner in OWNERS
                if owner not in closure or owner not in bare or owner == recipient
            }
            selector_failures += strict != set(OWNERS)

    closure = owner_closure(FULL_CAPTURE_BASE, SUPPORT_STATE, "d")
    base_owner = base_owner_map(FULL_CAPTURE_BASE)
    external = {}
    for owner in closure:
        external[owner] = sorted(
            good for good in SUPPORT_STATE[owner]
            if base_owner[good] == "charity" or base_owner[good] not in closure
        )
    full_capture_checks = {
        "seed_d_closure_is_d_r_q": closure == {"d", "r", "q"},
        "r_is_bare": external["r"] == [],
        "q_retains_base_charity_j": external["q"] == ["j"],
        "d_retains_base_charity_gr": external["d"] == ["gr"],
        "exactly_one_bare_closure_owner": sum(not goods for goods in external.values()) == 1,
        "current_charity_p_is_owned_by_outside_s": (
            SUPPORT_STATE["charity"] == ("p",)
            and base_owner["p"] == "s" and "s" not in closure
        ),
    }
    checks = {
        "complete_signed_labels_balance_if_self_responses_exist": conservation_failures == 0,
        "external_token_makes_unique_bare_owner_strict": selector_failures == 0,
        **full_capture_checks,
    }
    return {
        "schema": "external-token-two-bare-closure-separator-audit-v1",
        "status": "WITHDRAWN_PI_INFERENCE" if all(checks.values()) else "AUDIT_FAILED",
        "checks": checks,
        "signed_allocation_pairs_checked": conservation_records,
        "strictness_patterns_checked": strictness_records,
        "full_capture_closure": sorted(closure),
        "full_capture_external_packets": external,
        "document_sha256": hashlib.sha256(DOC.read_bytes()).hexdigest(),
        "claim_boundary": (
            "signed conservation and provenance census only. The missing "
            "common-safety implication invalidates the proposed PI-free "
            "two-bare separator and full-capture exclusion."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))


if __name__ == "__main__":
    main()
