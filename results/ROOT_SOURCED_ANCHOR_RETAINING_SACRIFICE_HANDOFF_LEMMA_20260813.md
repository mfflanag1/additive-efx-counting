# Root-sourced anchor-retaining sacrifice handoff lemma

**Date:** 2026-08-13

**Status:** cap-free elimination of complete-residual-pool payment as a
prerequisite for a root-sourced anchor collision

## Root-sourced collision

Let `X` be the globally maximal base with first-priority root `r`.  In a
post-recruitment protected selected-core state, let

\[
 K_r\subseteq Y_q
\]

be the permanent old root anchor.  Let the root have a current-safe response

\[
 E\subseteq Y_\ell,
 \qquad v_r(E)>v_r(Y_r)\ge v_r(X_r),              \tag{1}

in a different target occupied by selected core `A` of source `a != r`.
After the anchor-target nonoverlap reduction,

\[
 E\cap K_r=\varnothing.                           \tag{2}

Put `J=E intersect A`.  Let the other two represented owners retain their
protected selected cores.  Assume, as supplied by the post-recruitment
protected state, that every represented nonroot source pays every retained
selected-core threshold.

## Sacrificed-owner handoff

Assign

\[
 B_r=K_r\mathbin{\dot\cup}E,                     \tag{3}

retain the other two selected cores, and give the exact complement of these
three bundles in the active owner pool to `a`:

\[
 W=\mathcal P\setminus
 \left(B_r\mathbin{\dot\cup}B_c\mathbin{\dot\cup}B_s\right). \tag{4}

The allocation is physically feasible.  Equation (2) retains the permanent
anchor without duplication; removing `J` from `A` is automatic in the
complement (4); every residual atom not consumed by `E` is also in `W` unless
already assigned to a retained represented bundle.

The root is strictly above the base by (1) and positivity:

\[
 v_r(B_r)>v_r(E)>v_r(X_r).                        \tag{5}

Therefore an EFX allocation in (3)--(4) is a strict fixed-priority
lexicographic improvement even if the displaced source `a` is below every
previous payment floor.  In particular, neither payment from `R_q` nor
payment from the complete residual pool is an entry premise for the move.

## Exact response boundary

All targets except `B_r` and `W` are retained protected cores.  Every
represented owner pays those cores.  The sacrificed owner `a` is
automatically safe against her own residual `W`.  Hence every EFX failure is
one of exactly three forms:

1. `a` strongly envies a retained protected core or the enlarged root target
   `B_r`;
2. a represented source strongly envies `W`; or
3. a represented nonroot source strongly envies the enlarged root target
   `B_r`.

The root cannot fail against an old target: her utility has increased and
those targets are unchanged or shrink.  A failure against `B_r` admits a
globally minimal desired subset of this single new target; a failure against
`W` is the ordinary residual recapture edge.  Thus (3)--(4) enters the
already-recorded sacrificed-owner/two-target response compression rather
than returning to a scalar payment gate.

If `B_r` happens to be protected for every observer, branch 3 disappears
and the state is exactly the standard three-core/one-residual two-sided
star.  Otherwise the sole additional target is the explicitly labeled
anchor-retaining root bundle `K_r+E`; minimal response extraction either
adds a new finite response label or gives an exact recurrence of that label.

## Full-pool capture is diagnostic, not terminal

The complete-pool selector remains a valid optional paid shortcut.  If it
fails, its inequality

\[
 v_a(J)-v_a(\mathcal R_E)
 \ge v_a(A)-F_a>0                                 \tag{6}

explains why `a` loses in (4), but it does not prevent the priority-valid
allocation (3)--(4).  Hence (6) is no longer an independent terminal in the
root-sourced branch.  What remains is termination of the explicitly labeled
root-target/residual response recurrence.

## Claim boundary

This lemma proves physical feasibility, exact anchor retention, root
priority, irrelevance of displaced-owner payment to an EFX endpoint, and
the exhaustive three-form response boundary.  It does not prove that
`K_r+E` is observer-safe, terminate a repeated response to that enlarged
target or the residual, eliminate the anchor/root-critical least-good
certificate, close GG, or prove four-agent/general additive EFX.

