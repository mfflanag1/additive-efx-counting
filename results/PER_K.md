> **SUPERSEDED NOTE (2026-07-24, referee round):** claims below that identical/flat valuations
> imply shape 2222 are WITHDRAWN. Counterexample: four identical rows [100,1,1,1,1,1,1,1] admit
> 2,520 EFX0 allocations, all of shape 3221. Identical valuations are EFX-safe (Plaut-Roughgarden
> leximin) but not via 2222.

# The Per-k Feasibility Program for (4,8)

Builds on `MAHARA_EXTENSION.md` (five-shape reduction) and theory2's `RESIDUAL_ATTACK.md`
(contested-good ladder: sole EFX₀ shape tracks `k` = #universally-contested goods; each `k∈{0,1,2,3}`
individually necessary). Notation: `τ_i(S)=v_i(S)−min_{g∈S}v_i(g)`; strong envy `v_i(X_i)<τ_i(S)`; all
values positive ⇒ EFX₀≡EFX₊. Singleton bundles are strong-envy-immune (Lemma 1′).

**Proof obligation (equivalent to "(4,8) is EFX-safe"):** for the treasure-count `k` dictated by the
instance, the `k`-treasure shape is feasible — for all four `k`. Proven pieces are labelled **[PROVEN]**;
everything else is **[OPEN]** or **[HEURISTIC]** and the honest scope is stated in §6.

---

## 1. An instance-computable `k` (definition + validation) [PROVEN definition; HEURISTIC that it forces the shape]

For good `g` let its **floor** be `φ(g) = min_i v_i(g)` (how much the *least*-interested agent values it).
Sort floors `φ_(1) ≥ φ_(2) ≥ … ≥ φ_(8)`.

> **Definition (contested count).** `k(V) =` the **first** index `i` (from the top) with
> `φ_(i)/φ_(i+1) ≥ θ` (a multiplicative gap), else `0`. Threshold `θ=2` used below. The `k` contested
> goods are the `k` highest-floor goods.

*Rationale:* a good all four agents value highly (large floor) is one every agent "fights over"; a large
gap separates the contested tier from the rest.

**Validation — and a FAILURE that reshapes the program.**
- theory2's five sole-shape witnesses: `k(V)` = the shape's treasure count `0/1/2/2/3`. ✓ (the *first*-gap
  rule is essential; *largest*-gap misreads `4211` as `k=4`.) Generators match: `k=1:781/781, 2:5/5,
  3:1500/1500`.
- **BUT `k` FAILS on the actual near-witnesses (tested — do not claim otherwise):**
  `k(V)=4`, `k(V3)=4` (floors `[20,16,10,8,4,1,1,1]`, first gap `8/4` ⇒ 4 — a *nonsensical* count, there is
  no 4-treasure shape), and `k(V2)=1` (whereas V2's EFX₀ shapes are `4211`/`5111`, i.e. `k=2,3`). So the
  floor definition is **wrong exactly on the instances the campaign cares about.**

**Why (the load-bearing correction).** The floor `φ(g)=min_i v_i(g)` measures **universal** contest — a good
high for *all four* agents. But a **treasure** need only be high for the *one* agent who holds it as a
singleton. V's treasures (good 2 for agent 0, good 4 for agent 3) are **misaligned**: good 4 is `60,59` for
agents 2,3 but only `4` for agent 0, so `φ(good4)=4` — floor calls it a *tail*. No good in V is high for all
four, so V has *no* high-floor good, yet it is a genuine `2`-treasure instance. **Conclusion: theory2's
contested-good ladder and this floor-`k` are defined for the ALIGNED (universally-contested) regime; the
real near-witnesses are MISALIGNED and carry no well-defined `k`.** V/V2/V3 each span several shapes
(`{4211,3221,3311}` for V) with no unique treasure count. Alignment is a **second axis** the ladder does not
capture, and the "prove the ladder is a clean partition" sub-goal is therefore **not achievable as stated** —
misaligned instances are not partitioned by `k`.

**Salvage.** The instance-computable object that *does* generalize is the direct one: `k_min(V) =` the
minimum number of singletons over all EFX₀ allocations (`= 4 − max #bundles of size ≥2`), computed from
`efx0_shapes`. This is exact but not a "floor count"; it is `1` for V (a `3221` exists), matching that V's
cheapest certificate is one treasure. The floor-`k` is a valid regime label **only when the instance is
aligned** (some good has floor `≥ θ·`next); when no good clears the floor gap, the instance is misaligned
and the per-`k` program below applies per *shape*, not per floor-count.

---

## 2. Cross-cutting tool: the Peeling Theorem [PROVEN]

> **Peeling Theorem.** If some agent `a` has a good `t` with `v_a(t) ≥ τ_a(M\{t})` (a **dominant** good),
> then the (4,·) instance admits an EFX₀ allocation.

*Proof.* Allocate `{t}→a`. On `M\{t}` the other three agents (additive) get an EFX₀ allocation by **CGM
(3 agents, any #goods)**. Check: (i) for any bundle `B ⊆ M\{t}` held by another agent,
`τ_a(B) ≤ τ_a(M\{t}) ≤ v_a(t)=v_a(X_a)` (Fact 2 + hypothesis) — `a` never strongly-envies; (ii) the other
three don't strongly-envy `{t}` (singleton-immune); (iii) they are mutually EFX₀ by CGM. ∎

*(Confirmed: 1500/1500 constructed dominant-good instances are EFX₀.)* This is the standard "peel a
satisfied agent, recurse to `n−1`" reduction; stated here because it **covers every instance with a
dominant good, at any `k`**, and it produces whatever shape CGM picks (`1 + {shape of 7 goods over 3
agents}`). **Corollary — strengthened NC-A:** a `(4,8)` counterexample has **no dominant good at all**
(not merely no dominant *pair*): `∀ i,g: v_i(g) < v_i(M) − v_i(g) − min_{h≠g}v_i(h)`.

---

## 3. k=0 — no contested good ⇒ 2222 [PROVEN for near-identical; OPEN in general]

- **[PROVEN]** Identical valuations admit an EFX₀ `2222` allocation (Plaut–Roughgarden leximin on the
  4-way equal-size partition; for identical `v`, a leximin 2-2-2-2 split is EFX₀). Ladder Theorem 2
  (`TWO_TREASURE §2a`) extends this to the flat/`ρ≤2` regime.
- **[OPEN]** General `k=0`: theory2 exhibits **sole-2222** witnesses that are *not* trivially flat
  (e.g. `[[12,6,10,7,7,11,11,3],…]`, 2004 EFX₀ allocations all `2222`), so `2222`-feasibility for arbitrary
  low-contest instances is a genuine 4-way generalization of 2-agent EFX₀ and is **not** closed here. The
  clean sufficient condition is: some equal 4×2 partition has every agent's larger good in its own bundle
  ≥ every other bundle's larger good — a 4-dimensional matching/rounding statement.

## 4. k=3 — three contested goods ⇒ 5111 [PROVEN under the exact per-agent condition]

> **k=3 Theorem.** If there are three goods `T={t₁,t₂,t₃}` with, for **every** agent `i`,
> `min_{t∈T} v_i(t) ≥ τ_i(M\T)` (each contested good beats agent `i`'s threshold of the 5-good remainder),
> then the `5111` allocation "`t₁,t₂,t₃` to any three agents, remainder to the fourth" is EFX₀.

*Proof.* The three singletons are immune. The only target is the 5-bundle `D=M\T` held by `d`; each
singleton-holder `a` has `v_a(t_a) ≥ min_{t∈T}v_a(t) ≥ τ_a(D)`, so no strong envy; `d` envies no singleton.
∎ (theory2: 3000/3000 three-peak instances are `5111`-feasible.)

**Gap to "floor-k=3 ⇒ 5111".** `k(V)=3` says the three contested goods have high *floor*; the theorem
needs each to beat each agent's `τ_i(D)`, which depends on how agent `i` values the **remainder** `D`. When
`D`'s goods are small for *every* agent (true in the clean generator), `τ_i(D)` is small and the condition
holds; but a remainder good that is low-floor yet high for one agent `i` can push `τ_i(D)` above
`v_i(t)`. So **`k=3` ⇒ 5111 is not unconditional** — the per-agent condition above is the exact statement,
and it is what a `k=3` proof must verify. (This is the honest correction to "Fact 2 dominant-triple
finishes it": Fact 2 gives `τ_a(D) ≤ τ_a(M\{t_a})`, but `5111` needs the *tighter* `τ_a(D)` bound, which
floors do not control.)

## 5. k=1 — one contested good ⇒ 3221 [PROVEN for the dominant sub-case; OPEN otherwise]

- **[PROVEN]** If the contested good `t` is **dominant** for some agent `a` (`v_a(t) ≥ τ_a(M\{t})`), the
  Peeling Theorem gives EFX₀; CGM on the other 7 goods/3 agents returns a `3-2-2` (⇒ overall `3221`),
  `3-3-1`, `4-2-1`, or `5-1-1` allocation. theory2's sole-`3221` witness has good 7 dominant for all four
  agents, so Peeling directly produces its `3221`. Empirically the single contested good is dominant-ish
  whenever the floor gap is large.
- **[OPEN]** Contested but **not** dominant `t` (high to all, `< ½` for each): `3221` needs `a←{t}` with
  `v_a(t) ≥ τ_a(B)` for the largest bundle `B` in a `3-2-2` split of `M\{t}` — a weaker bound than
  dominance (`τ` of a ≤3-good bundle, not of all 7) — **and** the other three agents admitting a
  `3-2-2`-shaped EFX₀ split (CGM gives *some* shape, not necessarily `3-2-2`). Closing this needs a
  shape-controlled 3-agent EFX₀ existence, which CGM does not directly provide.

## 6. k=2 — the corridor [OPEN; exact system + the razor's-edge structure]

`k=2`: two contested goods `t₁,t₂`, six low-floor goods. The live shapes are `4211/3311` (both contested
goods as singletons — two-treasure) and `3221` (one contested singleton, the other inside a fat bundle);
`5111` needs a third contested good (absent ⇒ ¬5111 automatic) and `2222` is broken by the lumpiness that
two contested goods create. A `k=2` counterexample must satisfy simultaneously:

```
¬4211 ∧ ¬3311  :  the two-treasure system (t₁→a, t₂→b singletons; c,d split the 6 others) fails
                  for every treasure choice & split  ==  NC-B  (twotreasure.py = None)
¬3221          :  every (one contested singleton + 3-2-2 with the other contested good in a fat
                  bundle) has a holder strongly-envying a fat bundle
+ NC-A (no dominant good, §2), no global-min good (else Parking closes it), acyclic-envy WLOG.
```

**The razor's-edge observation (why the corridor is the wall).** In a *clean* `k=2` instance the two
contested goods dominate every half of the six small goods, so the two-treasure allocation `4211/3311`
is EFX₀ *easily* — `v_a(t₁) ≥ τ_a(3 \text{ small goods})` with room to spare. To make **NC-B** hold (break
both `4211` and `3311`), the instance must sit exactly where the contested goods **fail to dominate the
realized halves by a hair** — i.e. the "small" six are not small enough, or `t₁,t₂` not high enough,
relative to the *specific* split. That is precisely the slack-1 margin at which V/V2/V3 live
(`TWO_TREASURE §1`: loosest survivor slack 4, most at slack 1). Simultaneously `¬3221` forbids parking one
treasure and splitting `3-2-2`. So the corridor witness must thread: contested enough to break `2222` and
force `k=2`, but with both treasures *just* failing NC-B, *and* `3221` also failing — a four-way tie at
zero slack. **I did not derive a contradiction from `NC-A ∧ NC-B ∧ ¬3221 ∧ acyclic ∧ no-global-min`;**
doing so would resolve `(4,8)`. The exact system above is the CP-SAT target — and it is *narrower* than
theory2's five-shape stuck system precisely because at `k=2` the shapes `2222`/`5111` are auto-excluded, so
the solver need only be handed `NC-B ∧ ¬3221 ∧ NC-A ∧ no-global-min` with the contested count pinned to 2.

---

## 7. Honest assessment

**[PROVEN]** the Peeling Theorem (dominant good ⇒ EFX₀, strengthening NC-A to "no dominant good at all");
k=3 feasibility under the exact per-agent condition; k=0 for near-identical; k=1 for the dominant sub-case.

**[KEY NEGATIVE FINDING]** the floor-based `k` (and theory2's universal-contest ladder) is well-defined only
in the **aligned** regime; it **fails on the real near-witnesses** (`k(V)=k(V3)=4`, `k(V2)=1` — all wrong),
because their treasures are *misaligned* (high for the holder, low for others, hence low floor). So the
"ladder is a clean partition" premise is false: **alignment is a second axis**, and the misaligned regime —
where V/V2/V3 live and the campaign wall stands — is not indexed by any contested-good count. Any per-`k`
proof program covers only aligned instances; the open core is misaligned `k≈2`.

**[OPEN]** the unconditional per-`k` steps: k=0 general `2222` (a 4-way EFX₀ existence), k=1 non-dominant
`3221` (needs shape-controlled 3-agent EFX₀), and — the wall — the **k=2 corridor**, whose exact stuck
system is §6. The main *narrowing* delivered here: at `k=2` the residual collapses to
`NC-B ∧ ¬3221 ∧ NC-A ∧ no-global-min` (shapes `2222`,`5111` auto-excluded), and the binding tension is the
zero-slack two-treasure margin where the near-witnesses already sit. A proof would need to force NC-B's
failure to *contradict* `¬3221` (both treasures failing every half, yet no single-treasure `3-2-2` working)
— which I could not do, and which is the exact open content of `(4,8)`.

### Reproduction
- `k(V)`: floor gap, code in this session; validated against `sole_witness` rows and `mincover`
  generators.
- Peeling: 1500/1500 dominant-good instances EFX₀. k=3: theory2 3000/3000 three-peak `5111`.
