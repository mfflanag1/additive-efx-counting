import random, math, json
from fast47 import Counter
C = Counter(4, 7)

def hubrow(T=100, dset=(2,3,4)):
    return [30,33,37, T-dset[0],T-dset[1],T-dset[2], 1]   # covet 98,97,96 distinct

def build(nonhub, T=100):
    return [hubrow(T)] + nonhub

def count(nonhub):
    return C.count(build(nonhub))

def anneal(rng, iters):
    # non-hub rows: 3 agents, each 7 values. seed dense.
    nh = [[rng.randint(20,40) for _ in range(3)] + [ (100 if (2+i)==(3+k) else rng.randint(0,10)) for k in range(3)] + [1] for i in range(1,4)]
    # ensure agent i owns good 2+i at 100
    for idx,i in enumerate(range(1,4)):
        for k in range(3): nh[idx][3+k] = 5
        nh[idx][3+(i-1)] = 100
    cur = count(nh); best=cur; bestv=[r[:] for r in nh]; T=3.0
    for _ in range(iters):
        a=rng.randrange(3); g=rng.randrange(7)
        old=nh[a][g]; nh[a][g]=rng.randint(0,100)
        c=count(nh)
        if c<=cur or rng.random()<math.exp((cur-c)/max(T,.01)):
            cur=c
            if c<best: best=c; bestv=[r[:] for r in nh]
        else: nh[a][g]=old
        T*=0.9995
    return best,bestv

rng=random.Random(0)
gb=999; garg=None
for t in range(8):
    b,v=anneal(rng,4000)
    if b<gb: gb=b; garg=v
    print(f'run {t}: best {b}', flush=True)
print('MIN count with fixed hub knife-edge:', gb, flush=True)
print('hub:', hubrow(), flush=True)
for r in garg: print('  ', r, flush=True)
