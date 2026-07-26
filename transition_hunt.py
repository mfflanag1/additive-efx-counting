"""Hunt for EFX0-free instances in the DANGER ZONE: ambiguous peak-count, graded
peaks, asymmetric contests. Report no_efx and the lowest total EFX0 counts."""
import random, sys
from fastshape import efx0_shapes
from residual_test import satisfies_NCA, universal_min_good, pairwise_nonproportional

n,m=4,8

def gen(hi, mode):
    if mode=="graded":
        # peaks with values straddling the threshold, random subset of agents contest each
        V=[[random.randint(1,4) for _ in range(m)] for _ in range(n)]
        npk=random.randint(2,4)
        pks=random.sample(range(m),npk)
        for p in pks:
            base=random.randint(hi//3,hi)
            for i in range(n):
                if random.random()<0.75:  # asymmetric contest
                    V[i][p]=base+random.randint(-hi//4,hi//4)
                    V[i][p]=max(1,V[i][p])
        return V
    if mode=="mixed23":
        # 2 strong peaks (all contest) + 1 marginal (some contest)
        V=[[random.randint(1,4) for _ in range(m)] for _ in range(n)]
        s=random.sample(range(m),3); a,b,c=s
        for i in range(n):
            V[i][a]=random.randint(hi//2,hi); V[i][b]=random.randint(hi//2,hi)
            if random.random()<0.5: V[i][c]=random.randint(hi//3,hi)
        return V
    if mode=="twoscale":
        # two value scales, contested medium band
        V=[]
        for i in range(n):
            row=[random.choice([1,2,3, hi//4,hi//4+2, hi//2,hi]) for _ in range(m)]
            V.append(row)
        return V

def run(hi,N,mode,seed):
    random.seed(seed)
    no_efx=[]; lows=[]; tested_nc=0; efx=0
    for _ in range(N):
        V=gen(hi,mode)
        # only care about NC-satisfying (witness candidates)
        if universal_min_good(n,m,V) is not None: continue
        if not pairwise_nonproportional(n,m,V): continue
        if not satisfies_NCA(n,m,V): continue
        tested_nc+=1
        sh=efx0_shapes(V)
        tot=sum(sh.values())
        if tot==0: no_efx.append(V)
        else:
            efx+=1
            lows.append((tot,V,{tuple(int(x) for x in k):v for k,v in sh.items()}))
    lows.sort()
    print(f"mode={mode} hi={hi} N={N} seed={seed}: NC-tested={tested_nc} efx={efx} NO_EFX={len(no_efx)}")
    for V in no_efx[:5]: print("  !!! NO_EFX", V)
    print("  lowest counts:", [t for t,_,_ in lows[:8]])
    for t,V,shd in lows[:4]: print(f"    count={t} shapes={shd}")

if __name__=="__main__":
    hi=int(sys.argv[1]); N=int(sys.argv[2]); mode=sys.argv[3]; seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    run(hi,N,mode,seed)
