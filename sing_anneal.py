import random, math, json
from fast47 import Counter
C=Counter(4,7)
HUB=[19,21,30,69,66,63,1]
UTRI=[[17,17,18],[18,17,17],[17,18,17]]  # non-hub value of hub triple (fixed)
def build(S):
    v=[HUB[:]]
    for i in range(3):
        v.append(UTRI[i]+[S[i][0],S[i][1],S[i][2]]+[1])
    return v
def count(S): return C.count(build(S))
rng=random.Random(1)
best=999; bestS=None
for run in range(10):
    S=[[55,50,50],[50,55,50],[50,50,55]]
    cur=count(S); T=2.0
    for it in range(3000):
        i=rng.randrange(3); k=rng.randrange(3)
        old=S[i][k]; S[i][k]=rng.randint(30,70)
        c=count(S)
        if c<=cur or rng.random()<math.exp((cur-c)/max(T,.01)): cur=c
        else: S[i][k]=old
        if cur<best: best=cur; bestS=[r[:] for r in S]
        T*=0.999
    if best<=4: break
print('best count:', best)
print('S matrix (rows=agents, cols=singletons):')
for r in bestS: print('  ',r)
v=build(bestS); print('full instance count:', C.count(v))
for r in v: print('   ',r)
