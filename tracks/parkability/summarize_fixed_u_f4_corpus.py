#!/usr/bin/env python3
"""Summarize the per-profile (F4) minima table and the structure of split certificates."""
from __future__ import annotations
import argparse, collections, json
from pathlib import Path
from .decide_fixed_u_f4 import SUPPLIER, OWNERS, GOODS

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, required=True)
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    corpus = {p["sha256"]: p for p in json.loads(args.corpus.read_text())["profiles"]}
    rows = [json.loads(l) for l in open(args.results) if l.strip()]
    table = []
    for r in rows:
        ms = r["min_split_cap"]; me = r["min_edge_cap"]
        # monotonicity repair: closure at split cap c <= 4 with edge cap 4 implies min_edge <= 4
        if me is None and ms is not None and r["by_edge_cap"].get("4", {}).get("status") != "F4_HOLDS":
            statuses = {int(k): v["status"] for k, v in r["by_edge_cap"].items()}
            if all(statuses.get(e) == "RELAXED_OBSTRUCTION" for e in range(4)):
                me = 4; r["min_edge_repaired_by_monotonicity"] = True
        undecided = [int(c) for c, v in r["by_split_cap"].items() if v["status"] not in ("F4_HOLDS", "RELAXED_OBSTRUCTION")]
        table.append({"id": r["id"], "tag": r["tag"], "min_split": ms, "min_edge": me, "undecided_split_caps": undecided,
                      "seconds": r["seconds"], "error": r["error"]})
    by_tag = collections.defaultdict(collections.Counter)
    for t in table:
        by_tag[t["tag"]][(t["min_split"], t["min_edge"])] += 1
    # certificate structure for split >= 1
    struct = collections.Counter(); examples = []
    for r in rows:
        if not r.get("min_split_cap"):
            continue
        for t in r.get("closing_templates_at_min_split", []):
            tpl = t["template"]; splits = [g for g in tpl if "anchor" in tpl[g]]
            edges = set(tuple(e) for e in t["edges"])
            # which edges are carried by split pieces only
            split_edges = set()
            for g in splits:
                for key in ("selected_to", "complement_to"):
                    if tpl[g][key] != SUPPLIER[g]:
                        split_edges.add((SUPPLIER[g], tpl[g][key]))
            whole_edges = set()
            for g, spec in tpl.items():
                if "whole" in spec and spec["whole"] != SUPPLIER[g]:
                    whole_edges.add((SUPPLIER[g], spec["whole"]))
            carried_only_by_split = split_edges - whole_edges
            anchors = collections.Counter(tpl[g]["anchor"] for g in splits)
            piece_home = sum(1 for g in splits if SUPPLIER[g] in (tpl[g]["selected_to"], tpl[g]["complement_to"]))
            key = (len(splits), len(edges), len(carried_only_by_split), piece_home)
            struct[key] += 1
            if len(examples) < 12:
                examples.append({"id": r["id"], "splits": {g: tpl[g] for g in splits}, "edges": sorted(edges),
                                 "edges_carried_only_by_split_pieces": sorted(carried_only_by_split), "anchors": dict(anchors)})
    out = {"profiles": len(table), "by_tag": {k: {str(kk): v for kk, v in c.items()} for k, c in by_tag.items()},
           "overall": {str(k): v for k, v in collections.Counter((t["min_split"], t["min_edge"]) for t in table).items()},
           "undecided": [t for t in table if t["undecided_split_caps"] or t["min_split"] is None],
           "split_certificate_structure (n_splits, n_edges, edges_only_by_split_pieces, splits_keeping_a_piece_home)": {str(k): v for k, v in struct.items()},
           "examples": examples, "table": table}
    text = json.dumps(out, indent=1)
    if args.output: args.output.write_text(text + "\n")
    print(json.dumps({k: out[k] for k in ("profiles", "by_tag", "overall", "split_certificate_structure (n_splits, n_edges, edges_only_by_split_pieces, splits_keeping_a_piece_home)")}, indent=1))
    print("undecided:", [(t["id"], t["undecided_split_caps"], t["min_split"]) for t in out["undecided"]])

if __name__ == "__main__":
    main()
