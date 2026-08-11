# Floater-consuming reset source trichotomy

**Date:** 2026-08-11

**Status:** cap-free elimination of an arbitrary floater-overlap reset;
termination of the three named source handoffs remains open

## Deletion dichotomy

Let `A` be a common-safe desired core for source `i`, relative to the base
EFX-with-charity state `(X,{f})`, and suppose

\[
 f\in A,
 \qquad v_i(A)>v_i(X_i).                            \tag{1}
\]

Put `A^-=A-f`.  Common safety is hereditary under deletion.  Therefore
exactly one of the following holds.

1. **Floater-free response.** If
   \[
   v_i(A^-)>v_i(X_i),                               \tag{2}
   \]
   then `A^-` is itself a common-safe desired response.  Replace `A` by an
   inclusion-minimal desired subset of `A^-`; the retained family now avoids
   `f`, so the universal retained-support reset applies.
2. **Floater-critical response.** If (2) fails, then
   \[
   v_i(A^- )\le v_i(X_i)<v_i(A^-)+v_i(f),
   \]
   and hence
   \[
   v_i(f)>v_i(X_i)-v_i(A^-)ge0.                    \tag{3}
   \]

If `A` is inclusion-minimal desired, branch 2 necessarily holds and every
good of `A`, including `f`, is critical in the corresponding form.

## Flower source routing

In the floater-critical branch, the source label gives an exhaustive
trichotomy.

1. **Root source `i=r`.** Equation (3) is a root/floater response.  It enters
   the root-response floater-substitution selector when its physical support
   is the anchored evolved target.  Otherwise it enters maximum-matching
   owner-union compression with the floater supplier explicitly included;
   support compatibility must be checked before using the anchored handoff.
2. **Later mutual source `i=q`.** The floater is essential to a common-safe
   `q` response.  Retain that response instead of restoring `D(U)` and
   compress its complete physical owner union.  Failure records the explicit
   `q`-margin/floater polarity (3), not a support reset.
3. **External source `i in {c,s}`.** The core is a genuine external
   charity-response edge.  It enters maximum-matching owner-union growth;
   generalized PI-freeness excludes any internally supplied response cycle
   produced there.

Thus a reset never has to restore `f` through two simultaneously retained
cores.  It either removes `f` from the new core and uses the monotone
top-support reset, or follows one named floater-critical response source.

## Claim boundary

This lemma removes an untyped floater-consuming reset and proves its exact
criticality inequality.  It does not terminate the root, `q`, or external
floater handoff, prove every resulting owner-union relation has an SDR,
close the fixed-support recurrence, close `GG`, or prove four-agent/general
additive EFX.
