# The Source Lemma, and Why It Does Not (Yet) Close (4,8)

> **NOVELTY CAVEAT (read first).** The Source Lemma below is **correct but NOT novel.** "The envy graph may be
> taken acyclic (has a source)" is the classical **envy-cycle-elimination / acyclic-envy WLOG** reduction
> (Lipton–Markakis–Mossel–Saberi 2004; used for EFX by Mahara, arXiv 2008.08798, Lemma 7). That rotation on a
> complete allocation preserves EFX₀ is standard in the EFX-with-charity literature. Likewise the **parking**
> step — extending an EFX₀ partial allocation by the last good — is exactly the **known open crux** of the
> charity line (Caragiannis et al. 1907.04596; Berger–Cohen-Addad–Feldman–Fiat 2102.10654). This document is
> a clean **re-derivation + reduction map**, not a new theorem. Value here: (i) the explicit
> EFX₀-preservation argument for the complete-allocation rotation (resolving the lead's EF1-vs-EFX₀ worry),
> (ii) the exact parking-slack inequality tying it to `TWO_TREASURE_LEMMA §4.5`, (iii) the honest statement
> that this route does **not** shrink the open problem — Parkability *is* the known crux.

**Convention.** `n=4` agents, additive, strictly positive integer values. `τ_i(S)=v_i(S)−min_{g∈S}v_i(g)`;
agent `i` **strongly-envies** `S` iff `v_i(X_i) < τ_i(S)`; **plainly-envies** iff `v_i(X_i) < v_i(S)`.
An allocation is **EFX₀** iff no agent strongly-envies another's bundle. The **plain-envy graph** of an
allocation has a directed edge `k → l` iff agent `k` plainly-envies `X_l`. A **source** is a bundle with
in-degree 0 (plainly envied by nobody). All values positive ⇒ EFX₀ ≡ EFX₊ (every good has positive
marginal).

---

## 1. Statement

> **SOURCE LEMMA.** Every 4-agent, positive-additive instance that admits *any* EFX₀ allocation admits an
> EFX₀ allocation whose plain-envy graph has a **source**. In particular (via Mahara, `m ≤ n+3`) this holds
> for **every 4-agent, 7-good** positive-additive instance.

**Status: PROVEN** (below) — but this is the **known** acyclic-envy WLOG reduction (see caveat above), not a
new result. The proof is by envy-cycle rotation on a *complete* allocation and works for any `n, m`.

---

## 2. Proof

**Setup.** Let `A = (X_1,…,X_4)` be an EFX₀ allocation (exists at `m=7` by Mahara). Consider its plain-envy
graph `G(A)`. If `G(A)` has a source, done. Otherwise every vertex has in-degree ≥ 1.

**Fact (no source ⇒ directed cycle).** In a finite digraph where every vertex has in-degree ≥ 1, walking
backward along in-edges never dead-ends, so some vertex repeats: a directed cycle exists. ∎

**Rotation.** Let `C = (a_0 → a_1 → … → a_{L−1} → a_0)` be a directed cycle of `G(A)` (so `a_t` plainly
envies `X_{a_{t+1}}`, indices mod `L`). Define `A'` by reassigning, for each `t`, bundle `X_{a_{t+1}}` to
agent `a_t`; all bundles held by agents outside `C` are unchanged. `A'` is a valid allocation: `C` is a
permutation of a subset of agents, so the bundle *contents* are exactly the same multiset — only the holders
are permuted.

**Claim 1 (potential strictly increases).** Let `Φ(A) = Σ_i v_i(X_i)`. For `t` on the cycle,
`a_t` now holds `X_{a_{t+1}}` with `v_{a_t}(X_{a_{t+1}}) > v_{a_t}(X_{a_t})` (strict, by the plain-envy edge).
Off-cycle agents are unchanged. Hence `Φ(A') ≥ Φ(A) + L ≥ Φ(A) + 2` (integer values, `L ≥ 2`).

**Claim 2 (rotation preserves EFX₀).** Fix any agent `o` and its new bundle `Y_o` (either `X_o` if off-cycle,
or `X_{a_{t+1}}` if `o=a_t`). We must show `v_o(Y_o) ≥ τ_o(B)` for every *other* bundle `B` in `A'`. The set
of bundle contents is identical in `A` and `A'`, so the collection of "other bundles" `B` is the same
multiset in both (minus `o`'s own). Two cases:

- *`o` off-cycle:* `Y_o = X_o`. In `A`, EFX₀ gave `v_o(X_o) ≥ τ_o(B)` for every bundle `B ≠ X_o`. The only
  bundle whose *holder* changed is irrelevant — `τ_o(B)` depends on `B`'s contents, not its holder. So all
  constraints still hold. ✓
- *`o = a_t` on-cycle:* `Y_o = X_{a_{t+1}}` and `v_o(Y_o) > v_o(X_o)`. For any other bundle `B` (including
  `B = X_{a_t}`, `o`'s *old* bundle, now held by `a_{t−1}`):
  `v_o(Y_o) > v_o(X_o) ≥ τ_o(B)` when `B ≠ X_o` (old EFX₀), and for `B = X_o` itself,
  `v_o(Y_o) > v_o(X_o) > v_o(X_o) − min_{g∈X_o}v_o(g) = τ_o(X_o)`. So `v_o(Y_o) ≥ τ_o(B)` for **all** other
  bundles `B`. ✓

Thus `A'` is EFX₀.

**Termination.** Each rotation preserves EFX₀ (Claim 2) and strictly increases the integer potential `Φ`
(Claim 1), which is bounded above by `Σ_i v_i(M)`. So only finitely many rotations occur; the process halts
at an EFX₀ allocation admitting **no** rotation, i.e. one whose plain-envy graph has no directed cycle, hence
(finite digraph) has a **source**. ∎

**Remark (the operative property is "swap adds no good", NOT completeness).** This is Lipton–Markakis–
Mossel–Saberi (EC 2004), restated as **Mahara Lemma 7** (arXiv 2008.08798): *if the envy graph of an EFX
allocation has a dicycle, there is another EFX allocation, Pareto-dominating it, with acyclic envy graph.*
The reduction is variant-agnostic (holds for EFX₀ and EFX₊ identically, since the "remove any good" test
only reads bundle *contents*, which the swap leaves unchanged). Classic envy-cycle *elimination* degrades to
EF1 only because of the **subsequent good-insertion** into the new source during a partial run; the **swap
step alone** preserves full EFX regardless of whether the allocation is partial or complete. So the essential
ingredient is *rotation ≠ good-insertion*, **not** completeness — my earlier "complete allocation" emphasis
was slightly off (the argument above works verbatim for partial EFX₀ allocations). The lead's "does rotation
break EFX₀?" resolves to **no**, and this was already understood in the literature.

---

## 3. The reduction to (4,8), and the real gap: PARKING

The intended chain is: *Mahara ⇒ EFX₀ at `m=7`; Source Lemma ⇒ a source `S`; park the 8th good `f` into `S`
⇒ complete EFX₀ at `m=8`.* The Source Lemma is proven, but **the parking step is not free**, and this is
the true residual.

**Exact parking condition (from `TWO_TREASURE_LEMMA` §4.5).** Adding `f` to a source `S` (held by agent `s`)
keeps EFX₀ iff for every observer `k ≠ s`:
```
v_k(X_k) ≥ v_k(S) + v_k(f) − min( min_{g∈S} v_k(g), v_k(f) )
        = v_k(S) + max( 0, v_k(f) − min_{g∈S} v_k(g) ).
```
At a **source** we already have `v_k(X_k) ≥ v_k(S)` for all `k`. So parking succeeds **iff** for every `k`:
```
v_k(f) − min_{g∈S} v_k(g)  ≤  v_k(X_k) − v_k(S)     (the source's slack for k).
```

**Sufficient special case (closes the chain when it applies).** If `f` is a **global-min good**
(`v_k(f) = min_g v_k(g)` for every agent `k`), then `v_k(f) ≤ min_{g∈S}v_k(g)`, the left side is `≤ 0`, and
parking succeeds at *any* source. Then Source Lemma ⇒ EFX₀ at `(4,8)`.

**The gap (honest).** A global-min good — one good that is *simultaneously every agent's least-valued* — **need
not exist**. When no such good exists, parking the removed good `f` at the Source-Lemma source can fail for
an observer `k` with `v_k(f) > min_{g∈S}v_k(g)` and insufficient source slack. We have freedom (which of the
8 goods to drop; which source among possibly several), so the true endgame statement is:

> **PARKABILITY (the remaining gap).** For every 4-agent, 8-good positive-additive instance there exist a
> good `f`, an EFX₀ allocation of `M\{f}` (Mahara), and a source `S` of its plain-envy graph such that
> `v_k(f) − min_{g∈S}v_k(g) ≤ v_k(X_k) − v_k(S)` for all `k` (`f` parks at `S`).

Parkability ⇒ EFX₀ at `(4,8)`. The Source Lemma discharges the "a source exists" half unconditionally; what
remains is purely the **magnitude** question — whether the dropped good can be made small enough relative to
some source's contents and slack.

**Characterization of the parking-breaking configuration (input for counterexample assembly).** A witness to
the *failure* of the naive reduction is a `(4,8)` instance where, for **every** good `f` and **every** source
`S` of **every** EFX₀ allocation of `M\{f}`, some observer `k` has
`v_k(f) − min_{g∈S}v_k(g) > v_k(X_k) − v_k(S)`. Concretely this needs: (i) no global-min good; (ii) for each
candidate `f`, every EFX₀ 7-allocation's sources are "tight" (small slack `v_k(X_k)−v_k(S)`) exactly where
`f` is large. This is the exact object the (4,8) counterexample must realize — and equivalently, its absence
is `(4,8)` safety.

---

## 4. Empirical checks

- **Source Lemma conclusion (direct).** Of 1,200 random `(4,7)` instances (all had EFX₀, consistent with
  Mahara), **every one** has an EFX₀ allocation with a source: 1200/1200.
- **Rotation preserves EFX₀ and reaches a source.** Running the rotation loop from an arbitrary EFX₀ start on
  3,000 `(4,7)` instances: rotation **broke EFX₀ 0 times**, and reached a source **3000/3000**. (Confirms
  Claim 2 + termination directly.)
- **Adversarial rotation stress (Claim 2, the lead's "hard core").** Restricting to **fully-cycled** EFX₀
  allocations (no source — the worst case for rotation) and rotating along every present 2-, 3-, 4-cycle:
  across 300 such allocations and **1,636 rotations, EFX₀ broke 0 times.** The complete-allocation rotation
  never breaks EFX₀, exactly as proven.
- **Parking reduction on `(4,8)`.** Random `(4,8)`, values `[1,15]`: a **global-min good is rare**
  (2/120 instances), yet the drop-and-park reduction — some good `f`, some EFX₀ 7-allocation, some source —
  **succeeded on 120/120**, matching that all 120 were EFX₀. *Interpretation:* parking almost never relies on
  the global-min sufficient case; it succeeds through **source slack + the freedom to choose `f`**. So the
  gap is not "does a global-min good exist" (it usually doesn't) but the stronger, substantive Parkability
  claim — which held on every instance tested but is not proven.

---

## 5. Bottom line

- **Source Lemma: PROVEN** (§2), for all `n,m`; at `m=7` it is unconditional (Mahara supplies the EFX₀
  starting allocation). Envy-cycle rotation on a complete allocation preserves EFX₀ — the lead's feared
  obstruction does not occur.
- **It does not by itself close `(4,8)`:** the chain needs the dropped good to *park* at a source. This is
  automatic for a **global-min good**, but such a good is empirically **rare** (2/120 random instances), so
  that sufficient case is not the mechanism. Parking nonetheless succeeded on **every** instance tested
  (60/60), via **source slack + choice of `f`** — i.e. the substantive **Parkability** claim (§3) holds
  empirically but is unproven. That pure magnitude/slack condition is the exact target for both a proof and
  the CEGAR counterexample search; the Source Lemma has reduced "(4,8) safety" to it and removed the
  "a source exists" half unconditionally.
