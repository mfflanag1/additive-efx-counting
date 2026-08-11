# Root-response floater-substitution dichotomy

**Date:** 2026-08-11

**Status:** cap-free reduction of root-return capture to a joint mutual-owner
packet; termination of the joint packet remains open

## Captured root response

Use the root-sourced evolved-target capture branch.  Thus

\[
 D_r=T_q+f,
 \qquad W=B_q+L,
 \qquad A=K+J\subseteq B_q+L,
\]

where

\[
 K=A\cap B_q\ne\varnothing,
 \qquad J=A\cap L,
\]

`A` is a common-safe root response satisfying

\[
 v_r(A)>v_r(D_r)>v_r(X_r),                          \tag{1}
\]

and failed anchor return gives

\[
 v_q(K)>v_q(L\setminus J)+v_q(f).                  \tag{2}
\]

## Floater substitution

Return the captured bottom packet and the old top anchor to `q`, and replace
that packet in the root response by the charity good:

\[
 Z_r=J+f,
 \qquad
 Z_q=T_q+B_q+(L\setminus J)
     =X_q+(L\setminus J),
\]

while fixing `X_c,X_s` and retaining

\[
 R=(T_r\setminus L)+B_r
\]

as charity.  The two displayed targets partition exactly `D_r+W`.

If

\[
 v_r(J+f)\ge v_r(X_r),                              \tag{3}
\]

then nondegeneracy makes the comparison strict because `J+f` and `X_r` are
distinct bundles.  If `L\setminus J` is nonempty, `q` also strictly
improves.  If `J=L`, then `q` receives exactly `X_q`, while the earlier root
strictly improves, already contradicting global lexicographic maximality
once the allocation is EFX.

The root target `J+f` is common-safe because it is a subset of the original
common-safe mutual core `T_r+f`.  The external targets are unchanged, and
base EFX still dominates `R`.  Hence:

1. when `J=L`, every target is common-safe and `Z` is immediately EFX;
2. when `J` is proper in `L`, the sole possible EFX wall is against
   `Z_q=X_q+(L\setminus J)`.

Thus successful floater substitution gives the requested EFX/lex endpoint
or one named response/Hall augmentation.

## Joint packet alternative

If (3) fails, nondegeneracy gives

\[
 v_r(J+f)<v_r(X_r).                                 \tag{4}
\]

Put

\[
 \mu_r(A)=v_r(A)-v_r(X_r)>0.
\]

Using `A=K+J`, equation (4) yields

\[
 v_r(K)-v_r(f)
   =v_r(A)-v_r(J+f)
   >\mu_r(A),
\]

or equivalently

\[
 v_r(K)>v_r(f)+\mu_r(A).                            \tag{5}
\]

Together, (2) and (5) make `K` a simultaneous strict capture packet:

\[
 \begin{aligned}
 v_q(K)&>v_q(L\setminus J)+v_q(f),\\
 v_r(K)&>v_r(f)+\mu_r(A).
 \end{aligned}                                      \tag{6}
\]

The obstruction is therefore no longer an arbitrary unsafe allocation or
root response.  Both mutual owners need the same nonempty physical packet
from the original `B_q`, and in both rows its strict surplus pays for the
charity good.  An external response core disjoint from the full response
`A=K+J` remains available for a disjoint-core selector.  If no such core
exists, `A` is a hitting set for the external family.  Equation (6)
identifies the joint-critical part `K` inside that hitting set, but does not
by itself prove that an intersecting external core meets `K` rather than
`J`.

## Verification and claim boundary

[`root_response_floater_substitution_dichotomy_audit.json`](root_response_floater_substitution_dichotomy_audit.json)
checks support conservation, the `q` improvement, the root-margin
cancellation, both joint-capture inequalities, and the support containment
used by the analytic common-safety argument under Z3 5.0.0.

This lemma converts failed root anchor return into either an EFX/response
endpoint or the joint packet (6).  It does not prove that an external
desired core is disjoint from `A`, force an intersecting core to meet `K`
rather than `J`, eliminate the hitting-set branch, close the subsequent Hall
augmentation, close `GG`, or prove four-agent/general additive EFX.
