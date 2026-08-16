# BCFF composition audit for the adjacent-large length-four escape theorem

**Date:** 2026-08-16

**Status:** *Referee repair 2026-08-16* — written to close gap G4 of the
referee report `TWO_NONSINGLETON_COMPOSITION_REFEREE_REPORT_20260816.md`
(currently on `codex/efx-breakthrough-next-20260802`), which identified the
absence of an adjacent premise table as the reason the packet nondegeneracy
gap G1 went unnoticed.  Format mirrors
[`LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md`](LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md).

**Conclusion:** every hypothesis of Theorems 1--3 of
[`ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md`](ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md)
and of its two auxiliary lemmas is derived inside the adjacent-large branch
of the BCFF exactly-two-nonsingleton reduction, except for the BCFF
statements marked **EXTERNAL-TRUSTED**, which are not reproduced in this
repository and need a human check against
[arXiv:2102.10654](https://arxiv.org/abs/2102.10654).

## Structural premises shared by Theorems 1--3

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| One charity good `f` and partial EFX base | The contradiction state selected through BCFF Lemma 2.4 | **EXTERNAL-TRUSTED** (BCFF Lemma 2.4) |
| Global lexicographic maximality among *all* partial EFX allocations, rivals free to leave goods unallocated | Choice of maximum under the fixed BCFF domination order; the quantifier is fixed in [`ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md`](ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md) lines 46--51 | No transfer between orders |
| PI-free champion graph | BCFF Lemma 3.5 turns every PI cycle into a Pareto-improving EFX allocation | **EXTERNAL-TRUSTED** (BCFF Lemma 3.5, Definitions 3.1, 3.2 and 3.4; 3.3 is an Example) |
| Exactly two genuine edges, both entering the two nonsingleton bundles | Selected-cycle classification in [`TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md`](TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md) | No exact-graph and no chordlessness assumption |
| Adjacent normal form `p -f-> r -f-> q -> s -> p` with `X_p={x}`, `X_s={y}` | Relabel the consecutive-genuine-target length-four selected cycle (composition doc, classification table row 3) | Relabeling transports the fixed order; all 24 transported orders are covered |
| Selected desired sets `D_p=T_r+f` for `p`, `D_r=T_q+f` for `r`, `{y}` for `q`, `{x}` for `s`, all common-safe and strictly preferred by their sources | The two genuine edges and the two ordinary envy edges of the selected cycle | By definition (BCFF Definitions 2.6--2.7) |
| **Nonempty `T_r,B_r,T_q,B_q`** | "Packet nondegeneracy" section of the composition doc: empty top makes the desired set `{f}`, contradicting charity dominance; empty bottom makes the owner a self-`f`-champion via BCFF Observation 2.10 and positivity, and `f`-absorption is then an EFX lexicographic improvement in every order | **Was previously undischarged (gap G1).** Discharged as of 2026-08-16. Observation 2.10 is **EXTERNAL-TRUSTED** |
| Strictly positive, nondegenerate values | Nondegeneracy from the BCFF Lemma A.1 respecting witness; positivity from A.1's nondegeneracy **plus the paper's standing monotonicity**. The witness A.1 guarantees is *cancelable*, not necessarily additive; the additive respecting nondegenerate perturbation named in "Nonnegative values and ties" is folklore (Chaudhury et al.), not A.1. Only the final EFX allocation transfers back to the original profile | **EXTERNAL-TRUSTED** (BCFF Lemma A.1 + standing monotonicity) — see the A.1 note in the inventory below |

## Auxiliary lemma — reservoir extraction

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| `D` common-safe, `t=tau_j(D)` | `D` is one of the two selected desired sets | By definition |
| A pool `P` disjoint from `D` that *contains a desired set* | For `P=W=B_r+X_q`: `v_q(W)=b_q+v_q(B_r)>b_q`. For `P=U=X_r+B_q`: `v_r(U)=b_r+v_r(B_q)>b_r`. Then an inclusion-minimal subset on which some agent crosses her base is desired and common-safe | **Load-bearing use of nonempty bottoms and positivity:** with `B_r=∅` the pool `W` collapses to `X_q` and with `B_q=∅` the pool `U` collapses to `X_r`, and in each case the displayed strict inequality — the sole reason `P` contains a desired set — fails |
| No packet-size bound | The minimal-crossing argument is inclusion-based | No cap, no fixed move menu |

## Theorem 1 — every `r`-first order

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| `U=X_r+B_q` contains a desired set | Reservoir extraction premise above; needs `B_q` nonempty and positivity | See the load-bearing row |
| `D_r=T_q+f` common-safe and disjoint from `U` | Selected desired set of the genuine edge `r -f-> q`; disjointness is the `T_q/B_q` split | No |
| No desired subset of `U` is sourced by `p`, `q`, or `s` | The three compatible cycles (5) — `r -f-> q -(B_q)-> r`, `r -f-> q -> s -(B_q)-> r`, `r -f-> q -> s -> p -(B_q)-> r` — are PI in the sense of BCFF Definition 3.4, and the incoming set is released by the first edge | Covers extra champion edges rather than assuming they are absent |
| Base EFX and common safety for the EFX check of (3) and (6) | Base allocation is EFX; the constructed bundles are common-safe by extraction | Common safety is a *conclusion* of extraction, not a restriction on rivals |

## Escapes (8)--(12) — the `p`-first source wall

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| `W=B_r+X_q` contains a desired set | Reservoir extraction premise; needs `B_r` nonempty and positivity | **Load-bearing:** escapes (11) and (12) exist only because extraction returns a desired `A subseteq W` |
| `D_p=T_r+f` desired by `p` and common-safe | Selected desired set of the genuine edge `p -f-> r` | No |
| Source of `A` is `q` or `s` in the unresolved states | Sources `r` and `p` are excluded by inequality (9) and by escape (10) respectively | No exclusion of unrelated edges |

## Theorem 2 — contested-top contraction

Intermediate; it isolates the five hard priority/source types and is not used
to close any order.

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| An inclusion-minimal desired `B subseteq U`, sourced by `r` | Reservoir extraction plus the source wall (5); needs `B_q` nonempty and positivity | See above |
| `H=B∩D_p=B∩T_r` nonempty | Otherwise `(D_p,B,{x},{y})` is an EFX Pareto improvement | No |
| Downward closure of common safety under the quota split (14) | Additivity and base EFX | No |

## Safe-repartition lemma and Theorem 3 — every remaining `p`-first type

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| Disjoint `R,Q subseteq P=X_r+X_q+f` with `R` desired by `r`, `Q` common-safe at the base, `v_q(Q)>=tau_q(R)` | Supplied by the two extraction branches: branch 1 takes `R=D_r`, `Q` common-safe with `v_q(Q)>=tau_q(D_r)`; branch 2 takes `R=A` desired by `r`, `Q=D_r` | The lemma permits arbitrary repartition and discard inside `P`; neither bundle must be an old offer |
| `U=X_r+B_q` contains a desired set (both branches) | Reservoir extraction premise; needs `B_q` nonempty and positivity | **Load-bearing** |
| In branch 2, `A` is sourced by `r` | The three compatible cycles (5) exclude `p`, `q`, `s` | No |
| Strict inequality chain (19) `v_q(D_r)>tau_q(D_r)>v_q(A)>tau_q(A)` | Positivity plus branch inequality (18) | **EXTERNAL-TRUSTED** only through BCFF Lemma A.1 + standing monotonicity for positivity |
| `p,s` fixed at base and `r` strictly improved | The constructed allocation (16) keeps `Y_p={x}`, `Y_s={y}` | Lex improvement only when `r` precedes `q` ((16) may leave `q` below base); this suffices because all five remaining `p`-first types — `(p,r,s,q)`, `(p,r,q,s)`, `(p,s,r,q)` — have `r` before `q`; the three `p`-first orders with `q` before `r` are closed by escapes (11)/(12) instead |

## Order coverage

- 12 orders beginning with `q` or `s`: the easy singleton-first escapes.
- 6 orders beginning with `r`: Theorem 1.
- 6 orders beginning with `p`: escapes (8)--(12) close all but five
  priority/source types, and Theorem 3 closes those five.

Total 24, disjoint and exhaustive.

## EXTERNAL-TRUSTED inventory

Not reproduced in this repository.  Checked against the arXiv e-print by
[`BCFF_IMPORT_AUDIT_20260816.md`](BCFF_IMPORT_AUDIT_20260816.md), which found
the surface faithful; a human referee check is still wanted.

**Citation pin** (*BCFF-audit repair 2026-08-16*).  All numbering here follows
the **arXiv full build** of
[arXiv:2102.10654](https://arxiv.org/abs/2102.10654) (`\fulltrue`); v1
(2021-02-21) and v2 (2021-02-28) have identical Section 2 and Section 3
environment sequences, so the pin is "arXiv full version, v1 = v2".  The
AAAI-22 short build drops Definition 2.2, Example 2.5 and Definition 2.7 and
renumbers Section 2: under it "Lemma 2.4" is a Definition, "Definitions
2.6--2.7" are Observations, and **Observation 2.10 does not exist**.  Every
Section-2 citation below is coherent only under the full arXiv build.

| BCFF statement | Used for | Where |
|---|---|---|
| Lemma 2.4 | Existence/selection of the one-charity partial EFX contradiction state | Shared premises |
| Definitions 2.6--2.7 | Champion, desired set, common safety.  Caveat: the primitive "most envious of `S`" lives in unnumbered prose (its definition environment is commented out in both builds), so this is the best available citation, not complete provenance | Everywhere |
| **Observation 2.8** ("Every agent `i` has a champion with respect to `g`") | Every allocated bundle has an incoming `f`-champion — the seed of the selected-cycle classification | Shared premises, row "Exactly two genuine edges" (*added 2026-08-16*; it is not derivable from any other listed item) |
| Observation 2.10 | Empty bottom forces a self-`f`-champion | Packet nondegeneracy, part (a) |
| Definitions 3.1, 3.2 and 3.4 (3.3 is an Example) and Lemma 3.5 | PI cycles yield Pareto-improving EFX allocations | PI-freeness, and the source wall (5) |
| Lemma A.1 | A nondegenerate **cancelable** respecting witness `v'`, plus the one-directional transfer `EFX(v') => EFX(v)` — see the note below | Nondegeneracy; jointly with standing monotonicity, the positivity used in the extraction premises and in (19) |

**What Lemma A.1 does and does not supply** (*BCFF-audit repair 2026-08-16*,
correcting the one-line gloss this table previously carried; the import audit
records this as its single real drift).

1. **Not additivity.**  A.1 produces a *cancelable* respecting witness, not
   necessarily an additive one.  The additive respecting nondegenerate
   perturbation the "Nonnegative values and ties" section of the target
   document runs the argument in does exist, but it is folklore (Chaudhury et
   al.), **not** BCFF Lemma A.1.
2. **Not positivity.**  A.1 says nothing about positivity.  The strict
   positivity behind `v_r(U)>b_r`, `v_q(W)>b_q` and the chain (19) is A.1's
   nondegeneracy together with the paper's standing monotonicity assumption;
   cite it as "A.1 + standing monotonicity", never as A.1 alone.
3. **Not a round trip.**  The transfer is one-directional and carries only
   the final EFX allocation back to the original profile.  It does **not**
   carry lexicographic maximality, the one-charity normal form, or the
   champion graph — all of which are defined *inside* the perturbed profile,
   which is exactly why the argument is legitimate.  The correct in-corpus
   statement of this is `ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md`, lines
   276--281 ("Their Appendix A perturbation is sufficient for existence
   theorems but does not automatically preserve a designated tied maximal
   state or its selected champion graph"); that file is on
   `codex/efx-breakthrough-next-20260802`, see gap G5.

None of this reopens the conditional status of the composition: everything is
defined inside the perturbed profile and only the final EFX allocation
transfers back, which is precisely what A.1 licenses.  The residual question
— whether any step genuinely needs additivity rather than monotonicity plus
cancelability plus nondegeneracy — is swept in the
"Additivity-dependence sweep" section of
[`BCFF_IMPORT_AUDIT_20260816.md`](BCFF_IMPORT_AUDIT_20260816.md).

**Not used by the adjacent branch:** BCFF Theorem 3.16 and Definition 3.9.
Only the length-two case theorem invokes them (gap G4 of the referee report);
this branch never appeals to good-`f`-cycle edge discovery.

## Evidence status

Theorems 1--3 are analytic and independent of packet sizes.  The exact
computations recorded in the "Corrected exact diagnostics" section of the
target document — the 24 atomic QF_LRA-UNSAT orders, the one-packet splits,
and the binary safe-repartition gate — are fixed-cell diagnostics that
corroborate the theorems; they are not premises of any proof, and a
`(3,2,2,2)` pure-gate replay was deliberately retired without a decision.
The composition branch currently carries only 2 of the 13
`adjacent_large_*.json` artifacts (gap G5, version fragmentation).

## Exact claim boundary

This audit establishes that the adjacent-large theorems plug into the BCFF
**adjacent length-four branch** without additional premises, given the
EXTERNAL-TRUSTED rows.  It does not use or prove the length-two,
length-three, or alternating branches, and it does not address BCFF states
with three or four nonsingleton bundles.
