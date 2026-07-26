"""Exact two-treasure EFX0 screen for 4-agent additive instances.
Returns a witnessing (a,b,t1,t2,Hc,Hd) if some two-singleton + 2-split allocation is EFX0, else None.
Cost: 12 agent-role orderings * m*(m-1) treasure pairs * 2^(m-2) splits.
"""
import itertools
def tau(v,S):
    return 0 if not S else sum(v[g] for g in S)-min(v[g] for g in S)
def two_treasure_witness(V):
    n=len(V); m=len(V[0]); agents=range(n); goods=range(m)
    for a,b in itertools.permutations(agents,2):
        if a>b: continue  # a,b unordered as treasure-holders
        c,d=[x for x in agents if x!=a and x!=b]
        for t1,t2 in itertools.permutations(goods,2):
            # a<-t1, b<-t2 ; note t1,t2 ordered matters (a gets t1)
            R=[g for g in goods if g!=t1 and g!=t2]
            va_t1=V[a][t1]; vb_t2=V[b][t2]
            for bits in range(1<<len(R)):
                Hc=[R[i] for i in range(len(R)) if bits>>i&1]
                Hd=[R[i] for i in range(len(R)) if not bits>>i&1]
                if tau(V[a],Hc)>va_t1 or tau(V[a],Hd)>va_t1: continue
                if tau(V[b],Hc)>vb_t2 or tau(V[b],Hd)>vb_t2: continue
                if sum(V[c][g] for g in Hc) < tau(V[c],Hd): continue
                if sum(V[d][g] for g in Hd) < tau(V[d],Hc): continue
                return dict(a=a,b=b,c=c,d=d,t1=t1,t2=t2,Hc=Hc,Hd=Hd)
    return None
if __name__=='__main__':
    import time
    V=[[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[16,40,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]]
    t=time.time(); w=two_treasure_witness(V); dt=time.time()-t
    print('V witness:',w)
    print('screen time (s): %.3f'%dt)
