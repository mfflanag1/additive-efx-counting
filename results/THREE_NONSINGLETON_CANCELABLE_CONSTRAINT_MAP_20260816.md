# Three-nonsingleton (GG flower) cancelable-class constraint map — 2026-08-16

**This is not a widening claim.** The three-nonsingleton rung is OPEN: terminals `T_0` and
`T_{L,⊥}` are live, and `T_{L,×}` (floor-reset/supplier-star) was retired on 2026-08-16 after
the referee round (`TLX_CLOSURE_REFEREE_REPORT_20260816.md`, GAP FOUND) and the exhaustive
successor model check (`TLX_SUCCESSOR_MODEL_CHECK_20260816.md`, retirement recommended). The
retired floor-reset documents were not swept beyond noting that status.

What follows is a **forward-looking constraint map**: if and when the rung closes, which of its
components could inherit BCFF's nice-cancelable class, and which lemmas would need cancelable
re-proofs first. Method and verdict vocabulary are those of the two-nonsingleton passes
(`CANCELABLE_CLASS_SWEEP_20260816.md`), including the second-pass rule that **each file's own
`tau` and valuation conventions are recorded as found, with no normalizing preamble**.

---

## 0. Headline

**The GG rung is NOT additive-bound as a whole, but it is additive-bound where it counts.**

Of 40 files in the closure: **19 inequality-sufficient, 14 mixed, 3 additive-bound, 4
additive-by-design witnesses**. Most displayed additive arithmetic is decorative or exactly
restatable — 8 of the 14 "mixed" files are mixed only in notation. But three mechanisms have
**no cancelable analogue at all**, and one of them is the rung's currently-named live gate.

The decisive structural fact is not a per-lemma one. It is that this rung **represents the EFX
tail as (total, minimum)** — the additive parametrization `tau_i(Z) = v_i(Z) - m_i(Z)` — and
builds a first-class increment operator `kappa` on top of it. The two-nonsingleton corpus
converged on max-deletion `tau`; the GG rung is built on the additive form. That is a
different foundation, not a different notation.

---

## 1. Closure computation

Transitive citation closure from five seeds (the census, the contraction target, and the three
flower lemmas named in the task), chasing every `*.md` reference. **Closure: 40 files, 5,819
lines, zero dangling references** — a genuinely self-contained rung.

Seeding instead from `GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md` (the later Aug-12+ GG
cycle-class layer) blows up to **294 files**, i.e. essentially the whole 397-file repository,
because that document cites `README.md` and `GENERAL_EFX_GOAL_20260730.md`, which index
everything. That is citation transitivity, not dependency, so it is not a usable closure and
the 40-file Aug-9/11 flower closure is the right object. The later GG layer sits on top of this
one and would inherit whatever class this one supports.

### Correction to the second-pass report

`CANCELABLE_CLASS_SWEEP_20260816.md` §B.4 states that
`ROOT_CRITICAL_ALTERNATING_FRONTIER_LEMMA_20260811.md` and
`ALTERNATING_PAYMENT_COMPENSATION_CHAIN_LEMMA_20260810.md` are "cited by exactly three files:
`README.md`, `GENERAL_EFX_GOAL_20260730.md`, and `THREE_NONSINGLETON_CONTRACTION_TARGET_20260809.md`".
That sentence came from a grep that OR-ed both filenames, so the three hits are the union across
the pair, not the citers of each. Corrected, per file:

- `ALTERNATING_PAYMENT_COMPENSATION_CHAIN_LEMMA_20260810.md` — cited by the roadmap and by
  `THREE_NONSINGLETON_CONTRACTION_TARGET:192`. **In this closure** (depth 1). Swept below.
- `ROOT_CRITICAL_ALTERNATING_FRONTIER_LEMMA_20260811.md` — cited by **`README.md` only**. It is
  an **orphan**: not reached from the two-nonsingleton seeds *and* not reached from the GG-flower
  seeds either. Its own opening cites a "root-critical compensator dichotomy" (
  `ROOT_CRITICAL_COMPENSATOR_DICHOTOMY_LEMMA_20260811.md`), which is likewise outside this closure.

The out-of-cover **conclusion** for the two-nonsingleton composition is unaffected — neither file
is reachable from those seeds. Only the evidence sentence was wrong, and `ROOT_CRITICAL` is more
isolated than reported, not less.

---

## 2. The additive spine (rung-level finding)

Three linked commitments, none of which is a local notation choice.

**(S1) The tail is parametrized as (total, minimum).**
`THREE_NONSINGLETON_CYCLE_CENSUS:289-296`, "Cap-free packet-minimum support theorem":

> "The exact minimum of a union of nonempty packets is the minimum of their packet minima.
> Introducing one arbitrary total and one arbitrary positive minimum per nonempty packet
> therefore represents every displayed **EFX tail** exactly, without bounding packet cardinality."

Representing the tail by `(v_i(Z), m_i(Z))` *is* the additive form `tau_i(Z) = v_i(Z) - m_i(Z)`.
Under max-deletion `tau_i(Z) = max_{g in Z} v_i(Z\{g})`, the tail is **not** a function of the
total and the minimum, so this representation is exact only under additivity. Every 864-cell,
148/284, and payment-menu audit in the rung is computed inside this abstraction. This is an
**evidence-base** dependency: it does not by itself make an analytic lemma additive, but it means
the rung's machine corroboration certifies additive instances only — the opposite of the
two-nonsingleton situation, where the QF_LRA replay turned out to encode totals and deletion
maxima and therefore already certified at cancelable generality.

**(S2) The additive-form `tau` is written out explicitly in three files.**

| Site | Identity |
|---|---|
| `FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY:61-63` (5) | `tau_i(W) = v_i(B_q) + v_i(L) - m_i(B_q+L)` |
| `LEX_ROOTED_OWNER_CHARITY_DONATION_OBSTRUCTION:68-71` | `tau_i(R+x) = v_i(R) + max{v_i(x) - min_{z in R} v_i(z), 0}` |
| `FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION:103-105` | `tau_i(C+P) = tau_i(C) + kappa_i(C,P)` |

All three are **false under max-deletion `tau`**.

**(S3) `kappa` is a cross-file first-class operator.**
`kappa_i(C,P) = v_i(P) + m_i(C) - min{m_i(C), m_i(P)}` appears at
`FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION:57-59` and again, independently derived, at
`CHARITY_ROOTED_HUB_SPLIT_OBSTRUCTION:81-89`, where the delivered leaf-wall normal form (4) is
stated *in terms of it*: `kappa_i(k,R_k) > gamma_i + s_{ik}`. Downstream consumers take that
form literally. **A cancelable re-proof must eliminate `m_i` and `kappa`, not translate them,
and must do so in all three places at once.**

---

## 3. Derived tools used, and the exact fault line

Beyond C1 (iterated set-cancelation) and C2 (the biconditional, licensed by cancelable +
non-degenerate, stated in BCFF's Preliminaries), this sweep established and used:

> **C3 (matched-pair union) — VALID.** If `v(A)>v(B)` and `v(C)>v(D)` with `{A,B}` disjoint from
> `{C,D}`, then `v(A∪C) > v(B∪D)`. Route: `v(A∪C) > v(B∪C)` by C2 with `R=C`, then
> `v(C∪B) > v(D∪B)` by C2 with `R=B`.

C3 recovers most "sum of two inequalities" steps, which is why so many additive-looking files
came back inequality-sufficient. **The fault line is what C3 cannot do:**

1. **Subtraction / decomposition.** From `v(A∪B) > v(C∪D)` together with `v(B) > v(D)`, conclude
   `v(A) > v(C)`. No cancelable analogue. (C3 combines; it does not decompose.)
2. **Set value against a scalar built from differences** — `delta`, `sigma`, `gamma`, `epsilon`,
   `s_{ij}`. No set realizes the scalar.
3. **The minimum-good operator `m_i`** and the `kappa` increment.
4. **Additive objectives over independent choices** — subset-sum, knapsack, minimum-cost
   matching, LP duality.

This also confirms, on re-examination, that the two-nonsingleton verdict on **adjacent Theorem 2
stands**: its `v_p(H_p) > delta_p` is category (2), a set value against a difference-scalar, which
C3 does not touch.

---

## 4. Tally

| Verdict | Count | Meaning |
|---|---|---|
| **INEQUALITY-SUFFICIENT** | **19** | every displayed step recovers under monotone + normalized + cancelable + non-degenerate |
| **MIXED** | **14** | conclusions recover; some displayed steps or emphasized margins do not |
| **ADDITIVE-BOUND** | **3** | a load-bearing mechanism has no cancelable analogue |
| **WITNESS-ADDITIVE-OK** | **4** | counterexample/refutation; additive is correct and strictly stronger |
| | **40** | |

Of the 14 MIXED, **8 are mixed in notation only** (every load-bearing use has an exact cancelable
restatement, verified site by site); the other 6 carry an additive statement that is emphasized
but not consumed by the file's own conclusion.

---

## 5. Per-file inventory

`tau` column records the convention **as found**. "unused" = the symbol never appears;
"inherited" = used without definition.

### 5.1 Seeds and architecture

| File | `tau` | Scope line (verbatim) | Verdict |
|---|---|---|---|
| `THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809` | **additive form**, via the (total, minimum) support theorem at :289-296; `theta_u = max_j tau_u(Y_j)` at :208 is convention-agnostic | :10 "four **positive, nondegenerate additive** agents" | **MIXED** — the eight-class census (:27-56), return-edge reduction (Lemma 1), Corollary 2, the flower normal form, Lemma 3, and **Lemma 7 (payment menu, :241-268)** are all class-independent; the (total,min) abstraction layer and every audit computed in it are additive |
| `THREE_NONSINGLETON_CONTRACTION_TARGET_20260809` | unused | :11 "four **positive, nondegenerate additive** agents" | **MIXED (research log)** — a chronological log whose every entry is *stated* in additive arithmetic (`sigma=q(f)-q(R)` :166; `q(f)>q(E)+q(X_a)` :204; `r(K_T)>r(B_q-K_B)+r(X_a)` :238; `q(X_a)<q(K)<q(X_q)-q(f)` :153). Per §6 most of these restate; the log is a summary surface, not a proof |

### 5.2 Flower core (10)

| File | `tau` | Verdict |
|---|---|---|
| `FLOWER_EARLY_ROOT_CHARITY_ROTATION_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — the dichotomy at :62-66 is C2 with `R=T_r` |
| `FLOWER_LATER_OWNER_SINGLE_REPLACEMENT_SELECTOR_LEMMA_20260810` | inherited; `tau_q(D_r)=v_q(T_q)` at :50-54 is phrased in the additive "minimum good" idiom but **holds under max-deletion too** via C2 | **INEQUALITY-SUFFICIENT** (one decorative additive display at :59-61) |
| `FLOWER_COMPLEMENT_RETURN_AUGMENTATION_LEMMA_20260810` | unused | **MIXED** — structural branches 1-4 clean; §"Quantitative capture" (6)-(7) additive-bound (`delta`, `epsilon_a`) |
| `FLOWER_DUAL_FULL_CAPTURE_ESCAPE_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** (one decorative display at :77-79) |
| `FLOWER_EXTERNAL_RETURN_AUGMENTATION_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — cleanest file in the rung |
| `FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810` | **additive form** (`kappa` identity :103-105) | **MIXED** — rotation, dichotomy, and the **threshold-form wall** (:99-101, convention-agnostic) recover; the `kappa` re-expression (4)/(5) does not |
| `FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810` | **additive form, explicit** (:61-63) | **ADDITIVE-BOUND** |
| `FLOWER_THREE_ROTATION_POLARITY_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — all three rotations recover via C1/C2/C3 despite "subtraction" prose at :76-78 |
| `FLOWER_TWO_ROOT_RESIDUAL_SPLIT_RESPONSE_HALL_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** |
| `CROSS_STAR_HOLE_PIVOT_LEMMA_20260811` | **max-deletion**, used implicitly and correctly | **INEQUALITY-SUFFICIENT** |

### 5.3 Packet-replacement / root-flip / payment chain (10)

| File | `tau` | Verdict |
|---|---|---|
| `PACKET_REPLACEMENT_COMPLEMENT_RETURN_LEMMA_20260810` | inherited (:31) | **MIXED** — `Delta_a` scalar (:113) propagates to 5 files; (8) restates as `v_q(K∪{f})<v_q(X_q)`; **(11) payment-packet existence is the real gap** |
| `PACKET_REPLACEMENT_AGGREGATE_ROOT_FLIP_POLARITY_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — (4) fully recovered via C2 |
| `PACKET_REPLACEMENT_CHARITY_ABSORPTION_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — no additive arithmetic anywhere |
| `MAXIMAL_REPLACEMENT_FRONTIER_EXCHANGE_LEMMA_20260810` | unused | **ADDITIVE-BOUND** — the `sigma`-gap (:60, :71) |
| `ALTERNATING_PAYMENT_COMPENSATION_CHAIN_LEMMA_20260810` | unused | **MIXED** — termination is pure finiteness (:50-57); (1) `v_q(T_r)>Delta_a` irreducible in the Q-wall branch; (Q*) at :110 fully recovered via C1 |
| `Q_EXHAUSTION_ROOT_SWITCH_LEMMA_20260810` | unused | **MIXED** — conclusion survives (the used consequence `v_q(f)>v_q(E)` recovers via C2+C1); the emphasized three-term margin (3) does not |
| `RELEASED_OWNER_COMPENSATION_CHAIN_LEMMA_20260810` | unused | **MIXED** — terminal wall (R+) at :78 is already cancelable-clean; (4) margin gloss is not |
| `FULL_RESERVOIR_R_WALL_TOP_CAPTURE_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — the rung's most surprising result: additive notation throughout, nothing additive consumed. Its ":91-95 Cancel `T_q\K_T` from (7)" *is literally* C1 |
| `TOP_CORE_ROOT_EXCHANGE_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** |
| `TOP_CORE_RESIDUAL_RESET_LEMMA_20260811` | unused | **MIXED** — everything the factorization consumes recovers; the one irreducible step (4) at :49-53 is a **decomposition** (category 1) and is explicitly not consumed (:98-101) |

### 5.4 Hall / response-compression / component growth (10)

| File | `tau` | Verdict |
|---|---|---|
| `CHARITY_ROOTED_TRANSFER_TREE_RESPONSE_HALL_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — zero value arithmetic |
| `OPEN_LEAF_SOURCE_ROTATION_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — (6)/(7) fully recover via C1 |
| `OUTSIDE_SOURCE_SINK_AUGMENTATION_LEMMA_20260810` | unused | **MIXED (repairable)** — `gamma_a` restates; termination is the class-independent count "at most three times" (:104-105), not the margin |
| `OWNER_ROOTED_HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** — both improvement checks are clean C2 |
| `ALL_OWNER_HALL_RESPONSE_COMPRESSION_LEMMA_20260811` | unused | **MIXED** — everything proved recovers; only the failure certificate (7) at :103-105 is additive, and it feeds the open continuation |
| `WEIGHTED_RESPONSE_COMPRESSION_DUAL_LEMMA_20260811` | unused | **ADDITIVE-BOUND** |
| `LEX_SACRIFICED_RESPONSE_COMPRESSION_LEMMA_20260811` | inherited (:70), convention-agnostic use | **MIXED (strongly repairable)** — all deliverables recover; see §7.2 |
| `ROOT_ANCHORED_COMPRESSION_STAR_LEMMA_20260811` | inherited (:47), convention-agnostic use | **INEQUALITY-SUFFICIENT** — including the finiteness argument at :74-75 |
| `MINIMAL_HALL_OWNER_UNION_COMPRESSION_LEMMA_20260811` | unused | **INEQUALITY-SUFFICIENT** — pure Hall combinatorics; its additive hardened adversary is explicitly "not used in the analytic proof" (:116) |
| `HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810` | unused | **INEQUALITY-SUFFICIENT** |

### 5.5 Obstructions, infrastructure, refutations (8)

| File | Type | `tau` | Verdict |
|---|---|---|---|
| `LEX_ROOTED_OWNER_CHARITY_DONATION_OBSTRUCTION_LEMMA_20260810` | positive | **additive form, explicit** (:68-71) | **MIXED** — all four wall classifications and the conclusion recover; the `tau`-monotonicity *proof step* is additive (see §7.2) |
| `CHARITY_ROOTED_HUB_SPLIT_OBSTRUCTION_LEMMA_20260810` | positive | **additive form** via `kappa` (:89), explicit `m_i` (:74-76) | **MIXED** — hub wall, PI/release, Hall reduction recover; **leaf wall (3)-(4) additive-bound and consumed downstream** |
| `GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA` | positive | **opaque / convention-agnostic** — only `tau_i(∅)=0` | **INEQUALITY-SUFFICIENT** — see §6.0 |
| `THREE_TARGET_HUB_HALL_CLASSIFICATION_20260810` | unused | — | **INEQUALITY-SUFFICIENT** (class-independent: pure directed-graph enumeration) |
| `FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810` | refutation | unused | **WITNESS-ADDITIVE-OK** (+ a class-independent positive sub-argument at :22-33: "edge existence alone is not release compatibility") |
| `FIXED_REPLACEMENT_LEX_COMPLETION_REFUTATIONS_20260810` | refutation | unused | **WITNESS-ADDITIVE-OK** |
| `ARM_OWNER_HUB_SELECTOR_REFUTATION_20260810` | refutation | unused | **WITNESS-ADDITIVE-OK** |
| `LEAF_MUTUAL_TRAP_SCALAR_GATE_REFUTATION_20260810` | refutation | unused | **WITNESS-ADDITIVE-OK** — self-declared ":5 exact **additive** refutation" |

**Refutation disposition.** All four refutations still refute under a widened class, trivially:
additive ⊂ nice cancelable, so an additive countermodel to a universally-quantified shortcut
refutes it over any superclass. None draws a positive mathematical corollary from its witness.
**Zero additive dependencies counted against a future widening from this group.**

---

## 6. What is already class-independent (the good news)

**6.0 The rung's general infrastructure theorem is clean.**
`GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA` opens "Fix positive-additive valuations", but its
item-3 "component-additive" property is additivity of a **defined potential over a partition of
agents**, not additivity of `v` over goods. The file says so itself at :99-102: *"Theta is a sum
of one term depending only on each owner's own bundle … **No linearity of the threshold function
inside a bundle is required**."* It leaves `tau` opaque apart from `tau_i(∅)=0`, which makes it
the one file where an undefined `tau` is a virtue. Its scope line is inherited framing, exactly
like `ALTERNATING_EASY_PRIORITY_ESCAPE_LEMMA:4` in the two-nonsingleton corpus.

Also class-independent, and worth protecting in any re-proof:

- the **eight-class cycle census** and the **length-two flower reduction** (census :27-110) —
  pure BCFF Obs 2.8 / Thm 3.16 / Def 3.4 structure;
- **Lemma 7, the payment menu** (census :241-268) — reasons only about *strict orderings of
  bundles*, never about magnitudes. This is the template for what a cancelable proof in this
  rung looks like;
- every **response-Hall / SDR ⟹ PI** argument in the rung (7 files) — pure combinatorics;
- **`ROOT_ANCHORED_COMPRESSION_STAR`'s exclusion of `r` as the missing source**, and
  **`MINIMAL_HALL_OWNER_UNION`'s deficiency-one theorem** — both survive any widening unchanged;
- the three **termination arguments** that matter: finiteness of allocations
  (`ROOT_ANCHORED:74-75`), the counting bound "at most three times" (`OUTSIDE_SOURCE:104-105`),
  and monotone packet growth (`ALTERNATING_PAYMENT_COMPENSATION:50-57`). None needs a numeric
  potential.

---

## 7. Lemmas needing cancelable re-proofs, ranked by load-bearing weight

**Rank 1 — `WEIGHTED_RESPONSE_COMPRESSION_DUAL_LEMMA_20260811` (:17-72).**
The minimum-cost assignment selector and its LP dual. Irreducible and central. An assignment
problem minimizes `Σ w_ij` over independent edges; a cancelable valuation supplies a total order
on bundles but **no additive objective**, so neither the minimum-cost selector (3) nor strong
duality (4)-(6) is even well-posed off additivity. `THREE_NONSINGLETON_CONTRACTION_TARGET:376`
names contradicting this weighted dual as a live proof obligation — **so the rung's currently
advertised route to closure is, as stated, an additive-only route.** A cancelable re-proof must
replace the weighted matching with an order-theoretic selector, not translate it.

**Rank 2 — the `kappa` / `m_i` spine, in three files at once.**
`CHARITY_ROOTED_HUB_SPLIT_OBSTRUCTION:74-95` (leaf wall (3)-(4), a *delivered output* consumed
literally downstream), `FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION:57-59,103-105` (the wall's
`kappa` form), `LEX_ROOTED_OWNER_CHARITY_DONATION_OBSTRUCTION:68-71` (the third variant). The
semantic walls behind all three (`tau_i(X_k ∪ R_k) > v_i(Y_i)`, `tau_i(B_q+L) > tau_i(B_q+T_q)`)
**are** cancelable-expressible; only the `kappa`/`gamma`/`s` re-expressions are not. Fixing this
is mostly a matter of changing what the lemmas deliver.

**7.2 — the highest-value single repair, already identified.** `LEX_ROOTED:68-74` and
`CHARITY_ROOTED:55-59` both prove "the wall forces the swapped-in good to be worth more" via the
additive `tau` formula, and **both recover by the same route**: apply C2 to each deletion term
and take pointwise maxima. One repair pattern converts two additive proof steps in two
load-bearing lemmas. Independently, `LEX_SACRIFICED_RESPONSE_COMPRESSION:30-42` already converts
the weighted dual's additive certificate into the plain set comparison (4) `v_d(C) > v_d(E)` —
**that is the natural starting point for the Rank-1 re-proof.**

**Rank 3 — `FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810` (:55-80).**
The chain (1)→(4)→(5)→(6) produces `v_i(B_q) > 2·v_i(R) - m_i(L+R) + m_i(B_q+L)`. The **doubled
`2·v_i(R)`** is the signature: cancelability compares sets and can never produce a doubled term.
No route was found — the best cancelable chain yields only `v_i(R) < v_i(B_q ∪ L)`, strictly
weaker than the conclusion (2) `v_i(B_q) > v_i(R)`.

**Rank 4 — the census's (total, minimum) abstraction layer** (§2 S1). Affects the rung's entire
machine-checked evidence base — the 864-cell enumeration, the 148/284 split, the payment-menu
audit — rather than any analytic lemma. A cancelable rung would need its audits re-encoded
against bundle totals and deletion maxima, the way the two-nonsingleton QF_LRA replay already is.

**Rank 5 — `MAXIMAL_REPLACEMENT_FRONTIER_EXCHANGE_LEMMA_20260810` (:30, :60, :71).**
The `sigma`-gap: "every improving exchange jumps by more than `sigma`". The file names this as
its own useful content. The qualitative frontier (a value-maximal choice exists; every nonempty
residual packet crosses it) is fully cancelable; the *quantitative gap* is not.

**Rank 6 — payment-packet existence.** `v_q(T_r) > Delta_a`
(`PACKET_REPLACEMENT_COMPLEMENT_RETURN:126`, `ALTERNATING_PAYMENT_COMPENSATION_CHAIN:22`). Every
*use* of `Delta_a` in a compensation system has an exact C1 restatement, so `Delta_a` is a
notation problem — except here. The cancelable form `v_q(T_r ∪ X_a) > v_q(K)` is derivable only
when `v_q(X_a) ≥ v_q(f)`, i.e. **precisely outside the Q-wall branch these lemmas exist to
handle.**

---

## 8. Convention and bookkeeping defects found

1. **`tau` is undefined almost everywhere.** Of 40 files, 4 state a `tau` convention
   (3 additive-form, 1 opaque), 1 uses max-deletion implicitly and correctly
   (`CROSS_STAR_HOLE_PIVOT`), 4 use `tau` inherited-undefined, and the rest never mention it. The
   "unstated convention" defect flagged for `ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY` in the
   two-nonsingleton second pass is **near-universal here**.
2. **A live convention conflict inside the rung.** `FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION` and
   `FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY` use additive-form `tau`; `CROSS_STAR_HOLE_PIVOT` uses
   max-deletion. They are the same only under additivity. The first pair composes internally, so
   nothing is currently broken — but this is exactly the shape of the defect that blocked the
   two-nonsingleton gate.
3. **Valuation class is declared in only 8 of 40 files.** The other 32 declare a status line and
   inherit the class silently from the seeds. Notably `WEIGHTED_RESPONSE_COMPRESSION_DUAL` — the
   single most additive-bound file in the rung — **declares no class at all**.
4. **Wrong-axiom attributions**, same shape as those found in the earlier passes:
   `PACKET_REPLACEMENT_CHARITY_ABSORPTION:82` and `CHARITY_ROOTED_HUB_SPLIT:32` and
   `OWNER_ROOTED_HUB_SPLIT:41` and `ROOT_ANCHORED:50` credit "positivity" for steps that need
   monotonicity + non-degeneracy; `PACKET_REPLACEMENT_COMPLEMENT_RETURN:73` credits "additivity"
   for a step that is **C2**.
5. **`GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA` has no Date and no Status line** — the only
   file in the closure lacking them, and it is the rung's most reusable infrastructure theorem.

---

## 9. Forward-looking verdict

> **If the GG rung closes along its currently advertised route, it will be ADDITIVE-BOUND.**
> That route runs through the weighted response-compression dual (Rank 1), whose selector and
> obstruction certificate have no cancelable analogue.
>
> **The rung is not intrinsically additive.** 19 of 40 files are already inequality-sufficient,
> 8 more are additive in notation only, and the rung's general infrastructure theorem, its cycle
> census, its flower reduction, all its response-Hall/PI machinery, and all three of its
> termination arguments are class-independent. A cancelable closure is not ruled out — it is
> blocked by three identified mechanisms and one abstraction layer, in that order of difficulty.

Practical consequence: the decision is **cheapest to make now, while the rung is open**. Ranks 1
and 2 are the ones that would force a re-proof rather than a rewrite; if a cancelable rung is
wanted, the weighted-matching selector should be replaced before more lemmas are built on it,
and `LEX_SACRIFICED_RESPONSE_COMPRESSION:30-42` already shows the order-theoretic form that
replacement would take.

---

## 10. Scope statement

1. **Swept:** all 40 files of the flower closure, in full — 5,819 lines. The 38 lemma files were
   swept in four parallel batches under the second-pass conventions; the two seeds were read
   directly.
2. **Not swept, by instruction:** the retired `T_{L,×}` floor-reset documents, beyond recording
   their status. Also not swept: the later Aug-12+ GG cycle-class layer
   (`GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md` and the retired-root-support-ledger
   cluster), which sits above this closure and would inherit its class. If the live terminals
   `T_0` and `T_{L,⊥}` are pursued, their own documents need this treatment.
3. **Not re-derived:** BCFF's lemmas (unchanged from the earlier passes), and every frozen JSON
   audit and solver core in the rung — all of which are additive by construction, which is
   itself the Rank-4 finding.
4. **"Inequality suffices" means** derivable from monotone + normalized + cancelable +
   non-degenerate using at most C1/C2/C3, together with the structural facts the step already
   cites. It does **not** mean the step was verified against a proof assistant.
5. **This map says nothing about whether the rung's lemmas are correct.** It records which
   valuation hypotheses their proofs consume. The rung is open and several of its files carry
   their own "remains open" status lines.
