# BCFF composition audit for the alternating length-four escape theorem

**Date:** 2026-08-16

**Status:** *Referee repair 2026-08-16* — written to close gap G4 of the
referee report
[`TWO_NONSINGLETON_COMPOSITION_REFEREE_REPORT_20260816.md`](TWO_NONSINGLETON_COMPOSITION_REFEREE_REPORT_20260816.md), which identified the
absence of an alternating premise table as the reason the packet
nondegeneracy gap G1 went unnoticed.  Format mirrors
[`LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md`](LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md).

**Conclusion:** every hypothesis of
[`ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md`](ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md)
and of its four component lemmas is derived inside the alternating branch of
the BCFF exactly-two-nonsingleton reduction, except for the BCFF statements
marked **EXTERNAL-TRUSTED**, which are not reproduced in this repository and
need a human check against
[arXiv:2102.10654](https://arxiv.org/abs/2102.10654).

## Top-level theorem

Premises of the cap-free alternating global-lex theorem.

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| One charity good `f` and partial EFX base | The contradiction state selected through BCFF Lemma 2.4 | **EXTERNAL-TRUSTED** (BCFF Lemma 2.4) |
| Global lexicographic maximality among *all* partial EFX allocations, rivals free to leave goods unallocated | Choice of maximum under the fixed BCFF domination order; the quantifier is fixed in [`ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md`](ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md) lines 46--51 | No transfer between orders |
| PI-free champion graph | BCFF Lemma 3.5 turns every PI cycle into a Pareto-improving EFX allocation | **EXTERNAL-TRUSTED** (BCFF Lemma 3.5, Definitions 3.1, 3.2 and 3.4; 3.3 is an Example) |
| Exactly two genuine edges, both entering the two nonsingleton bundles | Selected-cycle classification in [`TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md`](TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md) | No exact-graph and no chordlessness assumption |
| Alternating normal form `p -f-> r -> s -f-> q -> p` with `X_p={x}`, `X_s={y}` | Relabel the opposite-genuine-target length-four selected cycle (composition doc, classification table row 4) | Relabeling transports the fixed order; all 24 transported orders are covered |
| `X_r,X_q` nonsingleton, with decompositions `X_r=T_r+B_r`, `X_q=T_q+B_q` | The two-nonsingleton hypothesis, plus the selected desired sets `T_r+f` of `p` and `T_q+f` of `s` | No decomposition choice beyond the selected edges |
| **Nonempty `T_r,B_r,T_q,B_q`** | "Packet nondegeneracy" section of the composition doc: empty top makes the desired set `{f}`, contradicting charity dominance; empty bottom makes the owner a self-`f`-champion via BCFF Observation 2.10 and positivity, and `f`-absorption is then an EFX lexicographic improvement in every order | **Was previously undischarged (gap G1).** Discharged as of 2026-08-16. Observation 2.10 is **EXTERNAL-TRUSTED** |
| Common safety of `T_r+f` and `T_q+f` | They are the desired sets of the two selected champions | By definition (BCFF Definitions 2.6--2.7) |
| Strictly positive, nondegenerate values | Nondegeneracy from the BCFF Lemma A.1 respecting witness; positivity from A.1's nondegeneracy **plus the paper's standing monotonicity**. The witness A.1 guarantees is *cancelable*, not necessarily additive; the additive respecting nondegenerate perturbation actually used is folklore (Chaudhury et al.), not A.1. Only the final EFX allocation transfers back to the original profile | **EXTERNAL-TRUSTED** (BCFF Lemma A.1 + standing monotonicity) — see the A.1 note in the inventory below |
| Presence *or* absence of the four compatible **generalized** champion families | Exhaustive dichotomy on the broad notion; present gives a PI cycle, absent feeds items 3--4 below | Sound only on the broad notion — see the warning row |
| *Warning row:* absence of the four **standard** cross-bottom seeds | Does **not** discharge the absence branch. Narrow presence implies broad presence, not conversely; the repaired hand profile of [`ALTERNATING_CROSS_BOTTOM_LOCAL_OBSTRUCTION.md`](ALTERNATING_CROSS_BOTTOM_LOCAL_OBSTRUCTION.md) has all four standard seeds absent and the generalized edge `r --B_r\|∅--> q` present | Trap for external readers; fixed in the theorem statement 2026-08-16 |

## Component lemma 1 — easy-priority escape

[`ALTERNATING_EASY_PRIORITY_ESCAPE_LEMMA.md`](ALTERNATING_EASY_PRIORITY_ESCAPE_LEMMA.md),
16 of 24 orders.

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| Alternating topology with `X_p={x}`, `X_s={y}` | Classification, as above | No |
| Ordinary envy edges `r -> s`, `q -> p`, i.e. `v_r(y)>v_r(X_r)` and `v_q(x)>v_q(X_q)` | The two non-genuine edges of the selected cycle are ordinary envy edges (composition doc: an edge into a singleton that retains `f` is not common-safe, so it is replaced by its parallel envy edge) | No |
| Rival allocations may leave goods unallocated | Uniform improvement order; the escape allocations are singleton-only and discard the rest | No — quantifier fixed at the top level |
| Nonnegative valuations (for "no agent strongly envies the empty set") | Standing monotonicity gives nonnegativity directly; the A.1 witness supplies nondegeneracy | **EXTERNAL-TRUSTED** (BCFF Lemma A.1 + standing monotonicity) |

No packet hypothesis is used by this lemma.

## Component lemma 2 — root-flip

[`ALTERNATING_ROOT_FLIP_LEMMA.md`](ALTERNATING_ROOT_FLIP_LEMMA.md), orders
`(p,q,r,s)` and `(s,r,q,p)`.

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| `X_p={x}`, `X_s={y}`, one unallocated `f` | Classification and one-charity normal form | No |
| Envy edges (2): `v_r(y)>v_r(X_r)`, `v_q(x)>v_q(X_q)` | As in lemma 1 | No |
| A selected desired set `D subseteq X_r+f` for `p` with `v_p(D)>v_p(x)` | The genuine edge `p -f-> r`; `D=T_r+f` | By definition of champion |
| Desired-set safety `v_i(D-g)<=v_i(X_i)` for all `i,g` | Common safety of a selected desired set | By definition |
| Base EFX inequalities on `X_q` | The base allocation is EFX | No |
| Monotone valuations | The paper's standing monotonicity assumption; the A.1 witness is respecting and nondegenerate but is not the source of monotonicity | **EXTERNAL-TRUSTED** (BCFF standing monotonicity; A.1 for nondegeneracy) |

This lemma needs neither packet nonemptiness nor family absence; it is the
only component that survives an empty bottom.

## Component lemma 3 — reservoir exchange

[`ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md),
orders `(p,s,r,q)` and `(s,p,q,r)`.

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| `D=T_q+f` is desired by `s` | The genuine edge `s -f-> q` and its selected desired set | No |
| `D` is common-safe | Selected desired set | By definition |
| No subset of `X_r+H`, any `H subseteq B_q`, is desired by `p` or `q` | Exactly the absence of the two compatible **generalized** champion families into `X_r`; the absent branch of the top-level dichotomy | Broad notion required — narrow absence is not enough |
| Values strictly positive | A.1's nondegeneracy plus standing monotonicity; A.1 alone says nothing about positivity | **EXTERNAL-TRUSTED** (BCFF Lemma A.1 + standing monotonicity) |
| **`B_q` nonempty** | "Packet nondegeneracy" section of the composition doc | **Load-bearing:** the proof opens with `v_r(U)=b_r+v_r(B_q)>b_r` (its equation (1)); with `B_q=∅` the pool `U=X_r` contains no desired set and the minimal-crossing step fails |
| Minimal-crossing fact | Proved inside the lemma from finiteness and common safety | No |

## Component lemma 4 — dual-reservoir trichotomy

[`ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md`](ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md),
orders `(p,s,q,r)`, `(p,q,s,r)` and their half-turns `(s,p,r,q)`,
`(s,r,p,q)`.

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| `D_p=T_r+f` is desired by `p` | The genuine edge `p -f-> r` and its selected desired set | No |
| `D_p` common-safe | Selected desired set | By definition |
| `q` strictly envies `X_p={x}` | The ordinary envy edge `q -> p` of the selected cycle | No |
| No subset of `W=X_q+B_r` is desired by `r` or `s` | Absence of the two compatible **generalized** families into `X_q` | Broad notion required |
| Values strictly positive | A.1's nondegeneracy plus standing monotonicity; A.1 alone says nothing about positivity | **EXTERNAL-TRUSTED** (BCFF Lemma A.1 + standing monotonicity) |
| **`B_r` nonempty** | "Packet nondegeneracy" section of the composition doc | **Load-bearing:** the proof opens with `v_q(W)=b_q+v_q(B_r)>b_q` (its equation (1)); with `B_r=∅` the pool `W=X_q` contains no desired set |

## Order coverage

The four components partition the 24 priority orders as `16+2+2+4`, disjoint
and exhaustive:

- easy-priority: the 16 orders beginning with `r` or `q`, with `p,r`, or with
  `s,q`;
- root-flip: `(p,q,r,s)`, `(s,r,q,p)`;
- reservoir exchange: `(p,s,r,q)`, `(s,p,q,r)`;
- dual-reservoir trichotomy: `(p,s,q,r)`, `(p,q,s,r)`, `(s,p,r,q)`,
  `(s,r,p,q)` — all four, because alternative 2 fixes `p,s` at base and
  improves `q` while `r` is last in both `p`-rooted orders.

The stale sentence in
[`ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md)
that credited the trichotomy with only two of those four orders was corrected
on 2026-08-16 (gap G3); a dated correction note is kept in place there.

The partition is regression-tested by
[`test_alternating_capfree_order_coverage.py`](../tracks/parkability/test_alternating_capfree_order_coverage.py).
That test is hard-coded set arithmetic over order labels: it asserts the
sizes `[16,2,2,4]` and the disjointness of the four sets.  It therefore
cannot detect a miscredited lemma, and it is evidence about bookkeeping only,
not about any component proof.

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
| Lemma 2.4 | Existence/selection of the one-charity partial EFX contradiction state | Top-level premise |
| Definitions 2.6--2.7 | Champion, desired set, common safety.  Caveat: the primitive "most envious of `S`" lives in unnumbered prose (its definition environment is commented out in both builds), so this is the best available citation, not complete provenance | Every component |
| **Observation 2.8** ("Every agent `i` has a champion with respect to `g`") | Every allocated bundle has an incoming `f`-champion — the seed of the selected-cycle classification | Top-level premise, row "Exactly two genuine edges" (*added 2026-08-16*; it is not derivable from any other listed item) |
| Observation 2.10 | Empty bottom forces a self-`f`-champion | Packet nondegeneracy, part (a) |
| Definitions 3.1, 3.2 and 3.4 (3.3 is an Example) and Lemma 3.5 | PI cycles yield Pareto-improving EFX allocations | PI-freeness, and both family-present branches |
| Lemma A.1 | A nondegenerate **cancelable** respecting witness `v'`, plus the one-directional transfer `EFX(v') => EFX(v)` — see the note below | Nondegeneracy; jointly with standing monotonicity, positivity |

**What Lemma A.1 does and does not supply** (*BCFF-audit repair 2026-08-16*,
correcting the one-line gloss this table previously carried; the import audit
records this as its single real drift).

1. **Not additivity.**  A.1 produces a *cancelable* respecting witness, not
   necessarily an additive one.  The additive respecting nondegenerate
   perturbation this corpus actually runs the argument in does exist, but it
   is folklore (Chaudhury et al.), **not** BCFF Lemma A.1.  Every place that
   previously credited A.1 with an "additive perturbation" was
   over-describing it.
2. **Not positivity.**  A.1 says nothing about positivity.  The strict
   positivity used by the reservoir premises is A.1's nondegeneracy together
   with the paper's standing monotonicity assumption; it should be cited as
   "A.1 + standing monotonicity", never as A.1 alone.
3. **Not a round trip.**  The transfer is one-directional and carries only
   the final EFX allocation back to the original profile.  It does **not**
   carry lexicographic maximality, the one-charity normal form, or the
   champion graph — all of which are defined *inside* the perturbed profile,
   which is exactly why the argument is legitimate.  The correct in-corpus
   statement of this is
   [`ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md`](ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md),
   lines 276--281 ("Their Appendix A perturbation is sufficient for existence
   theorems but does not automatically preserve a designated tied maximal
   state or its selected champion graph").  *G5 consolidation 2026-08-16*: that file is
   now co-resident on this branch and the citation is a live link.

None of this reopens the conditional status of the composition: everything is
defined inside the perturbed profile and only the final EFX allocation
transfers back, which is precisely what A.1 licenses.  The residual question
— whether any step genuinely needs additivity rather than monotonicity plus
cancelability plus nondegeneracy — is swept in the
"Additivity-dependence sweep" section of
[`BCFF_IMPORT_AUDIT_20260816.md`](BCFF_IMPORT_AUDIT_20260816.md).

**Not used by the alternating branch:** BCFF Theorem 3.16 and Definition 3.9.
Only the length-two case theorem invokes them (gap G4 of the referee report);
this branch never appeals to good-`f`-cycle edge discovery.

## Exact claim boundary

This audit establishes that the cap-free alternating theorem and its four
component lemmas plug into the BCFF **alternating length-four branch**
without additional premises, given the EXTERNAL-TRUSTED rows.  It does not
use or prove the length-two, length-three, or adjacent-large branches, and it
does not address BCFF states with three or four nonsingleton bundles.  The
component lemma proofs themselves were verified by a subagent, not by the
2026-08-16 referee.
