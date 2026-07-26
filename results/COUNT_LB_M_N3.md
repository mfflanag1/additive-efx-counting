# Counting EFX Lower Bound at m = n+3  (target n=4, m=7)

**Goal.** Extend Neoh–Teh (AAAI 2025, *Understanding EFX Allocations: Counting and
Variants*) Theorem 3.8 — "when m = n+2, every instance has ≥ n EFX allocations" — to the
open cell m = n+3, first for n = 4 (m = 7). At (4,7) EFX existence is guaranteed (Mahara,
m ≤ n+3), so "every (4,7) instance has ≥ 4 EFX₀ allocations" is well-posed and open
(Neoh–Teh Table 1 lists NO lower bound at m ≥ n+3).

Counts are of EFX₀ allocations (allow dropping any good, incl. zero-valued). For the
all-positive instances used in the tight examples EFX₀ = EFX+.

**Verifier.** `fast47.Counter(4,7).count` — exact full enumeration of 4⁷ = 16384
assignments — cross-checked against `fast_verify.count_efx0` (200/200 agree), itself
validated against the pure-Python reference `verify.enumerate_all`.

---

## VERDICT

- **Empirical (strong):** the minimum number of EFX₀ allocations over (4,7) instances is
  **exactly 4 = n**. No instance with < 4 was found across thousands of random and
  directed-adversarial (count-minimizing) instances; the annealer that pins the floor at
  4 for (4,8),(4,9),(4,10) also pins it at 4 for (4,7). This is consistent with — and new
  evidence for — Conjecture 6.1 at m = n+3.
- **Not proven:** a rigorous unconditional proof of "≥ 4" at (4,7). The cell remains open.
- **Rigorous conditional result:** every (4,7) instance possessing an *envy-free 3111
  base* has ≥ 4 EFX₀ allocations (parking-floor lemma, below). Every count-exactly-4
  instance found is of this form.
- **Named obstruction (the answer to "which step of Thm 3.8 breaks"):** see §2. In one
  line: the leftover pool grows from 3 to 4 goods, forcing the constructive step
  (Algorithm 1 / Lemma 3.9) to build a size-3-or-4 winner bundle whose EFX-safety would
  require every other agent to beat *three* pool goods, but envy-cycle elimination only
  certifies non-envy of a *two*-good virtual bundle. The counting layer (Lemma 3.11–3.12)
  does NOT break at the floor (§3).

---

## 1. Reconstruction of the Neoh–Teh m = n+2 argument

The bound "≥ n at m = n+2" is proved constructively via a **join-graph**.

**Algorithm 1.** Order agents 1..n. For i = 1..n−1, agent i greedily takes its favourite
remaining good (a singleton). This leaves a pool **P of exactly 3 goods** and agent n
empty. Create two *virtual goods* s, l with, for every observer i,
v_i(s) = min_{g∈P} v_i(g), v_i(l) = v_i(P) − v_i(s) (so s ≈ "cheapest single good of P",
l ≈ "top two goods of P"). Give l to agent n (State 1); envy-cycle-eliminate and give s to
the resulting non-envied agent (State 2); realize the virtual goods.

Why State 1 is EFX (this is the load-bearing step): the l-holder's realized bundle is 2
goods; removing its cheaper good leaves **1 good**, and every singleton-holder greedily
preferred its own good to every single good of P. Why adding s (→ a 3-good winner) stays
EFX: after envy-cycle elimination the winner's 2-good bundle l is **fully non-envied**, so
every other agent's bundle is worth ≥ v(l) = the top *two* goods of P; hence after the
winner absorbs the 3rd pool good, dropping the winner's least good still leaves ≤ 2 pool
goods, which every agent already beats. **The "beat two pool goods" guarantee comes for
free from non-envy of a two-good virtual good.**

**Lemma 3.9 (dichotomy).** For each agent i there is an EFX allocation, everyone ≥ 1 good,
with either (1) i gets 3 goods, or (2) i and some j each get 2 goods and one of {i,j} gets
its favourite in A_i∪A_j. These are the two partitions of n+2 into n positive parts:
`3·1^(n-1)` and `2·2·1^(n-2)`.

**Def 3.10 / Lemma 3.11 / Lemma 3.12 (counting).** Build a directed graph on agents:
self-loop (i,i) = an EFX alloc where i gets 3 goods; edge (i,j) = an EFX alloc where i,j
get 2 goods each and j gets its favourite. Distinct edges ⇒ distinct allocations (≥ |E|),
and every connected component has |E_x| ≥ |N_x| (Lemma 3.9 gives every agent an incident
edge; a virtual-good + envy-path argument rules out a source), so |E| ≥ n ⇒ ≥ n EFX.

---

## 2. The named obstruction at m = n+3   (which step breaks)

After the n−1 greedy singletons the pool **P has 4 goods** (not 3). The floor shapes are
the partitions of n+3 into n positive parts: `4·1^(n-1)` (4111), `3·2·1^(n-2)` (3211),
`2·2·2·1^(n-3)` (2221).

**(O1) The constructive step — Lemma 3.9 / Algorithm 1 — breaks.** To realize the floor
shapes 4111 and 3211 the winning agent must hold a bundle worth **3 pool goods** (all of P
minus one). EFX-safety of that winner requires every *other* agent's bundle to beat the
top-*three* goods of the pool. But the only non-envy certificate the envy-cycle machinery
produces is for a **two**-good virtual good l (as at m = n+2); there is no mechanism to
force every agent to beat three pool goods. Concretely:

- *State-1 break.* If one gives the empty agent l = "top-3 of P" (3 goods), removing its
  cheapest leaves **2 goods**, which a singleton-holder need not beat — EFX fails already
  at State 1. Demonstrated on the explicit instance in `results/` notes: agent-1 owns a
  good worth 10 but the winner's post-removal 2-good bundle is worth 18 → strong envy.
- *Whole-algorithm break.* The naive m=n+3 analog (n greedy singletons; place the top-2
  virtual then the remainder onto endowed agents) produces an EFX₀ allocation in only
  **325/5000 ≈ 6.5%** of random (4,7) instances, versus **4893/5000 ≈ 98%** for the
  genuine Algorithm 1 at (4,6) (`algo1.py`; the 2% miss at (4,6) is our simplified
  envy-cycle proxy, not the algorithm). The construction, not the bookkeeping, is what
  fails.

**(O2) A new hyperedge shape appears — but does NOT bind at the floor.** 2221 is an
*unordered triple* of 2-good agents, a 3-uniform hyperedge that the graph cycle-count of
Lemma 3.11–3.12 cannot absorb. However, §3 shows empirically that **2221 is never needed
at the floor**: every low-count instance is fully covered by the graph on {4111, 3211}
alone. So the counting layer is fine; the obstruction is entirely (O1), the construction.

---

## 3. Empirical structure of the floor at (4,7)

All figures from exact enumeration (`fast47`, `shape_analysis`, `tight_shapes.py`,
`hunt47.py`).

**Floor = 4, no sub-4.** Directed count-minimization (`hunt47.py`, 10 annealing seeds,
mixed random / near-witness starts) bottoms out at **4** with no instance below 4. A
20 000-instance random sweep bottoms out far higher (min 26); the floor is a
directed-search phenomenon, exactly as at (4,8)–(4,10).

**Tight instances are parking-floor instances.** Every count-exactly-4 instance found
(35/35 in one directed batch; more in the larger batch) has the identical shape multiset

> **3 × (3211)  +  1 × (4111)**,

whose join-graph is a **star with a self-loop at the hub**: a single "rich" agent h holds
a 3-good bundle, one good f is a *floater*, and f parks into each of the 4 agents — at the
hub → 4111 (self-loop (h,h)), at each of the other three → 3211 (edges (h,·)). |E| = 4 = n.
The shared-hub property (the 4111's 4-agent equals the common 3-agent of all three 3211s)
was verified on **66/66** distinct count-4 instances across two directed batches — every
one is a single-floater parking, none deviates.
Verified on the explicit instance
`[[30,66,69,9,21,19,63],[12,56,58,9,10,24,52],[12,33,45,20,24,8,64],[11,60,1,18,2,6,41]]`:
its 4 EFX₀ allocations are the base `a0={0,4,5}, a1={2}, a2={6}, a3={1}` (envy-free on the
6 goods {0,1,2,4,5,6}) with floater good 3 parked at each agent.

**2221 is never essential at the floor.** Over 76 low-count (≤ 6) directed instances:
0 instances below 4; 0 count-4 instances whose 4 allocations include a 2221; **0 instances
whose {4111,3211}-graph has fewer than 4 edges.** Shape-combo census:
- count 4:  35 × (3×3211 + 1×4111)
- count 5:  12 × (4×3211 + 1×4111),  1 × (3×3211 + 2×4111)
- count 6:  21 × (4×3211 + 2×4111),  7 × (5×3211 + 1×4111)

(2221 allocations are abundant in *high*-count/flat instances — random instances often
have 100+ EFX₀ allocations *all* of shape 2221 — but such instances are nowhere near the
floor. The lower-bound proof only needs the floor, where 2221 is inert.)

---

## 4. Rigorous conditional result and the reduced open crux

**Proposition (parking floor; rigorous).** Let I be a (4,7) instance. Suppose there is a
good f such that I∖{f} (a (4,6) = n+2 instance) has an EFX₀ allocation B that is
**envy-free** (every agent weakly prefers its own bundle). Then f parks into each of the n
agents keeping EFX₀ (each agent is a source of B's f-envy digraph), yielding **n = 4
distinct EFX₀ allocations** of I. *(This is the campaign's machine-verified Generalized
Parking Lemma; here it is exact because an envy-free base has all n agents as sources.)*

Every count-4 instance we found satisfies the hypothesis. So the entire open gap for a
full proof of "≥ 4 at (4,7)" is the single constructive claim:

> **Crux (open, empirically true).** Every (4,7) instance has an EFX₀ allocation whose
> join-graph (on shapes {4111, 3211}) has ≥ 4 edges — equivalently, one can always realize
> the star-with-self-loop structure of §3. This is exactly a Lemma-3.9 analog: every agent
> is incident to a 4111 or 3211 EFX₀ certificate. Proving it requires an EFX-preserving
> placement of a 3-good winner bundle at m = n+3 — the step that (O1) shows fails for the
> naive virtual-good construction.

A sufficient (and empirically always-available) special case that IS provable: whenever
some good f and an envy-free 3111 base exist, the Proposition closes it. The missing
lemma is that such a base always exists (or that, when it does not, ≥ 4 EFX₀ allocations
arise anyway — the annealer never falsifies this).

---

## 5. FALSE-BY-TEST (recorded to prevent re-derivation)

- **Parking-lifting bound `#EFX₀(I) ≥ #EFX₀(I∖{f})` for a universal-min good f is FALSE.**
  Counterexample from a directed search that clamps good 0 to be universal-min:
  `[[0,4,39,23,12,0,5],[0,7,24,36,34,5,0],[0,0,0,6,35,20,9],[0,9,35,34,32,21,8]]` has
  #EFX₀(I) = 5 but #EFX₀(I∖{good0}) = 12. Adding the universal-min good back can *reduce*
  the count. (Random universal-min instances show 0 violations, which is why the false
  bound looks true unless attacked adversarially — matches the campaign's finding that the
  single-floater parking toolkit is insufficient on its own.)

## Artifacts
`fast47.py` (fast exact counter + allocation enumerator), `shape_analysis.py`,
`hunt47.py` (floor search), `tight_shapes.py` (shape census), `algo1.py` (Algorithm-1
implementation + naive n+3 variant locating the break), `lifting_test.py`
(falsified parking-lifting bound).

---

# v2 (2026-07-24): the reduced crux is FALSE — the proof needs a dichotomy

**Correction (FALSE-BY-TEST).** §4 above reduced the open case to a single crux
("every (4,7) instance admits an envy-free 3111 base / a ≥4-edge {4111,3211} join-graph")
and called it "empirically always true." That is **wrong**. Counterexample: the **all-ones
instance** (every v_i(g)=1) has **no** envy-free base of any 6 goods (a singleton-holder
always plainly envies the 3-good bundle, 3 > 1) yet has **2520 EFX₀ allocations** — all of
shape 2221. A second, structured no-base witness (4 distinct rows, per-agent spread ≥ 4)
`[[6,2,2,2,2,2,1],[5,1,1,1,1,1,5],[1,1,1,1,1,1,6],[1,1,1,1,1,1,5]]` has **130** EFX₀
(30×2221 + 100×3211). So base-existence is NOT necessary for a large count; the crux as
stated is refuted. (Both checked with `dichotomy.py` + exact enumeration.)

**The correct shape of an unconditional proof is a DICHOTOMY on base-existence:**

- **Arm (a) — a base exists ⇒ ≥ n (RIGOROUS).**
  *If there is a universal-minimum good f (v_i(f)=min_g v_i(g) for every i) and I∖{f} has
  an envy-free EFX₀ allocation B (a "base", shape 3111 or 2211), then all n parkings of f
  are EFX₀, so there are ≥ n EFX₀ allocations.* Proof: for observer k and host i, f is k's
  least-valued good in B_i∪{f}, so removing it gives tau0 = v_k(B_i) ≤ v_k(B_k) (envy-free)
  — no strong envy. Validated: on a constructed envy-free-base + universal-min instance all
  4 parkings are EFX₀ (`dichotomy.py` companion check). This is the campaign's Generalized
  Parking Lemma specialised to an envy-free base. (The tight witnesses of §3 satisfy a
  weaker *per-observer* version — their floater is not universal-min but is still each
  observer's least concern in every host bundle — and likewise park n ways.)

- **Arm (b) — no base ⇒ ≥ n (OPEN; "abundance"). The split aligns with the count.**
  Exact tabulation of base-status against EFX₀ count (`dichotomy.py`/`fast_base.py`):
  **every instance of count 4 or 5 has an envy-free base** (so Arm (a) covers all tight
  instances), and **no-base instances have count ≥ 6** — a directed count-minimiser
  constrained to the no-base class bottoms out at **6**, e.g.
  `[[0,0,19,20,3,8,6],[8,6,20,22,3,3,6],[19,7,17,0,5,8,0],[20,8,16,12,5,2,2]]`
  (count 6, verified no-base, shapes 4·3211+2·4111). Across 24 000 *random* instances, every
  one with count ≤ 30 had a base — low-count no-base instances only appear under directed
  (adversarial) search. So the margin for Arm (b) is comfortable (≥ 6 > 4), but the bound
  itself is still unproven. The abundance is **shape-varied**: all-ones → 2520 pure-2221;
  the structured witness → 130 = 30·2221+100·3211; the count-6 witness → 3211+4111; the
  count-12 witness (`[[3,0,0,0,1,0,3],…]`) → 12 pure-4111. So a single-shape (e.g.
  "count the 2221 allocations") argument will NOT close Arm (b); the conjectured mechanism
  is the softer **no envy-free base ⇒ no agent can hoard a 3-good bundle without envy ⇒
  "flat-like" ⇒ balanced/large-bundle allocations are EFX-abundant.** Concrete sub-target
  (turns the bounded solver run into a two-case proof): *no envy-free base ⇒ count ≥ 4 for
  values ≤ K*, by hand for small K, paired with Arm (a).

**Backstop.** The counting-CEGAR has exactly verified **every (4,7) instance with values ≤ 4
has ≥ 4 EFX₀** (pool 1295); K=6 running. Combined with Arm (a) this gives a solver-backed
proof of the bounded statement; a hand proof of Arm (b) for values ≤ K would make it
solver-free.

**Binary (K=1) is the easiest sub-case — enormous abundance margin.** No-base binary
instances exist but are extremely flat: over 4000 random binary (4,7) instances the 6 that
were no-base had **min count 244** (≫ 4). Mechanism: a binary no-base instance forces many
**universally-worthless goods** (valued 0 by every agent), each freely placeable without
affecting EFX₀, multiplying the count combinatorially — e.g. the no-base witness
`[[0,0,1,1,0,0,0],[0,0,0,0,1,0,0],[0,0,1,1,1,0,0],[0,0,1,1,0,0,0]]` has 4 universally-0
goods. So "no envy-free base ⇒ ≥ 4" for K=1 holds with a margin of ~60×; a hand proof would
formalise "no-base ⇒ ≥ (a universally-worthless good count) ⇒ combinatorial abundance."

Added artifacts: `dichotomy.py` (envy-free-base detector + dichotomy checks),
`nobase_hunt.py` (min-count search over no-base instances).
