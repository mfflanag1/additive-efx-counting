import json, glob, sys
best=None
for f in glob.glob("tracks/model/fo_*.json")+glob.glob("tracks/model/fa_*.json")+glob.glob("tracks/model/hc_*.json")+glob.glob("tracks/model/opt*.json"):
    try:
        d=json.load(open(f))
    except Exception:
        continue
    c=d.get("best")
    if c is None: continue
    if best is None or c<best[0]:
        best=(c,d["values"],f)
if best:
    print(json.dumps({"best":best[0],"file":best[2],"values":best[1]}))
else:
    print("none")
