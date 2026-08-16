# BCFF composition audit for the alternating length-four escape theorem

**Date:** 2026-08-16

**Status:** *Referee repair 2026-08-16* — written to close gap G4 of the
referee report `TWO_NONSINGLETON_COMPOSITION_REFEREE_REPORT_20260816.md`
(currently on `codex/efx-breakthrough-next-20260802`), which identified the
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
| PI-free champion graph | BCFF Lemma 3.5 turns every PI cycle into a Pareto-improving EFX allocation | **EXTERNAL-TRUSTED** (BCFF Lemma 3.5, Definitions 3.1--3.4) |
| Exactly two genuine edges, both entering the two nonsingleton bundles | Selected-cycle classification in [`TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md`](TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md) | No exact-graph and no chordlessness assumption |
| Alternating normal form `p -f-> r -> s -f-> q -> p` with `X_p={x}`, `X_s={y}` | Relabel the opposite-genuine-target length-four selected cycle (composition doc, classification table row 4) | Relabeling transports the fixed order; all 24 transported orders are covered |
| `X_r,X_q` nonsingleton, with decompositions `X_r=T_r+B_r`, `X_q=T_q+B_q` | The two-nonsingleton hypothesis, plus the selected desired sets `T_r+f` of `p` and `T_q+f` of `s` | No decomposition choice beyond the selected edges |
| **Nonempty `T_r,B_r,T_q,B_q`** | "Packet nondegeneracy" section of the composition doc: empty top makes the desired set `{f}`, contradicting charity dominance; empty bottom makes the owner a self-`f`-champion via BCFF Observation 2.10 and positivity, and `f`-absorption is then an EFX lexicographic improvement in every order | **Was previously undischarged (gap G1).** Discharged as of 2026-08-16. Observation 2.10 is **EXTERNAL-TRUSTED** |
| Common safety of `T_r+f` and `T_q+f` | They are the desired sets of the two selected champions | By definition (BCFF Definitions 2.6--2.7) |
| Strictly positive, nondegenerate values | Standard respecting perturbation in BCFF Lemma A.1, removed again at the end | **EXTERNAL-TRUSTED** (BCFF Lemma A.1) |
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
| Nonnegative valuations (for "no agent strongly envies the empty set") | BCFF Lemma A.1 perturbation gives positivity, which is stronger | **EXTERNAL-TRUSTED** (BCFF Lemma A.1) |

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
| Monotone valuations | BCFF Lemma A.1 perturbation | **EXTERNAL-TRUSTED** (BCFF Lemma A.1) |

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
| Values strictly positive | BCFF Lemma A.1 perturbation | **EXTERNAL-TRUSTED** (BCFF Lemma A.1) |
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
| Values strictly positive | BCFF Lemma A.1 perturbation | **EXTERNAL-TRUSTED** (BCFF Lemma A.1) |
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

Not reproduced in this repository; each needs a human check against
[arXiv:2102.10654](https://arxiv.org/abs/2102.10654).

| BCFF statement | Used for | Where |
|---|---|---|
| Lemma 2.4 | Existence/selection of the one-charity partial EFX contradiction state | Top-level premise |
| Definitions 2.6--2.7 | Champion, desired set, common safety | Every component |
| Definitions 3.1--3.4 and Lemma 3.5 | PI cycles yield Pareto-improving EFX allocations | PI-freeness, and both family-present branches |
| Observation 2.10 | Empty bottom forces a self-`f`-champion | Packet nondegeneracy, part (a) |
| Lemma A.1 | Respecting positive nondegenerate perturbation; return to the original profile | Positivity everywhere |

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
