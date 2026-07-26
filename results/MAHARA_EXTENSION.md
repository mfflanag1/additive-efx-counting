> **SUPERSEDED NOTE (2026-07-24, referee round):** claims below that identical/flat valuations
> imply shape 2222 are WITHDRAWN. Counterexample: four identical rows [100,1,1,1,1,1,1,1] admit
> 2,520 EFX0 allocations, all of shape 3221. Identical valuations are EFX-safe (Plaut-Roughgarden
> leximin) but not via 2222.

# Toward Mahara's technique at (4,8): the bundle-shape reduction

**Goal.** Attempt to prove *EFX₀ exists for every 4-agent, 8-good, positive-additive instance* — the first
cell beyond Mahara's `m ≤ n+3`. Notation as in `TWO_TREASURE_LEMMA.md`: `τ_i(S)=v_i(S)−min_{g∈S}v_i(g)`,
strong envy `v_i(X_i) < τ_i(S)`; all values positive ⇒ EFX₀ ≡ EFX₊. Singleton immunity (Lemma 1′): a
size-1 bundle is never a strong-envy target.

**Honest scope.** A full proof here *is* the open problem. This document delivers what is achievable: (i) an
exact reduction to **five bundle-shapes**, (ii) the per-shape EFX₀ system, (iii) which shapes are
load-bearing (empirics), (iv) partial coverage results, and (v) the precise inequality system a stuck
instance must satisfy — the CP-SAT witness recipe.

---

## 1. WLOG all bundles nonempty ⇒ exactly five shapes (PROVEN)

**Lemma S0.** In any EFX₀ allocation of 8 positive-additive goods among 4 agents, **every bundle is
nonempty.**
*Proof.* Suppose agent `i` holds `∅` (`v_i(∅)=0`). The 8 goods lie in the other 3 bundles, so some bundle
`B` has `|B| ≥ ⌈8/3⌉ = 3 ≥ 2`. For `|B|≥2`, `τ_i(B) = v_i(B) − min_{g∈B}v_i(g) ≥ (\text{second-smallest
positive value}) > 0 = v_i(∅)`, so `i` strongly-envies `B`. Not EFX₀. ∎

Hence a complete EFX₀ (4,8) allocation has bundle-size multiset = a partition of 8 into 4 **positive** parts.
There are exactly **five**:

| shape | # singletons | strong-envy targets (size ≥ 2) | reduction |
|---|---|---|---|
| **5,1,1,1** | 3 | the 5-bundle | k=3 treasure (3 constraints) |
| **4,2,1,1** | 2 | 4-bundle, 2-bundle | k=2 two-treasure |
| **3,3,1,1** | 2 | both 3-bundles | k=2 two-treasure |
| **3,2,2,1** | 1 | 3-bundle, two 2-bundles | k=1 |
| **2,2,2,2** | 0 | all four 2-bundles | k=0 balanced |

**Proving `(4,8)` safe ⟺ every instance admits an EFX₀ allocation in ≥1 of these five shapes.**

---

## 2. Which shapes are load-bearing (empirics)

EFX₀ allocations of the dual-verified near-witnesses, classified by shape:
- **V (count 5):** `4211`×2, `3221`×2, `3311`×1.
- **V2 (count 10):** `4211`×8, `5111`×2.
- **V3 (count 4):** `3221`×2, `3311`×1, `4211`×1.

**Two facts jump out:** (a) near the boundary EFX₀ lives *only* in **singleton-containing** shapes
(`5111/4211/3311/3221`) — the **balanced `2222` shape carries none of the near-witness survivors**;
(b) the workhorse is **`4211`**, with `3221` close behind.

**CORRECTION (theory2 `RESIDUAL_ATTACK.md`).** The reading "4211/3221 are *the* hard cases" is a
**near-witness sampling bias** — those three instances came from one count-minimizing search that lands in
the 1–2-treasure basin. Across controlled regimes **all five shapes are individually load-bearing**: each of
`2222, 3221, 4211, 3311, 5111` is the *sole* EFX₀ shape on some instance satisfying every proven necessary
condition. In particular my earlier hypothesis "`2222` is never sole" is **FALSE** (my own sweep found
3/3000 sole-`2222`; theory2 has dual-verified witnesses). The correct organizing principle is the
**contested-good ladder** `k=0,1,2,3` — see `PER_K.md`, which supersedes this section's coverage read.

---

## 3. Per-shape EFX₀ system (via singleton immunity)

For an assignment realizing a shape, write the size-≥2 bundles as the *targets*; only these generate
constraints. Let the singletons be `{t}` (immune as targets).

- **5111** — 5-bundle `D` held by `d`; singletons `t_a,t_b,t_c` to `a,b,c`:
  `v_a(t_a) ≥ τ_a(D)`, `v_b(t_b) ≥ τ_b(D)`, `v_c(t_c) ≥ τ_c(D)`. (`d` envies no singleton.)
- **4211** — 4-bundle `F` (agent `d`), 2-bundle `P` (agent `c`), singletons `t_a,t_b`:
  each observer not holding it must tolerate `F` and `P`:
  `v_a(t_a) ≥ τ_a(F),τ_a(P)`; `v_b(t_b) ≥ τ_b(F),τ_b(P)`; `v_c(P) ≥ τ_c(F)`; `v_d(F) ≥ τ_d(P)`.
- **3311** — two 3-bundles `G,H` (agents `c,d`), singletons `t_a,t_b`:
  `v_a(t_a) ≥ τ_a(G),τ_a(H)`; `v_b(t_b) ≥ τ_b(G),τ_b(H)`; `v_c(G) ≥ τ_c(H)`; `v_d(H) ≥ τ_d(G)`.
- **3221** — 3-bundle `T` (agent `d`), two 2-bundles `P,Q` (agents `b,c`), singleton `t_a`:
  `v_a(t_a) ≥ τ_a(T),τ_a(P),τ_a(Q)`; `v_b(P) ≥ τ_b(T),τ_b(Q)`; `v_c(Q) ≥ τ_c(T),τ_c(P)`;
  `v_d(T) ≥ τ_d(P),τ_d(Q)`.
- **2222** — four 2-bundles: every agent tolerates the other three (12 ordered constraints,
  `τ_i(2\text{-bundle}) = ` its larger good).

An instance is EFX₀-solvable **iff** some shape's system is satisfiable over some good-assignment.

---

## 4. Partial coverage (what is provable)

- **5111 covers "3 dominant goods".** By Fact 2 (`τ_a(D) ≤ τ_a(M\{t_a})`), if three agents each own a
  dominant good (`v_a(t_a) ≥ τ_a(M\{t_a})`) on distinct goods, `5111` is EFX₀. (Strict extension of
  Theorem 1's two-treasure to three.)
- **2222 covers "flat/near-identical".** Theorem 2's ladder at `ρ ≤ 2` is a `2222`-type allocation; identical
  valuations always admit `2222` EFX₀ (Plaut–Roughgarden leximin). Empirically `2222` is *never the sole*
  EFX₀ shape near the boundary (§2), suggesting `2222` is dominated by singleton shapes exactly where the
  problem is hard.
- **4211/3311 cover the two-treasure regime** (Lemma 1 + NC-B) — the `CP`/peaks ladder lives here.
- **[PROVEN] Peeling Theorem (dominant good ⇒ EFX₀).** If any agent `a` has `v_a(t) ≥ τ_a(M\{t})`, peel
  `{t}→a` (satisfied against everything by Fact 2) and apply CGM to the other 3 agents on `M\{t}`. Covers
  every dominant-good instance at any `k`, and **strengthens NC-A** to "a witness has no dominant good at
  all." Full statement + proof in `PER_K.md §2`.

---

## 5. The stuck-instance inequality system (CP-SAT witness recipe)

A counterexample = an instance where **all five** shape-systems are infeasible over **all** good-assignments.
Combined with the proven necessary conditions, a witness `V` must satisfy simultaneously:
- **acyclic-envy WLOG** (Source Lemma / Mahara Lemma 7): on any EFX₀ sub-allocation the envy graph may be
  taken acyclic — so a witness cannot be "rescued" by rotation.
- **NC-A:** no good worth ≥ ½ its owner's universe (no dominant matching) ⇒ blocks `5111` via §4.
- **no global-min good** (else Source-Lemma parking closes it — empirically global-min is rare, §`SOURCE_LEMMA`).
- **NC-B / NC-Peaks:** the two-treasure and ladder systems fail ⇒ blocks `4211/3311` and the `CP` families.

The residual open core is: **`3221` and `4211` with tight sources**, i.e. an instance where every
`3221`/`4211` assignment has some singleton- or 2-bundle-holder strongly-envying a target by a hair, *and*
`5111` fails (NC-A) *and* `2222` fails (lumpy) *and* rotation cannot fix it (acyclic WLOG). The precise system
to hand CP-SAT is the conjunction of the §3 negations across shapes `5111/4211/3311/3221/2222`; the productive
seed is `4211`/`3221` with all four bundles' slacks driven to 0 simultaneously (the "tight-source" corner —
this is exactly where V sits, §2 shows V realizes `4211` and `3221` at slack 1).

---

## 6. Honest assessment

The bundle-shape reduction (Lemma S0 + the five-shape table) is clean and correct, and it localizes the
difficulty to shapes `4211`/`3221` — matching both the near-witness data and the lead's intuition. The
partial coverage (5111 for dominant, 2222 for flat, 4211/3311 for two-treasure) carves off the extremes. But
the **middle is the open problem**: I have **not** derived a contradiction that closes `4211`/`3221` for all
instances, and doing so would resolve `(4,8)` — beyond what the current lemmas force. The deliverable is
therefore the **reduction + residual system**, not a theorem. The residual system in §5 is the exact CP-SAT
target; the empirics (0 EFX₀-free in every search; K≤4 UNSAT) say the residual is very likely empty, i.e. the
theorem is very likely true, but its proof needs an idea that forces feasibility of the `4211`/`3221` system
from acyclicity + NC-A + NC-B + no-global-min — which I could not supply.
