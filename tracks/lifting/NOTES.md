# Track A (Lifting) — Mining fallen EFX neighbors for an additive n=4 goods witness

Target (open): EFX for **n=4 agents, ADDITIVE valuations, indivisible goods**.
Known safety walls we must clear:
- n ≤ 3 additive: EFX proven to exist (Chaudhury–Garg–Mehlhorn).
- ≤ 3 distinct additive valuation **types**: proven EFX-safe.  ← definition of "type" is load-bearing; see §3.
So any additive lift needs **4 agents with ≥4 pairwise-distinct valuation rows**.

---

## 1. Verbatim constructions extracted

### 1A. arXiv 2605.06451 — subadditive + submodular(weighted-coverage), 3 agents, 8 goods

**Shared scaffold.** 8 goods partitioned by type: `A={0,3}`, `B={1,4}`, `C={2,5}`, plus special
goods `x=6`, `y=7`. A single **canonical agent 0** valuation is defined; agents 1,2 are obtained by the
cyclic relabeling
```
σ = (0 1 2)(3 4 5),  x,y fixed         # A→B→C→A on the two triples
u_1(S) = u_0(σ(S)),  u_2(S) = u_0(σ²(S))
```
Crucially **both witness valuations depend only on the type-SUPPORT of S** (which of A,B,C,x,y are
touched), not on how many goods of each type are present. This is the whole engine.

**Instance 1 — subadditive (cardinal).**
```
λ = 2^(−1/6) ≈ 0.891
v_i(∅) = 0 ;  v_i(S) = λ^(7 − r_i(S))  for S ≠ ∅
```
`r_i` is a rank in {1..7} from agent 0's base order (support-only). Ranks:
- singletons: r=1 for every good
- pairs (base r0), from their Table 1:
  ```
  A-A:1  A-B:2  A-C:2  A-x:4  A-y:6
  B-B:1  B-C:5  B-x:1  B-y:3
  C-C:1  C-x:1  C-y:3
  x-y:1
  ```
- "exceptional" triples get rank 7:  012 015 024 045 123 135 234 345 126 156 246 456
- other triples: max rank of an internal pair;  |S|≥4: max rank of an internal triple.

Subadditivity holds only because every nonzero value ≥ λ⁶ = 1/2, so v(S)+v(T) ≥ 1 ≥ v(S∪T).
No α-EFX for α∈(λ,1]; via Lemma 3.3, r_i(T)>r_i(S) ⇒ v_i(S) ≤ λ·v_i(T).

**Instance 2 — submodular / weighted coverage (cardinal).**  χ_R(S)=1 iff S∩R≠∅.
```
u_0(S) =  χ_B(S) + χ_C(S)
        + 3·χ_{A∪{x}}(S) + 3·χ_{B∪{y}}(S) + 3·χ_{C∪{y}}(S)
        + 8·χ_{A∪B}(S)   + 8·χ_{A∪C}(S)
        + 9·χ_{B∪{x,y}}(S) + 9·χ_{C∪{x,y}}(S)
        + 2·χ_{A∪B∪{y}}(S) + 2·χ_{A∪C∪{y}}(S)
u_1 = u_0∘σ ,  u_2 = u_0∘σ²
```
Value ranges are separated by rank (rank0:0, r1:21–35, r2:36, r3:37–40, r4:41–45, r5:46, r6:47–48,
r7:49), so r_0(S)>r_0(T) ⇒ u_0(S)>u_0(T) — the cardinal witness realizes the ordinal one.

**Nonexistence (both).** Cyclic-symmetry lemma: EFX allocations are closed under
X ↦ (σX_1, σX_2, σX_0), collapsing case analysis to 3 size patterns of |X_0|:
`|X_0|≤1`, `(2,2,4)`, `(2,3,3)`. In each, some agent, after deleting **one good** from the envied
bundle, still strongly envies. The deleted good is (often) redundant under the coverage/support
valuation → deleting it does not lower the bundle's value. That redundancy is the mechanism additive
valuations cannot reproduce (§2).

### 1B. arXiv 2604.18216 — SAT-found, 3 agents, 8 goods, monotone/submodular

Smallest witness: **3 agents, 8 goods** g0..g7. Each valuation is a full 256-entry rank table
(subset→rank in 0..255), given only in Appendix A / the companion webpage — **not reproducible from
the abstract or html body**. Nonexistence is by exhaustive SAT over all 1,806 (nonempty-bundle)
allocations; only "272 of 5,796" allocations violate a single EFX condition. The authors state the
valuations exhibit **"substantial complementarity"** and are **"far from additive,"** deliberately.
→ This witness is the LEAST liftable: it is engineered against additivity and exposes no singleton
table to shadow. Treated as inspiration only (max-disagreement additive analogue, candidate C6).

### 1C. arXiv 2606.08872 — additive CHORES, n≥4, tri-valued, tight

n=4 fully instantiated. Chores in 3 groups: A={a1,a2,a3} (3), B={b1..b5} (5), C={c1..c5} (5); m=13.
Two agent types, tri-valued costs (Table 1):
```
              Group A   Group B   Group C
Agents 1,2       20        1         7
Agents 3,4       20        7         1
```
Per-agent total cost = 3·20 + 5·1 + 5·7 = 100; equal split = 25.
General n: |A|=n−1, |B|=|C|=2⌈n/2⌉+1; cost values (p,q,r)=(1, s+2, s(q+1)/2).
Nonexistence (n=4): (P1) no agent gets >1 A-item; (P2) an A-free agent has c_i(X_i)≥20; a B/C count
argument then forces some agent to strong-envy after removing one chore **from its own bundle**.

---

## 2. Where additivity breaks each construction (the analysis)

Write the additive closure of a valuation as `v'(S) = Σ_{g∈S} v({g})`.
Goods-EFX defect for the pair (i envies j):
```
def(i,j) = max_{g∈X_j} v_i(X_j \ {g}) − v_i(X_i)          # >0  ⇔  EFX violation
```

**(a) Coverage / subadditive witnesses (1A) — the "redundant good" collapses.**
Their argument keeps `def(i,j)>0` by choosing the deleted good g to be **redundant**: under a coverage
or support-only valuation a bundle can contain a good with **zero marginal value** (its type/coverage
is already present), so `v_i(X_j\{g}) = v_i(X_j)` and deletion buys the envied agent nothing.
The exact inequality that fails under additive closure: for additive v',
```
max_{g∈X_j} v'_i(X_j\{g}) = v'_i(X_j) − min_{g∈X_j} v_i({g})
```
so the hardest EFX comparison removes the single least-valued good. With strictly positive additive
values there is a positive cushion equal to the bottom good in the envied bundle, but it can be
arbitrarily small. Coverage can drive that cushion exactly to 0 through a redundant good. Concretely,
`def(i,j)_additive = v'_i(X_j) − v'_i(X_i) − min_{g∈X_j} v_i({g})`.

**Empirically fatal:** the additive shadow of Instance 2 (singletons of u_0, computed) is
```
agent0 = agent1 = agent2 = [23,23,23,23,23,23, 21, 28]   (goods A,B,C=23, x=21, y=28)
```
σ only permutes the *equal-valued* A/B/C goods and fixes x,y, so **all three shadows are identical → a
single type → provably EFX-safe.** The coverage weights that made bundles differ (8·χ_{A∪B}, 9·χ_{B∪xy},…)
are cross-type synergies that vanish under Σ-of-singletons: every good ends up in ~the same number of
weighted sets, giving a near-uniform singleton vector (bottom 21 ≈ average 23.4), i.e. a large cushion and
trivially curable envy. **Naive shadowing destroys the witness twice over: it flattens values AND
collapses the type count.**

**(b) Chores witness (1C) — the removal quantifier lands on the wrong bundle.**
Additive chores-EFX (envier removes from its OWN bundle):
`c_i(X_i) − min_{g∈X_i} c_i({g}) ≤ c_i(X_j)`.
Additive goods-EFX (envier removes from the ENVIED bundle):
`v_i(X_i) ≥ v_i(X_j) − min_{g∈X_j} v_i({g})`.
The standard negation/complement map `v_i(S)=c_i(M)−c_i(M∖S)` is additive⇒`v_i(S)=c_i(S)`; as an
*EFX-preserving* correspondence it is a bijection between goods- and chores-allocations **only when
n=2**, because there the complement of a bundle is exactly the other agent's bundle. For **n≥4 the
complement of X_i is the union of the other n−1 bundles, not any single agent's share**, so a chores
partition has no goods-partition image and the "remove one item from bundle Z" quantifier cannot be
transported to the same Z on the goods side. Hence the tri-valued chores counterexample does **not**
lift to goods by negation. (Its raw complement values 21−{20,1,7}={1,20,14} also give only 2 distinct
rows = 2 types = provably safe; see candidate C3 control.)

---

## 3. The "type" definitional caveat (decisive — flagged)

The ≤3-types safety theorem is stated over **distinct valuations = distinct value vectors (rows)**, not
distinct-up-to-relabeling-of-goods. Under that reading:
- A cyclic-relabeling additive instance has **≥4 distinct rows iff the base row is not σ-invariant.**
  My cyclic families (C1,C2,C4,C7) have 4 distinct rows and therefore escape the theorem — legitimately.
- BUT the 2605.06451 witnesses are relabeling-SYMMETRIC; if a future safety proof counted types
  *up to permutation*, all cyclic-only families collapse to 1 type and would be provably safe.
**Insurance:** candidate C9 uses four genuinely different value **multisets** (not permutations of each
other), so it is unambiguously 4 types under either reading. Any serious lift attempt should keep at
least one multiset-distinct family in play until the theorem's exact "type" definition is pinned down.

---

## 4. Candidate families written (see candidates.jsonl)

C1 cyclic-pairs-4type · C2 cyclic-pairs-steep · C3 chores-complement-2type (control) ·
C4 chores-gadget-4group-4type · C5 coverage-additive-shadow (identical-row control) ·
C6 sat-inspired-latin-rotation · C7 cyclic-pairs-m9 · C8 tri-valued-contested-m9 ·
C9 distinct-multiset-4type (type-definition insurance).
None is claimed to be a counterexample — the campaign's exact verifier decides.

---

## 5. No-go insight (lemma target)

**Claim (additive EFX-defect cushion).** For additive v and any pair (i,j),
```
def(i,j) = v_i(X_j) − v_i(X_i) − min_{g∈X_j} v_i({g}).
```
Strong envy therefore requires an agent i to value some bundle X_j MORE than its own by *strictly more
than the least valuable good in X_j*. Two consequences that doom naive lifts:

1. **Support-only / coverage witnesses shadow to near-uniform singletons** (bottom good ≈ average), so
   `min_{g∈X_j} v_i({g})` is a substantial fraction of `v_i(X_j)` and the cushion swallows modest envy — and the
   relabeling symmetry additionally collapses the shadow to one type. (Verified: coverage witness →
   `[23,23,23,23,23,23,21,28]`, identical across agents.)
2. **Chores witnesses cannot be complemented for n≥4** because complementation is a partition-bijection
   only at n=2; the EFX removal quantifier sits on the envier's own bundle for chores but on the envied
   bundle for goods.

**Lemma to prove/refute:** *Any additive instance obtained as the singleton-shadow of a coverage or
support-only valuation, or as the negation-complement of an additive chores instance with n≥4, has
≤3 distinct rows and admits an EFX allocation.* If true, it formally closes the naive-lift avenue and
forces the search onto instances (like C9) whose value multisets are engineered to be distinct AND to
keep `min_{g∈X_j} v_i({g})` small relative to the envy gap — i.e. bundles containing a tiny
observer-specific good, the additive regime where the EFX cushion is thinnest.
