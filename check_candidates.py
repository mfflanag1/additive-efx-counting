"""Run every candidate in a .jsonl through verifier #1. Any with efx0_count == 0 is
flagged for the full claim discipline (verifier #2, minimization) — never claimed here.
"""
import json
import sys

from verify import enumerate_all

path = sys.argv[1]
flagged = []
with open(path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        c = json.loads(line)
        r = enumerate_all(c["n"], c["m"], c["values"])
        tag = "*** NO EFX0 — FLAG ***" if not r["efx0_exists"] else ""
        print(f"{c.get('name', '?')}: efx0_count={r['efx0_count']} "
              f"efxplus_count={r['efxplus_count']} {tag}")
        if not r["efx0_exists"]:
            flagged.append(c)
if flagged:
    print(json.dumps(flagged, indent=1))
else:
    print("-- no witnesses among candidates --")
