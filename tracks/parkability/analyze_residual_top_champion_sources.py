#!/usr/bin/env python3
"""Census champion sources for the residual-augmented flower target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from .analyze_flexible_later_owner_escape_topologies import (
        AGENTS,
        DEFAULT_PROFILES,
        old_bundles,
    )
except ImportError:
    from analyze_flexible_later_owner_escape_topologies import (
        AGENTS,
        DEFAULT_PROFILES,
        old_bundles,
    )


POOL = (
    "ar_tr_0", "ar_tr_1", "tr_rest_0", "tr_rest_1",
    "ar_bq_0", "ar_bq_1",
)
RESIDUAL = {"tr_rest_0", "tr_rest_1"}
BOTTOM = {"ar_bq_0", "ar_bq_1"}
RETAINED = {"ar_tr_0", "ar_tr_1"}
TQ = {"aq_tq_0", "aq_tq_1"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def amount(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return amount(values, observer, goods) - min(values[observer][good] for good in goods)


def run(root, profiles=DEFAULT_PROFILES):
    old = old_bundles()
    records = []
    for filename in profiles:
        path = root / "results" / filename
        payload = json.loads(path.read_text())
        values = {
            agent: {good: Fraction(str(entry)) for good, entry in row.items()}
            for agent, row in payload["values"].items()
        }
        base = {agent: amount(values, agent, old[agent]) for agent in AGENTS}
        desired = []
        for size in range(1, len(POOL) + 1):
            for goods in itertools.combinations(POOL, size):
                if not all(tail(values, observer, goods) <= base[observer] for observer in AGENTS):
                    continue
                for source in AGENTS:
                    if amount(values, source, goods) > base[source]:
                        desired.append({
                            "source": source,
                            "goods": list(goods),
                            "retains_residual": bool(set(goods) & RESIDUAL),
                            "retains_all_residual": RESIDUAL <= set(goods),
                            "retains_all_bottom": BOTTOM <= set(goods),
                        })
        sources = sorted({entry["source"] for entry in desired})
        residual_sources = sorted({
            entry["source"] for entry in desired if entry["retains_residual"]
        })
        rotation_failures = {
            "q_bottom_for_charity": (
                values["q"]["f"] <= amount(values, "q", BOTTOM)
            ),
            "r_cross_bundle": (
                amount(values, "r", old["q"]) < base["r"]
            ),
            "q_cross_bundle": (
                amount(values, "q", old["r"]) <= base["q"]
            ),
            "q_retained_top_payment": (
                amount(values, "q", RETAINED) <= amount(values, "q", TQ)
            ),
        }
        records.append({
            "profile": filename,
            "profile_sha256": sha256(path),
            "desired_bundle_count": len(desired),
            "champion_sources": sources,
            "residual_retaining_sources": residual_sources,
            "source_excluding_c_exists": any(source != "c" for source in sources),
            "source_excluding_c_residual_exists": any(
                source != "c" for source in residual_sources
            ),
            "rotation_failures": rotation_failures,
            "survives_live_rotation_gate": all(rotation_failures.values()),
            "desired_bundles": desired,
        })
    script = Path(__file__).resolve()
    return {
        "schema": "residual-top-champion-source-census-v1",
        "status": "CLASSIFIED",
        "profile_count": len(records),
        "records": records,
        "claim_boundary": (
            "exact subset census on seven frozen two-atom flower profiles; it "
            "tests source-excluding residual championship but is not a cap-free lemma"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.root.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "profiles": [
            {
                "profile": record["profile"],
                "sources": record["champion_sources"],
                "residual_sources": record["residual_retaining_sources"],
                "source_excluding_c": record["source_excluding_c_exists"],
                "source_excluding_c_residual": record["source_excluding_c_residual_exists"],
                "survives_live_rotation_gate": record["survives_live_rotation_gate"],
            }
            for record in result["records"]
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
