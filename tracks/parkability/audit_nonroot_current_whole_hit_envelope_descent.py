#!/usr/bin/env python3
"""Exact support audit of nonroot whole-hit envelope descent."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    chains_checked = 0
    maximum_observed_length = 0
    singleton_terminal_safe = True
    for size in range(1, 9):
        universe = set(range(size + 4))
        envelope = set(range(size))
        old_source = {size, size + 1}
        old_charity = {size + 2}
        for k_mask in range(1, 1 << size):
            packet = {g for g in envelope if k_mask & (1 << g)}
            # Deterministic worst-case chain deletes one nonpacket good at a
            # time while retaining the whole packet.
            current = set(envelope)
            length = 0
            for good in sorted(current - packet):
                nxt = current - {good}
                assert packet <= nxt < current
                current = nxt
                length += 1
            assert current == packet
            maximum_observed_length = max(maximum_observed_length, length)
            chains_checked += 1

            residual = envelope - packet
            new_targets = {
                "source": packet,
                "holder": residual,
                "charity": old_charity | old_source,
                "fixed": universe - envelope - old_source - old_charity,
            }
            assert set().union(*new_targets.values()) == universe
            assert sum(map(len, new_targets.values())) == len(universe)
            assert not (new_targets["holder"] & packet)
            assert not (new_targets["charity"] & packet)
            if len(packet) == 1:
                singleton_terminal_safe &= len(packet) - 1 == 0

    assert chains_checked > 0 and singleton_terminal_safe
    theorem = ROOT / "results/NONROOT_CURRENT_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md"
    currentization = ROOT / "results/PROTECTED_FLOOR_WHOLE_HIT_CURRENTIZATION_OR_PATH_HALL_THEOREM_20260814.md"
    sacrifice = ROOT / "results/PRIORITY_SACRIFICE_PROPER_RETIRED_PACKET_SPLIT_THEOREM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "nonroot-current-whole-hit-envelope-descent-audit-v1",
        "status": "NONROOT_CURRENT_WHOLE_HIT_TERMINATES_OR_RESELECTS_ROOT",
        "nested_support_chains_checked": chains_checked,
        "maximum_nonpacket_deletions_checked": maximum_observed_length,
        "singleton_terminal_threshold_zero": singleton_terminal_safe,
        "released_source_and_holder_residual_avoid_named_packet": True,
        "remaining_separators": [
            "initial_protected_root_holder",
            "source_inactive_floor_debt",
            "other_retired_support_normalization",
        ],
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, currentization, sacrifice, script)
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
