# Parallel-root pivot reduction

**Date:** 2026-08-09

**Status:** cap-free analytic closure of the parallel-root safety recurrence;
residual payment remains

## Setup

Let `E=T+f` be any desired set witnessing a parallel
`p -f-> r` decomposition of
\(X_r=T\mathbin{\dot\cup}B\).  Let `T_q+f` be the selected
desired set on `r -f-> q`.

Absence of a self-`f`-champion at `r`, applied through BCFF Observation
2.10 to this particular decomposition, gives

\[
v_r(T+f)<b_r=v_r(T)+v_r(B),
\]

and hence `v_r(f)<v_r(B)`.  Since `r` desires `T_q+f`,

\[
v_r(T_q)>v_r(T).
\tag{1}
\]

This holds for every valid parallel decomposition, not only the initially
selected one.

## Failed fallback and charity transition

The fallback allocation using `T_q` pays the `r`-tail of `E` whenever

\[
v_r(T_q)\ge\tau_r(E).
\tag{2}
\]

Suppose (2) fails.  Choose a deletion attaining `tau_r(E)`.  By (1), that
deletion cannot remove `f`; it removes a good `g in T`.  Additivity yields

\[
v_r(f)>v_r(g).
\tag{3}
\]

Replace `g` in `X_r` by `f`.  An EFX result would Pareto-improve `r`, so at
global maximality an unsafe deletion exposes a new genuine edge
`k -f-> r`, with desired set `E'` containing `f` and omitting `g` and one
further deletion witness.

Sources `r`, `q`, and `s` route respectively to a forbidden self-champion,
the length-two residual, and one of the already-described swapped
length-three cells.  Only `k=p` stays in the parallel-root recurrence.

## Strict augmented-root potential

Suppose `k=p`.  Both `E` and `E'` are inclusion-minimal desired sets for
`p`.  Desired-set safety of `E` gives

\[
v_p(E-g)\le b_p<v_p(E').
\]

Since `g notin E'`, additivity gives the strict augmented improvement

\[
v_p(E'+g)>v_p(E).
\tag{4}
\]

Thus the new root does not merely replace the old decomposition: returning
the removed pivot creates a strictly increasing `p`-coordinate.

The augmented bundle `E'+g` has only one kind of unresolved safety face.
Deleting `g` leaves `E'`.  If an external agent `i in {r,q,s}` envies
`E'`, then, because `E'` is common-safe, `i` is itself an `f`-champion of
`r` using the `E'` decomposition.  Its source routes exactly as above.
Therefore, in the live parallel-`p` branch, deletion of `g` is safe for
every external observer.

If deleting `z in E'` is unsafe for an external observer at her base
threshold, every inclusion-minimal crossing set in

\[
(E'-z)+g
\tag{5}
\]

must contain `g`: without `g` it lies in a deletion remainder of the
common-safe set `E'`.  Consequently every unresolved recurrence step has
the exact output

\[
g\in A\subseteq(E'-z)+g
\tag{6}
\]

for a base-desired set.  Indeed, a set not containing `g` lies inside the
base-safe deletion remainder `E'-z`, while inclusion-minimality makes every
deletion of `A` base-safe.

This last pivot family routes completely.  Since
`E'+g subseteq X_r+f`, there are two cases.

1. If `f notin A`, then the source of `A` envies a subset of `X_r` and
   therefore envies `X_r` itself.  Source `q` creates the PI cycle
   `q -> r -f-> q`; source `s` creates
   `s -> r -f-> q -> s` in the external-`q` cell; source `r` cannot envy a
   subset of her own bundle.  The recipient `p` is not an external
   observer.
2. If `f in A`, common safety makes its source an `f`-champion of `r` using
   the `A` decomposition.  Source `r` is a forbidden self-champion, source
   `q` enters the length-two residual, and source `s` enters the swapped
   length-three cell routed in the adaptive-singleton theorem.

Thus every pivot-containing safety failure either is already PI or exits to
an explicitly named residual class.  In the branch that remains in the
original length-three cell, `E'+g` is externally safe.

## Consequence

The external-`q` parallel-root recurrence is closed at the safety level.  A
new augmented root strictly raises `p` by (4), and every failure of its
external safety routes to a PI cycle, the swapped length-three cell, or the
length-two residual.  No root cycle or contested safety pivot remains.

The live same-cell obligation is now only to pay `r` from the complement of
the externally safe augmented root while assigning the two singleton goods.
This reduction does not assert that the residual always meets that payment
threshold.

The total-capacity failure has one scalar form.  Write
`E'=T'+f`, \(X_r=T'\mathbin{\dot\cup}B'\); the pivot `g` belongs to `B'`.
The residual
of `E'+g` after reserving the two singleton goods is

\[
U=(B'-g)+X_q.
\tag{7}
\]

Applying (1) to the new parallel root gives `v_r(T_q)>v_r(T')`, and hence

\[
v_r(U)>b_r+v_r(B_q)-v_r(g).
\tag{8}
\]

The established external safety of `E'+g` gives
`tau_r(E'+g)<=b_r`.  Consequently

\[
v_r(U)<\tau_r(E'+g)
\quad\Longrightarrow\quad
v_r(g)>v_r(B_q).
\tag{9}

Thus packet-wide capacity cannot fail diffusely: it fails only when the
single returned pivot outweighs the entire released `q`-bottom packet.
When (9) is false, total `r`-capacity exists and only safety of a minimal
payment remains to be routed.

The four scalar implications (1), (3), (4), and (9) replay independently as
QF_LRA-UNSAT when negated in
[`length_three_parallel_pivot_scalar_audit.json`](length_three_parallel_pivot_scalar_audit.json).
This audit checks the displayed algebra; the champion-source routing remains
the analytic part of the proof.
