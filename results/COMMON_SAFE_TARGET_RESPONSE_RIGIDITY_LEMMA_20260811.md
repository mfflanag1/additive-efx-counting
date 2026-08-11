# Common-safe target response-rigidity lemma

**Date:** 2026-08-11

**Status:** cap-free analytic rigidity theorem

## Statement

Let `X` be the base EFX allocation and let `A` be a nonempty bundle that is
common-safe at the base:

\[
 \tau_i(A)\le v_i(X_i) \qquad\text{for every owner }i. \tag{1}
\]

If an owner `i` has a strict desired subset `D subseteq A`,

\[
 v_i(D)>v_i(X_i),                                     \tag{2}
\]

then necessarily

\[
 D=A.                                                  \tag{3}
\]

Indeed, if `D` were proper, choose any `h in A\setminus D`.  Additivity and
positivity give

\[
 v_i(D)\le v_i(A-h)\le\tau_i(A)\le v_i(X_i),
\]

contradicting (2).

## Response consequence

Every base-response edge into a selected common-safe core is therefore a
whole-target edge.  A most-envious source may discard goods from an unsafe
target or from a residual bundle, but it cannot discard any good from an
already common-safe target while remaining strictly above its base bundle.

In particular, in the cross-star hole pivot the response
`C_d subseteq A_j` is exactly `C_d=A_j`.  The pivot simplifies to

\[
 Z'_i=D_i,
 \qquad Z'_d=A_j,
 \qquad W'=(W\setminus D_i)+A_i.                     \tag{4}
\]

Thus the core-side edge moves a complete common-safe core from the new hole
to the old hole.  All proper-subset support evolution occurs on the residual
side.  This separates whole-core hole motion from residual-core extraction
in the recurrence analysis.

## Verification and claim boundary

[`common_safe_target_response_rigidity_audit.json`](common_safe_target_response_rigidity_audit.json)
checks the proper-subset contradiction and the simplified pivot support
partition under Z3 5.0.0 and 4.15.3.

This lemma is valid for arbitrary positive additive bundles.  It simplifies
the recurrence support but does not terminate residual-side overlap,
source-inactive repair, captured-bottom handoffs, close `GG`, or prove
four-agent/general additive EFX.
