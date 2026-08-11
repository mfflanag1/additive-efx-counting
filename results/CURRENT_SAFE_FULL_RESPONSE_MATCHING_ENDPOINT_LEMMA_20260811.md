# Current-safe full-response matching endpoint lemma

**Date:** 2026-08-11

**Status:** cap-free observer-payment closure for a rank-four response
matching at one paid state; mixed old/new response margins remain open

## Full current-response matching

Let `X` be the globally lex-maximal partial EFX base and let `Y` be a paid
splice state:

\[
 v_i(Y_i)\ge v_i(X_i)\qquad(i\in N).              \tag{1}
\]

Suppose four pairwise-disjoint physical cores `A_i`, one for every owner,
satisfy

\[
 v_i(A_i)>v_i(Y_i)                                \tag{2}
\]

and are EFX-safe relative to the same current state:

\[
 \tau_h(A_i)\le v_h(Y_h)
 \qquad(h\in N).                                  \tag{3}
\]

Assign `A_i` to owner `i` and leave every unselected good unallocated.  For
every observer `h` and target `i!=h`,

\[
 \tau_h(A_i)\le v_h(Y_h)<v_h(A_h).                \tag{4}
\]

Thus the resulting partial allocation is EFX.  By (1)--(2), every owner
strictly improves over `X`, so it Pareto dominates—and hence lexicographically
dominates—the globally maximal base.  No separate charity-safety inequality
is needed for this contradiction: EFX constrains allocated owner bundles,
not the union of unallocated goods.

If the exact response/release labels are internally supplied, the same four
edges also give the desired release-compatible connected certificate.  The
EFX conclusion itself only needs disjointness.

## Exact mixed-matching budget

The selected core for owner `h` need not always satisfy (2).  For an arbitrary
rank-four selection put

\[
 m_h=v_h(A_h)-v_h(X_h),
 \qquad
 b_{h i}=\bigl(\tau_h(A_i)-v_h(X_h)\bigr)_+.      \tag{5}

Assuming every `m_h>=0`, the selected allocation is EFX exactly when

\[
 m_h\ge \max_{i\ne h}b_{h i}qquad(h\in N).       \tag{6}

A base-common-safe old edge has `b_{hi}=0`.  A core current-safe at `Y` has

\[
 b_{hi}\le\Delta_h,
 \qquad \Delta_h=v_h(Y_h)-v_h(X_h).               \tag{7}

If `A_h` is itself current-desired then `m_h>Delta_h`, so it pays every
current-safe target automatically.  Therefore failure of (6) can occur only
in a **mixed** matching where some observer `h` receives an older merely
base-desired core with

\[
 m_h<b_{hi}\le\Delta_h                            \tag{8}

for a newer current-safe decorated target `A_i`.

Equation (8) is the exact remaining observer-payment separator.  Replacing
`h`'s edge by a current-desired response raises its own margin above every
current-safe debt in row `h`; the physical target collision created by that
replacement is the charity-hole pivot problem.

## Consequence for the repeated-support bridge

At an exact full signed-transfer state, a rank-four matching made entirely
of current responses closes immediately by (4).  Dynamic edge labels are no
longer relevant.  A surviving return must mix old base responses with new
current responses and exhibit (8).  The universal bridge has therefore been
reduced to one combinatorial operation: pivot every underfunded old source
to a current-desired core while retaining target distinctness, or derive a
release-compatible alternating component from the displaced edges.

## Verification and boundary

[`current_safe_full_response_matching_endpoint_audit.json`](current_safe_full_response_matching_endpoint_audit.json)
checks (4), the exact surplus-budget identity (6), implication (7), automatic
payment by a current-desired assigned core, and the strict mixed separator
symbolically over the rationals.

This lemma does not prove that every rank-four retained matching can be made
entirely current-desired, resolve the mixed separator (8), force the necessary
target-distinct pivots, close the repeated-support theorem, close GG, or prove
four-agent/general additive EFX.
