#!/usr/bin/env python3
"""Role audit for singleton-source elimination and the forced GGS cycle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    source_pairs = (("c", "q"), ("c", "s"))
    orientations = []
    singleton_source_contradictions = 0
    forced_ggs_orientations = 0
    profiles = []

    for sources in source_pairs:
        nonsource = next(v for v in ("c", "q", "s") if v not in sources)
        for a in sources:
            b = next(v for v in sources if v != a)
            forced = ((b, a), (nonsource, b))
            orientations.append((sources, a, b, nonsource, forced))
            if "s" in sources:
                # If a=s then b->a enters the singleton; if b=s then t->b
                # enters it. Either champion is nongenuine and creates an
                # ordinary incoming edge, contradicting sourcehood.
                incoming_singleton = (b, a) if a == "s" else (nonsource, b)
                assert incoming_singleton[1] == "s"
                singleton_source_contradictions += 1
                profiles.append(
                    {
                        "sources": list(sources),
                        "ordinary_source": a,
                        "verdict": "SINGLETON_SOURCE_CONTRADICTION",
                        "incoming_singleton_champion": list(incoming_singleton),
                    }
                )
            else:
                assert sources == ("c", "q") and nonsource == "s"
                cycle = (f"{b}-G->{a}", f"{a}-S->s", f"s-G->{b}")
                forced_ggs_orientations += 1
                profiles.append(
                    {
                        "sources": list(sources),
                        "ordinary_source": a,
                        "verdict": "FORCED_GGS",
                        "cycle": list(cycle),
                    }
                )

    assert len(orientations) == 4
    assert singleton_source_contradictions == 2
    assert forced_ggs_orientations == 2

    theorem = ROOT / "results/TWO_SOURCE_SINGLETON_SOURCE_ELIMINATION_AND_GGS_SWITCH_THEOREM_20260814.md"
    debt = ROOT / "results/TWO_SOURCE_ROOT_THRESHOLD_DEBT_DERANGEMENT_THEOREM_20260814.md"
    census = ROOT / "results/THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "The singleton cannot be a source" in theorem_text
    assert "cyclic word is `GGS`" in theorem_text
    assert "Merely changing the selected" in theorem_text

    return {
        "schema": "two-source-singleton-source-elimination-ggs-switch-audit-v1",
        "status": "SINGLETON_SOURCE_PAIR_CLOSED_SOLE_SURVIVOR_FORCES_NONROOT_GGS",
        "source_pair_orientations_checked": len(orientations),
        "singleton_source_contradictions": singleton_source_contradictions,
        "forced_ggs_orientations": forced_ggs_orientations,
        "profiles": profiles,
        "surviving_source_pair": ["c", "q"],
        "forced_cycle_word": "GGS",
        "forced_cycle_is_release_compatible_pi": False,
        "ledger_preserving_cycle_switch_proved": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, debt, census, contract, script)
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
