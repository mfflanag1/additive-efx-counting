# Rank-three PI-free crossed-provenance import lemma

**Date:** 2026-08-13

**Status:** cap-free support consequence for base-common-safe desired cores;
unconditional at `d->q`, conditional at the current-only `d->r` wall

**Status correction (2026-08-13):** the original statement treated both
`d` responses symmetrically. The recurrent `d->q` core is ordinary
base-desired, but the strong-wall edge `d->r` may be only current-desired.
Because `d` is below base, current desire does not imply a base champion
edge, so items 3--4 below require an additional base-response hypothesis.

## Response cores

Let the rank-three selected matching have represented sources
`R={r,q,s}` and pairwise-distinct physical targets. Write `A_i` for a
minimal common-safe desired core assigned to selected source `i`. The cores
`A_r,A_q,A_s` are pairwise disjoint.

The unmatched owner `d` has a minimal base-common-safe desired core `D_q` in
the physical `q` target. If the strong-wall response into physical target
`r` is also base-common-safe desired, denote such a core by `D_r`. The selected core
sharing the `q` target is always `A_r`. The selected core sharing the `r`
target is

\[
 A_q\quad\text{in form R2},
 \qquad A_s\quad\text{in form R3}.               \tag{1}
\]

## Four forced imports

Assume the base champion graph has no generalized PI cycle. Then items 1--2
hold unconditionally; items 3--4 require the displayed base-response
hypothesis for `D_r`:

1. `A_r union A_q union A_s` contains a good base-owned by `d`;
2. `D_q union A_q union A_s` contains a good base-owned by `r`;
3. in R2, `D_r union A_r union A_s` contains a good base-owned by `q`;
4. in R3, `D_r union A_r union A_q` contains a good base-owned by `s`.

For (1), otherwise the three selected disjoint cores are closed over source
set `{r,q,s}` plus charity, so the closed-core characterization gives a PI
cycle.

For (2), remove the selected core `A_r` and insert `D_q`. The three retained
cores are pairwise disjoint because `D_q` lies in the physical target formerly
shared only with `A_r`, while `A_q,A_s` lie in the other selected targets. If
their union contained no base-`r` good, they would be closed over source set
`{d,q,s}` plus charity and again form PI. The proofs of (3)--(4) are identical
after removing the selected source named in (1).

No good, packet-size, or valuation cap is used. The argument needs only
physical target disjointness, minimal common-safe desire, and generalized
PI-freeness.

## Consequence

The rank-three survivor unconditionally contains crossed base-support
dependencies at the selected matching and at target `q`:

- the original selected triple imports sacrificed-owner support; and
- replacing the target-`q` selected core by `D_q` forces support of the
  displaced represented source back into the remaining triple.

The corresponding target-`r` statement holds when `d->r` is base-desired.
If it is current-only, the remaining obligation is a mixed-floor support
walk, not a base generalized-PI consequence.

Thus base full-margin overlap capture cannot remain provenance-local. It
creates a support walk crossing `d` and target `q`, conditionally extending
through target `r`. Returning all
support along the least closed walk pays its owners by the base-support
closure lemma. The remaining issue is to compress that paid return to at
most three owner edges plus the charity edge while preserving observer EFX.

## Verification and boundary

`audit_rank_three_pi_free_crossed_provenance_import.py` independently checks
the combinatorial closure implication for both forms and both replacement
families. It does not verify that the target-`r` response satisfies the
base-response hypothesis; that is now explicit in the claim boundary.

This lemma forces the crossed support walk. It does not bound the complete
base-support reassembly by four edges, pay an arbitrary partial return, or
prove the final complete EFX allocation.
