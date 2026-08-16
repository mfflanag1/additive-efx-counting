# Cancelable-class sweep — length-two and length-three chains (2026-08-16)

Completes the additivity-dependence sweep begun in
[`BCFF_IMPORT_AUDIT_20260816.md`](BCFF_IMPORT_AUDIT_20260816.md) ("Additivity-dependence
sweep"), whose stated boundary was: *"The length-two chain — the only one invoking Theorem
3.16 and Definition 3.9 — was out of scope for this sweep"*, and which also left the
length-three chain uncovered. This note sweeps both, plus the packet-nondegeneracy section
of [`TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md`](TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md).

**OVERALL VERDICT: YES — the composition strengthens to BCFF's nice-cancelable class.**
No order-closing step in either chain needs additivity. Every value computation resolves to
monotone + cancelable + non-degenerate, and the one class of steps that *looks* like it needs
the forbidden reverse direction of cancelability turns out to be exactly the move BCFF
themselves make and license. Zero blocking sites. Four wording repairs are listed at the end;
none is load-bearing.

---

## 0. What the class actually is (checked against the e-print, not paraphrase)

Pulled `arxiv.org/e-print/2102.10654v2` and read `Inputs/2.Preliminaries.tex` directly.
Verbatim, in the corpus's citation pin (arXiv full build):

| BCFF source | Statement |
|---|---|
| `2.Preliminaries.tex:13` | "Each agent has a valuation `v_i: 2^M -> R_{>=0}`, which is **normalized and monotone**, i.e. `v(S) <= v(T)` whenever `S subseteq T` and `v(emptyset)=0`." |
| `2.Preliminaries.tex:57-64` | *cancelable*: for `S,T subseteq M` and `g in M\(S∪T)`, `v(S∪{g}) > v(T∪{g}) => v(S) > v(T)`. |
| `2.Preliminaries.tex:76` | *non-degenerate*: `v(S) != v(T)` for any two **different** bundles `S,T`. |
| `2.Preliminaries.tex:83` | *nice*: a cancelable `v` is **nice** if there is a non-degenerate cancelable `v'` that respects `v`. |
| `1.Introduction.tex:207` | "All our results hold for (*)**nice cancelable** valuations, generalizing additive valuations." |

Three consequences settle most of this sweep before a single corpus line is read.

**(0a) What "nice" adds — nothing, after Lemma A.1.** "Nice" is not an extra structural axiom
on the working profile. It is *precisely* the tie-breakability hypothesis that Lemma A.1
consumes: nice = "a non-degenerate cancelable respecting witness exists". Once A.1 is applied,
one works inside `v'`, which is cancelable and non-degenerate, and "nice" is never mentioned
again (BCFF, `2.Preliminaries.tex:99`: "for the remainder of this paper we assume that all
valuations are cancelable and non-degenerate"). **No corpus step in either chain needs "nice"
for anything except the A.1 invocation itself** — which is where the corpus already invokes it.
This also means finding 7's DRIFT is even more benign than recorded: A.1's witness being
cancelable-not-additive is not a shortfall, because nothing downstream wanted additivity.

**(0b) Iterated (set) cancelation is available.** By induction on `|R|`: if `R ∩ (S∪T) = ∅`
and `v(S∪R) > v(T∪R)`, peel one `g in R` at a time (`g` is outside `S∪R'` and `T∪R'`), giving
`v(S) > v(T)`. BCFF state this themselves in a commented-out block at
`2.Preliminaries.tex:66-73` and use it in the appendix (`9.Appendix.tex:226`). Call this
**tool C1**.

**(0c) The "reverse direction" IS available in this class — this is the sweep's key finding.**
The task brief flags `v(S) > v(T) => v(S∪{g}) > v(T∪{g})` as a direction cancelability does not
give, and warns that any step using it would be a real obstacle. Correct in isolation — but
**cancelable + non-degenerate together give it**, and BCFF say so explicitly at
`2.Preliminaries.tex:101`:

> `v(S ∪ R) > v(T ∪ R)  <=>  v(S) > v(T)`   (for `R subseteq M\(S∪T)`)

Proof of the `<=`: `v(S) > v(T)` forces `S != T`, hence `S∪R != T∪R`, hence by non-degeneracy
`v(S∪R) != v(T∪R)`; if `v(S∪R) < v(T∪R)` then tool C1 gives `v(S) < v(T)`, contradiction.
Call this **tool C2**. BCFF's own Section 3 machinery runs on it: `3.NewTechniques.tex:460`
("`T_i <_i T_succ(i)`. Hence, **by cancelability**, `X_i = T_i ∪ B_i <_i T_succ(i) ∪ B_i`") and
again at `:480` and `:649`. **Every reverse-direction use found in the corpus is an instance of
C2 and is therefore sound.** No blocking site arises from this axis.

**(0d) "Strict positivity" is free.** Monotone + normalized + non-degenerate gives
`v_i({g}) != v_i(∅) = 0` and `v_i({g}) >= 0`, hence `v_i({g}) > 0`; more generally
`S ⊊ T => v_i(S) < v_i(T)`. Every corpus appeal to "positivity" is this. Confirmed against
BCFF's own proof of Observation 2.8 (`2.Preliminaries.tex:281`): "Since valuations are
**non-degenerate and monotone**, `X_i <_i X_i ∪ {g}`." BCFF derive the corpus's positivity
step from exactly monotone + non-degenerate, never from additivity.

**(0e) Every BCFF import is free.** Lemma 2.4, Obs 2.8/2.9/2.10/2.11, Defs 2.6-2.7, Defs
3.1-3.4, Lemma 3.5, Def 3.9, Lemmas 3.13/3.14, Def 3.15, Theorem 3.16, Cor 3.18 and Lemma A.1
are all proved by BCFF for nice cancelable valuations. The length-two chain's reliance on
Theorem 3.16 — the corpus's "most important external interface" — costs nothing at the
cancelable level. Spot-checked: Thm 3.16 (`3.NewTechniques.tex:603`) is proved from
`lem:alg_start` (:451) and `lem:alg_step` (:465), whose only valuation-level moves are Obs 2.11
plus tool C2.

**(0f) Section-2 numbering reconstructed from source, corroborating the pin.** Environment
order in `Inputs/2.Preliminaries.tex` under `\fulltrue`: `obs:exists-champion` (:269) = **2.8**,
`obs:g_notin_bottom` (:293) = **2.9**, `obs:non-champion-doesnt-envy-top-half` (:326) =
**2.10**, `obs:T_k<T_j` (:352) = **2.11**. In `Inputs/3.NewTechniques.tex`:
`obs:good_cycle_g_decomposition` (:373) = 3.10, `obs:no_B_j_champ_of_j` (:414) = **3.11**,
`obs:pred(i)_nchamp_B(i)` (:432) = **3.12**, `lem:alg_start` (:451) = 3.13, `lem:alg_step`
(:465) = 3.14, and the theorem at :603 = **3.16**. This independently reproduces the mapping
`BCFF_IMPORT_AUDIT_20260816.md` relies on.

Reading of non-degeneracy used below is the same as the first sweep's, and it now matches BCFF
verbatim: distinct subsets get distinct values; monotonicity gives `>=`, non-degeneracy
upgrades to `>` whenever the two sets differ.

---

## 1. Length-two chain

Site inventory of
[`TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md`](TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md)
(the repaired 159-line version on this branch). Grepping every occurrence of `v_`, `b_`, `tau`,
"prefer" and "value" in that file returns **exactly one hit**, at line 48. The closure theorem
proper (Theorem 2, lines 57-139) is pure directed-graph combinatorics and contains no valuation
arithmetic at all.

| Site | Displayed step | Verdict |
|---|---|---|
| :15-20, (2) | `X_r = T_r ⊍ B_r`, `X_q = T_q ⊍ B_q` with nonempty bottoms | **inequality suffices** — set decomposition supplied by BCFF Obs 2.9 (`g ∉ D(i,j)` when `i` does not envy `j`); nonemptiness discharged in §3 below |
| :23-28 | "the only good internal `B_r`-edge is the edge from `r` into `q`"; both internal alternatives excluded, so each bottom has an external edge, (3) | **inequality suffices** — BCFF Thm 3.16 + Obs 3.11 (`H ∩ S = ∅` kills the `B_j\|B_j` target, a pure set condition, `3.NewTechniques.tex:414-427`) + Obs 2.11 with tool C2 (`3.NewTechniques.tex:432-448`). All at nice-cancelable level in BCFF |
| :43-50, **Lemma 1** | "no agent strongly envies `X_a ∪ {f}`: deleting `f` leaves the unenvied singleton, deleting its singleton good leaves the unenvied charity. **Positive additivity** makes owner `a` strictly prefer the pair" | **inequality suffices** — the only consumed fact is `v_a(X_a ∪ {f}) > v_a(X_a)`. `f ∉ X_a` makes the sets distinct; monotone gives `>=`, non-degeneracy makes it strict. This is *verbatim* BCFF's own Obs 2.8 proof step. The words "positive additivity" are decorative; **repair R1** below |
| :52-53 | "The ordinary envy graph is acyclic, since an envy cycle is already a basic PI cycle" | **inequality suffices** — BCFF Defs 3.1-3.4 + Lemma 3.5, no valuation arithmetic |
| :60-112, Thm 2 distinct-source branch, (4)-(9) | four combination cases, each closing a PI cycle; case 1 uses two vertex-disjoint cycles with mutual packet supply | **inequality suffices** — no value computation whatsoever. Case 1's "packet supply is mutual" is the Def 3.4 disjoint-incoming-set check, a set condition |
| :114-139, shared-source branch, (10)-(12) | `d -> a` forced by Lemma 1 + acyclicity; `r -> d` or `q -> d` closes (11)/(12) | **inequality suffices** — pure combinatorics on top of Lemma 1 |
| :141-143 | "does not need the shared-source envy exception in BCFF Corollary 3.18" | n/a — a non-use; correctly avoids Cor 3.18 (whose single-outsider hypothesis two outside singletons defeat) |

**Length-two verdict: clean.** One decorative additive phrase, zero additive dependencies,
zero reverse-cancelation uses. The chain's whole valuation content is the single inequality
`v_a(X_a) < v_a(X_a ∪ {f})`.

---

## 2. Length-three chain

The authoritative artifact is
[`LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md`](LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md)
(per the dependency ledger of `TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md:160`).
[`LENGTH_THREE_GLOBAL_LEX_TARGET.md`](LENGTH_THREE_GLOBAL_LEX_TARGET.md) contributes its
normal-form derivation (lines 1-500); its own header (:5-7) and :484-487 declare everything
below line 500 superseded — see §4.

Throughout, `tau_j(S) = max_{g in S} v_j(S \ {g})` and *common-safe* means `tau_i(S) <= b_i`
for every agent `i`.

### 2.1 Reservoir-order escape theorem

| Site | Displayed step | Verdict |
|---|---|---|
| ESCAPE:30-41 | **Minimal-threshold extraction.** "If `v_j(P)<t`, take a minimal desired subset of `P`" | **inequality suffices** — `A subseteq P` so `v_j(A) <= v_j(P) < t` by monotonicity alone |
| ESCAPE:38-40 | "take an inclusion-minimal `Q subseteq P` crossing `t`. If `Q` is unsafe, a minimal desired subset of an unsafe deletion `Q-h` has `j`-value below `t`" | **inequality suffices** — minimality of `Q` gives `v_j(Q-h) < t`; `A subseteq Q-h` gives `v_j(A) <= v_j(Q-h)` by monotonicity. Existence of a minimal *desired* (= envied, not strongly envied by anyone) subset of an envied set is BCFF's "most envious agent" definition, finiteness only. Degenerate case checked: a singleton `Q` can never be unsafe, since `v_i(∅) = 0 <= b_i` (normalization), so the branch is well-defined |
| ESCAPE:53, (2) | `v_q(W) = b_q + v_q(B_r) > b_q`, `W = X_q + B_r` | **inequality suffices** — only `v_q(X_q ∪ B_r) > v_q(X_q)` is consumed; `B_r != ∅` makes the sets distinct, monotone + non-degenerate gives strict. Same shape as the already-swept ALTERNATING_RESERVOIR_EXCHANGE_LEMMA:81 and ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY:77. The additive equality is decorative; **repair R2** |
| ESCAPE:55-63, (3) | `(D_p,Q,{x},{y})` is EFX; "`p` and `q` strictly improve, while `s` is fixed" | **inequality suffices** — `D_p` and `Q` common-safe; `{x},{y}` deletion-safe by normalization; `r` holding `Q` compares only against `D_p` (threshold `v_r(Q) >= t_r`) and two singletons. Note `v_r(Q) >= b_r` is *not* needed and not claimed |
| ESCAPE:80-83, (4) | `v_r(D_p) > tau_r(D_p) > v_r(A) >= tau_r(A)` | **inequality suffices** — first `>` is monotone + non-degenerate (`D_p != D_p - g`); middle `>` is the extraction branch hypothesis, not arithmetic; last `>=` is monotone. Identical shape to ADJACENT :166/:219/:390, already ruled sufficient |
| ESCAPE:66-88 | the six-row `q`-before-`r` source table; every displayed bundle common-safe or singleton | **inequality suffices** — each row checked: recipients hold a desired set (`> b_i` by desiredness), their own base bundle, or an envied singleton; the sole nonsingleton-vs-nonsingleton comparison is (4). In the `s,a=r` row, `r` holds `{y}` with `v_r({y}) > b_r >= tau_r(D_p)`, `tau_r(A)` — common safety, monotone |
| ESCAPE:99, (5) | `v_r(U) = b_r + v_r(B_q) > b_r`, `U = X_r + B_q` | **inequality suffices** — mirror of ESCAPE:53, `B_q != ∅`. **repair R2** |
| ESCAPE:102-109, (6) | `({x},D_r,Q,{y})` is EFX, fixes `p,s`, strictly improves `r` | **inequality suffices** — same structure as (3) |
| ESCAPE:111-117 | low-source exclusion: "If `H = A ∩ B_q` is empty, a `p`- or `q`-source would envy `X_r`" | **inequality suffices** — `H = ∅` puts `A subseteq X_r`, so `v_p(A) > b_p` and monotonicity give `v_p(X_r) > b_p`, contradicting the large-bundle no-envy lemma. **Monotonicity alone** |
| ESCAPE:117-139 | `A = (X_r \ S) ⊍ H`; the `(H\|S)` generalized champion edge; both PI cycles satisfy Def 3.4 | **inequality suffices** — a set identity plus BCFF Def 3.2/3.4. The disjointness check ("`r -f-> q` releases the whole bottom `B_q`, hence `H subseteq B_q`; the remaining incoming set `{f}` is unallocated") is set-theoretic |
| ESCAPE:150-153, (8) | `v_q(D_r) > tau_q(D_r) > v_q(A) >= tau_q(A)` | **inequality suffices** — identical to (4) |
| ESCAPE:157-170 | the three-row `s`-source table for `r`-before-`q`; "(8) settles `q`'s comparison" | **inequality suffices** — as for the `q`-before-`r` table |
| ESCAPE:198-205 | "no genuine edge enters a singleton": `{f}` unenvied by charity dominance, `{z,f}` not common-safe since deleting `f` leaves the envied `{z}` | **inequality suffices** — structural + monotone |
| ESCAPE:213-219 | empty top contradicts charity dominance; empty bottom forces a self-`f`-champion via Obs 2.10 + positivity; nonowner envy of a large bundle closes a PI cycle | **inequality suffices** — see §3; positivity is (0d) |
| ESCAPE:228-232 | "apply BCFF Lemma A.1, run the argument in its respecting positive nondegenerate perturbation, and return the EFX allocation" | **inequality suffices** — and this is now *exactly* what A.1 delivers, since nothing downstream wanted additivity. Correctly one-directional as written |

### 2.2 Normal-form derivation, `LENGTH_THREE_GLOBAL_LEX_TARGET.md` lines 1-500

This is the region that contains the chain's only genuinely subtle valuation algebra.

| Site | Displayed step | Verdict |
|---|---|---|
| TARGET:17-20, (1) | `v_i(f) <= v_i(X_i)` | **inequality suffices** — BCFF Lemma 2.4's "moreover" clause |
| TARGET:59-71 | four packets nonempty; empty `B_r` + Obs 2.10 "would make the negation of the self-edge `r -> r` imply `v_r(X_r) > v_r(X_r+f)`, contradicting positivity" | **inequality suffices** — Obs 2.10 instantiated at `i=j=r`, `B_r=∅`, `T_r=X_r`. Contradiction is `v_r(X_r) < v_r(X_r ∪ {f})` = monotone + non-degenerate (0d) |
| TARGET:76-78 | `v_r(T_r+f) < b_r`, `v_q(T_q+f) < b_q` | **inequality suffices** — Obs 2.10 at `i=j` |
| TARGET:82-84 | `v_r(f) < v_r(B_r)` | **inequality suffices — genuinely cancelable, and this is BCFF's own derivation.** From `v_r(T_r ∪ {f}) < b_r = v_r(T_r ∪ B_r)` cancel the common `T_r` by **tool C1** (`T_r` disjoint from `{f}` and from `B_r`). BCFF do exactly this in a dropped observation at `2.Preliminaries.tex:377-378`: "`(X_j \ D(i,j)) ∪ {g} <_j X_j = (X_j \ D(i,j)) ∪ D(i,j)`. Since valuations are cancelable, it follows that `{g} <_j D(i,j)`" |
| TARGET:82-84 | `v_r(T_q) > v_r(T_r)` | **inequality suffices** — from `v_r(T_q+f) > b_r > v_r(T_r+f)`, cancel the single good `f`. This is BCFF Obs 2.11 |
| **TARGET:86** | "**the mixed pool `B_r+T_q` strictly improves `r` over `X_r`**", i.e. `v_r(B_r ∪ T_q) > v_r(B_r ∪ T_r) = b_r` | **inequality suffices — REVERSE-DIRECTION USE, but licensed.** This is the one site in either chain that consumes `v(S) > v(T) => v(S∪R) > v(T∪R)`. It is **tool C2** with `R = B_r`, valid under cancelable + non-degenerate, and it is character-for-character the move BCFF make in the proof of Lemma 3.13 (`3.NewTechniques.tex:460`: "`T_i <_i T_succ(i)`. Hence, by cancelability, `X_i = T_i ∪ B_i <_i T_succ(i) ∪ B_i`"). **Not a blocking site.** Additivity is not needed and the corpus does not claim it here |
| TARGET:86-88 | `v_p(T_q+f) < b_p < v_p(T_r+f)`, hence `v_p(T_r) > v_p(T_q)` | **inequality suffices** — cancel `f`; BCFF Obs 2.11 again |
| TARGET:95-101 | Singleton-absorption lemma: giving `f` to an unenvied `{z}` is EFX and Pareto-improves | **inequality suffices** — deletion of `f` leaves `{z}` (unenvied), deletion of `z` leaves `{f}` (unenvied by (1)); the improvement is `v_j({z}) < v_j({z,f})`, monotone + non-degenerate |
| TARGET:115-134, (4a) | Large-bundle no-envy: `v_i(X_r) <= b_i (i != r)`, `v_i(X_q) <= b_i (i != q)` | **inequality suffices** — each contrary edge closes a cycle with at most one genuine `f`-edge, PI by Lemma 3.5 |
| TARGET:136-174 | BCFF basic-cycle classification into four residual classes | **inequality suffices** — combinatorial; the singleton-target exclusion is (1) + common safety |
| TARGET:176-189 | Easy-priority lemma: "every allocation giving each agent at most one good is EFX" | **inequality suffices** — deletion leaves `∅` and `v_i(∅) = 0 <= v_i(Y_i)`. Same as the already-swept ALTERNATING_EASY_PRIORITY_ESCAPE_LEMMA:36-40 |
| TARGET:206-217 | reservoir structure `W = X_q + B_r`: "`D_p` and `W` are disjoint, `q` values `W` strictly above her base" | **inequality suffices** — as ESCAPE:53 |
| TARGET:226-263, (5)-(6) | all-source `W` return; `tau_r(A) < t <= v_r(D_p)` | **inequality suffices** — as (4) |
| TARGET:277-316, (7)-(8) | rotated `U` return; `v_r(U) = b_r + v_r(B_q) > b_r`; `tau_p(A) < t' <= v_p(D_r)` | **inequality suffices** — as ESCAPE:99 and (4). **repair R2** applies to the displayed equality |
| TARGET:322-355, (9)-(10) | three-promotion lemma. "minimality gives `tau_s(C) < t`"; "`p` and `q` do not envy `X_r` and `r` values `X_r` at her base. Hence `C` lies below the new utilities of `p,r,q`"; `v_s(D_r) >= tau_s(D_r) > v_s(X_r) >= tau_s(X_r)` | **inequality suffices** — `C subseteq X_r` gives `v_i(C) <= v_i(X_r) <= b_i` by monotonicity; the three new utilities all exceed `b_i` by desiredness/envy; the displayed chain is monotone + branch hypothesis |
| TARGET:366-388, (11)-(12) | mirror lemma with `u = tau_s(D_p)`, `C subseteq X_q`; "the low inequality gives `v_s(D_p) > tau_s(X_q)`" | **inequality suffices** — same shape |
| TARGET:398-404, (13) first | `v_r(R) > b_r`, `R = B_r + T_q` | **inequality suffices — tool C2**, identical to TARGET:86 (this is where :86 is consumed) |
| TARGET:398-410, (13) second | `v_p(R) < v_p(D_p)`, justified as "`v_p(T_r) > v_p(T_q)`" **and** "`v_p(f) > v_p(B_r)`" | **inequality suffices — needs restating, but no additivity.** As written the justification reads as summing two independent strict inequalities across disjoint parts, which cancelability does not license. It is however obtainable by a two-step C2 chain: `v_p(T_q) < v_p(T_r)` gives `v_p(T_q ∪ B_r) < v_p(T_r ∪ B_r) = v_p(X_r)` (C2 with `R = B_r`), and `v_p(X_r) <= b_p < v_p(D_p)` is the no-envy row (4a) plus desiredness of `D_p` — the second sub-inequality `v_p(f) > v_p(B_r)` is not needed at all. **repair R4**; not load-bearing (see §4) |
| TARGET:412-418 | inclusion-minimal `C subseteq R` with `v_r(C) > b_r`; `tau_p(C) < v_p(D_p)` | **inequality suffices** given (13) — `C subseteq R` and monotonicity |
| TARGET:429-434, (15) | `tau_q(C) <= v_q(x)`, `tau_s(C) <= b_s` | **inequality suffices** — stated as the iff conditions, no arithmetic |
| TARGET:465-498 | Final reservoir-order closure; the two orientations partition all 24 orders | **inequality suffices** — routing only |

**Length-three verdict: clean.** Two decorative additive equalities, one reverse-direction use
that is licensed by C2 and matched by BCFF's own practice, and one justification (13)-second
that needs a one-line restatement to be visibly cancelable. No blocking site.

---

## 3. Packet-nondegeneracy section

[`TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md`](TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md),
lines 70-139 (the 2026-08-16 referee repair closing gap G1).

| Site | Displayed step | Verdict |
|---|---|---|
| :81-88 | setup: genuine edge into `X_w`, `D = T + f`, `B = X_w \ T`; "uses only that the edge is genuine, that `D` is common-safe, that valuations are strictly positive, and that `X` is globally lex-maximal" | **inequality suffices** — and the hypothesis list is now exactly right, with "strictly positive" reading as (0d) |
| :90-98, **(a)** | `v_w(D) = b_w + v_w(f) > b_w` for `D = X_w + f` | **inequality suffices** — only `v_w(X_w ∪ {f}) > v_w(X_w)` is consumed; `f ∉ X_w`, monotone + non-degenerate. Already flagged by the first sweep's "further flags"; **repair R3** |
| :100-103 | "excluded by BCFF Observation 2.10 at a maximum: negating the self-edge `w -> w` would force `v_w(X_w) > v_w(X_w+f)`, contradicting positivity" | **inequality suffices** — verified against Obs 2.10's actual statement (`2.Preliminaries.tex:326-350`, label `obs:non-champion-doesnt-envy-top-half`: "If `i` is not a champion of `j` and `j` is `g`-decomposed into `T_j ⊍ B_j`, then `X_i >_i T_j ∪ {g}`") at `i=j=w`, `B_w=∅`. BCFF's own contradiction here is monotone + non-degenerate |
| :103-110 | explicit route: `Y_w = X_w+f`; "the only new comparison any observer `i` makes is against `Y_w`, and `v_i(Y_w-g) = v_i(D-g) <= b_i = v_i(Y_i)` is precisely the common safety of `D`; the owner `w` strictly improves, so every comparison she made at the base still holds" | **inequality suffices** — observers: common safety verbatim. Owner: `v_w(Y_j - g) = v_w(X_j - g) <= b_w < v_w(Y_w)`, monotone. This makes (a) self-contained without Obs 2.10 |
| :110-113 | "a strict lexicographic improvement in **every** priority order" | **inequality suffices** — one utility up, all others fixed |
| :120-125, **(b)** | `T = ∅ => D = {f}` contradicts charity dominance | **inequality suffices** — no arithmetic |
| :131-135 | parenthetical derivation of charity dominance: "if `v_i({f}) > b_i`, replacing `X_i` by `{f}` is EFX — deleting the lone good leaves the empty set — improves `i`, and fixes everyone else" | **inequality suffices** — observers see `v_j(∅) = 0 <= b_j` (normalization); `i`'s own comparisons are `v_i(X_j - g) <= b_i < v_i({f})`, monotone |
| :39-48 | referee repair on the in-degree-one selected graph ("a second disjoint cycle would need two further genuine edges and none exist") | **inequality suffices** — counting argument |
| :50-54 | no genuine edge enters a singleton | **inequality suffices** — as ESCAPE:198-205 |

**Packet-nondegeneracy verdict: clean.** One decorative additive equality (R3), already noted
by the first sweep. The section is topology-independent and therefore discharges the
nonempty-packet hypotheses of items 1, 3 and 4 at the cancelable level.

---

## 4. The superseded region of `LENGTH_THREE_GLOBAL_LEX_TARGET.md` (lines 500-2800)

**Genuinely additive, pervasively — and not load-bearing for any order closure.**

The document's own header (:5-7) says the material below is "retained as proof-mining history
and are superseded by the two reservoir-order orientations", and :484-487 says "the
adaptive-singleton, parallel-root, augmented-root, hybrid-pair, and fractional-pivot sections
below are no longer completion gates". Independently confirmed: the reservoir-order escape
theorem uses only `W = X_q + B_r`, `U = X_r + B_q` and the thresholds `tau_r(D_p)`,
`tau_q(D_r)`; it never invokes `R = B_r + T_q`, the quota transversal, the dual-mode potential,
or the fractional pivot.

Representative additive sites, none repairable by C1/C2 and none needed:

| Site | Step | Why genuinely additive |
|---|---|---|
| :1395-1402, (16al) | `v_i(F) - v_i(B_k) > v_i(U(P,Q)) - b_i`, "it crosses both additive budgets" | differences of set values; no shared common part to cancel |
| :1860-1875, (16ak.6-7) | "Combining (16ak.2), (16ak.5), and **additivity of `U' = U - F + B_k`** yields ..."; "`v_r(B_k) - v_r(F) < vartheta'_r - v_r(U) <= 0`" | explicitly names additivity; arithmetic on differences |
| :2152-2160 | "the live anchored deficit is again one **additive demand** against two scalar prices" | knapsack framing |
| :2260-2275, (16ak.26-27) | `v_s(U_C) = T_s - v_s(C) >= b_s`; "Minimizing either cost subject to the **additive `l` threshold** is a fractional knapsack" | complement-value identity |
| :2598-2604 | `delta_q = b_q - v_q(A \ H)`, `delta_r = b_r - v_r(B \ H)`, "the strict **additive** deficits" | **structurally identical to the one genuinely additive site the first sweep found** (ADJACENT Theorem 2, eqs (14)-(15)) — the same `delta = b - v(D \ H)` quota construction |

This is a *stronger* form of the first sweep's finding, not a contradiction of it: the same
quota-arithmetic technique appears in both branches, and in both branches it sits in
intermediate contractions that close no priority order and are superseded by an
additivity-free theorem. The recommendation is the same: either attach an explicit additivity
hypothesis to these sections, or state that they are offered only inside the additive class.
Since they are explicitly labelled falsification history, a header note is enough.

The exact atomic motif audit (:2800-2828) is likewise additive by construction (`5^7`
enumeration over per-good values) and is explicitly "for discovery only" / "proves no packet
theorem". Not a dependency.

---

## 5. Machine-check scope — a correction in the strengthening's favour

`LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md:243` says of the 24-case replay: *"That audit
checks the **additive** inequalities."* Read
`tracks/parkability/decide_length_three_reservoir_order.py`. It is **not** an additive model.
Each bundle is represented by two scalars — a total and a `tail` (= `tau`) — with the only
constraints being `total > 0`, `0 <= tail < total`, `tail <= base`, plus the base envy/desire
signs. There is no per-good decomposition and no sum anywhere in the encoding. Those
constraints are exactly the monotone + non-degenerate + common-safety facts, so **the QF_LRA
replay certifies the aggregate argument at the cancelable level, not merely the additive one**.

Replayed on this branch to confirm it still reproduces: `status: ALL_FORCED, cases: 24`
(z3 5.0.0). **repair R5** is a one-word wording fix, and it makes the trust boundary stronger.

---

## 6. Cancelability-direction audit (the specific risk raised)

Systematic check for the pattern `v(S) > v(T) => v(S ∪ R) > v(T ∪ R)`, which single-good
cancelability alone does not give and monotonicity does not give either.

| Occurrences found | Where | Status |
|---|---|---|
| 1 | `LENGTH_THREE_GLOBAL_LEX_TARGET.md:86` (consumed at :398, eq (13) first) | **licensed by tool C2** — cancelable + non-degenerate makes set-cancelation a biconditional (BCFF `2.Preliminaries.tex:101`), and BCFF use the identical move at `3.NewTechniques.tex:460`, `:480`, `:649` |
| 1 (apparent) | `LENGTH_THREE_GLOBAL_LEX_TARGET.md:398-410`, eq (13) second | **not actually reverse-direction** once restated — see repair R4; the currently displayed justification sums two disjoint-part inequalities, which is neither C1 nor C2, but the conclusion follows from C2 plus the no-envy row (4a) |
| 0 | length-two chain | — |
| 0 | packet-nondegeneracy section | — |
| 0 | reservoir-order escape theorem | — |

No step anywhere in the two chains requires a direction of cancelability that the class does
not supply.

---

## 7. Overall verdict

> **The two-nonsingleton composition strengthens from additive to BCFF's full nice-cancelable
> valuation class: YES.**

Blocking sites: **none.**

Summary by branch, merging this sweep with the first one:

| Branch | Order-closing steps needing additivity | Notes |
|---|---|---|
| length two | none | one decorative phrase (R1) |
| length three | none | two decorative equalities (R2), one restatement (R4), all in superseded or non-load-bearing positions |
| adjacent-4 | none | first sweep; Thm 2 (14)-(15) additive but intermediate and superseded |
| alternating-4 | none | first sweep |
| packet nondegeneracy | none | one decorative equality (R3) |

"Nice" is consumed only at the Lemma A.1 step, which is where the corpus already invokes it,
and A.1's cancelable witness is exactly what the argument needs. The corpus's headline framing
("four positive, nondegenerate **additive** agents",
`TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md:10`) understates what has been proved.

### Recommended repairs (reported, not applied — this sweep is read-only outside this file)

| | File:line | Fix |
|---|---|---|
| R1 | `TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md:47-48` | "Positive additivity makes owner `a` strictly prefer the pair" -> "Monotonicity and non-degeneracy make owner `a` strictly prefer the pair" |
| R2 | `LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md:53` and `:99`; `LENGTH_THREE_GLOBAL_LEX_TARGET.md:282` | replace `v_q(W) = b_q + v_q(B_r) > b_q` by `v_q(W) > v_q(X_q) = b_q` (and likewise for `U`) |
| R3 | `TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md:96` | replace `v_w(D) = b_w + v_w(f) > b_w` by `v_w(D) = v_w(X_w ∪ {f}) > v_w(X_w) = b_w` |
| R4 | `LENGTH_THREE_GLOBAL_LEX_TARGET.md:406-410` | rewrite the justification of `v_p(R) < v_p(D_p)` as: `v_p(T_q) < v_p(T_r)` gives `v_p(R) < v_p(X_r)` by cancelability, and `v_p(X_r) <= b_p < v_p(D_p)` by (4a) and desiredness. Drop the appeal to `v_p(f) > v_p(B_r)` |
| R5 | `LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md:243` | "That audit checks the additive inequalities" -> "That audit checks the aggregate threshold inequalities; its encoding uses only bundle totals and deletion maxima, so it is valid for cancelable valuations" |
| R6 | `LENGTH_THREE_GLOBAL_LEX_TARGET.md:5-7` and `:484-487` | add "these superseded sections are additive-only" to the existing supersession notice |
| R7 | `TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md:10`, `:175-177` | once R1-R4 land, the class hypothesis can be widened from "additive" to "nice cancelable" |
| R8 | `LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md:20`, `:80-83` | the note "the additive respecting nondegenerate perturbation actually run here is folklore, not A.1" can be dropped: no additive perturbation is needed, A.1's cancelable witness suffices |

---

## 8. Scope statement (honest boundary)

1. **What was swept.** Every displayed value computation, equality and inequality in
   `TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md` (all 159 lines),
   `LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md` (all 245 lines),
   `LENGTH_THREE_GLOBAL_LEX_TARGET.md` lines 1-500 (the load-bearing normal form and the
   reservoir lemmas), and the packet-nondegeneracy section of
   `TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md` (lines 70-139), on branch
   `codex/efx-gg-cycle-referee-20260812`.

2. **What was sampled, not swept.** `LENGTH_THREE_GLOBAL_LEX_TARGET.md` lines 500-2800. These
   are declared superseded by the document itself and are not reachable from the
   reservoir-order theorem. They were characterised by targeted inspection at five sites, not
   line-by-line. If any of that material is ever revived as load-bearing, it must be re-swept;
   the sampling found it uniformly additive.

3. **What was NOT re-derived.** BCFF's own lemmas. The claim "every BCFF import is available at
   the nice-cancelable level" rests on BCFF's stated scope (`1.Introduction.tex:207`) plus
   spot-checks of the proofs of Obs 2.8, 2.9, 2.10, 2.11, Lemma 3.13, Lemma 3.14 and the
   structure of Thm 3.16 — not on re-proving them.

4. **Verdict granularity.** "Inequality suffices" means: the step is derivable from monotone +
   normalized + cancelable + non-degenerate, using at most tools C1/C2 of §0, together with
   whatever structural facts (common safety, desiredness, base EFX, global lex-maximality, PI
   routing) the step already cites. It does **not** mean the step was re-verified against a
   formal proof assistant.

5. **What this does not establish.** The correctness of the four cycle-class theorems
   themselves. This sweep is about *which valuation hypotheses* their proofs consume, not about
   whether those proofs are right. The independent referee checks recorded in the dependency
   ledger — in particular the length-two BCFF Theorem 3.16 interface — remain outstanding.

6. **Nondegeneracy convention.** As in the first sweep, and now confirmed verbatim against
   BCFF `2.Preliminaries.tex:76`: distinct bundles receive distinct values. Every "positivity"
   appeal in the corpus is monotonicity upgraded to strictness by this.
