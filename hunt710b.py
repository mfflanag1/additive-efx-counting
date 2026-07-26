import random, math, json, time
from fast_verify import count_efx0
V6=[[15,86,103,193,191,192,195,196],[6,3,12,105,23,65,4,2],[11,68,55,10,152,8,7,2],[49,3,11,2,64,104,8,7],[2,6,31,79,40,61,104,7],[53,45,3,105,102,103,151,152]]
FL=[1,1,1,1,1,2]  # existing floater(good9) values
def build(g8, a6):
    # g8: value of new singleton good8 for the 6 existing agents (hub=g8[0])
    v=[]
    for i in range(6):
        v.append(V6[i]+[g8[i]]+[FL[i]])
    v.append(a6)
    return v
def count(g8,a6,cap=40): return count_efx0(build(g8,a6),cap=cap)[0]
rng=random.Random(0)
g8=[190,4,4,4,4,4]              # hub covets new singleton at 190; existing agents low
a6=[20,20,20,5,5,5,5,5,150,1]   # agent6 owns good8=150
cur=count(g8,a6); best=cur; bestcfg=(g8[:],a6[:])
print(f'start {cur}',flush=True)
t0=time.time(); it=0; Temp=5.0
while time.time()-t0<7200:
    it+=1
    if rng.random()<0.4:
        k=rng.randrange(6); old=g8[k]; g8[k]=rng.randint(0,200)
        c=count(g8,a6)
        if c<=cur or rng.random()<math.exp((cur-c)/max(Temp,.05)): cur=c
        else: g8[k]=old
    else:
        k=rng.randrange(10); old=a6[k]; a6[k]=rng.randint(0,200)
        c=count(g8,a6)
        if c<=cur or rng.random()<math.exp((cur-c)/max(Temp,.05)): cur=c
        else: a6[k]=old
    if cur<best:
        best=cur; bestcfg=(g8[:],a6[:])
        print(f'[{it}] best {best} g8={g8} a6={a6}',flush=True)
    Temp*=0.999
    if it%40==0: print(f'[{it}] cur={cur} best={best} t={int(time.time()-t0)}s',flush=True)
print('FINAL',best,flush=True); print(json.dumps(bestcfg),flush=True)
