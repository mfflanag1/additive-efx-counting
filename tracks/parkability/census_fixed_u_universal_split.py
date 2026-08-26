#!/usr/bin/env python3
"""Census: universal split oracle over every profile in the fixed-U cut ledgers."""
from __future__ import annotations

import argparse
import json
import sys
from multiprocessing import Pool
from pathlib import Path

from .fixed_u_universal_split import load_rows, universal_decide, load_profile


def profiles(paths):
    out = []
    for path in paths:
        for i, line in enumerate(Path(path).read_text().splitlines()):
            if not line.strip():
                continue
            row = json.loads(line)
            if "round" in row and "totals" in row["round"]:
                out.append((f"{Path(path).name}#{i}", row["round"]))
            elif "totals" in row:
                out.append((f"{Path(path).name}#{i}", row))
            elif "profile_totals" in row:
                out.append((f"{Path(path).name}#{i}", {"totals": row["profile_totals"], "minima": row["profile_minima"]}))
    return out


def work(args):
    name, round_, split_cap, edge_cap, timeout = args
    totals, minima = load_rows(round_)
    try:
        r = universal_decide(totals, minima, split_cap, edge_cap, timeout, max_rounds=300)
    except AssertionError as e:
        return {"name": name, "status": "SHAPE_ERROR", "detail": repr(e)}
    return {"name": name, "split_cap": split_cap, "edge_cap": edge_cap, "status": r["status"],
            "menu_size": r.get("menu_size"), "max_split_used": r.get("max_split_used"),
            "obstructing_cell": r.get("obstructing_cell"), "seconds": round(r["seconds"], 1),
            "multi_roles": r.get("multi_roles")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=Path, action="append", required=True)
    ap.add_argument("--split-cap", type=int, default=4)
    ap.add_argument("--edge-cap", type=int, default=4)
    ap.add_argument("--timeout-seconds", type=int, default=60)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    rows = profiles(a.ledger)
    jobs = [(n, r, a.split_cap, a.edge_cap, a.timeout_seconds) for n, r in rows]
    with a.output.open("w") as f, Pool(a.workers) as pool:
        for res in pool.imap_unordered(work, jobs):
            f.write(json.dumps(res, sort_keys=True) + "\n"); f.flush()
            print(res["name"], res["status"], res.get("menu_size"), res.get("seconds"), flush=True)


if __name__ == "__main__":
    main()
