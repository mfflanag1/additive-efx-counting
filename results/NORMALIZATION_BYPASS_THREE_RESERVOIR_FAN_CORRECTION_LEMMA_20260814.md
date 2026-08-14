# Normalization-bypass three-reservoir fan correction

**Date:** 2026-08-14

**Status:** cap-free correction of the unmerged all-unsafe fan claim; the
rank-three missing-source defect remains open

## Four disjoint response cores

Let the four current owner targets be indexed by `N`.  Suppose target `t`
contains a nonempty common-safe core `D_t`, the four cores are pairwise
disjoint, and `D_t` is strictly desired by a named nonself source `f(t)`:

\[
 D_t\cap D_u=\varnothing\quad(t\ne u),
 \qquad f(t)\ne t.                               \tag{1}
\]

This is the output asserted by the all-unsafe branch of the reservoir-
reversal construction: the original response plus one reversed response
from each of the other three physical target reservoirs.

## Surjective source case

If `f` is surjective, the four sources are distinct.  Relabel the four
packets by source, choose an inclusion-minimal desired subcore for each
source, and apply the closed disjoint-core characterization with `V=N`.
Every base owner of every selected good lies in `N` (or the good is base
charity), so base-owner closure is automatic.  The four pairwise-disjoint
cores therefore form a generalized PI family.

No incomplete “cores-only EFX allocation” is needed for this conclusion;
all unselected residual goods remain irrelevant to the PI certificate.

## Nonsurjective source case

If `f` is not surjective, current-supplier cyclicity does **not** by itself
give generalized PI.  The exact alternatives are:

1. `|im(f)|=3`: one owner is missing as a response source and exactly one
   other source occurs twice;
2. `|im(f)|=2`: two sources are missing, with multiplicities `2+2` or
   `3+1`.

Image size one is impossible under `f(t)!=t`, because the unique source's
own target would create a self edge.

The unmerged theorem at commit
`34709c9ce22dbde23a5fa381a2ccea7898dfe1ca` claimed that following the
current supplier-source edges always produces a supplier-closed PI cycle.
That inference is invalid: generalized PI closure is with respect to the
**base owners** of the selected goods and the packets released from their
base bundles, not merely their current holders.

## Exact counterexample to current-cycle closure

Take owners `0,1,2,3`, four singleton cores in their four respective current
targets, and source map

\[
 f(0)=1,\qquad f(1)=0,\qquad f(2)=0,\qquad f(3)=0. \tag{2}
\]

The current supplier-source graph contains the two-cycle `0 <-> 1`.  Give
the four core goods base owners `2,3,2,3`, respectively.  Each singleton can
be made common-safe and strictly desired by its displayed source: give that
source value two for the singleton and current floor one; singleton EFX
thresholds are zero.

There is nevertheless no closed disjoint desired-core family:

- source `1` has only a core base-owned by `2`, so any closed owner set
  containing `1` must also contain `2`, which has no desired core;
- every core for source `0` is base-owned by `2` or `3`, neither of which
  has a desired core;
- a full-owner family is impossible because sources `2,3` are missing.

Thus (2) is an exact positive-additive counterexample to the implication
“current supplier cycle implies generalized PI.”  It is not a countermodel
to the full fixed-U premises.

## Correct fixed-U boundary

In the rank-three saturated program the all-unsafe fan therefore gives:

- generalized PI if it recruits all four response sources; or
- an exact deficient source set.  In the rank-three case this is normally
  the `3+1` pattern: one missing owner and one duplicated represented source.

To close the universal theorem, the missing owner's mandatory frozen
response must be added.  If its minimal core is disjoint from the fan, all
four sources give generalized PI by the surjective case.  Otherwise that
core's complete strict response margin is captured by the fan union.  The
remaining theorem is reversal of this capture within four physical edges or
conversion to the represented-component/base-margin terminal.

## Claim boundary

Proved: the surjective-source PI implication, exhaustive source-image
classification, and an exact counterexample to current-supplier-cycle
closure.  Not proved: reversal of the missing-source capture, closure of the
safe-payment reservoir branch, the fixed-U theorem, or additive EFX.
