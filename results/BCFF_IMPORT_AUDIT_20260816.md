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
