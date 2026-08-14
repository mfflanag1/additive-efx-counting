# Liquidated-root response full-source-swap frontier

**Date:** 2026-08-14

**Status:** cap-free repair of the p-augmented root-capture branch; strict
direct-safety and decorated recurrence remain

## Input

Use a liquidated-root probe from
`FIXED_U_LIQUIDATED_ROOT_THREE_PLACEMENT_RESPONSE_FRONTIER_LEMMA_20260814.md`.
Thus the root holds the permanent anchor `A`, a fixed nonroot owner `k`
holds the nonempty original-root cell `Y_r`, and the singleton `p` is parked
at a nonroot owner other than the response source `i`.

Suppose a globally minimum singleton-disjoint response has root target and
core

\[
                         \varnothing\ne E\subseteq A.           \tag{1}
\]

Let the source's original nonroot cell after removing the anchor be

\[
 S_i=\begin{cases}
       Y_q\setminus A,&i=q,\\
       Y_i,&i\ne q.
     \end{cases}                                                  \tag{2}
\]

At the chosen probe the source holds `S_i`, and also `Y_r` when `i=k`.
Because `E` is desired there,

\[
 v_i(E)>v_i(S_i+\mathbf 1_{i=k}Y_r).             \tag{3}
\]

## Full-source swap

Return all of `Y_r` to the root, transfer all of `S_i` to the root, transfer
`E` to source `i`, and give `p` to the root.  The final relevant bundles are

\[
 C_r=(A\setminus E)+Y_r+S_i+p,qquad C_i=E.       \tag{4}
\]

Every other owner retains its original nonroot cell, with the evident
removal of `S_i` from its old holder.  Equation (3) shows that `i` strictly
improves even when `i=k` and therefore releases both `S_i` and `Y_r`.

Relative to the original current allocation, the only possible nonself
supplier pairs are

\[
 q\to r:A\setminus E,qquad q\to i:E,qquad
 i\to r:S_i,qquad charity\to r:p.               \tag{5}

Self-pairs disappear and coincident `q -> r` packets merge.  Hence (4) uses
at most four physical packet-transfer edges, without a packet-size bound.

## Exact root frontier

Put

\[
 B_r=Y_r+A,qquad \delta_r=v_r(B_r)-v_r(X_r)>0.
\]

The root in (4) remains strictly above its base coordinate exactly when

\[
             v_r(E)-v_r(S_i)<\delta_r+v_r(p).     \tag{6}

If (6) holds, (4) is a complete priority-valid at-most-four-edge probe.  If
it is EFX, it is the required endpoint; otherwise it supplies the next
actual decorated response without a floor-reset or collision argument.

Failure of (6) gives

\[
 v_r(S_i)+v_r(p)\le v_r(E)-\delta_r
                  \le v_r(A)-\delta_r
                  =v_r(X_r)-v_r(Y_r)
                  <v_r(X_r).                     \tag{7}

Thus p-augmented root capture is not the final scalar obstruction.  It is
either repaired by the full-source swap or strengthens to the strict
direct-safety wall (7).

## Claim boundary

Proved: source payment, conservation, the four-edge bound, the exact root
condition, and strict direct safety on failure.  Not proved: contradiction
of (7) from the other signed rows, closure of the failed swap's decorated
response, the fixed-U theorem, or additive EFX.
