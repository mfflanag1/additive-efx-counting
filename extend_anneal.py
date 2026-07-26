import random, math, json
from fast47 import Counter as _Cnt
_C58=_Cnt(5,8)
def count_efx0(v,cap=None):
    return (_C58.count(v),None)
base4=[[30,66,69,9,21,19,63],[12,56,58,9,10,24,52],[12,33,45,20,24,8,64],[11,60,1,18,2,6,41]]
# variables: existing agents' value of new good7 (4 values incl hub), + new agent5 row (8 values)
def make(newcol, a4):
    v=[base4[i][:]+[newcol[i]] for i in range(4)]
    v.append(a4[:])
    return v
def count(newcol,a4): return count_efx0(make(newcol,a4),cap=40)[0]
rng=random.Random(3)
best=999; bestcfg=None
for run in range(3):
    newcol=[60,1,1,1]              # hub covets good7 ~T-10; others low
    a4=[5,5,5,5,5,5,5,60]
    cur=count(newcol,a4); T=3.0
    for it in range(1500):
        if rng.random()<0.3:
            k=rng.randrange(4); old=newcol[k]; newcol[k]=rng.randint(0,70)
            c=count(newcol,a4)
            if c<=cur or rng.random()<math.exp((cur-c)/max(T,.01)): cur=c
            else: newcol[k]=old
        else:
            k=rng.randrange(8); old=a4[k]; a4[k]=rng.randint(0,70)
            c=count(newcol,a4)
            if c<=cur or rng.random()<math.exp((cur-c)/max(T,.01)): cur=c
            else: a4[k]=old
        if cur<best: best=cur; bestcfg=(newcol[:],a4[:])
        T*=0.9995
    print(f'run {run}: best {best}', flush=True)
print('BEST extension count:', best, flush=True)
if bestcfg:
    v=make(*bestcfg)
    print('confirm:', count_efx0(v)[0], flush=True)
    for r in v: print(' ',r, flush=True)
