"""Count-minimizer seeded from random NO-universal-min instances (every good is some
agent's strict non-min), to escape the single-floater parking-floor regime."""
import sys,random,math,json,time
sys.path.insert(0,'.')
from verify import enumerate_all
def has_universal_min(V):
    # a good g is universal-min if it's the min for every agent
    return any(all(V[k][g]==min(V[k]) for k in range(4)) for g in range(8))
def rand_nomin(rng):
    while True:
        V=[[rng.randint(1,40) for _ in range(8)] for _ in range(4)]
        if not has_universal_min(V): return V
def count(V): return enumerate_all(4,8,V,collect=0)['efx0_count']
def neighbor(V,rng):
    W=[r[:] for r in V]; i,g=rng.randrange(4),rng.randrange(8)
    W[i][g]=max(1,min(120,W[i][g]+rng.choice([-5,-3,-2,-1,1,2,3,5])))
    return W
def run(seed,iters=30000):
    rng=random.Random(seed); V=rand_nomin(rng); cur=count(V); best=cur; bV=V; t=time.time()
    with open('results/nomin_elites.jsonl','a') as f:
        for it in range(iters):
            temp=2.0*(1-it/iters)+0.02; W=neighbor(V,rng); c=count(W)
            if c<=cur or rng.random()<math.exp(-(c-cur)/temp):
                V,cur=W,c
                if cur<best:
                    best=cur; bV=[r[:] for r in V]
                    f.write(json.dumps({'count':cur,'seed':seed,'iter':it,'values':V})+'\n'); f.flush()
                    print(f'seed{seed} it{it} count={cur} ({time.time()-t:.0f}s)',flush=True)
                    if cur==0: print('*** WITNESS ***',json.dumps(V),flush=True); return
            if it%3000==2999: V=[r[:] for r in bV]; cur=best
    print(f'seed{seed} done best={best}',flush=True)
if __name__=='__main__': run(int(sys.argv[1]))
