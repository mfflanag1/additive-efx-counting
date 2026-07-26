"""Fast coupling sweep: precompute EFX0 tables once per instance."""
import sys,random,json
sys.path.insert(0,'.')
from verify import precompute, check_allocation

def bmask(B,n):
    bd=[0]*n
    for a in range(n):
        for g in B[a]: bd[a]|=1<<g
    return bd

def efx0(bd,n,tabs): 
    return check_allocation(n,bd,tabs[0],tabs[1],tabs[2])[0]

def enum_has_efx0(n,m,tabs):
    assign=[0]*m
    while True:
        bd=[0]*n
        for g in range(m): bd[assign[g]]|=1<<g
        if check_allocation(n,bd,tabs[0],tabs[1],tabs[2])[0]: return True
        g=0
        while g<m:
            assign[g]+=1
            if assign[g]<n: break
            assign[g]=0; g+=1
        else: return False

def park_places(V,B,f,n,m,tabs):
    good=[]
    for i in range(n):
        assign=[None]*m
        for a in range(n):
            for g in B[a]: assign[g]=a
        assign[f]=i
        bd=[0]*n
        for g,a in enumerate(assign): bd[a]|=1<<g
        if efx0(bd,n,tabs): good.append(i)
    return good

def vv(V,k,S): return sum(V[k][g] for g in S)
def envy_edges(V,B):
    n=len(B); return [[i!=j and vv(V,i,B[i])<vv(V,i,B[j]) for j in range(n)] for i in range(n)]
def find_cycle(E):
    n=len(E)
    for s in range(n):
        st=[(s,[s])]
        while st:
            u,p=st.pop()
            for v in range(n):
                if E[u][v]:
                    if v==s and len(p)>=2: return p
                    if v not in p: st.append((v,p+[v]))
    return None
def rotate(B,cyc):
    B2=[b[:] for b in B]
    for idx in range(len(cyc)):
        B2[cyc[idx]]=B[cyc[(idx+1)%len(cyc)]][:]
    return B2
def rot_recovers(V,B,f,n,m,tabs,mx=12):
    cur=[b[:] for b in B]
    for _ in range(mx):
        if park_places(V,cur,f,n,m,tabs): return True
        c=find_cycle(envy_edges(V,cur))
        if c is None: return bool(park_places(V,cur,f,n,m,tabs))
        cur=rotate(cur,c)
    return bool(park_places(V,cur,f,n,m,tabs))

def run(trials,n=4,m=8,vmax=25,seed=1):
    rng=random.Random(seed)
    unpark=rot_ok=full_ok=0; cex=[]; rf=[]
    for t in range(trials):
        V=[[rng.randint(1,vmax) for _ in range(m)] for _ in range(n)]
        tabs=precompute(n,m,V)
        full=None
        for f in range(m):
            rest=[g for g in range(m) if g!=f]
            for _ in range(25):
                B=[[] for _ in range(n)]
                for g in rest: B[rng.randrange(n)].append(g)
                if not all(B): continue
                if not efx0(bmask(B,n),n,tabs): continue
                if park_places(V,B,f,n,m,tabs): continue
                unpark+=1
                if full is None: full=enum_has_efx0(n,m,tabs)
                if full: full_ok+=1
                else: cex.append((V,B,f))
                if rot_recovers(V,B,f,n,m,tabs): rot_ok+=1
                elif len(rf)<8: rf.append((V,B,f))
                break
    print(f"un-parkable bases: {unpark}")
    print(f"full instance HAS EFX0 elsewhere: {full_ok}/{unpark}")
    print(f"cycle-rotation recovers EFX0: {rot_ok}/{unpark}")
    print(f"COUNTEREXAMPLES: {len(cex)}")
    for c in cex[:5]: print("  *** CEX ***",json.dumps(c[0]),"base",c[1],"f",c[2])
    print(f"rotation-missed (EFX0 exists, rotation didn't find): {len(rf)}")
    for c in rf[:8]: print("  rotmiss",json.dumps(c[0]),"base",c[1],"f",c[2])
if __name__=='__main__': run(int(sys.argv[1]) if len(sys.argv)>1 else 2000)
