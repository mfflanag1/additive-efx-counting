# BCFF import audit — arXiv:2102.10654 vs. this corpus (2026-08-16)

Independent audit of every EXTERNAL-TRUSTED import, checked against the arXiv LaTeX
e-print (both versions pulled; theorem counter reconstructed from source honoring the
`\fullversion`/`\shortversion` build guards — no ar5iv/markdown paraphrase risk).

**OVERALL: the EXTERNAL-TRUSTED surface is FAITHFUL.** Every numbered import resolves to
the intended statement. One real DRIFT (Lemma A.1, provenance not mathematics), two
bookkeeping defects, one process observation.

## Version pin (load-bearing)

Corpus numbering matches the **arXiv FULL build** (`\fulltrue`); v1 (2021-02-21) and v2
(2021-02-28) have identical Section 2/3 environment sequences (diffed), so pin = "arXiv
full version, v1 = v2". The AAAI-22 short build (`\fullfalse`) drops Def 2.2, Ex 2.5,
Def 2.7 and renumbers Section 2: "Lemma 2.4" would be a Definition, "Definitions 2.6-2.7"
Observations, and "Observation 2.10" would NOT EXIST. All Section-2 citations are coherent
only under the full arXiv version — and under it, all are correct. The audits should state
this pin explicitly.

## Per-statement verdicts

1. **Lemma 2.4 — MATCH** (k → k−1 unallocated converter; its "moreover" clause = the
   corpus's unenvied-charity input). Global-lex maximality is not in 2.4's statement; the
   audits correctly mark that row derived, not EXTERNAL-TRUSTED.
2. **Definitions 2.6–2.7 — MATCH**, caveat: the primitive "most envious of S" lives in
   UNNUMBERED prose (its definition environment is commented out in both builds); 2.6-2.7
   is the best available citation but incomplete provenance.
3. **Definitions 3.1–3.4 + Lemma 3.5 — MATCH**; nit: 3.3 is an Example — cite
   "Definitions 3.1, 3.2 and 3.4". Def 3.4's H-disjointness/release clauses verified
   clause-by-clause on the corpus's length-two PI instance (valid). Corollary 3.6 is an
   immediate consequence of 3.4+3.5 (covered).
4. **Observation 2.10 — MATCH.** Instantiation i=j=w with B_w=∅ checked: w must
   self-f-champion, exactly the packet-nondegeneracy claim; strictness = nondegeneracy +
   the paper's standing monotonicity ("positivity").
5. **Definition 3.9 (good g-cycle) — MATCH, all clauses verified** on the 2-cycle {r,q}.
   No chordlessness beyond clause 3, no distinct-source condition, no constraint on agents
   off the cycle. Nothing the length-two configuration does can violate it. (Clause 1,
   r≠q, is left implicit by the corpus — harmless.)
6. **Theorem 3.16 — MATCH**, sole hypothesis "C is a good g-cycle", no length restriction
   (Lemmas 3.13/3.14 valid at k=2). The corpus's length-two specialization is verbatim
   BCFF's own argument (Thm 5.1 proof Case 1, four agents; Lemma 6.2 proof Case 1). The
   "only good internal B_r-edge" claim independently re-derived (Obs 3.11 kills H∩S≠∅
   targets; Obs 2.11 + cancelability kills the self-edge). TRAPPED_SOURCE:159's Lemma 6.2
   citation correct in full-version numbering. Cor 3.18 correctly stated and correctly
   NOT relied on (two outside singletons defeat its single-outsider use). Benign
   ambiguity: Def 3.15's "three agents" — under the distinct reading no good edge exists
   on a 2-cycle and 3.16 forces external immediately; corpus conclusion holds either way;
   BCFF itself uses the non-distinct reading.
7. **Lemma A.1 — DRIFT (the one real finding; most-cited import, 18 mentions).** A.1
   delivers exactly: non-degeneracy, a CANCELABLE (not necessarily additive) witness, and
   one-directional transfer EFX(v') ⟹ EFX(v). The corpus over-describes it three ways:
   (a) ADDITIVITY — ADJACENT_LARGE:421 and LENGTH_THREE_GLOBAL_LEX_TARGET:2848-2850 claim
   an "additive" perturbation; A.1 says cancelable. Additive-respecting-nondegenerate
   perturbations exist but that is folklore/Chaudhury et al., not A.1.
   (b) POSITIVITY — audit rows attribute positivity to A.1; it says nothing about it.
   Correct attribution: "A.1 + standing monotonicity".
   (c) ROUND TRIP — transfer carries ONLY EFX-ness, one-directionally; not lex-maximality,
   the normal form, or the champion graph. ONE_LARGE:276-281 states this correctly; the
   three audit tables' one-line gloss does not.
   DOES NOT reopen conditional status: everything is defined inside the perturbed profile
   and only the final EFX allocation transfers back — exactly what A.1 licenses; the
   load-bearing reservoir premises need only the strict inequality (monotonicity +
   nondegeneracy), not the additive equalities. RESIDUAL RISK: sweep the
   alternating/adjacent proofs for any step genuinely needing additivity — such a step
   currently rests on a citation that does not support it.
8. **UNLISTED IMPORT — Observation 2.8** ("Every agent has a champion with respect to g"),
   the seed of the whole selected-cycle classification. Cited correctly once
   (THREE_NONSINGLETON...:455) but misattributed to Definition 2.6 at
   LENGTH_THREE_GLOBAL_LEX_TARGET.md:22, and absent from ALL THREE EXTERNAL-TRUSTED
   inventories while the length-three premise row asserts it with "Hidden assumption? No".
   Not derivable from any listed item. Fix: correct :22 and add Obs 2.8 to all three
   inventories.
9. **Spot-checks all correct:** Thm 5.1, Cor 3.18, Lemma 6.2, "Sections 2.3 and 3"
   pointer. Grep-confirmed: only the length-two chain cites 3.16/3.9.
10. **Process observation:** the length-three audit (08-09) has no EXTERNAL-TRUSTED
    inventory and marks identical BCFF rows "Hidden assumption? No" where the newer audits
    (08-16) mark them EXTERNAL-TRUSTED. Bring it into the newer format.

## Additivity-dependence sweep (BCFF-audit repair 2026-08-16)

Requested by finding 7's residual risk: since Lemma A.1 delivers a *cancelable*
witness, any proof step that genuinely needs **additivity** rests on a citation that
does not support it. Sweep of the alternating and adjacent chains as they stand on
`codex/efx-gg-cycle-referee-20260812`. Reading of "nondegenerate" throughout: distinct
subsets receive distinct values (the sense used at LENGTH_THREE_GLOBAL_LEX_TARGET.md:64-71
and in the `1000a_g+2^{e_g}` construction of ALTERNATING_CROSS_BOTTOM_LOCAL_OBSTRUCTION.md).
Under that reading, monotonicity gives `>=` and nondegeneracy upgrades it to `>` whenever
the two sets differ — which is what every "positivity" step below actually consumes.

**VERDICT: finding 7's claim is CONFIRMED for every order-closing step.** Exactly one
genuinely additive step exists in the two branches, and it sits in an intermediate
contraction that closes no priority order and is superseded by an additivity-free theorem.

### Sites where the inequality suffices

| Site | Displayed step | Why monotone + cancelable + nondegenerate is enough |
|---|---|---|
| ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md:81, eq (1) | `v_r(U)=b_r+v_r(B_q)>b_r`, `U=X_r+B_q` | Only `v_r(X_r ∪ B_q) > v_r(X_r)` is consumed. `B_q≠∅` makes the two sets distinct; monotonicity gives `>=`, nondegeneracy makes it strict. The additive equality is decorative |
| ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md:77, eq (1) | `v_q(W)=b_q+v_q(B_r)>b_q`, `W=X_q+B_r` | Identical shape, with `B_r≠∅` |
| ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md:104 and :368 | `v_q(W)>b_q`, `v_r(U)>b_r` (the reservoir-extraction premise "the pool contains a desired set") | Same; these are already written as inequalities, not equalities |
| Both reservoir lemmas + adjacent extraction, minimal-crossing bodies | `tau_j(A)<=v_j(A)<=v_j(P)`, `v_j(A)<=v_j(R-h)<t` | Pure set-inclusion monotonicity plus minimality of the chosen crossing set |
| ADJACENT :166 (6), :219 (10), :390 (19) | `v_i(D)>tau_i(D)>v_i(A)>=tau_i(A)` | "Total exceeds every one-good deletion" is monotonicity + nondegeneracy; the middle strict step is the branch inequality, not an additive computation |
| ADJACENT safe-repartition lemma (16) | conditions 1--3 and the EFX verification | Desiredness, common safety, one threshold inequality. Common safety is downward closed under monotonicity alone (`Z'⊆Z`, `g∈Z'` ⟹ `Z'-g ⊆ Z-g`) |
| ALTERNATING_ROOT_FLIP_LEMMA.md, (8)/(9) contradiction | `v_s(X_q)>v_s(D)` from `v_s(X_q-h)>v_s(D)` | Monotonicity. The lemma states this itself at :147 ("uses only monotonicity, base EFX, desired-set safety, and the two strict envy relations; additivity ... not needed") — confirmed |
| ALTERNATING_EASY_PRIORITY_ESCAPE_LEMMA.md:36-40 | singleton-only allocations are automatically EFX | Deletion leaves `∅` and `v_i(∅)<=v_i(Y_i)`; nonnegativity/monotonicity. Its header "four additive agents" is inherited framing, not a consumed hypothesis |
| ALTERNATING_TWO_SAFE_BUNDLE_REDUCTION.md, proof of (4)/(5) | every EFX comparison in the handoff allocation | Base-safety, the two strict envy relations, and threshold inequality (3); self-comparisons by nonnegativity |
| ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md:106-112 | EFX check of all three alternatives | Common safety against base, plus the single displayed `r`-threshold inequality |

### The one genuinely additive site

**ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md, Theorem 2 "Contested-top contraction",
equations (14)--(15) — GENUINELY ADDITIVE.** With `δ_p=b_p-v_p(D_p∖H)` and
`δ_r=b_r-v_r(B∖H)`, the step "if `v_p(H_p)>δ_p` then `D'_p=(D_p∖H)+H_p` is desired by `p`"
is exactly the additive identity `v_p((D_p∖H) ∪ H_p) = v_p(D_p∖H) + v_p(H_p)`. Under
monotone + cancelable + nondegenerate valuations the value of a union is not determined by
the values of its parts, so the quota arithmetic and the resulting obstruction (15) do not
survive the weakening. (The *common-safety* half of the same step — "would remain
common-safe by downward closure" — is fine on monotonicity alone.)

**Mitigation, and why this does not touch the result.** Theorem 2 is explicitly
intermediate: the document says it "was the intermediate contraction that isolated the five
hard types", and the next theorem "closes them without having to solve the quota wall
directly". It closes no priority order. Theorem 3 (safe repartition) supersedes it and is
additivity-free per the table above, so no order-closing step in the adjacent branch depends
on additivity. Recommended follow-up, not applied here: either attach an explicit
additivity hypothesis to Theorem 2, or state that it is offered only inside the additive
class where the corpus's headline theorem lives.

### Two further flags (no action taken)

- **TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md, "Packet nondegeneracy" part (a)**
  displays `v_w(D)=b_w+v_w(f)>b_w`. Only `v_w(X_w+f)>v_w(X_w)` is consumed, so
  "inequality suffices"; the additive equality introduced by the 2026-08-16 referee repair
  is decorative and could be replaced in one line. Left as written, since this sweep was
  scoped to report rather than edit.
- **ALTERNATING_CROSS_BOTTOM_LOCAL_OBSTRUCTION.md** says "Positive additivity makes every
  offer obtained by shrinking the incoming packet or enlarging the prescribed release still
  less valuable" — monotonicity alone gives the shrinking direction. Its profile `V*` and
  the `1000a_g+2^{e_g}` nondegeneracy argument *are* genuinely additive, but that is a
  counterexample witness: living in the additive class makes the refutation stronger, not
  weaker, so this is not a hidden premise.

### Sweep boundary

Displayed proof bodies of the alternating and adjacent chains on this branch only. BCFF's
own lemmas were not re-derived. The length-two chain — the only one invoking Theorem 3.16
and Definition 3.9 — was out of scope for this sweep.
