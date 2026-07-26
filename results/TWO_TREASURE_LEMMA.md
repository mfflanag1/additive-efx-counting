# The Two-Treasure Repair Lemma

**Setting.** 4 agents `{0,1,2,3}`, additive valuations with **strictly positive integer** values,
`m` goods, EFX₀: for all `i≠j` and every `g ∈ X_j`, `v_i(X_i) ≥ v_i(X_j) − v_i(g)`.

**Notation.** For observer `i` and bundle `S` define the **EFX₀ removal-threshold**
`τ_i(S) := v_i(S) − min_{g∈S} v_i(g)` (for `|S|=0` set `τ_i(∅)=0`).
Then agent `i` *strongly-envies* `S` (while holding `X_i`) iff `v_i(X_i) < τ_i(S)`.
An allocation is EFX₀ iff `v_i(X_i) ≥ τ_i(X_j)` for all `i≠j`.

Running example (best near-witness, from the ledger):
`V = [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[16,40,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]]`.
It has exactly **5 EFX₀ allocations, all two-treasure**: agent 0 holds good 2, agent 3 holds good 4,
agents 1 & 2 split the rest, good 3 floats.

---

## 1. Why the 5 survivors are EFX — the slack structure (PROVEN, by direct computation)

Two elementary facts drive everything.

**Fact 1 (singleton immunity).** If `|S|=1` then `τ_i(S)=0` for every `i`; a singleton is *never*
strongly-envied. (Removing its one good leaves value 0.)

**Fact 2 (threshold monotonicity).** For `H ⊆ S` (nonneg. additive values), `τ_i(H) ≤ τ_i(S)`.
*Proof.* `v_i(H) ≤ v_i(S)` and `min_{g∈H} v_i(g) ≥ min_{g∈S} v_i(g)`; subtract. ∎

Computed slacks (own value − threshold) for the size-≥2 envied bundles of each survivor
(singleton-held bundles omitted — Fact 1 makes them slack `= own value`, never binding):

| survivor | bundles (a0,a1,a2,a3) | binding constraint | bottleneck slack |
|---|---|---|---|
| 0 | `{2} / {0,6} / {1,3,5,7} / {4}` | agent0 vs `{0,6}` (τ=16) | **4** |
| 1 | `{2,3} / {0,1} / {5,6,7} / {4}` | agent2 vs `{2,3}` (τ=59) | 2 |
| 2 | `{2} / {0,1,3} / {5,6,7} / {4}` | agent0 vs `{0,1,3}` (τ=19) | 1 |
| 3 | `{2} / {0,1} / {3,5,6,7} / {4}` | agent1 vs `{3,5,6,7}` (τ=64) | 1 |
| 4 | `{2} / {0,1} / {5,6,7} / {3,4}` | agent2 vs `{3,4}` (τ=60) | 1 |

**Observations.**
- Every binding constraint is either **treasure-holder vs a block-half** or **block-splitter vs block-splitter**.
  No constraint ever involves a singleton *as the envied bundle* (Fact 1).
- The two treasure holders (agent 0 with good 2, agent 3 with good 4) are held as singletons in
  survivors 0–3 and hence *immune*; the only reason they appear on the *envier* side is that their
  singletons are small, so they are the agents most at risk of envying a block-half.
- The single **loosest** two-treasure allocation is survivor 0, bottleneck slack **4**, binding on
  agent 0 (weakest treasure, `v_0(good2)=20`) vs agent 1's half `{0,6}` (`τ_0=27−11=16`). This is the
  "last to die": destroying *all* two-treasure allocations requires eroding ≥4 units of this slack while
  simultaneously killing the four tighter survivors — consistent with the CP-SAT result that no witness
  exists within L∞ distance 6 of `V`.
- **Floaters cost one constraint.** Survivors 1 and 4 attach the near-worthless good 3 to a treasure
  (`{2,3}`, `{3,4}`). This is *not* free: `{t,f}` has `τ_i({t,f})=max(v_i(t),v_i(f))`, so the bundle
  becomes strongly-enviable with threshold `v_i(t)` (when `f` is everyone's min good). That is exactly
  the slack-1/2 constraints agent2-vs-`{2,3}` and agent2-vs-`{3,4}`. Both singletons (survivors 0,2,3) is
  the safest shape.

---

## 2. The reduction (KEY LEMMA — PROVEN)

**Definition (two-treasure allocation).** Distinct agents `a,b` receive singletons `{t₁},{t₂}`
(`t₁≠t₂`); the other two agents `c,d` receive `H_c, H_d` with `H_c ⊍ H_d = M\{t₁,t₂}` (a full split of
the remaining block `R := M\{t₁,t₂}`).

**Lemma 1 (exact EFX₀ characterization).** A two-treasure allocation is EFX₀ **iff** all six hold:

```
(E1) v_a(t₁) ≥ τ_a(H_c)        (E2) v_a(t₁) ≥ τ_a(H_d)      [a doesn't strongly-envy a block-half]
(E3) v_b(t₂) ≥ τ_b(H_c)        (E4) v_b(t₂) ≥ τ_b(H_d)      [b doesn't strongly-envy a block-half]
(E5) v_c(H_c) ≥ τ_c(H_d)       (E6) v_d(H_d) ≥ τ_d(H_c)     [c,d 2-agent-EFX₀ on the split]
```

*Proof.* EFX₀ demands `v_i(X_i) ≥ τ_i(X_j)` for every ordered pair. Partition the constraints by the
*envied* bundle `X_j`:
- `X_j ∈ {{t₁},{t₂}}`: `τ=0` by Fact 1 — satisfied automatically (this discharges *all* envy aimed at
  `a` and `b`, in particular `a↔b` and `c,d↔` the treasures).
- `X_j = H_c`, enviers `{a,b,d}`: gives E1, E3, E6.
- `X_j = H_d`, enviers `{a,b,c}`: gives E2, E4, E5.

These are all constraints; conversely E1–E6 imply every EFX₀ inequality. ∎

**Consequence — the EFX₀ check collapses.** For the two-treasure family the *only* bundles that can be
strongly-envied are the two block-halves. The lone treasures contribute **zero** constraints as targets.
This is why the family is the natural EFX₀-refuge for 4 agents: 2 singletons + a 2-way split minimizes the
number of "fat" (strongly-enviable) bundles to exactly two, while keeping each fat bundle small
(a half-block rather than a 3-way remainder).

### 2a. Generalization to k-treasure families (PROVEN) — covers V2's 3-treasure survivors

**Definition (k-treasure allocation).** Choose `k` agents to be **singleton-holders** (each gets one
"treasure" good) and the remaining `4−k` agents to be **fat-holders** who partition the rest
`R = M\{treasures}`. `k ∈ {0,1,2,3}`.

**Lemma 1′ (general singleton-immunity reduction).** A `k`-treasure allocation is EFX₀ **iff no agent
strongly-envies any fat bundle** — i.e. `v_i(X_i) ≥ τ_i(F)` for every fat bundle `F` and observer `i`
not holding `F`. Singleton bundles impose **no** constraints as targets (Fact 1). *Proof:* identical to
Lemma 1, splitting constraints by whether the envied bundle is a singleton (τ=0) or fat. ∎

Specializations, by number of fat bundles `4−k`:
- **k=3 (one fat bundle `D`, |D| large):** 3 constraints, `v_i(t_i) ≥ τ_i(D)` for the three
  singleton-holders `i`. No split to choose — the simplest family, hence a robust escape. *This is V2's
  base:* singletons `{7},{1},{0}` to agents 0,1,2; `D={2,3,4,5,6}` to agent 3. Its 10 survivors are this
  k=3 base plus (a) the floater good 3 relocating and (b) k=2 variants where a singleton-holder absorbs one
  extra good, shrinking `D`. So V2 spans the **k=3 ↔ k=2 boundary**.
  The three k=3 constraints hold with slacks 4, 6, 6 (`v_i(t_i)`=18/20/19 vs `τ_i(D)`=14/14/13) — loosest
  is agent 0 at 4, again a small-but-positive margin.
- **k=2 (two fat halves):** Lemma 1 (six constraints). *V and V3's base.*
- **k=1 (three fat bundles):** the three fat-holders need a 3-agent-EFX₀ split of `R` (exists — CGM 2020),
  plus the lone singleton-holder must tolerate all three fat bundles (3 constraints).
- **k=0:** fully balanced; every bundle is a target.

**Which k is the tightest wall?** A larger fat bundle is *easier* to strongly-envy (bigger `τ`), so k=3
(one 5-good bundle) is comparatively *easy to block* — a counterexample readily makes the dumping-ground
bundle envied. The **hardest family to block is k=2 with a balanced split**, because each fat bundle is only
~half the block, minimizing `τ`. This is why the purest, most robust near-witness (V) is k=2, and why the
two-treasure screen (§3c) is the sharpest cheap filter. A counterexample must nonetheless block **all** k
simultaneously; the k=3 and floater checks below are additional necessary conditions.

---

## 3. Sufficient existence conditions

### 3a. Global-dominant pair (PROVEN, clean, but weak)

**Definition.** Call `(i,g)` **dominant** if `v_i(g) ≥ τ_i(M\{g})` — equivalently
`2·v_i(g) + min_{h≠g} v_i(h) ≥ v_i(M)`, i.e. `g` is worth at least ~half of `i`'s universe.

**Theorem 1.** If there exist distinct goods `t₁≠t₂` and distinct agents `a,b` with `(a,t₁)` and
`(b,t₂)` both dominant, then an EFX₀ allocation exists.

*Proof.* Give `a←{t₁}`, `b←{t₂}`; let `c,d` split `R=M\{t₁,t₂}` by any 2-agent EFX₀ allocation of `R`
(exists — see Lemma 2 below), yielding E5, E6. For any half `H ⊆ R ⊆ M\{t₁}`, Fact 2 gives
`τ_a(H) ≤ τ_a(M\{t₁}) ≤ v_a(t₁)`, i.e. E1, E2; symmetrically E3, E4. Lemma 1 ⟹ EFX₀. ∎

**Lemma 2 (2-agent EFX₀, PROVEN).** For two additive agents with positive values, any good-set admits an
EFX₀ split. *Proof sketch.* Agent `c` takes a self-EFX₀ partition `(P,Q)` of `R` (an EFX₀ split under `c`'s
own valuation — the identical-valuation case, Plaut–Roughgarden 2018 via leximin); `d` takes the half it
prefers, `c` the other. `c` is EFX₀ by self-EFX₀; `d` holds its `≥`-valued half `P`, so
`v_d(P) ≥ v_d(Q) ≥ τ_d(Q)`. ∎ *(Empirically: 0 failures in 200,000 random positive-additive instances.)*

*Empirical check of Theorem 1:* 400/400 constructed dominant-pair instances had EFX₀; the two-treasure
screen (§3c) is **sound** in 800/800 random instances (0 false positives).

### 3b. Why Theorem 1 is not tight — the R-relative frontier

`V` has **no dominant good at all** (agent 3's good 4 is the closest: `59` vs threshold `62`), yet two-treasure
EFX₀ holds. The reason: E1/E2 only require the treasure to beat the **realized block-halves** `τ_a(H)`,
not `τ_a(M\{t₁})`. When `c,d` split `R` *balanced-for-`a`*, `τ_a(H) ≈ v_a(R)/2`, so `a` needs only
`v_a(t₁) ≳ v_a(R)/2`, i.e. the treasure worth ~half of the **residual** `R` (not the whole universe `M`).
In survivor 2 this binds at slack 1: `v_0(good2)=20` vs `v_0(R)/2 = 38/2 = 19`. **The true sufficient
condition is the exact feasibility of E1–E6, not global dominance.**

### 3c. Exact screen (PROVEN sound; the practical tool)

`twotreasure.py :: two_treasure_witness(V)` (in the repo root) decides E1–E6 feasibility exactly by iterating the
6 unordered `{a,b}` role-choices × `m(m−1)` ordered treasure pairs × `2^{m−2}` splits — **~0.03 s** for
`m=8` (vs `4⁸=65536` for full enumeration). It returns a witnessing `(a,b,t₁,t₂,H_c,H_d)` or `None`.
On `V` it returns `a=0,b=3,t₁=2,t₂=4,H_c={0,1},H_d={3,5,6,7}`. **Any candidate counterexample must make this
screen return `None`** — a cheap necessary filter for the hunt.

*Completeness caveat (empirical).* Two-treasure is a **sufficient** certificate, far from complete: in
800 flat random instances (values 1–12) it certified 71, while 729 had EFX₀ via non-two-treasure
(balanced) allocations, and **0 lacked EFX₀**. Its relevance is precisely the **lumpy** near-witness regime:
for `V`, all 5 EFX₀ allocations *are* two-treasure — so there, killing two-treasure = killing EFX₀.

---

## 4. Necessary conditions on any true counterexample (new no-go constraints)

Let `V` be a 4-agent additive EFX₀ counterexample. Then all of the following must hold.

**NC-0 (screen returns None).** `two_treasure_witness(V) = None`: E1–E6 is infeasible for *every* choice of
`(a,b,t₁,t₂,split)`. (Exact, cheap, necessary.)

**NC-A (no dominant matching — PROVEN via Theorem 1 + König).** The dominant relation
`D = {(i,g) : v_i(g) ≥ τ_i(M\{g})}` contains **no matching of size 2**. Hence either **at most one agent
owns any dominant (≥ ½-universe) good**, or all dominant pairs share a single physical good. Concretely:
**at most one agent may value some single good at ≥ half of its total valuation.** *(`V` satisfies this with
`D=∅`.)*

**NC-B (residual-balanced starvation — the sharp frontier, PROVEN as the contrapositive of Lemma 1).**
For **every** ordered pair of distinct agents `(a,b)`, every `t₁≠t₂`, and the induced `c,d`, there is **no**
split `(H_c,H_d)` of `R=M\{t₁,t₂}` with

```
max(τ_a(H_c),τ_a(H_d)) ≤ v_a(t₁)  AND  max(τ_b(H_c),τ_b(H_d)) ≤ v_b(t₂)
AND  v_c(H_c) ≥ τ_c(H_d)  AND  v_d(H_d) ≥ τ_d(H_c).
```

Informally: for **every** way to pick two "anchor" goods and hand them to two agents, at least one anchor
holder strongly-envies **every** balanced-enough split of the residual (or the residual admits no
2-agent-EFX₀ split compatible with both anchors). Since a good worth `≥ v_a(R)/2` to `a` always lets `a`
tolerate a balanced split, NC-B forces, for every agent `a` and every candidate residual `R`:
`max_g v_a(g) < ½·v_a(R) + (min-good correction)` — **no agent has a good reaching half of any residual it
could anchor.** This is strictly stronger than NC-A (which uses the whole universe `M`) and is the operative
squeeze: `V` fails to be a counterexample by exactly the margins in the §1 table (loosest slack 4).

**NC-C (k=3 dumping-ground envy — PROVEN via Lemma 1′).** For **every** choice of 3 goods `t₀,t₁,t₂`
handed as singletons to 3 agents, the 4th agent's remainder `D = M\{t₀,t₁,t₂}` must be strongly-envied by
one of the three singleton-holders: `∃ i: v_i(t_i) < τ_i(D)`. (`V2` fails this — its k=3 base holds with
slacks 4/6/6.) Because `D` has 5 goods, `τ_i(D)` is large, so NC-C is comparatively *easy* to satisfy for a
witness — it is the k=2 conditions NC-0/NC-B that bind hardest.

**NC-D (floater un-parkability — PROVEN via §4.5).** For every EFX₀ base of `M\{f}` (guaranteed to exist,
Berger et al.), the good `f` must be un-parkable: every placement detonates. For a global-min `f` this forces
the base plain-envy graph to have **every bundle envied (a directed cycle)** — yet all three near-witnesses
have **envy-free** bases, so their floaters park freely. This is the sharpest structural gap between the
near-witnesses and a true counterexample.

---

## 4.5. The floater / charity-gap structure (V3) — a sharp no-go direction

V3's 4 survivors are **one base allocation** `B = ({2},{0,1},{5,6,7},{4})` on the 7 goods `M\{3}`, plus the
floater good 3 (values `[1,2,1,1]`) parked in **any** of the 4 bundles. This is exactly the ledger's
charity structure: Berger et al. (2102.10654) *guarantee* a 4-agent additive EFX₀ allocation leaving ≤1
good uncalled, so such a base always exists; a counterexample needs the uncalled good to be **un-parkable**
everywhere.

**Placement condition (PROVEN).** With base `B` EFX₀ on `M\{f}`, parking `f` in `B_i` keeps EFX₀ iff for
every observer `k≠i`:
```
v_k(B_k) ≥ v_k(B_i) + v_k(f) − min( m_{k,i}, v_k(f) ),   where m_{k,i} = min_{g∈B_i} v_k(g).
```
Equivalently, placement `i` is **detonated** by observer `k` iff
`v_k(B_k) < v_k(B_i) + max(0, v_k(f) − m_{k,i})`.

**Detonation-requires-envy (PROVEN).**
- If `v_k(f) ≤ m_{k,i}` (f is not k's cheapest good in `B_i` — the case for a genuine *charity/min* good):
  detonation `⟺ v_k(B_k) < v_k(B_i)`, i.e. **k plainly envies `B_i`.**
- If `v_k(f) > m_{k,i}`: detonation is easier by the surplus `v_k(f)−m_{k,i}` (the loophole for a
  *high-value* floater).

**No-Go Lemma (small/charity floater, PROVEN).** Let `f` be a global-minimum good
(`v_k(f) = min_g v_k(g)` for all `k`). Then `f` is a **universal detonator** (all 4 placements fail) iff in
the base every bundle is plainly envied by someone — i.e. the base **plain-envy graph has every vertex with
in-degree ≥ 1, hence contains a directed cycle.** Consequently, **if the base envy graph is acyclic (has a
source `B_i`), the floater parks safely in `B_i` and a complete EFX₀ allocation exists.**

**Check against all three near-witnesses.** The plain-envy graphs of the V, V2, V3 bases are **completely
empty** (every in-degree 0 — the bases are outright envy-free). So their floaters park anywhere; this is
*precisely* why V (5), V2 (10), V3 (4) are EFX₀ and not counterexamples. The floaters are structurally
un-detonatable.

**Is the floater system infeasible? NO — but the global constraint is the wall (PROVEN by construction).**
EFX₀ bases *with* a full plain-envy cycle **do exist** (found in <1000 random trials, e.g.
`V=[[8,10,18,12,6,12,19],[5,7,3,3,10,10,12],[6,9,7,4,7,11,20],[8,3,5,20,7,16,15]]`, base
`({6},{2,4},{0,5},{1,3})`, all bundles envied). Appending a global-min floater `[1,1,1,1]` **detonates all
4 placements of that base** — so the local charity-gap system is *feasible*, and this is **not** an
infeasibility no-go on its own. **However**, the resulting 8-good instance has **197 other EFX₀
allocations** (248 and 189 for two more such constructions). Detonating one base's placements is trivial;
it merely reshuffles the goods into a *different* EFX₀ allocation elsewhere.

**The governing tension (the real guidance).** There is a pull in opposite directions (evidence: 6 direct
data points — see caveat):
- **Few total EFX₀ allocations** (the near-witness property that makes an instance *close* to a
  counterexample) coincides here with **envy-free bases**: all three dual-verified near-witnesses (counts
  4/5/10) have base plain-envy graphs that are *completely empty*. An envy-free base has a floater-source,
  so its charity good is always placeable.
- **A detonatable floater** requires a base with a **full plain-envy cycle** — but the three such bases I
  constructed each had **~200 alternative EFX₀ allocations** (197/248/189). Injecting the envy needed to
  detonate appears to multiply the alternatives.

*Evidence caveat:* this rests on 6 hand/constructed points, not a controlled sweep. A 1200-instance random
sweep (values 1–25) produced **no** low-count instances at all — every random instance had >40 EFX₀
allocations (mean 3.76 plain-envy edges in a sampled EFX₀ allocation). Near-witnesses are far off the random
manifold and only appear under directed search, so the correlation is *suggested*, not statistically
established; a targeted sweep over annealer/CEGAR elites would be needed to confirm it.

A counterexample must achieve **both at once**: a base with a full envy cycle (every bundle envied) that is
*still* EFX₀, *and* no other complete allocation EFX₀. EFX₀ pins each envied bundle into the **thin band**
`v_k(B_i) − m_{k,i} ≤ v_k(B_k) < v_k(B_i)` (k envies `B_i`, but by less than `B_i`'s cheapest good — the
"one good thick" frontier of the ledger). Every bundle must sit in this band for some observer,
*simultaneously*, while every re-rotation of the cycle and every other partition fails EFX₀. I did **not**
find such an instance, and I did **not** prove one cannot exist — but the two requirements are in direct
empirical opposition, which is the structural reason the CP-SAT search finds nothing within L∞ 6 of V.

## 5. Guidance: can an instance break ALL two-treasure AND all balanced allocations?

This is the honest crux, and the reasoning below is **heuristic** (not proven).

Two opposing pressures act on per-agent value concentration:

- **Kill two-treasure (NC-B):** no agent's top good may reach ~half of any residual → valuations must be
  *flat* (no private peak large enough to anchor a singleton while the other two share the rest).
- **Kill balanced (2-2-2-2 and other equal splits):** the instance must be *lumpy* — some agents value a
  few goods so highly that no equal-size partition is EFX₀. Flat valuations make balanced/round-robin/MNW
  allocations EFX₀ (confirmed: 0/800 flat random instances lacked EFX₀).

These pull opposite directions on concentration, but they are **not outright contradictory** — they can be
reconciled only by **conflicting (mis-aligned) peaks**: every agent concentrates value, but on *overlapping*
goods, so (i) no single good is a *private* half-treasure for one agent that the others don't also want
(defeats the clean anchor, satisfying NC-B), yet (ii) the contested peaks make every equal split leave some
agent strongly-envying another's share (defeats balanced). `V` sits right on this seam: agents 1,2,3 all
value goods 4 and 6 highly (60/60, 46/17, 59/…), goods 2 is agent 0's and agent 2's peak — heavy overlap —
while no agent clears the half-of-residual bar. The window is **narrow**: the CP-SAT no-witness ball of
radius 6 around `V` and the slack-4 loosest survivor say `V` is close to, but on the wrong side of, that seam.

**Assessment of feasibility.** I did **not** find a proof that the window is empty (no full m=8 nonexistence
proof follows from this family alone — two-treasure is only one EFX₀ certificate; a counterexample must also
defeat balanced, 3-treasure, and every other allocation). But the pressures are genuinely opposed, which is
consistent with the difficulty of the hunt. The concrete, actionable output is **NC-B as a search
constraint**: seed the search toward instances with maximally **conflicting peaks** (all four agents' top
1–2 goods coinciding) and enforce, per agent, `max_g v_a(g) < ½ v_a(M\{peak-pair})`, then let the solver
also break balanced. If NC-B and "balanced fails" ever prove jointly infeasible for m=8, that would be a
nonexistence proof; I could not close that here.

---

### Reproduction
- Screen: `twotreasure.py` (repo root; sound decision of E1–E6; ~0.03 s at m=8).
- Slack table & robustness: recomputed via `from verify import precompute` on `V`.
- Envy graphs / floater detonation for V, V2, V3: all three bases have empty plain-envy graphs; all 4
  placements SAFE. EFX₀ bases *with* full envy cycles exist and their global-min floater detonates all 4
  placements, yet the 8-good instance keeps 197/248/189 other EFX₀ allocations.
- Empirical: 2-agent EFX₀ 200k/200k; Theorem 1 400/400; screen soundness 800/800; flat-random EFX₀ 800/800;
  random sweep (1200 inst, values 1–25) — all had >40 EFX₀ allocations (near-witnesses are off the random
  manifold, only reachable by directed search).
