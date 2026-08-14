# Permanent-anchor full-residual liquidation corollary

**Date:** 2026-08-14

**Status:** cap-free priority-valid probe; complete-EFX continuation remains
open at the nonroot normalization-bypass gate

## Statement

Use the permanent-anchor state

\[
 B_r=Y_r\mathbin{\dot\cup}A,\qquad B_q=Y_q\setminus A,
 \qquad v_r(A)>v_r(X_r),
\]

with nonempty original-root residual `Y_r` and positive singleton charity
good `p`.  For any nonroot owner `i`, form a complete allocation by leaving
the root with `A`, giving all of `Y_r` and `p` to `i`, and leaving every
other anchored bundle unchanged.

Relative to the original current allocation, this uses only

\[
 q\to r:A,\qquad r\to i:Y_r,\qquad charity\to i:p,
\]

after deleting self-pairs and merging coincident pairs.  Hence it uses at
most three physical supplier-recipient pairs, with no packet-size bound.
The root remains strictly above its base coordinate because

\[
                         v_r(A)>v_r(X_r),
\]

and `i` strictly improves relative to the anchored state because valuations
are positive and `Y_r` is nonempty.

## Relation to the bilateral separator

Put

\[
 \delta_r=v_r(B_r)-v_r(X_r).
\]

The strict anchor inequality gives

\[
 v_r(Y_r)=v_r(B_r)-v_r(A)
          <v_r(B_r)-v_r(X_r)=\delta_r.
\]

Thus the bilateral probe with `H=Y_r` and empty compensator automatically
satisfies

\[
                    v_r(H)<\delta_r+v_r(p).
\]

Equivalently, the universal bilateral-failure conclusion
`v_r(H)>=delta_r+v_r(p)` cannot hold when `H=Y_r` is nonempty.  This is
exactly the first probe of
`STRICT_ROOT_SURPLUS_RESET_RETIRE_RETURN_CLOSURE_THEOREM_20260814.md`, not a
new collision theorem.

## Exact claim boundary

If this complete probe is EFX, it is the desired strict-priority endpoint.
If it is not EFX, minimum-response extraction still has to be composed with
the frozen saturation record.  The current imported collision argument does
not cover a nonroot holder whose repeated normalized response avoids the
retired packet; that is the open branch isolated in
`NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md`.

Therefore this corollary eliminates payment, conservation, packet-size, and
edge-count obstruction on the nonempty-residual face.  It does **not** prove
that the probe is EFX, close the normalization bypass, prove the saturated
fixed-`U` theorem, or prove additive EFX.

The canonical rank-three application also requires a careful symbol-level
check that its forced nonempty response into the root lies in the `Y_r`
cell used here.  The graph lemma records such a root-facing response, but
that interface should be checked independently before this corollary is
advertised as covering every frozen target state.
