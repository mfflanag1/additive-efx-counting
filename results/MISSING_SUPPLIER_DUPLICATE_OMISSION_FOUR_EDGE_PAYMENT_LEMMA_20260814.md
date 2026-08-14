# Missing-supplier duplicate-omission payment and support frontier

**Date:** 2026-08-14

**Status:** cap-free all-owner-payment closure of 24 of the 48 corrected
rank-three fan maps; the original-supplier edge bound and observer closure
remain

## Input

Use the `3+1` fan of
`MISSING_SOURCE_TWO_CHOICE_FAN_DOUBLE_CAPTURE_LEMMA_20260814.md`.  The four
pairwise-disjoint common-safe desired cores `D_t subseteq Z_t` have exactly
three sources.  Let `m` be the missing source and `a` the duplicated source.

Assume the missing owner supplies one of the two cores desired by `a`:

\[
                         f(m)=a.                 \tag{1}
\]

Let `u!=m` be the other target with `f(u)=a`.

## Duplicate omission

Omit `D_m`: owner `m` retains its entire current bundle.  Select `D_u` for
source `a`, and select the unique fan core for each of the other two
represented sources.  Transfer those three selected cores to their named
sources, retain every unselected target residual, and give the positive
charity singleton `p` to `m`.

The three selected cores have distinct current targets and distinct sources.
Each response is nonself, so they create exactly three **current-holder**
target-to-source moves.  Charity creates one additional move.

This is not automatically the objective's original-supplier edge bound.  At
a later probe, one current target may contain cells from several suppliers
in the frozen allocation `Y`.  Let `sigma(g)` be good `g`'s supplier in `Y`.
The exact physical pair set is

\[
 \Pi=\{(\sigma(g),f(t)):g\in D_t, t\text{ selected},
                         \sigma(g)\ne f(t)\}.     \tag{2}
\]

Together with the charity pair, the candidate meets the theorem's edge bound
if and only if `|Pi union {(charity,m)}|<=4`.  In particular it is a genuine
four-edge endpoint whenever each selected core is supplier-homogeneous in
the three displayed holder-source pairs.  No universal supplier-
homogeneity inference is asserted here.

## All-owner payment

Let represented source `i` receive its selected desired core `C_i` and let
`R_i` be the part of its old current bundle left after any selected outgoing
core is removed.  Since `C_i` is desired above `i`'s complete old bundle,

\[
 v_i(R_i+C_i)\ge v_i(C_i)>v_i(Z_i).              \tag{3}
\]

Thus all three represented sources strictly improve.  The missing source
loses nothing because `D_m` was omitted and receives `p`, so

\[
                         v_m(Z_m+p)>v_m(Z_m).     \tag{4}
\]

Every owner is strictly current-paid.

## Consequence

If the resulting complete allocation satisfies the physical condition after
(2) and is EFX, it is the desired four-edge endpoint (and, when the current
state pays the GG base, a lexicographic contradiction).  If it is not EFX,
globally minimum extraction gives a common-safe desired response at an
all-owner-paid allocation; the exact original-supplier decoration must be
retained.
Unsafe enlarged-target continuation must then be converted to a new
decorated record, release-compatible PI, strict support/progress, or an exact
paid-record repeat.

The 24 complementary `3+1` maps have `f(m)!=a`: the missing target's core is
the unique core paying another represented source, so it cannot simply be
omitted.  Those are precisely the foreign-duplicate-supplier hole/capture
class.

## Claim boundary

Proved: complete conservation, three current-holder moves plus charity, and
strict payment of all owners for exactly the missing-supplies-duplicate
class, together with the exact physical support criterion (2).  Not proved:
universal satisfaction of that criterion, observer safety, closure of an
exact paid decorated repeat, the 24 foreign-supplier maps, the fixed-U
theorem, or additive EFX.
