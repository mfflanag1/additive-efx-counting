# The Conflicting-Peaks Window: Definition, Ladder Theorem, and Residual System

**Goal.** Formalize the §5 "conflicting-peaks" regime and decide whether some allocation family is
*always* EFX₀ there for `n=4, m=8` — closing the window, or exposing the exact inequalities a witness must
satisfy. Notation and `τ_i(S)=v_i(S)−min_{g∈S}v_i(g)` as in `TWO_TREASURE_LEMMA.md`; all values positive
integers, so EFX₀ = EFX₊.

---

## 1. Regime definition (precise)

**Conflicting-peaks instance `CP(P, T; flat)`.** A partition of the goods `M = P ⊍ T` into a **peak set**
`P` (`|P| = p`) and a **tail set** `T` (`|T| = m−p`) such that:
- **(Shared peaks / domination)** for every agent `i` and every `g∈P, h∈T`: `v_i(g) > v_i(h)`. The same
  `p` goods are the top-`p` goods for *all* agents. *(This is the "conflicting" hypothesis — peaks
  coincide across agents.)*
- **(Flat tails)** for every agent `i`, all tails share one value `c_i := v_i(h)`, `h∈T`. (Relaxation
  "near-flat": tails in `[c_i, c_i(1+δ)]`; the results below degrade gracefully in `δ`.)
- Peak magnitudes: write `π_i^{(g)} = v_i(g)` for `g∈P`. **Peak/tail ratio** of agent `i`:
  `r_i := min_{g∈P} π_i^{(g)} / c_i > 1`.

For `n=4` the case of interest is `p=3` (`|T|=5`), which is what the CEGAR run targets.

**Important empirical caveat (measured).** The three dual-verified near-witnesses are **not** clean
`CP` instances: their per-agent argmax goods are *spread* (V/V3: argmaxes `{2,6,4,4}`, top-3 sets intersect
in only `{2,6}`; V2: argmaxes `{7,1,0,1}`). They are *perturbations* of `CP` with agent-specific favorites
and one or two high "tail" goods. So the clean `CP` regime is a **model** of the near-witness basin, not an
exact container — a fact that matters for interpreting a CEGAR-UNSAT on `CP` (§5).

---

## 2. The family ladder (PROVEN for identical / near-identical valuations)

Fix `p=3, |T|=5`. Consider the one-parameter family `F_j`, `j ∈ {2,3,4,5}` (`j` = size of the tail-dump):

```
F_j :  one "dump" agent d holds D = { j tails }
       (5−j) agents each hold a peak + one tail   {p, t}
       (j−2) agents each hold a bare peak          {p}
       (uses exactly 3 peaks and 5 tails; requires 2 ≤ j ≤ 5)
```

**Lemma 2 (ladder EFX₀ conditions — PROVEN via singleton-immunity, Lemma 1′).** With flat tails
(`v_o(h)=c_o`) and domination (`v_o(p) ≥ c_o`), the only strongly-enviable bundles are the peak+tail
bundles and the dump `D` (bare peaks are immune). Observer `o`'s thresholds are
`τ_o({p,t}) = v_o(p)` and `τ_o(D) = (j−1)c_o`. Hence `F_j` is EFX₀ **iff** for every agent `o`:
```
(vs each peak+tail bundle {p,t}):   v_o(X_o) ≥ v_o(p)          for all peaks p not held by o
(vs the dump D):                    v_o(X_o) ≥ (j−1) c_o
```
where `v_o(X_o)` is `v_o(p_o)+c_o` (peak+tail holder), `v_o(p_o)` (bare-peak holder), or `j·c_o` (dump).

**Theorem 2 (identical agents ⇒ `CP` is always EFX₀).** If all agents share one valuation (peaks `P`, tail
`c`), then some `F_j` is EFX₀. *Proof.* Write `ρ = P/c` (take equal peaks for the clean statement). The
binding constraints of `F_j` reduce to: a **bare peak** tolerates the dump (`P ≥ (j−1)c ⟺ ρ ≥ j−1`) and the
**dump agent** tolerates a peak+tail (`jc ≥ P ⟺ ρ ≤ j`). So `F_j` works iff `ρ ∈ [j−1, j]`. As `j` runs
`2..4` these intervals tile `[1,4]`, and `F_5` (= the k=3 "all-bare-peaks + 5-dump", no peak+tail bundle,
hence no upper bound) covers `ρ ≥ 4`. Every ratio `ρ ≥ 1` is covered, so an EFX₀ allocation always exists.
∎ *(Independently guaranteed: identical valuations always admit EFX₀ — Plaut–Roughgarden leximin.
Verified computationally across ratios 1.5–4; see `TWO_TREASURE_LEMMA` reproduction.)*

**Corollary (near-identical).** If the four valuations are within a multiplicative `(1+ε)` band and
`ρ` avoids the interval endpoints `{2,3,4}` by margin `> ε·(stuff)`, the same `F_j` remains EFX₀ (each
inequality has slack `≥` one tail-unit at an interior ratio). So the window can only open where valuations
are **genuinely heterogeneous** — different agents wanting different dump sizes.

---

## 3. Where the ladder can break (the residual — heuristic, then exact system)

The ladder assigns **one** dump size `j` to the whole instance, but `F_j`'s two-sided constraint couples
agents with *different* ratios:
- a **bare-peak** holder `y` needs `v_y(p_y) ≥ (j−1)c_y` → forces `j` **small** if some agent has a low
  peak (small `r_y`);
- the **dump** holder `d` needs `j·c_d ≥ max_p v_d(p)` → forces `j` **large** if the dump agent has a high
  ratio `r_d`.

Because we may *choose* which agent is `d` and which peak each agent anchors, a break requires that **no**
choice of `(d, peak-assignment, j)` clears both sides at once. Intuitively: spread the ratios so that
whoever is forced to hold the dump has a high ratio (wants big `j`) while some unavoidable bare-peak holder
has a low ratio (needs small `j`), for every rotation. This is the residual target.

**Exact residual system (PROVEN sufficient — a witness must violate all of it).** A `CP(P,T;flat)` instance
with `p=3` admits an EFX₀ allocation **if** there exist `j∈{2,3,4,5}`, a dump agent `d`, and an injection
`assign: {other 3 agents} → P` of peaks (with `5−j` of those agents additionally receiving one tail) such
that, writing `X_o` for the resulting bundle:
```
∀ agents o, ∀ peaks p not in X_o:     v_o(X_o) ≥ v_o(p)
∀ agents o ≠ d:                        v_o(X_o) ≥ (j−1) c_o
d :                                    j·c_d ≥ v_d(p)   for every peak p     (i.e. j c_d ≥ max_p v_d(p))
```
Enumerated cost: `4 (dump) × 4 (j) × 3! (peak assign) × (choice of which agents get a tail) × (which tail)`
— a few thousand checks; implemented as `peaks_ladder.py :: ladder_witness(V, P, T)` (repo root), a
**sound** sufficient screen for `CP` instances (analogous to `two_treasure_witness`). *Note:* the role
assignment must range over **which** of the 3 non-dump agents get a paired tail, not just the first ones —
a first draft that fixed the roles by index missed genuine ladder allocations.

**NC-Peaks (necessary condition on any `CP` witness).** Negation of the above for *all* `(j,d,assign)`:
for every choice of dump agent `d`, peak-assignment, and `j∈{2,3,4,5}`, at least one ladder inequality
fails. In slogan form — **spread ratios, no common dump size:** for every agent that could hold the dump,
its ratio `r_d` demands a dump size `j ≥ ⌈r_d⌉` that some forced bare-peak holder cannot tolerate
(`r_y < j−1`). (This is necessary for the *ladder* to fail; a full witness must additionally defeat
two-treasure/NC-B and all non-ladder allocations.)

---

## 4. Empirical verdict on the clean `CP` regime

**The clean `CP(p=3, flat tails)` regime appears fully safe — no EFX₀-free instance found, and the ladder
family certifies every instance:**

| test | samples | EFX₀-free found | min EFX₀ count |
|---|---|---|---|
| Ladder coverage, **adversarial spread-ratio** CP (fixed screen) | 25,000 | — (**0 uncovered**) | — |
| Full enumeration, mid-ratio CP (peaks 6–12, tails 1–5) | 1,500 | **0** | 45 |
| Full enumeration, adversarial spread-ratio CP | 1,500 | **0** | 23 |
| Full enumeration, wide-magnitude CP (peaks `c+1..c+40`) | 1,500 | **0** | 8 |
| Full enumeration, perturbed/bumpy-tail V-like generator | 4,000 | **0** | 68 |
| CEGAR (team lead), spread ladder-straddling bands + NC-A | — | **UNSAT (2s)** | — |

So within the clean regime EFX₀ exists *abundantly* (tens of allocations); the instance sits far from the
boundary. This supports **Theorem 3 (conjectured): every `CP(p=3, flat tails)` instance admits an EFX₀
ladder allocation.** No general proof (the §3 system couples the peak-assignment matrix), but the ladder is a
*sound* certificate covering 100% of 25k adversarial cases, and the lead's CEGAR confirms UNSAT on
spread bands.

**Why flatness is load-bearing (the real escape hatch).** Theorem 2 and the ladder screen assume **flat
tails**: the formula `τ_o(D) = (j−1)c_o` for the dump holds only when every tail has the same value `c_o`.
With **bumpy tails** (some tail goods worth much more to some agents), `τ_o(D)` is no longer `(j−1)c_o` and
the ladder's clean tiling collapses. The three near-witnesses are exactly this: their "tails" are **not
flat** and their peaks are **misaligned** — good `g` is a peak for one agent and a near-tail for another
(V: good 1 is 49 for agent 1 but 8 for agent 0). My random bumpy-tail generator did **not** get near the
boundary (min 68 — random misses the manifold, as before), so it is a weak probe; the informative test is a
*structured* misalignment (§5).

---

## 5. Band geometries worth testing (the spread-ratio UNSAT does *not* cover these)

The 2s-UNSAT ran flat tails + shared peaks + spread ratios — exactly the regime the **flat-tail ladder
already closes** (Theorem 2/3). It says nothing about the geometries where the ladder's `τ_o(D)=(j−1)c_o`
assumption is *false*. Three concrete, seconds-cheap cells, in priority order:

**(G1) Misaligned peaks (the V regime — highest priority).** Not a shared peak set — a **Latin-square /
permutation** value structure: each agent `i` has a *private* signature good `s_i` that is a **near-tail
for everyone else**. This is what all three near-witnesses do and what the ladder cannot model (there is no
common `P`).
   - Bands: 4 signature goods `s_0..s_3`; `v_i(s_i) ∈ [45,65]`, `v_i(s_j) ∈ [1,20]` for `j≠i`; one or two
     *shared* contested goods `v_·(g) ∈ [40,60]` (all agents) to force competition; remaining 2–3 goods
     flat tails `[1,8]`. Enforce NC-A (no ≥½-universe good) and the two-treasure screen `= None`
     (`twotreasure.py`) and NC-B. This is the tightest emulation of V/V2; a UNSAT here is far more
     decisive than the flat-tail cell.

**(G2) Bumpy tails on top of shared peaks.** Keep `P={0,1,2}` shared, but make the 5 tails **non-flat**:
per agent, tails drawn from a wide band `[1, 20]` (not a single `c_i`), so `τ_o(dump)` varies with *which*
tails land in the dump — breaking the ladder tiling. Bands: peaks `[20,45]`, tails **`[1,20]`** (wide),
NC-A on.

**(G3) `p=2` and `p=4` contested-set sizes.** `p=4` matches V's four contested goods `{1,2,4,6}`: four
"peak-ish" goods `[25,60]`, four flat tails `[1,6]`, misaligned (each agent's argmax among the four is
distinct). `p=2`: two peaks `[30,60]`, six-good block with two internally-elevated goods `[15,30]` (so the
block is not flat and two-treasure's E5/E6 split is stressed).

If any of G1–G3 returns UNSAT, that is genuinely new coverage; if any returns SAT, verify with both checkers
(`verify.py` + `verify2.py`) and read off §3/NC-B/NC-D to see which family the witness defeats.

---

## 6. Skeleton of a `(4,8)`-safety argument (endgame map; asks for ONE lemma)

**Claim to prove:** every 4-agent, 8-good, all-positive additive instance has an EFX₀ allocation.

**Proven pieces (this campaign + literature):**
- **P1. Singleton immunity + k-treasure reduction** (Lemma 1, 1′): a size-1 bundle is never strongly
  envied; a k-treasure allocation is EFX₀ iff no agent strongly-envies a *fat* bundle.
- **P2. Two-treasure existence** (Theorem 1): a dominant pair (two agents with ≥½-universe goods on distinct
  goods) ⇒ EFX₀. Rests on **2-agent EFX₀ always existing** (Plaut–Roughgarden / cut-and-choose).
- **P3. Identical / near-identical safety** (Theorem 2 + PR leximin): the flat-tail family ladder tiles the
  ratio line; identical valuations always admit EFX₀.
- **P4. Almost-full existence** (Berger–Cohen-Addad–Feldman–Fiat, black box): every 4-agent additive
  instance admits an EFX₀ allocation leaving **≤ 1 good** in charity.
- **P5. Floater/charity dichotomy** (§4.5, proven): given an EFX₀ base of `M\{f}`, the good `f` parks safely
  in any bundle `B_i` that is a **source** of the base's plain-envy graph (for a global-min `f`, and more
  generally whenever the placement inequality holds). Un-parkability ⇒ the base envy graph is a full cycle.

**Exact-search results that plug bounded holes (conditional theorems):**
- values `{1,2,3}` UNSAT; values `{1..4}` (K=4) UNSAT; `(4,9)` `{1,2,3}` UNSAT.
- spread-ratio flat-tail band family UNSAT (2s); box-UNSAT radius 6 around count-5 seed; anatomy pool 3000+
  with no SAT-witness; floater columns FREE in both count-4 basins.

**The single remaining gap (name it):**

> **GAP LEMMA (Parkability).** For every 4-agent, 8-good positive-additive instance there exist a good `f`
> and an EFX₀ allocation of `M\{f}` (guaranteed to exist by P4) such that `f` can be added to some bundle
> **keeping EFX₀** — i.e. among all almost-full EFX₀ bases, at least one has a placeable charity good.

By P4 an almost-full EFX₀ base always exists; the *entire* open question is whether the last good can be
placed. P5 makes this concrete and structural: **Parkability fails only if every EFX₀ base of every `M\{f}`
has its charity good detonated at all placements** — which by P5 forces every such base to have a plain-envy
graph with no source (a full cycle) *and* every re-rotation of that cycle to fail EFX₀. §4.5 showed the
local floater system is satisfiable but that detonating one base opens ~200 other EFX₀ allocations; the Gap
Lemma is the statement that this "reshuffling" can never be simultaneously closed off. Proving it (or the
weaker "some `f`-base among the exponentially many is a source") would complete `(4,8)` safety; it is
equivalent in strength to the open problem but now has a precise envy-graph target rather than a brute
allocation search.

**Honest status:** P1–P5 are proven; P3 covers identical/near-identical and P2 covers dominant instances;
the flat-tail ladder + spread-ratio UNSAT close the aligned-peaks regime. The uncovered core is exactly the
**misaligned-peaks / bumpy-tail** regime (G1–G3), and the one lemma that would close everything is
**Parkability**.

---

## 7. After G1 UNSAT: the shrunken residual and a coverage sweep

**G1 closed (lead's CEGAR: UNSAT, 35s, 74 iters).** The misaligned-signature cell — the top-priority
V-emulation — has no witness at those bands. The residual does **not** open a new axis; it is the
**product corner these single-axis cells each miss**, plus one value band both skipped:

- **The intermediate-value band (concrete, from V).** V's non-contested goods are *not* all flat: good 0 is
  `[10,16]` across agents — an **intermediate** shared good sitting in the gap between G1's flat tails
  `[1,8]` and the contested band `[40,60]`. Neither flat-tail CP nor G1 populated `[9,~35]`. This is the
  exact structural feature that makes V a near-witness and it is currently **unsearched**.
- **The untested corner = misaligned × bumpy simultaneously.** G1 = misaligned + flat; G2 = aligned + bumpy.
  V is **both** (misaligned peaks *and* an intermediate/bumpy shared good). Test the conjunction:
  signature `v[i][i]∈[45,65]`, `v[j][i]∈[1,20]`; **one intermediate shared good `∈[10,35]`** (the "good 0"
  role); contested `∈[40,60]`; 2–3 genuinely flat tails `[1,8]`; NC-A + `twotreasure_witness=None` + NC-B.

**Framing for a quantitative writeup (two complementary coverage claims).**
1. *Structured-band UNSAT* = witness-absence inside a **box** of value space — heuristic de-risking of the
   near-witness manifold (where a witness would plausibly hide). Not a global proof.
2. *Rigorous coverage* = the **value-capped full cell** (integer K-ladder / Z3 full cell over all `[1,V]^{32}`):
   K≤4 already UNSAT. This is the exhaustive statement; bands only prioritize where to look.

**Probative sweep axes (map the phase diagram, not scattered boxes):**
| axis | range | why probative |
|---|---|---|
| `ρ` = min-peak / max-tail | 1.25 → 8 (step ≈0.5) | controls the ladder tiling; boundaries at 2,3,4 |
| `β` = tail/intermediate ceiling | flat(`=c`) → `peak_lo` → beyond | **the key line:** when `β ≥ peak_lo` the peak/tail *gap closes* and all peak/tail structure (incl. the ladder) is gone → generic regime |
| misalignment `m` | aligned(4-share) / partial(2–3) / signature(1) | G1 did signature-flat only |
| `p` (contested-set size) | 2, 3, 4 | V-like is `p≈4` |

The **primary 2-D grid is `ρ × β`** at each `(m,p)`. Sweep `β` upward through `peak_lo` at fixed `ρ`: the
cell where the gap just closes (`β ≈ peak_lo`) is the single most probative box — it is where V lives and
where every structural lemma (ladder, domination, singleton-anchoring) simultaneously loses its grip. If
that strip is UNSAT across `ρ∈[1.25,8]` and `m,p`, the structured coverage claim becomes: *no 4×8 witness
with any peak/tail geometry inside the searched value box* — a quantitative statement to pair with the
K-ladder full-cell result.

---

### Reproduction
- Identical ladder families by ratio: `enumerate_all(4,8,[[P,P,P,c,c,c,c,c]]*4)` — families
  `balanced → 3-dump → 4-dump → 5-dump(k=3)` as `P/c` crosses `2,3,4`.
- Ladder screen (sound sufficient certificate): `peaks_ladder.py :: ladder_witness(V, P, T)` — 0 uncovered
  in 25,000 adversarial CP instances.
- `CP` searches: `scratchpad/peaks_all.py` (mid / adversarial / wide), `scratchpad/perturbed.py` (V-like).
  All 4,500 flat-tail + 4,000 perturbed full-enumerations: 0 EFX₀-free. G1 (misaligned) UNSAT via lead's CEGAR.
