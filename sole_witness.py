"""Find one clean small-value NC-satisfying instance whose EFX0 allocations are
ALL of a single target shape, for each of the 5 shapes. Dual-verify via verify.py."""
import random
from fastshape import efx0_shapes
from verify import enumerate_all
from collections import Counter
from residual_test import satisfies_NCA, universal_min_good, pairwise_nonproportional, dominant_pairs

n,m=4,8
TARGETS=[(2,2,2,2),(3,2,2,1),(4,2,1,1),(3,3,1,1),(5,1,1,1)]

def genpeaks(hi,k):
    V=[[random.randint(1,4) for _ in range(m)] for _ in range(n)]
    for p in random.sample(range(m),k):
        for i in range(n): V[i][p]=random.randint(hi//2,hi)
    return V

def nc_ok(V):
    return universal_min_good(n,m,V) is None and pairwise_nonproportional(n,m,V) and satisfies_NCA(n,m,V)

found={}
random.seed(7)
# map shape->preferred peak count
plan={(2,2,2,2):0,(3,2,2,1):1,(4,2,1,1):2,(3,3,1,1):2,(5,1,1,1):3}
tries=0
while len(found)<5 and tries<400000:
    tries+=1
    tgt=[t for t in TARGETS if t not in found]
    t=random.choice(tgt)
    hi=random.choice([12,16,20,24])
    V=genpeaks(hi,plan[t])
    if not nc_ok(V): continue
    sh=efx0_shapes(V)
    keys={tuple(int(x) for x in k) for k in sh}
    if keys=={t}:
        # score by smallness
        mx=max(max(r) for r in V)
        if t not in found or mx<found[t][1]:
            found[t]=(V,mx,sum(sh.values()))

for t in TARGETS:
    if t in found:
        V,mx,cnt=found[t]
        # dual verify
        r=enumerate_all(4,8,V,collect=99999)
        c=Counter(tuple(sorted([ex.count(i) for i in range(4)],reverse=True)) for ex in r['examples_efx0'])
        print(f"SHAPE {t}: maxval={mx} totalEFX0={r['efx0_count']} shapes={dict(c)}")
        print(f"   V={V}")
        print(f"   NC-A={satisfies_NCA(n,m,V)} univmin={universal_min_good(n,m,V)} nonprop={pairwise_nonproportional(n,m,V)} dom={dominant_pairs(n,m,V)}")
    else:
        print(f"SHAPE {t}: none found")
