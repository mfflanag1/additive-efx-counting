#!/usr/bin/env python3
"""Independent exhaustive replay of the global-exterior root cut.

This implementation does not import the primary audit and uses only integer
subset arithmetic with superincreasing weights.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def submasks(mask: int):
    sub = mask
    while sub:
        yield sub
        sub = (sub - 1) & mask


def run() -> dict[str, object]:
    n = 6
    universe = (1 << n) - 1
    weights = tuple(1 << good for good in range(n))

    def value(mask: int) -> int:
        return sum(weights[good] for good in range(n) if mask & (1 << good))

    strict_cases = 0
    strict_bad_packet_hits = 0
    equality_cases = 0
    equality_identity_failures = 0
    equality_spread_failures = 0
    underpayment_cases = 0
    recurrent_states = 0
    base_containment_failures = 0

    for base in range(1, universe):
        # Frozen GG has three nonempty nonroot bundles and the charity good.
        if (universe ^ base).bit_count() < 4:
            continue
        x = value(base)
        for current in range(1, universe + 1):
            if value(current) <= x:
                continue
            delta = value(current) - x
            exterior = universe ^ current
            for packet in submasks(current):
                every_transfer_underpaid = True
                for transferred in submasks(packet):
                    root_target = universe ^ transferred
                    return_target = transferred
                    margin = value(root_target) - x
                    identity_margin = delta + value(exterior) - value(transferred)
                    assert margin == identity_margin
                    assert not (root_target & return_target)
                    assert (root_target | return_target) == universe

                    if margin > 0:
                        every_transfer_underpaid = False
                        strict_cases += 1
                        if transferred != packet:
                            strict_bad_packet_hits += int(
                                (root_target & packet) == packet
                                or (return_target & packet) == packet
                            )
                        elif packet.bit_count() >= 2:
                            # Every one-good deletion of the full return target
                            # is a proper packet response.
                            for good in range(n):
                                if packet & (1 << good):
                                    assert (packet ^ (1 << good)) != packet
                    elif margin == 0:
                        every_transfer_underpaid = False
                        equality_cases += 1
                        equality_identity_failures += int(root_target != base)
                        assert transferred == (universe ^ base)
                        assert transferred.bit_count() >= 4
                        good = (transferred & -transferred).bit_length() - 1
                        transferred_prime = transferred ^ (1 << good)
                        equality_spread_failures += int(
                            value(universe ^ transferred_prime) <= x
                            or not transferred_prime
                            or transferred_prime == packet
                        )
                    else:
                        underpayment_cases += 1

                if every_transfer_underpaid:
                    recurrent_states += 1
                    base_containment_failures += int(packet & ~base != 0)

    assert strict_cases > 0
    assert equality_cases > 0
    assert underpayment_cases > 0
    assert recurrent_states > 0
    assert strict_bad_packet_hits == 0
    assert equality_identity_failures == 0
    assert equality_spread_failures == 0
    assert base_containment_failures == 0

    theorem = ROOT / "results/ROOT_GLOBAL_EXTERIOR_SUBPACKET_SACRIFICE_THEOREM_20260814.md"
    containment = ROOT / "results/GLOBAL_EXTERIOR_DOMINANCE_BASE_CONTAINMENT_AND_CHARITY_RESET_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-global-exterior-subpacket-sacrifice-independent-audit-v1",
        "status": "INDEPENDENT_INTEGER_REPLAY_CONFIRMS_GLOBAL_ROOT_CUT_AND_BASE_CONTAINMENT",
        "method": "exhaustive_subset_arithmetic_superincreasing_integer_weights",
        "ground_set_size": n,
        "weights": list(weights),
        "strict_cases": strict_cases,
        "strict_bad_packet_hits": strict_bad_packet_hits,
        "equality_cases": equality_cases,
        "equality_identity_failures": equality_identity_failures,
        "equality_spread_failures": equality_spread_failures,
        "underpayment_cases": underpayment_cases,
        "fully_underpaid_recurrent_states": recurrent_states,
        "base_containment_failures": base_containment_failures,
        "imports_primary_audit": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, containment, script)
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
