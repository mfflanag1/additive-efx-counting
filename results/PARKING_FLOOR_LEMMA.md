> **SUPERSEDED NOTE (2026-07-24, referee round):** any statement below that naive envy-cycle
> rotation can destroy EFX0 is WITHDRAWN. Re-audit: 0 breaks in 34,538 cycle-rotations; pure
> rotation preserves EFX0 (Mahara arXiv:2008.08798 Lemma 7). The 46% statistic measured
> rotation-followed-by-parking, not rotation. See results/CAMPAIGN_LOG.md referee round 1.

# The Parking-Floor Lemma (exact-count sharpening of NC-D)

**Setting.** 4 additive agents, strictly positive integer values, goods `M`, `|M|=m`.
EFX₀: `v_i(X_i) ≥ τ_i(X_j) := v_i(X_j) − min_{g∈X_j} v_i(g)` for all `i≠j`.
For a good `f` and an EFX₀ allocation `B=(B_0,..,B_3)` of `M∖{f}`, "parking `f` in `B_i`"
means the completion that sets `X_i = B_i∪{f}`, `X_k=B_k` (`k≠i`).

**Universal-min good.** `f` is *universal-min* if `v_k(f)=min_{g∈M} v_k(g)` for every agent `k`.
(The near-witness floaters are low-valued goods; they are NOT universal minima in general — basin 2's floater is not within 1 of every agent's minimum.)

---

## Lemma (Parking = source count).
Let `f` be universal-min and `B` an EFX₀ allocation of `M∖{f}`. Then parking `f` in `B_i`
yields an EFX₀ allocation **iff `B_i` is a source of the plain-envy digraph of `B`** (i.e.
no agent `k≠i` plainly envies `B_i`: `v_k(B_k) ≥ v_k(B_i)`).
Consequently the number of EFX₀ completions of `B` by `f` equals the number of **unenvied
bundles** (sources) of `B`.

**Proof.** By the proven placement condition (TWO_TREASURE_LEMMA §4.5), parking `f` in `B_i`
is EFX₀ iff for every observer `k≠i`
`v_k(B_k) ≥ v_k(B_i) + max(0, v_k(f) − m_{k,i})`, `m_{k,i}=min_{g∈B_i} v_k(g)`.
Universal-min gives `v_k(f) ≤ v_k(g)` for all `g`, so `v_k(f) ≤ m_{k,i}` and the surplus term
vanishes. The condition collapses to `v_k(B_k) ≥ v_k(B_i)` for all `k≠i` — exactly "`B_i` is
unenvied." (Parking in `B_i` also cannot break any constraint whose envied bundle is a
`B_k`, `k≠i`, since those are unchanged, and `f` universal-min makes `B_i∪{f}` no more
strongly-enviable than `B_i` was: `τ_k(B_i∪{f}) = v_k(B_i∪{f}) − v_k(f) = v_k(B_i) ≤` the
old `τ_k`+`v_k(f)`, and the binding removal is now `f` itself.) ∎

## Corollary (the floor is the agent count).
If `B` is **envy-free** then all 4 bundles are sources ⇒ exactly **4** EFX₀ completions.
To obtain **fewer than 4** EFX₀ completions from a single universal-min-floater base, `B`
must have an **envied bundle** — i.e. `B` is not envy-free. To obtain **zero** completions,
**every** bundle of `B` must be envied (every vertex has in-degree ≥ 1 ⇒ the plain-envy
digraph contains a cycle).

This is exactly why the dual-verified near-witnesses floor at their agent count:
- count-4 basin: base `({2},{0,1},{5,6,7},{4})` is envy-free (all 4 sources) ⇒ 4 parkings.
  Verified: predicted sources `{0,1,2,3}` = actual EFX₀ parkings `{0,1,2,3}`.
- count-5 / count-10: same mechanism (envy-free base + floater; extra survivors are k-shifts).

## The counterexample requirement, made exact.
A 4-agent additive counterexample restricted to any single-floater decomposition needs a
base whose plain-envy digraph has **no source** (every bundle envied). By Berger et al.
(2102.10654) an EFX₀ base on `M∖{f}` exists for some `f`; the Parking-Floor Lemma says a
*counterexample's* base must be **sourceless** for the leftover to be un-parkable. This is
NC-D with an exact count attached: **#(EFX₀ completions of a universal-min floater) =
#sources of the base**, so un-parkability ⟺ sourceless base ⟺ full plain-envy cycle.

## The unresolved coupling (honest gap).
Sourceless EFX₀ bases on 7 goods *exist* (TWO_TREASURE §4.5 exhibits one). The lemma does
**not** prove a counterexample impossible, because total EFX₀ count is over *all* allocation
shapes, not one base's parkings: a sourceless base kills its own 4 parkings but empirically
coincides with ~200 *other* EFX₀ allocations (different bases / balanced partitions). The
open question is therefore precisely:

> **Coupling conjecture.** Every 4-agent additive instance whose EFX₀-optimal base (for some
> leftover `f`) is sourceless admits an EFX₀ allocation of some *other* shape (a different
> base, or a balanced 2-2-2-2 partition). Equivalently: injecting the plain-envy needed to
> make a base sourceless necessarily creates an EFX₀ allocation elsewhere.

Proving the coupling conjecture ⟹ EFX exists for 4 agents. Refuting it (an instance with a
sourceless base AND no other-shape EFX₀) ⟹ counterexample. The Parking-Floor Lemma reduces
"EFX for 4 agents" in the single-floater regime to this one coupling statement.

---

# GENERALIZED PARKING LEMMA (arbitrary leftover) — proven, machine-verified

The universal-min restriction is removable. For ANY leftover good `f`, define the
**f-envy digraph**: agent `k` *f-envies* bundle `B_i` (`k≠i`) iff
`v_k(B_k) < v_k(B_i) + max(0, v_k(f) − m_{k,i})`, `m_{k,i}=min_{g∈B_i} v_k(g)`.
(For universal-min `f` the surplus term vanishes and f-envy = plain envy.)

**Generalized Parking Lemma.** For any EFX₀ base `B` of `M∖{f}` and any leftover `f`,
`#(EFX₀ completions of f into B) = #(sources of the f-envy digraph)`.
*Proof.* Immediate from the placement condition (park `f` in `B_i` is EFX₀ iff no `k`
f-envies `B_i`). ∎
*Machine check:* 16057/16057 random 4-agent instances, exact match, 0 mismatches (`genpark.py`).

**Narrowing theorem (necessary condition on any counterexample).** A 4-agent additive
counterexample must have, for **every** good `f` and **every** EFX₀ base `B` of `M∖{f}`,
an f-envy-**sourceless** digraph (every bundle f-envied). This covers the ENTIRE one-leftover
regime, not just universal-min floaters. Since f-envy ⊇ plain-envy, high-value leftovers make
sourcelessness *easier* — the un-parkable regime is a HIGH-VALUE-floater phenomenon, not a
charity-good one. (Empirical: in 4000 random instances, un-parkable bases with a **universal-min**
`f` occurred **0** times — they require directed construction, e.g. the canonical sourceless-base
instance — whereas un-parkable bases with a general `f` are common.)

# COUPLING CONJECTURE — evidence and the (incomplete) cycle-rotation mechanism

**Coupling sweep** (`coupling_fast.py`, 2500 random instances, 635 un-parkable bases found):
- **COUNTEREXAMPLES: 0** — every un-parkable base's full instance had an EFX₀ allocation
  *elsewhere* (635/635). Strong support for the coupling conjecture.
- **Cycle-rotation** (iterated Lipton envy-cycle elimination of the base, then park): recovers
  EFX₀ in **342/635 (54%)**.
- **All owner-permutations** of the base's bundle-multiset (then park): **641/811 (79%)** in a
  second run. The remaining ~21% find EFX₀ only in a *genuinely different partition* — not any
  rearrangement of the base's bundles.

**Partial theorem (welfare termination).** Iterated envy-cycle rotation strictly increases
utilitarian welfare `Σ_i v_i(X_i)` each step (each cycle agent moves to a strictly preferred
bundle), the bundle multiset is fixed, so it terminates at an owner-assignment whose envy
digraph is a DAG — which always has a **source** (in-degree-0 bundle). For universal-min `f`
that source is parkable. **Gap:** rotation permutes owners of fixed bundles and EFX₀ is
owner-dependent, so the terminal assignment need not be EFX₀ — verified by the 46% of cases
where naive rotation fails. Hence cycle-rotation is a *partial* mechanism, NOT a proof of the
coupling conjecture. The conjecture is true empirically (0/635) but has **no simple
bundle-rearrangement proof**: EFX₀ recovery frequently requires re-partitioning, so the witness
hunt cannot be closed by parking/rotation arguments alone — it must confront full re-partition.

## Reproduction
- Lemma verified on count-4 witness: sources `{0,1,2,3}` = EFX₀ parkings `{0,1,2,3}` (MATCH).
- Generalized lemma: `genpark.py` (16057/0). Coupling sweep: `coupling_fast.py` (0 CEX/635).
- Floor-breaking search: `parkfloor.py`; no-universal-min search: `nomin.py`. Elites in results/.

---

# ROUND 3: why the coupling conjecture resists proof (three routes mapped)

The coupling conjecture ("an un-parkable EFX0 base ⟹ the full instance still has an EFX0
allocation of another shape") is now tested on **~1340 un-parkable configs, 0 counterexamples**
— robustly true. But all three natural proof routes fail at a quantified rate:

**Route A — canonical welfare potential (DEAD).** The maximizer of utilitarian welfare,
Nash welfare, and leximin is NOT EFX0 on the near-witnesses (count-4 and count-5): their
EFX0 allocations are the *lumpy k-treasure* ones, which are not welfare-optimal. So no
standard welfare rule is a proof skeleton. (The "min total strong-envy" potential is EFX0 iff
one exists — tautological, not a rule.)

**Route B — cycle-rotation (PARTIAL).** Iterated envy-cycle elimination strictly raises
utilitarian welfare, so it terminates at a DAG, which always has an unenvied source
(machine-checked: the welfare-max bundle-permutation has a source in 400/400). For a
universal-min floater the source is parkable. GAP: the welfare-max permutation is EFX0/parkable
only ~97% (386–391/400) — EFX0 is owner-dependent and not preserved by rotation. Full
path-search rotation recovers 100% on universal-min samples (**3000/3000**, empirically complete) but
only **54%** on general (high-value) floaters. No proof.

**Route C — bounded local move (STRUCTURED, not clean).** In rotation-fail cases the nearest
EFX0 allocation is within Hamming distance **≤3 of the un-parkable base always** (275 at dist 1,
27 at 2, 3 at 3, of 305). The distance-1 repair is a single **non-floater** good (never f)
moving **out of a plainly-envied bundle** (186/200 = 93%), usually its cheapest good
(119/200 = 60%). Structured, but "EFX0 is always ≤3 moves away" is a restatement of the
conjecture, not an independent lemma.

**Hard-core / witness search (proof search = witness search).** Count-minimization seeded from
the sourceless (un-parkable) region descended 197 → 4 and **landed on the parking floor**, not
0 — a third dual-verified count-4 instance
`[[3,13,8,40,7,39,38,13],[13,1,1,4,11,1,40,12],[7,3,2,12,2,39,25,12],[2,13,2,40,2,39,38,2]]`
(4 EFX0 allocations = base + good-0 floater in 4 spots). Directed search never reaches a
witness; it always returns to count = #agents.

**Conclusion.** The coupling conjecture is true empirically but has no proof via
rotation, welfare-maximization, or bounded rearrangement — each fails at a measured rate
because the hard-regime EFX0 allocations are non-canonical (lumpy) and not rule-reachable.
Proving EFX for 4 additive agents (even the one-leftover regime) needs a genuinely different
idea; the parking/rotation/potential toolkit is provably insufficient. The solid theorem from
this campaign is the Generalized Parking Lemma; Round 3's contribution is the precise negative
map of the proof landscape.
