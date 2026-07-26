import itertools
def tau(v,S): return 0 if not S else sum(v[g] for g in S)-min(v[g] for g in S)
def ladder_witness(V, P, T):
    """Full ladder F_j screen: dump agent d holds j tails; the other 3 agents each hold a distinct peak,
    and any (5-j) of them additionally hold one distinct tail. Try ALL role/peak/tail assignments."""
    n=4
    for d in range(n):
        others=[a for a in range(n) if a!=d]
        for j in range(2,6):
            npt=5-j
            if npt<0 or npt>3: continue
            for perm in itertools.permutations(P):                 # peak per other-agent (by others order)
                for tailagents in itertools.combinations(range(3),npt):   # which others get a tail
                    for tailsel in itertools.permutations(T, npt):        # which tail each gets
                        used=set(tailsel); dumptails=[t for t in T if t not in used]
                        if len(dumptails)!=j: continue
                        bundles=[None]*n; bundles[d]=list(dumptails)
                        ti=0
                        for k,a in enumerate(others):
                            b=[perm[k]]
                            if k in tailagents:
                                b.append(tailsel[ti]); ti+=1
                            bundles[a]=b
                        if all(sum(V[o][g] for g in bundles[o])>=tau(V[o],bundles[jj])
                               for o in range(n) for jj in range(n) if o!=jj):
                            return (j,d,bundles)
    return None
