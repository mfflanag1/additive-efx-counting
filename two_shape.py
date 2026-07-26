"""Sharpest reduction test: does {2222, 4211} cover every EFX0-existent (4,8)?
i.e. is there an instance with EFX0 but no 2222 and no 4211 allocation?
Sweep random (flat/lumpy/skew) + elites + directed search around near-witnesses."""
import random, sys, json, glob
from fastshape import efx0_shapes

n, m = 4, 8
B2222=(2,2,2,2); B4211=(4,2,1,1); B3221=(3,2,2,1)

def keys_of(V):
    sh=efx0_shapes(V)
    return {tuple(int(x) for x in k) for k in sh}, sh

def gen(hi, mode):
    if mode=="flat": return [[random.randint(1,hi) for _ in range(m)] for _ in range(n)]
    if mode=="lumpy":
        V=[]
        for i in range(n):
            row=[random.randint(1,3) for _ in range(m)]
            for _ in range(random.randint(1,3)): row[random.randrange(m)]=random.randint(hi//2,hi)
            V.append(row)
        return V
    if mode=="skew": return [[random.choice([1,1,1,2,2,3,hi//2,hi]) for _ in range(m)] for _ in range(n)]
    if mode=="peaks":  # conflicting peaks - the NC-B seam
        peaks=random.sample(range(m),2)
        V=[]
        for i in range(n):
            row=[random.randint(1,5) for _ in range(m)]
            for p in peaks: row[p]=random.randint(hi//2,hi)
            V.append(row)
        return V

def run(hi,N,mode,seed):
    random.seed(seed)
    fail_2222_4211=[]   # efx but neither 2222 nor 4211
    fail_cover3=[]      # efx but none of 2222/4211/3221
    efxcnt=0
    for _ in range(N):
        V=gen(hi,mode)
        keys,sh=keys_of(V)
        if not keys: continue
        efxcnt+=1
        if not (keys & {B2222,B4211}):
            fail_2222_4211.append((V,{tuple(int(x) for x in k):v for k,v in sh.items()}))
        if not (keys & {B2222,B4211,B3221}):
            fail_cover3.append((V,{tuple(int(x) for x in k):v for k,v in sh.items()}))
    print(f"mode={mode} hi={hi} N={N} seed={seed}: efx={efxcnt} "
          f"fail{{2222,4211}}={len(fail_2222_4211)} fail{{2222,4211,3221}}={len(fail_cover3)}")
    for V,shd in fail_2222_4211[:6]:
        print("   NO_2222_NO_4211:", V, shd)
    return fail_2222_4211, fail_cover3

if __name__=="__main__":
    hi=int(sys.argv[1]); N=int(sys.argv[2]); mode=sys.argv[3]; seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    run(hi,N,mode,seed)
