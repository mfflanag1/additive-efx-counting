"""Determine the minimal shape-covering set empirically. For each regime, count
sole-shape instances and cover failures of candidate sets. Also try to force
sole-5111."""
import random, sys
from fastshape import efx0_shapes

n,m=4,8
ALL=[(2,2,2,2),(4,2,1,1),(3,2,2,1),(3,3,1,1),(5,1,1,1)]

def gen(hi,mode):
    if mode=="flat": return [[random.randint(1,hi) for _ in range(m)] for _ in range(n)]
    if mode=="lumpy":
        V=[]
        for i in range(n):
            row=[random.randint(1,3) for _ in range(m)]
            for _ in range(random.randint(1,3)): row[random.randrange(m)]=random.randint(hi//2,hi)
            V.append(row)
        return V
    if mode=="skew": return [[random.choice([1,1,1,2,2,3,hi//2,hi]) for _ in range(m)] for _ in range(n)]
    if mode.startswith("peaks"):
        k=int(mode[5:]) if len(mode)>5 else 2
        peaks=random.sample(range(m),k)
        V=[]
        for i in range(n):
            row=[random.randint(1,5) for _ in range(m)]
            for p in peaks: row[p]=random.randint(hi//2,hi)
            V.append(row)
        return V
    if mode=="onebig":  # one agent has a dominant-ish good (test 5111)
        V=[[random.randint(1,4) for _ in range(m)] for _ in range(n)]
        for i in range(n):
            V[i][i]=random.randint(hi//2,hi)  # each agent a distinct private peak
        return V

def run(hi,N,mode,seed):
    random.seed(seed)
    sole={s:0 for s in ALL}
    cover_fail_4={s:0 for s in [ (2,2,2,2),(4,2,1,1),(3,2,2,1),(3,3,1,1) ]}
    fail4=0; fail_all=0; efx=0
    ex4=[]; exall=[]
    C4={(2,2,2,2),(4,2,1,1),(3,2,2,1),(3,3,1,1)}
    for _ in range(N):
        V=gen(hi,mode)
        sh=efx0_shapes(V)
        if not sh: fail_all+=1; exall.append(V); continue
        efx+=1
        keys={tuple(int(x) for x in k) for k in sh}
        if len(keys)==1:
            sole[next(iter(keys))]+=1
        if not (keys & C4):
            fail4+=1
            if len(ex4)<6: ex4.append((V,{tuple(int(x) for x in k):v for k,v in sh.items()}))
    print(f"mode={mode} hi={hi} N={N} seed={seed}: efx={efx} no_efx={fail_all} "
          f"fail_cover{{2222,4211,3221,3311}}={fail4}")
    print(f"   sole: "+", ".join(f"{s}:{sole[s]}" for s in ALL if sole[s]))
    for V,shd in ex4[:6]: print("   COVER4_FAIL", V, shd)
    for V in exall[:4]: print("   NO_EFX", V)

if __name__=="__main__":
    hi=int(sys.argv[1]); N=int(sys.argv[2]); mode=sys.argv[3]; seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    run(hi,N,mode,seed)
