# Root-sourced evolved-target return-or-capture lemma

**Date:** 2026-08-11

**Status:** cap-free conversion of a common-safe root response; termination
of the captured-`B_q` compensation branch remains open

## Anchored residual state

Use the retained-support residual rotation

\[
 D_r=T_q+f,
 \qquad W=B_q+L,
 \qquad R=(T_r\setminus L)+B_r,
\]

where `L` is a nonempty subset of `T_r` and

\[
 v_q(L)>v_q(T_q).
\]

Thus `r` strictly prefers the common-safe root anchor `D_r` to `X_r`, and
`q` strictly prefers the evolved target `W` to `X_q`.  Put

\[
 \delta_q=v_q(W)-v_q(X_q)
          =v_q(L)-v_q(T_q)>0.                       \tag{1}
\]

Suppose the sole evolved-target wall has a **common-safe root response**

\[
 A\subseteq W,
 \qquad v_r(A)>v_r(D_r).                            \tag{2}
\]

The stronger threshold in (2), rather than merely `v_r(A)>v_r(X_r)`, is
available whenever the root is the actual observer creating the wall.

## Anchor-return allocation

Exchange the root response core with the old root anchor:

\[
 Z_r=A,
 \qquad Z_q=(W\setminus A)+D_r,
 \qquad Z_c=X_c,
 \qquad Z_s=X_s,
\]

and retain `R` as charity.  This is a complete reallocation of the same
goods.  The root strictly improves over both `D_r` and her base bundle.  The
later mutual owner has exact gain

\[
 v_q(Z_q)-v_q(X_q)
   =\delta_q+v_q(D_r)-v_q(A).                       \tag{3}
\]

Consequently, if

\[
 v_q(A)-v_q(D_r)<\delta_q,                          \tag{4}
\]

then both mutual owners strictly improve.  The external owners are
unchanged.  Every owner still dominates the charity: for any `ell in L`,
base EFX against `X_r` gives

\[
 v_i(X_i)\ge v_i(X_r-\ell)\ge v_i(R).
\]

The root target `A` is common-safe and the external targets are unchanged.
Hence the only possible EFX wall of `Z` is against the single evolved
target `Z_q`.  The anchor return therefore yields either an EFX flower
improvement or another named response/Hall augmentation; it creates no
unlocalized target or charity wall.

## Exact capture alternative

If the anchor return does not strictly improve `q`, then (3) gives

\[
 v_q(A)-v_q(D_r)\ge\delta_q.                        \tag{5}
\]

In the positive nondegenerate convention equality would make the distinct
bundles `Z_q` and `X_q` equal in `q`'s row, so the inequality is strict.
Substituting (1) and `D_r=T_q+f` into (5) cancels `T_q`:

\[
 v_q(A)>v_q(L)+v_q(f).                              \tag{6}
\]

Write the disjoint support decomposition

\[
 K=A\cap B_q,
 \qquad J=A\cap L.
\]

Because `A` is contained in `B_q+L`, equation (6) is exactly

\[
 v_q(K)>v_q(L\setminus J)+v_q(f).                  \tag{7}
\]

In particular `K` is nonempty.  Thus a failed anchor return cannot remain
an arbitrary root-sourced response: it exposes a root-held packet from
`B_q` whose value to `q` dominates both the entire omitted retained packet
and the charity good.  The support `L` is not restored to the old mutual
core.

## Composition consequence

Every common-safe root response to the evolved target has one of two
outcomes:

1. anchor return pays `q`, giving an EFX improvement or a new response/Hall
   augmentation with only one possible target wall; or
2. a nonempty packet `K subseteq B_q` satisfies the strict capture
   inequality (7).

The second branch is the correct input to an alternating compensation
chain between `K` and the released root anchor `D_r`.  Any successful
exchange returns to branch 1; exhaustion must terminate on `T_q` or `f`,
where the existing top/floater and anchored residual-rotation handoffs
apply.

## Verification and claim boundary

[`root_sourced_evolved_target_return_or_capture_audit.json`](root_sourced_evolved_target_return_or_capture_audit.json)
checks the exact payment identity, the successful-return implication, the
capture cancellation, the nonempty-`B_q` support conclusion, and charity
containment under Z3 5.0.0.

This lemma eliminates an unstructured common-safe root response.  It does
not build the alternating compensation chain for (7), eliminate an unsafe
root wall, close the resulting response/Hall augmentation, close `GG`, or
prove four-agent/general additive EFX.
