import random
from collections import defaultdict
from fast47 import Counter
from fast_base import has_ef_base
C = Counter(4, 7)
rng = random.Random(20)
tab = defaultdict(lambda: [0, 0])   # count -> [has_base, no_base]
lowest_nobase = (999, None)
n_nobase = 0
for scale in (1, 2, 3, 4, 6, 9):
    for _ in range(4000):
        v = [[rng.randint(0, scale) for _ in range(7)] for _ in range(4)]
        c = C.count(v)
        if c <= 30:
            hb = has_ef_base(v)
            tab[c][0 if hb else 1] += 1
            if not hb:
                n_nobase += 1
                if c < lowest_nobase[0]:
                    lowest_nobase = (c, v)
print("count : [has_base, NO_base]")
for c in sorted(tab):
    print(f"  {c:3d}: {tab[c]}")
print("total no-base seen (count<=30):", n_nobase)
print("LOWEST no-base count:", lowest_nobase[0], lowest_nobase[1])
