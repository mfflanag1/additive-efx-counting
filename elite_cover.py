"""Scan all directed-search elites: test the {2222,4211,3221} cover and
whether 5111/3311 is ever the sole EFX0 shape, focusing on lowest-count."""
import json, glob
from fastshape import efx0_shapes

files = ["results/anneal_elites.jsonl","results/parkfloor_elites.jsonl","results/nomin_elites.jsonl","results/sweep_results.jsonl"]
# known dual-verified count-4 instances
known = [
 [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[28,28,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]],
 [[3,13,8,40,7,39,38,13],[13,1,1,4,11,1,40,12],[7,3,2,12,2,39,25,12],[2,13,2,40,2,39,38,2]],
 [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[16,40,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]],
]
insts = []
for f in files:
    try:
        for line in open(f):
            line=line.strip()
            if not line: continue
            d=json.loads(line)
            if "values" in d:
                insts.append((d.get("count",-1), d["values"]))
    except FileNotFoundError:
        pass
for V in known:
    insts.append((-99, V))

cover_fail=[]; sole5111=[]; sole3311=[]; notarget=[]  # notarget = no 4211/3221 but efx
mincount=[]
for cnt,V in insts:
    sh=efx0_shapes(V)
    if not sh:
        mincount.append((0,V,{})); continue
    keys={tuple(int(x) for x in k) for k in sh}
    shd={tuple(int(x) for x in k):v for k,v in sh.items()}
    tot=sum(shd.values())
    if not (keys & {(2,2,2,2),(4,2,1,1),(3,2,2,1)}):
        cover_fail.append((V,shd))
    if not (keys & {(4,2,1,1),(3,2,2,1)}):
        notarget.append((V,shd))
    if keys=={(5,1,1,1)}: sole5111.append((V,shd))
    if keys=={(3,3,1,1)}: sole3311.append((V,shd))
    mincount.append((tot,V,shd))

print(f"elites scanned: {len(insts)}")
print(f"cover_fail (efx but not in 2222/4211/3221): {len(cover_fail)}")
print(f"no 4211/3221 (efx elsewhere): {len(notarget)}")
print(f"sole 5111: {len(sole5111)}  sole 3311: {len(sole3311)}")
print("--- lowest EFX0-count elites and their shapes ---")
for tot,V,shd in sorted(mincount)[:15]:
    print(f"  count={tot} shapes={shd}")
    if tot>0 and not ({(4,2,1,1),(3,2,2,1)} & set(shd)):
        print("     ^^ NO 4211/3221:", V)
for V,shd in notarget[:10]:
    print("NOTARGET", V, shd)
