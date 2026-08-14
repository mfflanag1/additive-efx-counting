# Form-2 all-target-change exact-repeat rank no-go

**Date:** 2026-08-14

**Status:** exact positive-rational refutation of automatic rank growth from
an all-target-changing four-edge repeat; full saturated GG implication open

## The tempting inference

The six canonical form-2 branches change all four owner bundles and charity.
At saturation, a paid non-EFX branch therefore yields either a new decorated
record or an exact earlier cross-state record.  It is tempting to infer that
the latter repeat supplies the fourth response edge needed by represented-
component charity extraction.

That inference is false, even in the canonical paid owner-only response
geometry.

## Exact witness

Start from the physical packets

\[
\begin{array}{c|ccccc}
 &r&q&s&d&c\\ \hline
Y&\{r_0,S,D_r\}&\{q_0,R,D_q\}&\{s_0,Q\}&\{d_0\}&\{p\}.
\end{array}
\]

Use the branch selecting `D_r` and omitting source `r`.  Move

\[
 p:c\to r,\qquad D_r:r\to d,\qquad
 S:r\to s,\qquad Q:s\to q.
\]

The final complete allocation is

\[
 Z=(\{r_0,p\},\{q_0,R,D_q,Q\},\{s_0,S\},\{d_0,D_r\}).
\]

These four edges form a spanning tree, and every owner target and charity
changes.  Give each owner value `3/2` for her own final bundle, against a
declared unit base-payment floor.  Put value
`2` on the following singleton desired cores:

\[
 r:R,\qquad q:S,\qquad s:r_0,\qquad d:D_q,\qquad d:p,
\]

and value `1/100` on every other good outside that owner's final bundle.
All values are positive rationals.  The exact nonself desired-target relation
is

\[
 r\to q,\quad q\to s,\quad s\to r,\quad d\to q,
 \quad d\to r.                                   \tag{1}
\]

Each displayed singleton is common-safe because deleting its only good gives
the empty bundle.  Allocation `Z` is nevertheless not EFX: for example,
source `r` still values the `q` target above `3/2` after deletion of `q_0`.

Relation (1) is connected on all four owners and has the canonical
three-cycle plus both root-facing unmatched-source responses.  But all its
edges use only the three targets `r,q,s`; hence its maximum matching rank is
exactly three.  Declaring the complete physical and response record of `Z`
to have occurred earlier makes it an exact cross-state repeat without
changing that rank.

## Consequence

All-target change, four-edge current-support connectivity, payment against
the declared unit floors,
a common-safe failed response, complete state reconstruction, and exact
cross-state repetition do **not** imply rank-four response representation.
Therefore the exact repeat cannot be closed merely by invoking matching
augmentation or the rank-equals-component-size represented-component
theorem.

The remaining proof must use an additional saturated GG inequality:
base-margin/direct-safety, release-compatible PI, strict record progress, or
one of the supplier/double-margin exits.  Equivalently, a future exact
decision encoding must include those premises explicitly; a repeat-only
encoding is underconstrained.

## Verification and claim boundary

`audit_form2_all_target_change_exact_repeat_rank_no_go.py` independently
checks packet conservation, the four-edge spanning tree, change of all five
targets, exact positive-rational response relation, common safety, non-EFX,
and maximum matching rank three.

This is not a saturated fixed-`U` countermodel.  It does not encode base EFX,
global lexicographic maximality, generalized-PI exclusion, the complete
base-margin separator, or continuation exclusions 7--12.  It refutes only
the proposed admission inference from the already proved repeat data.
