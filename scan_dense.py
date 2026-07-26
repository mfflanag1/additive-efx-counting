from fast47 import Counter
C=Counter(4,7)
def build(P,Q,R,S,T):
    m=7; v=[[0]*m for _ in range(4)]
    for g in range(3): v[0][g]=P
    for g in range(3,6): v[0][g]=S
    v[0][6]=1
    for i in range(1,4):
        for g in range(3): v[i][g]=Q
        for g in range(3,6): v[i][g]=T
        v[i][2+i]=R
        v[i][6]=1
    return v
hits=[]
vals=[1,4,9,16,25,36,50,70]
for P in vals:
 for Q in vals:
  if Q>P: continue
  for R in vals:
   for S in vals:
    for T in vals:
      v=build(P,Q,R,S,T)
      if C.count(v)==4: hits.append((P,Q,R,S,T))
print('exact-4 formulas found:',len(hits),flush=True)
for h in hits[:60]: print('  ',h,flush=True)
