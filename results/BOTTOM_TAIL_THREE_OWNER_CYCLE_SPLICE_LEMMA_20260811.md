# Bottom-tail three-owner cycle-splice lemma

**Date:** 2026-08-11

**Status:** cap-free endpoint and exact selector for the smallest operation
escaping the support-disjoint bottom plateau; forcing selector feasibility
from all GG inequalities remains open

## Packet geometry

Consider the canonical support-disjoint state in which the root holds
`A+H`, a protected source `q` holds `Q`, and the distinguished external hole
`d` holds residual `W`.  The retained bottom tail `H` is nonempty and is not
used by any selected response core.

Choose

\[
 K\subseteq Q,
 \qquad W=G_r\mathbin{\dot\cup}G_q                 \tag{1}
\]

and allocate

\[
 Y_r=A+G_r,
 \qquad Y_q=(Q\setminus K)+G_q,
 \qquad Y_d=K+H.                                   \tag{2}
\]

Every other owner is unchanged. The supplier graph is

\[
 r\to d:H,
 \qquad d\to r:G_r,
 \qquad d\to q:G_q,
 \qquad q\to d:K.                                 \tag{3}
\]

After isolated zero-packet edges are deleted, any choice changing all three
owners is a connected component. It is the smallest operation that both
releases the already retained bottom tail and compensates its old root,
without restarting the same response compression.

## Exact endpoint selector

Let `C(H,A,Q,W)` be the finite family of triples `(K,G_r,G_q)` satisfying
(1), root-first lexicographic improvement

\[
 v_r(A+G_r)>v_r(X_r),                              \tag{4}
\]

and the observer-indexed surplus conditions of the connected-component
endpoint theorem for (2). An owner below base may instead be placed in `L`
only after directly satisfying every final EFX and charity comparison.

Exactly one of the following occurs.

1. `C(H,A,Q,W)` is nonempty. Then (2) is EFX with charity, strictly
   lexicographically dominates the base in root-first priority, and has the
   connected supplier graph (3).
2. The family is empty. Because all packet supports are finite, every split
   has a named failed inequality: root replacement (4), weak payment for an
   owner outside `L`, one observer-target surplus budget, or one direct
   comparison for an owner in `L`. A globally maximizing split therefore
   supplies an exact separating certificate and identifies which extra
   packet or gain the analytic GG argument must force.

This is stronger than another support counter: it tests the whole branching
operation at once and permits realized gains to pay for unsafe target tails.

## Exact adversarial witness

The eleven-good retained-bottom plateau has canonical state

\[
 (A_r,q,c,W).
\]

Its selector contains the exact allocation

\[
 \begin{aligned}
 Y_r&=\{q1,c2,s1\},\\
 Y_q&=\{c1,s2,f\},\\
 Y_c&=\{q2,h\},\\
 Y_s&=\{r1,r2,k\}.
 \end{aligned}                                     \tag{5}
\]

Relative to the canonical state, (5) uses

\[
 H=\{h\},\quad G_r=\{s1\},\quad G_q=\{c1\},
 \quad K=\{q2\}.                                  \tag{6}
\]

Exact arithmetic verifies that (5) is EFX and that the root strictly beats
her base. Thus the first support-disjoint plateau does not refute the splice;
it demonstrates precisely the four-packet connected repair.

## Consequence and boundary

The live GG obligation is now the **cycle-splice feasibility theorem**:
derive a member of `C(H,A,Q,W)` from the root-concentration, protected-source,
and minimal Hall-defect inequalities, or produce a full-premise positive-
additive state in which every split has an exact separating certificate.

[`bottom_tail_three_owner_cycle_splice_audit.json`](bottom_tail_three_owner_cycle_splice_audit.json)
checks support conservation, connectedness, the generic surplus-budget
endpoint implication, and the exact witness (5)--(6).

This lemma does not prove that `C(H,A,Q,W)` is always nonempty, promote the
local witness to global GG maximality, close the reverse-support branch,
close GG, or prove four-agent/general additive EFX.
