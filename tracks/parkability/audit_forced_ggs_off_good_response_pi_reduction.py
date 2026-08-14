#!/usr/bin/env python3
"""Exact role census for off-good response PI routing in forced GGS."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    profiles = []
    survivors = []
    for ordinary_source in ("c", "q"):
        for response_source in ("c", "q", "s"):
            if response_source == "q":
                verdict = "PI_Q_R_TWO_CYCLE"
            elif ordinary_source == "q" and response_source == "s":
                verdict = "PI_R_Q_S_THREE_CYCLE"
            else:
                verdict = "SURVIVES_ONE_GENUINE_TEST"
                survivors.append((ordinary_source, response_source))
            profiles.append(
                {
                    "ordinary_source_to_singleton": ordinary_source,
                    "off_good_response_source": response_source,
                    "verdict": verdict,
                }
            )

    assert len(profiles) == 6
    assert survivors == [("c", "c"), ("c", "s"), ("q", "c")]

    theorem = ROOT / "results/FORCED_GGS_OFF_GOOD_RESPONSE_PI_REDUCTION_THEOREM_20260814.md"
    switch = ROOT / "results/TWO_SOURCE_SINGLETON_SOURCE_ELIMINATION_AND_GGS_SWITCH_THEOREM_20260814.md"
    flower = ROOT / "results/THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "Response source `q`" in theorem_text
    assert "only off-good response source that survives is `i=c`" in theorem_text
    assert "No on-good source is closed" in theorem_text

    return {
        "schema": "forced-ggs-off-good-response-pi-reduction-audit-v1",
        "status": "OFF_GOOD_Q_AND_Q_TO_S_SOURCE_PROFILES_PI_CLOSED",
        "off_good_role_profiles_checked": len(profiles),
        "profiles": profiles,
        "pi_closed_profiles": len(profiles) - len(survivors),
        "surviving_profiles": [list(profile) for profile in survivors],
        "on_good_profiles_closed": 0,
        "overlapping_f_edges_declared_pi": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, switch, flower, contract, script)
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
