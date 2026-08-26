#!/usr/bin/env python3
"""Assemble the deduplicated totals/minima profile corpus for the F4 decision."""
from __future__ import annotations
import argparse, hashlib, json
from fractions import Fraction
from pathlib import Path

OWNERS = ("r", "q", "d", "s")

def canon(totals, minima):
    return json.dumps({"totals": {o: {g: str(Fraction(v)) for g, v in sorted(totals[o].items())} for o in OWNERS},
                       "minima": {o: {g: str(Fraction(v)) for g, v in sorted(minima[o].items())} for o in OWNERS}},
                      sort_keys=True)

def add(corpus, totals, minima, source, tag):
    key = canon(totals, minima)
    digest = hashlib.sha256(key.encode()).hexdigest()
    if digest in corpus:
        corpus[digest]["sources"].append(source)
        return
    corpus[digest] = {"id": digest[:12], "sha256": digest, "sources": [source], "tag": tag,
                      **json.loads(key)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--extra-jsonl", type=Path, nargs="*", default=[])
    args = ap.parse_args()
    corpus = {}
    for i, line in enumerate(open("results/fixed_u_multi_split_chart_cuts_20260820.jsonl")):
        d = json.loads(line)["round"]; add(corpus, d["totals"], d["minima"], f"multi_split_chart_cuts_20260820:{i}", "retained-205")
    for i, line in enumerate(open("results/fixed_u_tame_or_anchor_cuts_20260821.jsonl")):
        d = json.loads(line); add(corpus, d["profile_totals"], d["profile_minima"], f"tame_or_anchor_cuts_20260821:{i}", "fresh-81")
    for i, line in enumerate(open("results/fixed_u_dynamic_anchor_cuts_20260821.jsonl")):
        d = json.loads(line)
        t = d.get("profile_totals") or d.get("round", {}).get("totals"); m = d.get("profile_minima") or d.get("round", {}).get("minima")
        if t and m: add(corpus, t, m, f"dynamic_anchor_cuts_20260821:{i}", "anchor-7")
    for name, tag in (("results/fixed_u_tame_or_anchor_cegar_20260821.json", "terminal-four-split"),
                      ("results/fixed_u_wild_forced_terminal_profile_20260820.json", "terminal-wild-forced")):
        d = json.loads(Path(name).read_text())
        for tk, mk in (("terminal_profile_totals", "terminal_profile_minima"), ("profile_totals", "profile_minima"), ("totals", "minima")):
            if tk in d and mk in d:
                add(corpus, d[tk], d[mk], name, tag); break
    for extra in args.extra_jsonl:
        for i, line in enumerate(open(extra)):
            d = json.loads(line)
            t = d.get("profile_totals") or d.get("totals") or d.get("round", {}).get("totals")
            m = d.get("profile_minima") or d.get("minima") or d.get("round", {}).get("minima")
            if t and m: add(corpus, t, m, f"{extra.name}:{i}", "banked-113")
    out = {"schema": "fixed-u-f4-profile-corpus-v1", "count": len(corpus),
           "by_tag": {}, "profiles": sorted(corpus.values(), key=lambda p: p["id"])}
    for p in out["profiles"]:
        out["by_tag"][p["tag"]] = out["by_tag"].get(p["tag"], 0) + 1
    args.output.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"count": out["count"], "by_tag": out["by_tag"]}))

if __name__ == "__main__":
    main()
