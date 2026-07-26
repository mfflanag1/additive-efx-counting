import random, math, json, time
from fast_verify import count_efx0

T=204; GAPS=(8,9,10,11,12,13); TRI=[15,86,103]
def build(S):
    v=[TRI+[T-g for g in GAPS]+[1]]      # hub row, floater=1
    for i in range(6):
        v.append([20,20,20]+list(S[i])+[1])
    return v
def count(S, cap=15):
    return count_efx0(build(S), cap=cap)[0]

# condition-4 start: own-singleton highest, all others high & near, distinct perturbations
def start_S(rng):
    S=[]
    for i in range(6):
        row=[145 + ((i*6+k)%9) for k in range(6)]
        row[i]=150 + i          # own highest, distinct
        S.append(row)
    return S

rng=random.Random(0)
S=start_S(rng)
cur=count(S)
best=cur; bestS=[r[:] for r in S]
print(f'start count {cur}', flush=True)
t0=time.time(); it=0; Temp=4.0
while time.time()-t0 < 9000:   # ~2.5h budget
    it+=1
    i=rng.randrange(6); k=rng.randrange(6)
    old=S[i][k]; S[i][k]=random.randint(120,160)
    c=count(S)
    if c<=cur or rng.random()<math.exp((cur-c)/max(Temp,0.05)):
        cur=c
        if c<best:
            best=c; bestS=[r[:] for r in S]
            print(f'[{it}] new best {best}  S={json.dumps(bestS)}', flush=True)
            if best<=7:
                print('REACHED <=7', flush=True)
    else:
        S[i][k]=old
    Temp*=0.999
    if it%50==0:
        print(f'[{it}] cur={cur} best={best} elapsed={int(time.time()-t0)}s', flush=True)
print(f'FINAL best={best}', flush=True)
print(json.dumps(bestS), flush=True)
# exact full count of best (no cap) for the record
print('exact count of best (full):', count_efx0(build(bestS))[0], flush=True)
